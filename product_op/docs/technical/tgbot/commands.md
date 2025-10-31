# Bot 命令详解

本文档详细说明所有 Telegram Bot 支持的命令。

## 命令分类

系统支持三类命令：
1. **Gen Commands (生成命令)**: 在 ShellAgent Bot 中使用，用于管理和创建 Bot
2. **Running Commands (运行命令)**: 在用户创建的 Bot 中使用
3. **Trial Commands (试用命令)**: 在 Playground Bot 中使用（特殊场景）

---

## 一、Gen Commands（ShellAgent Bot 命令）

### 1. /start

**功能**: 启动 Bot，显示欢迎消息和主菜单

**使用场景**:
- 用户首次与 ShellAgent Bot 交互
- 用户想要查看主菜单
- 通过 DeepLink 启动（带参数）

**行为**:
- 检查用户是否已注册，如果是新用户则自动创建账号
- 如果是首次用户（无 Bot）：显示简单的欢迎提示
- 如果是返回用户（有 Bot）：显示完整菜单和快捷命令按钮

**DeepLink 参数支持**:

格式: `/start {param}`

参数类型:
1. **s_kol_v_{value}_bid_{bot_id}** 或 **s_kol_v_{value}_bn_{bot_name}**
   - 来源: KOL 推广
   - 行为: 保存邀请记录

2. **s_fb_v_{value}_bid_{bot_id}** 或 **s_fb_v_{value}_bn_{bot_name}**
   - 来源: 从其他 Bot 跳转
   - 行为: 记录统计数据

3. **s_egy_v_{value}_bid_{bot_id}** 或 **s_egy_v_{value}_bn_{bot_name}**
   - 来源: 能量相关（能量不足跳转）
   - 行为: 显示购买能量的引导
   - value 示例: "noenergy"

4. **s_rmx_v_{value}_bid_{bot_id}** 或 **s_rmx_v_{value}_bn_{bot_name}**
   - 来源: Remix Bot
   - 行为:
     - 如果用户有 Bot：显示 Remix 教程
     - 如果是首次用户：创建试用 Bot 并保存 Remix 关系

5. **s_cpg_v_{value}_bid_{bot_id}** 或 **s_cpg_v_{value}_bn_{bot_name}**
   - 来源: 活动推广
   - 行为: 记录活动统计

6. **s_bdt_v_{value}_bid_{bot_id}** 或 **s_bdt_v_{value}_bn_{bot_name}**
   - 来源: 绑定 Token（Playground Bot）
   - 行为: 设置用户状态为 PLAYGROUND_WAIT_INPUT_TOKEN，引导用户输入 Token

**代码位置**: `internal/domain/service/tg2app/tg_gen_commands/tg_gen_command.start.service.go`

**示例**:
```
用户: /start
Bot: Welcome to ShellAgent! You can create any type of Telegram bot using natural language.
     /newbot - create a new bot
     /mybots - edit your bots
     ...
```

```
用户: /start s_rmx_v_demo_bn_MyAwesomeBot
Bot: You're remixing @MyAwesomeBot. Tell me what bot you want to build based on it.
```

---

### 2. /newbot

**功能**: 创建新的 Telegram Bot

**使用场景**:
- 用户想要创建一个全新的 Bot
- 用户需要添加额外的 Bot

**工作流程**:
1. 设置用户状态为 `NEWBOT_WAIT_USER_INPUT_BOT_TOKEN`
2. 显示从 @BotFather 获取 Bot Token 的教程
3. 等待用户输入 Token
4. 验证 Token 格式和有效性
5. 检查 Token 是否已被使用
6. 保存 Bot 信息并设置为当前 Bot
7. 重置用户状态为 `IDLE`

**输出**:
- 显示详细的 @BotFather 操作教程
- 包含5个步骤的清晰指引

**后续状态**: 用户需要输入 Bot Token（见 State Handler: `NEWBOT_WAIT_USER_INPUT_BOT_TOKEN`）

**代码位置**: `internal/domain/service/tg2app/tg_gen_commands/tg_gen_command.newbot.service.go`

**示例**:
```
用户: /newbot
Bot: 1. Search @BotFather (blue check) and open the chat.
     2. Tap Start (or send /start).
     3. Send /newbot.
     ...

用户: 7089876543:AAH3wE9x-aAbBcCdD1234567890aBcDeFgH
Bot: ✅ Success!
     Your bot @MyNewBot has been successfully registered!
     ...
```

---

### 3. /mybots

**功能**: 查看和管理用户创建的所有 Bot

**使用场景**:
- 用户想要查看自己拥有的 Bot 列表
- 用户想要选择并编辑某个 Bot
- 用户想要切换当前正在编辑的 Bot

**工作流程**:
1. 查询用户的所有 Bot
2. 如果没有 Bot：提示使用 /newbot 创建
3. 如果有 Bot：显示 Bot 列表（每行2个按钮）
4. 用户点击某个 Bot 按钮
5. 显示 Bot 详情和操作选项（Edit Bot / Back To Bot List）
6. 用户点击 Edit Bot：设置为当前 Bot 并进入编辑模式

**按钮布局**:
- Bot 列表：Inline Keyboard，每行最多2个 Bot
- Bot 详情：Inline Keyboard
  - Edit Bot 按钮
  - <<Back To Bot List 按钮

**代码位置**: `internal/domain/service/tg2app/tg_gen_commands/tg_gen_command.mybots.service.go`

**示例**:
```
用户: /mybots
Bot: Choose a bot from the list below:
     [ @Bot1 ]  [ @Bot2 ]
     [ @Bot3 ]  [ @Bot4 ]

用户: 点击 @Bot1
Bot: Bot Selected: @Bot1
     What would you like to do with this bot?
     [ Edit Bot ]
     [ <<Back To Bot List ]

用户: 点击 Edit Bot
Bot: ✅ You've selected Bot1
     📝 Bot Description: A helpful assistant bot
     🚀 Just type in the chat box to let the AI edit the bot.
```

---

### 4. /currentbot

**功能**: 显示用户当前正在编辑的 Bot 的详细信息

**使用场景**:
- 用户想要查看当前选择的 Bot
- 用户忘记了当前正在编辑哪个 Bot
- 用户想要确认 Bot 的配置状态

**输出信息**:
- Bot 名称 (@username)
- Bot ID
- Bot 描述（如果有）
- Bot Token 状态（已配置 / 未配置）

**特殊情况**:
- 如果用户未选择 Bot：提示使用 /mybots 选择
- 如果之前选择的 Bot 已被删除：提示 Bot 不存在

**代码位置**: `internal/domain/service/tg2app/tg_gen_commands/tg_gen_command.currentbot.service.go`

**示例**:
```
用户: /currentbot
Bot: Current Bot Information

     Name: @MyBot
     Bot ID: 123456789
     Description: A helpful customer service bot

     ✅ Bot token is configured
```

---

### 5. /remix

**功能**: 基于现有的 Bot 创建一个新的 Bot（Remix）

**使用场景**:
- 用户想要复制/修改别人的 Bot
- 用户想要基于现有 Bot 创建变体
- 用户看到了喜欢的 Bot 想要自己的版本

**工作流程**:
1. 设置用户状态为 `REMIX_WAIT_USER_INPUT_BOT_NAME`
2. 提示用户输入要 Remix 的 Bot 名称
3. 用户输入 Bot 名称（如 @SourceBot）
4. 系统查找该 Bot 并验证:
   - Bot 是否存在
   - Bot 是否有有效的 Token
   - Bot 是否有运行中的版本
5. 如果验证通过，设置状态为 `REMIX_WAIT_USER_INPUT_BOT_TOKEN`
6. 显示 GIF 教程，提示用户输入新 Bot 的 Token
7. 用户输入新 Token
8. 创建新 Bot 并复制源 Bot 的配置和代码
9. 保存 Remix 关系（用于统计）

**涉及的状态**:
- `REMIX_WAIT_USER_INPUT_BOT_NAME`: 等待输入 Bot 名称
- `REMIX_WAIT_USER_INPUT_BOT_TOKEN`: 等待输入新 Bot Token

**代码位置**:
- Command: `internal/domain/service/tg2app/tg_gen_commands/tg_gen_command.remix.service.go`
- State Handlers: `internal/domain/service/tg2app/tg_gen_states/remix.wait_bot_name.state.service.go`

**示例**:
```
用户: /remix
Bot: Please enter the bot name you want to remix (e.g. @xxxxx)

用户: @AwesomeBot
Bot: [GIF动画]
     ✅ Found Bot @AwesomeBot
     Please enter your new bot token (get it from @BotFather):

用户: 7089876543:AAH3wE9x...
Bot: ✅ Success! Your bot @MyAwesomeBot has been created based on @AwesomeBot
```

---

## 二、Running Commands（用户 Bot 命令）

这些命令在用户创建的 Bot 中使用，由终端用户发送。

### 1. /start

**功能**: 启动用户的 Bot

**使用场景**:
- 终端用户首次与该 Bot 交互
- 用户想要查看 Bot 的功能介绍
- 通过分享链接或搜索进入 Bot

**特殊行为**:
- 如果是 Playground Bot 且用户总消息数 ≤ 1：使用 Trial Command Handler
- 其他情况：转发到用户的 Bot App 处理

**行为**:
- 自动获取或创建用户账号
- 记录用户与 Bot 的关系
- 更新 Bot 统计数据（新用户数等）
- 检查用户能量余额

**代码位置**: `internal/domain/service/tg2app/tg_running_commands/` （如果有自定义逻辑）

**示例**:
```
终端用户: /start
用户Bot: [由 Bot App 自定义的欢迎消息]
```

---

### 2. /subscribe

**功能**: 管理定时任务的订阅

**使用场景**:
- Bot 支持定时任务（Cron Jobs）
- 用户想要接收定时推送
- 用户想要管理自己的订阅

**工作流程**:
1. 查询该 Bot 所有可订阅的定时任务
2. 查询用户已订阅的任务
3. 显示任务列表和订阅状态
4. 用户点击任务按钮进行订阅/取消订阅

**按钮状态**:
- 未订阅: `{task_name}` → 点击订阅
- 已订阅: `{task_name} (subscribed)` → 点击取消订阅

**特殊情况**:
- 如果 Bot 没有定时任务：显示提示消息

**代码位置**: `internal/domain/service/tg2app/tg_running_commands/tg_running_command.subscribe.service.go`

**示例**:
```
终端用户: /subscribe
用户Bot: Click on the buttons below to manage your subscriptions to scheduled tasks:

         Daily News: Get daily tech news at 9 AM
         Weekly Summary: Weekly summary every Monday

         [ Daily News (subscribed) ]
         [ Weekly Summary ]

终端用户: 点击 Weekly Summary
用户Bot: ✅ Successfully subscribed to Weekly Summary
```

---

### 3. 其他自定义命令

**说明**: 除了上述内置命令，用户的 Bot App 可以定义自己的命令

**处理方式**: 系统会将这些命令转发到用户的 Bot Sandbox App 进行处理

**示例**:
- `/help` - 显示帮助
- `/settings` - 设置
- `/menu` - 菜单
- 等等...

---

## 三、Trial Commands（Playground Bot 命令）

这些是 Playground Bot 的特殊命令，仅在特定场景下触发。

### 1. /start（首次使用）

**功能**: Playground Bot 的首次启动欢迎

**触发条件**:
- 用户在 Playground Bot 中发送 /start
- 用户的总消息数 ≤ 1（首次使用）
- Bot 是 Playground Bot

**行为**: 由 Trial Command Handler 自定义处理，通常显示试用引导

**代码位置**: `internal/domain/service/tg2app/tg_trial_commands/tg_trial_command.start.service.go`

---

## 四、管理员命令（Trial Bot 特有）

### trybot:{bot_id}

**功能**: 管理员设置要试用的 Bot

**使用场景**: 内部测试和调试

**权限**: 仅管理员可用（配置在 `config.ThirdParty.Tg2AppTelegram.AdminTgIds`）

**工作流程**:
1. 检查用户是否是管理员
2. 解析 Bot ID
3. 验证 Bot 是否存在
4. 在 Redis 中保存管理员试用的 Bot ID（有效期24小时）
5. 之后管理员的所有消息都会路由到该 Bot

**示例**:
```
管理员: trybot:123456789
Bot: 您接下来要体验 TestBot 了，请在24h内体验, 可以随时通过trybot:<botid>更换体验的bot

管理员: 你好
Bot: [路由到 Bot ID 123456789 进行处理]
```

---

## 五、命令处理优先级

在 ShellAgent Bot (Gen Webhook) 中:
1. 检查是否是命令（以 / 开头）
2. 查找对应的 Command Handler
3. 如果找不到：显示 "Sorry, I don't understand the command"
4. 如果不是命令：
   - 检查用户状态（State）
   - 如果有状态：使用 State Handler 处理
   - 如果无状态（IDLE）：作为 Bot 编辑/生成请求处理

在用户 Bot (Running Webhook) 中:
1. 检查是否是内置 Button callback
2. 检查是否是内置 Command（如 /subscribe）
3. 否则：转发到用户的 Bot Sandbox App 处理

---

## 六、命令验证和错误处理

### 能量验证
所有需要消耗资源的操作都会先检查用户能量:
- 生成/编辑 Bot
- 在用户 Bot 中发送消息

如果能量不足：
- 停止处理
- 显示能量不足提示
- 提供购买能量的按钮
- 记录埋点事件

### 并发控制
生成/编辑 Bot 时使用 Redis 锁防止并发:
- 锁键: `tg2app:bot_generating:{bot_id}`
- 超时: 1分钟（开发环境）/ 5分钟（生产环境）
- 如果获取锁失败：提示 Bot 正在处理中

### Token 验证
创建或 Remix Bot 时的 Token 验证:
1. 格式验证（正则匹配）
2. 调用 Telegram API 验证 Token 有效性
3. 检查 Token 是否已被其他 Bot 使用
4. 获取 Bot 信息并保存

---

## 七、命令扩展指南

### 添加新的 Gen Command
1. 在 `internal/domain/service/tg2app/tg_gen_commands/` 创建新文件
2. 实现 `TgGenCommandHandler` 接口
3. 在 `provider.go` 中注册
4. 在 Command Type 枚举中添加新命令

### 添加新的 Running Command
1. 在 `internal/domain/service/tg2app/tg_running_commands/` 创建新文件
2. 实现 `TgRunningCommandHandler` 接口
3. 在 `provider.go` 中注册
4. 在 Command Type 枚举中添加新命令

---

## 八、命令映射表

| 命令 | Gen Bot | Running Bot | Trial Bot | 说明 |
|------|---------|-------------|-----------|------|
| /start | ✅ | ✅ | ✅ | 启动命令，各场景行为不同 |
| /newbot | ✅ | ❌ | ❌ | 创建新 Bot |
| /mybots | ✅ | ❌ | ❌ | 管理 Bot 列表 |
| /currentbot | ✅ | ❌ | ❌ | 查看当前 Bot |
| /remix | ✅ | ❌ | ❌ | Remix 现有 Bot |
| /subscribe | ❌ | ✅ | ❌ | 订阅管理 |
| trybot:{id} | ❌ | ❌ | ✅ | 管理员测试命令 |
| 自定义命令 | ❌ | ✅ | ✅ | 转发到 Bot App |

---

## 九、快捷键盘（Reply Keyboard）

ShellAgent Bot 在欢迎消息中会显示快捷命令键盘（仅返回用户）:

```
┌─────────────┬─────────────┐
│  /mybots    │  /newbot    │
├─────────────┼─────────────┤
│  /remix     │ /currentbot │
└─────────────┴─────────────┘
```

**特点**:
- 持久显示在聊天输入框上方
- 用户点击即发送对应命令
- 仅在用户有 Bot 时显示
