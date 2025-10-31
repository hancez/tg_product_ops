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
