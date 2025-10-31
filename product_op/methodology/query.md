查询用户和shellagent的对话记录
```
curl --location --request POST 'https://api.myshell.ai/v1/tg2app/admin/list_shellagent_history_msgs' \
--header 'myshell-service-name: organics-api' \
--header 'content-type: application/json' \
--data-raw '{
  "myshell_userid": "35478751"
}'
```


查询用户和哪些bot对话过
```
curl --location --request POST 'https://api.myshell.ai/v1/tg2app/admin/search_uesr_chat_bots' \
--header 'myshell-service-name: organics-api' \
--header 'content-type: application/json' \
--data-raw '{
  "tg_userid": "5009271945"
}'
```


查询用户和指定bot的对话记录
```
curl --location --request POST 'https://api.myshell.ai/v1/tg2app/admin/list_userbot_history_msgs' \
--header 'myshell-service-name: organics-api' \
--header 'content-type: application/json' \
--data-raw '{
  "myshell_userid": "3547875",
  "bot_id": "1957742452589494272"
}'
```