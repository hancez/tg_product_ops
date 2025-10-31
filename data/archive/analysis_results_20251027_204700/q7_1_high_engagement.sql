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
