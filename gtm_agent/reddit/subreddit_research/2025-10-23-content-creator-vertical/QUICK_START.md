# Quick Start Guide - Reddit GTM Campaign

This guide will help you launch a Reddit marketing campaign in 3-4 hours using the improved workflow with real bots.

---

## Prerequisites

- ✅ Two Reddit accounts (one for OP, one for shill comments)
- ✅ Both accounts have some karma and post history (at least 100 karma each)
- ✅ Access to Claude with MCP tools enabled
- ✅ Python 3.8+ installed (for tracking scripts)

---

## Phase 1: Research (60 min)

### Step 1: Validate Target Subreddits (30 min)

Open Claude and run:

```
Use the Reddit MCP tool to fetch hot threads from these subreddits:
- r/NewTubers
- r/YouTubers
- r/ContentMarketing
- r/GrowthHacking
- r/Blogging

For each subreddit, analyze:
1. Average upvotes and comments
2. Community tone (supportive vs critical)
3. Post quality (detailed vs spam)

Generate a validation report scoring each as Tier 1/2/3.
```

**Output**: Save results to `subreddit_validation.md`

---

### Step 2: Analyze Community Style (30 min)

For your top 3 Tier 1 subreddits:

```
For r/[SUBREDDIT], fetch the top 10 hot threads and analyze:
1. Capitalization patterns (formal vs casual)
2. Common post angles (questions, experiences, experiments)
3. Comment engagement style
4. Acceptable promotion level

Generate a style guide for this community.
```

**Output**: Save to `community_style_analysis.md`

---

## Phase 2: Content Generation (90 min)

### Step 3: Select Posts to Deploy (15 min)

Review `draft_posts_v3_real_bots.md` and select 4-6 posts:

**Selection Criteria**:
- ✅ Post fits validated subreddit's style
- ✅ Uses real bots only (check bot names)
- ✅ OP and shill have different writing styles
- ✅ Comments don't use bullet points
- ✅ No "built it with shell agent" mentions
- ✅ Provides value beyond bot promotion

**Recommended Starting Posts**:
- Post 1 (r/GrowthHacking) - Time sink discussion
- Post 2 (r/NewTubers) - YouTube lessons learned
- Post 8 (r/ContentMarketing) - Failure vs success posts
- Post 15 (r/YouTubers) - Stuck at 1k subs

---

### Step 4: Customize Posts (45 min)

For each selected post:

1. **Adjust for subreddit style**
   - Match capitalization patterns from your analysis
   - Adjust tone (more/less casual)

2. **Verify bot mentions are natural**
   - Check bot exists in real_bots_mapping.md
   - Ensure context makes sense
   - Keep pricing vague

3. **Check differentiation**
   - OP style ≠ shill style
   - Comments are flowing paragraphs
   - No obvious tells they're the same person

**Output**: Save customized posts to `final_posts_for_deployment.md`

---

### Step 5: Create Deployment Schedule (30 min)

Map posts to subreddits and times:

**Day 1**:
- 7am EST: Post 1 → r/GrowthHacking
- 2pm EST: Post 2 → r/NewTubers

**Day 3**:
- 8am EST: Post 8 → r/ContentMarketing
- 6pm EST: Post 15 → r/YouTubers

**Day 4-5** (Shill comments):
- +24h after each post: Deploy shill comment
- +2-6h after shill: Deploy OP reply

**Output**: `deployment_schedule.md`

---

## Phase 3: Deployment (30-60 min)

### Step 6: Deploy Main Posts (20 min)

For each scheduled post:

1. Log into **OP Reddit account**
2. Navigate to subreddit
3. Click "Create Post"
4. Copy-paste title and body from final_posts_for_deployment.md
5. Submit
6. **Copy post URL immediately**
7. Add to tracking:

```bash
python3 scripts/track_posts.py
# Choose option 1: Add new post
# Enter: subreddit, title, URL
```

**Pro tip**: Set phone reminders for shill comment timing (12-24h later)

---

### Step 7: Monitor Initial Response (24 hours)

Check each post after 6-12 hours:

**Good signs** ✅:
- 5+ upvotes
- 2+ real user comments
- Supportive or curious tone

**Warning signs** ⚠️:
- 0 or negative upvotes
- Accusatory comments ("this is an ad")
- Post shows [removed]

**Action**: If post is removed, note the reason and adjust future posts

---

### Step 8: Deploy Shill Comments (30 min, next day)

After 12-24 hours:

1. Check if post has any real comments
2. If yes, read them first (helps you blend in)
3. Log into **shill Reddit account** (different from OP)
4. Navigate to your post
5. Comment with shill content from final_posts_for_deployment.md
6. **Don't use exact copy-paste** - adjust tone slightly
7. Add to tracking

**Timing**:
- Don't reply immediately as OP
- Wait 2-6 hours
- If real users comment on shill, reply to them first (as shill)
- Then reply as OP

---

## Phase 4: Monitoring (Ongoing)

### Step 9: Daily Check (5 min/day)

Update post metrics:

```bash
python3 scripts/track_posts.py
# Choose option 2: Update metrics
# Enter: post ID, current upvotes, comments
```

**What to track**:
- Upvotes (main post and shill comment)
- Real user comments
- Tone of engagement
- Any accusations of advertising
- Post removal

---

### Step 10: Respond to Real Users (As needed)

When real users ask questions:

**Do** ✅:
- Reply authentically as OP
- Provide helpful info beyond bots
- Acknowledge when bot isn't perfect
- Share your actual experience

**Don't** ❌:
- Copy-paste replies
- Ignore non-bot questions
- Over-promote bots
- Get defensive about criticism

---

### Step 11: Weekly Analysis (60 min, end of week)

Generate report:

```bash
python3 scripts/track_posts.py
# Choose option 4: Generate report
```

Review:
- Which subreddits performed best?
- Which post angles got most engagement?
- Any posts removed? Why?
- Any accusations of advertising?
- Real user feedback themes

**Output**: `weekly_analysis.md` with insights

---

## Success Criteria

### Per Post:
- **Minimum**: Not removed, 3+ upvotes, 1+ real comment
- **Good**: 10+ upvotes, 5+ real comments
- **Great**: 30+ upvotes, 10+ real comments, follow-up questions

### Per Campaign (4-6 posts):
- **Minimum**: 80% posts survive, 50% have real engagement
- **Good**: 100% posts survive, 75% have real engagement
- **Great**: 100% posts survive, 100% have engagement, 1+ viral (50+ upvotes)

---

## Red Flags (Stop and Revise)

⛔ **Stop if**:
- 2+ posts removed in first 3 days
- Multiple users accuse you of advertising
- Shill comments consistently downvoted
- Zero real user engagement across all posts

🔄 **Then**:
1. Review what went wrong
2. Adjust writing style or bot mentions
3. Test on lower-risk subreddits first
4. Increase value-to-promotion ratio

---

## Common Mistakes to Avoid

### 1. Posting Too Fast
❌ Bad: Post to same subreddit twice in one day
✅ Good: Space posts 2-3 days apart

### 2. Obvious Shill Comments
❌ Bad: "I use @BotName and it costs $4 and saves 2 hours!"
✅ Good: "been testing a few bots lately, @BotName helps with titles but needs editing like 30% of the time"

### 3. Identical Writing Styles
❌ Bad: OP and shill both use lowercase, same colloquialisms
✅ Good: OP uses proper caps, shill uses lowercase OR vice versa

### 4. No Real Value
❌ Bad: Post is just a vehicle for bot promotion
✅ Good: Post provides insights, bot is mentioned as one tool among many

### 5. Replying Too Fast
❌ Bad: OP replies to shill within 5 minutes
✅ Good: OP waits 2-6 hours, maybe replies to other comments first

---

## Tools and Files Reference

### Key Documents:
- `draft_posts_v3_real_bots.md` - Post templates with real bots
- `differentiated_style_guide.md` - Writing style guidelines
- `real_bots_mapping.md` - List of real bots and use cases
- `end_to_end_workflow.md` - Detailed workflow documentation

### Scripts:
- `scripts/research_subreddits.py` - Automate subreddit research
- `scripts/track_posts.py` - Track post performance

### Tracking Files (you'll create these):
- `subreddit_validation.md`
- `community_style_analysis.md`
- `final_posts_for_deployment.md`
- `deployment_schedule.md`
- `post_tracking.json`
- `performance_tracking.csv`
- `weekly_analysis.md`

---

## Need Help?

### Issue: Post got removed
**Check**:
- Does your account meet karma requirements?
- Did you trigger keyword filters? (check title for "free", "bot", "tool")
- Is account age sufficient? (some subs require 30+ days)

**Fix**: Post with older account or adjust wording

---

### Issue: Shill comment accused of being ad
**Check**:
- Is bot mention too prominent?
- Did you acknowledge limitations?
- Is the comment mostly about bot vs mostly about experience?

**Fix**: Rewrite to focus 70% on experience, 30% on bot

---

### Issue: No real user engagement
**Check**:
- Is post providing value?
- Is title compelling?
- Did you post during peak hours?

**Fix**: Study top posts in subreddit more carefully, adjust angles

---

## Timeline at a Glance

**Week 1**:
- Day 1: Research + deploy 2 posts (3-4 hours)
- Day 2-3: Deploy 2 more posts (30 min)
- Day 4-5: Deploy shill comments (60 min)
- Daily: Monitor and respond (5-10 min/day)

**Week 2**:
- Continue monitoring
- Deploy remaining shill comments
- Respond to engagement
- End-of-week analysis (60 min)

**Total time**: ~6-8 hours across 2 weeks

---

## Next Steps

1. ✅ Read this quick start guide
2. ✅ Ensure you have 2 Reddit accounts with karma
3. ✅ Run Phase 1 research (60 min)
4. ✅ Generate and customize posts (90 min)
5. ✅ Deploy first 2 posts
6. ✅ Set reminders for shill comments (12-24h later)
7. ✅ Monitor and iterate

**Good luck! 🚀**

---

## Questions?

Refer to `end_to_end_workflow.md` for detailed workflow
Refer to `differentiated_style_guide.md` for writing guidelines
Refer to `real_bots_mapping.md` for bot information
