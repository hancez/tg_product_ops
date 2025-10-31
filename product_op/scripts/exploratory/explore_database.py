#!/usr/bin/env python3
"""
Explore database structure to find accessible tables
"""

import pymysql
import os

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

print("🔍 Exploring database structure...\n")

# Try to list tables
print("=" * 60)
print("Attempting to list tables...")
print("=" * 60)

try:
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"✅ Found {len(tables)} tables:\n")
    for table in tables[:50]:  # Show first 50
        print(f"  - {table[0]}")
    if len(tables) > 50:
        print(f"  ... and {len(tables) - 50} more")
except Exception as e:
    print(f"❌ Cannot list tables: {e}")

print("\n" + "=" * 60)
print("Searching for bot-related tables...")
print("=" * 60)

# Search for tables with 'bot' or 'tg' in name
try:
    cursor.execute("SHOW TABLES")
    all_tables = [t[0] for t in cursor.fetchall()]
    bot_tables = [t for t in all_tables if 'bot' in t.lower() or 'tg' in t.lower() or 'telegram' in t.lower()]

    if bot_tables:
        print(f"✅ Found {len(bot_tables)} bot/telegram related tables:\n")
        for table in bot_tables:
            print(f"  📊 {table}")

            # Try to get row count
            try:
                cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
                count = cursor.fetchone()[0]
                print(f"     Rows: {count:,}")
            except Exception as e:
                print(f"     (Cannot access: {str(e)[:50]})")

            # Try to get column info
            try:
                cursor.execute(f"DESCRIBE `{table}`")
                columns = cursor.fetchall()
                print(f"     Columns: {', '.join([c[0] for c in columns[:5]])}")
                if len(columns) > 5:
                    print(f"              ... and {len(columns) - 5} more")
            except:
                pass

            print()
    else:
        print("❌ No bot/telegram related tables found")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("Checking specific table names mentioned in documentation...")
print("=" * 60)

check_tables = [
    'tg2app_bot_running_messages',
    'tg2app_tg_bots',
    'tg2app_bot_messages',
    'tg2app_bot_remix_relations',
    'bot_running_messages',
    'tg_bots',
    'bot_messages'
]

for table in check_tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        count = cursor.fetchone()[0]
        print(f"✅ {table}: {count:,} rows")
    except Exception as e:
        print(f"❌ {table}: {str(e)[:80]}")

cursor.close()
conn.close()

print("\n" + "=" * 60)
print("Exploration complete!")
print("=" * 60)
