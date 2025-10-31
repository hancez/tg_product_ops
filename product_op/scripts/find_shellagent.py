#!/usr/bin/env python3
"""
Find the real ShellAgent generation bot
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

print("🔍 Finding ShellAgent Generation Bot\n")
print("=" * 80)

# Method 1: Search by name
print("Method 1: Searching by name patterns...")
cursor.execute("""
    SELECT id, name, description
    FROM tg2app_tg_bots
    WHERE name LIKE '%shell%agent%'
       OR name LIKE '%ShellAgent%'
       OR name LIKE '%generate%bot%'
       OR name LIKE '%builder%'
    ORDER BY name
""")

candidates = cursor.fetchall()
print(f"Found {len(candidates)} candidates:\n")
for bot_id, name, desc in candidates:
    desc_preview = (desc[:80] + '...') if desc and len(desc) > 80 else (desc or 'N/A')
    print(f"  {bot_id}: {name}")
    print(f"    Description: {desc_preview}\n")

# Method 2: Look for bots with most users (likely ShellAgent)
print("\n" + "=" * 80)
print("Method 2: Bots with most users (100+ users)...\n")

content_bot_ids = [
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
]

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
    HAVING unique_users >= 100
    ORDER BY unique_users DESC
    LIMIT 20
""")

top_bots = cursor.fetchall()
print(f"{'Bot ID':20} {'Name':40} {'Users':>10} {'Messages':>12}")
print("-" * 85)
for bot_id, name, users, messages in top_bots:
    name_display = (name[:37] + '...') if name and len(name) > 40 else (name or 'NULL')
    print(f"{str(bot_id):20} {name_display:40} {users:>10,} {messages:>12,}")

# Method 3: Check specific bot IDs mentioned in CLAUDE.md documentation
print("\n" + "=" * 80)
print("Method 3: Checking documented bot IDs from CLAUDE.md...\n")

# From CLAUDE.md, the generation bot should be the one users talk to for creating bots
# Let's check if there's a tg2app_tg_users or similar table

cursor.execute("SHOW TABLES LIKE '%user%'")
user_tables = cursor.fetchall()
print("Tables with 'user' in name:")
for table in user_tables:
    print(f"  - {table[0]}")

# Check tg2app_bot_user_relations if it exists
print("\n" + "=" * 80)
print("Method 4: Checking bot_user_relations table...\n")

try:
    cursor.execute("DESCRIBE tg2app_bot_user_relations")
    columns = cursor.fetchall()
    print("tg2app_bot_user_relations structure:")
    for col in columns:
        print(f"  {col[0]:30} {col[1]:20}")

    cursor.execute("""
        SELECT bot_id, COUNT(DISTINCT user_id) as user_count
        FROM tg2app_bot_user_relations
        GROUP BY bot_id
        HAVING user_count >= 50
        ORDER BY user_count DESC
        LIMIT 10
    """)

    relations = cursor.fetchall()
    print("\nBots with most user relationships:")
    for bot_id, count in relations:
        cursor.execute("SELECT name FROM tg2app_tg_bots WHERE id = %s", (bot_id,))
        name = cursor.fetchone()[0] if cursor.rowcount > 0 else "Unknown"
        print(f"  {bot_id}: {name} ({count} users)")

except Exception as e:
    print(f"  Table not accessible or doesn't exist: {e}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("✨ Search complete!")
