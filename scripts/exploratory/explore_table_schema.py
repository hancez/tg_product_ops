#!/usr/bin/env python3
"""
Explore tg2app_bot_running_messages table schema to find timestamp columns
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

print("🔍 Exploring tg2app_bot_running_messages table schema...\n")
print("=" * 70)

# Get full table structure
cursor.execute("DESCRIBE tg2app_bot_running_messages")
columns = cursor.fetchall()

print(f"📊 Found {len(columns)} columns:\n")
for col in columns:
    field, type_, null, key, default, extra = col
    print(f"  {field:30} {type_:20} {f'NULL: {null}':12} {f'Key: {key}':10}")

print("\n" + "=" * 70)
print("🕒 Looking for timestamp-related columns...\n")

timestamp_cols = [col for col in columns if any(
    keyword in col[0].lower()
    for keyword in ['time', 'date', 'created', 'updated', 'timestamp']
)]

if timestamp_cols:
    print(f"✅ Found {len(timestamp_cols)} timestamp columns:\n")
    for col in timestamp_cols:
        print(f"  📅 {col[0]:30} {col[1]}")
else:
    print("❌ No obvious timestamp columns found")

print("\n" + "=" * 70)
print("📊 Sample data from table (first 3 rows)...\n")

cursor.execute("""
    SELECT *
    FROM tg2app_bot_running_messages
    WHERE bot_id = 1965760104392110080
    LIMIT 3
""")

sample_rows = cursor.fetchall()
col_names = [desc[0] for desc in cursor.description]

print(f"Columns: {', '.join(col_names)}\n")
for i, row in enumerate(sample_rows, 1):
    print(f"Row {i}:")
    for col_name, value in zip(col_names, row):
        if value is not None and len(str(value)) < 100:
            print(f"  {col_name}: {value}")

cursor.close()
conn.close()

print("\n" + "=" * 70)
print("✨ Schema exploration complete!")
