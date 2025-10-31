# Content Maker Toolkit - Structured Database (AI-Optimized)
**Last Updated**: 2025-10-23
**Purpose**: AI-readable structured data for Reddit GTM strategy targeting content creators/influencers

---

## Taxonomy

### Creation Stage Classification
1. **Research Stage (调研阶段)**: Competitor analysis, trend monitoring
2. **Topic Selection Stage (选题阶段)**: Idea generation, trend-based topics
3. **Content Production Stage (内容制作阶段)**: Text generation, image generation, video generation
4. **Content Repurposing Stage (内容再利用)**: Cross-platform adaptation, format transformation

### Platform Classification
- **YouTube**: Long-form video platform
- **X (Twitter)**: Short-form text + image platform
- **Instagram**: Image + short video platform
- **TikTok**: Short vertical video platform
- **LinkedIn**: Professional network, long-form text
- **Universal (通用)**: Cross-platform tools

### Function Classification
- **Page Analysis (页面分析)**: Scrape & analyze competitor channels
- **Search & Summarization (搜索总结)**: Trend monitoring, topic discovery
- **Text Rewriting (文案改写)**: Cross-platform content adaptation
- **Image Generation (生图)**: Thumbnail, meme, carousel creation
- **Text Generation (生文案)**: Titles, descriptions, posts, hooks
- **Video Generation (生视频)**: B-roll creation
- **Video Processing (视频处理)**: Editing, clipping
- **Video-to-Text (视频转文字)**: Transcription, summarization

---

## Bot Inventory (25 Bots)

### Category 1: Research Stage (4 bots)

#### Bot 1.1: YouTube Rival Analyzer Bot
**Function**: Analyze 1+ competitor YouTube channels → extract top-performing videos, keywords, thumbnail styles, title patterns
**Platform**: YouTube
**Function Type**: Page Analysis
**Status**: Not Built
**Competitor Reference**: https://vidiq.com/features/competitors/
**Use Case**: "Before creating YouTube content, analyze what's working for competitors"

#### Bot 1.2: X Rival Analyzer Bot ✅
**Function**: Analyze 1+ competitor X accounts → extract top posts, keywords, copywriting style, content patterns
**Platform**: X (Twitter)
**Function Type**: Page Analysis
**Status**: **BUILT** - @X_Rival_Analysis_bot
**Bot Link**: https://t.me/X_Rival_Analysis_bot
**Competitor Reference**: https://www.rivaliq.com/free-social-media-analytics/twitter-head-to-head/
**Use Case**: "Discover what X content is driving engagement for competitors"

#### Bot 1.3: Instagram Rival Analyzer Bot
**Function**: Analyze 1+ competitor Instagram accounts → extract top posts, keywords, image/video style, content patterns
**Platform**: Instagram
**Function Type**: Page Analysis
**Status**: Not Built
**Competitor Reference**: https://www.rivaliq.com/free-social-media-analytics/instagram-head-to-head/
**Use Case**: "Understand visual trends and hashtag strategies from Instagram competitors"

#### Bot 1.4: TikTok Rival Analyzer Bot
**Function**: Analyze 1+ competitor TikTok accounts → extract top posts, keywords, video style, content patterns
**Platform**: LinkedIn (NOTE: CSV shows "LinkedIn" but description says TikTok - likely error)
**Function Type**: Page Analysis
**Status**: Not Built
**Competitor Reference**: https://www.rivaliq.com/free-social-media-analytics/tiktok-head-to-head/
**Use Case**: "Identify viral TikTok formats and trending audio from competitors"

---

### Category 2: Topic Selection Stage (2 bots)

#### Bot 2.1: Viral Idea Spark Bot ✅
**Function**: Input niche (e.g., "AI", "food") → monitor & push trending topics/challenges from TikTok, X, Instagram
**Platform**: Universal
**Function Type**: Search & Summarization
**Status**: **BUILT** - @Viral_Idea_Spark_Bot
**Bot Link**: https://t.me/Viral_Idea_Spark_Bot
**Competitor Reference**: https://trendspark.live/
**Use Case**: "Stay updated on trending topics in your niche for timely content creation"

#### Bot 2.2: Topic Generator Bot ✅
**Function**: Input niche/keyword → scrape social media hot discussions & search trends → generate 10-20 topic suggestions with reference links
**Platform**: Universal
**Function Type**: Search & Summarization
**Status**: **BUILT** - @Topic_generator8_bot
**Bot Link**: https://t.me/Topic_generator8_bot
**Competitor Reference**: https://www.hootsuite.com/social-media-tools/content-ideas-generator
**Use Case**: "Generate data-driven topic ideas based on what audiences are actively discussing"

---

### Category 3: Content Production Stage (11 bots)

#### Bot 3.1: Content Summarizer Bot
**Function**: Input long video/article link → summarize key points → convert to X-optimized short copy
**Platform**: Universal
**Function Type**: Text Rewriting, Video-to-Text
**Status**: Not Built
**Competitor Reference**: https://www.reddit.com/r/n8n/comments/1luu4iq/i_built_an_n8n_workflow_to_convert_web_articles/
**Use Case**: "Quickly turn long-form research into social media posts"

#### Bot 3.2: YouTube Thumbnail Bot ✅
**Function**: Input caption OR upload image + caption → generate viral YouTube thumbnail
**Platform**: YouTube
**Function Type**: Image Generation
**Status**: **BUILT** - @myshell_thumbmaker_bot
**Bot Link**: https://t.me/myshell_thumbmaker_bot
**Competitor Reference**: https://pikzels.com/
**Use Case**: "Create eye-catching thumbnails without design skills"

#### Bot 3.3: Vertical Thumbnail Generator Bot ✅
**Function**: Mode 1: Text/image + description → generate vertical thumbnail | Mode 2: Upload horizontal thumbnail → auto-crop to vertical
**Platform**: TikTok
**Function Type**: Image Generation
**Status**: **BUILT** - @myshell_vertical_thumbnail_bot
**Bot Link**: https://t.me/myshell_vertical_thumbnail_bot
**Competitor Reference**: https://pikzels.com/
**Use Case**: "Adapt YouTube thumbnails for TikTok/Shorts/Reels"

#### Bot 3.4: YouTube Clickbait Title Generator Bot ✅
**Function**: Input keyword/video script → generate 10 viral YouTube titles following platform best practices
**Platform**: YouTube
**Function Type**: Text Generation
**Status**: **BUILT** - @youtube_clickbait_title_bot
**Bot Link**: https://t.me/youtube_clickbait_title_bot
**Competitor Reference**: https://www.hootsuite.com/social-media-tools/ai-caption-generator-social-media
**Use Case**: "Generate click-worthy titles optimized for YouTube algorithm"

#### Bot 3.5: YouTube Video Description Generator Bot ✅
**Function**: Input keyword/video script → generate professional YouTube description with keywords, timestamps, CTA
**Platform**: YouTube
**Function Type**: Text Generation
**Status**: **BUILT** - @YouTube_Video_Text_Bot
**Bot Link**: https://t.me/YouTube_Video_Text_Bot
**Competitor Reference**: https://vidiq.com/ai-description-generator/
**Use Case**: "Create SEO-optimized video descriptions that improve discoverability"

#### Bot 3.6: X Hook Generator Bot ✅
**Function**: Input core idea/topic → generate 10 viral X post hooks based on psychological triggers
**Platform**: X (Twitter)
**Function Type**: Text Generation
**Status**: **BUILT** - @Hook_Generator_Bot, @Aillen_XHook_bot
**Bot Links**: https://t.me/Hook_Generator_Bot, https://t.me/Aillen_XHook_bot
**Competitor Reference**: https://www.copy.ai/tools/hook-generator
**Use Case**: "Write attention-grabbing first lines for X threads"

#### Bot 3.7: X Post Generator Bot ✅
**Function**: Provide 5 reference X posts (style examples) → input topic → generate 3-5 posts in learned style
**Platform**: X (Twitter)
**Function Type**: Text Generation
**Status**: **BUILT** - @xPostGenerator_Bot
**Bot Link**: https://t.me/xPostGenerator_Bot
**Competitor Reference**: https://predis.ai/social-media-post-generator/
**Use Case**: "Maintain consistent brand voice across X posts"

#### Bot 3.8: LinkedIn Post Generator Bot ✅
**Function**: Provide 5 reference LinkedIn posts (style examples) → input topic → generate 3-5 posts in learned style
**Platform**: LinkedIn
**Function Type**: Text Generation
**Status**: **BUILT** - @CFLinkedinPostBot
**Bot Link**: https://t.me/CFLinkedinPostBot
**Competitor Reference**: https://predis.ai/social-media-post-generator/
**Use Case**: "Generate professional LinkedIn content matching your voice"

#### Bot 3.9: Carousel Post Bot
**Function**: Input text/article + select template & brand colors → generate multi-page carousel with unified visual style
**Platform**: Instagram, LinkedIn
**Function Type**: Image Generation
**Status**: Not Built
**Competitor Reference**: https://postnitro.ai/zh
**Use Case**: "Create swipeable educational content for Instagram/LinkedIn"

#### Bot 3.10: Meme Generator Bot ✅
**Function**: Input idea/keyword → match trending meme templates → generate meme image
**Platform**: Universal
**Function Type**: Image Generation
**Status**: **BUILT** - @CfMemeBot
**Bot Link**: https://t.me/CfMemeBot
**Competitor Reference**: https://supermeme.ai/
**Use Case**: "Create engaging memes for social media engagement"

#### Bot 3.11: B-Roll Generator Bot ✅
**Function**: Mode 1: Input text description → generate B-roll footage | Mode 2: Upload video → auto-identify B-roll needs → generate footage
**Platform**: YouTube
**Function Type**: Video Generation
**Status**: **BUILT** - @BRoll_Generator_Bot
**Bot Link**: https://t.me/BRoll_Generator_Bot
**Competitor Reference**: https://www.kapwing.com/ai/b-roll-generator
**Use Case**: "Generate supplementary video footage without stock footage subscriptions"

---

### Category 4: Content Repurposing Stage (4 bots)

#### Bot 4.1: X to LinkedIn Post Transformer Bot
**Function**: Input X post → extract core idea → rewrite for LinkedIn audience (longer, professional tone)
**Platform**: X, LinkedIn
**Function Type**: Text Rewriting
**Status**: Not Built
**Competitor Reference**: https://reepl.io/free-tools/linkedin-post-twitter-threads
**Use Case**: "Expand X threads into LinkedIn thought leadership posts"

#### Bot 4.2: X to Video Script Transformer Bot ✅
**Function**: Input X post → extract core idea → rewrite as TikTok/Reels short-video script
**Platform**: X, TikTok
**Function Type**: Text Rewriting
**Status**: **BUILT** - @XtoVideoScriptTransformer_Bot
**Bot Link**: https://t.me/XtoVideoScriptTransformer_Bot
**Competitor Reference**: https://reepl.io/free-tools/linkedin-post-twitter-threads
**Use Case**: "Turn written content into video scripts for short-form platforms"

#### Bot 4.3: Content Repurposing Bot - Long Video to Short Video
**Function**: Upload long video (YouTube) → auto-detect "golden quotes" or highlights → clip into multiple TikTok/Shorts/Reels with auto-subtitles
**Platform**: TikTok, YouTube
**Function Type**: Video Processing
**Status**: Not Built
**Competitor Reference**: https://www.reddit.com/r/n8n/comments/1k4njod/how_i_automated_repurposing_youtube_videos_to/
**Use Case**: "Maximize ROI from long-form video by creating short clips"

#### Bot 4.4: Content Repurposing Bot - Video to Copy ✅
**Function**: Upload video → convert core ideas to X short copy OR LinkedIn long copy (user selects)
**Platform**: X, LinkedIn, YouTube
**Function Type**: Video-to-Text
**Status**: **BUILT** - @CRBVideotoCopy_bot
**Bot Link**: https://t.me/CRBVideotocopy_bot
**Competitor Reference**: https://www.reddit.com/r/n8n/comments/1lvlb8n/i_built_a_content_repurposing_system_that_turns/
**Use Case**: "Repurpose video content into text posts without manual transcription"

#### Bot 4.5: Content Repurposing Bot - Long Copy to Short Copy
**Function**: Upload blog/video script → auto-split into 10 X-ready tweets
**Platform**: X (Twitter)
**Function Type**: Text Rewriting, Video-to-Text
**Status**: Not Built
**Use Case**: "Break down long-form content into bite-sized social posts"

---

## Built vs. Not Built Status

### Currently Built (16/25 = 64%)
1. ✅ X Rival Analyzer Bot
2. ✅ Viral Idea Spark Bot
3. ✅ Topic Generator Bot
4. ✅ YouTube Thumbnail Bot
5. ✅ Vertical Thumbnail Generator Bot
6. ✅ YouTube Clickbait Title Generator Bot
7. ✅ YouTube Video Description Generator Bot
8. ✅ X Hook Generator Bot (2 versions)
9. ✅ X Post Generator Bot
10. ✅ LinkedIn Post Generator Bot
11. ✅ Meme Generator Bot
12. ✅ B-Roll Generator Bot
13. ✅ X to Video Script Transformer Bot
14. ✅ Content Repurposing Bot - Video to Copy

### Not Yet Built (9/25 = 36%)
1. ❌ YouTube Rival Analyzer Bot
2. ❌ Instagram Rival Analyzer Bot
3. ❌ TikTok Rival Analyzer Bot
4. ❌ Content Summarizer Bot
5. ❌ Carousel Post Bot
6. ❌ X to LinkedIn Post Transformer Bot
7. ❌ Content Repurposing Bot - Long Video to Short Video
8. ❌ Content Repurposing Bot - Long Copy to Short Copy

---

## GTM Strategy Implications

### Remixability Angle
**Core Message**: "These bots were all built with one sentence in Shell Agent. You can remix any of them to fit your exact workflow."

### Pain Point → Bot Mapping

**Pain Point 1**: "I don't know what content to create"
- **Bots**: Viral Idea Spark Bot, Topic Generator Bot, X/YouTube/Instagram/TikTok Rival Analyzer Bots
- **Reddit Angle**: "I used to spend hours scrolling for content ideas. Now my Telegram bot monitors trends for me."

**Pain Point 2**: "Content creation takes too long"
- **Bots**: YouTube Thumbnail Bot, X Hook Generator, Meme Generator, B-Roll Generator
- **Reddit Angle**: "I cut my thumbnail creation from 30 min to 30 seconds with this Telegram bot."

**Pain Point 3**: "I need to post on multiple platforms but don't have time to rewrite"
- **Bots**: X to LinkedIn Transformer, X to Video Script Transformer, Video to Copy Bot
- **Reddit Angle**: "I repurpose one YouTube video into 10 X posts + 3 LinkedIn articles automatically."

**Pain Point 4**: "I want to match competitor performance but don't know their strategy"
- **Bots**: All Rival Analyzer bots
- **Reddit Angle**: "I analyzed my top 3 YouTube competitors in 5 minutes. Here's what I learned."

### Platform-Specific Messaging

**For YouTube Creators:**
- "Thumbnail + Title + Description generation in <2 minutes"
- "Analyze competitors' viral video patterns without manual tracking"
- "Turn long videos into TikTok clips automatically"

**For X/Twitter Creators:**
- "Generate 10 viral hooks in 30 seconds"
- "Maintain consistent voice across 100+ posts/month"
- "Repurpose X content into video scripts & LinkedIn posts"

**For Multi-Platform Influencers:**
- "One video → 10 X posts + 3 LinkedIn articles + 5 TikTok clips"
- "Unified workflow in Telegram - no switching between 5 different tools"

---

## Competitive Positioning

### vs. Existing Tools
| Competitor | Limitation | Shell Agent Advantage |
|------------|-----------|----------------------|
| VidIQ, TubeBuddy | YouTube-only, subscription | Multi-platform, one-time build |
| Hootsuite, Buffer | Scheduling focus, no content generation | Full creation workflow |
| Predis.ai, Copy.ai | Web-based, context-switching | Telegram-native, chat interface |
| n8n workflows | Requires technical setup | Natural language creation |

### Unique Value Props
1. **Telegram-Native**: No app switching, all bots in one chat
2. **One-Sentence Creation**: Describe bot in plain English, get working bot in 10 min
3. **Remixable**: Every bot is customizable via natural language editing
4. **Cross-Platform**: Covers YouTube, X, TikTok, Instagram, LinkedIn in one ecosystem

---

## Reddit Post Angle Prioritization

### Angle 1 (Highest Conversion): "I Built X Bot" - Personal Story
**Template**: "I was spending [time] on [task], so I built a Telegram bot to do it in [shorter time]. Here's how."
**Example**: "I was spending 2 hours/day finding content ideas. Built a Telegram bot that monitors TikTok trends for me. Now it takes 5 minutes."
**Why It Works**: Personal pain → solution → specific time saved = relatable + credible

### Angle 2 (High Engagement): "X Bots I Use Daily as a [Platform] Creator"
**Template**: "Here are the 5 Telegram bots that save me [X hours/week] as a [YouTube/TikTok/X] creator."
**Example**: "5 Telegram bots that save me 10 hours/week as a YouTube creator: Thumbnail gen, Title gen, Description gen, B-roll gen, Competitor analyzer."
**Why It Works**: List format + time quantification + platform-specific = actionable

### Angle 3 (Moderate Conversion): "How I Automated [Workflow]"
**Template**: "How I automated my [platform] content workflow with Telegram bots (and you can too)."
**Example**: "How I automated my YouTube → TikTok repurposing workflow: One video → 10 TikTok clips with auto-subtitles."
**Why It Works**: Workflow-focused = appeals to efficiency-minded creators

### Angle 4 (Brand Awareness): "Competitor Analysis Results"
**Template**: "I analyzed [number] top [platform] creators. Here's what they all do."
**Example**: "I analyzed 10 top YouTube tech channels. They all use these 3 thumbnail patterns."
**Why It Works**: Data-driven insights = high value, builds authority

---

## Next Steps for Reddit Research

### Target Subreddit Criteria (Content Creator Vertical)
1. **Primary Audience**: Content creators, influencers, social media managers
2. **Platform Focus**: YouTube, TikTok, X, Instagram, LinkedIn creators
3. **Pain Point Alignment**: Content ideation, production speed, multi-platform management
4. **Self-Promo Tolerance**: Medium to high (creator communities often allow tool sharing)
5. **Engagement Level**: 50+ upvotes on hot threads = active community

### Research Questions to Answer
1. Which subreddits have the most active content creator discussions?
2. Which platforms (YouTube/TikTok/X) dominate each subreddit?
3. What content formats perform best (lists, stories, data)?
4. Are competitor analysis/tool recommendation posts welcome?
5. What's the remix messaging angle (one-sentence bot creation) reception?

### Post Angle Testing Priority
1. **Test First**: "I built X bot" personal story (lowest friction)
2. **Test Second**: "X bots I use" list format (high engagement)
3. **Test Last**: "Competitor analysis" data posts (builds authority)
