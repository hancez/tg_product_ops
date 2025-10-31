# Phase 5: 用户需求整理与可行性评估报告

**分析日期**: 2025-10-25
**数据来源**: Phase 2 用户行为分析 (275 用户)
**评估依据**: product_context.md 产品能力矩阵
**分析目标**: 区分"合理可实现"与"过于不合理"的需求，为算法团队提供优化方向

---

## 📊 执行摘要（Executive Summary）

### 核心发现

1. **高频且可行的需求（优先实现）**:
   - 图片/缩略图生成 bot (71 次) - ✅ 高可行性，当前成功率 17%，需优化 UX
   - AI 聊天/对话 bot (100 次) - ✅ 高可行性，但需改进生成准确度
   - 数据追踪/记录 bot (55 次) - ✅ 高可行性，应推广 Mini App 方案

2. **高频但技术受限的需求（需评估投入）**:
   - 视频下载 bot (41 次) - ⚠️ 中等可行性，技术复杂度高
   - 群组管理 bot (38 次) - ✅ 可行但需专门优化

3. **低频且不可行的需求（明确拒绝）**:
   - 音乐播放 bot (5 次) - ❌ 100% 失败，建议明确告知不支持
   - 支付 bot (3 次) - ❌ 技术与合规难度极高

### 优先级矩阵

| 需求类型 | 频次 | 技术可行性 | 当前成功率 | 优先级 | 建议 |
|---------|------|----------|----------|--------|------|
| 图片生成 bot | 71 | ✅ 高 | 17% | P0 | 优化 UX，提升到 40%+ |
| AI 聊天 bot | 100 | ✅ 高 | 中等 | P0 | 改进意图理解 |
| 数据追踪 bot | 55 | ✅ 高 | 低 | P1 | 推 Mini App 方案 |
| 视频下载 bot | 41 | ⚠️ 中 | 低 | P1 | 评估技术投入 |
| 群组管理 bot | 38 | ✅ 高 | 低 | P1 | 专门优化 |
| 游戏 bot | 27 | ✅ 高 | 中等 | P2 | 保持现状 |
| 定时提醒 bot | 15 | ✅ 高 | 低 | P2 | 长期优化 |
| 音乐播放 bot | 5 | ❌ 低 | 0% | P3 | 明确不支持 |
| 支付 bot | 3 | ❌ 低 | 0% | P3 | 明确不支持 |

---

## 🔍 详细需求分析

---

## 类别 A: 高频且合理可实现（P0 优先级）

---

### A1. 图片/缩略图生成 bot

**需求频次**: 71 次（第 2 高频）
**当前成功率**: 17%（12/71 使用顺畅）
**技术可行性**: ✅ 高（已验证）

#### 用户具体需求（来自 CSV 详细原因）

**典型案例**:
1. Instagram 缩略图生成器（多次提及）
2. AI 艺术生成器（从文本生成图片）
3. Logo 生成器
4. 表情包/Meme 生成器
5. 头像生成器

#### 可行性评估

**参考 product_context.md 能力矩阵**:
```markdown
| Image Generation | AI art bot, thumbnail creator | ✅ High |
| Text→Image | Meme generator, quote cards | ✅ High |
```

✅ **结论**: **完全可行，当前已支持**

#### 问题诊断（为什么成功率只有 17%？）

**根据 Phase 3 分析**:
1. ❌ **UX 问题严重**: 11/71 用户"不会用"
   - 命令式交互不直观（需要 /generate → 上传图片 → 描述）
   - 缺少按钮引导
   - 非英语用户困惑（俄语用户占多数）

2. ❌ **24% 用户仅简单体验**: 17/71 用户试了一下就走
   - 缺少"啊哈时刻"
   - 没有示例 demo
   - 首次使用门槛高

3. ❌ **24% 成人内容请求**: 17/71 尝试生成 NSFW 内容被拒绝
   - 这是合规必要措施，无需改进

#### 优化建议

**建议 1: 改用按钮式引导（Phase 4 最佳实践）**
```diff
- 当前流程（命令式）:
  用户: /start
  Bot: Welcome! To create a thumbnail:
     1. Use /generate to start
     2. Upload your image
     3. Describe your video

+ 改进流程（按钮式）:
  用户: /start
  Bot: 👋 Welcome! Let's create your first thumbnail.

  [🎨 Start Creating]  [📖 How It Works]  [🌐 Language: EN]

  ---

  用户点击 [Start Creating]:
  Bot: Step 1/3: Upload your image 📸

  [用户上传图片]
  Bot: Perfect! ✅ Step 2/3: Tell me about your video

  [用户输入描述]
  Bot: 🎨 Creating your thumbnail... (15 seconds)
  Bot: ✅ Done! [显示结果]
```

**建议 2: 添加快速 Demo 模式**
```diff
+ 用户: /start
+ Bot: 👋 Want to see what I can do?
+
+ [🎨 Try Example Image]  [✨ Create My Own]
+
+ ---
+
+ 用户点击 [Try Example]:
+ Bot: Here's an example thumbnail I created:
+      [显示预制图片]
+
+      Like it? You can create your own in 30 seconds!
+      [✨ Create My Own Thumbnail]
```

**建议 3: 多语言支持（至少俄语）**
- 11 个案例中，至少 7 人是非英语用户（俄语 5 人，波斯语 2 人）
- 建议添加语言检测和俄语支持

**预期改善**:
- 成功率从 17% → **40-50%**
- "不会用"从 11 人 → **2 人以下**
- "仅简单体验"从 17 人 → **5 人以下**

**实施优先级**: **P0（最高）**

---

### A2. AI 聊天/对话 bot

**需求频次**: 100 次（最高频）
**当前成功率**: 中等（未统计具体数据）
**技术可行性**: ✅ 高（已验证）

#### 用户具体需求

**典型案例**:
1. 通用聊天 bot（类似 ChatGPT）
2. 角色扮演 bot（特定人格）
3. 客服 bot（回答特定领域问题）
4. 教育 bot（语言学习、知识问答）
5. 陪伴 bot（情感支持）

#### 可行性评估

**参考 product_context.md 能力矩阵**:
```markdown
| LUI Chat | Q&A bot, conversational planner | ✅ High |
| Text Generation | Blog post drafts, captions | ✅ High |
```

✅ **结论**: **完全可行，当前已支持**

#### 问题诊断

**根据 Phase 2-3 分析**:
1. ❌ **生成类型错误**: 部分用户想要聊天 bot，但生成了其他类型
2. ❌ **功能简单**: 用户期望高级功能（如记忆上下文、个性化），但实际功能基础
3. ✅ **成功率相对较高**: 对话类 bot 相对容易使用

#### 优化建议

**建议 1: 改进 AI 意图理解（避免生成错误类型）**
- 参考 Phase 3 偏差点 5："Bot 生成了错误类型"
- 建议在生成前添加确认步骤：
```diff
+ 用户: I want a chatbot that can answer questions about history
+ Bot: 💭 Let me confirm what you want to create...
+
+ Bot Type: Q&A Chatbot
+ Topic: History
+ Core Features:
+ • Answer questions about historical events
+ • Provide detailed explanations
+ • Support follow-up questions
+
+ [✅ Yes, Create This!]  [✏️ No, Let Me Clarify]
```

**建议 2: 提供聊天 bot 模板库**
```diff
+ 用户: /start
+ Bot: What type of bot do you want to create?
+
+ [💬 Chatbot] [📸 Image Bot] [📝 Tracker] [🎮 Game]
+
+ ---
+
+ 用户点击 [Chatbot]:
+ Bot: Choose a chatbot type:
+
+ [🤖 General AI Chat]  - Like ChatGPT
+ [🎭 Roleplay Bot]     - Specific character
+ [📚 Knowledge Bot]    - Answer domain questions
+ [💬 Customer Support] - Handle inquiries
```

**预期改善**:
- 生成准确率提升 20-30%
- 减少"功能不符合预期"流失

**实施优先级**: **P0（高）**

---

### A3. 数据追踪/记录 bot

**需求频次**: 55 次（第 3 高频）
**当前成功率**: 低
**技术可行性**: ✅ 高（已验证）

#### 用户具体需求

**典型案例**:
1. 习惯追踪器（每日打卡）
2. 支出记录器（财务追踪）
3. 健身记录器（锻炼、饮食）
4. 情绪日记（心情追踪）
5. 工作日志（任务管理）

#### 可行性评估

**参考 product_context.md 能力矩阵**:
```markdown
| CRUD Mini App | Habit tracker, expense log | ✅ High |
```

✅ **结论**: **完全可行，建议优先使用 Mini App**

#### 问题诊断

**为什么成功率低？**
1. ❌ **Bot 交互不适合数据输入**: 表单式输入用对话界面很繁琐
2. ❌ **缺少可视化**: 用户想看图表、日历，但 Bot 无法提供
3. ❌ **数据浏览不便**: Bot 无法展示列表、筛选、搜索

**根本原因**: **数据追踪类需求更适合 Mini App 而非传统 Bot**

#### 优化建议

**建议 1: 智能推荐 Mini App（而非 Bot）**
```diff
+ 用户: Create a habit tracker bot
+ ShellAgent: 💡 Based on your request, I recommend creating a Mini App instead of a bot.
+
+ Why Mini App?
+ ✅ Visual calendar view
+ ✅ Statistics dashboard with charts
+ ✅ Easy data entry with forms
+ ✅ Better user experience for tracking
+
+ [✅ Create Mini App]  [🤖 Create Bot Instead]
```

**建议 2: 提供 CRUD Mini App 模板**
```markdown
模板: Habit Tracker Mini App
功能:
- 每日打卡日历视图
- 添加/编辑习惯
- 统计图表（连续天数、完成率）
- 提醒功能
```

**预期改善**:
- 数据追踪类 bot 成功率从低 → **60%+**（通过 Mini App）
- 用户满意度显著提升

**实施优先级**: **P1（中高）**

---

## 类别 B: 高频但技术受限（P1 优先级，需评估投入）

---

### B1. 视频下载 bot

**需求频次**: 41 次（第 4 高频）
**当前成功率**: 低
**技术可行性**: ⚠️ 中等（技术复杂度高）

#### 用户具体需求

**典型案例**:
1. YouTube 视频下载器
2. Instagram/TikTok 视频下载器
3. Twitter 视频下载器
4. 通用视频/音频提取器

#### 可行性评估

**参考 product_context.md 能力矩阵**:
```markdown
| Video→Text | YouTube video summarizer | ✅ High |
```
（注意：这里是 Video→Text，不是 Video Download）

⚠️ **技术挑战**:
1. ❌ **版权与合规风险**: YouTube、Instagram 等平台禁止未授权下载
2. ❌ **API 限制**: 大部分平台不提供官方下载 API
3. ⚠️ **技术复杂度**: 需要处理多种格式、分辨率、加密
4. ⚠️ **存储与带宽**: 视频文件大，需要 CDN 支持

**当前问题**（Phase 2 分析）:
- bot 功能正常但用户仅简单体验: 10 次
- bot 功能不符合预期: 6 次
- bot 功能有 bug: 5 次

#### 结论与建议

❌ **不建议作为 P0 优先级**

**替代方案**:

**方案 1: 支持"视频摘要"而非"视频下载"**
```markdown
用户: I want a YouTube video downloader
ShellAgent: 💡 Due to copyright restrictions, I can't create a video downloader.

However, I can create a bot that:
✅ Summarizes YouTube videos (extracts key points)
✅ Transcribes video to text
✅ Answers questions about video content

[✅ Create Video Summarizer]  [❌ Cancel]
```

**方案 2: 明确告知不支持，推荐替代方案**
```markdown
ShellAgent: ⚠️ Video downloading violates most platforms' Terms of Service.

I can't create this bot, but here are alternatives:
• Video Summarizer (extract key points)
• Link Saver (bookmark videos)
• Transcript Bot (convert speech to text)

[View Alternatives]
```

**预期结果**:
- 减少"功能不符合预期"投诉
- 提升合规性

**实施优先级**: **P1（评估后决定）**

---

### B2. 群组管理 bot

**需求频次**: 38 次（第 5 高频）
**当前成功率**: 低
**技术可行性**: ✅ 高（但需专门优化）

#### 用户具体需求

**典型案例**:
1. 自动欢迎新成员
2. 反垃圾邮件/过滤
3. 管理员权限管理
4. 自动踢出违规用户
5. 群组统计（活跃度、成员增长）

#### 可行性评估

**参考 product_context.md 能力矩阵**:
```markdown
| Group Moderation | Auto-welcome, spam filter | ✅ High |
```

✅ **结论**: **完全可行**

#### 问题诊断

**为什么成功率低？**
1. ❌ **需求复杂**: 群组管理需要多个功能组合，单一功能不够
2. ❌ **权限配置复杂**: 用户不理解 Telegram Bot 的权限系统
3. ❌ **测试困难**: 用户需要把 bot 加入群组才能测试，门槛高

#### 优化建议

**建议 1: 提供群组管理 bot 专用模板**
```markdown
模板: Group Admin Bot
核心功能（预配置）:
✅ 自动欢迎新成员（可自定义欢迎语）
✅ 反垃圾链接过滤
✅ 自动删除违规消息
✅ 成员统计面板
✅ 自定义规则引擎

一键生成，无需手动配置
```

**建议 2: 简化测试流程**
```diff
+ ShellAgent: ✅ Your Group Admin Bot is ready!
+
+ How to test:
+ 1️⃣ Add @YourBot to your group
+ 2️⃣ Give it admin permissions
+ 3️⃣ Send /start in the group to configure
+
+ [📖 Step-by-Step Guide]  [🎥 Watch Video Tutorial]
```

**预期改善**:
- 群组管理 bot 成功率提升至 40%+
- 降低配置难度

**实施优先级**: **P1（中）**

---

## 类别 C: 中频且可行（P2 优先级，长期优化）

---

### C1. 游戏 bot

**需求频次**: 27 次
**当前成功率**: 中等
**技术可行性**: ✅ 高

#### 用户具体需求
1. 骰子游戏
2. 猜谜游戏
3. 问答/Trivia
4. 文字 RPG
5. 投票/民调

#### 可行性评估
✅ **完全可行**，当前成功率相对较高

#### 建议
- 保持现状，无需优先优化
- 可提供游戏 bot 模板库（长期）

**实施优先级**: **P2（低）**

---

### C2. 定时提醒 bot

**需求频次**: 15 次
**当前成功率**: 低
**技术可行性**: ✅ 高

#### 用户具体需求
1. 每日提醒（喝水、吃药、锻炼）
2. 定时推送（新闻、天气）
3. 任务到期提醒

#### 可行性评估

**参考 product_context.md 能力矩阵**:
```markdown
| Scheduled Tasks | Daily reminders, recurring reports | ✅ High |
```

✅ **完全可行**

#### 问题诊断
- 用户不理解如何设置定时任务
- 缺少时区配置
- 提醒管理界面不友好

#### 建议
- 提供定时提醒 bot 模板
- 添加可视化时间设置（Mini App）

**实施优先级**: **P2（低）**

---

### C3. 翻译 bot

**需求频次**: 12 次
**技术可行性**: ✅ 高

#### 可行性评估
✅ **完全可行**

#### 建议
- 提供翻译 bot 模板
- 支持常见语言对（中英、英俄等）

**实施优先级**: **P2（低）**

---

### C4. 天气 bot

**需求频次**: 7 次
**技术可行性**: ✅ 高

#### 可行性评估

**参考 product_context.md 能力矩阵**:
```markdown
| External APIs | Weather bot, stock tracker | ✅ High |
```

✅ **完全可行**

#### 建议
- 集成免费天气 API（OpenWeatherMap）
- 提供天气 bot 模板

**实施优先级**: **P2（低）**

---

## 类别 D: 低频且不可行（P3 优先级，明确拒绝）

---

### D1. 音乐播放 bot

**需求频次**: 5 次
**当前成功率**: **0%（100% 失败）**
**技术可行性**: ❌ 极低

#### 用户具体需求
1. 播放 Spotify/YouTube 音乐
2. 音乐搜索与推荐
3. 群组音乐播放

#### 可行性评估

**技术与法律障碍**:
1. ❌ **版权问题**: Spotify、YouTube 禁止未授权播放
2. ❌ **API 限制**: 没有合法的音乐播放 API
3. ❌ **Telegram 限制**: Telegram Bot 无法实时播放音频流
4. ❌ **存储成本**: 音乐文件大，需要大量存储

**Phase 2 数据**:
```markdown
音乐播放bot (5次提及)
使用情况分布:
- bot功能不符合预期: 3次
- bot功能有bug: 2次
结论: 100%失败率
```

#### 结论与建议

❌ **不支持，应明确告知用户**

**建议文案**:
```markdown
用户: I want a music player bot
ShellAgent: ⚠️ Sorry, I can't create music player bots due to:
   • Copyright restrictions
   • Telegram API limitations
   • Streaming platform policies

Alternatives I can create:
✅ Music Recommendation Bot (suggest songs)
✅ Lyrics Bot (search and display lyrics)
✅ Playlist Saver (bookmark favorite songs)

[View Alternatives]  [Cancel]
```

**预期结果**:
- 避免浪费用户时间
- 减少"功能不符合预期"投诉

**实施优先级**: **P3（立即实施拒绝提示）**

---

### D2. 支付 bot

**需求频次**: 3 次
**当前成功率**: 极低
**技术可行性**: ❌ 极低

#### 用户具体需求
1. 接受支付（Stripe、PayPal）
2. 加密货币支付
3. 群组收款/分账

#### 可行性评估

**技术与法律障碍**:
1. ❌ **合规难度极高**: 需要 PCI DSS 认证、金融牌照
2. ❌ **安全风险**: 支付信息泄露责任重大
3. ❌ **Telegram 限制**: 支付 API 有严格限制
4. ❌ **用户认证**: KYC/AML 合规要求

#### 结论与建议

❌ **不支持，明确拒绝**

**建议文案**:
```markdown
用户: I want a payment bot
ShellAgent: ⚠️ Sorry, payment bots require:
   • Financial licenses
   • Security certifications
   • Complex compliance (KYC/AML)

I can't create this for legal and security reasons.

Alternatives:
✅ Telegram's built-in payment feature
✅ Link to external payment pages (Stripe, PayPal)

[Learn More]  [Cancel]
```

**实施优先级**: **P3（立即实施拒绝提示）**

---

### D3. 抓取/爬虫 bot（部分不可行）

**需求频次**: 4 次
**技术可行性**: ⚠️ 部分可行

#### 用户具体需求
1. 抓取群组成员 ID
2. 抓取 Instagram 用户照片
3. 抓取网页数据

#### 可行性评估

**参考 product_context.md 能力矩阵**:
```markdown
| Data Scraping | RSS reader, price tracker | ✅ High |
```

⚠️ **部分可行，需区分合法与非法**

**合法场景**:
✅ RSS 订阅
✅ 公开 API 数据抓取（天气、股票）
✅ 自己网站的数据

**非法场景**:
❌ 抓取群组成员（隐私侵犯）
❌ 抓取 Instagram/Facebook（违反 TOS）
❌ 未授权网页抓取

#### 建议

**方案: 区分并明确告知**
```markdown
用户: I want to scrape Instagram photos
ShellAgent: ⚠️ Scraping Instagram violates their Terms of Service.

However, I can create bots that scrape:
✅ Public RSS feeds
✅ Open APIs (weather, news, stocks)
✅ Your own website data

[View Legal Options]  [Cancel]
```

**实施优先级**: **P3（立即实施合规检查）**

---

## 📋 需求优先级总结

### P0 - 立即优化（预期 ROI 最高）

| 需求 | 频次 | 当前问题 | 优化方向 | 预期改善 |
|------|------|---------|---------|---------|
| 图片生成 bot | 71 | UX 差，11 人不会用 | 按钮式引导 + Demo | 17% → 40%+ |
| AI 聊天 bot | 100 | 生成类型错误 | 意图理解 + 确认步骤 | +20-30% 准确率 |

### P1 - 近期优化（显著改善用户体验）

| 需求 | 频次 | 当前问题 | 优化方向 | 预期改善 |
|------|------|---------|---------|---------|
| 数据追踪 bot | 55 | Bot 不适合数据输入 | 推 Mini App 方案 | 低 → 60%+ |
| 视频下载 bot | 41 | 技术+合规难度 | 转为视频摘要 bot | 减少投诉 |
| 群组管理 bot | 38 | 配置复杂 | 模板 + 教程 | 低 → 40%+ |

### P2 - 长期优化（降低优先级）

| 需求 | 频次 | 建议 |
|------|------|------|
| 游戏 bot | 27 | 保持现状 |
| 定时提醒 bot | 15 | 提供模板 |
| 翻译 bot | 12 | 提供模板 |
| 天气 bot | 7 | 集成 API |

### P3 - 明确拒绝（不可行或不合规）

| 需求 | 频次 | 原因 | 建议 |
|------|------|------|------|
| 音乐播放 bot | 5 | 版权+技术限制 | 明确告知不支持 + 替代方案 |
| 支付 bot | 3 | 合规+安全 | 明确拒绝 + 外部方案 |
| 部分爬虫 bot | 4 | 隐私+TOS | 区分合法/非法 |

---

## 🎯 给算法团队的优化方向

### 优化 1: 改进意图理解（P0）

**问题**: 23 人"功能不符合预期"（想要 X，生成了 Y）

**建议**:
1. ✅ 在生成前添加确认步骤，展示 AI 理解的需求
2. ✅ 识别常见意图模式（聊天、图片、下载、追踪、管理）
3. ✅ 当用户需求模糊时，主动询问澄清

**实现方式**:
```python
# 伪代码
user_request = "I want a bot that can help with Instagram"

# 意图识别（多分类）
intent = classify_intent(user_request)
# 可能结果: ["image_generation", "content_download", "analytics"]

if len(intent) > 1 or confidence < 0.8:
    # 需要澄清
    bot.send_message(f"I see you want something related to Instagram. Which one?")
    bot.show_buttons([
        "📸 Generate Instagram-style images",
        "📊 Track Instagram analytics",
        "💾 Download Instagram content (not supported)",
    ])
else:
    # 确认理解
    bot.send_message(f"I'll create a {intent[0]} bot. Is this correct?")
```

---

### 优化 2: 模板库系统（P0）

**问题**: 用户不知道可以创建什么，冷启动困难

**建议**:
建立 bot 模板库，包含以下类别：

**Category 1: 图片生成类**
- AI 艺术生成器
- Instagram 缩略图生成器
- Logo 生成器
- 表情包生成器

**Category 2: 数据追踪类（Mini App）**
- 习惯追踪器
- 支出记录器
- 健身日志
- 情绪日记

**Category 3: 聊天类**
- 通用 AI 聊天
- 角色扮演 bot
- 知识问答 bot
- 客服 bot

**Category 4: 群组工具**
- 群组管理 bot
- 欢迎/告别 bot
- 反垃圾 bot

**Category 5: 其他实用工具**
- 翻译 bot
- 天气 bot
- 提醒 bot
- RSS 订阅 bot

**实现方式**:
```diff
+ 用户: /start
+ Bot: 🎉 Welcome! Choose a category to get started:
+
+ [📸 Image Bots] [📝 Trackers] [💬 Chatbots] [👥 Group Tools]
+
+ Or describe your own idea:
+ [✨ Create Custom Bot]
```

---

### 优化 3: 明确不支持的功能（P3）

**问题**: 用户尝试创建音乐、支付等不可行的 bot，浪费时间

**建议**:
在 AI 生成流程中，添加"不可行检测"：

```python
# 伪代码
forbidden_keywords = [
    "music player", "play music", "spotify",
    "payment", "accept money", "cryptocurrency",
    "scrape instagram", "download facebook", "group member IDs",
]

if any(keyword in user_request.lower() for keyword in forbidden_keywords):
    # 明确拒绝并提供替代方案
    bot.send_rejection_with_alternatives(user_request)
```

**拒绝文案模板**:
```markdown
⚠️ Sorry, I can't create [REQUESTED_BOT_TYPE] due to:
   • [REASON_1]
   • [REASON_2]

Alternatives I can create:
✅ [ALTERNATIVE_1]
✅ [ALTERNATIVE_2]

[View Alternatives]  [Cancel]
```

---

### 优化 4: 智能推荐 Bot vs Mini App（P1）

**问题**: 数据追踪类需求用 Bot 体验差

**建议**:
根据需求类型，智能推荐 Bot 或 Mini App

**判断逻辑**:
```python
def recommend_type(user_request):
    if contains_keywords(user_request, ["track", "log", "record", "habit", "expense"]):
        return "mini_app"  # 数据追踪类推荐 Mini App

    if contains_keywords(user_request, ["chat", "talk", "conversation"]):
        return "bot"  # 对话类推荐 Bot

    if contains_keywords(user_request, ["generate", "create", "image", "picture"]):
        return "bot"  # 生成类推荐 Bot

    if contains_keywords(user_request, ["manage", "admin", "moderate"]):
        return "bot"  # 管理类推荐 Bot

    return "bot"  # 默认 Bot
```

---

## 📄 附录：完整需求清单（按频次排序）

| 排名 | Bot 类型 | 频次 | 技术可行性 | 优先级 | 建议 |
|------|---------|------|----------|--------|------|
| 1 | AI 聊天/对话 bot | 100 | ✅ 高 | P0 | 改进意图理解 |
| 2 | 图片/缩略图生成 bot | 71 | ✅ 高 | P0 | 优化 UX |
| 3 | 数据追踪/记录 bot | 55 | ✅ 高 | P1 | 推 Mini App |
| 4 | 视频下载 bot | 41 | ⚠️ 中 | P1 | 转为摘要 bot |
| 5 | 群组管理 bot | 38 | ✅ 高 | P1 | 专门优化 |
| 6 | 游戏 bot | 27 | ✅ 高 | P2 | 保持现状 |
| 7 | 定时提醒 bot | 15 | ✅ 高 | P2 | 提供模板 |
| 8 | 翻译 bot | 12 | ✅ 高 | P2 | 提供模板 |
| 9 | 天气 bot | 7 | ✅ 高 | P2 | 集成 API |
| 10 | 音乐播放 bot | 5 | ❌ 低 | P3 | 明确拒绝 |
| 11 | 抓取/爬虫 bot | 4 | ⚠️ 部分 | P3 | 区分合法/非法 |
| 12 | 支付 bot | 3 | ❌ 低 | P3 | 明确拒绝 |

---

**Phase 5 完成** ✅

下一步: Phase 6 - 输出交互优化和算法优化的可执行文档
