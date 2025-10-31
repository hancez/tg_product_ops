#!/usr/bin/env python3
"""
Deep exploration of database schema to find all relevant tables for funnel analysis
"""

import pymysql

def load_env():
    env_vars = {}
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

env = load_env()
conn = pymysql.connect(
    host=env['DB_HOST'],
    port=int(env.get('DB_PORT', 3306)),
    user=env['DB_USER'],
    password=env['DB_PASS'],
    database=env['DB_NAME']
)

cursor = conn.cursor()

print("=" * 80)
print("🔍 COMPREHENSIVE DATABASE EXPLORATION FOR FUNNEL ANALYSIS")
print("=" * 80)
print()

# 1. Find all tables with 'bot' in name
print("📊 STEP 1: Finding all bot-related tables")
print("-" * 80)
cursor.execute("SHOW TABLES")
all_tables = [t[0] for t in cursor.fetchall()]
bot_tables = [t for t in all_tables if 'bot' in t.lower() or 'tg' in t.lower()]

print(f"Found {len(bot_tables)} bot/telegram related tables:\n")
for table in sorted(bot_tables):
    try:
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        count = cursor.fetchone()[0]
        print(f"  ✅ {table:50} {count:>10,} rows")
    except Exception as e:
        print(f"  ❌ {table:50} (no access)")

print("\n" + "=" * 80)
print("📊 STEP 2: Finding ShellAgent bot ID")
print("-" * 80)

# ShellAgent should be in tg2app_tg_bots table
try:
    cursor.execute("""
        SELECT id, name, description
        FROM tg2app_tg_bots
        WHERE name LIKE '%shell%agent%'
           OR name LIKE '%generate%'
           OR name LIKE '%builder%'
           OR id IN (
               -- Try to find the generation bot from webhook patterns
               SELECT DISTINCT bot_id
               FROM tg2app_bot_running_messages
               LIMIT 1
           )
        ORDER BY name
    """)
    results = cursor.fetchall()

    if results:
        print("Possible ShellAgent bots found:\n")
        for bot_id, name, desc in results:
            desc_preview = (desc[:100] + '...') if desc and len(desc) > 100 else desc
            print(f"  ID: {bot_id}")
            print(f"  Name: {name}")
            print(f"  Desc: {desc_preview}")
            print()
    else:
        print("⚠️  No obvious ShellAgent bot found in tg2app_tg_bots")
        print("    Let's check all bots to identify it manually...")

        cursor.execute("""
            SELECT id, name
            FROM tg2app_tg_bots
            ORDER BY id
            LIMIT 20
        """)
        all_bots = cursor.fetchall()
        print("\nFirst 20 bots in system:")
        for bot_id, name in all_bots:
            print(f"  {bot_id}: {name}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 STEP 3: Checking for remix/creation tracking tables")
print("-" * 80)

check_tables = [
    'tg2app_bot_remix_relations',
    'tg2app_user_bots',
    'tg2app_bot_creation',
    'tg2app_user_created_bots',
    'user_bots',
    'bot_remix',
    'bot_creation_log'
]

print("Checking known table names:\n")
for table in check_tables:
    if table in all_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table}: {count:,} rows")

            # Get schema
            cursor.execute(f"DESCRIBE `{table}`")
            columns = cursor.fetchall()
            print(f"     Columns: {', '.join([c[0] for c in columns[:5]])}")
            if len(columns) > 5:
                print(f"              ... and {len(columns) - 5} more")
            print()
        except Exception as e:
            print(f"  ⚠️  {table}: exists but no access ({str(e)[:50]})")
    else:
        print(f"  ❌ {table}: does not exist")

print("\n" + "=" * 80)
print("📊 STEP 4: Analyzing tg2app_bot_running_messages for clues")
print("-" * 80)

# Find most used bots (excluding the 8 content creator bots)
content_bot_ids = [
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
]

try:
    cursor.execute(f"""
        SELECT
            t1.bot_id,
            tb.name as bot_name,
            COUNT(DISTINCT t1.user_id) as unique_users,
            COUNT(*) as total_messages
        FROM tg2app_bot_running_messages t1
        LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
        WHERE t1.bot_id NOT IN ({','.join(map(str, content_bot_ids))})
        GROUP BY t1.bot_id, tb.name
        HAVING unique_users >= 10
        ORDER BY unique_users DESC
        LIMIT 20
    """)

    other_bots = cursor.fetchall()
    print("Top 20 other bots by user count (excluding our 8 content bots):\n")
    print(f"{'Bot ID':20} {'Name':40} {'Users':>10} {'Messages':>12}")
    print("-" * 85)
    for bot_id, name, users, messages in other_bots:
        name_display = (name[:37] + '...') if name and len(name) > 40 else (name or 'NULL')
        print(f"{str(bot_id):20} {name_display:40} {users:>10,} {messages:>12,}")

    print("\n💡 The bot with most users is likely ShellAgent (the generation bot)")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 STEP 5: Looking for remix commands in messages")
print("-" * 80)

try:
    cursor.execute("""
        SELECT
            COUNT(*) as remix_count,
            COUNT(DISTINCT user_id) as unique_users
        FROM tg2app_bot_running_messages
        WHERE (raw_text LIKE '%/remix%' OR raw_text LIKE '%remix%')
          AND src = 'send'
    """)

    remix_count, remix_users = cursor.fetchone()
    print(f"Messages containing 'remix': {remix_count:,}")
    print(f"Unique users who mentioned remix: {remix_users:,}")

    if remix_count > 0:
        print("\nSample remix messages:")
        cursor.execute("""
            SELECT user_id, bot_id, raw_text, created_date
            FROM tg2app_bot_running_messages
            WHERE (raw_text LIKE '%/remix%' OR raw_text LIKE '%remix%')
              AND src = 'send'
            ORDER BY created_date DESC
            LIMIT 10
        """)

        samples = cursor.fetchall()
        for user_id, bot_id, text, created in samples:
            text_preview = (text[:80] + '...') if text and len(text) > 80 else text
            print(f"  User {user_id} → Bot {bot_id}: {text_preview}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 STEP 6: Checking if raw_text is accessible (for content analysis)")
print("-" * 80)

try:
    cursor.execute("""
        SELECT user_id, bot_id, src,
               CASE
                   WHEN raw_text IS NULL THEN '[NULL]'
                   WHEN raw_text = '' THEN '[EMPTY]'
                   ELSE LEFT(raw_text, 50)
               END as text_preview
        FROM tg2app_bot_running_messages
        WHERE bot_id IN ({})
        ORDER BY created_date DESC
        LIMIT 10
    """.format(','.join(map(str, content_bot_ids))))

    samples = cursor.fetchall()
    print("Sample messages from our 8 content bots:\n")

    has_text = False
    for user_id, bot_id, src, text in samples:
        print(f"  User {user_id}, Bot {bot_id}, {src}: {text}")
        if text and text not in ['[NULL]', '[EMPTY]']:
            has_text = True

    if has_text:
        print("\n✅ raw_text is accessible! Can analyze conversation content")
    else:
        print("\n⚠️  raw_text seems to be NULL/empty for these samples")

except Exception as e:
    print(f"❌ Error: {e}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("✨ Exploration complete!")
print("=" * 80)
