#!/usr/bin/env python3
"""
GTM Conversion Analysis: Solution-Led Growth Strategy Validation

Focus: Do users who experience our 8 professional content creator bots
       convert to becoming bot creators themselves on ShellAgent?

Key Metrics:
1. Total users of the 8 marketing bots
2. Conversion rate: Bot Users → Bot Creators
3. Time to conversion
4. Remix adoption
5. User engagement patterns
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
output_dir = f"gtm_analysis_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("🎯 GTM STRATEGY VALIDATION: Solution-Led Growth Analysis")
print("=" * 80)
print()
print("Strategy: Professional Content Bots → User Adoption → Bot Creation")
print()

# The 8 professional content creator bots (marketing use cases)
content_bot_ids = [
    1965760104392110080,  # Hook_Generator_bot
    1970046615507873792,  # myshell_thumbmaker_bot
    1972858715723681792,  # QuickVid_bot
    1974427421370437632,  # NanoBannana_bot
    1974701461545680896,  # ThreadMaker_bot
    1974829619605544960,  # HealAI_bot
    1975400765027258368,  # DeepSeek_R1_bot
    1975961906457870336   # SongMaker_bot
]

print("📋 Marketing Bots Being Analyzed:")
print("-" * 80)
cursor.execute(f"""
    SELECT id, name, user_id, created_date
    FROM tg2app_tg_bots
    WHERE id IN ({','.join(map(str, content_bot_ids))})
    ORDER BY created_date
""")
marketing_bots = cursor.fetchall()
for bot_id, name, creator_id, created in marketing_bots:
    print(f"  {name:30} (ID: {bot_id})")
print()

# ============================================================================
# QUERY 1: All Users of Marketing Bots (with latest data)
# ============================================================================
print("=" * 80)
print("📊 QUERY 1: Users of Marketing Bots")
print("-" * 80)

cursor.execute(f"""
    SELECT
        user_id,
        COUNT(DISTINCT bot_id) as bots_used,
        COUNT(*) as total_messages,
        MIN(created_date) as first_interaction,
        MAX(created_date) as last_interaction,
        TIMESTAMPDIFF(DAY, MIN(created_date), MAX(created_date)) as engagement_days
    FROM tg2app_bot_running_messages
    WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
    GROUP BY user_id
    ORDER BY bots_used DESC, total_messages DESC
""")

marketing_bot_users = cursor.fetchall()
total_users = len(marketing_bot_users)

print(f"✅ Total users of marketing bots: {total_users}")
print()

# Engagement distribution
single_bot_users = sum(1 for u in marketing_bot_users if u[1] == 1)
power_users = sum(1 for u in marketing_bot_users if u[1] >= 2)
super_users = sum(1 for u in marketing_bot_users if u[1] >= 4)

print("User Engagement Distribution:")
print(f"  Single-bot users (1 bot):      {single_bot_users:>4} ({single_bot_users/total_users*100:>5.1f}%)")
print(f"  Power users (2+ bots):         {power_users:>4} ({power_users/total_users*100:>5.1f}%)")
print(f"  Super users (4+ bots):         {super_users:>4} ({super_users/total_users*100:>5.1f}%)")
print()

# Save user list
with open(f"{output_dir}/marketing_bot_users.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['user_id', 'bots_used', 'total_messages', 'first_interaction', 'last_interaction', 'engagement_days'])
    writer.writerows(marketing_bot_users)
print(f"💾 Saved: {output_dir}/marketing_bot_users.csv")
print()

# Extract user IDs for next queries
user_ids = [row[0] for row in marketing_bot_users]

# ============================================================================
# QUERY 2: Conversion - Did These Users Create Their Own Bots?
# ============================================================================
print("=" * 80)
print("📊 QUERY 2: Conversion to Bot Creators")
print("-" * 80)

cursor.execute(f"""
    SELECT
        user_id,
        COUNT(*) as bots_created,
        MIN(created_date) as first_bot_created,
        MAX(created_date) as last_bot_created,
        GROUP_CONCAT(id ORDER BY created_date SEPARATOR ',') as bot_ids,
        GROUP_CONCAT(name ORDER BY created_date SEPARATOR ' | ') as bot_names
    FROM tg2app_tg_bots
    WHERE user_id IN ({','.join(map(str, user_ids))})
    GROUP BY user_id
    ORDER BY bots_created DESC
""")

bot_creators = cursor.fetchall()
creators_count = len(bot_creators)
conversion_rate = (creators_count / total_users * 100) if total_users > 0 else 0

print(f"✅ Users who became bot creators: {creators_count} / {total_users}")
print(f"🎯 Conversion Rate: {conversion_rate:.1f}%")
print()

if creators_count > 0:
    # Distribution of bots created
    bots_created_dist = {}
    for creator in bot_creators:
        count = creator[1]
        bots_created_dist[count] = bots_created_dist.get(count, 0) + 1

    print("Distribution of bots created:")
    for count in sorted(bots_created_dist.keys(), reverse=True):
        num_users = bots_created_dist[count]
        print(f"  {count} bot(s):  {num_users:>3} users ({num_users/creators_count*100:>5.1f}% of creators)")
    print()

    # Top bot creators
    print("Top 10 bot creators:")
    for user_id, bots_created, first_created, last_created, bot_ids, bot_names in bot_creators[:10]:
        print(f"  User {user_id}: {bots_created} bots")
        if bot_names:
            names = bot_names.split(' | ')
            for name in names[:3]:  # Show first 3 bot names
                print(f"    - {name}")
            if len(names) > 3:
                print(f"    ... and {len(names) - 3} more")
    print()

# Save creator data
with open(f"{output_dir}/bot_creators.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['user_id', 'bots_created', 'first_bot_created', 'last_bot_created', 'bot_ids', 'bot_names'])
    writer.writerows(bot_creators)
print(f"💾 Saved: {output_dir}/bot_creators.csv")
print()

# ============================================================================
# QUERY 3: Conversion Timeline Analysis
# ============================================================================
print("=" * 80)
print("📊 QUERY 3: Conversion Timeline - From User to Creator")
print("-" * 80)

# Create creator user_id list
creator_user_ids = [row[0] for row in bot_creators]

if creator_user_ids:
    cursor.execute(f"""
        SELECT
            u.user_id,
            u.first_usage,
            u.bots_used,
            u.messages_sent,
            c.first_creation,
            c.bots_created,
            TIMESTAMPDIFF(HOUR, u.first_usage, c.first_creation) as hours_to_conversion,
            TIMESTAMPDIFF(DAY, u.first_usage, c.first_creation) as days_to_conversion
        FROM (
            SELECT
                user_id,
                MIN(created_date) as first_usage,
                COUNT(DISTINCT bot_id) as bots_used,
                COUNT(*) as messages_sent
            FROM tg2app_bot_running_messages
            WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
              AND user_id IN ({','.join(map(str, creator_user_ids))})
            GROUP BY user_id
        ) u
        INNER JOIN (
            SELECT
                user_id,
                MIN(created_date) as first_creation,
                COUNT(*) as bots_created
            FROM tg2app_tg_bots
            WHERE user_id IN ({','.join(map(str, creator_user_ids))})
            GROUP BY user_id
        ) c ON u.user_id = c.user_id
        ORDER BY hours_to_conversion
    """)

    timeline_data = cursor.fetchall()

    # Calculate statistics
    conversion_times = [row[6] for row in timeline_data]  # hours_to_conversion

    # Categorize conversion speed
    immediate = sum(1 for t in conversion_times if t < 1)  # < 1 hour
    same_day = sum(1 for t in conversion_times if 1 <= t < 24)  # 1-24 hours
    week = sum(1 for t in conversion_times if 24 <= t < 168)  # 1-7 days
    later = sum(1 for t in conversion_times if t >= 168)  # 7+ days

    print(f"Conversion Speed Analysis ({len(timeline_data)} converted users):")
    print(f"  Immediate (< 1 hour):      {immediate:>3} ({immediate/len(timeline_data)*100:>5.1f}%)")
    print(f"  Same day (1-24 hours):     {same_day:>3} ({same_day/len(timeline_data)*100:>5.1f}%)")
    print(f"  Within week (1-7 days):    {week:>3} ({week/len(timeline_data)*100:>5.1f}%)")
    print(f"  Later (7+ days):           {later:>3} ({later/len(timeline_data)*100:>5.1f}%)")
    print()

    # Average time to conversion
    avg_hours = sum(conversion_times) / len(conversion_times)
    median_hours = sorted(conversion_times)[len(conversion_times) // 2]
    print(f"Time to Conversion:")
    print(f"  Average: {avg_hours:.1f} hours ({avg_hours/24:.1f} days)")
    print(f"  Median:  {median_hours:.1f} hours ({median_hours/24:.1f} days)")
    print()

    # Show examples
    print("Examples of conversion journeys:")
    print("  Fast converters (< 24 hours):")
    fast_converters = [row for row in timeline_data if row[6] < 24][:5]
    for user_id, first_use, bots_used, msgs, first_create, bots_created, hours, days in fast_converters:
        print(f"    User {user_id}: Used {bots_used} bots → Created {bots_created} bots in {hours:.1f}h")

    print()
    print("  Slow converters (7+ days):")
    slow_converters = [row for row in timeline_data if row[6] >= 168][:5]
    for user_id, first_use, bots_used, msgs, first_create, bots_created, hours, days in slow_converters:
        print(f"    User {user_id}: Used {bots_used} bots → Created {bots_created} bots in {days:.0f} days")
    print()

    # Save timeline data
    with open(f"{output_dir}/conversion_timeline.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'first_usage', 'bots_used', 'messages_sent', 'first_creation', 'bots_created', 'hours_to_conversion', 'days_to_conversion'])
        writer.writerows(timeline_data)
    print(f"💾 Saved: {output_dir}/conversion_timeline.csv")
    print()

# ============================================================================
# QUERY 4: Remix Analysis - Feature Adoption
# ============================================================================
print("=" * 80)
print("📊 QUERY 4: Remix Feature Adoption")
print("-" * 80)

# Check remix relations from marketing bots
cursor.execute(f"""
    SELECT
        source_bot_id,
        target_bot_id,
        COUNT(*) as remix_count
    FROM tg2app_bot_remix_relations
    WHERE source_bot_id IN ({','.join(map(str, content_bot_ids))})
    GROUP BY source_bot_id, target_bot_id
""")

remix_relations = cursor.fetchall()
total_remixes = len(remix_relations)

print(f"Remixes from marketing bots: {total_remixes}")

if total_remixes > 0:
    print("\nRemix flows:")
    for source_id, target_id, count in remix_relations[:20]:
        cursor.execute("SELECT name FROM tg2app_tg_bots WHERE id = %s", (source_id,))
        source_name = cursor.fetchone()
        source_name = source_name[0] if source_name else "Unknown"

        cursor.execute("SELECT name FROM tg2app_tg_bots WHERE id = %s", (target_id,))
        target_name = cursor.fetchone()
        target_name = target_name[0] if target_name else "Unknown"

        print(f"  {source_name[:25]:25} → {target_name[:25]:25} ({count} remixes)")

    with open(f"{output_dir}/remix_relations.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['source_bot_id', 'target_bot_id', 'remix_count'])
        writer.writerows(remix_relations)
    print(f"\n💾 Saved: {output_dir}/remix_relations.csv")
else:
    print("⚠️  No remix relationships found from marketing bots")
print()

# Check /remix command usage
cursor.execute(f"""
    SELECT
        user_id,
        bot_id,
        COUNT(*) as remix_mentions,
        MIN(created_date) as first_mention,
        MAX(created_date) as last_mention
    FROM tg2app_bot_running_messages
    WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
      AND (raw_text LIKE '%/remix%' OR raw_text LIKE '/remix%')
      AND src = 'send'
    GROUP BY user_id, bot_id
""")

remix_command_users = cursor.fetchall()
print(f"/remix command usage: {len(remix_command_users)} instances")

if len(remix_command_users) > 0:
    print("\nUsers who used /remix command:")
    for user_id, bot_id, count, first, last in remix_command_users[:10]:
        print(f"  User {user_id}: {count} times")

    with open(f"{output_dir}/remix_command_usage.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'bot_id', 'remix_mentions', 'first_mention', 'last_mention'])
        writer.writerows(remix_command_users)
    print(f"\n💾 Saved: {output_dir}/remix_command_usage.csv")
else:
    print("⚠️  No users used /remix command in marketing bots")
print()

# ============================================================================
# QUERY 5: User Segmentation - Creator Profile Analysis
# ============================================================================
print("=" * 80)
print("📊 QUERY 5: Creator Profile Analysis")
print("-" * 80)

if creator_user_ids:
    # Analyze usage patterns of creators vs non-creators
    cursor.execute(f"""
        SELECT
            user_id,
            COUNT(DISTINCT bot_id) as bots_used,
            COUNT(*) as messages_sent,
            COUNT(DISTINCT DATE(created_date)) as active_days,
            MIN(created_date) as first_interaction,
            MAX(created_date) as last_interaction,
            CASE
                WHEN user_id IN ({','.join(map(str, creator_user_ids))})
                THEN 'Creator'
                ELSE 'Non-Creator'
            END as user_type
        FROM tg2app_bot_running_messages
        WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
        GROUP BY user_id
    """)

    user_segments = cursor.fetchall()

    # Calculate averages for each segment
    creators = [u for u in user_segments if u[6] == 'Creator']
    non_creators = [u for u in user_segments if u[6] == 'Non-Creator']

    print(f"Segment Comparison:")
    print()
    print(f"{'Metric':<30} {'Creators':<15} {'Non-Creators':<15}")
    print("-" * 60)

    # Bots used
    creator_bots = sum(u[1] for u in creators) / len(creators) if creators else 0
    non_creator_bots = sum(u[1] for u in non_creators) / len(non_creators) if non_creators else 0
    print(f"{'Avg bots used':<30} {creator_bots:<15.2f} {non_creator_bots:<15.2f}")

    # Messages sent
    creator_msgs = sum(u[2] for u in creators) / len(creators) if creators else 0
    non_creator_msgs = sum(u[2] for u in non_creators) / len(non_creators) if non_creators else 0
    print(f"{'Avg messages sent':<30} {creator_msgs:<15.1f} {non_creator_msgs:<15.1f}")

    # Active days
    creator_days = sum(u[3] for u in creators) / len(creators) if creators else 0
    non_creator_days = sum(u[3] for u in non_creators) / len(non_creators) if non_creators else 0
    print(f"{'Avg active days':<30} {creator_days:<15.1f} {non_creator_days:<15.1f}")
    print()

    # Power user conversion rate
    creator_power_users = sum(1 for u in creators if u[1] >= 2)
    non_creator_power_users = sum(1 for u in non_creators if u[1] >= 2)

    print(f"Power Users (2+ bots):")
    print(f"  Creators:     {creator_power_users}/{len(creators)} ({creator_power_users/len(creators)*100:.1f}%)")
    print(f"  Non-Creators: {non_creator_power_users}/{len(non_creators)} ({non_creator_power_users/len(non_creators)*100:.1f}%)")
    print()

    # Save segmentation
    with open(f"{output_dir}/user_segmentation.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'bots_used', 'messages_sent', 'active_days', 'first_interaction', 'last_interaction', 'user_type'])
        writer.writerows(user_segments)
    print(f"💾 Saved: {output_dir}/user_segmentation.csv")
    print()

# ============================================================================
# Summary Report
# ============================================================================
print("=" * 80)
print("📈 GTM STRATEGY VALIDATION SUMMARY")
print("=" * 80)
print()
print(f"Marketing Bot Users:         {total_users}")
print(f"Converted to Creators:       {creators_count} ({conversion_rate:.1f}%)")
print(f"Power Users (2+ bots):       {power_users} ({power_users/total_users*100:.1f}%)")
print()

if creator_user_ids:
    print(f"Conversion Insights:")
    print(f"  Fast converters (< 24h):   {immediate + same_day}")
    print(f"  Average time to convert:   {avg_hours:.1f} hours")
    print()

print(f"Remix Adoption:")
print(f"  Remix relationships:       {total_remixes}")
print(f"  /remix command usage:      {len(remix_command_users)}")
print()

print(f"Key Findings:")
if conversion_rate > 15:
    print(f"  ✅ Strong conversion rate ({conversion_rate:.1f}%) - GTM strategy is working")
else:
    print(f"  ⚠️  Low conversion rate ({conversion_rate:.1f}%) - Needs improvement")

if total_remixes == 0 and len(remix_command_users) == 0:
    print(f"  🔴 Remix feature is NOT being used - Critical issue")
else:
    print(f"  ✅ Remix feature has some adoption")

if power_users / total_users > 0.15:
    print(f"  ✅ Good power user ratio ({power_users/total_users*100:.1f}%)")
else:
    print(f"  ⚠️  Low power user engagement")

print()
print("=" * 80)
print(f"✨ Analysis complete! Results saved to {output_dir}/")
print("=" * 80)

cursor.close()
conn.close()
