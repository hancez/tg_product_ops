# Reddit GTM Campaign - Deployment Checklist

**Campaign**: Content Creator Vertical v3
**Phase**: 1 (Week 1)
**Target**: 3 posts across r/NewTubers (2) + r/ContentMarketing (1)

---

## PRE-DEPLOYMENT (Complete before posting anything)

### Account Verification
- [ ] **OP Reddit Account Ready**
  - [ ] Has 100+ karma
  - [ ] Account age 30+ days
  - [ ] Has genuine post/comment history
  - [ ] Not shadowbanned (test by posting in r/ShadowBan)

- [ ] **Shill Reddit Account Ready**
  - [ ] Has 100+ karma
  - [ ] Account age 30+ days
  - [ ] Has genuine post/comment history
  - [ ] Different IP/device from OP account
  - [ ] Not shadowbanned

### Subreddit Rules Research
- [ ] **r/NewTubers Rules Checked**
  - [ ] Visit https://www.reddit.com/r/NewTubers/about/rules
  - [ ] Note minimum karma requirement
  - [ ] Note self-promotion policy
  - [ ] Check for forbidden keywords

- [ ] **r/ContentMarketing Rules Checked**
  - [ ] Visit https://www.reddit.com/r/ContentMarketing/about/rules
  - [ ] Note minimum karma requirement
  - [ ] Note self-promotion policy
  - [ ] Check for forbidden keywords

### Content Preparation
- [ ] **Posts Ready to Copy-Paste**
  - [ ] Post 1 (r/NewTubers help) - saved in deployment doc
  - [ ] Post 2 (r/NewTubers observation) - saved in deployment doc
  - [ ] Post 3 (r/ContentMarketing data) - saved in deployment doc

- [ ] **Shill Comments Ready**
  - [ ] Shill Comment 1 (Post 1)
  - [ ] Shill Comment 2 (Post 2)
  - [ ] Shill Comment 3 (Post 3)

- [ ] **OP Replies Ready**
  - [ ] OP Reply 1 (to Shill 1)
  - [ ] OP Reply 2 (to Shill 2)
  - [ ] OP Reply 3 (to Shill 3)

### Tracking Setup
- [ ] **Tracking System Ready**
  - [ ] `track_posts.py` script tested
  - [ ] Backup spreadsheet created
  - [ ] Know how to add posts to tracker

- [ ] **Calendar Reminders Set**
  - [ ] Day 1: Deploy Post 1
  - [ ] Day 2: Deploy Shill Comment 1
  - [ ] Day 3: Deploy Post 3
  - [ ] Day 4: Deploy Post 2 + Shill Comment 3
  - [ ] Day 5: Deploy Shill Comment 2
  - [ ] Day 7: Weekly analysis

---

## DAY 1 - Monday (Post 1 Deployment)

### Morning (7-9am EST)
- [ ] **Deploy Post 1 to r/NewTubers**
  - [ ] Log into OP account
  - [ ] Navigate to r/NewTubers
  - [ ] Create text post
  - [ ] Copy title: "feeling stuck at 1k subs for 6 months. what am i doing wrong?"
  - [ ] Copy body from phase1_deployment_plan.md (Post 1)
  - [ ] Double-check no typos
  - [ ] Submit

- [ ] **Track Post 1**
  - [ ] Copy post URL immediately
  - [ ] Add to track_posts.py:
    ```bash
    python3 scripts/track_posts.py
    # Option 1: Add new post
    # Subreddit: NewTubers
    # Title: feeling stuck at 1k subs...
    # URL: [paste URL]
    # Type: main
    ```
  - [ ] Set 24-hour reminder for shill comment

### Evening Check (6-8pm EST)
- [ ] **Check Post 1 Status**
  - [ ] Post still visible? (not removed)
  - [ ] Current upvotes: _____
  - [ ] Current comments: _____
  - [ ] Any real user comments? Yes/No
  - [ ] Tone of comments: Supportive / Neutral / Critical

- [ ] **Update Tracker**
  ```bash
  python3 scripts/track_posts.py
  # Option 2: Update metrics
  # Post ID: 1
  # Upvotes: ____
  # Comments: ____
  # Status: active
  ```

---

## DAY 2 - Tuesday (Shill Comment 1)

### Morning Check (9am EST)
- [ ] **Check Post 1 Performance**
  - [ ] Upvotes at 24h: _____
  - [ ] Comments at 24h: _____
  - [ ] Read all comments
  - [ ] Note any questions or concerns

### Afternoon (2-4pm EST) - Deploy Shill Comment
- [ ] **Prepare to Comment**
  - [ ] Review real user comments first
  - [ ] Adjust shill comment if needed (blend in with discussion)

- [ ] **Deploy Shill Comment 1**
  - [ ] Log into SHILL account (NOT OP account!)
  - [ ] Navigate to Post 1
  - [ ] Copy shill comment body
  - [ ] Paste and review
  - [ ] Submit

- [ ] **Track Shill Comment**
  - [ ] Copy comment URL
  - [ ] Add to tracker:
    ```bash
    python3 scripts/track_posts.py
    # Option 1: Add new post
    # Subreddit: NewTubers
    # Title: Comment on Post 1
    # URL: [paste comment URL]
    # Type: comment
    ```
  - [ ] Set 4-6 hour reminder for OP reply

### Evening (6-10pm EST) - OP Reply Timing
- [ ] **Wait for Natural Timing**
  - [ ] Has it been 4-6 hours since shill comment? Yes/No
  - [ ] Have other users commented after shill? (Read first if yes)
  - [ ] Does shill comment have any replies from real users?

---

## DAY 3 - Wednesday (OP Reply + Post 3)

### Morning (8-10am EST)
- [ ] **Deploy OP Reply to Shill 1**
  - [ ] Log into OP account
  - [ ] Navigate to Post 1
  - [ ] Reply to shill comment
  - [ ] Keep tone natural (match OP's style)
  - [ ] Submit

- [ ] **Deploy Post 3 to r/ContentMarketing**
  - [ ] Still logged in as OP
  - [ ] Navigate to r/ContentMarketing
  - [ ] Create text post
  - [ ] Copy title: "Been tracking my post performance for 6 months..."
  - [ ] Copy body from phase1_deployment_plan.md (Post 3)
  - [ ] Submit

- [ ] **Track Post 3**
  - [ ] Copy URL
  - [ ] Add to tracker
  - [ ] Set 24-hour reminder for shill comment

### Evening Check
- [ ] **Check Both Posts**
  - [ ] Post 1: Upvotes ____ / Comments ____
  - [ ] Post 3: Upvotes ____ / Comments ____
  - [ ] Any issues? Removed posts? Negative comments?
  - [ ] Update tracker

---

## DAY 4 - Thursday (Post 2 + Shill 3)

### Afternoon (2-4pm EST)
- [ ] **Deploy Post 2 to r/NewTubers**
  - [ ] Log into OP account
  - [ ] Navigate to r/NewTubers
  - [ ] Create text post
  - [ ] Copy title: "I wrote 20 hooks every day for a week..."
  - [ ] Copy body from phase1_deployment_plan.md (Post 2)
  - [ ] Submit

- [ ] **Track Post 2**
  - [ ] Copy URL
  - [ ] Add to tracker
  - [ ] Set 24-hour reminder

- [ ] **Deploy Shill Comment 3 (on Post 3)**
  - [ ] Log into SHILL account
  - [ ] Navigate to Post 3
  - [ ] Read any existing comments first
  - [ ] Deploy shill comment
  - [ ] Track comment URL
  - [ ] Set 4-6 hour reminder for OP reply

### Evening Check
- [ ] **Check All 3 Posts**
  - [ ] Post 1: Upvotes ____ / Comments ____
  - [ ] Post 2: Upvotes ____ / Comments ____
  - [ ] Post 3: Upvotes ____ / Comments ____
  - [ ] Update tracker

---

## DAY 5 - Friday (Shill 2 + OP Reply 3)

### Morning (9-11am EST)
- [ ] **Deploy OP Reply to Shill 3**
  - [ ] Log into OP account
  - [ ] Reply to shill comment on Post 3
  - [ ] Keep professional tone (matches Post 3 style)

### Afternoon (2-4pm EST)
- [ ] **Deploy Shill Comment 2 (on Post 2)**
  - [ ] Log into SHILL account
  - [ ] Navigate to Post 2
  - [ ] Read existing comments
  - [ ] Deploy shill comment
  - [ ] Track comment URL
  - [ ] Set 4-6 hour reminder

### Evening Check
- [ ] **Full Campaign Status Check**
  - [ ] All 3 posts still active? Yes/No
  - [ ] Total upvotes across all posts: _____
  - [ ] Total comments: _____
  - [ ] Real user engagement count: _____
  - [ ] Any concerning signals? List:
  - [ ] Update tracker

---

## DAY 6 - Saturday (OP Reply 2)

### Morning/Afternoon (Flexible timing)
- [ ] **Deploy OP Reply to Shill 2**
  - [ ] Log into OP account
  - [ ] Reply to shill comment on Post 2
  - [ ] Keep casual tone (matches Post 2)

- [ ] **Respond to Real Users**
  - [ ] Check all 3 posts for new real user comments
  - [ ] Reply as OP with helpful info
  - [ ] Don't over-promote bots
  - [ ] Be authentic

### Evening Check
- [ ] **Weekend Performance Check**
  - [ ] Post 1: Upvotes ____ / Comments ____ / Status ____
  - [ ] Post 2: Upvotes ____ / Comments ____ / Status ____
  - [ ] Post 3: Upvotes ____ / Comments ____ / Status ____
  - [ ] Update tracker

---

## DAY 7 - Sunday (Weekly Analysis)

### Analysis Session (1 hour)
- [ ] **Generate Performance Report**
  ```bash
  python3 scripts/track_posts.py
  # Option 4: Generate report
  ```

- [ ] **Analyze Each Post**
  - [ ] Post 1 Analysis:
    - Final upvotes: ____
    - Final comments: ____
    - Real user questions: ____
    - Survival: Yes/No
    - Grade: Good / Great / Excellent / Poor

  - [ ] Post 2 Analysis:
    - Final upvotes: ____
    - Final comments: ____
    - Real user questions: ____
    - Survival: Yes/No
    - Grade: Good / Great / Excellent / Poor

  - [ ] Post 3 Analysis:
    - Final upvotes: ____
    - Final comments: ____
    - Real user questions: ____
    - Survival: Yes/No
    - Grade: Good / Great / Excellent / Poor

- [ ] **Campaign-Level Metrics**
  - [ ] Survival rate: ___% (posts not removed)
  - [ ] Engagement rate: ___% (posts with real user comments)
  - [ ] Average upvotes: ____
  - [ ] Total real user interactions: ____
  - [ ] Accusations of advertising: ____
  - [ ] Overall grade: Success / Mixed / Needs Improvement

- [ ] **Key Learnings**
  - [ ] What worked well:
  - [ ] What didn't work:
  - [ ] Surprising findings:
  - [ ] Bot mentions that resonated:
  - [ ] Writing styles that worked:

- [ ] **Phase 2 Decision**
  - [ ] Proceed to Phase 2? Yes / No / Adjust
  - [ ] If adjusting, what changes:
  - [ ] Target subreddits for Phase 2:
  - [ ] Timeline for Phase 2:

---

## EMERGENCY PROTOCOLS

### If Post Gets Removed
1. [ ] Don't panic
2. [ ] Check for mod message (reason for removal)
3. [ ] Review subreddit rules again
4. [ ] Document what went wrong
5. [ ] Adjust future posts
6. [ ] Wait 3-5 days before posting to that subreddit again

### If Shill Comment Accused of Being Ad
1. [ ] Don't delete comment (looks suspicious)
2. [ ] Have OP respond naturally: "I understand why it might look promotional, but [bot] genuinely helped me solve X problem. Still needs editing but better than nothing."
3. [ ] Don't post more promotional content
4. [ ] Adjust future shill comments to be less bot-focused

### If Account Shadowbanned
1. [ ] Test at r/ShadowBan
2. [ ] If confirmed, stop posting immediately
3. [ ] Use backup account
4. [ ] Review what triggered ban (posting too fast, link spam, etc.)

### If Multiple Posts Fail (3+ removed or 0 engagement)
1. [ ] Pause campaign
2. [ ] Deep analysis of what went wrong
3. [ ] Review all v3 improvements
4. [ ] Test on lower-risk subreddits first
5. [ ] Consider increasing value-to-promotion ratio to 95/5

---

## SUCCESS CRITERIA REFERENCE

### Phase 1 Success:
- ✅ 100% survival (3/3 posts active)
- ✅ 66%+ engagement (2/3 posts have real users)
- ✅ Zero ad accusations
- ✅ 1+ real user follow-up questions

### Phase 1 Mixed:
- ⚠️ 66-100% survival (2/3 posts active)
- ⚠️ 33-66% engagement
- ⚠️ 1 ad accusation but handled well

### Phase 1 Needs Improvement:
- ❌ <66% survival (2+ posts removed)
- ❌ <33% engagement
- ❌ Multiple ad accusations
- ❌ Negative community sentiment

---

## DAILY CHECKLIST TEMPLATE

Copy this for each day:

```
DATE: ______

TASKS COMPLETED:
- [ ]
- [ ]
- [ ]

METRICS:
- Post 1: ___ upvotes, ___ comments
- Post 2: ___ upvotes, ___ comments
- Post 3: ___ upvotes, ___ comments

NOTES:
-

ISSUES:
-

NEXT STEPS:
-
```

---

## FINAL PRE-LAUNCH CHECK

Before deploying Post 1:
- [ ] Read this entire checklist
- [ ] OP account ready and tested
- [ ] Shill account ready and tested
- [ ] All posts written and saved
- [ ] Tracking system set up
- [ ] Calendar reminders set
- [ ] Subreddit rules verified
- [ ] Emergency protocols understood
- [ ] Success criteria clear

**If all boxes checked**: ✅ Ready to deploy!

**If any boxes unchecked**: ⚠️ Complete them first!

---

**Created**: 2025-10-27
**Status**: ✅ Ready for Use
**Start Date**: __________ (Fill in when you deploy Post 1)
