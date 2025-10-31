#!/usr/bin/env python3
"""
Non-Creator Analysis: Why didn't the 70 non-creators convert?

Focus: Understand the behavior of users who used marketing bots
       but did NOT create their own bots.
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

# Connect to database
env = load_env()
conn = pymysql.connect(
    host=env['DB_HOST'],
    port=int(env.get('DB_PORT', 3306)),
    user=env['DB_USER'],
    password=env['DB_PASS'],
    database=env['DB_NAME']
)

cursor = conn.cursor()

# Create output directory
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_dir = f"non_creator_analysis_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("🔍 NON-CREATOR ANALYSIS: Understanding the 70 Users Who Didn't Convert")
print("=" * 80)
print()

# The 8 marketing bots
content_bot_ids = [
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
]

# Get all marketing bot users
cursor.execute(f"""
    SELECT DISTINCT user_id
    FROM tg2app_bot_running_messages
    WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
""")
all_users = [row[0] for row in cursor.fetchall()]

# Get users who created bots
cursor.execute(f"""
    SELECT DISTINCT user_id
    FROM tg2app_tg_bots
    WHERE user_id IN ({','.join(map(str, all_users))})
""")
creators = [row[0] for row in cursor.fetchall()]

# Non-creators are the difference
non_creators = [u for u in all_users if u not in creators]

print(f"Total marketing bot users: {len(all_users)}")
print(f"Creators: {len(creators)}")
print(f"Non-Creators: {len(non_creators)}")
print()

# ============================================================================
# QUERY 1: Detailed engagement patterns of non-creators
# ============================================================================
print("=" * 80)
print("📊 QUERY 1: Non-Creator Engagement Patterns")
print("-" * 80)

cursor.execute(f"""
    SELECT
        user_id,
        COUNT(DISTINCT bot_id) as bots_used,
        COUNT(*) as total_messages,
        MIN(created_date) as first_interaction,
        MAX(created_date) as last_interaction,
        TIMESTAMPDIFF(HOUR, MIN(created_date), MAX(created_date)) as engagement_hours,
        COUNT(DISTINCT DATE(created_date)) as active_days
    FROM tg2app_bot_running_messages
    WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
      AND user_id IN ({','.join(map(str, non_creators))})
    GROUP BY user_id
    ORDER BY total_messages DESC
""")

non_creator_engagement = cursor.fetchall()

# Engagement distribution
print(f"\nEngagement Distribution ({len(non_creator_engagement)} users):")
print()

# By messages
one_msg = sum(1 for u in non_creator_engagement if u[2] == 1)
few_msg = sum(1 for u in non_creator_engagement if 2 <= u[2] <= 5)
many_msg = sum(1 for u in non_creator_engagement if u[2] > 5)

print("By message count:")
print(f"  1 message only:        {one_msg:>3} ({one_msg/len(non_creator_engagement)*100:>5.1f}%)")
print(f"  2-5 messages:          {few_msg:>3} ({few_msg/len(non_creator_engagement)*100:>5.1f}%)")
print(f"  6+ messages:           {many_msg:>3} ({many_msg/len(non_creator_engagement)*100:>5.1f}%)")
print()

# By active days
one_day = sum(1 for u in non_creator_engagement if u[6] == 1)
few_days = sum(1 for u in non_creator_engagement if 2 <= u[6] <= 3)
many_days = sum(1 for u in non_creator_engagement if u[6] > 3)

print("By active days:")
print(f"  1 day only:            {one_day:>3} ({one_day/len(non_creator_engagement)*100:>5.1f}%)")
print(f"  2-3 days:              {few_days:>3} ({few_days/len(non_creator_engagement)*100:>5.1f}%)")
print(f"  4+ days:               {many_days:>3} ({many_days/len(non_creator_engagement)*100:>5.1f}%)")
print()

# Average engagement
avg_messages = sum(u[2] for u in non_creator_engagement) / len(non_creator_engagement)
avg_days = sum(u[6] for u in non_creator_engagement) / len(non_creator_engagement)

print(f"Average engagement:")
print(f"  Messages per user:     {avg_messages:.1f}")
print(f"  Active days per user:  {avg_days:.1f}")
print()

# Top engaged non-creators
print("Top 10 most engaged non-creators:")
for user_id, bots, msgs, first, last, hours, days in non_creator_engagement[:10]:
    print(f"  User {user_id}: {bots} bots, {msgs} messages, {days} days")
print()

# Save data
with open(f"{output_dir}/non_creator_engagement.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['user_id', 'bots_used', 'total_messages', 'first_interaction', 'last_interaction', 'engagement_hours', 'active_days'])
    writer.writerows(non_creator_engagement)
print(f"💾 Saved: {output_dir}/non_creator_engagement.csv")
print()

# ============================================================================
# QUERY 2: Which bots do non-creators use most?
# ============================================================================
print("=" * 80)
print("📊 QUERY 2: Bot Popularity Among Non-Creators")
print("-" * 80)

cursor.execute(f"""
    SELECT
        t1.bot_id,
        tb.name as bot_name,
        COUNT(DISTINCT t1.user_id) as unique_users,
        COUNT(*) as total_messages,
        AVG(msg_per_user) as avg_messages_per_user
    FROM tg2app_bot_running_messages t1
    LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
    LEFT JOIN (
        SELECT bot_id, user_id, COUNT(*) as msg_per_user
        FROM tg2app_bot_running_messages
        WHERE user_id IN ({','.join(map(str, non_creators))})
          AND bot_id IN ({','.join(map(str, content_bot_ids))})
        GROUP BY bot_id, user_id
    ) per_user ON t1.bot_id = per_user.bot_id
    WHERE t1.bot_id IN ({','.join(map(str, content_bot_ids))})
      AND t1.user_id IN ({','.join(map(str, non_creators))})
    GROUP BY t1.bot_id, tb.name
    ORDER BY unique_users DESC
""")

bot_popularity = cursor.fetchall()

print("\nBot Usage by Non-Creators:")
print(f"{'Bot Name':<30} {'Users':>6} {'Messages':>9} {'Avg/User':>9}")
print("-" * 80)
for bot_id, name, users, msgs, avg in bot_popularity:
    name_display = (name[:27] + '...') if name and len(name) > 30 else (name or 'NULL')
    print(f"{name_display:<30} {users:>6} {msgs:>9} {avg:>9.1f}")
print()

# Save data
with open(f"{output_dir}/bot_popularity_non_creators.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['bot_id', 'bot_name', 'unique_users', 'total_messages', 'avg_messages_per_user'])
    writer.writerows(bot_popularity)
print(f"💾 Saved: {output_dir}/bot_popularity_non_creators.csv")
print()

# ============================================================================
# QUERY 3: Did non-creators interact with ShellAgent generation bot?
# ============================================================================
print("=" * 80)
print("📊 QUERY 3: ShellAgent Generation Bot Interaction")
print("-" * 80)

# Find ShellAgent bot (the generation bot, not user-created bots)
cursor.execute("""
    SELECT
        tb.id,
        tb.name,
        COUNT(DISTINCT t1.user_id) as user_count
    FROM tg2app_tg_bots tb
    LEFT JOIN tg2app_bot_running_messages t1 ON tb.id = t1.bot_id
    WHERE (
        tb.name LIKE '%ShellAgent%'
        OR tb.name LIKE '%shellagent%'
    )
    AND tb.name NOT LIKE '%ShellAgent_Playground%'
    AND tb.name NOT LIKE '%Test%'
    GROUP BY tb.id, tb.name
    HAVING user_count > 50
    ORDER BY user_count DESC
    LIMIT 5
""")

shellagent_candidates = cursor.fetchall()

if shellagent_candidates:
    print("Potential ShellAgent generation bots:")
    for bot_id, name, users in shellagent_candidates:
        print(f"  {name} (ID: {bot_id}): {users} users")
    print()

    shellagent_bot_id = shellagent_candidates[0][0]
    shellagent_name = shellagent_candidates[0][1]

    # Check if non-creators used ShellAgent
    cursor.execute(f"""
        SELECT
            user_id,
            COUNT(*) as message_count,
            MIN(created_date) as first_interaction,
            MAX(created_date) as last_interaction
        FROM tg2app_bot_running_messages
        WHERE bot_id = {shellagent_bot_id}
          AND user_id IN ({','.join(map(str, non_creators))})
        GROUP BY user_id
        ORDER BY message_count DESC
    """)

    shellagent_users = cursor.fetchall()

    print(f"Non-creators who interacted with {shellagent_name}:")
    print(f"  Total: {len(shellagent_users)} / {len(non_creators)} ({len(shellagent_users)/len(non_creators)*100:.1f}%)")
    print()

    if len(shellagent_users) > 0:
        print("Top 10 interactions:")
        for user_id, msgs, first, last in shellagent_users[:10]:
            print(f"  User {user_id}: {msgs} messages to ShellAgent")
        print()

        # Save data
        with open(f"{output_dir}/non_creators_with_shellagent.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'message_count', 'first_interaction', 'last_interaction'])
            writer.writerows(shellagent_users)
        print(f"💾 Saved: {output_dir}/non_creators_with_shellagent.csv")
    else:
        print("⚠️  None of the non-creators interacted with ShellAgent generation bot")
    print()
else:
    print("⚠️  Could not identify ShellAgent generation bot")
    print()

# ============================================================================
# QUERY 4: Sample conversations from high-engagement non-creators
# ============================================================================
print("=" * 80)
print("📊 QUERY 4: Conversion Blockers - Sample User Journeys")
print("-" * 80)

# Get top 5 most engaged non-creators
high_engagement_non_creators = [u[0] for u in non_creator_engagement[:5]]

print("\nAnalyzing top 5 engaged non-creators who didn't convert:")
print()

for user_id in high_engagement_non_creators:
    # Get their bot usage
    cursor.execute(f"""
        SELECT
            tb.name,
            COUNT(*) as message_count,
            MIN(t1.created_date) as first_msg,
            MAX(t1.created_date) as last_msg
        FROM tg2app_bot_running_messages t1
        LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
        WHERE t1.user_id = {user_id}
          AND t1.bot_id IN ({','.join(map(str, content_bot_ids))})
        GROUP BY tb.name
        ORDER BY message_count DESC
    """)

    user_bots = cursor.fetchall()

    print(f"User {user_id}:")
    for bot_name, msgs, first, last in user_bots:
        days_active = (last - first).days if (last - first).days > 0 else 0
        print(f"  - {bot_name}: {msgs} messages over {days_active} days")
    print()

# ============================================================================
# Summary
# ============================================================================
print("=" * 80)
print("📈 NON-CREATOR ANALYSIS SUMMARY")
print("=" * 80)
print()
print(f"Total non-creators:           {len(non_creators)}")
print(f"Average messages per user:    {avg_messages:.1f}")
print(f"Average active days:          {avg_days:.1f}")
print()
print("Engagement patterns:")
print(f"  Low engagement (1 msg):     {one_msg} ({one_msg/len(non_creators)*100:.1f}%)")
print(f"  Medium (2-5 msgs):          {few_msg} ({few_msg/len(non_creators)*100:.1f}%)")
print(f"  High (6+ msgs):             {many_msg} ({many_msg/len(non_creators)*100:.1f}%)")
print()

if shellagent_candidates:
    print(f"ShellAgent interaction:       {len(shellagent_users)} users ({len(shellagent_users)/len(non_creators)*100:.1f}%)")
    print(f"Did NOT try ShellAgent:       {len(non_creators) - len(shellagent_users)} users")
    print()

print("🎯 Key Questions:")
print("  1. Why didn't high-engagement users (6+ messages) convert?")
print("  2. Did they know about ShellAgent's bot creation capability?")
print("  3. Were the marketing bots too specific/niche for their needs?")
print("  4. Is there a missing CTA or onboarding flow?")
print()
print("=" * 80)
print(f"✨ Analysis complete! Results saved to {output_dir}/")
print("=" * 80)

cursor.close()
conn.close()
