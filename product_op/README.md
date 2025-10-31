# ShellAgent Product Operations

**Last Updated**: 2025-10-29

This repository contains product operations, research, and analysis for the ShellAgent Telegram bot builder, focusing on user behavior, funnel performance, and product optimization.

## 🎯 Latest Findings (2025-10-29)

- ✅ **23.1% of marketing bot users are existing bot creators** (21 of 91) — upside confirms solution-led growth traction
- 🚨 **0 net-new conversions** from the marketing bots — all creators built before engaging with showcase bots
- 🎯 **70 high-intent non-creators** identified for immediate outreach and remix education
- 📊 Deep-dive report: [`reports/archive/GTM_STRATEGY_VALIDATION_REPORT.md`](reports/archive/GTM_STRATEGY_VALIDATION_REPORT.md)

## 🧰 Required MCP Tooling

Agents need the following MCP integrations configured before running playbooks or research workflows:

- `mcp__tavily__tavily_search` – primary web search for competitive research, policy lookups, and quick fact checks
- `mcp__tavily__tavily_extract` (optional but recommended) – structured extraction for long-form sources returned by Tavily search
- `mcp__reddit__fetch_reddit_hot_threads` – collect live subreddit activity for community validation
- `mcp__reddit__fetch_reddit_post_content` – retrieve full post content and top-level comment context

> ⚙️ If any MCP endpoint is unavailable, document the limitation in your output and fall back to minimal `http(s)` retrieval as described in `methodology/wide_research_prompt.md`.

## 📂 Repository Structure

### Core Guides (`docs/product/`)
- **`CLAUDE.md`** ⭐ – Master guide for AI agents (data sources, workflows, documentation)
- **`product_context.md`** – Product capabilities, constraints, and GTM strategy
- **`shellagent_interaction_overview.md`** – Golden path overview and UX checkpoints

### Analysis Reports (`reports/`)
- **`FINAL_BOT_ANALYSIS_INSIGHTS.md`** – Latest bot behavior insights (2025-10-28)
- **`archive/GTM_STRATEGY_VALIDATION_REPORT.md`** – Solution-led GTM validation (2025-10-29)
- **`archive/`** – Historical reports and supporting briefs

### Data Assets (`data/`)
- **`latest_results/`** ⭐ – Current CSV outputs for funnel, segmentation, and outreach lists
- **`archive/`** – Historical analysis snapshots and SQL exports (timestamped folders)

### Methodology (`methodology/`)
- **`task_v6.md`** – User behavior annotation framework
- **`wide_research_prompt.md`** – MCP-first research workflow
- **`query.md`** – API query recipes for production systems

### Execution Tooling
- `scripts/` – Python analytics scripts (`gtm_conversion_analysis.py`, `non_creator_analysis.py`, `funnel_analysis.py`, etc.)
- `scripts_shell/` – Shell helpers for environment setup and batch execution
- `sql/` – Verified queries (including `queries_to_execute.sql` and supporting docs)
- `analysis_runs/` – Legacy experiment logs for back-reference (Oct 2025 studies)
- `docs/technical/tgbot/` – Detailed bot interaction flows, commands, messages, and state machine specs

## 🚀 Quick Start

### View Latest Analysis & Data

```bash
# GTM validation deck
open reports/archive/GTM_STRATEGY_VALIDATION_REPORT.md

# Bot behavior insights
open reports/FINAL_BOT_ANALYSIS_INSIGHTS.md

# Latest CSV outputs
ls data/latest_results/
```

### Run GTM Conversion Analysis

```bash
# 1. Configure database credentials
cp .env.template .env
# Edit .env with readonly production credentials

# 2. Execute conversion pipeline
python3 scripts/gtm_conversion_analysis.py

# 3. Inspect refreshed datasets
ls data/latest_results/
```

## 📊 Key Metrics Snapshot

| Metric | Value | Status |
|--------|-------|--------|
| Marketing bot users (8 showcase bots) | 91 | Baseline |
| Existing creators within cohort | 21 (23.1%) | ✅ High leverage |
| Net-new conversions post-experience | 0 | 🔴 Critical issue |
| High-intent non-creators | 70 | 🎯 Outreach target |

## 💡 Current Priorities

### Immediate (0-1 Week)
- Embed remix education and CTAs inside marketing bot welcome/onboarding flows
- Launch targeted outreach to the 70 high-intent non-creators with tailored prompts
- QA remix runtime to ensure blockers are documented or removed

### Short-term (1-4 Weeks)
- Ship a "Clone & Tweak" lightweight alternative for users avoiding full remix
- Cross-promote showcase bots to the 558 compatible creators already on the platform
- Measure remix → creator funnel weekly and track uplift vs. baseline (0%)

Full action plans: [`reports/archive/GTM_STRATEGY_VALIDATION_REPORT.md`](reports/archive/GTM_STRATEGY_VALIDATION_REPORT.md)

## 🔧 Maintenance Scripts

```bash
# Optional: replay file reorganization (kept for reference)
bash reorganize_files.sh
```

Refer to `reports/archive/REORGANIZATION_PLAN.md` for a full changelog of the 2025-10-28 restructure.

## 📖 Quick Reference Links

- [AI Agent Guide](docs/product/CLAUDE.md)
- [Product Context](docs/product/product_context.md)
- [Interaction Overview](docs/product/shellagent_interaction_overview.md)
- [Quick Start Guide](docs/QUICKSTART.md)
- [Execution Guide](docs/EXECUTION_GUIDE.md)

## Value Proposition

This repository is the single source of truth for ShellAgent product decisions, experiment planning, and GTM analytics. Find:

- ✅ Data-backed GTM insights and prioritized recommendations
- ✅ Up-to-date analysis scripts aligned with production tables
- ✅ Ready-to-run MCP workflows for external research validation
- ✅ Comprehensive documentation for onboarding new analysts or agents

Contribute improvements by keeping data outputs current, logging MCP limitations, and documenting new findings in `reports/`.


