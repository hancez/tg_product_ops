#!/usr/bin/env python3
"""
Bot User Behavior Analysis - SQL Query Executor
Uses Python to execute SQL queries and save results to CSV
"""

import os
import sys
import csv
from datetime import datetime

def load_env():
    """Load environment variables from .env file"""
    env_vars = {}
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    return env_vars

def execute_query(cursor, query, query_name):
    """Execute a SQL query and return results"""
    print(f"  Executing: {query_name}...")
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        print(f"  ✅ Success: {len(results)} rows returned")
        return columns, results
    except Exception as e:
        print(f"  ❌ Failed: {str(e)}")
        return None, None

def save_to_csv(columns, results, filename):
    """Save query results to CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(results)
    print(f"  💾 Saved to: {filename}")

def main():
    print("🔍 Bot User Behavior Analysis - SQL Executor")
    print("=" * 50)
    print()

    # Load configuration
    print("📂 Loading configuration...")
    env = load_env()

    DB_HOST = env.get('DB_HOST')
    DB_PORT = int(env.get('DB_PORT', 3306))
    DB_USER = env.get('DB_USER')
    DB_PASS = env.get('DB_PASS')
    DB_NAME = env.get('DB_NAME')

    if not all([DB_HOST, DB_USER, DB_PASS, DB_NAME]):
        print("❌ Missing database configuration in .env file")
        sys.exit(1)

    print(f"   Host: {DB_HOST}")
    print(f"   Database: {DB_NAME}")
    print()

    # Try to import pymysql
    try:
        import pymysql
    except ImportError:
        print("❌ pymysql not installed. Installing...")
        os.system(f"{sys.executable} -m pip install pymysql")
        import pymysql

    # Connect to database
    print("🔌 Connecting to database...")
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            connect_timeout=10
        )
        print("✅ Connected successfully!")
        print()
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        sys.exit(1)

    cursor = conn.cursor()

    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"analysis_results_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output directory: {output_dir}")
    print()

    # Query 1: All Users
    print("Query 1: All User IDs")
    query1 = """
    SELECT DISTINCT user_id
    FROM tg2app_bot_running_messages
    WHERE bot_id IN (
        1965760104392110080, 1970046615507873792, 1972858715723681792,
        1974427421370437632, 1974701461545680896, 1974829619605544960,
        1975400765027258368, 1975961906457870336
    )
    ORDER BY user_id
    """
    cols, results = execute_query(cursor, query1, "q1_all_users")
    if results:
        save_to_csv(cols, results, f"{output_dir}/q1_all_users.csv")
    print()

    # Query 2: Power Users (MOST CRITICAL)
    print("Query 2: Power User Analysis ⭐")
    query2 = """
    SELECT
        user_id,
        COUNT(DISTINCT bot_id) as bot_count,
        SUM(message_count) as total_messages
    FROM (
        SELECT
            user_id,
            bot_id,
            COUNT(*) as message_count
        FROM tg2app_bot_running_messages
        WHERE bot_id IN (
            1965760104392110080, 1970046615507873792, 1972858715723681792,
            1974427421370437632, 1974701461545680896, 1974829619605544960,
            1975400765027258368, 1975961906457870336
        )
        GROUP BY user_id, bot_id
    ) t1
    GROUP BY user_id
    HAVING bot_count >= 2
    ORDER BY bot_count DESC, total_messages DESC
    """
    cols, results = execute_query(cursor, query2, "q2_power_users")
    if results:
        save_to_csv(cols, results, f"{output_dir}/q2_power_users.csv")
    print()

    # Query 3: Per-User Statistics
    print("Query 3: Per-User Message Statistics")
    query3 = """
    SELECT
        user_id,
        tb.name as bot_name,
        COUNT(*) as total_messages,
        MIN(t1.created_at) as first_message_time,
        MAX(t1.created_at) as last_message_time,
        TIMESTAMPDIFF(DAY, MIN(t1.created_at), MAX(t1.created_at)) as usage_span_days
    FROM tg2app_bot_running_messages t1
    LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
    WHERE t1.bot_id IN (
        1965760104392110080, 1970046615507873792, 1972858715723681792,
        1974427421370437632, 1974701461545680896, 1974829619605544960,
        1975400765027258368, 1975961906457870336
    )
    GROUP BY user_id, t1.bot_id, tb.name
    ORDER BY total_messages DESC
    """
    cols, results = execute_query(cursor, query3, "q3_user_stats")
    if results:
        save_to_csv(cols, results, f"{output_dir}/q3_user_stats.csv")
    print()

    # Query 4: High Engagement Users
    print("Query 4: High Engagement Users (100+ messages)")
    query4 = """
    SELECT
        t1.user_id,
        tb.name as bot_name,
        COUNT(*) as message_count,
        TIMESTAMPDIFF(DAY, MIN(created_at), MAX(created_at)) as usage_span_days
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
    cols, results = execute_query(cursor, query4, "q4_high_engagement")
    if results:
        save_to_csv(cols, results, f"{output_dir}/q4_high_engagement.csv")
    print()

    # Close connection
    cursor.close()
    conn.close()

    print("=" * 50)
    print("✨ Analysis execution complete!")
    print(f"📊 Results saved to: {output_dir}/")
    print()
    print("Next steps:")
    print("  1. Review CSV files in output directory")
    print("  2. Claude Code will analyze results automatically")
    print()

if __name__ == "__main__":
    main()
