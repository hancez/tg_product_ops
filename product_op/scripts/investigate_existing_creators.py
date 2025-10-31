#!/usr/bin/env python3
"""
深入调查：10个"先创建bot后使用营销bot"的用户
目的：理解他们是谁，创建了什么bot，为什么会来使用营销bot
"""

import pymysql
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

print("=" * 100)
print("🔍 深入调查：10个现有创作者")
print("=" * 100)
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

# Step 1: 获取营销bot创建者
cursor.execute(f"""
    SELECT DISTINCT user_id
    FROM tg2app_tg_bots
    WHERE id IN ({','.join(map(str, marketing_bot_ids))})
""")
marketing_bot_creators = set(row[0] for row in cursor.fetchall())

# Step 2: 获取所有使用营销bot的用户
cursor.execute(f"""
    SELECT DISTINCT user_id
    FROM tg2app_bot_running_messages
    WHERE bot_id IN ({','.join(map(str, marketing_bot_ids))})
""")
all_users = [row[0] for row in cursor.fetchall()]
users_excluding_creators = [u for u in all_users if u not in marketing_bot_creators]

# Step 3: 找出创建了bot的用户
cursor.execute(f"""
    SELECT DISTINCT user_id
    FROM tg2app_tg_bots
    WHERE user_id IN ({','.join(map(str, users_excluding_creators))})
""")
bot_creators = [row[0] for row in cursor.fetchall()]

# Step 4: Timeline分析 - 找出先创建bot后使用营销bot的用户
cursor.execute(f"""
    SELECT
        u.user_id,
        u.first_usage,
        c.first_creation,
        TIMESTAMPDIFF(HOUR, u.first_usage, c.first_creation) as hours_to_conversion
    FROM (
        SELECT
            user_id,
            MIN(created_date) as first_usage
        FROM tg2app_bot_running_messages
        WHERE bot_id IN ({','.join(map(str, marketing_bot_ids))})
          AND user_id IN ({','.join(map(str, bot_creators))})
        GROUP BY user_id
    ) u
    INNER JOIN (
        SELECT
            user_id,
            MIN(created_date) as first_creation
        FROM tg2app_tg_bots
        WHERE user_id IN ({','.join(map(str, bot_creators))})
        GROUP BY user_id
    ) c ON u.user_id = c.user_id
    WHERE TIMESTAMPDIFF(HOUR, u.first_usage, c.first_creation) < 0
    ORDER BY hours_to_conversion
""")

existing_creators = [row[0] for row in cursor.fetchall()]

print(f"找到 {len(existing_creators)} 位现有创作者（先创建bot后使用营销bot）")
print()

# Step 5: 详细分析每个现有创作者
for idx, user_id in enumerate(existing_creators, 1):
    print("=" * 100)
    print(f"现有创作者 #{idx}: User {user_id}")
    print("=" * 100)

    # 5.1 他们创建的bot
    cursor.execute(f"""
        SELECT
            id,
            name,
            created_date,
            DATEDIFF(NOW(), created_date) as days_ago
        FROM tg2app_tg_bots
        WHERE user_id = {user_id}
        ORDER BY created_date
    """)

    bots = cursor.fetchall()
    print(f"\n📊 创建了 {len(bots)} 个bot:")
    print("-" * 100)
    for bot_id, name, created, days_ago in bots:
        print(f"  - {name}")
        print(f"    ID: {bot_id}")
        print(f"    创建于: {created} ({days_ago}天前)")

    # 5.2 检查是否创建了营销类bot（名字类似）
    marketing_keywords = ['hook', 'thumbnail', 'broll', 'video', 'script', 'post', 'linkedin', 'viral', 'idea', 'analysis']
    marketing_like_bots = []
    for bot_id, name, created, days_ago in bots:
        if any(keyword in name.lower() for keyword in marketing_keywords):
            marketing_like_bots.append((bot_id, name))

    if marketing_like_bots:
        print(f"\n⚠️  发现 {len(marketing_like_bots)} 个营销类bot:")
        for bot_id, name in marketing_like_bots:
            print(f"  - {name} (ID: {bot_id})")

    # 5.3 使用了哪些营销bot
    cursor.execute(f"""
        SELECT
            tb.id,
            tb.name,
            COUNT(*) as msg_count,
            MIN(rm.created_date) as first_use,
            MAX(rm.created_date) as last_use
        FROM tg2app_bot_running_messages rm
        INNER JOIN tg2app_tg_bots tb ON rm.bot_id = tb.id
        WHERE rm.user_id = {user_id}
          AND rm.bot_id IN ({','.join(map(str, marketing_bot_ids))})
        GROUP BY tb.id, tb.name
        ORDER BY first_use
    """)

    marketing_usage = cursor.fetchall()
    print(f"\n📈 使用了 {len(marketing_usage)} 个营销bot:")
    print("-" * 100)
    for bot_id, name, msg_count, first_use, last_use in marketing_usage:
        print(f"  - {name}: {msg_count}条消息")
        print(f"    首次使用: {first_use}")
        print(f"    最后使用: {last_use}")

    # 5.4 Timeline对比
    cursor.execute(f"""
        SELECT MIN(created_date) as first_bot_creation
        FROM tg2app_tg_bots
        WHERE user_id = {user_id}
    """)
    first_bot_creation = cursor.fetchone()[0]

    cursor.execute(f"""
        SELECT MIN(created_date) as first_marketing_use
        FROM tg2app_bot_running_messages
        WHERE user_id = {user_id}
          AND bot_id IN ({','.join(map(str, marketing_bot_ids))})
    """)
    first_marketing_use = cursor.fetchone()[0]

    hours_diff = (first_marketing_use - first_bot_creation).total_seconds() / 3600
    days_diff = hours_diff / 24

    print(f"\n⏱️  Timeline:")
    print("-" * 100)
    print(f"  首次创建bot: {first_bot_creation}")
    print(f"  首次使用营销bot: {first_marketing_use}")
    print(f"  时间差: {days_diff:.1f}天 (先创建了{abs(days_diff):.1f}天后才使用营销bot)")

    # 5.5 使用其他用户的bot吗？
    cursor.execute(f"""
        SELECT DISTINCT
            tb.id,
            tb.name,
            tb.user_id as creator_id,
            COUNT(*) as msg_count
        FROM tg2app_bot_running_messages rm
        INNER JOIN tg2app_tg_bots tb ON rm.bot_id = tb.id
        WHERE rm.user_id = {user_id}
          AND tb.user_id != {user_id}
          AND tb.id NOT IN ({','.join(map(str, marketing_bot_ids))})
        GROUP BY tb.id, tb.name, tb.user_id
        HAVING COUNT(*) > 5
        ORDER BY msg_count DESC
        LIMIT 10
    """)

    other_bots = cursor.fetchall()
    if other_bots:
        print(f"\n🔄 使用了其他创作者的bot:")
        print("-" * 100)
        for bot_id, name, creator_id, msg_count in other_bots:
            is_in_list = creator_id in existing_creators
            marker = "⭐ (在10人名单中)" if is_in_list else ""
            print(f"  - {name} (created by User {creator_id}) {marker}")
            print(f"    消息数: {msg_count}")
    else:
        print(f"\n✅ 没有使用其他创作者的bot（或使用很少）")

    print()

# Step 6: 分析这10人是否互相使用彼此的bot
print("=" * 100)
print("🔗 群体分析：这10人是否互相使用彼此的bot？")
print("=" * 100)
print()

# 构建互相使用矩阵
usage_matrix = {}
for user_id in existing_creators:
    cursor.execute(f"""
        SELECT DISTINCT tb.user_id as creator_id
        FROM tg2app_bot_running_messages rm
        INNER JOIN tg2app_tg_bots tb ON rm.bot_id = tb.id
        WHERE rm.user_id = {user_id}
          AND tb.user_id IN ({','.join(map(str, existing_creators))})
          AND tb.user_id != {user_id}
    """)

    creators_used = [row[0] for row in cursor.fetchall()]
    if creators_used:
        usage_matrix[user_id] = creators_used

if usage_matrix:
    print("发现互相使用关系:")
    print("-" * 100)
    for user_id, creators_used in usage_matrix.items():
        print(f"  User {user_id} 使用了以下人的bot: {creators_used}")
else:
    print("✅ 这10人之间没有互相使用彼此bot的关系")

print()

# Step 7: 检查他们的bot创建时间是否集中
print("=" * 100)
print("📅 Bot创建时间分析")
print("=" * 100)
print()

cursor.execute(f"""
    SELECT
        user_id,
        MIN(created_date) as first_bot,
        MAX(created_date) as last_bot,
        COUNT(*) as bot_count
    FROM tg2app_tg_bots
    WHERE user_id IN ({','.join(map(str, existing_creators))})
    GROUP BY user_id
    ORDER BY first_bot
""")

print("创建时间线:")
print("-" * 100)
for user_id, first_bot, last_bot, bot_count in cursor.fetchall():
    print(f"  User {user_id}: 首次创建于 {first_bot} ({bot_count}个bot)")

# Step 8: 找出他们的第一个bot是什么
print()
print("=" * 100)
print("🎯 他们的第一个bot是什么？")
print("=" * 100)
print()

for user_id in existing_creators:
    cursor.execute(f"""
        SELECT id, name, created_date
        FROM tg2app_tg_bots
        WHERE user_id = {user_id}
        ORDER BY created_date
        LIMIT 1
    """)

    bot_id, name, created = cursor.fetchone()
    print(f"  User {user_id}: {name} (创建于 {created})")

print()
print("=" * 100)
print("💡 分析总结")
print("=" * 100)
print()
print("基于以上数据，可以帮助回答：")
print("1. 这10人是否在同一个创作者群里？")
print("2. 他们是通过什么渠道知道营销bot的？")
print("3. 他们创建的bot和营销bot有什么关系？")
print("4. 他们是否互相使用彼此的bot？")

cursor.close()
conn.close()
