# Telegram Bot 交互流程图

## 1. 整体用户旅程

```mermaid
graph TD
    Start[用户打开 Telegram] --> SearchBot[搜索 ShellAgent Bot]
    SearchBot --> SendStart[发送 /start]
    SendStart --> CheckUser{是否新用户?}

    CheckUser -->|是| CreateUser[创建用户账号]
    CheckUser -->|否| ExistingUser[加载用户信息]

    CreateUser --> CheckBots{是否有 Bot?}
    ExistingUser --> CheckBots

    CheckBots -->|无| FirstTime[首次使用流程]
    CheckBots -->|有| ReturningUser[返回用户流程]

    FirstTime --> ShowWelcome[显示欢迎消息:<br/>Tell me what bot you want to build]
    ReturningUser --> ShowMenu[显示主菜单:<br/>/newbot /mybots /remix /currentbot]

    ShowWelcome --> UserInput[用户输入 Bot 想法]
    ShowMenu --> UserChoice{用户选择}

    UserChoice -->|/newbot| NewBotFlow[创建新 Bot 流程]
    UserChoice -->|/mybots| MyBotsFlow[管理已有 Bot 流程]
    UserChoice -->|/remix| RemixFlow[Remix Bot 流程]
    UserChoice -->|/currentbot| CurrentBotFlow[查看当前 Bot]
    UserChoice -->|直接输入| UserInput

    UserInput --> ProcessInput[处理用户输入并生成 Bot]
```

## 2. 创建新 Bot 流程（/newbot）

```mermaid
sequenceDiagram
    participant U as 用户
    participant SB as ShellAgent Bot
    participant BF as BotFather
    participant SYS as 系统后端
    participant DB as 数据库

    U->>SB: /newbot
    SB->>DB: 设置用户状态为 WAIT_BOT_TOKEN
    SB->>U: 显示获取 Bot Token 教程<br/>1. 搜索 @BotFather<br/>2. 发送 /newbot<br/>3. 设置名称和用户名<br/>4. 复制 HTTP API token

    U->>BF: 按照教程操作
    BF->>U: 返回 Bot Token

    U->>SB: 粘贴 Bot Token
    SB->>SYS: 验证 Token 格式

    alt Token 无效
        SYS->>U: ❌ Invalid bot token format
    else Token 已被使用
        SYS->>DB: 检查 Token 是否存在
        SYS->>U: ❌ Bot token already used
    else Token 有效
        SYS->>DB: 保存 Bot 信息
        SYS->>DB: 设置为当前 Bot
        SYS->>DB: 重置用户状态为 IDLE
        SYS->>U: ✅ Success!<br/>Your bot @xxx has been successfully registered!<br/>Bot Information:<br/>• Name: xxx<br/>• Username: @xxx<br/>• ID: xxx<br/><br/>You can now start building your bot.
    end
```

## 3. 管理已有 Bot 流程（/mybots）

```mermaid
sequenceDiagram
    participant U as 用户
    participant SB as ShellAgent Bot
    participant DB as 数据库

    U->>SB: /mybots
    SB->>DB: 查询用户的 Bot 列表

    alt 无 Bot
        SB->>U: You don't have any bots yet.<br/>Use /newbot to create one!
    else 有 Bot
        SB->>U: Choose a bot from the list below:<br/>[显示 Bot 按钮列表，每行2个]

        U->>SB: 点击某个 Bot 按钮
        SB->>DB: 获取 Bot 详情
        SB->>U: Bot Selected: @xxx<br/>What would you like to do with this bot?<br/>[Edit Bot 按钮]<br/>[<<Back To Bot List 按钮]

        alt 点击 Edit Bot
            U->>SB: 点击 Edit Bot
            SB->>DB: 设置为当前 Bot
            SB->>DB: 设置用户状态为 IDLE
            SB->>U: ✅ You've selected xxx<br/>📝 Bot Description: xxx<br/>🚀 Just type in the chat box to let the AI edit the bot.
        else 点击返回
            U->>SB: 点击 <<Back To Bot List
            SB->>U: 返回 Bot 列表界面
        end
    end
```

## 4. Bot 编辑和生成流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant SB as ShellAgent Bot
    participant DB as 数据库
    participant MQ as 消息队列
    participant MS as Modal Sandbox
    participant AI as AI 生成服务

    Note over U,AI: 前提：用户已选择当前 Bot

    U->>SB: 输入文本（描述想要的功能）
    SB->>DB: 检查用户能量余额

    alt 能量不足
        SB->>U: ⚠️ You don't have enough energy.<br/>Please buy energy to continue.<br/>Remaining Energy: 0<br/>[Buy Energy 按钮]
    else 能量充足
        SB->>DB: 检查 Bot 是否正在处理中（加锁）

        alt Bot 正在处理
            SB->>U: xxx is still setting up and can't take messages yet.<br/>Please resend your message after setup completes
        else 可以处理
            SB->>DB: 设置处理锁（1-5分钟）
            SB->>U: Your request has been received! 💪<br/>We're hard at work building @xxx for you right now.<br/>Please bear with us! 👷‍♀️⚙️<br/>This usually takes 5–10 minutes.<br/>You can leave the chat, and we'll notify you once it's finished.

            SB->>DB: 保存消息记录
            SB->>MQ: 发送生成任务到消息队列

            MQ->>MS: 创建或复用 Sandbox
            MS->>AI: 调用 AI 生成 Bot 代码
            AI->>MS: 返回生成的代码
            MS->>DB: 保存生成结果
            MS->>SB: 回调通知完成

            SB->>DB: 释放处理锁
            SB->>U: 更新之前的提示消息或发送新消息<br/>✅ Bot setup complete!<br/>[Deploy Bot 按钮] 或其他操作按钮
        end
    end
```

## 5. Remix Bot 流程

```mermaid
sequenceDiagram
    participant U as 用户
    participant SB as ShellAgent Bot
    participant DB as 数据库

    U->>SB: /remix
    SB->>DB: 设置用户状态为 REMIX_WAIT_BOT_NAME
    SB->>U: Please enter the bot name you want to remix (e.g. @xxxxx)

    U->>SB: 输入 @bot_name
    SB->>DB: 根据名称查询 Bot

    alt Bot 不存在
        SB->>U: ❌ Bot @xxx does not exist or has no bot-token,<br/>please enter a correct bot name
    else Bot 无运行版本
        SB->>U: ❌ Bot @xxx has no available running version
    else Bot 存在且可用
        SB->>U: [GIF 动画]<br/>✅ Found Bot @xxx<br/>Please enter your new bot token (get it from @BotFather):
        SB->>DB: 设置用户状态为 REMIX_WAIT_BOT_TOKEN<br/>保存源 Bot 信息到状态参数

        U->>SB: 输入新的 Bot Token
        SB->>DB: 验证并保存新 Bot
        SB->>DB: 复制源 Bot 的配置和代码
        SB->>DB: 保存 Remix 关系
        SB->>U: ✅ Success! Your bot @xxx has been created<br/>based on @source_bot
    end
```

## 6. DeepLink 启动流程（带参数的 /start）

```mermaid
graph TD
    Start[用户点击 DeepLink] --> ParseParam{解析参数类型}

    ParseParam -->|s_kol_v_xxx| KolSource[KOL 来源]
    ParseParam -->|s_fb_v_xxx| FromBot[来自其他 Bot]
    ParseParam -->|s_egy_v_xxx| Energy[能量相关]
    ParseParam -->|s_rmx_v_xxx| RemixLink[Remix Bot]
    ParseParam -->|s_cpg_v_xxx| Campaign[活动来源]
    ParseParam -->|s_bdt_v_xxx| BindToken[绑定 Token]

    KolSource --> SaveInvite[保存邀请记录]
    FromBot --> SaveStats[保存统计数据]

    Energy --> CheckBots{是否有 Bot?}
    CheckBots -->|有| ShowEnergyBtn[显示: Click the button below to open workshop<br/>and buy energy or view details<br/>[Buy Or View Energy 按钮]]
    CheckBots -->|无| WelcomeMsg[显示欢迎消息]

    RemixLink --> CheckUserBots{用户是否有 Bot?}
    CheckUserBots -->|有| ShowRemixGuide[显示 Remix 教程:<br/>You're remixing @xxx. Before you start,<br/>you need to get your bot token. Here is how:<br/>1. Search @BotFather<br/>2. Tap Start<br/>3. Send /newbot<br/>...]
    CheckUserBots -->|无| CreateTrial[创建试用 Bot<br/>并显示: You're remixing @xxx.<br/>Tell me what bot you want to build based on it.]

    BindToken --> SetState[设置状态为 PLAYGROUND_WAIT_INPUT_TOKEN]
    SetState --> ShowTokenGuide[显示获取 Token 教程]

    SaveInvite --> Continue[继续正常流程]
    SaveStats --> Continue
    ShowEnergyBtn --> Continue
    WelcomeMsg --> Continue
    ShowRemixGuide --> Continue
    CreateTrial --> Continue
    ShowTokenGuide --> Continue

    Continue --> ShowFinal[显示最终欢迎消息或菜单]
```

## 7. 用户 Bot 运行流程（Running Webhook）

```mermaid
sequenceDiagram
    participant EU as 终端用户
    participant UB as 用户的 Bot
    participant SYS as 系统后端
    participant DB as 数据库
    participant APP as Bot Sandbox App

    EU->>UB: 发送消息/命令
    UB->>SYS: Webhook 请求到 Running Webhook
    SYS->>DB: 验证 Bot Token
    SYS->>DB: 获取或创建用户
    SYS->>DB: 保存消息记录
    SYS->>DB: 检查用户能量

    alt 能量不足
        SYS->>UB: ⚠️ You don't have enough energy.<br/>Please click the button below and open workshop to buy energy<br/>[Buy Energy 按钮]
    else 能量充足
        SYS->>DB: 更新 Bot-User 关系

        alt 是后端内置按钮
            SYS->>SYS: 处理内置按钮逻辑
        else 是命令
            alt 是 /subscribe
                SYS->>DB: 查询可订阅的定时任务
                SYS->>UB: 显示订阅管理界面<br/>[任务1 按钮] [任务2 按钮] ...
            else 是 /start
                alt 是首次使用且是 Playground Bot
                    SYS->>UB: 显示试用欢迎消息
                else 其他情况
                    SYS->>APP: 转发到用户 Bot App
                end
            else 其他命令
                SYS->>APP: 转发到用户 Bot App
            end
        else 是普通消息
            SYS->>DB: 获取运行版本的 Webhook URL
            SYS->>APP: 转发完整的 Update 对象（含文件 URL）
            APP->>APP: 处理用户逻辑
            APP->>SYS: 回调返回响应
            SYS->>UB: 发送响应给终端用户
        end
    end
```

## 8. 试用 Bot 流程（Trial Webhook）

```mermaid
sequenceDiagram
    participant U as 用户
    participant TB as Trial/Playground Bot
    participant SYS as 系统后端
    participant DB as 数据库

    U->>TB: 与 Playground Bot 交互
    TB->>SYS: Webhook 到 Trial Webhook

    alt 用户是管理员
        alt 是 trybot 命令
            U->>TB: trybot:<bot_id>
            SYS->>DB: 设置管理员要试用的 Bot ID（24小时）
            SYS->>U: 您接下来要体验 xxx 了，请在24h内体验
        else 已设置试用 Bot
            SYS->>DB: 获取管理员当前试用的 Bot
            SYS->>SYS: 使用该 Bot 处理请求
        else 未设置试用 Bot
            SYS->>U: 请先使用 trybot:<bot-id> 设置要测试的bot
        end
    else 普通用户
        SYS->>DB: 获取用户当前选择的 Bot
        alt 无当前 Bot
            SYS->>U: no current bot found
        else 有当前 Bot
            SYS->>SYS: 转发到 Running Webhook 处理
        end
    end
```

## 9. 用户状态机

```mermaid
stateDiagram-v2
    [*] --> IDLE: 初始/重置

    IDLE --> NEWBOT_WAIT_BOT_TOKEN: 执行 /newbot
    IDLE --> REMIX_WAIT_BOT_NAME: 执行 /remix
    IDLE --> PLAYGROUND_WAIT_INPUT_TOKEN: BindToken DeepLink
    IDLE --> IDLE: 普通消息（生成/编辑 Bot）

    NEWBOT_WAIT_BOT_TOKEN --> IDLE: 输入有效 Token
    NEWBOT_WAIT_BOT_TOKEN --> NEWBOT_WAIT_BOT_TOKEN: 输入无效 Token（重试）

    REMIX_WAIT_BOT_NAME --> REMIX_WAIT_BOT_TOKEN: 输入有效 Bot 名称
    REMIX_WAIT_BOT_NAME --> REMIX_WAIT_BOT_NAME: 输入无效名称（重试）

    REMIX_WAIT_BOT_TOKEN --> IDLE: 输入有效 Token（创建 Remix Bot）
    REMIX_WAIT_BOT_TOKEN --> REMIX_WAIT_BOT_TOKEN: 输入无效 Token（重试）

    PLAYGROUND_WAIT_INPUT_TOKEN --> IDLE: 输入有效 Token（绑定成功）
    PLAYGROUND_WAIT_INPUT_TOKEN --> PLAYGROUND_WAIT_INPUT_TOKEN: 输入无效 Token（重试）

    note right of IDLE
        IDLE 状态下用户可以：
        - 执行各种命令
        - 发送消息编辑当前 Bot
        - 点击按钮
    end note
```

## 10. 能量检查流程

```mermaid
graph TD
    UserAction[用户发送消息] --> CheckEnergy{检查能量余额}

    CheckEnergy -->|余额 = 0| NoEnergy[显示能量不足提示]
    CheckEnergy -->|余额 > 0| ProcessRequest[处理请求]

    NoEnergy -->|生成 Bot 场景| GenNoEnergy[⚠️ You don't have enough energy.<br/>Please buy energy to continue.<br/>Remaining Energy: 0<br/>[Buy Energy 按钮]]

    NoEnergy -->|运行 Bot 场景| RunNoEnergy[⚠️ You don't have enough energy.<br/>Please click the button below and<br/>open workshop to buy energy<br/>[Buy Energy 按钮]]

    GenNoEnergy --> TrackEvent[记录埋点事件]
    RunNoEnergy --> TrackEvent
    TrackEvent --> End[结束]

    ProcessRequest --> Continue[继续正常流程]
```
