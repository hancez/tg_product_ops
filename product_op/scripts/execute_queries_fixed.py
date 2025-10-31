#!/usr/bin/env python3
"""
Bot User Behavior Analysis - Fixed SQL Queries
"""

import os
import csv
import pymysql
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
output_dir = "analysis_results_20251028_153847"  # Use same directory

print("🔧 Fixing failed queries...\n")

# Query 3: Per-User Statistics (FIXED - corrected column name to created_date)
print("Query 3: Per-User Message Statistics (Fixed)")
query3 = """
SELECT
    t1.user_id,
    tb.name as bot_name,
    COUNT(*) as total_messages,
    MIN(t1.created_date) as first_message_time,
    MAX(t1.created_date) as last_message_time,
    TIMESTAMPDIFF(DAY, MIN(t1.created_date), MAX(t1.created_date)) as usage_span_days
FROM tg2app_bot_running_messages t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
WHERE t1.bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
GROUP BY t1.user_id, t1.bot_id, tb.name
ORDER BY total_messages DESC
"""

try:
    cursor.execute(query3)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    print(f"  ✅ Success: {len(results)} rows")

    with open(f"{output_dir}/q3_user_stats.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)
    print(f"  💾 Saved to: {output_dir}/q3_user_stats.csv")
except Exception as e:
    print(f"  ❌ Failed: {e}")

print()

# Query 4: High Engagement Users (FIXED - corrected column name to created_date)
print("Query 4: High Engagement Users (Fixed)")
query4 = """
SELECT
    t1.user_id,
    tb.name as bot_name,
    COUNT(*) as message_count,
    TIMESTAMPDIFF(DAY, MIN(t1.created_date), MAX(t1.created_date)) as usage_span_days
FROM tg2app_bot_running_messages t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
WHERE t1.bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
GROUP BY t1.user_id, t1.bot_id, tb.name
HAVING message_count >= 100
ORDER BY message_count DESC
"""

try:
    cursor.execute(query4)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    print(f"  ✅ Success: {len(results)} rows")

    with open(f"{output_dir}/q4_high_engagement.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)
    print(f"  💾 Saved to: {output_dir}/q4_high_engagement.csv")
except Exception as e:
    print(f"  ❌ Failed: {e}")

print()

# Bonus Query: Bot usage breakdown per user
print("Bonus Query: Which bots do Power Users use?")
query_bonus = """
SELECT
    t1.user_id,
    tb.name as bot_name,
    COUNT(*) as message_count
FROM tg2app_bot_running_messages t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
WHERE t1.user_id IN (
    36879844, 38410758, 38410475, 39230842, 38988493,
    38945267, 36878910, 36880251, 330325
)
AND t1.bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
GROUP BY t1.user_id, t1.bot_id, tb.name
ORDER BY t1.user_id, message_count DESC
"""

try:
    cursor.execute(query_bonus)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    print(f"  ✅ Success: {len(results)} rows")

    with open(f"{output_dir}/q5_power_user_bots.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)
    print(f"  💾 Saved to: {output_dir}/q5_power_user_bots.csv")
except Exception as e:
    print(f"  ❌ Failed: {e}")

cursor.close()
conn.close()

print("\n✨ All queries complete!")
