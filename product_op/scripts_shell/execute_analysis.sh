#!/bin/bash

# ============================================
# Bot User Behavior Analysis - Execution Script
# Date: 2025-10-27
# ============================================

set -e  # Exit on error

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="/Users/hancezhang/Claude code exp/product_op/analysis_results_${TIMESTAMP}"
mkdir -p "${OUTPUT_DIR}"

echo "📊 Starting Bot User Behavior Analysis..."
echo "Output directory: ${OUTPUT_DIR}"
echo ""

# ============================================
# PART 1: SQL QUERIES (Requires database access)
# ============================================

echo "⚠️  NOTE: SQL queries require database access"
echo "If you have database credentials, export them as:"
echo "  export DB_HOST=..."
echo "  export DB_USER=..."
echo "  export DB_PASS=..."
echo "  export DB_NAME=tg2app"
echo ""

# Check if database credentials are set
if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ]; then
    echo "❌ Database credentials not found. Skipping SQL queries."
    echo "   Please set DB_HOST, DB_USER, DB_PASS environment variables."
    echo ""
    SKIP_SQL=true
else
    SKIP_SQL=false
    echo "✅ Database credentials found. Executing SQL queries..."
fi

# Function to execute SQL query
execute_sql() {
    local query_name=$1
    local sql_file=$2

    if [ "$SKIP_SQL" = false ]; then
        echo "  Executing: ${query_name}..."
        mysql -h"${DB_HOST}" -u"${DB_USER}" -p"${DB_PASS}" "${DB_NAME}" \
            < "${sql_file}" \
            > "${OUTPUT_DIR}/${query_name}.csv" 2>&1

        if [ $? -eq 0 ]; then
            echo "  ✅ Saved to ${query_name}.csv"
        else
            echo "  ❌ Failed: ${query_name}"
        fi
    fi
}

# Generate individual SQL files from main query file
echo "📝 Generating SQL query files..."

# Q1.1: All users across all bots
cat > "${OUTPUT_DIR}/q1_1_all_users.sql" << 'EOF'
SELECT DISTINCT user_id
FROM tg2app_bot_running_messages
WHERE bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
ORDER BY user_id;
EOF

# Q1.2: Power User Analysis
cat > "${OUTPUT_DIR}/q1_2_power_users.sql" << 'EOF'
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
ORDER BY bot_count DESC, total_messages DESC;
EOF

# Q4.2: Per-user message statistics
cat > "${OUTPUT_DIR}/q4_2_user_stats.sql" << 'EOF'
SELECT
    user_id,
    tb.name as bot_name,
    COUNT(*) as total_messages,
    MIN(created_at) as first_message_time,
    MAX(created_at) as last_message_time,
    TIMESTAMPDIFF(DAY, MIN(created_at), MAX(created_at)) as usage_span_days
FROM tg2app_bot_running_messages t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
WHERE t1.bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
GROUP BY user_id, t1.bot_id, tb.name
ORDER BY total_messages DESC;
EOF

# Q7.1: High engagement users
cat > "${OUTPUT_DIR}/q7_1_high_engagement.sql" << 'EOF'
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
ORDER BY message_count DESC;
EOF

# Execute priority queries
if [ "$SKIP_SQL" = false ]; then
    echo ""
    echo "🔍 Executing Priority SQL Queries..."
    execute_sql "q1_1_all_users" "${OUTPUT_DIR}/q1_1_all_users.sql"
    execute_sql "q1_2_power_users" "${OUTPUT_DIR}/q1_2_power_users.sql"
    execute_sql "q4_2_user_stats" "${OUTPUT_DIR}/q4_2_user_stats.sql"
    execute_sql "q7_1_high_engagement" "${OUTPUT_DIR}/q7_1_high_engagement.sql"
fi

# ============================================
# PART 2: API QUERIES (Requires user IDs from Part 1)
# ============================================

echo ""
echo "📡 Preparing API queries..."

# Check if we have user IDs from SQL queries
if [ -f "${OUTPUT_DIR}/q1_1_all_users.csv" ]; then
    echo "✅ User IDs available. Generating API query script..."

    # Create API query script
    cat > "${OUTPUT_DIR}/execute_api_queries.sh" << 'EOFAPI'
#!/bin/bash

# This script will be generated after SQL queries complete
# It will query ShellAgent conversations for sampled users

API_OUTPUT_DIR="./api_results"
mkdir -p "${API_OUTPUT_DIR}"

# Read user IDs from SQL result
# (Will be populated after SQL execution)

echo "API queries will be generated here..."
EOFAPI

    chmod +x "${OUTPUT_DIR}/execute_api_queries.sh"
else
    echo "⚠️  User IDs not available. API queries will need to be run separately."
    echo "   After SQL queries complete, run the generated API script."
fi

# ============================================
# PART 3: Summary
# ============================================

echo ""
echo "================================"
echo "📊 Analysis Execution Summary"
echo "================================"
echo ""
echo "Output directory: ${OUTPUT_DIR}"
echo ""

if [ "$SKIP_SQL" = true ]; then
    echo "⚠️  SQL queries were SKIPPED (no database credentials)"
    echo ""
    echo "To execute SQL queries manually:"
    echo "  1. Set database environment variables:"
    echo "     export DB_HOST=your_db_host"
    echo "     export DB_USER=your_db_user"
    echo "     export DB_PASS=your_db_pass"
    echo "     export DB_NAME=tg2app"
    echo ""
    echo "  2. Re-run this script: ./execute_analysis.sh"
    echo ""
    echo "Or execute SQL files manually:"
    ls -1 "${OUTPUT_DIR}"/*.sql
else
    echo "✅ SQL queries executed. Results saved to:"
    ls -1 "${OUTPUT_DIR}"/*.csv 2>/dev/null || echo "  (No results yet)"
fi

echo ""
echo "📝 Next Steps:"
echo "  1. Review SQL query results in: ${OUTPUT_DIR}/"
echo "  2. Run API queries (if needed): ${OUTPUT_DIR}/execute_api_queries.sh"
echo "  3. Analyze results with Claude Code"
echo ""
echo "✨ Done!"
