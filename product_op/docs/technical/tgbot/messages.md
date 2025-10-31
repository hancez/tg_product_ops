# Bot 消息文案汇总

本文档汇总了所有 Bot 向用户发送的消息文案。

## 1. 欢迎和引导消息

### 1.1 首次用户欢迎消息
**场景**: 用户第一次使用，没有任何 Bot
**文案**:
```
Tell me what bot you want to build. One or two sentences are enough.
```

### 1.2 返回用户欢迎消息
**场景**: 用户已有 Bot，执行 /start 命令
**文案**:
```
Welcome to ShellAgent! You can create any type of Telegram bot using natural language.

/newbot - create a new bot
/mybots - edit your bots
/remix - remix a new bot
/currentbot - show your current bot info
```
**附带**: Reply Keyboard（快捷按钮）
- /mybots
- /newbot
- /remix
- /currentbot

## 2. Bot Token 相关消息

### 2.1 获取 Bot Token 教程
**场景**:
- 执行 `/newbot` 命令后
- Remix Bot 时需要新 Token
- BindToken DeepLink

**文案**:
```
1. Search @BotFather (blue check) and open the chat.
2. Tap Start (or send /start).
3. Send /newbot.
4. When asked:
   - Give a name (anything).
   - Give a username ending with bot (e.g., my_cool_bot).
5. BotFather replies "Done!" with your HTTP API token → copy it.
```

### 2.2 Token 验证失败消息

#### 格式错误
**文案**:
```
❌ Invalid bot token format. Please make sure you copied the token correctly from @BotFather. The token should be in the format: 123456789:ABCdefGhIJKlmNoPqrsTUVwxyZ-123456789
```

#### Token 无效或过期
**文案**:
```
❌ Invalid bot token. Please make sure you copied the token correctly from @BotFather.
```

#### Token 已被使用
**文案**:
```
❌ Bot token already used. Please use a different token.
```

#### Bot Token 未设置
**场景**: 用户选择了一个没有 Token 的 Bot
**文案**:
```
⚠️ Your bot token is not set. Please set your bot token to continue using this service. You can regenerate the token from @BotFather and update it in your MyShell settings.
```

#### Bot Token 无效或过期（编辑时）
**场景**: 编辑 Bot 时发现 Token 失效
**文案**:
```
⚠️ Your bot token appears to be invalid or expired. Please update your bot token to continue using this service. You can regenerate the token from @BotFather and update it in your MyShell settings.
```

### 2.3 Bot 创建成功消息
**场景**: 用户成功提供有效的 Bot Token
**文案**:
```
✅ Success!

Your bot @{username} has been successfully registered!

Bot Information:
• Name: {first_name}
• Username: @{username}
• ID: {bot_id}

You can now start building your bot.
```

## 3. Bot 管理消息

### 3.1 查看 Bot 列表

#### 无 Bot
**场景**: 执行 `/mybots` 但用户没有任何 Bot
**文案**:
```
You don't have any bots yet. Use /newbot to create one!
```

#### 有 Bot
**场景**: 执行 `/mybots` 且用户有 Bot
**文案**:
```
Choose a bot from the list below:
```
**附带**: Inline Keyboard（每行2个 Bot 按钮）

### 3.2 选择 Bot 后
**场景**: 用户点击某个 Bot 按钮
**文案**:
```
Bot Selected: @{bot_name}

What would you like to do with this bot?
```
**附带**: Inline Keyboard
- Edit Bot 按钮
- <<Back To Bot List 按钮

### 3.3 编辑 Bot 确认
**场景**: 用户点击 Edit Bot 按钮
**文案**:
```
✅ You've selected {bot_name}

📝 Bot Description:
{bot_description}

🚀 Just type in the chat box to let the AI edit the bot.
```
**Callback Query 提示**:
```
✨ Bot selected successfully!
```

### 3.4 当前 Bot 信息

#### 未选择 Bot
**场景**: 执行 `/currentbot` 但未选择当前 Bot
**文案**:
```
You haven't selected a bot yet. Use /mybots to select one!
```

#### Bot 不存在
**场景**: 之前选择的 Bot 已被删除
**文案**:
```
Your previously selected bot no longer exists. Use /mybots to select another one!
```

#### 显示当前 Bot 信息
**场景**: 成功查询当前 Bot
**文案**:
```
Current Bot Information

Name: @{bot_name}
Bot ID: {bot_id}
Description: {description}  // 如果有

✅ Bot token is configured  // 或 ❌ Bot token not configured
```

### 3.5 未选择 Bot 提示
**场景**: 用户发送消息但未选择当前 Bot（且有其他 Bot）
**文案**:
```
Please select a Bot first before we can begin our building journey! 🚀
```

**场景**: 用户尝试编辑但没有选择 Bot
**文案**:
```
You haven't selected a bot yet. Use /mybots and edit bot to select one!
```

## 4. Bot 生成和编辑消息

### 4.1 接收请求提示
**场景**: 用户发送消息开始生成/编辑 Bot（正式 Bot）
**文案**:
```
Your request has been received! 💪 We're hard at work building @{bot_name} for you right now. Please bear with us! 👷‍♀️⚙️
This usually takes 5–10 minutes. You can leave the chat, and we'll notify you once it's finished.
```

**场景**: 试用 Bot（Playground Bot）
**文案**:
```
Building draft...
```

### 4.2 Bot 正在处理中
**场景**: Bot 当前正在生成/编辑，无法接收新消息
**文案**:
```
{bot_name} is still setting up and can't take messages yet. Please resend your message after setup completes
```

### 4.3 部署成功
**场景**: 用户点击 Deploy Bot 按钮后
**文案**:
```
🚀 Bot @{bot_name} has been deployed successfully!
```

## 5. Remix 相关消息

### 5.1 输入 Bot 名称提示
**场景**: 执行 `/remix` 命令
**文案**:
```
Please enter the bot name you want to remix (e.g. @xxxxx)
```

### 5.2 Bot 不存在或无效
**场景**: 输入的 Bot 名称找不到或无 Token
**文案**:
```
❌ Bot @{bot_name} does not exist or has no bot-token, please enter a correct bot name
```

### 5.3 Bot 无运行版本
**场景**: Bot 存在但没有可用的运行版本
**文案**:
```
❌ Bot @{bot_name} has no available running version
```

### 5.4 找到 Bot，等待新 Token
**场景**: 找到要 Remix 的 Bot
**文案**:
```
✅ Found Bot @{bot_name}

Please enter your new bot token (get it from @BotFather):
```
**附带**: GIF 动画教程（newbot-tutorial.gif）

### 5.5 Remix 启动（已有 Bot 的用户）
**场景**: 通过 DeepLink 启动 Remix，用户已有 Bot
**文案**:
```
You're remixing @{bot_name}. Before you start, you need to get your bot token. Here is how:
1. Search @BotFather (blue check) and open the chat.
2. Tap Start (or send /start).
3. Send /newbot.
4. When asked:
   - Give a name (anything).
   - Give a username ending with bot (e.g., my_cool_bot).
5. BotFather replies "Done!" with your HTTP API token → copy it.
```

### 5.6 Remix 启动（首次用户）
**场景**: 通过 DeepLink 启动 Remix，用户是首次使用
**文案**:
```
You're remixing @{bot_name}. Tell me what bot you want to build based on it. One or two sentences are enough.
```

## 6. 能量相关消息

### 6.1 能量不足（生成 Bot 场景）
**场景**: 在 ShellAgent Bot 中编辑，能量为0
**文案**:
```
⚠️ You don't have enough energy. Please buy energy to continue. Remaining Energy: 0
```
**附带**: Inline Keyboard
- Buy Energy 按钮（跳转到购买页面）

### 6.2 能量不足（运行 Bot 场景）
**场景**: 在用户自己的 Bot 中交互，能量为0
**文案**:
```
⚠️ You don't have enough energy. Please click the button below and open workshop to buy energy
```
**附带**: Inline Keyboard
- Buy Energy 按钮

### 6.3 Energy DeepLink 消息
**场景**: 通过 Energy 相关的 DeepLink 启动
**文案**:
```
Click the button below to open workshop and buy energy or view details
```
**附带**: Inline Keyboard
- Buy Or View Energy 按钮（打开 Mini App）

## 7. 命令相关消息

### 7.1 未知命令
**场景**: 用户发送了不支持的命令
**文案**:
```
Sorry, I don't understand the command '{command}'. Please use /start to see available commands.
```

### 7.2 订阅管理（/subscribe）

#### 无可订阅任务
**场景**: Bot 没有定时任务
**文案**:
```
Bot doesn't have any scheduled tasks available for subscription.
```

#### 显示订阅列表
**场景**: Bot 有可订阅的定时任务
**文案**:
```
Click on the buttons below to manage your subscriptions to scheduled tasks:

{task_name_1}: {description_1}
{task_name_2}: {description_2}
...
```
**附带**: Inline Keyboard（每个任务一个按钮）
- 已订阅: "{task_name} (subscribed)" → 点击取消订阅
- 未订阅: "{task_name}" → 点击订阅

## 8. 错误和异常消息

### 8.1 文件过大
**场景**: 用户发送的文件超过20MB
**文案**:
```
⚠️ The file you sent is too large to process (maximum size is 20MB). Please try with a smaller file.
```

### 8.2 Bot 工作异常
**场景**: 转发到用户 Bot App 失败
**文案**:
```
the bot is not working properly, please try again later.
request_id: {trace_id}
```

### 8.3 Webhook URL 为空
**场景**: Bot 没有配置 Webhook URL
**系统日志**: `webhook url is empty, bot_id: {bot_id}, user_id: {user_id}`

## 9. Trial/Playground Bot 特殊消息

### 9.1 管理员未设置试用 Bot
**场景**: 管理员在 Trial Bot 中操作但未设置试用的 Bot
**文案**:
```
请先使用 trybot:<bot-id> 设置要测试的bot
```

### 9.2 管理员设置试用 Bot 成功
**场景**: 管理员执行 `trybot:<bot_id>`
**文案**:
```
您接下来要体验 {bot_name} 了，请在24h内体验, 可以随时通过trybot:<botid>更换体验的bot
```

### 9.3 管理员 Bot 不存在
**场景**: 管理员设置的 Bot ID 无效
**文案**:
```
Bot with ID {bot_id} not found
```

### 9.4 普通用户无当前 Bot
**场景**: 普通用户在 Trial Bot 中操作但没有当前 Bot
**系统日志**: `no current bot found for tg_user_id: {tg_user_id}`

### 9.5 首次使用 Trial Bot（/start）
**场景**: 用户第一次在 Playground Bot 中发送 /start（总消息数<=1）
**文案**: （由 Trial Command Handler 自定义处理）

## 10. DeepLink 特殊场景消息

### 10.1 BindToken DeepLink
**场景**: 用户通过 BindToken DeepLink 启动
**文案**:
```
1. Search @BotFather (blue check) and open the chat.
2. Tap Start (or send /start).
3. Send /newbot.
4. When asked:
   - Give a name (anything).
   - Give a username ending with bot (e.g., my_cool_bot).
5. BotFather replies "Done!" with your HTTP API token → copy it.
```
**后续**: 用户状态设置为 `PLAYGROUND_WAIT_USER_INPUT_TOKEN`

## 11. 按钮文案

### 11.1 Inline Keyboard 按钮

#### 能量相关
- **Buy Energy**: 购买能量（跳转到购买页面或 DeepLink）
- **Buy Or View Energy**: 购买或查看能量（打开 Mini App）

#### Bot 管理
- **@{bot_name}**: Bot 选择按钮（SelectBot）
- **Edit Bot**: 编辑 Bot
- **<<Back To Bot List**: 返回 Bot 列表
- **Deploy Bot**: 部署 Bot

#### 订阅管理
- **{task_name}**: 未订阅，点击订阅
- **{task_name} (subscribed)**: 已订阅，点击取消订阅

### 11.2 Reply Keyboard 按钮

快捷命令按钮（2x2布局）:
- `/mybots`
- `/newbot`
- `/remix`
- `/currentbot`

## 12. 多媒体内容

### 12.1 GIF 动画
- **newbot-tutorial.gif**: 创建新 Bot 教程动画
  - URL: `https://www.myshellstatic.com/image/t2tg/newbot-tutorial.gif`
  - 使用场景: Remix Bot 时引导用户

## 13. 消息解析模式

大部分消息使用 `ParseMode: models.ParseModeHTML`，支持以下 HTML 标签：
- `<b>text</b>`: 粗体
- `<i>text</i>`: 斜体
- `<code>text</code>`: 等宽字体
- `<a href="url">text</a>`: 链接

## 14. 回复参数（Reply Parameters）

某些错误消息会使用 ReplyParameters 回复用户的原始消息：
```go
ReplyParameters: &models.ReplyParameters{
    MessageID: update.Message.ID,
}
```

使用场景：
- 文件过大错误
- 其他需要明确指向用户消息的错误提示
