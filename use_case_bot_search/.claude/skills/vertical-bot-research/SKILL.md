---
name: Vertical Bot Research
description: Research and identify Telegram bot use cases for specific verticals (e.g., content creators, developers, educators). Use when exploring what bot to build for a target audience, finding product-market fit, or identifying trending opportunities. Analyzes Product Hunt, Hacker News, YouTube, and GitHub to discover viable bot ideas that match Telegram's capabilities.
allowed-tools: mcp__tavily__tavily_search, mcp__hackernews__getTopStories, mcp__hackernews__getItem, mcp__reddit__fetch_reddit_hot_threads, Read, Write, Glob, Grep, Bash
---

# Vertical Bot Research

Research use cases for Telegram bots targeting specific verticals by analyzing trending products, discussions, and content across multiple platforms.

## Objective

Identify 5-10 high-potential Telegram bot ideas for a given vertical by:
1. Scanning Product Hunt, Hacker News, and YouTube for trending automation tools
2. Analyzing pain points and workflows in the target vertical
3. Filtering ideas by Telegram bot technical capabilities
4. Prioritizing based on market validation and implementation feasibility

## Target Bot Capabilities (Telegram Platform)

### ✅ Can Do
- **Interaction**: Simple CRUD Mini Apps, LUI (Language UI) with buttons, natural language chat
- **Generation**: Images, videos, text, audio
- **Personal Tools**: Planners, trackers, reminders, habit tracking
- **Modal Conversion**: Audio→text, video→text, text→image, image→text, etc.
- **Data Scraping**: Web scraping, API integrations, RSS feeds
- **External APIs**: Payment APIs, calendar APIs, social media APIs
- **Scheduling**: Cron jobs, timed reminders, recurring tasks
- **Group Bots**: Group management, moderation, activity tracking
- **Multi-Input**: Accept images, audio, video, documents as input

### ❌ Cannot Do
- Complex B2B SaaS products
- Real-time collaborative editing (beyond basic group chat)
- Heavy data processing requiring persistent databases (limited by Telegram storage)
- Native mobile app features (camera filters, AR, etc.)

## Research Workflow

### Phase 1: Vertical Definition (5 min)
1. Define target vertical (e.g., "content creators", "developers", "fitness coaches")
2. Identify key personas and pain points
3. List common workflows and tools used in the vertical

### Phase 2: Multi-Source Data Collection (20-30 min)

Execute in parallel:

**A. Product Hunt Search** (Use tavily_search)
- Query: `site:producthunt.com [vertical] automation tool 2025`
- Extract: Top 10 products with description, votes, key features
- Focus: Tools with >100 upvotes launched in last 6 months

**B. Hacker News Analysis** (Use mcp__hackernews__)
- Get top stories related to the vertical
- Analyze comments for pain points and feature requests
- Identify trending automation patterns

**C. YouTube Content Mining** (Use tavily_search + transcript analysis)
- Search: `[vertical] automation workflow tutorial`
- Target: Videos with >50k views from last 12 months
- Extract: Workflow steps, tools mentioned, pain points discussed
- **Innovation**: Transcribe top 3-5 videos to understand exact workflows

**D. GitHub Trending** (Use tavily_search)
- Query: `site:github.com [vertical] automation bot telegram`
- Identify: Existing bots, star count, feature sets
- Extract: Popular features, gaps in current solutions

### Phase 3: Idea Filtering (10 min)

For each discovered tool/workflow, evaluate:

**Technical Fit Score (1-5)**
- Can it be implemented with Telegram bot capabilities?
- Does it require complex infrastructure?
- Can it be completed in ~10 min generation time?

**Market Validation Score (1-5)**
- Product Hunt votes / HN comments / YouTube views
- Evidence of real user pain
- Existing competitors (moderate competition = validated market)

**Remix Potential (1-5)**
- Can users easily customize for their needs?
- Clear template structure?
- Multiple use case variations?

### Phase 4: Report Generation (15 min)

Create structured report with:

1. **Executive Summary**: Top 3 bot ideas with one-line pitch
2. **Detailed Analysis**: For each idea (5-10 total):
   - Name & Description
   - Target User Persona
   - Key Features (3-5 bullet points)
   - Technical Feasibility Score
   - Market Validation Score
   - Example Workflow
   - Source Links (Product Hunt, HN, YouTube, GitHub)
   - Remix Opportunities
3. **Implementation Roadmap**: Suggested build order
4. **Risk & Limitations**: Potential blockers

## Output Format

```markdown
# [Vertical] Telegram Bot Research Report
**Date**: [YYYY-MM-DD]
**Vertical**: [Target audience]

## Executive Summary
1. **[Bot Idea 1]**: [One-line pitch] (Technical: 4/5, Market: 5/5)
2. **[Bot Idea 2]**: [One-line pitch] (Technical: 5/5, Market: 4/5)
3. **[Bot Idea 3]**: [One-line pitch] (Technical: 3/5, Market: 5/5)

## Detailed Bot Ideas

### 1. [Bot Name]
**Persona**: [Target user]
**Pitch**: [2-3 sentence description]

**Key Features**:
- Feature 1
- Feature 2
- Feature 3

**Example Workflow**:
1. Step 1
2. Step 2
3. Step 3

**Technical Feasibility**: [Score + reasoning]
**Market Validation**: [Evidence with links]
**Remix Opportunities**: [How users can customize]

**Sources**:
- Product Hunt: [link]
- Hacker News: [link]
- YouTube: [link]

---

[Repeat for each bot idea]

## Implementation Roadmap
1. **Quick Win**: [Easiest bot to build first]
2. **High Impact**: [Most valuable bot]
3. **Moonshot**: [Ambitious but high reward]

## Risks & Limitations
- [Limitation 1]
- [Limitation 2]
```

## Data Collection Best Practices

1. **Timestamps**: Always note data collection date (trends shift fast)
2. **Source Attribution**: Link to every claim for verifiability
3. **Confidence Levels**:
   - [Verified]: Multiple sources confirm
   - [Inferred]: Based on indirect evidence
   - [Unverified]: Needs manual check

4. **Bias Awareness**:
   - Product Hunt skews toward tech-savvy users
   - HN favors developer tools
   - YouTube shows public workflows (not enterprise)

## Example Queries

**For Content Creators Vertical**:
- Product Hunt: `site:producthunt.com content creator automation social media 2025`
- HN: Search stories mentioning "creator economy", "content workflow"
- YouTube: `content creator automation workflow tutorial`
- GitHub: `site:github.com telegram bot social media content`

**For Fitness Coaches Vertical**:
- Product Hunt: `site:producthunt.com fitness coaching client management`
- YouTube: `fitness coach client tracking automation`
- Reddit: Use mcp__reddit__ to fetch r/fitness, r/personaltraining

## Edge Cases

1. **Too Few Results**: Broaden vertical definition or search adjacent verticals
2. **Too Many Results**: Narrow to sub-niche (e.g., "YouTube creators" vs "content creators")
3. **Outdated Data**: Filter by date, prioritize 2024-2025 content
4. **Paywall Content**: Use tavily_extract or skip (don't violate terms)

## Quality Checklist

Before finalizing report:
- [ ] At least 5 bot ideas documented
- [ ] Each idea has Technical + Market scores
- [ ] All sources have clickable links
- [ ] Example workflows are concrete (not vague)
- [ ] Remix opportunities identified
- [ ] Report follows markdown template
- [ ] Data collection date noted
- [ ] No hallucinated features (verify against Telegram capabilities)

## Next Steps After Research

1. **User Validation**: Share top 3 ideas in target community (Telegram groups, Reddit)
2. **Prototype**: Build simplest bot first using Playground
3. **Iterate**: Get user feedback, remix based on needs
4. **Scale**: Package as template for wider distribution

---

**Remember**: The goal is not perfection, but actionable insights. Bias toward shipping and learning.
