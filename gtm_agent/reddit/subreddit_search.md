# Subreddit Research SOP

## 1. 建立候选清单
- **锁定营销目标**：先弄清楚要触达谁、要卖什么价值，再反推他们平时会订阅/搜索的主题。
- **列首批关键词**：围绕“痛点 / 兴趣 / 使用场景”，每类写 3–5 个词。
  - 例：想吸引对自动化、No Code 感兴趣但不会 n8n 的人 → `nocode`、`vibe coding`、`automation`
  - 例：想吸引自媒体创作者 → `social media`、`content creators`、`content marketing`、`youtuber`
- **让模型扩展词表**：要求输出近义词、职业别称、行业标签（如 `social media` → `social media manager`、`social media marketing`）。
- **多渠道搜候选**：
  - Reddit 搜索框直接查关键词，记录推荐的 subreddit
  - Google `site:reddit.com <关键词>`
  - Reddit Ads 新建广告计划 → 输入一条 subreddit → 取系统推荐的相似社区
  - 关注若干目标 subreddit，利用首页“猜你喜欢”收集
  - 外部工具：Anvaka 的地图 https://anvaka.github.io/map-of-reddit
- **整理一级表格**：列关键词、来源、初步匹配度（高/中/低）、待验证信息（如规则、活跃度、受众质感）。

## 2. 评估并打分
- **流量/活跃度**（越大越好）
  - 看成员数、在线人数、每周访客、每周发帖；重点用 `Top -> This year / month / week` 观察前十帖的 upvote 水位
  - 经验阈值：在线人数 ≥200 = 大流量；60–199 = 中等；<60 = 小众
- **版规松紧**
  - 阅读 self promotion / spam 条款：区分禁止 / 限频 / 几乎无规则
    - 严格：明确写 NO self promotion（例：r/NewTubers、r/content_marketing、r/Entrepreneur）
    - 有条件：允许 1:10 自推（例：r/AI_Agents、r/AIAssisted）
    - 极宽松：几乎没规则（例：r/TelegramBots、r/ProductivityApps）
  - 观察帖子：是否有人成功挂链？链接是裸链还是嵌入？被删评论多不多？
- **竞争强度**
  - `Sort by New` 看 1 小时 / 1 天 / 1 周的发帖数量
  - 流量接近时优先选择新帖密度低的社区（例：r/SideProject 每小时 27 贴 > r/InternetIsBeautiful 每小时 2 贴 → 后者曝光概率高）
- **社区氛围**
  - 评论区是否支持性强？新帖是否普遍被踩到 0？
- **评估表建议**：将上面四项做 1–5 分打分，附一句主观备注与风险提示。

## 3. 内容角度调研
- `Top -> This year / month / week` 拉取近十条爆帖，归类格式（故事 / 清单 / 提问 / 直接推广 / meme 等）。
  - 例：r/nocode 爆帖偏长篇故事、工具清单、开放式问题、直接推广
  - 例：r/ProductivityApps 爆帖多为开放式讨论
- 记录每条的标题、互动量、是否带链接、链接形态。
- 基于版规判断可复用度，输出可复用的结构模板。

## 4. 交付与迭代
- **候选清单**：列优先级、核心受众、最合适的发帖角度、注意事项。
- **研究档案**：存版规链接、样例帖子、Flair 或格式要求、常见踩雷点。
- **投放复盘**：每次实投后更新社区卡片（是否被移除、曝光/互动、后续建议），形成滚动资产库。
