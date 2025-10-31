# CLAUDE.md - Product Operations & Analysis Guide

**Last Updated**: 2025-10-29
**Purpose**: Comprehensive guide for AI agents working on ShellAgent/Telegram Bot product analysis, user behavior research, and product optimization

---

## 🎯 Current GTM Strategy (Updated 2025-10-29)

### **Solution-Led Growth Model**

ShellAgent's primary Go-To-Market strategy focuses on validating whether professional content creator bots can drive platform adoption and bot creation.

#### The Strategy
```
Professional Content Bots (8 marketing use cases)
    ↓
Users experience value through pre-built solutions
    ↓
Users want to create similar/customized bots
    ↓
Users adopt ShellAgent platform to become creators
```

#### The 8 Professional Marketing Bots
These are **professionally created showcase bots** (not user-generated content for analysis):
1. **Hook_Generator_Bot** (1965760104392110080) - Content hook generation
2. **myshell_thumbmaker_bot** (1970046615507873792) - Thumbnail creation
3. **BRoll_Generator_Bot** (1972858715723681792) - B-roll generation
4. **XtoVideoScriptTransformer_Bot** (1974427421370437632) - Script transformation
5. **xPostGenerator_Bot** (1974701461545680896) - X/Twitter post generation
6. **CFLinkedinPostBot** (1974829619605544960) - LinkedIn post creation
7. **Viral_Idea_Spark_Bot** (1975400765027258368) - Viral content ideation
8. **X_Rival_Analysis_bot** (1975961906457870336) - Competitive analysis

#### Key Analysis Focus
When analyzing these bots, focus on:
- **Users of these bots** (not the creators of these bots)
- **Conversion funnel**: Bot User → Bot Creator (using ShellAgent platform)
- **Engagement patterns**: Do users who experience these bots convert to creating their own?
- **Remix adoption**: Is the remix feature driving bot creation?
- **Retention**: Do users come back after first use?

#### Latest Findings (2025-10-29)
**Critical Discovery**:
- ✅ 23.1% of marketing bot users are bot creators (strong number)
- 🚨 BUT: 100% created their bots BEFORE using marketing bots (inverted funnel!)
- ❌ True new-user → creator conversion rate: **0%**
- 🎯 Real opportunity: 70 non-creator users with high engagement but no conversion

**See**: `reports/GTM_STRATEGY_VALIDATION_REPORT.md` for complete analysis

---

## What This Folder Contains

This is a **product operations and analysis repository** for the ShellAgent Telegram Bot product - a no-code bot builder that uses natural language to create Telegram bots.

**Documentation Types**:
1. **Technical Documentation** (`tgbot/`) - Bot interaction flows, API specs, state machines
2. **Product Strategy** (`product_context.md`) - GTM strategy, positioning, target users
3. **User Behavior Data** (`user_behavior_analysis.csv`) - 276 annotated user sessions with churn analysis
4. **Analysis Methodology** (`task_v6.md`) - User behavior annotation framework
5. **Research Tools** (`wide_research_prompt.md`, `query.md`) - Methods for large-scale research and data querying

---

## 📊 Data Sources

### Database Access
For GTM strategy validation and bot user analysis, you have readonly access to the production MySQL database:

**Connection Details**: See `.env` file (credentials provided)

**Key Tables**:
- `tg2app_bot_running_messages` - All user-bot interactions
- `tg2app_tg_bots` - Bot metadata, creators, timestamps
- `tg2app_bot_remix_relations` - Remix relationships between bots
- `tg2app_bot_user_relations` - User-bot relationship data

**Analysis Scripts** (in `scripts/`):
- `gtm_conversion_analysis.py` - Main GTM conversion funnel analysis
- `non_creator_analysis.py` - Analyzes non-converting users
- `funnel_analysis.py` - Legacy funnel analysis
- `find_bot_creators.py` - Identifies bot creators

**Latest Analysis Results** (in `data/latest_results/`):
- `marketing_bot_users.csv` - All 91 users of marketing bots
- `bot_creators.csv` - 21 users who created bots
- `conversion_timeline.csv` - Timeline analysis showing inverted funnel
- `non_creator_engagement.csv` - 70 users who didn't convert
- `bot_popularity_non_creators.csv` - Which bots non-creators use

### API Access
For querying conversation history and user data:

See `query.md` for API endpoint examples using curl commands.

---

## 🎯 Primary Use Cases

### 1. **GTM Strategy Validation** ⭐ NEW PRIMARY FOCUS
Analyzing the effectiveness of Solution-Led Growth strategy:
- Do marketing bots drive new creator acquisition?
- What's the actual conversion funnel?
- Why aren't engaged users converting?
- Is Remix feature working as a conversion bridge?

**Key Files**:
- `reports/GTM_STRATEGY_VALIDATION_REPORT.md` - Complete analysis (2025-10-29)
- `scripts/gtm_conversion_analysis.py` - Main analysis script
- `scripts/non_creator_analysis.py` - Non-converter deep dive
- `CLAUDE.md` - This file (GTM strategy overview)

### 2. **User Behavior Analysis & Churn Investigation**
Analyzing the 276 user sessions to identify:
- Where users drop off in the funnel
- Why users abandon bot creation or usage
- Patterns in successful vs. failed user journeys

**Key Files**:
- `user_behavior_analysis.csv` - Annotated user behavior data
- `task_v6.md` - Annotation methodology (shellagent对话轮次, 成功生成bot数, bot对话轮次, 使用情况, 流失阶段, 详细原因)
- `query.md` - API endpoints to fetch raw conversation data

### 2. **Product Optimization & Feature Planning**
Understanding user needs and proposing improvements:
- Interaction design improvements (UX flow optimization)
- Algorithm/feature enhancements (bot generation quality, functionality gaps)
- Prioritizing user requests (feasible vs. infeasible)

**Key Files**:
- `product_context.md` - Product capabilities and constraints
- `tgbot/interaction-flows.md` - Expected vs. actual user flows
- `shellagent_interaction_overview.md` - Core interaction patterns

### 3. **Competitive Research**
Learning from other Telegram bot products:
- Onboarding best practices
- User retention strategies
- Feature design patterns

**Key Files**:
- `wide_research_prompt.md` - Framework for large-scale parallel research

---

## 📊 Understanding User Behavior Data

### Data Structure (`user_behavior_analysis.csv`)

The CSV contains **276 annotated user sessions** with the following dimensions:

| Field | Description | Possible Values |
|-------|-------------|-----------------|
| `userid` | User identifier | String |
| `置信度` | Annotation confidence (1-10) | Integer |
| `置信度说明` | Reason for confidence score | Text (20-50 chars) |
| `shellagent对话轮次(剔除start)` | User messages to ShellAgent (excluding /start) | `0`, `1`, `1-5`, `>5` |
| `成功生成bot数` | Number of successfully created bots | Integer (0, 1, 2, 3...) |
| `bot对话轮次` | User messages to their created bot | `0`, `1`, `1-5`, `>5` |
| `使用情况` | Usage outcome | See below |
| `流失阶段` | Churn stage | `生成阶段`, `已生成未使用`, `使用阶段`, `使用顺畅` |
| `详细原因` | Detailed reason for behavior | Text (150-300 chars) |

**Usage Outcome Categories**:
- `使用顺畅` - Successful usage
- `bot功能不符合预期` - Bot functionality doesn't meet expectations
- `bot功能有bug` - Bot has bugs
- `bot功能正常但用户不会用` - Bot works but user doesn't know how to use it
- `bot功能正常但用户仅简单体验` - Bot works but user only tried briefly
- `bot生成成功但未使用` - Bot created but never used
- `成人内容生成失败` - Adult content request rejected
- `盗版内容生成失败` - Piracy content request rejected
- `无生成bot倾向的闲聊` - No intent to create bot (just chatting)
- `其他` - Other

### Key Metrics from Data

To analyze churn patterns, focus on:

1. **Funnel Drop-off Points**:
   - How many users reach each stage? (生成阶段 → 已生成未使用 → 使用阶段)
   - What percentage complete the golden path?

2. **High-Frequency Churn Reasons**:
   - Group by `使用情况` to find most common failure modes
   - Cross-reference with `详细原因` for root causes

3. **Successful User Patterns**:
   - Filter for `使用情况 == "使用顺畅"`
   - Identify common behaviors (对话轮次, 生成bot数, etc.)

---

## 🔍 Analysis Workflows

### Workflow 1: Churn Funnel Analysis

**Goal**: Understand where and why users drop off

**Steps**:
1. Load `user_behavior_analysis.csv`
2. Calculate funnel conversion:
   ```
   Total users (276)
   ↓
   Users who attempted bot creation (shellagent对话轮次 > 0)
   ↓
   Users who successfully generated bot (成功生成bot数 > 0)
   ↓
   Users who used their bot (bot对话轮次 > 0)
   ↓
   Users with smooth usage (使用情况 == "使用顺畅")
   ```
3. Identify largest drop-off points
4. For each drop-off, analyze `详细原因` patterns

### Workflow 2: Feature Gap Analysis

**Goal**: Extract unmet user needs from failed sessions

**Steps**:
1. Filter users by `使用情况`:
   - `bot功能不符合预期`
   - `bot功能有bug`
   - `成人内容生成失败` (understand intent, not implement)
   - `盗版内容生成失败` (understand intent, not implement)
2. Read `详细原因` for each user
3. Extract:
   - What did user want to create?
   - Why did it fail? (technical limitation, policy, UX confusion)
   - Is this a feasible request? (check against `product_context.md`)
4. Group similar requests
5. Prioritize by frequency + feasibility

### Workflow 3: Interaction Flow Mapping

**Goal**: Compare actual user behavior to expected golden path

**Steps**:
1. Read golden path from `shellagent_interaction_overview.md`
2. For a sample of users (e.g., 10 from each 使用情况 category):
   - Use `query.md` API to fetch raw conversation logs
   - Map actual conversation to expected flow
   - Identify deviation points
3. Aggregate deviation patterns
4. Propose UX improvements

---

## 🛠️ API Reference for Raw Data Queries

### Querying User Conversations

```bash
# Get user conversation history with ShellAgent
curl --location --request POST 'https://api.myshell.ai/v1/tg2app/admin/list_shellagent_history_msgs' \
--header 'myshell-service-name: organics-api' \
--header 'content-type: application/json' \
--data-raw '{
  "myshell_userid": "USER_ID"
}'

# Find which bots a user has chatted with
curl --location --request POST 'https://api.myshell.ai/v1/tg2app/admin/search_uesr_chat_bots' \
--header 'myshell-service-name: organics-api' \
--header 'content-type: application/json' \
--data-raw '{
  "tg_userid": "TG_USER_ID"
}'

# Get conversation between user and specific bot
curl --location --request POST 'https://api.myshell.ai/v1/tg2app/admin/list_userbot_history_msgs' \
--header 'myshell-service-name: organics-api' \
--header 'content-type: application/json' \
--data-raw '{
  "myshell_userid": "USER_ID",
  "bot_id": "BOT_ID"
}'
```

### Reading Product Documentation

When analyzing user behavior or proposing product improvements:

1. **Always start with**: `shellagent_interaction_overview.md` (comprehensive overview of expected user flow)
2. **For interaction design issues**, reference:
   - `tgbot/interaction-flows.md` - Detailed user journey flowcharts with mermaid diagrams
   - `tgbot/commands.md` - All bot commands and their specifications
   - `tgbot/buttons.md` - Button interactions and callback data
   - `tgbot/state-machine.md` - User state management and transitions
   - `tgbot/messages.md` - Message templates and exact copy
3. **For technical constraints**, reference:
   - `tgbot/api-endpoints.md` - Webhook and API implementation details
   - `product_context.md` - Product capabilities matrix (what's feasible vs. infeasible)
4. **For research methodology**, reference:
   - `wide_research_prompt.md` - Framework for parallel research (Telegram bot best practices, competitive analysis)

---

## 📂 Folder Structure

```
product_op/
├── CLAUDE.md                              # ⭐ This file - Master guide for analysis
├── user_behavior_analysis.csv             # 276 annotated user sessions
├── task_v6.md                             # Annotation methodology
├── query.md                               # API endpoints for raw data
├── wide_research_prompt.md                # Parallel research framework
├── product_context.md                     # GTM strategy & capabilities
├── shellagent_interaction_overview.md     # Quick interaction reference
└── tgbot/                                 # Detailed technical documentation
    ├── interaction-flows.md               # User journey flowcharts (mermaid)
    ├── commands.md                        # Command specifications
    ├── buttons.md                         # Button interaction details
    ├── state-machine.md                   # State management logic
    ├── messages.md                        # Message templates
    └── api-endpoints.md                   # API/webhook specifications
```

---

## Key Product Concepts

### Three Types of Bots

1. **ShellAgent Bot** (Generation Bot)
   - Purpose: Create and manage user bots
   - Webhook: `/v1/tg2app/telegram/generate/webhook`
   - Commands: `/start`, `/newbot`, `/mybots`, `/remix`, `/currentbot`

2. **Running Bot** (User's Production Bot)
   - Purpose: End-user interaction with deployed bots
   - Webhook: `/v1/tg2app/telegram/running/webhook/{bot_id}/{bot_token}`
   - Commands: Custom commands defined by user

3. **Trial/Playground Bot**
   - Purpose: Testing environment before token binding
   - Webhook: `/v1/tg2app/telegram/trial/webhook`

### The Golden Path (Expected User Flow)

```
1. User sends /start
   ↓
2. Bot: "Tell me what bot you want to build. One or two sentences are enough."
   ↓
3. User describes bot in 1-2 sentences
   ↓
4. Bot: "Building draft..."
   ↓
5. During build, any message gets: "ShellAgent_Playground_Bot is still setting up..."
   ↓
6. On success: Success card with bot capabilities + balance + preview link
   ↓
7. User tests in Playground Bot
   ↓
8. User binds real Token via /newbot → BotFather flow
   ↓
9. User deploys to production
```

### User State Machine

**States**:
- `IDLE` - Default state, can accept commands or bot edit requests
- `NEWBOT:WAIT_USER_INPUT_BOT_TOKEN` - Waiting for BotFather token
- `REMIX:WAIT_USER_INPUT_BOT_NAME` - Waiting for source bot name
- `REMIX:WAIT_USER_INPUT_BOT_TOKEN` - Waiting for new bot token
- `PLAYGROUND:WAIT_USER_INPUT_TOKEN` - Waiting for playground token binding

**Important**: When in non-IDLE state, only specific inputs are accepted.

---

## Common Tasks and How to Execute

### Task: Analyze User Churn

**Steps**:
1. Read `shellagent_interaction_overview.md` for expected flow
2. Query user conversation data via API (see `query.md`)
3. Compare actual behavior with golden path
4. Reference `tgbot/state-machine.md` to understand where users got stuck
5. Check `tg2用户分析.md` for existing churn analysis patterns

**Key Metrics**:
- Drop-off at /start (immediate abandonment)
- Drop-off at bot description (cold start problem)
- Drop-off during generation (timeout or complexity)
- Playground → Production conversion rate (Token binding)

### Task: Understand Bot Command Behavior

**Steps**:
1. Check `tgbot/commands.md` for command specifications
2. Reference `tgbot/state-machine.md` for state changes triggered
3. Check `tgbot/messages.md` for exact message copy
4. See `tgbot/buttons.md` for associated button actions

### Task: Debug User Journey Issue

**Steps**:
1. Start with `tgbot/interaction-flows.md` for visual flowchart
2. Map user's actual actions to expected flow
3. Identify deviation point
4. Check relevant state transition in `state-machine.md`
5. Verify message/button configuration in respective files

### Task: Propose Product Improvements

**Reference**:
1. Existing analysis: `tg2用户分析.md` (40% churn before first bot)
2. Existing suggestions: `telegram产品设计建议.md`
3. Always cite specific flow issues from `tgbot/interaction-flows.md`

---

## Important Conventions

### Documentation Language
- Most files are in **English** (technical specs)
- Analysis files may be in **Chinese** (`tg2用户分析.md`, `telegram产品设计建议.md`)
- API responses are in **JSON**

### File Naming
- Technical specs: lowercase with hyphens (e.g., `state-machine.md`)
- Analysis docs: Chinese characters allowed
- MCP references: Use exact file paths when reading

### Code References
When referencing implementation details:
- Format: `file_path:line_number`
- Example: `tg_gen_commands/tg_gen_command.start.service.go:250-259`

---

## Known Issues and Bottlenecks

### 1. Cold Start Problem
**Issue**: Users see "Tell me what bot you want to build" and don't know what to say
**Evidence**: 25%+ immediate abandonment after /start
**Location**: `tgbot/commands.md` - `/start` command section

### 2. Policy Violation Confusion
**Issue**: Users try to create bots for pirated content, adult material, etc., then get rejected
**Evidence**: 25% drop-off due to policy blocks
**Location**: Message rejection logic (not fully documented)

### 3. Playground → Production Gap
**Issue**: 90% of users stay in Playground, never bind real Token
**Evidence**: Historical data from `tg2用户分析.md`
**Location**: `tgbot/interaction-flows.md` - Post-generation flow

### 4. Complexity Management Missing
**Issue**: System doesn't guide users to simplify overly complex requests
**Evidence**: Users send 4000+ character requirements, likely causing failures
**Location**: No current handling in `tgbot/state-machine.md`

---

## When to Use Each Document

| Question | Document to Read | Why |
|----------|------------------|-----|
| "How does the product work?" | `shellagent_interaction_overview.md` | Quick overview with golden path |
| "What happens when user clicks X?" | `tgbot/buttons.md` | Button interaction specs |
| "What does /command do?" | `tgbot/commands.md` | Command specifications |
| "Why is user stuck in this state?" | `tgbot/state-machine.md` | State transitions and requirements |
| "What should the bot reply?" | `tgbot/messages.md` | Message templates and copy |
| "How do I query user data?" | `query.md` | API endpoint examples |
| "What are known churn issues?" | `tg2用户分析.md` | Existing analysis |
| "What's the full user journey?" | `tgbot/interaction-flows.md` | Visual flowcharts |

---

## Best Practices for AI Agents

### DO
✅ Always start with `shellagent_interaction_overview.md` for context
✅ Cross-reference multiple docs for complete picture
✅ Query actual user data when analyzing churn
✅ Compare actual behavior vs. expected flow from docs
✅ Cite specific document sections in your analysis
✅ Note gaps or inconsistencies in documentation

### DON'T
❌ Assume behavior without checking specs
❌ Make up API endpoints (always use `query.md`)
❌ Ignore existing analysis in `tg2用户分析.md`
❌ Propose improvements without evidence
❌ Confuse the three bot types (Gen/Running/Playground)
❌ Forget to check state machine when debugging user issues

---

## External Resources

- **Workshop URL**: `https://tg-workshop.myshell.ai` (Mini App for user management)
- **Staging Workshop**: `https://telegram-miniapp.myshell.fun/profile`
- **BotFather**: `@BotFather` (Telegram's official bot for creating bots)
- **API Base**: `https://api.myshell.ai/v1/tg2app/`

---

## Quick Troubleshooting

**Q: User says they're stuck, how do I debug?**
A:
1. Query their conversation history via `query.md` API
2. Check their current state (should be in API response)
3. Reference `tgbot/state-machine.md` for state requirements
4. Compare with expected flow in `tgbot/interaction-flows.md`

**Q: Need to understand a specific command?**
A: `tgbot/commands.md` has full specifications + example interactions

**Q: What's the difference between Playground and Production?**
A: Read `shellagent_interaction_overview.md` section "系统与入口" - Playground uses trial webhook, Production uses user's own bot token

**Q: How do I analyze churn patterns?**
A:
1. Start with existing analysis: `tg2用户分析.md`
2. Query user data for specific cohort
3. Map to golden path in `shellagent_interaction_overview.md`
4. Identify deviation points using `tgbot/interaction-flows.md`

---

## 📝 Output Deliverables Format

When completing product analysis, deliver structured documents with the following format:

### 1. **Interaction Optimization Report**

**Target**: UX/Product team
**Structure**:
```markdown
# Interaction Optimization Recommendations

## Executive Summary
- Key findings (3-5 bullet points)
- Impact assessment (high/medium/low priority)

## Churn Analysis
### Funnel Overview
- [Conversion rates at each stage]
- [Largest drop-off points]

### Top 5 Interaction Issues
For each issue:
- **Issue**: [Clear description]
- **Evidence**: [Data from user_behavior_analysis.csv + specific user examples]
- **Current Flow**: [What happens now, reference tgbot/interaction-flows.md]
- **Proposed Fix**: [Specific UX change]
- **Expected Impact**: [Which 使用情况 categories will this fix]
- **Implementation Complexity**: [Low/Medium/High]

## Low-Hanging Fruit (Quick Wins)
- [Issues that are easy to fix with high impact]

## Long-Term Improvements
- [Systemic changes requiring more effort]
```

### 2. **Algorithm & Feature Optimization Report**

**Target**: Algorithm/Engineering team
**Structure**:
```markdown
# Algorithm & Feature Recommendations

## User Needs Analysis
### Category 1: [e.g., "Video Download Bots"]
- **Frequency**: [How many users requested this]
- **Example Requests**: [Quotes from 详细原因]
- **Current Limitation**: [Why it fails now]
- **Feasibility**: [Feasible/Infeasible/Partial, reference product_context.md]
- **Recommendation**: [What to implement or why to reject]

### Category 2: [...]
[Repeat structure]

## Bot Generation Quality Issues
### Issue 1: [e.g., "Bot generates wrong type"]
- **Pattern**: [Common misunderstandings]
- **Root Cause**: [AI prompt issue? Parsing issue?]
- **Fix**: [Specific algorithm/prompt change]

## Priority Matrix
| Feature Request | User Impact | Feasibility | Priority |
|----------------|-------------|-------------|----------|
| [Request 1]    | High        | High        | P0       |
| [Request 2]    | Medium      | Low         | P2       |
```

### 3. **Competitive Research Findings**

**Target**: Product strategy team
**Structure**:
```markdown
# Telegram Bot Product Best Practices

## Onboarding Patterns
- [Pattern 1]: [Description + Examples from research]
- [Pattern 2]: [...]

## User Retention Strategies
- [Strategy 1]: [How other products do it]
- [Applicable to us?]: [Yes/No + Reasoning]

## Feature Inspirations
- [Feature idea from competitor]
- [How to adapt for ShellAgent]
```

### 4. **Bottleneck & Issues Log**

**Format**: Append to a persistent log file
```markdown
## [Date] - [Issue Title]
**Category**: [Data Quality / Tool Limitation / Research Gap]
**Description**: [What went wrong or was unclear]
**Impact**: [How this affects analysis]
**Workaround**: [What was done instead]
**Long-term Fix**: [What should be improved]
```

---

## ⚠️ Important Principles

### DO ✅
- Always cite specific user IDs and 详细原因 when making claims
- Cross-reference technical docs (`tgbot/`) when proposing UX changes
- Check feasibility against `product_context.md` before recommending features
- Separate "user wants this" from "we should build this"
- Record bottlenecks and data gaps for future improvement

### DON'T ❌
- Don't propose building adult content or piracy features (even if users requested)
- Don't guess at technical feasibility - check docs or mark as "requires engineering assessment"
- Don't aggregate without preserving individual user stories
- Don't recommend UX changes that conflict with technical constraints (e.g., Telegram API limits)

---

## Updates and Maintenance

This CLAUDE.md should be updated when:
- New analysis methodologies are developed
- Additional data sources become available
- Product capabilities change (update `product_context.md` reference)
- New research frameworks are added
- Known analysis bottlenecks are resolved

**Owner**: Product Operations & Analysis Team
**Last Major Update**: 2025-10-25 (Added analysis workflows and output formats)

---

*This file serves as your master guide for product analysis. For technical details, reference the specific documents in `tgbot/`. For raw data, use `query.md` APIs. For methodology, see `task_v6.md` and `wide_research_prompt.md`.*
