# Telegram Bot Interaction Overview（上位概览）

本文件为给 AI 合作者的“速览版”，以 `product_op/tgbot/` 目录为准则，汇总最关键的交互事实与可复用话术，避免每次都通读细节文档。需要深入请跳转：
- 交互流程图：`product_op/tgbot/interaction-flows.md`
- 消息文案：`product_op/tgbot/messages.md`
- 命令详解：`product_op/tgbot/commands.md`
- 按钮交互：`product_op/tgbot/buttons.md`
- 状态机：`product_op/tgbot/state-machine.md`
- Webhook/API：`product_op/tgbot/api-endpoints.md`

## 系统与入口（三类 Bot / 三个 Webhook）
- ShellAgent Bot（生成/管理）→ `/v1/tg2app/telegram/generate/webhook`
- Running Bot（用户自己的 Bot）→ `/v1/tg2app/telegram/running/webhook/{bot_id}/{bot_token}`
- Trial / Playground Bot（试用）→ `/v1/tg2app/telegram/trial/webhook`

生产环境常用外链：
- Workshop（Mini App 管理台）：`https://tg-workshop.myshell.ai`（可展示信用余额、已有 Bot 等）

## 黄金路径（新用户首次）
1) 用户发送 `/start` → 机器人英文引导：
```text
Tell me what bot you want to build. One or two sentences are enough.
```
2) 用户用 1–2 句话描述需求 → 机器人进入草稿构建：
```text
Building draft...
```
3) 构建期间，任何用户消息一律统一回复（直到完成）：
```text
ShellAgent_Playground_Bot is still setting up and can’t take messages yet. Please resend your message after setup completes
```
4) 完成后返回“成功卡片”（示例：YouTube 缩略图 Bot）：
```text
✅ Done! Your YouTube thumbnail bot @ShellAgent_Playground_Bot can:
• Generate custom thumbnails for your videos
• Choose from 5 professional styles  
• Add text overlays with your guidance
• Create YouTube-optimized 16:9 images
• Provide multiple options to choose from

To use it:
/start - Get started with the main menu
/generate - Create a new thumbnail
/help - See detailed instructions

🎨 Available styles: Bold & energetic, Clean & professional, Colorful & vibrant, Dramatic & cinematic, Minimalist & modern, or your custom style!

Just message the bot to start creating professional thumbnails!
```
5) 追加余额提示 + Workshop 链接（可点击打开 Mini App 管理）：
```text
⚡ Balance 234 · Est. 2 requests
```
6) 主动引导打开 Playground 预览：
```text
Open Preview @ShellAgent_Playground_Bot
```

备注：以上文案均为最终对外话术，生成/编辑期的“锁定/排队/能量”等逻辑仅在需要时以最少文案暴露。

## 返回用户（有 Bot）
- `/start`：可展示主菜单或直接引导用户继续编辑/管理（详见 commands/buttons）。
- `/mybots` 列表 → 选择某个 Bot → `Edit Bot` → 进入编辑模式（状态重置为 IDLE，直接发文本即可编辑）。

## 关键命令（最小集合）
- ShellAgent（Gen）
  - `/start` 首次引导或返回欢迎
  - `/newbot` 新建 Bot（引导 @BotFather 流程）
  - `/mybots` 管理已有 Bot（Inline 列表 + 详情页）
  - `/currentbot` 查看当前 Bot 信息
  - `/remix` 基于他人 Bot 创建变体（两段式：输入源 Bot 名 → 新 Token）
- Running（用户 Bot）
  - `/start` 终端用户欢迎（或转发到 Bot App）
  - `/subscribe` 订阅管理（如有 Cron 任务）
  - 其他自定义命令 → 转发到用户 Bot App
- Trial / Playground（特殊）
  - `/start` 首次试用欢迎（受 Trial Handler 控制）
  - 管理员：`trybot:{bot_id}` 指定试用目标

## 按钮与键盘（核心模式）
- Inline Keyboard（主）
  - Gen：`SelectBot (select_bot:{id})` / `Edit Bot (edit_bot:{id})` / `Deploy Bot (deploy_bot:{id})` / `<<Back To Bot List (mybots)`
  - Running：`Subscribe/Unsubscribe (subscribe:{name}/unsubscribe:{name})` / `Buy Energy`（URL/WebApp）
- Reply Keyboard（仅 ShellAgent 返回用户展示）
  - 2×2 快捷：`/mybots` `/newbot` `/remix` `/currentbot`
- 注意：`callback_data` ≤ 64 bytes（Telegram 限制）。

## 深链 / Mini App / 能量
- 深链 `start` 参数：`s_kol` / `s_fb` / `s_egy`（能量）/ `s_rmx`（Remix）/ `s_cpg`（活动）/ `s_bdt`（BindToken）。
- Mini App（Workshop）用作：购买/查看能量、管理已有 Bot、后续 Remix/编辑入口。
- 能量（Energy）：不足时在相应场景弹出购买引导与按钮。（详见 messages.md / buttons.md）

## 状态机（对话级）
- `IDLE`（默认）
- `NEWBOT:WAIT_USER_INPUT_BOT_TOKEN`
- `REMIX:WAIT_USER_INPUT_BOT_NAME`
- `REMIX:WAIT_USER_INPUT_BOT_TOKEN`
- `PLAYGROUND:WAIT_USER_INPUT_TOKEN`

要点：
- 编辑/生成时统一加“处理锁”，并在占用时用固定文案回复“still setting up”。
- 完成后重置为 `IDLE`；编辑 Bot 会强制重置为 `IDLE`。

## 可直接复用的话术（最少集）
- 首次引导：
```text
Tell me what bot you want to build. One or two sentences are enough.
```
- 进入构建：
```text
Building draft...
```
- 构建期间统一回复：
```text
ShellAgent_Playground_Bot is still setting up and can’t take messages yet. Please resend your message after setup completes
```
- 余额提示：
```text
⚡ Balance 234 · Est. 2 requests
```
- Playground 预览 CTA：
```text
Open Preview @ShellAgent_Playground_Bot
```

## 查阅指引（当需要细节时）
- 交互流程分支与泳道图 → `interaction-flows.md`
- 粒度到字段级的消息/命令/按钮文案 → `messages.md` / `commands.md` / `buttons.md`
- 状态管理与参数传递 → `state-machine.md`
- Webhook、转发到 Sandbox、回调协议、环境差异 → `api-endpoints.md`

