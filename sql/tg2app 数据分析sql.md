# tg2app 数据分析sql

- 使用botname(不是昵称)查询 botid, 使用人数, 消息数
    
    ```protobuf
    select
          t1.bot_id,
          tb.name as bot_name,
          t1.使用人数,
          t1.消息数
      from (
          select
              bot_id,
              count(distinct(user_id)) as '使用人数',
              count(*) as '消息数'
          from tg2app_bot_running_messages
          where bot_id in (
              select id
              from tg2app_tg_bots
              where name in (
                  "myshell_thumbmaker_bot",
                  "Hook_Generator_Bot",
                  "xPostGenerator_Bot",
                  "Viral_Idea_Spark_Bot",
                  "CFLinkedinPostBot",
                  "BRoll_Generator_Bot",
                  "XtoVideoScriptTransformer_Bot",
                  "X_Rival_Analysis_bot"
              )
          )
          group by bot_id
      ) t1
      left join tg2app_tg_bots tb on t1.bot_id = tb.id;
    ```
    
- 用botid查询聊天记录
    - src
        - send是用户发送
        - reply是回复
    
    ```protobuf
    select * from tg2app_bot_running_messages where bot_id in (1965760104392110080);
    
    ```
    
- 使用bot-id查询对话人数
    
    ```protobuf
    select count(distinct(user_id) from tg2app_bot_running_messages where bot_id in (1965760104392110080);
    
    ```
    
- 使用bot-id查询对话user-id
    
    ```protobuf
    select distinct(user_id) from tg2app_bot_running_messages where bot_id in (1965760104392110080);
    
    ```
    
- 用userid查询和shellagentbot的对话消息
    
    ```protobuf
    select * from tg2app_bot_messages where user_id in (37148573);
    
    ```
    
- 用userid查询用户的bot数
    
    ```protobuf
    select user_id,count(*) from tg2app_tg_bots where user_id in (37148573) group by user_id;
    
    ```
    
- 用botid查询被remix的次数
    
    ```protobuf
    select source_bot_id,count(*) from tg2app_bot_remix_relations where source_bot_id in (1965760104392110080);
    
    ```