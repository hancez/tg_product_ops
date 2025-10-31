# Bot Analysis Execution Guide

**Status**: ⚠️ Pending Database Access
**Created**: 2025-10-27
**Output**: `/Users/hancezhang/Claude code exp/product_op/analysis_results_20251027_204700/`

---

## 🚨 Current Situation

**What Happened**:
- ✅ Analysis plan created (`bot_analysis_plan.md`)
- ✅ SQL queries generated (`queries_to_execute.sql`)
- ✅ Insight report drafted (`bot_behavior_insights_report.md`)
- ✅ Execution script created (`execute_analysis.sh`)
- ❌ **SQL queries SKIPPED** - No database credentials

**What's Available**:
- 4 priority SQL query files in `analysis_results_20251027_204700/`:
  - `q1_1_all_users.sql` - Get all 106 user IDs
  - `q1_2_power_users.sql` - Identify users with 2+ bots
  - `q4_2_user_stats.sql` - Per-user message statistics
  - `q7_1_high_engagement.sql` - Users with 100+ messages

---

## 🎯 Three Options to Proceed

### Option 1: You Execute SQL Queries (Fastest)

If you have direct database access:

```bash
# Set your database credentials
export DB_HOST="your_host"
export DB_USER="your_user"
export DB_PASS="your_password"
export DB_NAME="tg2app"

# Re-run the analysis script
cd "/Users/hancezhang/Claude code exp/product_op"
./execute_analysis.sh
```

The script will:
1. Execute 4 priority SQL queries
2. Save results to CSV files
3. Generate an API query script based on user IDs

---

### Option 2: Manual SQL Execution

If you prefer to run queries manually:

**Step 1**: Go to your database tool (MySQL Workbench, DBeaver, etc.)

**Step 2**: Execute these queries in order:

#### Query 1: Get All User IDs (Foundation)
```sql
-- File: analysis_results_20251027_204700/q1_1_all_users.sql
SELECT DISTINCT user_id
FROM tg2app_bot_running_messages
WHERE bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
ORDER BY user_id;
```
**Expected**: ~106 rows (one per user)
**Save as**: `user_ids.csv`

#### Query 2: Power User Analysis (Critical!)
```sql
-- File: analysis_results_20251027_204700/q1_2_power_users.sql
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
```
**Expected**: ~10-50 rows (users with 2+ bots)
**Save as**: `power_users.csv`
**This answers**: How many users use multiple bots? (Critical for strategy)

#### Query 3: Per-User Statistics
```sql
-- File: analysis_results_20251027_204700/q4_2_user_stats.sql
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
```
**Expected**: ~106+ rows (one per user-bot combination)
**Save as**: `user_stats.csv`
**This answers**: Is myshell_thumbmaker_bot's 2832 messages concentrated in a few users?

#### Query 4: High Engagement Users
```sql
-- File: analysis_results_20251027_204700/q7_1_high_engagement.sql
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
```
**Expected**: ~5-20 rows (super users)
**Save as**: `high_engagement_users.csv`
**This answers**: Who are the top 10% users?

---

**Step 3**: Upload CSV files to the analysis directory

```bash
# Move your exported CSV files here:
cp ~/Downloads/user_ids.csv "/Users/hancezhang/Claude code exp/product_op/analysis_results_20251027_204700/"
cp ~/Downloads/power_users.csv "/Users/hancezhang/Claude code exp/product_op/analysis_results_20251027_204700/"
cp ~/Downloads/user_stats.csv "/Users/hancezhang/Claude code exp/product_op/analysis_results_20251027_204700/"
cp ~/Downloads/high_engagement_users.csv "/Users/hancezhang/Claude code exp/product_op/analysis_results_20251027_204700/"
```

---

### Option 3: Provide Query Results to Me

If you run the queries and get results, just paste them here or upload the CSV files, and I'll analyze them immediately.

**Example**:
```
"Here's the power_users.csv result:
user_id,bot_count,total_messages
12345,3,450
67890,2,120
..."
```

---

## 📊 What Each Query Will Tell Us

### Query 1 (All User IDs)
**Question**: Who are the 106 users?
**Why It Matters**: Foundation for all other queries
**Next Action**: Use these IDs for API queries (ShellAgent conversations)

### Query 2 (Power Users) - **MOST CRITICAL**
**Question**: How many users use multiple bots?
**Three Possible Outcomes**:

1. **Low Overlap (<10%)**:
   - Each bot attracts different users
   - Need separate GTM strategy for each bot
   - Hook_Generator ≠ gateway to other bots

2. **Medium Overlap (10-30%)**:
   - Some cross-pollination happening
   - Optimize bot discovery flow
   - Target power users for upsell

3. **High Overlap (>30%)**:
   - Hook_Generator IS a gateway
   - Double down on it as entry point
   - Focus on funnel optimization

**This single query determines entire product strategy!**

### Query 3 (User Stats)
**Question**: Is myshell_thumbmaker_bot's high engagement due to a few super users or evenly distributed?

**Two Scenarios**:
1. **Evenly Distributed** (most users 50-200 messages):
   - Product has strong PMF
   - Should scale it up

2. **Power Law** (2-3 users with 500+ messages, rest <50):
   - Only certain user types need it
   - Target acquisition on those users

### Query 4 (High Engagement)
**Question**: Who are the top 10% users?
**Why It Matters**:
- Interview them (understand what makes them successful)
- Clone their behavior patterns
- Target similar users in acquisition

---

## 🔄 After SQL Queries Complete

Once you have the CSV files, I'll:

1. **Immediate Analysis** (5 minutes):
   - Calculate power user percentage
   - Identify distribution patterns
   - Validate/reject hypotheses from initial report

2. **Deep Dive** (30 minutes):
   - Segment users by behavior
   - Map user journeys
   - Identify churn patterns

3. **API Queries** (if needed):
   - Sample 10-20 users for conversation analysis
   - Understand why Hook_Generator has low retention
   - Understand why myshell_thumbmaker has high retention

4. **Final Report** (1 hour):
   - Data-driven product recommendations
   - GTM strategy adjustments
   - Feature prioritization

---

## 🚀 Quick Start Commands

### If you have database access:
```bash
cd "/Users/hancezhang/Claude code exp/product_op"
export DB_HOST="your_host"
export DB_USER="your_user"
export DB_PASS="your_password"
./execute_analysis.sh
```

### If you prefer manual execution:
```bash
# Open the SQL files:
open "analysis_results_20251027_204700/q1_2_power_users.sql"
# Execute in your database tool
# Export results to CSV
# Upload back to analysis directory
```

### If you want me to wait:
Just say "wait" and execute queries yourself, then share results.

---

## 📝 Current Status Summary

| Task | Status | Files |
|------|--------|-------|
| Analysis Plan | ✅ Complete | `bot_analysis_plan.md` |
| SQL Queries | ✅ Generated | `queries_to_execute.sql` + 4 priority files |
| Insight Report | ✅ Draft | `bot_behavior_insights_report.md` |
| Execution Script | ✅ Ready | `execute_analysis.sh` |
| **SQL Execution** | ⏳ **Pending** | **Need database access** |
| API Queries | ⏸️ Waiting | Need user IDs from SQL first |
| Final Analysis | ⏸️ Waiting | Need SQL results |

---

## ❓ FAQ

**Q: I don't have database credentials. Can you still help?**
A: I need at least the 4 priority SQL query results. You can run them manually and paste the results.

**Q: Which query is most important?**
A: **Query 2 (Power Users)**. This single query determines product strategy.

**Q: Can't you just use the API instead?**
A: The APIs require individual user IDs, which I can only get from SQL Query 1.

**Q: How long will this take?**
A:
- SQL execution: 1-5 minutes (depending on database size)
- My analysis: 5-60 minutes (depending on result size)
- Total: <2 hours for complete analysis

**Q: What if I can only run 1 query?**
A: Run Query 2 (Power Users). It's the most critical.

---

Ready to proceed? Let me know:
1. "I'll run the queries" - I'll wait for your results
2. "Set up database access" - Tell me the credentials
3. "Here are the results" - Paste the CSV data
