# 📂 Product_Op 文件夹重组计划

**日期**: 2025-10-28
**目的**: 清理混乱的文件结构，建立清晰的分类体系

---

## 📊 当前状态诊断

### 问题
1. ✗ 根目录有 27 个文件，过于混乱
2. ✗ 分析报告、脚本、文档混在一起
3. ✗ 多个重复的 analysis_results 文件夹
4. ✗ 临时探索脚本未清理
5. ✗ 没有清晰的"最新结果"入口

---

## 🎯 新文件夹结构

```
product_op/
│
├── 📄 README.md                        # 项目总览
├── 📄 CLAUDE.md                        # AI Agent 使用指南（最重要）
├── 📄 product_context.md               # 产品背景
├── 🔒 .env                             # 数据库凭证（不提交）
├── 🔒 .env.template                    # 凭证模板
│
├── 📊 reports/                         # 分析报告（最终输出）
│   ├── STRATEGIC_FUNNEL_ANALYSIS.md    # ⭐ 最新战略分析（2025-10-28）
│   ├── FINAL_BOT_ANALYSIS_INSIGHTS.md  # ⭐ 最新 Bot 分析（2025-10-28）
│   └── archive/                        # 历史报告存档
│       ├── bot_behavior_insights_report.md
│       ├── bot_analysis_plan.md
│       └── ANALYSIS_STATUS.md
│
├── 🐍 scripts/                         # Python 查询脚本
│   ├── funnel_analysis.py              # 漏斗分析（主要）
│   ├── find_bot_creators.py            # 查找 Bot 创建者
│   ├── find_shellagent.py              # 查找 ShellAgent bot
│   ├── execute_queries_fixed.py        # 执行 SQL 查询（最新版）
│   └── exploratory/                    # 探索性脚本（已完成任务）
│       ├── explore_database.py
│       ├── explore_full_schema.py
│       ├── explore_table_schema.py
│       ├── quick_explore.py
│       └── execute_queries.py          # 旧版，被 _fixed 替代
│
├── 📝 sql/                             # SQL 查询文件
│   ├── queries_to_execute.sql
│   └── tg2app数据分析sql.md
│
├── 💾 data/                            # 分析结果数据
│   ├── latest_results/                 # 最新数据（重要！）
│   │   ├── q1_all_users.csv
│   │   ├── q2_power_users.csv
│   │   ├── q3_user_stats.csv
│   │   ├── q4_high_engagement.csv
│   │   ├── q5_power_user_bots.csv
│   │   ├── user_overlap.csv
│   │   └── users_who_use_and_create.csv
│   └── archive/                        # 历史数据存档
│       ├── 20251027_204700/
│       ├── 20251028_151258/
│       └── 20251028_153847/
│
├── 📖 docs/                            # 文档和指南
│   ├── EXECUTION_GUIDE.md              # 执行指南
│   ├── QUICKSTART.md                   # 快速开始
│   ├── task_v6.md                      # 任务方法论
│   ├── query.md                        # API 查询文档
│   ├── shellagent_interaction_overview.md
│   └── wide_research_prompt.md
│
├── 🔧 scripts_shell/                   # Shell 脚本
│   ├── execute_analysis.sh
│   └── setup_and_run.sh
│
├── 📁 tgbot/                           # Telegram Bot 技术文档
│   └── (已有文件，不改动)
│
└── 📁 analysis_runs/                   # 历史分析运行记录
    └── (已有文件，不改动)
```

---

## 🔄 文件移动计划

### Phase 1: 创建新文件夹结构
```bash
mkdir -p reports/archive
mkdir -p scripts/exploratory
mkdir -p sql
mkdir -p data/latest_results
mkdir -p data/archive
mkdir -p docs
mkdir -p scripts_shell
```

### Phase 2: 移动分析报告
```bash
mv STRATEGIC_FUNNEL_ANALYSIS.md reports/
mv FINAL_BOT_ANALYSIS_INSIGHTS.md reports/
mv bot_behavior_insights_report.md reports/archive/
mv bot_analysis_plan.md reports/archive/
mv ANALYSIS_STATUS.md reports/archive/
```

### Phase 3: 移动脚本
```bash
mv funnel_analysis.py scripts/
mv find_bot_creators.py scripts/
mv find_shellagent.py scripts/
mv execute_queries_fixed.py scripts/

# 探索性脚本（已完成任务）
mv explore_database.py scripts/exploratory/
mv explore_full_schema.py scripts/exploratory/
mv explore_table_schema.py scripts/exploratory/
mv quick_explore.py scripts/exploratory/
mv execute_queries.py scripts/exploratory/  # 旧版
```

### Phase 4: 移动 SQL 文件
```bash
mv queries_to_execute.sql sql/
mv "tg2app 数据分析sql.md" sql/
```

### Phase 5: 整理数据文件
```bash
# 复制最新数据到 latest_results
cp analysis_results_20251028_153847/*.csv data/latest_results/
cp funnel_analysis_20251028/*.csv data/latest_results/

# 移动历史数据到 archive
mv analysis_results_20251027_204700 data/archive/
mv analysis_results_20251028_151258 data/archive/
mv analysis_results_20251028_153847 data/archive/
mv funnel_analysis_20251028 data/archive/
mv funnel_analysis_20251028_161818 data/archive/
```

### Phase 6: 移动文档
```bash
mv EXECUTION_GUIDE.md docs/
mv QUICKSTART.md docs/
mv task_v6.md docs/
mv query.md docs/
mv shellagent_interaction_overview.md docs/
mv wide_research_prompt.md docs/
```

### Phase 7: 移动 Shell 脚本
```bash
mv execute_analysis.sh scripts_shell/
mv setup_and_run.sh scripts_shell/
```

---

## 🗑️  可删除的文件（谨慎处理）

### 临时探索脚本（已归档到 scripts/exploratory/）
如果你确认不再需要，可以删除整个 `scripts/exploratory/` 文件夹：
- ❓ `explore_database.py` - 初步探索数据库结构
- ❓ `explore_full_schema.py` - 完整 schema 探索
- ❓ `explore_table_schema.py` - 表结构探索
- ❓ `quick_explore.py` - 快速探索
- ❓ `execute_queries.py` - 被 execute_queries_fixed.py 替代

**建议**: 先归档 1-2 周，确认没问题再删除

### 重复的分析结果文件夹（已归档到 data/archive/）
- ❓ `analysis_results_20251027_204700/`
- ❓ `analysis_results_20251028_151258/`
- ❓ `funnel_analysis_20251028_161818/`

**建议**: 最新结果已复制到 `data/latest_results/`，旧的可以保留 1 个月后删除

---

## 📋 重组后的文件导航

### 快速查找指南

**想看最新分析报告？**
→ `reports/STRATEGIC_FUNNEL_ANALYSIS.md`（战略分析）
→ `reports/FINAL_BOT_ANALYSIS_INSIGHTS.md`（Bot 分析）

**想查询数据？**
→ `scripts/funnel_analysis.py`（主要脚本）
→ `scripts/find_bot_creators.py`（查找创建者）
→ `data/latest_results/*.csv`（最新数据）

**想了解产品背景？**
→ `CLAUDE.md`（AI Agent 使用指南）
→ `product_context.md`（产品上下文）
→ `docs/task_v6.md`（任务方法论）

**想执行新分析？**
→ `docs/QUICKSTART.md`（快速开始）
→ `docs/EXECUTION_GUIDE.md`（详细指南）

**想查看历史数据？**
→ `data/archive/`（所有历史数据）

---

## ✅ 重组后的优势

1. ✅ **清晰的分类**: 报告、脚本、数据、文档各就各位
2. ✅ **快速找到最新结果**: `data/latest_results/` 和 `reports/`
3. ✅ **历史可追溯**: `archive/` 文件夹保存所有历史
4. ✅ **临时文件隔离**: `exploratory/` 文件夹单独存放
5. ✅ **降低认知负担**: 根目录只有 5 个文件 + 8 个文件夹

---

## 🚀 执行重组

**选项 1: 自动执行（推荐）**
```bash
# 我会创建一个脚本一次性完成所有移动
bash reorganize_files.sh
```

**选项 2: 手动执行**
按照上面 Phase 1-7 的命令逐步执行

**选项 3: 逐步执行**
先创建文件夹，确认后再移动文件

---

## ⚠️  注意事项

1. **不要删除**:
   - `.env`（数据库凭证）
   - `tgbot/`（技术文档）
   - `analysis_runs/`（历史运行记录）

2. **谨慎删除**:
   - `scripts/exploratory/`（先归档 1-2 周）
   - `data/archive/`（至少保留 1 个月）

3. **备份建议**:
   - 重组前：`git commit -m "Backup before reorganization"`
   - 重组后：`git commit -m "Reorganize folder structure"`

---

**准备好执行重组了吗？告诉我选择哪个选项！**
