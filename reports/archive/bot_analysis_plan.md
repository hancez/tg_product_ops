# Bot User Behavior Analysis Plan

**Date**: 2025-10-27
**Bots Analyzed**: 8 content creator bots from Reddit GTM campaign

---

## 📊 Phase 1: Current Data Overview

### Bot Usage Statistics (from image.png)

| Rank | Bot Name | Bot ID | 使用人数 | 消息数 | 人均消息 | 被remix数 |
|------|----------|--------|---------|--------|---------|----------|
| 1 | Hook_Generator_Bot | 1965760104392110080 | 67 | 774 | 11.6 | - |
| 2 | myshell_thumbmaker_bot | 1970046615507873792 | 18 | 2832 | **157.3** | 2 |
| 3 | Viral_Idea_Spark_Bot | 1975400765027258368 | 5 | 122 | 24.4 | - |
| 4 | xPostGenerator_Bot | 1974701461545680896 | 4 | 401 | 100.3 | - |
| 5 | BRoll_Generator_Bot | 1972858715723681792 | 4 | 157 | 39.3 | - |
| 6 | XtoVideoScriptTransformer_Bot | 1974427421370437632 | 3 | 269 | 89.7 | - |
| 7 | CFLinkedinPostBot | 1974829619605544960 | 3 | 91 | 30.3 | - |
| 8 | X_Rival_Analysis_bot | 1975961906457870336 | 2 | 138 | 69.0 | - |
| **Total** | | | **106** | **4784** | **45.1** | **2** |

### Initial Insights

**🔥 Key Findings**:

1. **Hook_Generator_Bot 是流量之王**
   - 67 用户（占总用户 63%）
   - 但人均互动仅 11.6 条（倒数第二）
   - **Hypothesis**: 易上手，用户试用后快速离开

2. **myshell_thumbmaker_bot 是深度使用之王**
   - 仅 18 用户，但人均 157 条消息（是平均值的 3.5 倍）
   - 被 remix 2 次（唯一被 remix 的 bot）
   - **Hypothesis**: 功能强大/工作流友好，用户反复使用

3. **长尾分布明显**
   - Top 2 bots 占 80% 用户（85/106）
   - Bottom 5 bots 仅 21 用户

4. **人均消息数差异巨大**
   - 最高 157.3（myshell_thumbmaker_bot）
   - 最低 11.6（Hook_Generator_Bot）
   - 差距 13.5 倍

**🤔 Open Questions**:
- 为什么 Hook_Generator_Bot 用户多但互动低？
- 为什么 myshell_thumbmaker_bot 用户少但互动极高？
- 哪些用户同时使用多个 bot？（Power Users）
- 这些用户是如何发现这些 bot 的？（通过 Reddit 帖子 vs 自然搜索）
- 用户在创建这些 bot 时和 ShellAgent 的对话是什么样的？

---

## 🔍 Phase 2: Deep Dive Query Plan

### Query Set 1: User-Level Analysis

#### Q1.1: 获取每个 bot 的用户 ID 列表
**SQL**:
```sql
-- Hook_Generator_Bot
select distinct(user_id) from tg2app_bot_running_messages
where bot_id = 1965760104392110080;

-- myshell_thumbmaker_bot
select distinct(user_id) from tg2app_bot_running_messages
where bot_id = 1970046615507873792;

-- [Repeat for all 8 bots]
```

**Purpose**: 获取 106 个用户的 ID，用于后续深入分析

**Expected Output**:
- 8 个 CSV 文件，每个包含该 bot 的用户 ID 列表
- 可以识别出哪些用户使用了多个 bot

---

#### Q1.2: 识别 Power Users（使用多个 bot 的用户）
**SQL**:
```sql
-- 查询每个用户使用了几个 bot
select user_id, count(distinct bot_id) as bot_count
from tg2app_bot_running_messages
where bot_id in (
    1965760104392110080, 1970046615507873792, 1972858715723681792,
    1974427421370437632, 1974701461545680896, 1974829619605544960,
    1975400765027258368, 1975961906457870336
)
group by user_id
order by bot_count desc;
```

**Purpose**:
- 找出使用 2+ bots 的用户
- 了解用户是否会尝试多个 bot

**Expected Insights**:
- Power User 占比（e.g., 10% 用户使用 3+ bots）
- 哪些 bot 组合常被同时使用（e.g., Hook + Thumbnail bots）

---

#### Q1.3: 查询用户的总 bot 数（不限于这 8 个）
**SQL**:
```sql
-- 对于每个用户，查询他们创建了多少个 bot
select user_id, count(*) as total_bots_created
from tg2app_tg_bots
where user_id in (
    -- [从 Q1.1 获取的 106 个用户 ID]
)
group by user_id
order by total_bots_created desc;
```

**Purpose**:
- 了解这些用户是否是平台的活跃创建者
- 这 8 个 bot 占他们总 bot 数的多少

**Expected Insights**:
- 如果用户平均创建 5+ bots，说明这些是 power users
- 如果用户只有这 1-2 个 bot，说明这些 bot 是他们的首次尝试

---

### Query Set 2: Bot Creation Journey Analysis

#### Q2.1: 查询用户和 ShellAgent 的对话（bot 生成过程）
**API**:
```bash
# 对于每个用户（从 Q1.1 获取）
curl --location --request POST 'https://api.myshell.ai/v1/tg2app/admin/list_shellagent_history_msgs' \
--header 'myshell-service-name: organics-api' \
--header 'content-type: application/json' \
--data-raw '{
  "myshell_userid": "USER_ID"
}'
```

**Purpose**:
- 看用户是如何描述 bot 需求的
- ShellAgent 生成这些 bot 用了几轮对话
- 是否有失败/重试记录

**Sample Users to Query**:
- Top 5 myshell_thumbmaker_bot 用户（高互动用户）
- 随机 10 个 Hook_Generator_Bot 用户（对比低互动用户）

**Expected Insights**:
- 高互动用户的 bot 描述是否更详细？
- 生成过程是否更顺利（fewer iterations）？

---

#### Q2.2: 查询用户和特定 bot 的对话记录
**API**:
```bash
# 例如：查询某用户和 myshell_thumbmaker_bot 的对话
curl --location --request POST 'https://api.myshell.ai/v1/tg2app/admin/list_userbot_history_msgs' \
--header 'myshell-service-name: organics-api' \
--header 'content-type: application/json' \
--data-raw '{
  "myshell_userid": "USER_ID",
  "bot_id": "1970046615507873792"
}'
```

**Purpose**:
- 了解用户如何使用这些 bot
- 识别常见使用模式
- 发现 bug 或功能不符合预期的情况

**Sample Size**:
- 全量查询 myshell_thumbmaker_bot 的 18 个用户（小样本）
- 抽样 20 个 Hook_Generator_Bot 用户

**Expected Insights**:
- myshell_thumbmaker_bot 为什么人均 157 条消息？
  - 是因为功能强大需要反复调试？
  - 还是因为有 bug 用户反复重试？
  - 还是因为工作流设计好用户愿意持续使用？

---

### Query Set 3: Remix Analysis

#### Q3.1: 查询 bot 被 remix 的详细信息
**SQL**:
```sql
-- myshell_thumbmaker_bot 被 remix 了 2 次
select
    source_bot_id,
    target_bot_id,
    remix_user_id,
    remix_time
from tg2app_bot_remix_relations
where source_bot_id = 1970046615507873792;
```

**Purpose**:
- 谁 remix 了这个 bot？
- remix 后的 bot 做了什么修改？
- 为什么只有 myshell_thumbmaker_bot 被 remix？

**Expected Insights**:
- Remix 用户是原 bot 的使用者还是新用户？
- Remix 是否代表 bot 质量高？

---

### Query Set 4: Message Pattern Analysis

#### Q4.1: 查询每个 bot 的消息时间分布
**SQL**:
```sql
-- 分析消息时间分布（按小时/天）
select
    bot_id,
    date(created_at) as date,
    hour(created_at) as hour,
    count(*) as message_count
from tg2app_bot_running_messages
where bot_id in (
    1965760104392110080, 1970046615507873792, [...]
)
group by bot_id, date, hour
order by bot_id, date, hour;
```

**Purpose**:
- 用户何时使用这些 bot？（工作时间 vs 晚上）
- 使用频率如何？（每天多次 vs 偶尔使用）

---

#### Q4.2: 分析用户的第一条和最后一条消息
**SQL**:
```sql
-- 对于每个用户，查询第一条和最后一条消息的时间
select
    user_id,
    bot_id,
    min(created_at) as first_message,
    max(created_at) as last_message,
    count(*) as total_messages,
    timestampdiff(day, min(created_at), max(created_at)) as usage_span_days
from tg2app_bot_running_messages
where bot_id in (
    1965760104392110080, 1970046615507873792, [...]
)
group by user_id, bot_id
order by usage_span_days desc;
```

**Purpose**:
- 用户使用 bot 的时间跨度
- 是一次性尝试还是持续使用？

**Expected Insights**:
- myshell_thumbmaker_bot 用户的 usage_span_days 是否更长？
- Hook_Generator_Bot 用户是否大多是"try and leave"？

---

### Query Set 5: Failure & Churn Analysis

#### Q5.1: 识别 bot 生成失败的用户
**SQL**:
```sql
-- 查询用户和 ShellAgent 的对话轮次 > 5 但没有生成这 8 个 bot 的用户
-- （需要结合 user_behavior_analysis.csv）
```

**Purpose**:
- 有多少用户尝试创建这些类型的 bot 但失败了？
- 失败原因是什么？

---

#### Q5.2: 识别 bot 生成成功但未使用的用户
**SQL**:
```sql
-- 查询创建了 bot 但消息数 = 0 的用户
-- （需要 bot owner 信息，可能需要额外的表）
```

**Purpose**:
- Bot 生成成功但用户为什么不用？
- 是否有 onboarding 问题？

---

## 🎯 Phase 3: Execution Priority

### High Priority (Must Do)

1. **Q1.1** - 获取用户 ID 列表（基础数据）
2. **Q1.2** - 识别 Power Users（了解用户画像）
3. **Q2.2** - 查询 myshell_thumbmaker_bot 的 18 个用户的对话（理解高互动原因）
4. **Q2.2** - 抽样 20 个 Hook_Generator_Bot 用户的对话（对比低互动原因）
5. **Q4.2** - 分析使用时间跨度（理解留存）

### Medium Priority (Should Do)

6. **Q1.3** - 查询用户的总 bot 数（了解用户活跃度）
7. **Q2.1** - 查询 bot 生成过程（了解生成质量）
8. **Q3.1** - Remix 详细信息（理解 viral potential）
9. **Q4.1** - 消息时间分布（了解使用场景）

### Low Priority (Nice to Have)

10. **Q5.1** - 失败用户分析
11. **Q5.2** - 未使用 bot 分析

---

## 📈 Expected Deliverables

### 1. User Segmentation Report
- Power Users (2+ bots)
- Single Bot Users
- High Engagement Users (人均 50+ 消息)
- Low Engagement Users (人均 <20 消息)

### 2. Bot Performance Deep Dive
- **myshell_thumbmaker_bot**: 为什么人均 157 条消息？
- **Hook_Generator_Bot**: 为什么用户多但互动低？

### 3. Actionable Recommendations
- 如何将 Hook_Generator_Bot 的流量转化为深度使用？
- 如何复制 myshell_thumbmaker_bot 的成功模式？
- 哪些 bot 应该加大推广？
- 哪些 bot 需要改进功能？

---

## 🚀 Next Steps

1. **Execute SQL queries** (Q1.1, Q1.2, Q1.3, Q4.2) → Get user IDs and basic patterns
2. **Execute API queries** (Q2.1, Q2.2) → Understand user conversations
3. **Analyze results** → Generate insights
4. **Create visualization** → Dashboard for stakeholders
5. **Write recommendations** → Product/GTM strategy updates

---

## 📝 Notes

- All queries assume access to `tg2app_*` tables
- API queries require `myshell-service-name: organics-api` header
- Sample size for API queries should balance depth vs. API cost
- Consider caching API results to avoid repeated calls
