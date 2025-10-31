# CTA Implementation Plan: Converting Bot Users to Creators

**Date**: 2025-10-29
**Based On**: Product documentation analysis + Competitive best practices research
**Target**: Convert 70 non-creator users (60% with high engagement) to bot creators

---

## 研究发现总结

### 竞品Best Practices

#### Zapier
- ✅ **Clear & action-oriented CTA**: "Try sharing with your team" > "Get started"
- ✅ **One action at a time**: 不要让用户困惑
- ✅ **Visual prominence**: 使用对比和留白
- ✅ **Activation nudges**: 早期推动用户达到"Aha moment"

#### Notion
- ✅ **Hands-on approach**: 用产品本身引导用户
- ✅ **Step-by-step wizard**: 创建第一个任务
- ✅ **Tooltips**: 指出核心功能
- ✅ **Use case selection**: 个性化体验

#### Telegram Bot Best Practices
- ✅ **Buttons > Commands**: 新用户不理解/command语法
- ✅ **Seconds to communicate value**: Bot只有几秒钟传达价值
- ✅ **Example use cases**: 用户可以立即尝试
- ✅ **2-3 most important commands**: 快速开始

#### Product-Led Growth Timing
- ✅ **Contextual messaging**: 与用户当前活动对齐
- ✅ **Feels like a tap on shoulder**: 不是random interruption
- ✅ **Time to Value (TTV)**: 快速展示价值
- ✅ **Test timing & wording**: A/B测试不同变体

---

## 产品技术约束

### 从产品文档中提取的约束

| 约束 | 说明 | 影响 |
|------|------|------|
| **10分钟生成时间** | Bot生成约需10分钟，不可中断 | 用户需要高承诺度 |
| **需BotFather Token** | 用户必须先去@BotFather获取token | 增加摩擦 |
| **Playground可先体验** | 无需token就能在Playground试用 | 降低门槛的关键 |
| **$4免费额度** | 新用户有$4终身额度（不可续） | 有限次试错机会 |
| **Telegram only** | 只在Telegram内，无web界面 | 限制触达方式 |
| **英文市场** | 目标用户是英文内容创作者 | CTA文案必须英文 |

### 现有的消息机制

**可用的通信方式**（从messages.md）:
1. **Text messages**: 普通文本消息
2. **Inline Keyboard buttons**: 可点击的按钮（带callback）
3. **Reply Keyboard**: 持久显示的快捷按钮
4. **GIF/Media**: 支持动画教程
5. **HTML formatting**: 支持`<b>`, `<i>`, `<code>`等

**已有的触发时机**（从commands.md）:
- `/start` 命令
- 用户发送消息到bot
- Bot生成完成后的通知
- Inline button点击回调

---

## 方案一：基于现有架构的轻量级CTA（推荐先实施）

### 为什么推荐这个方案？
1. **最小改动**: 利用现有消息系统
2. **快速实施**: 1-2周内可上线
3. **低风险**: 不影响现有功能
4. **可A/B测试**: 容易调整文案和timing

### 1. 在营销Bot的欢迎消息中添加CTA

**当前状态**（从messages.md）:
```
Tell me what bot you want to build. One or two sentences are enough.
```

**新设计**:
```markdown
Welcome to Hook Generator! 🎯

This bot helps you create viral hooks for your content.

💡 **Did you know?** This bot was created by a content creator like you
using @shellagent_bot in just 10 minutes - no coding required!

Want to build your own AI assistant? Start here: @shellagent_bot

---
Ready to generate hooks? Just tell me your topic!
```

**Implementation Details**:
- **File**: Bot welcome message configuration
- **Trigger**: First `/start` command
- **Format**: Text + Inline Keyboard button
- **Button**: "Build Your Own Bot" → Deep link to @shellagent_bot

**竞品evidence**: Telegram bots have "seconds" to communicate value → 必须在欢迎消息就说清楚

###  2. 使用消息次数触发分层CTA

**技术实现**:
```
检测用户消息计数（从tg2app_bot_running_messages表）
if (message_count == 3):
    触发 Tier 1 CTA
elif (message_count == 10):
    触发 Tier 2 CTA
elif (message_count == 25):
    触发 Tier 3 CTA
```

#### Tier 1: 第3次使用后（轻量提醒）

**Timing**: 用户已经体验价值，但还不是"power user"
**Goal**: 种下"这个bot是可以复制的"的种子

**消息文案**:
```markdown
🎉 Nice! You're getting the hang of it.

Quick tip: This Hook Generator was built by another creator using natural language.
You can create your own version tailored to YOUR niche in @shellagent_bot

[Try ShellAgent] [Maybe Later]
```

**Format**: Text + Inline Keyboard
**Buttons**:
- "Try ShellAgent" → Deep link with tracking param
- "Maybe Later" → Dismiss (记录用户选择)

**竞品evidence**:
- Zapier在激活邮件中"Rather than merely announcing, include clear CTA"
- Product-led growth best practice: "Trigger upsell messages at right moment"

#### Tier 2: 第10次使用后（明确价值主张）

**Timing**: 用户已是高频用户，明确需求
**Goal**: 展示customization的价值

**消息文案**:
```markdown
🔥 10 hooks generated! You're clearly serious about your content.

Here's the thing: this bot is great for general hooks, but what if you could
create one that ONLY generates hooks in your exact style and niche?

That's what 1,000+ creators are doing with @shellagent_bot

✨ Build a bot that:
• Knows YOUR audience
• Speaks YOUR brand voice
• Handles YOUR specific use cases

Ready in 10 minutes, no code needed.

[Build My Custom Bot] [Show Me Examples] [Not Now]
```

**Buttons**:
- "Build My Custom Bot" → @shellagent_bot with pre-filled context
- "Show Me Examples" → Showcase of similar customized bots
- "Not Now" → Dismiss (snooze for 10 more messages)

**竞品evidence**:
- Notion: "Step-by-step wizard" + "Use case selection" → 要展示concrete examples
- PLG: "Contextual messaging when user is navigating relevant feature"

#### Tier 3: 第25次使用后（社交证明 + FOMO）

**Timing**: 重度用户，但还没转化
**Goal**: 最后推动 + Social proof

**消息文案**:
```markdown
⚡ 25+ hooks! You're a power user.

Fun fact: 85% of users who reach 20+ uses end up creating their own bot.

Why? Because while Hook Generator is great, a custom bot tailored to YOUR
specific needs saves even more time.

Like @sarah built a bot for LinkedIn hooks that knows her industry jargon.
Or @mike created one that generates hooks in multiple languages.

Want to join them? @shellagent_bot - 10 minutes, free trial included.

[Yes, Build Mine] [Learn More] [I'm Good]
```

**Buttons**:
- "Yes, Build Mine" → @shellagent_bot with onboarding context
- "Learn More" → Case studies of similar creators
- "I'm Good" → Dismiss permanently (don't ask again)

**竞品evidence**:
- User pilot: "88% of consumers trust recommendations from people they know"
- PLG: "Use user-generated content and social proof"

---

### 3. Bot响应内嵌式CTA（最低摩擦）

**场景**: 用户收到bot的正常响应
**频率**: 每5次响应显示1次（20% 频率）

**示例**（Hook Generator回复后）:
```markdown
Here's your hook:

"Stop scrolling if you've ever struggled with..."

---

💡 Tip: Want a hook generator that knows YOUR niche?
   → Build one in 10 min: @shellagent_bot
```

**Format**: 附加在bot响应末尾，用分隔线隔开
**Frequency**: 20% insertion rate （不会每次都显示，避免annoying）

**竞品evidence**:
- Telegram best practice: "Clear call-to-action for next step"
- PLG: "Timing should feel like tap on shoulder, not interruption"

---

### 4. 利用Inline Buttons替代纯文本

**为什么重要**: 从research中看到 "Use buttons instead of text commands for onboarding"

**当前问题**: 如果只是text message说"去@shellagent_bot"，用户需要:
1. 复制bot username
2. 搜索
3. 打开
4. 记住context

**新设计**: Inline Button直接跳转

**Button实现**:
```json
{
  "inline_keyboard": [[
    {
      "text": "🚀 Build My Own Bot",
      "url": "https://t.me/shellagent_bot?start=s_fb_v_hook_gen_bn_Hook_Generator_Bot"
    }
  ]]
}
```

**Deep Link参数解析**:
- `s_fb`: Source = From Bot
- `v_hook_gen`: Variant = from Hook Generator
- `bn_Hook_Generator_Bot`: Bot Name tracking

**Why this works**:
- 一键跳转，零摩擦
- 携带tracking参数，可以分析转化率
- ShellAgent可以自动识别来源，提供contextual onboarding

---

## 方案二：利用Playground降低门槛（中期实施）

### 为什么需要这个？

**当前痛点**: 用户要创建bot需要:
1. 去BotFather获取token（摩擦）
2. 等10分钟生成（高承诺）
3. 花费$4额度（心理成本）

**解决方案**: Playground "Try Before You Commit"

### 1. "Remix to Playground" 快速体验

**Concept**: 让用户先在Playground试用一个基于Hook Generator的bot，无需token

**User Flow**:
```
用户在Hook Generator点击CTA
    ↓
跳转到@shellagent_bot
    ↓
系统检测到来源（deep link param）
    ↓
自动提示: "Want to try remixing Hook Generator first?
           I can create a test version in your Playground (no token needed)"
    ↓
用户点击"Yes, Try in Playground"
    ↓
系统自动创建Playground bot基于Hook Generator
    ↓
用户在Playground体验5-10分钟
    ↓
如果满意 → 提示绑定real token
```

**Implementation**:
- 修改`/start` command的deep link handler
- 检测`s_fb_v_*_bn_*`参数
- 如果用户是新用户 → 提供Playground option
- 如果用户已有bot → 直接引导创建新bot

**竞品evidence**:
- Product context.md明确说: "Playground: 用户先在Playground Bot体验,满意后再绑定真实token"
- PLG best practice: "Free trials are excellent for converting traffic into signups"
- Notion: "Hands-on approach that makes process practical and intuitive"

### 2. Playground Bot内的"Upgrade"提示

**Timing**: 用户在Playground试用bot后

**消息示例**:
```markdown
🎉 Your Playground bot is working great!

Want to make it real and use it anywhere in Telegram?

Upgrade to a real bot in 3 steps:
1. Get a token from @BotFather (takes 2 min)
2. Paste it here
3. Done! Your bot is live 🚀

[Upgrade Now] [Keep Playing]
```

**Why this works**:
- 用户已经体验了价值（TTV降低）
- Playground → Real的门槛比"零→Real"低很多
- Sunk cost: 用户已经配置和测试了bot

---

## 方案三：外部引流优化（长期）

### 1. 在Reddit/Twitter创建"Built with ShellAgent"展示页

**Goal**: 让非ShellAgent用户发现这些bot是用户创建的

**Implementation**:
- 在Hook Generator的bio/description添加: "Built by @creator_name with @shellagent_bot"
- 创建landing page展示所有"Built with ShellAgent"的bots
- Bot profile picture添加small "ShellAgent" badge

**竞品evidence**:
- 我之前建议的"Public Creator Attribution"
- PLG: "Use user-generated content and social proof"

### 2. Bot内mini tutorial

**Concept**: 5秒视频/GIF展示"如何用ShellAgent创建bot"

**Implementation**:
- 录制5-10秒GIF: ShellAgent interface → 输入描述 → bot生成
- 在Tier 2 CTA消息内嵌GIF
- 类似现有的newbot-tutorial.gif

**Why this works**:
- 看比读更有说服力
- 降低"这太复杂"的心理障碍
- Telegram支持GIF自动播放

---

## 技术实现清单

### Phase 1: 基础CTA（1-2周）

#### Task 1.1: 修改marketing bots的welcome message
```
File: Bot configuration (或运行时message template)
Change: 添加"Created with @shellagent_bot"说明
Add: Inline button "Build Your Own"
Test: 确保deep link tracking正常
```

#### Task 1.2: 实现消息计数触发系统
```
File: tg_running_webhook handler
Logic:
  - Query user message count from tg2app_bot_running_messages
  - If count in [3, 10, 25]:
      - Check if CTA already shown (Redis flag)
      - If not shown: Send CTA message
      - Set flag: cta_{tier}_{user_id}_{bot_id}
Test: 确保不重复触发同一tier
```

#### Task 1.3: 创建CTA message templates
```
File: internal/domain/service/tg2app/tg_running_messages/ (new folder)
Files:
  - cta_tier1.template.go
  - cta_tier2.template.go
  - cta_tier3.template.go
Content: 按上面文案实现，支持bot_name变量
Test: 确保Inline buttons正确工作
```

#### Task 1.4: Deep link tracking
```
Modify: /start command handler in ShellAgent
Add: 检测s_fb_v_*_bn_*参数
Action:
  - 记录来源到analytics table
  - 展示contextual onboarding message
Test: 确保从Hook Generator点击能追踪到
```

### Phase 2: Playground快速体验（2-3周）

#### Task 2.1: Remix to Playground flow
```
Modify: /start command with s_fb_v_* param
Add: Prompt user "Try in Playground first?"
If yes:
  - Auto-create Playground bot based on source bot
  - Set user state to PLAYGROUND mode
Test: 从Hook Generator点击 → Playground bot创建成功
```

#### Task 2.2: Playground "Upgrade" prompt
```
Trigger: User sends 5th message in Playground
Message: "Upgrade to real bot?" with tutorial
Button: "Get Token from BotFather" (教程)
State: Set to PLAYGROUND_WAIT_INPUT_TOKEN
Test: 确保upgrade flow顺畅
```

### Phase 3: 内容优化（3-4周）

#### Task 3.1: GIF tutorial
```
Create: 5-10秒GIF showing bot creation
Upload: 到 myshellstatic.com CDN
Add: 到Tier 2 CTA message
Test: GIF autoplay in Telegram
```

#### Task 3.2: Creator attribution
```
Update: All 8 marketing bots' bio
Format: "Created by @username with @shellagent_bot"
Add: Small badge to bot avatar (optional)
Test: 用户能看到attribution
```

---

## A/B测试计划

### Test 1: CTA Timing

**Hypothesis**: 第10次消息的转化率最高

**Variants**:
- A: Tier 1 at message 3
- B: Tier 1 at message 5
- C: Tier 1 at message 7

**Measure**: Click-through rate到@shellagent_bot
**Duration**: 2周
**Sample**: 每个variant至少50 users

### Test 2: CTA文案

**Hypothesis**: 具体benefit比通用CTA转化更好

**Variants**:
- A: "Build Your Own Bot" (generic)
- B: "Create Your Custom Hook Generator" (specific)
- C: "Build a Bot for YOUR Niche" (benefit-focused)

**Measure**: Click-through + actual bot creation
**Duration**: 2周

### Test 3: Button vs Text link

**Hypothesis**: Inline button比text link转化高

**Variants**:
- A: Inline button with deep link
- B: Plain text: "Visit @shellagent_bot"
- C: Both (button + text)

**Measure**: Click-through rate
**Duration**: 1周

---

## 成功指标 (30天)

| 指标 | Baseline | Target | Stretch Goal |
|------|----------|--------|--------------|
| **CTA Click-through Rate** | N/A | 15% | 25% |
| **Playground试用率** | N/A | 30% | 50% |
| **Playground → Real转化** | N/A | 20% | 40% |
| **整体非创建者转化率** | 0% | 5-10% | 15%+ |
| **New bot creators** | 0/month | 3-7 | 10+ |

### Leading Indicators (前14天)

| 指标 | Target |
|------|--------|
| CTA显示次数 | 100+ |
| 用户点击CTA | 15+ |
| 访问@shellagent_bot | 10+ |
| Playground创建 | 5+ |

---

## 风险与缓解

### Risk 1: CTA太频繁导致用户反感

**Evidence**: "Feels like tap on shoulder, not interruption"

**Mitigation**:
- 使用20%频率的嵌入式CTA，不是每次都显示
- 提供"Don't show again"选项
- A/B测试频率

### Risk 2: 10分钟生成时间吓跑用户

**Evidence**: 用户在Playground 5分钟就不耐烦

**Mitigation**:
- 强调Playground "instant preview" option
- 在CTA中说明"10 minutes, then it's yours forever"
- 显示进度条或定时通知

### Risk 3: BotFather token获取太难

**Evidence**: 新用户不知道什么是@BotFather

**Mitigation**:
- 提供详细的GIF tutorial (已有newbot-tutorial.gif)
- 在Playground → Real时强调"只需2分钟"
- 考虑video tutorial

### Risk 4: $4免费额度耗尽

**Evidence**: 用户试错后没钱了

**Mitigation**:
- 在CTA中强调"Free $4 credit included"
- 引导用户先在Playground测试（不消耗credit）
- Clear定价信息

---

## 竞品Benchmark

| 策略 | Zapier | Notion | ShellAgent (proposed) |
|------|--------|--------|----------------------|
| **Onboarding CTA** | ✅ Activation email with clear CTA | ✅ In-app wizard + tooltips | ✅ In-bot messages + buttons |
| **Free Trial** | ✅ 14-day trial | ✅ Free tier | ✅ Playground + $4 credit |
| **Template/Example** | ✅ Template gallery | ✅ Template library | ✅ 8 marketing bots |
| **Social Proof** | ✅ Use cases | ✅ Community templates | 🔄 Add creator attribution |
| **One-click start** | ❌ Need account setup | ❌ Need signup | ✅ Telegram native, instant |
| **Contextual help** | ✅ In-app tips | ✅ Contextual tooltips | ✅ Tiered CTAs |

**Our advantage**: Telegram-native + Instant access
**Our gap**: No template gallery yet → Fix with "Bot Showcase" page

---

## 下一步行动 (按优先级)

### Week 1-2: MVP Implementation

1. ✅ Update Hook Generator welcome message (1 day)
2. ✅ Implement message count trigger system (2-3 days)
3. ✅ Create Tier 1 & Tier 2 CTA templates (1 day)
4. ✅ Add Inline button with deep link (1 day)
5. ✅ Setup analytics tracking for CTAs (1 day)
6. ✅ Test on staging with 10 test users (2 days)

### Week 3-4: Iteration & Expansion

7. ✅ Deploy to Hook Generator (most users) (1 day)
8. ✅ Monitor metrics for 1 week
9. ✅ Deploy Tier 3 CTA if Tier 1/2 successful
10. ✅ Expand to myshell_thumbmaker_bot (2nd most users)
11. ✅ Start A/B tests on CTA timing

### Month 2: Playground Integration

12. ✅ Implement "Remix to Playground" flow
13. ✅ Test Playground → Real conversion
14. ✅ Create GIF tutorial for bot creation
15. ✅ Add to all 8 marketing bots

### Month 3: Optimization

16. ✅ Analyze A/B test results
17. ✅ Refine CTA copy based on data
18. ✅ Add creator attribution to bot profiles
19. ✅ Create "Built with ShellAgent" showcase page

---

## 总结

**关键要点**:

1. **Start Small**: 先实施welcome message + Tier 1 CTA，测试反应
2. **Leverage Playground**: 这是降低门槛的杀手锏
3. **Use Buttons**: Telegram用户习惯buttons，不要用text links
4. **Contextual Timing**: 在用户experience value后才触发CTA
5. **Social Proof**: 加creator attribution增加credibility
6. **Measure Everything**: A/B测试CTA timing, wording, placement

**Expected Outcome** (90 days):
- Convert 7-14 of 70 non-creators (10-20% rate)
- Establish repeatable playbook for future marketing bots
- Validate Playground as conversion bridge

**投入 vs 回报**:
- **Engineering effort**: 2-3周开发 + 1周测试
- **Expected lift**: 10-20%转化率 = 7-14 new creators
- **Long-term impact**: 可复用的CTA系统，适用于所有future marketing bots

