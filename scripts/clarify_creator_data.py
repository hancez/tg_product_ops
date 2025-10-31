#!/usr/bin/env python3
"""
数据澄清：排除8个营销bot的原创作者后的真实转化数据
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
print("🔍 数据澄清：排除营销bot原创者")
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

# Step 1: 找出这8个bot的创建者
print("Step 1: 查找8个营销bot的创建者")
print("-" * 80)

cursor.execute(f"""
    SELECT id, name, user_id, created_date
    FROM tg2app_tg_bots
    WHERE id IN ({','.join(map(str, marketing_bot_ids))})
    ORDER BY created_date
""")

marketing_bot_creators = {}
for bot_id, name, user_id, created in cursor.fetchall():
    marketing_bot_creators[bot_id] = user_id
    print(f"  {name:30} created by user {user_id}")

print(f"\n✅ 营销bot创建者user_ids: {set(marketing_bot_creators.values())}")
print()

# Step 2: 所有使用营销bot的用户
print("Step 2: 所有使用营销bot的用户")
print("-" * 80)

cursor.execute(f"""
    SELECT DISTINCT user_id
    FROM tg2app_bot_running_messages
    WHERE bot_id IN ({','.join(map(str, marketing_bot_ids))})
""")

all_marketing_bot_users = [row[0] for row in cursor.fetchall()]
print(f"✅ 总用户数: {len(all_marketing_bot_users)}")
print()

# Step 3: 排除营销bot创建者
marketing_bot_creator_user_ids = set(marketing_bot_creators.values())
users_excluding_creators = [u for u in all_marketing_bot_users if u not in marketing_bot_creator_user_ids]

print("Step 3: 排除营销bot创建者后")
print("-" * 80)
print(f"  原始用户数: {len(all_marketing_bot_users)}")
print(f"  营销bot创建者: {len(marketing_bot_creator_user_ids)} users")
print(f"  排除后用户数: {len(users_excluding_creators)}")
print()

# Step 4: 这些用户中有多少创建了bot（任何bot）
print("Step 4: 排除后的用户中，有多少人创建了bot？")
print("-" * 80)

if users_excluding_creators:
    cursor.execute(f"""
        SELECT DISTINCT user_id
        FROM tg2app_tg_bots
        WHERE user_id IN ({','.join(map(str, users_excluding_creators))})
    """)

    bot_creators_excluding_marketing = [row[0] for row in cursor.fetchall()]

    print(f"✅ 创建了bot的用户: {len(bot_creators_excluding_marketing)}")
    print(f"✅ 未创建bot的用户: {len(users_excluding_creators) - len(bot_creators_excluding_marketing)}")
    print(f"✅ 转化率: {len(bot_creators_excluding_marketing)/len(users_excluding_creators)*100:.1f}%")
    print()

    # 显示这些创建者的详情
    if bot_creators_excluding_marketing:
        print("创建了bot的用户详情:")
        cursor.execute(f"""
            SELECT
                user_id,
                COUNT(*) as bots_created,
                GROUP_CONCAT(name SEPARATOR ' | ') as bot_names
            FROM tg2app_tg_bots
            WHERE user_id IN ({','.join(map(str, bot_creators_excluding_marketing))})
            GROUP BY user_id
            ORDER BY bots_created DESC
            LIMIT 10
        """)

        for user_id, count, names in cursor.fetchall():
            print(f"  User {user_id}: {count} bots")
            if names:
                name_list = names.split(' | ')
                for name in name_list[:3]:
                    print(f"    - {name}")
                if len(name_list) > 3:
                    print(f"    ... and {len(name_list) - 3} more")

print()
print("=" * 80)
print("Step 5: Timeline分析 - 这些创建者是先用bot还是先创建？")
print("-" * 80)

if bot_creators_excluding_marketing:
    cursor.execute(f"""
        SELECT
            u.user_id,
            u.first_usage,
            c.first_creation,
            TIMESTAMPDIFF(HOUR, u.first_usage, c.first_creation) as hours_to_conversion,
            u.bots_used,
            c.bots_created
        FROM (
            SELECT
                user_id,
                MIN(created_date) as first_usage,
                COUNT(DISTINCT bot_id) as bots_used
            FROM tg2app_bot_running_messages
            WHERE bot_id IN ({','.join(map(str, marketing_bot_ids))})
              AND user_id IN ({','.join(map(str, bot_creators_excluding_marketing))})
            GROUP BY user_id
        ) u
        INNER JOIN (
            SELECT
                user_id,
                MIN(created_date) as first_creation,
                COUNT(*) as bots_created
            FROM tg2app_tg_bots
            WHERE user_id IN ({','.join(map(str, bot_creators_excluding_marketing))})
            GROUP BY user_id
        ) c ON u.user_id = c.user_id
        ORDER BY hours_to_conversion
    """)

    timeline_data = cursor.fetchall()

    # 分析时间线
    created_before = sum(1 for row in timeline_data if row[3] < 0)  # negative = created before using
    created_after = sum(1 for row in timeline_data if row[3] > 0)   # positive = created after using
    created_same_time = sum(1 for row in timeline_data if row[3] == 0)

    print(f"\n时间线分析 ({len(timeline_data)} 创建者):")
    print(f"  先创建bot，后使用营销bot: {created_before} ({created_before/len(timeline_data)*100:.1f}%)")
    print(f"  先使用营销bot，后创建bot: {created_after} ({created_after/len(timeline_data)*100:.1f}%)")
    print(f"  同一时间: {created_same_time}")
    print()

    if created_after > 0:
        print("✅ 真正的GTM转化案例（先使用营销bot → 后创建）:")
        true_conversions = [row for row in timeline_data if row[3] > 0]
        for user_id, first_use, first_create, hours, bots_used, bots_created in true_conversions[:10]:
            days = hours / 24
            print(f"  User {user_id}: Used {bots_used} marketing bots → Created {bots_created} bots after {days:.1f} days")

    if created_before > 0:
        print(f"\n❌ 非GTM转化（先创建 → 后使用营销bot）: {created_before} users")
        print("   这些用户是现有创建者来学习/借鉴营销bot")

print()
print("=" * 80)
print("📊 修正后的GTM指标")
print("=" * 80)
print(f"营销bot用户（排除原创者）:     {len(users_excluding_creators)}")
print(f"真正的GTM转化（先用后创建）:     {created_after if bot_creators_excluding_marketing else 0}")
print(f"真实GTM转化率:                 {created_after/len(users_excluding_creators)*100 if users_excluding_creators and bot_creators_excluding_marketing else 0:.1f}%")
print()
print(f"现有创建者（先创建后使用）:     {created_before if bot_creators_excluding_marketing else 0}")
print(f"非创建者（真正的目标用户）:     {len(users_excluding_creators) - len(bot_creators_excluding_marketing)}")
print("=" * 80)

cursor.close()
conn.close()
