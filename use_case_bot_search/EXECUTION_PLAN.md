# Vertical Bot Research - Execution Plan

## Overview

This plan outlines how to use the Vertical Bot Research agent to identify high-potential Telegram bot ideas for specific verticals.

## Agent Architecture

```
Vertical Bot Research Agent
│
├── Input: Target Vertical (e.g., "content creators")
│
├── Data Collection (Parallel)
│   ├── Product Hunt → Trending automation tools
│   ├── Hacker News → Pain points & discussions
│   ├── YouTube → Workflow tutorials & pain points
│   └── GitHub → Existing bots & feature gaps
│
├── Analysis Pipeline
│   ├── Filter by Telegram capabilities
│   ├── Score: Technical Feasibility (1-5)
│   ├── Score: Market Validation (1-5)
│   └── Score: Remix Potential (1-5)
│
└── Output: Structured Report (5-10 bot ideas)
```

## Usage Instructions

### Quick Start

1. Navigate to the project directory:
```bash
cd "/Users/hancezhang/Claude code exp/use_case_bot_search"
```

2. Start Claude Code:
```bash
claude
```

3. Invoke the research agent:
```
Research Telegram bot use cases for [VERTICAL_NAME]
```

Example verticals:
- Content creators
- Fitness coaches
- Language learners
- Small business owners
- Developers
- Teachers/educators
- Photographers

### Sample Prompts

**Basic Research**:
```
Research Telegram bot use cases for content creators
```

**Focused Research**:
```
Research Telegram bot use cases for YouTube creators specifically focused on video editing workflow automation
```

**Comparative Research**:
```
Compare top Telegram bot ideas for fitness coaches vs. nutrition coaches
```

## Expected Workflow

### Phase 1: Data Collection (20-30 min)

The agent will:
1. Search Product Hunt for automation tools in your vertical
2. Fetch top Hacker News stories and analyze comments
3. Find and transcribe relevant YouTube tutorial videos
4. Search GitHub for existing Telegram bots

**Parallel Execution**:
- 4-6 MCP tool calls per batch
- 2-3 batches total
- Each source produces child_outputs/<source>.md

### Phase 2: Analysis (10-15 min)

For each discovered tool/workflow:
1. Evaluate technical fit (Can Telegram do this?)
2. Assess market validation (Is there demand?)
3. Identify remix potential (Can users customize?)

### Phase 3: Report Generation (10 min)

Structured markdown report with:
- Executive summary (top 3 ideas)
- Detailed analysis (5-10 bot ideas)
- Implementation roadmap
- Risks & limitations

**Total Time**: ~45-55 minutes

## Output Structure

```
runs/
└── YYYY-MM-DD-[vertical]-research/
    ├── child_outputs/
    │   ├── producthunt.md
    │   ├── hackernews.md
    │   ├── youtube.md
    │   └── github.md
    ├── raw/
    │   └── [cached API responses]
    ├── logs/
    │   └── [execution logs]
    ├── final_report.md          # Main deliverable
    └── aggregated_raw.md        # Audit trail
```

## Telegram Bot Capability Matrix

Use this to quickly evaluate if an idea fits:

| Capability | Example | Feasibility |
|------------|---------|-------------|
| CRUD Mini App | Habit tracker, expense log | ✅ High |
| LUI Chat | Q&A bot, conversational planner | ✅ High |
| Image Generation | AI art bot, thumbnail creator | ✅ High |
| Video Generation | Short video creator, montages | ✅ Medium |
| Text Generation | Blog post drafts, captions | ✅ High |
| Audio→Text | Voice note transcription | ✅ High |
| Video→Text | YouTube video summarizer | ✅ High |
| Text→Image | Meme generator, quote cards | ✅ High |
| Data Scraping | RSS reader, price tracker | ✅ High |
| External APIs | Weather bot, stock tracker | ✅ High |
| Scheduled Tasks | Daily reminders, recurring reports | ✅ High |
| Group Moderation | Auto-welcome, spam filter | ✅ High |
| Real-time Collab | Live document editing | ❌ Low |
| B2B SaaS | Multi-tenant CRM | ❌ Low |
| Heavy Compute | Video rendering, ML training | ❌ Low |

## Example: Content Creator Research

### Sample Output

```markdown
# Content Creator Telegram Bot Research Report
**Date**: 2025-10-24
**Vertical**: YouTube & Social Media Creators

## Executive Summary
1. **Caption AI**: Generate Instagram/TikTok captions from video descriptions (Technical: 5/5, Market: 5/5)
2. **Content Calendar Bot**: Schedule and track content across platforms (Technical: 4/5, Market: 5/5)
3. **Thumbnail A/B Tester**: Compare thumbnail performance (Technical: 3/5, Market: 4/5)

## Detailed Bot Ideas

### 1. Caption AI
**Persona**: Social media creators posting 5-10x per week
**Pitch**: Transform video scripts or descriptions into engaging captions for Instagram, TikTok, YouTube community posts. Supports tone variations (casual, professional, funny).

**Key Features**:
- Input: Video script, topic, or rough notes
- Output: 3-5 caption variations with hashtags
- Tone selector: Casual, professional, humorous, inspirational
- Platform optimizer: Different lengths for IG vs TikTok

**Example Workflow**:
1. Creator sends voice note describing video
2. Bot transcribes voice note
3. Bot generates 5 caption variations
4. Creator selects favorite, bot copies to clipboard

**Technical Feasibility**: 5/5
- Voice→text: ✅ Native capability
- Text→text generation: ✅ LLM integration
- No complex state management: ✅ Stateless

**Market Validation**:
- Product Hunt: "CaptionGen" - 847 upvotes (2025-08)
- YouTube: "How I Write 100 Captions in 10 Minutes" - 230K views
- HN Discussion: "Caption writing is my biggest time sink" - 89 upvotes

**Remix Opportunities**:
- Add custom brand voice training
- Support multiple languages
- Integrate with scheduling tools

**Sources**:
- Product Hunt: https://producthunt.com/posts/captiongen
- YouTube: https://youtube.com/watch?v=...
- HN: https://news.ycombinator.com/item?id=...

---

[... more bot ideas ...]
```

## Advanced Usage

### Custom Scoring Weights

Modify the agent to prioritize different factors:

```
Research content creator bots but prioritize technical feasibility over market size
```

### Comparative Analysis

```
Compare bot opportunities for:
1. Fitness coaches
2. Nutrition coaches
3. Yoga instructors

Focus on group management features
```

### Niche Deep-Dive

```
Research Telegram bots specifically for podcast editors, focusing on audio workflow automation
```

## Troubleshooting

### Issue: Too Many Results
**Solution**: Narrow the vertical
```
Instead of: "Research bots for creators"
Try: "Research bots for YouTube creators with <100k subscribers"
```

### Issue: No Market Validation Found
**Solution**: Expand search timeframe or adjacent markets
```
If no data for "Telegram bots", search for "Discord bots" or "Slack bots" and adapt
```

### Issue: Ideas Don't Fit Telegram
**Solution**: Review capability matrix and re-filter
- Check that bot doesn't require real-time collaboration
- Verify no heavy compute needs
- Ensure fits CRUD / LUI / Generation pattern

## Success Metrics

After research, evaluate if output meets:

- [ ] **Quantity**: 5-10 bot ideas documented
- [ ] **Quality**: Each idea has scores and sources
- [ ] **Actionability**: Clear "Quick Win" identified
- [ ] **Differentiation**: Ideas aren't duplicates of existing popular bots
- [ ] **Feasibility**: All ideas score ≥3/5 on technical feasibility

## Next Steps After Research

1. **Validate Top Idea** (2-3 days)
   - Post in target community Telegram groups
   - Gauge interest (ask for emoji reactions)
   - Collect feature requests

2. **Build MVP** (1 week)
   - Use Shell Agent Playground
   - Implement top 3 features only
   - Test with 5-10 beta users

3. **Iterate** (2-4 weeks)
   - Collect feedback
   - Add remix templates
   - Expand feature set

4. **Scale** (ongoing)
   - Add to Telegram bot directory
   - Create YouTube tutorial
   - Share on Product Hunt

## Resources

- **Wide Research Prompt**: See `wide_research_prompt.md`
- **Product Context**: See `product_context.md`
- **SKILL Definition**: See `.claude/skills/vertical-bot-research/SKILL.md`

## Questions?

Common questions to ask the agent:

```
What data sources will you use for this research?
How long will this take?
Can you prioritize [SPECIFIC FEATURE TYPE]?
Show me examples of bots that scored 5/5 on technical feasibility
```

---

**Last Updated**: 2025-10-24
**Agent Version**: 1.0
**Estimated Completion Time**: 45-55 minutes per vertical
