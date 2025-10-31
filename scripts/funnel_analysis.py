#!/usr/bin/env python3
"""
Complete Funnel Analysis: Bot Users → ShellAgent → Remix → Creation
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
output_dir = "funnel_analysis_" + datetime.now().strftime('%Y%m%d_%H%M%S')
import os
os.makedirs(output_dir, exist_ok=True)

print("=" * 80)
print("🔍 COMPLETE FUNNEL ANALYSIS")
print("=" * 80)
print()

# The 8 content creator bots
content_bot_ids = [
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
]

print("📊 QUERY 1: Remix Relations Table Analysis")
print("-" * 80)

try:
    # Check structure of remix table
    cursor.execute("DESCRIBE tg2app_bot_remix_relations")
    columns = cursor.fetchall()
    print("Table structure:")
    for col in columns:
        print(f"  {col[0]:30} {col[1]:20}")

    print("\nQuerying remix relations from our 8 bots...")
    cursor.execute(f"""
        SELECT
            source_bot_id,
            target_bot_id,
            COUNT(*) as remix_count
        FROM tg2app_bot_remix_relations
        WHERE source_bot_id IN ({','.join(map(str, content_bot_ids))})
        GROUP BY source_bot_id, target_bot_id
        ORDER BY remix_count DESC
    """)

    remix_relations = cursor.fetchall()
    print(f"\n✅ Found {len(remix_relations)} remix relationships")

    if remix_relations:
        print("\nRemix flows from our 8 content bots:")
        for source, target, count in remix_relations[:20]:
            # Get bot names
            cursor.execute("SELECT name FROM tg2app_tg_bots WHERE id = %s", (source,))
            source_name = cursor.fetchone()[0] if cursor.rowcount > 0 else "Unknown"
            cursor.execute("SELECT name FROM tg2app_tg_bots WHERE id = %s", (target,))
            target_name = cursor.fetchone()[0] if cursor.rowcount > 0 else "Unknown"

            print(f"  {source_name[:30]:30} → {target_name[:30]:30} ({count} remixes)")

        # Save to CSV
        with open(f"{output_dir}/remix_relations.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['source_bot_id', 'target_bot_id', 'remix_count'])
            writer.writerows(remix_relations)
        print(f"\n💾 Saved to {output_dir}/remix_relations.csv")
    else:
        print("⚠️  No remix relationships found from our 8 bots")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 QUERY 2: Find ShellAgent Bot (Generation Bot)")
print("-" * 80)

try:
    # ShellAgent should have the most unique users
    cursor.execute("""
        SELECT
            t1.bot_id,
            tb.name as bot_name,
            COUNT(DISTINCT t1.user_id) as unique_users,
            COUNT(*) as total_messages,
            MIN(t1.created_date) as first_seen,
            MAX(t1.created_date) as last_seen
        FROM tg2app_bot_running_messages t1
        LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
        WHERE t1.bot_id NOT IN ({})
        GROUP BY t1.bot_id, tb.name
        HAVING unique_users >= 50
        ORDER BY unique_users DESC
        LIMIT 10
    """.format(','.join(map(str, content_bot_ids))))

    top_bots = cursor.fetchall()
    print("Top 10 bots by user count (excluding our 8 content bots):\n")
    print(f"{'Bot ID':20} {'Name':40} {'Users':>8} {'Msgs':>10} {'Period'}")
    print("-" * 100)

    shellagent_candidates = []
    for bot_id, name, users, messages, first, last in top_bots:
        name_display = (name[:37] + '...') if name and len(name) > 40 else (name or 'NULL')
        period = f"{first.strftime('%Y-%m-%d')} to {last.strftime('%Y-%m-%d')}"
        print(f"{str(bot_id):20} {name_display:40} {users:>8,} {messages:>10,} {period}")

        # Identify ShellAgent candidates
        if name and ('shellagent' in name.lower() or 'generate' in name.lower() or 'builder' in name.lower()):
            shellagent_candidates.append((bot_id, name, users))

    if shellagent_candidates:
        print("\n🎯 ShellAgent candidates found:")
        for bot_id, name, users in shellagent_candidates:
            print(f"  Bot ID {bot_id}: {name} ({users} users)")

        # Use the one with most users
        shellagent_bot_id = shellagent_candidates[0][0]
        shellagent_name = shellagent_candidates[0][1]
    else:
        print("\n⚠️  No obvious ShellAgent found. Using top bot as ShellAgent:")
        shellagent_bot_id = top_bots[0][0]
        shellagent_name = top_bots[0][1]

    print(f"\n✅ Using Bot ID {shellagent_bot_id} ({shellagent_name}) as ShellAgent")

except Exception as e:
    print(f"❌ Error: {e}")
    shellagent_bot_id = None

print("\n" + "=" * 80)
print("📊 QUERY 3: Bot Users vs ShellAgent Users Overlap")
print("-" * 80)

if shellagent_bot_id:
    try:
        cursor.execute(f"""
            SELECT
                bot_users.user_id,
                bot_users.bot_count as content_bots_used,
                bot_users.total_messages as content_bot_messages,
                CASE WHEN shellagent_users.user_id IS NOT NULL THEN 1 ELSE 0 END as used_shellagent,
                COALESCE(shellagent_users.message_count, 0) as shellagent_messages
            FROM (
                -- Users of our 8 content bots
                SELECT
                    user_id,
                    COUNT(DISTINCT bot_id) as bot_count,
                    COUNT(*) as total_messages
                FROM tg2app_bot_running_messages
                WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
                GROUP BY user_id
            ) bot_users
            LEFT JOIN (
                -- Users of ShellAgent
                SELECT
                    user_id,
                    COUNT(*) as message_count
                FROM tg2app_bot_running_messages
                WHERE bot_id = {shellagent_bot_id}
                GROUP BY user_id
            ) shellagent_users ON bot_users.user_id = shellagent_users.user_id
            ORDER BY used_shellagent DESC, bot_users.bot_count DESC
        """)

        overlap_data = cursor.fetchall()

        # Calculate stats
        total_bot_users = len(overlap_data)
        shellagent_users = sum(1 for row in overlap_data if row[3] == 1)
        overlap_rate = (shellagent_users / total_bot_users * 100) if total_bot_users > 0 else 0

        print(f"Total bot users (our 8 bots): {total_bot_users}")
        print(f"Also used ShellAgent: {shellagent_users}")
        print(f"Overlap rate: {overlap_rate:.1f}%")

        # Power users overlap
        power_users = [row for row in overlap_data if row[1] >= 2]
        power_users_with_shellagent = sum(1 for row in power_users if row[3] == 1)

        print(f"\nPower users (2+ bots): {len(power_users)}")
        print(f"Power users also using ShellAgent: {power_users_with_shellagent}")
        print(f"Power user overlap rate: {(power_users_with_shellagent / len(power_users) * 100) if power_users else 0:.1f}%")

        # Save to CSV
        with open(f"{output_dir}/user_overlap.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'content_bots_used', 'content_bot_messages', 'used_shellagent', 'shellagent_messages'])
            writer.writerows(overlap_data)
        print(f"\n💾 Saved to {output_dir}/user_overlap.csv")

        # Show sample users
        print("\nSample bot users who ALSO used ShellAgent:")
        shellagent_users_sample = [row for row in overlap_data if row[3] == 1][:10]
        for user_id, bots, msgs, _, sa_msgs in shellagent_users_sample:
            print(f"  User {user_id}: {bots} bots, {msgs} msgs on content bots, {sa_msgs} msgs on ShellAgent")

        print("\nSample bot users who NEVER used ShellAgent:")
        no_shellagent_sample = [row for row in overlap_data if row[3] == 0][:10]
        for user_id, bots, msgs, _, _ in no_shellagent_sample:
            print(f"  User {user_id}: {bots} bots, {msgs} msgs on content bots, 0 msgs on ShellAgent")

    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 QUERY 4: Remix Command Usage Analysis")
print("-" * 80)

try:
    cursor.execute("""
        SELECT
            user_id,
            bot_id,
            COUNT(*) as remix_mentions,
            MIN(created_date) as first_remix_mention,
            MAX(created_date) as last_remix_mention
        FROM tg2app_bot_running_messages
        WHERE (raw_text LIKE '%/remix%' OR raw_text LIKE '/remix%')
          AND src = 'send'
        GROUP BY user_id, bot_id
        ORDER BY remix_mentions DESC
        LIMIT 50
    """)

    remix_users = cursor.fetchall()
    print(f"Found {len(remix_users)} user-bot pairs with remix mentions\n")

    # Check how many are from our content bots
    from_content_bots = [row for row in remix_users if row[1] in content_bot_ids]
    print(f"Remix mentions from our 8 content bots: {len(from_content_bots)}")

    if from_content_bots:
        print("\nTop remix users from our content bots:")
        for user_id, bot_id, count, first, last in from_content_bots[:10]:
            cursor.execute("SELECT name FROM tg2app_tg_bots WHERE id = %s", (bot_id,))
            bot_name = cursor.fetchone()[0] if cursor.rowcount > 0 else "Unknown"
            print(f"  User {user_id} mentioned remix {count} times in {bot_name}")

    # Save all remix users
    with open(f"{output_dir}/remix_command_users.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'bot_id', 'remix_mentions', 'first_mention', 'last_mention'])
        writer.writerows(remix_users)
    print(f"\n💾 Saved to {output_dir}/remix_command_users.csv")

except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("📊 QUERY 5: User Journey Analysis - Sequential Bot Usage")
print("-" * 80)

try:
    # For power users, see if they used content bots BEFORE ShellAgent
    if shellagent_bot_id:
        cursor.execute(f"""
            SELECT
                user_id,
                MIN(CASE WHEN bot_id IN ({','.join(map(str, content_bot_ids))}) THEN created_date END) as first_content_bot_use,
                MIN(CASE WHEN bot_id = {shellagent_bot_id} THEN created_date END) as first_shellagent_use,
                COUNT(DISTINCT CASE WHEN bot_id IN ({','.join(map(str, content_bot_ids))}) THEN bot_id END) as content_bots_count,
                COUNT(CASE WHEN bot_id = {shellagent_bot_id} THEN 1 END) as shellagent_messages
            FROM tg2app_bot_running_messages
            WHERE user_id IN (
                SELECT DISTINCT user_id
                FROM tg2app_bot_running_messages
                WHERE bot_id IN ({','.join(map(str, content_bot_ids))})
            )
            GROUP BY user_id
            HAVING first_content_bot_use IS NOT NULL OR first_shellagent_use IS NOT NULL
            ORDER BY user_id
        """)

        journey_data = cursor.fetchall()

        # Categorize users
        content_first = []
        shellagent_first = []
        content_only = []
        shellagent_only = []

        for user_id, content_first_date, shellagent_first_date, bots, sa_msgs in journey_data:
            if content_first_date and shellagent_first_date:
                if content_first_date < shellagent_first_date:
                    content_first.append((user_id, bots, sa_msgs))
                else:
                    shellagent_first.append((user_id, bots, sa_msgs))
            elif content_first_date:
                content_only.append((user_id, bots))
            elif shellagent_first_date:
                shellagent_only.append((user_id, sa_msgs))

        print(f"User Journey Patterns:")
        print(f"  Content Bot → ShellAgent: {len(content_first)} users")
        print(f"  ShellAgent → Content Bot: {len(shellagent_first)} users")
        print(f"  Content Bot only (never used ShellAgent): {len(content_only)} users")
        print(f"  ShellAgent only (never used content bots): {len(shellagent_only)} users")

        conversion_rate = (len(content_first) / len(content_only) * 100) if content_only else 0
        print(f"\n🎯 Conversion rate (Content Bot → ShellAgent): {conversion_rate:.1f}%")

        # Save journey data
        with open(f"{output_dir}/user_journey.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'first_content_bot', 'first_shellagent', 'content_bots_count', 'shellagent_messages'])
            writer.writerows(journey_data)
        print(f"\n💾 Saved to {output_dir}/user_journey.csv")

except Exception as e:
    print(f"❌ Error: {e}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print(f"✨ Analysis complete! Results saved to {output_dir}/")
print("=" * 80)
