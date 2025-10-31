#!/usr/bin/env python3
"""
Find who created these 8 content bots and analyze creation patterns
"""

import pymysql
import csv
from datetime import datetime

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
print("🔍 FINDING BOT CREATORS & CREATION PATTERNS")
print("=" * 80)
print()

# The 8 content creator bots
content_bot_ids = [
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
]

print("📊 QUERY 1: Bot ownership from tg2app_tg_bots")
print("-" * 80)

try:
    cursor.execute(f"""
        SELECT id, name, user_id, created_date, updated_date
        FROM tg2app_tg_bots
        WHERE id IN ({','.join(map(str, content_bot_ids))})
        ORDER BY id
    """)

    bot_owners = cursor.fetchall()
    print(f"Found {len(bot_owners)} bots:\n")

    owner_ids = set()
    for bot_id, name, user_id, created, updated in bot_owners:
        print(f"Bot {bot_id}: {name}")
        print(f"  Owner user_id: {user_id}")
        print(f"  Created: {created}")
        print()
        if user_id:
            owner_ids.add(user_id)

    print(f"Total unique owners: {len(owner_ids)}")
    print(f"Owner IDs: {owner_ids}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 QUERY 2: Checking tg2app_bot_user_relations")
print("-" * 80)

try:
    cursor.execute("DESCRIBE tg2app_bot_user_relations")
    columns = cursor.fetchall()
    print("Table structure:")
    for col in columns:
        print(f"  {col[0]:30} {col[1]:20}")

    # Check relationships for our bots
    cursor.execute(f"""
        SELECT bot_id, user_id, relation_type, created_date
        FROM tg2app_bot_user_relations
        WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
        ORDER BY bot_id, created_date
    """)

    relations = cursor.fetchall()
    print(f"\nFound {len(relations)} user-bot relationships:\n")

    for bot_id, user_id, rel_type, created in relations:
        cursor.execute("SELECT name FROM tg2app_tg_bots WHERE id = %s", (bot_id,))
        bot_name = cursor.fetchone()[0] if cursor.rowcount > 0 else "Unknown"
        print(f"Bot {bot_id} ({bot_name}): User {user_id}, Type: {rel_type}, Created: {created}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 QUERY 3: Find users who created bots (any bots)")
print("-" * 80)

try:
    cursor.execute("""
        SELECT user_id, COUNT(DISTINCT id) as bot_count
        FROM tg2app_tg_bots
        WHERE user_id IS NOT NULL
        GROUP BY user_id
        HAVING bot_count >= 1
        ORDER BY bot_count DESC
        LIMIT 20
    """)

    bot_creators = cursor.fetchall()
    print(f"Top 20 users by number of bots created:\n")
    print(f"{'User ID':15} {'Bots Created':>15}")
    print("-" * 35)
    for user_id, bot_count in bot_creators:
        print(f"{str(user_id):15} {bot_count:>15}")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 QUERY 4: Users who use our 8 bots AND also created bots")
print("-" * 80)

try:
    cursor.execute(f"""
        SELECT DISTINCT
            bot_users.user_id,
            bot_users.bot_count as bots_used,
            bot_users.total_messages,
            COALESCE(bot_creators.bots_created, 0) as bots_created
        FROM (
            -- Users who use our 8 content bots
            SELECT
                user_id,
                COUNT(DISTINCT bot_id) as bot_count,
                COUNT(*) as total_messages
            FROM tg2app_bot_running_messages
            WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
            GROUP BY user_id
        ) bot_users
        LEFT JOIN (
            -- Users who created bots
            SELECT user_id, COUNT(*) as bots_created
            FROM tg2app_tg_bots
            WHERE user_id IS NOT NULL
            GROUP BY user_id
        ) bot_creators ON bot_users.user_id = bot_creators.user_id
        WHERE bot_creators.bots_created > 0
        ORDER BY bot_creators.bots_created DESC, bot_users.bot_count DESC
    """)

    overlap = cursor.fetchall()
    print(f"Users who both USE our bots AND CREATED bots: {len(overlap)}\n")

    if overlap:
        print(f"{'User ID':15} {'Bots Used':>12} {'Messages':>12} {'Bots Created':>15}")
        print("-" * 60)
        for user_id, used, msgs, created in overlap:
            print(f"{str(user_id):15} {used:>12} {msgs:>12} {created:>15}")

        # Save to CSV
        output_dir = "funnel_analysis_" + datetime.now().strftime('%Y%m%d')
        import os
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/users_who_use_and_create.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'bots_used', 'messages', 'bots_created'])
            writer.writerows(overlap)
        print(f"\n💾 Saved to {output_dir}/users_who_use_and_create.csv")
    else:
        print("⚠️  NO users both use our 8 bots AND created their own bots!")
        print("     This means 0% conversion from bot users to bot creators!")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 QUERY 5: Check tg2app_user_current_bot_ids (active bot tracking)")
print("-" * 80)

try:
    cursor.execute("DESCRIBE tg2app_user_current_bot_ids")
    columns = cursor.fetchall()
    print("Table structure:")
    for col in columns:
        print(f"  {col[0]:30} {col[1]:20}")

    cursor.execute("SELECT COUNT(*) FROM tg2app_user_current_bot_ids")
    count = cursor.fetchone()[0]
    print(f"\nTotal rows: {count:,}")

    cursor.execute("""
        SELECT user_id, bot_id, created_date
        FROM tg2app_user_current_bot_ids
        ORDER BY created_date DESC
        LIMIT 20
    """)

    current_bots = cursor.fetchall()
    print("\nLatest 20 user-bot assignments:")
    for user_id, bot_id, created in current_bots:
        print(f"  User {user_id}: Bot {bot_id}, Set at {created}")

except Exception as e:
    print(f"❌ Error: {e}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("✨ Analysis complete!")
print("=" * 80)
