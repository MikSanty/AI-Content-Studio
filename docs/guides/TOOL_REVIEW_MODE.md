# Tool Review Mode Guide

**Complete guide to using AI-Content-Studio for generating professional, story-driven tool reviews**

---

## Table of Contents

1. [What is Tool Review Mode?](#what-is-tool-review-mode)
2. [When to Use It](#when-to-use-it)
3. [Key Differences from Article Mode](#key-differences-from-article-mode)
4. [Quick Start](#quick-start)
5. [Step-by-Step Workflow](#step-by-step-workflow)
6. [Template Reference](#template-reference)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## What is Tool Review Mode?

Tool Review Mode is a specialized content generation workflow designed specifically for creating **personable, story-driven, evidence-backed software/tool reviews** that are optimized for both human readers and LLM comprehension.

It follows a specific template structure inspired by professional tech review sites and includes:

- ✅ First-person narrative voice
- ✅ 6-10 real user quotes from review sites
- ✅ Detailed pricing breakdowns with scaling information
- ✅ Conditional framing ("If you're X... if you're Y...")
- ✅ Honest pros, cons, and fit analysis
- ✅ Product-aware details (migration paths, implementation steps)
- ✅ Strict format requirements (no em dashes, clean headers, sources appendix)

---

## When to Use It

**Use Tool Review Mode when you're writing:**
- SaaS tool reviews
- Software comparisons
- Product evaluations
- "Is [Tool] Worth It?" articles
- "[Tool] Review for [Audience]" content

**Use General Article Mode when you're writing:**
- How-to guides
- Industry analyses
- Thought leadership pieces
- General blog content
- Educational articles

---

## Key Differences from Article Mode

| Feature | Article Mode | Tool Review Mode |
|---------|--------------|------------------|
| **Voice** | Professional, flexible | First-person, story-driven |
| **Evidence** | Optional citations | Required 6-10 quotes |
| **Structure** | Flexible template | Fixed review sections |
| **Pricing** | Not required | Detailed breakdown required |
| **Format Rules** | Standard | Strict (no em dashes, etc.) |
| **Audience** | General | Defined in pre-flight questions |
| **Templates** | `manual.md`, `template.md` | `tool_review_brief.md`, `tool_review_structure.md` |
| **Rules** | `llmon_rules.md`, `editor_rules.md` | `llmon_tool_review_rules.md`, `editor_tool_review_rules.md` |

---

## Quick Start

### 1. Set Content Mode

**Option A: Set in .env file**
```env
CONTENT_MODE=tool_review
```

**Option B: Let the system auto-detect**
- The system will detect tool review mode if you use `templates/tool_review_brief.md`

### 2. Fill Out the Tool Review Brief

Copy and edit `templates/tool_review_brief.md`:

**Required sections:**
1. **Pre-Writing Interview Questions** (4 questions about title, audience, motivation, benefit)
2. **Tool Information** (name, category, pricing overview)
3. **Collected Quotes** (6-10 quotes with exact URLs)
4. **Product-Specific Details** (pricing breakdown, migration paths, implementation)
5. **Review Hub Ratings** (G2, Capterra, etc.)

See `examples/example_tool_review_brief.md` for a complete example.

### 3. Run the Workflow

```bash
python main.py
```

The system will automatically use tool review templates and rules.

---

## Step-by-Step Workflow

### Phase 1: Research & Quote Collection

**Before writing**, gather your evidence:

1. **Visit review sites:**
   - G2.com
   - Capterra.com
   - Reddit (r/SaaS, r/entrepreneur, tool-specific subreddits)
   - Trustpilot.com
   - Product Hunt
   - Tech blogs (TechCrunch, The Verge, etc.)

2. **Collect 6-10 diverse quotes:**
   - Different perspectives (beginners vs experts)
   - Different use cases (solo vs team)
   - Mix of positive and critical feedback
   - Recent quotes (2024-2025)
   - Deduplicate overlapping sentiments

3. **Document each quote in the brief:**
   ```markdown
   ### Quote 1
   **Quote:**
   "[Exact quote text]"
   
   **Source Name:**
   [e.g., Sarah M., Marketing Manager via G2]
   
   **Source URL:**
   https://www.g2.com/...
   
   **Date:**
   [Month Year, e.g., January 2025]
   ```

**💡 Tip:** Use browser extensions like "Copy as Markdown" to quickly copy quotes.

### Phase 2: Answer Pre-Writing Questions

Fill out the 4 critical questions in `tool_review_brief.md`:

**1. Article Title**
- Be specific: "Surfer SEO Review: Is It Worth $99/Month in 2025?"
- Include target year and key decision point
- Infer your angle from the title

**2. Target Audience**
- Be specific about role, stage, and context
- Example: "Solo SaaS founders launching their first product" (not just "founders")

**3. Reader Motivation**
- What problem are they solving?
- What decision are they making?
- Why now?

**4. Reader Benefit**
- What concrete outcome will they get?
- What questions will be answered?
- What can they do after reading?

### Phase 3: Gather Product Details

**Pricing Breakdown:**
- Get exact numbers (not "starts around $X")
- Document all tiers (free + 2-3 paid)
- Explain scaling model (by seats? projects? traffic?)
- Show cost evolution at different scales

**Migration Information:**
- How to switch TO this tool (from competitors)
- How to switch FROM this tool (exit path)
- Data portability
- Timeline and friction points

**Implementation Steps:**
- Realistic setup process (3-7 steps)
- Typical time investment
- Integration requirements
- Team onboarding considerations

**Review Hub Ratings:**
- G2 rating + review count
- Capterra rating + review count
- Product Hunt upvotes (if relevant)
- Trustpilot (if relevant)

### Phase 4: Run the Workflow

```bash
python main.py
```

**What happens:**

1. **WRITER Agent** generates outline or draft
   - Uses `tool_review_structure.md` template
   - Applies `tool_review_writer_prompt.md` instructions
   - Integrates your collected quotes
   - Creates first-person narrative

2. **LLMON Agent** creates 3 variations
   - Variation 1: Clear & Accessible
   - Variation 2: Deep & Analytical
   - Variation 3: Engaging & Persuasive
   - Preserves quotes, pricing, and story elements

3. **EDITOR Agent** polishes with format validation
   - Pass 1: Format compliance (em dashes, headers, dividers)
   - Pass 2: Factual accuracy check
   - Pass 3: Grammar, clarity & flow
   - Pass 4: Final consistency & polish

### Phase 5: Review & Refine

**Check the output for:**

- [ ] Story-driven narrative present
- [ ] 6-10 quotes integrated naturally
- [ ] All quotes appear in Sources appendix
- [ ] Conditional framing used (2-4 callouts)
- [ ] First-person voice maintained
- [ ] No em dashes (—)
- [ ] No parenthetical text in headers
- [ ] No divider lines
- [ ] Pricing details complete
- [ ] 900-1,400 words (soft range)
- [ ] All required sections present

**If something needs adjustment:**
- Use the revision loops at each stage
- Provide specific feedback
- The system learns your preferences over time (if Workflow Memory enabled)

---

## Template Reference

### Tool Review Brief Structure

```markdown
# Tool Review Content Brief

## Pre-Writing Interview Questions
1. Article Title
2. Target Audience
3. Reader Motivation
4. Reader Benefit

## Tool Information
- Tool Name
- Category
- Best For
- Ease of Use
- Pricing Overview

## Collected Quotes & Evidence (6-10 required)
Quote 1-10 with source names, URLs, dates

## Product-Specific Details
- Pricing Breakdown (all tiers)
- Migration Path (in and out)
- Implementation Details (setup steps)
- Templates & Integrations (optional)
- Compliance & Trust (optional)

## Review Hub Ratings
- G2
- Capterra
- Product Hunt (optional)
- Trustpilot (optional)

## Additional Context & Notes
- Personal Experience
- Comparative Notes
- Key Differentiators
```

### Required Review Sections

1. **[Tool Name]** - With metadata
2. **What is [Tool]?** - Natural query answer
3. **How [Tool] Works** - Copyable workflow
4. **How I Use [Tool]** - Personal narrative
5. **Why It Matters** - "So you can..." outcomes
6. **AI Features** - Optional, only if tool has AI
7. **Who Should Use [Tool]?** - Conditional framing
8. **Pricing Plans** - Detailed breakdown
9. **Pros** - 4-6 strengths as outcomes
10. **Cons** - 3-5 honest limitations
11. **Caveats** - Optional, hidden costs
12. **Ratings & Reviews** - G2, Capterra, etc.
13. **Sources** - Appendix with all quote URLs

---

## Best Practices

### Quote Collection

**✅ DO:**
- Collect from multiple sources (G2, Reddit, Capterra, blogs)
- Get recent quotes (2024-2025)
- Include diverse perspectives
- Copy exact text (don't paraphrase)
- Save complete URLs
- Deduplicate similar sentiments

**❌ DON'T:**
- Use marketing copy as "quotes"
- Include testimonials from the vendor's website
- Paraphrase or modify quote text
- Use quotes without URLs
- Repeat the same sentiment across multiple quotes

### Writing Personal Narrative

**✅ DO:**
- Use "I've found...", "In my experience..."
- Share actual use cases and outcomes
- Be specific about your setup and workflow
- Tie opinions to concrete results

**❌ DON'T:**
- Invent fake personal stories
- Make claims you can't back up
- Overuse first-person (once per major section max)
- Make it about you instead of the reader

### Conditional Framing

**✅ DO:**
- "If you're a solo founder, you'll get X; if you're post-PMF, you'll want Y"
- "Better than [Alt] for speed; weaker than [Alt] for analytics"
- "This is not for you if you need HIPAA compliance"

**❌ DON'T:**
- "This tool is great for everyone"
- "It's the best in the market"
- Avoid mentioning limitations

### Pricing Analysis

**✅ DO:**
- Show exact numbers: "$99/month" not "around $100"
- Explain scaling: "At 50 users, expect $500/month"
- Mention hidden costs or overage charges
- Compare value at different tiers

**❌ DON'T:**
- Be vague: "Starts at around $100"
- Omit important pricing details
- Ignore scaling implications
- Copy marketing speak

---

## Troubleshooting

### Issue: "Tool review brief file is missing"

**Solution:**
- Ensure `templates/tool_review_brief.md` exists
- Copy from `examples/example_tool_review_brief.md` if needed
- Check file name spelling

### Issue: "Failed to generate tool review"

**Solution:**
- Verify all required sections in brief are filled out
- Check that you have 6-10 quotes with URLs
- Ensure pricing details are complete
- Review API key configuration

### Issue: "Quotes not integrating properly"

**Solution:**
- Make sure each quote has exact text, source name, URL, and date
- Check that quote text is between quotation marks in the brief
- Verify URLs are complete (start with https://)

### Issue: "Output has em dashes despite rules"

**Solution:**
- This should be caught in Editor pass 1 (Format Compliance)
- If it persists, provide feedback: "Remove all em dashes and replace with semicolons or periods"
- Check that `ENABLE_MULTIPASS_EDITING` is True in config

### Issue: "Story doesn't feel personal"

**Solution:**
- Fill out "Personal Experience" section in brief with real use case
- In revision feedback, request: "Add more first-person narrative to 'How I Use' section"
- Provide specific anecdote you want included

### Issue: "Pricing section too vague"

**Solution:**
- In the brief, provide exact numbers for each tier
- Specify scaling model (seats, projects, etc.)
- Show small/medium/large usage examples
- Revision feedback: "Make pricing more specific with exact dollar amounts"

### Issue: "Missing required sections"

**Solution:**
- Check `tool_review_structure.md` for required sections
- Ensure brief has all product details filled out
- Some sections are optional (AI Features, Caveats)
- Request in revision: "Add missing [Section Name] section"

---

## Advanced Tips

### Using Workflow Memory

If `ENABLE_WORKFLOW_MEMORY=True`, the system learns your preferences:

- After 2-3 reviews, it adapts to your style
- Remembers what feedback you commonly give
- Reduces iterations over time

### Parallel Processing

If `ENABLE_PARALLEL_VARIATIONS=True`:

- All 3 LLMON variations generate simultaneously
- Saves 60-90 seconds per iteration
- No quality compromise

### Quality Scoring

If `ENABLE_QUALITY_SCORING=True`:

- Get objective metrics for each output
- Readability, SEO, Engagement scores
- Helps identify weak areas before final polish

---

## Example Workflow Timeline

**Total time:** ~30-45 minutes (after research)

- **Research & Quote Collection:** 45-60 minutes (one-time)
- **Fill Out Brief:** 15-20 minutes
- **Generate Outline:** 1-2 minutes
- **Review Outline:** 2-3 minutes
- **Generate Draft:** 2-3 minutes
- **Review Draft:** 5 minutes
- **LLMON Variations:** 2-3 minutes
- **Select Variation:** 3-5 minutes
- **Editor Polish:** 2-3 minutes
- **Final Review:** 5 minutes

**💡 Tip:** The research phase is the most time-consuming. Once you have a good brief, you can generate multiple variations quickly.

---

## Resources

- **Example Brief:** `examples/example_tool_review_brief.md`
- **Example Output:** `examples/example_tool_review_output.md`
- **Structure Template:** `templates/tool_review_structure.md`
- **Writer Prompt:** `templates/tool_review_writer_prompt.md`
- **LLMON Rules:** `rules/llmon_tool_review_rules.md`
- **Editor Rules:** `rules/editor_tool_review_rules.md`

---

## Next Steps

1. Copy `examples/example_tool_review_brief.md` to `templates/tool_review_brief.md`
2. Fill it out with your tool's information
3. Collect 6-10 quotes with URLs
4. Set `CONTENT_MODE=tool_review` in `.env` (or let it auto-detect)
5. Run `python main.py`
6. Review and refine using the interactive workflow

**Questions?** Check the main [README.md](../../README.md) or review the [Quick Start Guide](QUICK_START.md).

---

**Happy reviewing! 🚀**

