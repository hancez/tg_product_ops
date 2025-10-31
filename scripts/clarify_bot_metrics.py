#!/usr/bin/env python3
"""
澄清Bot指标：Hook Generator 83%市场份额 vs Thumbnail Maker消息数
"""

import pymysql
import csv
from datetime import datetime
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

print("=" * 80)
print("🔍 澄清Bot指标口径")
print("=" * 80)
print()

# 8个营销bot
marketing_bot_ids = [
    1965760104392110080,  # Hook_Generator_Bot
    1970046615507873792,  # myshell_thumbmaker_bot
    1972858715723681792,  # BRoll_Generator_Bot
    1974427421370437632,  # XtoVideoScriptTransformer_Bot
    1974701461545680896,  # xPostGenerator_Bot
    1974829619605544960,  # CFLinkedinPostBot
    1975400765027258368,  # Viral_Idea_Spark_Bot
    1975961906457870336   # X_Rival_Analysis_bot
]

# Step 1: 找出营销bot创建者
cursor.execute(f"""
    SELECT id, user_id
    FROM tg2app_tg_bots
    WHERE id IN ({','.join(map(str, marketing_bot_ids))})
""")

marketing_bot_creators = set(row[1] for row in cursor.fetchall())
print(f"营销bot创建者: {marketing_bot_creators}")
print()

# Step 2: 所有使用营销bot的用户（排除创建者）
cursor.execute(f"""
    SELECT DISTINCT user_id
    FROM tg2app_bot_running_messages
    WHERE bot_id IN ({','.join(map(str, marketing_bot_ids))})
""")

all_users = [row[0] for row in cursor.fetchall()]
users_excluding_creators = [u for u in all_users if u not in marketing_bot_creators]

print(f"总用户数（排除创建者）: {len(users_excluding_creators)}")
print()

# Step 3: 找出这些用户中的创建者
cursor.execute(f"""
    SELECT DISTINCT user_id
    FROM tg2app_tg_bots
    WHERE user_id IN ({','.join(map(str, users_excluding_creators))})
""")

bot_creators = [row[0] for row in cursor.fetchall()]
non_creators = [u for u in users_excluding_creators if u not in bot_creators]

print(f"创建者: {len(bot_creators)} (这些是先创建bot后使用营销bot的用户)")
print(f"非创建者: {len(non_creators)} (真正的目标用户)")
print()

print("=" * 80)
print("📊 指标1: 用户覆盖率 (User Coverage)")
print("=" * 80)
print()

# 按bot统计使用过的用户数（非创建者）
cursor.execute(f"""
    SELECT
        tb.id,
        tb.name,
        COUNT(DISTINCT rm.user_id) as unique_users
    FROM tg2app_tg_bots tb
    INNER JOIN tg2app_bot_running_messages rm ON tb.id = rm.bot_id
    WHERE tb.id IN ({','.join(map(str, marketing_bot_ids))})
      AND rm.user_id IN ({','.join(map(str, non_creators))})
    GROUP BY tb.id, tb.name
    ORDER BY unique_users DESC
""")

print("按使用过的非创建者用户数排序:")
print("-" * 80)
user_coverage = {}
for bot_id, name, users in cursor.fetchall():
    user_coverage[bot_id] = users
    pct = users / len(non_creators) * 100
    print(f"  {name:35} {users:3} users ({pct:5.1f}% of 70 non-creators)")

print()

print("=" * 80)
print("📊 指标2: 消息总数 (Total Messages)")
print("=" * 80)
print()

# 按bot统计消息总数（非创建者）
cursor.execute(f"""
    SELECT
        tb.id,
        tb.name,
        COUNT(*) as total_messages
    FROM tg2app_tg_bots tb
    INNER JOIN tg2app_bot_running_messages rm ON tb.id = rm.bot_id
    WHERE tb.id IN ({','.join(map(str, marketing_bot_ids))})
      AND rm.user_id IN ({','.join(map(str, non_creators))})
    GROUP BY tb.id, tb.name
    ORDER BY total_messages DESC
""")

print("按消息总数排序:")
print("-" * 80)
message_totals = {}
for bot_id, name, msgs in cursor.fetchall():
    message_totals[bot_id] = msgs
    print(f"  {name:35} {msgs:5} messages")

print()

print("=" * 80)
print("📊 指标3: 平均每用户消息数 (Avg Messages per User)")
print("=" * 80)
print()

# 计算平均每用户消息数
print("按平均每用户消息数排序:")
print("-" * 80)
avg_msgs = {}
for bot_id in user_coverage.keys():
    if user_coverage[bot_id] > 0:
        avg = message_totals[bot_id] / user_coverage[bot_id]
        avg_msgs[bot_id] = avg

for bot_id, name in sorted(avg_msgs.items(), key=lambda x: x[1], reverse=True):
    cursor.execute(f"""
        SELECT name FROM tg2app_tg_bots WHERE id = {bot_id}
    """)
    bot_name = cursor.fetchone()[0]
    print(f"  {bot_name:35} {avg_msgs[bot_id]:6.1f} msgs/user")

print()

print("=" * 80)
print("📊 澄清：为什么Hook Generator 83%但Thumbnail Maker消息多？")
print("=" * 80)
print()

# 获取Hook Generator和Thumbnail Maker的数据
hook_gen_id = 1965760104392110080
thumb_maker_id = 1970046615507873792

hook_users = user_coverage.get(hook_gen_id, 0)
thumb_users = user_coverage.get(thumb_maker_id, 0)
hook_msgs = message_totals.get(hook_gen_id, 0)
thumb_msgs = message_totals.get(thumb_maker_id, 0)

print(f"Hook_Generator_Bot:")
print(f"  用户数: {hook_users} (占非创建者 {hook_users/len(non_creators)*100:.1f}%)")
print(f"  消息数: {hook_msgs}")
print(f"  平均每用户: {hook_msgs/hook_users if hook_users > 0 else 0:.1f} msgs/user")
print()

print(f"myshell_thumbmaker_bot:")
print(f"  用户数: {thumb_users} (占非创建者 {thumb_users/len(non_creators)*100:.1f}%)")
print(f"  消息数: {thumb_msgs}")
print(f"  平均每用户: {thumb_msgs/thumb_users if thumb_users > 0 else 0:.1f} msgs/user")
print()

print("✅ 结论:")
print(f"  Hook Generator 有 {hook_users/len(non_creators)*100:.1f}% 用户覆盖率 (市场份额)")
print(f"  Thumbnail Maker 有 {thumb_msgs} 条消息总数 (使用频次)")
print()
print("  这两个指标不矛盾:")
print(f"  - Hook Generator 覆盖了更多用户 (广度)")
print(f"  - Thumbnail Maker 单个用户使用更频繁 (深度)")
print()

print("=" * 80)
print("📊 非创建者用户参与度分布")
print("=" * 80)
print()

# 找出最活跃的非创建者用户
cursor.execute(f"""
    SELECT
        user_id,
        bot_id,
        COUNT(*) as msg_count
    FROM tg2app_bot_running_messages
    WHERE bot_id IN ({','.join(map(str, marketing_bot_ids))})
      AND user_id IN ({','.join(map(str, non_creators))})
    GROUP BY user_id, bot_id
    ORDER BY msg_count DESC
    LIMIT 10
""")

print("Top 10 最活跃的非创建者用户:")
print("-" * 80)
for user_id, bot_id, msg_count in cursor.fetchall():
    cursor.execute(f"SELECT name FROM tg2app_tg_bots WHERE id = {bot_id}")
    bot_name = cursor.fetchone()[0]
    print(f"  User {user_id}: {msg_count:4} msgs to {bot_name}")

print()

cursor.close()
conn.close()
