# ShellAgent Product Operations

This repository collects the product operations, research, and analysis collateral for the ShellAgent Telegram bot builder. It mirrors the materials used to investigate user behavior, identify churn drivers, and plan interaction and algorithm improvements across the ShellAgent experience.

## Repository Contents

- `CLAUDE.md` – Master guide covering data sources, analysis workflows, and documentation references for ShellAgent.
- `product_context.md` – Product capabilities, constraints, and GTM notes to validate feasibility of user requests.
- `analysis_runs/` – End-to-end analysis artifacts (data deep-dives, interaction gap reports, best-practice research, and phase deliverables from the 2025-10-25 study).
- `tgbot/` – Technical documentation for ShellAgent bots (commands, state machine, messages, API endpoints, and interaction flows).
- `query.md` – API recipes for fetching raw conversation history and bot usage data.
- `task_v6.md` – User behavior annotation methodology.
- `wide_research_prompt.md` – Framework for large-scale competitive and UX research.
- `shellagent_interaction_overview.md` – Expected golden path and system architecture overview.
- `analysis_runs/run_2025-10-25/input/user_behavior_analysis.csv` – Annotated dataset of 276 user sessions used in the latest analyses.

## Getting Started

```bash
git clone https://github.com/hancez/tg_product_ops.git
cd tg_product_ops
```

All documentation is Markdown or CSV and can be opened with any text editor or spreadsheet tool. For data analysis, load the CSV into your analytics environment of choice (Python, R, spreadsheet) following the column definitions in `CLAUDE.md`.

## Value Proposition

The repository provides:

- A complete snapshot of user behavior findings and prioritized product issues (see `analysis_runs/.../deliverables`).
- Tactical UX and algorithm recommendations to increase ShellAgent’s bot success rate from 8.4% to an expected 25–35%.
- Technical reference material to align product insights with implementation constraints.

Use this repo as the single source of truth when coordinating ShellAgent product decisions, planning experiments, or onboarding new collaborators to the analysis workstream.


