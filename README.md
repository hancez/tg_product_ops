# ShellAgent Product Operations

**Last Updated**: 2025-10-28

This repository contains product operations, research, and analysis for the ShellAgent Telegram bot builder, focusing on user behavior, funnel optimization, and product improvement strategies.

## 🎯 Latest Findings (2025-10-28)

🎉 **22% conversion rate** from bot users to bot creators (higher than industry average)

⚠️  **Remix feature underutilized** - 0 /remix commands despite feature existing

📊 **Detailed analysis**: See [`reports/STRATEGIC_FUNNEL_ANALYSIS.md`](reports/STRATEGIC_FUNNEL_ANALYSIS.md)

## 📂 Repository Structure

### Core Documents (Root)
- **`CLAUDE.md`** ⭐ - Master guide for AI agents (data sources, workflows, documentation)
- **`product_context.md`** - Product capabilities, constraints, and GTM strategy
- **`README.md`** - This file

### Analysis Reports (`reports/`)
- **`STRATEGIC_FUNNEL_ANALYSIS.md`** ⭐ - Complete funnel analysis (2025-10-28)
- **`FINAL_BOT_ANALYSIS_INSIGHTS.md`** ⭐ - Bot behavior insights (2025-10-28)
- `archive/` - Historical reports

### Scripts (`scripts/`)
- **`funnel_analysis.py`** - Main funnel analysis script
- **`find_bot_creators.py`** - Identify bot creators
- `exploratory/` - Exploratory scripts (completed tasks)

### Data (`data/`)
- **`latest_results/`** ⭐ - Latest analysis data (CSV files)
- `archive/` - Historical analysis runs

### Documentation (`docs/`)
- **`QUICKSTART.md`** - Quick start guide
- **`EXECUTION_GUIDE.md`** - Detailed execution guide
- `task_v6.md` - User behavior annotation methodology
- `query.md` - API query recipes
- `shellagent_interaction_overview.md` - Golden path overview
- `wide_research_prompt.md` - Research framework

### Other Folders
- `tgbot/` - Technical bot documentation (commands, state machine, APIs)
- `sql/` - SQL query files
- `scripts_shell/` - Shell scripts for automation
- `analysis_runs/` - Legacy analysis runs (2025-10-25 study)

## 🚀 Quick Start

### View Latest Analysis

```bash
# Strategic funnel analysis
open reports/STRATEGIC_FUNNEL_ANALYSIS.md

# Bot behavior insights
open reports/FINAL_BOT_ANALYSIS_INSIGHTS.md

# Latest data (CSV)
ls data/latest_results/
```

### Run New Analysis

```bash
# 1. Configure database credentials
cp .env.template .env
# Edit .env with your credentials

# 2. Run funnel analysis
python3 scripts/funnel_analysis.py

# 3. View results
ls data/latest_results/
```

## 📊 Key Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Bot users (8 content creator bots) | 90 | Baseline |
| Power users (2+ bots) | 9 (10%) | Growing |
| Conversion to creators | 20 (22%) | ✅ Strong |
| Remix usage | 0 | 🔴 Critical issue |

## 💡 Priority Recommendations

### Immediate (This Week)
- ✅ Add Remix CTAs in bot welcome messages
- ✅ Target Power Users with custom invitations
- ✅ Audit Remix functionality

### Short-term (1 Month)
- ✅ Develop "Clone & Tweak" feature (simpler than Remix)
- ✅ Cross-promote bots to 558 other creators

Full recommendations: [`reports/STRATEGIC_FUNNEL_ANALYSIS.md`](reports/STRATEGIC_FUNNEL_ANALYSIS.md)

## 🔧 File Reorganization

**Note**: File structure was reorganized on 2025-10-28 for better organization.

To execute reorganization:
```bash
bash reorganize_files.sh
```

See `REORGANIZATION_PLAN.md` for details.

## 📖 Important Links

- [AI Agent Guide (CLAUDE.md)](CLAUDE.md)
- [Strategic Analysis](reports/STRATEGIC_FUNNEL_ANALYSIS.md)
- [Quick Start Guide](docs/QUICKSTART.md)
- [Product Context](product_context.md)

## Value Proposition

This repository provides:

- ✅ Complete funnel analysis with 22% conversion rate finding
- ✅ Tactical UX recommendations to improve Remix adoption
- ✅ Data-driven insights on user behavior patterns
- ✅ Technical reference material for implementation

Use this repo as the single source of truth for ShellAgent product decisions, experiment planning, and analysis workflows.


