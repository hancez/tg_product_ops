# Reddit GTM End-to-End Workflow
**Version**: 1.0
**Date**: 2025-10-27
**Purpose**: Complete workflow from subreddit research to post deployment

---

## Overview

This workflow covers:
1. **Phase 1**: Subreddit research and validation
2. **Phase 2**: Content generation with real bots
3. **Phase 3**: Post deployment and tracking
4. **Phase 4**: Monitoring and iteration

Total time: ~3-4 hours per campaign

---

## Phase 1: Subreddit Research (60-90 min)

### Step 1.1: Identify Target Subreddits (15 min)

**Input**: Target vertical (e.g., "content creators", "YouTubers", "bloggers")

**Process**:
1. Brainstorm seed subreddits based on vertical
2. Use Tavily to find related subreddits
3. Create initial list of 10-15 candidates

**Tools**:
- `mcp__tavily__tavily_search` for discovery
- Manual brainstorming

**Output**: `target_subreddits.md` with candidate list

**Example**:
```bash
# Tavily query
"content creator subreddits YouTube TikTok Instagram"
"YouTuber communities small channels growth"
```

---

### Step 1.2: Validate Subreddits (30-45 min)

**Input**: Candidate subreddit list

**Process**:
For each subreddit:
1. Fetch hot threads using Reddit MCP
2. Analyze:
   - Member engagement (upvotes, comments)
   - Content quality (detailed posts vs spam)
   - Community tone (supportive vs toxic)
   - Posting frequency
3. Check rules (manual verification at /r/[name]/about/rules)
4. Score subreddit as Tier 1/2/3

**Tools**:
- `mcp__reddit__fetch_reddit_hot_threads`
- Manual rule checking

**Output**: `subreddit_validation.md` with scores

**Scoring Criteria**:
- **Tier 1**: 100k+ members, active daily, permits soft promotion, supportive tone
- **Tier 2**: 20k-100k members, active weekly, limited promotion, mixed tone
- **Tier 3**: <20k members, sporadic activity, strict rules, risky tone

**Keep**: Only Tier 1 and selected Tier 2 subreddits

---

### Step 1.3: Analyze Community Style (15-30 min)

**Input**: Validated subreddit list

**Process**:
For each Tier 1 subreddit:
1. Fetch top 10 hot threads
2. Read post bodies and top comments
3. Document:
   - Writing style (formal vs casual, capitalization patterns)
   - Post angles (questions, experiences, experiments, help requests)
   - Comment patterns (short vs detailed, supportive vs critical)
   - Acceptable promotion level (none, subtle, direct)

**Tools**:
- `mcp__reddit__fetch_reddit_post_content` for detailed analysis

**Output**: `community_style_analysis.md`

---

## Phase 2: Content Generation (90-120 min)

### Step 2.1: Map Real Bots to Use Cases (20 min)

**Input**: Real bot list (from `real_bots_mapping.md`)

**Process**:
1. Review available real bots
2. Map bots to target subreddit pain points
3. Create use case scenarios

**Example**:
- r/NewTubers pain points: titles, thumbnails, hooks
- Relevant bots: @youtube_clickbait_title_bot, @myshell_thumbmaker_bot, @Hook_Generator_Bot

**Output**: `bot_use_case_mapping.md`

---

### Step 2.2: Generate Posts (60-90 min)

**Input**:
- Validated subreddits
- Community style analysis
- Bot use case mapping
- Writing style guide (`differentiated_style_guide.md`)

**Process**:
1. For each subreddit, generate 2-3 posts using different angles:
   - Open discussion
   - Observation/discovery
   - Experiment/test
   - Help/confusion

2. For each post, create:
   - Main post (OP)
   - Shill comment 1 (posted 12-24h later)
   - Shill comment 2 (optional, if needed)
   - OP replies to shill comments

3. Apply differentiated writing styles:
   - OP: Style A (e.g., proper capitalization, organized)
   - Shill 1: Style B (e.g., lowercase, casual)
   - OP Reply: Match OP's main style

4. Include real bot mentions naturally:
   - In context of solving a problem
   - Acknowledge limitations (30% need editing, etc.)
   - Vague pricing ("like $4 for 50 uses")
   - No "built it with shell agent" mentions

**Tools**:
- Claude with style guide context
- Manual editing for authenticity

**Output**: `draft_posts_v3_real_bots.md`

---

### Step 2.3: Quality Check (10-20 min)

**Input**: Draft posts

**Process**:
Check each post for:
- [ ] OP and shill have different writing styles
- [ ] Comments use flowing paragraphs (no bullet points)
- [ ] Bot mentions are natural and in context
- [ ] No "built it with shell agent" mentions
- [ ] Limitations acknowledged naturally
- [ ] Price mentions are vague and casual
- [ ] Post angle fits subreddit culture
- [ ] Content provides value beyond bot promotion

**Output**: Approved posts ready for deployment

---

## Phase 3: Post Deployment (30-60 min)

### Step 3.1: Prepare Deployment Schedule (10 min)

**Input**: Approved posts

**Process**:
1. Assign each post to a subreddit
2. Schedule posting times:
   - Don't post multiple posts to same subreddit on same day
   - Space posts 2-3 days apart per subreddit
   - Consider subreddit peak hours (usually 7am-10am, 5pm-8pm local time)

**Output**: `deployment_schedule.md`

**Example**:
```
Day 1:
- 7am EST: Post 1 to r/NewTubers
- 2pm EST: Post 2 to r/ContentMarketing

Day 3:
- 8am EST: Post 3 to r/YouTubers
- 6pm EST: Post 4 to r/GrowthHacking

Day 5:
- 7am EST: Shill comment on Post 1 (r/NewTubers)
- 3pm EST: Shill comment on Post 2 (r/ContentMarketing)
```

---

### Step 3.2: Deploy Main Posts (20-30 min)

**Process**:
1. Use OP Reddit account
2. Copy post title and body from approved posts
3. Submit to scheduled subreddits
4. Record post URLs in tracking sheet

**Manual Steps** (Reddit requires manual posting):
- Log into Reddit account
- Navigate to subreddit
- Click "Create Post"
- Paste title and body
- Submit
- Copy post URL

**Output**: `post_tracking.md` with URLs

---

### Step 3.3: Deploy Shill Comments (20-30 min, 12-24h after main posts)

**Process**:
1. Wait 12-24 hours after main post
2. Use shill Reddit account (different from OP)
3. Comment on main post with shill comment
4. Wait for OP reply trigger (either real users asking questions OR after 4-6 hours)
5. Reply with OP account

**Timing Strategy**:
- Don't reply immediately (looks fake)
- Wait for 1-2 real comments first (if possible)
- OP reply should come 2-6 hours after shill comment

**Output**: Updated `post_tracking.md` with comment URLs

---

## Phase 4: Monitoring and Iteration (Ongoing)

### Step 4.1: Track Performance (Daily for first week)

**Metrics to Track**:
- Upvotes on main post
- Comment count
- Shill comment upvotes
- OP reply upvotes
- Real user engagement (questions, follow-ups)
- Negative signals (downvotes, accusations of advertising)
- Post removal (deleted by mods)

**Tools**:
- Manual checking (Reddit doesn't have good APIs for this)
- Spreadsheet tracking

**Output**: `performance_tracking.csv`

---

### Step 4.2: Respond to Real Users (As needed)

**Process**:
When real users ask questions:
1. Reply authentically as OP
2. Provide helpful info beyond just bot mentions
3. Don't be overly promotional
4. Acknowledge when bot isn't the best solution

**Red Flags to Avoid**:
- Copy-paste replies
- Ignoring non-bot questions
- Over-promoting bots
- Defensive responses to criticism

---

### Step 4.3: Analyze and Iterate (Weekly)

**Process**:
1. Review performance data
2. Identify patterns:
   - Which subreddits performed best?
   - Which post angles got most engagement?
   - Which bots resonated most?
   - What caused negative reactions?
3. Update strategy for next batch

**Output**: `weekly_analysis.md`

**Key Questions**:
- Did posts get removed? Why?
- Did shill comments get accused of being ads?
- Which writing styles worked best?
- Were bot mentions too obvious or too subtle?
- Did we provide enough value beyond promotion?

---

## Workflow Automation Scripts

### Script 1: Subreddit Research

```python
# research_subreddits.py
# Fetches hot threads from target subreddits
# Outputs: subreddit_validation.md

import json
import time

subreddits = [
    "NewTubers",
    "YouTubers",
    "ContentMarketing",
    "GrowthHacking",
    "Blogging",
    "Podcasting"
]

for sub in subreddits:
    # Use MCP tool: mcp__reddit__fetch_reddit_hot_threads
    print(f"Researching r/{sub}...")
    # Process results
    time.sleep(2)  # Rate limiting
```

---

### Script 2: Style Analysis

```python
# analyze_community_style.py
# Analyzes top posts for writing patterns
# Outputs: community_style_analysis.md

def analyze_post_style(post_content):
    patterns = {
        "lowercase_starts": 0,
        "bullet_points": 0,
        "avg_paragraph_length": 0,
        "colloquialisms": [],
        "capitalization_style": ""
    }
    # Analysis logic
    return patterns
```

---

### Script 3: Deployment Tracking

```python
# track_posts.py
# Tracks post URLs and performance
# Outputs: post_tracking.md, performance_tracking.csv

import csv
from datetime import datetime

class PostTracker:
    def __init__(self):
        self.posts = []

    def add_post(self, subreddit, title, url, timestamp):
        self.posts.append({
            "subreddit": subreddit,
            "title": title,
            "url": url,
            "timestamp": timestamp,
            "upvotes": 0,
            "comments": 0
        })

    def update_metrics(self, url, upvotes, comments):
        # Update post metrics
        pass

    def export_csv(self):
        # Export to CSV
        pass
```

---

## Common Issues and Solutions

### Issue 1: Post Gets Removed
**Cause**: Triggered subreddit filters (keywords, account age, karma)
**Solution**:
- Check if account has minimum karma requirements
- Avoid obvious marketing keywords in title
- Try posting from account with more history

### Issue 2: Shill Comment Accused of Being Ad
**Cause**: Too obvious, too salesy, or timing is suspicious
**Solution**:
- Make shill comment more about sharing experience, less about bot
- Acknowledge bot limitations more prominently
- Don't mention pricing in shill comment
- Wait longer before posting shill comment (24h+ instead of 12h)

### Issue 3: No Real User Engagement
**Cause**: Post doesn't provide enough value or doesn't fit community
**Solution**:
- Increase value-to-promotion ratio (90% value, 10% bot mention)
- Choose more relatable post angles
- Study top posts in community more carefully

### Issue 4: Low Upvotes
**Cause**: Title isn't compelling or posting time is bad
**Solution**:
- Test different title formats (curiosity vs descriptive)
- Post during peak hours (7-10am, 5-8pm EST)
- Make first sentence of body more engaging

---

## Success Metrics

### Per Post:
- **Good**: 5+ upvotes, 3+ real comments
- **Great**: 20+ upvotes, 10+ real comments, 1+ follow-up questions
- **Excellent**: 50+ upvotes, 20+ real comments, multiple real users discussing bot

### Per Campaign (10 posts):
- **Good**: 70%+ posts not removed, 3+ posts with real engagement
- **Great**: 90%+ posts not removed, 6+ posts with real engagement, 2+ viral posts (50+ upvotes)
- **Excellent**: 100% posts not removed, 8+ posts with real engagement, 5+ viral posts

### Red Flags (Stop and Revise):
- 3+ posts removed in first week
- Multiple accusations of advertising
- Consistent 0 or negative upvotes
- No real user questions or engagement

---

## File Structure

```
gtm agent/reddit/subreddit_research/[campaign-date]/
├── target_subreddits.md
├── subreddit_validation.md
├── community_style_analysis.md
├── bot_use_case_mapping.md
├── draft_posts_v3_real_bots.md
├── deployment_schedule.md
├── post_tracking.md
├── performance_tracking.csv
└── weekly_analysis.md
```

---

## Timeline Summary

**Day 1** (3-4 hours):
- Subreddit research (90 min)
- Content generation (90-120 min)
- Deploy first 2-3 posts (20 min)

**Day 2-3** (30 min):
- Deploy next 2-3 posts
- Monitor first posts

**Day 4-5** (60 min):
- Deploy shill comments on first posts
- Deploy final posts
- Respond to real users

**Week 2** (2-3 hours):
- Continue monitoring
- Deploy shill comments on later posts
- Respond to engagement
- Analyze performance

**Week 3-4** (1 hour):
- Final performance analysis
- Iterate strategy for next campaign

---

**End of Workflow**
