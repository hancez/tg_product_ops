-- ============================================
-- Bot User Behavior Analysis - SQL Queries
-- Date: 2025-10-27
-- Purpose: Deep dive into 8 content creator bots
-- ============================================

-- ============================================
-- SECTION 1: USER ID EXTRACTION
-- ============================================

-- Q1.1: Get all unique users for each bot
-- This is the foundation for all subsequent queries

-- Hook_Generator_Bot (67 users expected)
SELECT DISTINCT user_id, 'Hook_Generator_Bot' as bot_name
FROM tg2app_bot_running_messages
WHERE bot_id = 1965760104392110080
ORDER BY user_id;

-- myshell_thumbmaker_bot (18 users expected)
SELECT DISTINCT user_id, 'myshell_thumbmaker_bot' as bot_name
FROM tg2app_bot_running_messages
WHERE bot_id = 1970046615507873792
ORDER BY user_id;

-- BRoll_Generator_Bot (4 users expected)
SELECT DISTINCT user_id, 'BRoll_Generator_Bot' as bot_name
FROM tg2app_bot_running_messages
WHERE bot_id = 1972858715723681792
ORDER BY user_id;

-- XtoVideoScriptTransformer_Bot (3 users expected)
SELECT DISTINCT user_id, 'XtoVideoScriptTransformer_Bot' as bot_name
FROM tg2app_bot_running_messages
WHERE bot_id = 1974427421370437632
ORDER BY user_id;

-- xPostGenerator_Bot (4 users expected)
SELECT DISTINCT user_id, 'xPostGenerator_Bot' as bot_name
FROM tg2app_bot_running_messages
WHERE bot_id = 1974701461545680896
ORDER BY user_id;

-- CFLinkedinPostBot (3 users expected)
SELECT DISTINCT user_id, 'CFLinkedinPostBot' as bot_name
FROM tg2app_bot_running_messages
WHERE bot_id = 1974829619605544960
ORDER BY user_id;

-- Viral_Idea_Spark_Bot (5 users expected)
SELECT DISTINCT user_id, 'Viral_Idea_Spark_Bot' as bot_name
FROM tg2app_bot_running_messages
WHERE bot_id = 1975400765027258368
ORDER BY user_id;

-- X_Rival_Analysis_bot (2 users expected)
SELECT DISTINCT user_id, 'X_Rival_Analysis_bot' as bot_name
FROM tg2app_bot_running_messages
WHERE bot_id = 1975961906457870336
ORDER BY user_id;

-- Combined: All users across all 8 bots
SELECT DISTINCT user_id
FROM tg2app_bot_running_messages
WHERE bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
ORDER BY user_id;


-- ============================================
-- SECTION 2: POWER USER ANALYSIS
-- ============================================

-- Q1.2: Identify users who use multiple bots
SELECT
    user_id,
    COUNT(DISTINCT bot_id) as bot_count,
    GROUP_CONCAT(DISTINCT tb.name ORDER BY tb.name) as bot_names,
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
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
GROUP BY user_id
HAVING bot_count >= 2
ORDER BY bot_count DESC, total_messages DESC;

-- Q1.2b: Distribution of power users
SELECT
    bot_count as '使用bot数',
    COUNT(*) as '用户数',
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT user_id) FROM tg2app_bot_running_messages WHERE bot_id IN (
        1965760104392110080, 1970046615507873792, 1972858715723681792,
        1974427421370437632, 1974701461545680896, 1974829619605544960,
        1975400765027258368, 1975961906457870336
    )), 2) as '占比%'
FROM (
    SELECT
        user_id,
        COUNT(DISTINCT bot_id) as bot_count
    FROM tg2app_bot_running_messages
    WHERE bot_id IN (
        1965760104392110080, 1970046615507873792, 1972858715723681792,
        1974427421370437632, 1974701461545680896, 1974829619605544960,
        1975400765027258368, 1975961906457870336
    )
    GROUP BY user_id
) t1
GROUP BY bot_count
ORDER BY bot_count DESC;


-- ============================================
-- SECTION 3: USER ACTIVITY LEVELS
-- ============================================

-- Q1.3: Total bots created by these users (not limited to the 8 bots)
-- Note: Requires user_ids from Section 1 results
-- Replace [USER_IDS] with actual comma-separated user IDs

-- Template:
/*
SELECT
    user_id,
    COUNT(*) as total_bots_created,
    COUNT(CASE WHEN id IN (
        1965760104392110080, 1970046615507873792, 1972858715723681792,
        1974427421370437632, 1974701461545680896, 1974829619605544960,
        1975400765027258368, 1975961906457870336
    ) THEN 1 END) as target_bots_count
FROM tg2app_tg_bots
WHERE user_id IN ([USER_IDS])
GROUP BY user_id
ORDER BY total_bots_created DESC;
*/


-- ============================================
-- SECTION 4: USAGE PATTERNS & RETENTION
-- ============================================

-- Q4.2: Per-user message statistics and usage span
SELECT
    user_id,
    tb.name as bot_name,
    COUNT(*) as total_messages,
    MIN(created_at) as first_message_time,
    MAX(created_at) as last_message_time,
    TIMESTAMPDIFF(DAY, MIN(created_at), MAX(created_at)) as usage_span_days,
    TIMESTAMPDIFF(HOUR, MIN(created_at), MAX(created_at)) as usage_span_hours,
    CASE
        WHEN COUNT(*) >= 100 THEN 'High Engagement (100+)'
        WHEN COUNT(*) >= 50 THEN 'Medium Engagement (50-99)'
        WHEN COUNT(*) >= 20 THEN 'Low Engagement (20-49)'
        ELSE 'Very Low Engagement (<20)'
    END as engagement_level
FROM tg2app_bot_running_messages t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
WHERE t1.bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
GROUP BY user_id, t1.bot_id, tb.name
ORDER BY total_messages DESC, usage_span_days DESC;


-- Q4.2b: Aggregate usage patterns by bot
SELECT
    tb.name as bot_name,
    COUNT(DISTINCT t1.user_id) as unique_users,
    COUNT(*) as total_messages,
    ROUND(AVG(total_messages_per_user), 2) as avg_messages_per_user,
    ROUND(AVG(usage_span_days), 2) as avg_usage_span_days,
    MAX(usage_span_days) as max_usage_span_days,
    SUM(CASE WHEN usage_span_days >= 7 THEN 1 ELSE 0 END) as users_retained_7days,
    ROUND(SUM(CASE WHEN usage_span_days >= 7 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT t1.user_id), 2) as '7day_retention_%'
FROM (
    SELECT
        user_id,
        bot_id,
        COUNT(*) as total_messages_per_user,
        TIMESTAMPDIFF(DAY, MIN(created_at), MAX(created_at)) as usage_span_days
    FROM tg2app_bot_running_messages
    WHERE bot_id IN (
        1965760104392110080, 1970046615507873792, 1972858715723681792,
        1974427421370437632, 1974701461545680896, 1974829619605544960,
        1975400765027258368, 1975961906457870336
    )
    GROUP BY user_id, bot_id
) t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
GROUP BY t1.bot_id, tb.name
ORDER BY avg_messages_per_user DESC;


-- ============================================
-- SECTION 5: MESSAGE TEMPORAL PATTERNS
-- ============================================

-- Q4.1: Message distribution by hour of day
SELECT
    tb.name as bot_name,
    HOUR(created_at) as hour_of_day,
    COUNT(*) as message_count,
    COUNT(DISTINCT user_id) as unique_users
FROM tg2app_bot_running_messages t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
WHERE t1.bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
GROUP BY t1.bot_id, tb.name, hour_of_day
ORDER BY tb.name, hour_of_day;


-- Q4.1b: Message distribution by day of week
SELECT
    tb.name as bot_name,
    DAYNAME(created_at) as day_of_week,
    DAYOFWEEK(created_at) as day_number,
    COUNT(*) as message_count,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT DATE(created_at)) as unique_days
FROM tg2app_bot_running_messages t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
WHERE t1.bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
GROUP BY t1.bot_id, tb.name, day_of_week, day_number
ORDER BY tb.name, day_number;


-- ============================================
-- SECTION 6: REMIX ANALYSIS
-- ============================================

-- Q3.1: Remix details for myshell_thumbmaker_bot
SELECT
    source_bot_id,
    target_bot_id,
    tb_source.name as source_bot_name,
    tb_target.name as target_bot_name,
    tb_target.user_id as remixer_user_id,
    created_at as remix_time
FROM tg2app_bot_remix_relations t1
LEFT JOIN tg2app_tg_bots tb_source ON t1.source_bot_id = tb_source.id
LEFT JOIN tg2app_tg_bots tb_target ON t1.target_bot_id = tb_target.id
WHERE source_bot_id = 1970046615507873792;


-- Q3.1b: Check if remixer was original bot user
-- (Requires joining with usage data)
SELECT
    remix.target_bot_id,
    remix.remixer_user_id,
    CASE
        WHEN usage.user_id IS NOT NULL THEN 'Yes - Was User'
        ELSE 'No - New User'
    END as was_original_user,
    COALESCE(usage.message_count, 0) as original_bot_message_count
FROM (
    SELECT
        target_bot_id,
        tb_target.user_id as remixer_user_id
    FROM tg2app_bot_remix_relations
    LEFT JOIN tg2app_tg_bots tb_target ON tg2app_bot_remix_relations.target_bot_id = tb_target.id
    WHERE source_bot_id = 1970046615507873792
) remix
LEFT JOIN (
    SELECT
        user_id,
        COUNT(*) as message_count
    FROM tg2app_bot_running_messages
    WHERE bot_id = 1970046615507873792
    GROUP BY user_id
) usage ON remix.remixer_user_id = usage.user_id;


-- ============================================
-- SECTION 7: ENGAGEMENT COHORT ANALYSIS
-- ============================================

-- Q7.1: High engagement users (100+ messages)
SELECT
    t1.user_id,
    tb.name as bot_name,
    COUNT(*) as message_count,
    TIMESTAMPDIFF(DAY, MIN(created_at), MAX(created_at)) as usage_span_days,
    ROUND(COUNT(*) * 1.0 / NULLIF(TIMESTAMPDIFF(DAY, MIN(created_at), MAX(created_at)), 0), 2) as messages_per_day
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


-- Q7.2: Compare engagement across bot types
SELECT
    tb.name as bot_name,
    ROUND(AVG(CASE WHEN message_count >= 100 THEN 1.0 ELSE 0.0 END) * 100, 2) as 'pct_high_engagement_%',
    ROUND(AVG(CASE WHEN message_count >= 50 THEN 1.0 ELSE 0.0 END) * 100, 2) as 'pct_medium_engagement_%',
    ROUND(AVG(CASE WHEN message_count >= 20 THEN 1.0 ELSE 0.0 END) * 100, 2) as 'pct_low_engagement_%',
    ROUND(AVG(CASE WHEN message_count < 20 THEN 1.0 ELSE 0.0 END) * 100, 2) as 'pct_very_low_engagement_%'
FROM (
    SELECT
        bot_id,
        user_id,
        COUNT(*) as message_count
    FROM tg2app_bot_running_messages
    WHERE bot_id IN (
        1965760104392110080, 1970046615507873792, 1972858715723681792,
        1974427421370437632, 1974701461545680896, 1974829619605544960,
        1975400765027258368, 1975961906457870336
    )
    GROUP BY bot_id, user_id
) t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
GROUP BY t1.bot_id, tb.name
ORDER BY pct_high_engagement_% DESC;


-- ============================================
-- SECTION 8: BOT CREATION TIMELINE
-- ============================================

-- Q8.1: When were these bots created?
SELECT
    id as bot_id,
    name as bot_name,
    user_id as creator_user_id,
    created_at as bot_created_time,
    TIMESTAMPDIFF(DAY, created_at, NOW()) as days_since_creation
FROM tg2app_tg_bots
WHERE id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
ORDER BY created_at;


-- Q8.2: First and last message timestamps for each bot
SELECT
    tb.name as bot_name,
    MIN(t1.created_at) as first_usage,
    MAX(t1.created_at) as last_usage,
    TIMESTAMPDIFF(DAY, MIN(t1.created_at), MAX(t1.created_at)) as active_days,
    TIMESTAMPDIFF(DAY, MAX(t1.created_at), NOW()) as days_since_last_use
FROM tg2app_bot_running_messages t1
LEFT JOIN tg2app_tg_bots tb ON t1.bot_id = tb.id
WHERE t1.bot_id IN (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
GROUP BY t1.bot_id, tb.name
ORDER BY last_usage DESC;


-- ============================================
-- END OF QUERIES
-- ============================================

-- Notes:
-- 1. Some queries require user_ids from previous results - marked with [USER_IDS]
-- 2. All timestamps assume MySQL/MariaDB datetime functions
-- 3. Adjust GROUP_CONCAT limits if needed (default is 1024 chars)
-- 4. Consider adding LIMIT clauses for large result sets
