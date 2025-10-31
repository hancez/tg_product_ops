#!/usr/bin/env python3
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

print("1. Finding bot-related tables...")
cursor.execute("SHOW TABLES")
all_tables = [t[0] for t in cursor.fetchall()]
bot_tables = [t for t in all_tables if 'bot' in t.lower() or 'tg' in t.lower()]
print(f"Found {len(bot_tables)} tables")
for t in sorted(bot_tables)[:20]:
    print(f"  - {t}")

print("\n2. Finding all bots...")
cursor.execute("SELECT id, name FROM tg2app_tg_bots ORDER BY id LIMIT 30")
bots = cursor.fetchall()
for bot_id, name in bots:
    print(f"  {bot_id}: {name}")

print("\n3. Checking for remix in messages...")
cursor.execute("""
    SELECT COUNT(*) as cnt, COUNT(DISTINCT user_id) as users
    FROM tg2app_bot_running_messages
    WHERE raw_text LIKE '%remix%'
""")
cnt, users = cursor.fetchone()
print(f"  Messages with 'remix': {cnt}, Users: {users}")

print("\nDone!")
cursor.close()
conn.close()
