# AI-Content-Studio

**An Intelligent Multi-Agent AI Workflow for Professional Content Creation**

Transform a content brief into publication-ready articles through an advanced 3-agent pipeline powered by AI, featuring intelligent quality scoring, adaptive learning, and parallel processing.

---

## 🎯 What is AI-Content-Studio?

A sophisticated content creation system that uses **three specialized AI agents** working in sequence:

1. **WRITER** - Generates structured outlines and initial drafts
2. **LLMON** - Creates 3 distinct stylistic variations (in parallel)
3. **EDITOR** - Applies multi-pass professional polish

### ✨ What Makes It Special?

- 🧠 **Learns from your feedback** - Memory system adapts to your preferences
- 📊 **Objective quality metrics** - Multi-dimensional scoring (readability, SEO, engagement)
- ⚡ **3x faster** - Parallel variation generation
- 🎯 **Intelligent validation** - Ensures variations are truly different
- 🔄 **Iterative refinement** - Approve, revise, or reject at each stage
- 🎨 **Flexible providers** - OpenAI (GPT-4o/GPT-4.1) or Google Gemini

---

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
# Clone or download this repository
cd ai-content-studio

# Install Python packages
pip install -r requirements.txt
```

### 2. Set Up API Access

**Option A: OpenAI (Recommended)**
```bash
# Run interactive setup
python setup_env.py

# Or manually create .env file:
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_WRITER_MODEL=gpt-5-nano
OPENAI_LLMON_MODEL=gpt-4o-mini
OPENAI_EDITOR_MODEL=gpt-4.1-mini
```

**Option B: Google Gemini (Free Tier)**
```bash
AI_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-key-here
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Gemini: https://makersuite.google.com/app/apikey

### 3. Create Your Content Brief

Edit `templates/manual.md`:
```markdown
# Article Topic
How AI is transforming content creation in 2025

# Target Audience
Marketing professionals and content creators

# Key Points
- AI-powered workflows save 10+ hours per week
- Multi-agent systems produce higher quality
- [Add your key points...]
```

### 4. Run the Workflow

```bash
python main.py
```

**That's it!** The system will guide you through each stage with interactive prompts.

---

## 🌟 Key Features

### 🎯 Six Intelligence Enhancements (v1.0+)

<details>
<summary><b>1. Outline Generation Phase</b> - Plan before writing</summary>

- Generate and approve article structure before full draft
- Iterate on outlines faster than full revisions
- Better validation of approach early in process

**Example:**
```
→ OUTLINE GENERATION PHASE
→ Generating article outline...

ARTICLE OUTLINE
# Introduction
- Hook: Latest AI statistics
- Thesis: Multi-agent workflows transform content

## Section 1: Current Challenges
- Time constraints in content creation
- Maintaining quality at scale

[Approve/Revise/Reject]
```
</details>

<details>
<summary><b>2. Parallel Variation Generation</b> - 3x faster processing</summary>

- All 3 LLMON variations generate simultaneously
- **90-180 seconds → 30-60 seconds**
- No quality compromise

</details>

<details>
<summary><b>3. Quality Scoring System</b> - Objective metrics for every output</summary>

Five-dimensional analysis:
- 📖 **Readability** (82/100) - Flesch-Kincaid, grade level, complexity
- 🔍 **SEO** (78/100) - Word count, headings, keyword density
- 💡 **Engagement** (88/100) - Questions, examples, action verbs
- 📋 **Structure** (90/100) - Template matching, completeness
- ✓ **Factual** (85/100) - Citation tracking, reference alignment

**Overall Score: 85/100**
</details>

<details>
<summary><b>4. Workflow Memory</b> - System learns your preferences</summary>

- Tracks all feedback across sessions
- Extracts patterns from approvals/rejections
- Provides historical context to agents
- Reduces iterations over time

</details>

<details>
<summary><b>5. Variation Validation</b> - Ensures true diversity</summary>

- Automatic differentiation checking (TF-IDF cosine similarity)
- Enforces 30% minimum difference threshold
- Auto-regeneration if variations too similar
- Up to 2 retry attempts

**Example Report:**
```
VARIATION DIFFERENTIATION REPORT
Minimum Difference: 45.2%
Average Difference: 52.8%
✓ All variations are sufficiently different!
```
</details>

<details>
<summary><b>6. Multi-Pass Editing</b> - Professional polish</summary>

Four focused editing passes:
1. **Grammar & Mechanics** - Technical correctness (temp: 0.4)
2. **Style & Voice** - Tone consistency (temp: 0.5)
3. **Flow & Transitions** - Readability (temp: 0.5)
4. **Final Consistency** - Validation (temp: 0.4)

Higher quality than single-pass editing.
</details>

### 🔧 Multi-Provider Support (v2.0+)

- **OpenAI GPT-4o** - Premium quality (~$0.43/article)
- **OpenAI GPT-4.1** - Next-generation models
- **Google Gemini** - Free tier option
- **Per-agent model configuration** - Mix and match models for cost optimization

### 🎨 Additional Features

- ✅ **Interactive approval gates** at each stage
- ✅ **Dynamic rule editing** for LLMON variations
- ✅ **Session management** - All drafts saved with timestamps
- ✅ **Comprehensive test suite** (23 tests, 100% passing)
- ✅ **Rich documentation** with guides and examples

---

## 📁 Project Structure

```
AI-Content-Studio/
├── 🚀 ENTRY POINTS
│   ├── main.py                      # Main application
│   ├── run.bat / run.sh             # Quick launch scripts
│   └── setup_env.py                 # Interactive API setup
│
├── ⚙️ CORE SYSTEM
│   ├── workflow.py                  # Orchestrator (3-agent pipeline)
│   ├── config.py                    # Configuration & feature flags
│   ├── api_client.py                # Multi-provider API client
│   └── utils.py                     # Helper functions
│
├── 🤖 AI AGENTS
│   └── agents/
│       ├── writer_agent.py          # Stage 1: Draft + Outline
│       ├── llmon_agent.py           # Stage 2: Parallel variations
│       └── editor_agent.py          # Stage 3: Multi-pass polish
│
├── 🧠 INTELLIGENCE MODULES
│   ├── quality_analyzer.py          # Multi-dimensional scoring
│   ├── workflow_memory.py           # Cross-stage learning
│   └── variation_differentiator.py  # Variation validation
│
├── 📝 USER INPUTS (YOU EDIT THESE)
│   ├── templates/
│   │   ├── manual.md                # ⚠️ Your content brief (REQUIRED)
│   │   ├── template.md              # Article structure
│   │   ├── references.md            # Research & data
│   │   └── writer_prompt.md         # Writing instructions
│   └── rules/
│       ├── llmon_rules.md           # Variation styles
│       └── editor_rules.md          # Polish guidelines
│
├── 📚 DOCUMENTATION
│   └── docs/
│       ├── INDEX.md                 # Complete file navigation
│       ├── guides/
│       │   ├── QUICK_START.md       # 5-minute setup guide
│       │   ├── WORKFLOW_DIAGRAM.md  # Visual workflow
│       │   └── ENHANCEMENTS_GUIDE.md # Feature deep-dive
│       ├── setup/
│       │   ├── SETUP.md             # Detailed instructions
│       │   └── OPENAI_SETUP_INSTRUCTIONS.md
│       └── project/
│           ├── PROJECT_SUMMARY.md   # System overview
│           ├── CHANGELOG.md         # Version history
│           └── AGENT_ANALYSIS.md    # Technical analysis
│
├── 💡 EXAMPLES
│   └── examples/
│       ├── example_manual.md        # Sample content brief
│       ├── example_references.md    # Sample references
│       └── template_*.md            # Templates
│
├── 📊 OUTPUTS (AUTO-GENERATED)
│   └── outputs/
│       └── [timestamp]/
│           ├── 01_writer_outline.md
│           ├── 01_writer_draft.md
│           ├── 02_llmon_variation1.md (+ quality scores)
│           ├── 02_llmon_variation2.md
│           ├── 02_llmon_variation3.md
│           ├── 03_editor_polished.md
│           └── FINAL_ARTICLE.md     # ✨ Final output
│
├── 🧪 TESTING
│   ├── test_setup.py                # Setup verification
│   └── test_enhancements.py         # Feature tests (23 tests)
│
├── 💾 MEMORY (AUTO-CREATED)
│   └── memory/                      # Persistent learning data
│
└── 📋 CONFIG
    ├── .env                         # API keys (YOU CREATE THIS)
    ├── requirements.txt             # Dependencies
    └── README.md                    # This file
```

---

## 🔄 The 3-Agent Workflow

### Stage 1: WRITER Agent

**What Happens:**
1. **Outline Phase** - Creates structured outline from your brief
2. **Review** - You approve, revise, or reject the outline
3. **Full Draft** - Generates complete article from approved outline
4. **Quality Score** - Provides multi-dimensional quality metrics

**Your Inputs:**
- `templates/manual.md` - Content brief (**required**)
- `templates/template.md` - Article structure
- `templates/references.md` - Research materials
- `templates/writer_prompt.md` - Writing instructions

**Approval Options:**
- ✓ Approve → Continue to LLMON
- ✎ Revise with feedback → Regenerate with your input
- ✗ Reject → Stop workflow

---

### Stage 2: LLMON Agent

**What Happens:**
1. **Parallel Generation** - Creates 3 distinct variations simultaneously
2. **Differentiation Check** - Validates variations are >30% different
3. **Quality Scoring** - Analyzes each variation
4. **Comparison** - Presents all 3 with differentiation report

**Your Inputs:**
- `rules/llmon_rules.md` - Stylistic transformation rules
- Previous stage approved article

**Approval Options:**
- Select Variation 1/2/3 → Continue to EDITOR
- ↻ Iterate with edited rules → Modify rules, regenerate
- ✗ Reject all → Stop workflow

---

### Stage 3: EDITOR Agent

**What Happens:**
1. **Pass 1: Grammar** - Technical correctness
2. **Pass 2: Style** - Tone and voice consistency
3. **Pass 3: Flow** - Readability and transitions
4. **Pass 4: Consistency** - Final validation
5. **Quality Score** - Final quality assessment

**Your Inputs:**
- `rules/editor_rules.md` - Polish guidelines
- Selected variation from Stage 2

**Approval Options:**
- ✓ Approve as final → Complete! Save to FINAL_ARTICLE.md
- ✎ Request revisions → Provide specific feedback
- ✗ Reject → Stop workflow

---

## 📊 Quality Scoring Explained

Every output receives a comprehensive quality analysis:

```
QUALITY ANALYSIS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Score: 85/100

📖 Readability: 82/100
   • Grade Level: 10 (General Adult)
   • Reading Ease: 65.2 (Standard)
   • Avg Sentence Length: 18.3 words
   • Complex Word %: 12.4%

🔍 SEO: 78/100
   • Word Count: 1,847 ✓
   • Headings: 8 ✓
   • Keyword Density: 2.1% ✓
   • URL-friendly: Yes

💡 Engagement: 88/100
   • Questions: 5
   • Examples: 7
   • Action Verbs: High
   • Emotional Words: Moderate

📋 Structure: 90/100
   • Template Match: 95%
   • Section Completeness: 100%
   • Logical Flow: Excellent

✓ Factual Consistency: 85/100
   • Reference Alignment: High
   • Citation Count: 6
   • Keyword Overlap: 78%
```

---

## ⚙️ Configuration Guide

### Feature Toggles (config.py)

All enhancements enabled by default:

```python
# Enhancement Feature Flags
ENABLE_OUTLINE_PHASE = True           # Outline generation
ENABLE_PARALLEL_VARIATIONS = True     # 3x speed boost
ENABLE_QUALITY_SCORING = True         # Objective metrics
ENABLE_WORKFLOW_MEMORY = True         # Learning system
ENABLE_VARIATION_VALIDATION = True    # Differentiation check
ENABLE_MULTIPASS_EDITING = True       # 4-pass polish
```

### AI Provider Configuration

**OpenAI (Per-Agent Models):**
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...

# Different models for different agents
OPENAI_WRITER_MODEL=gpt-5-nano        # Fast drafting
OPENAI_LLMON_MODEL=gpt-4o-mini        # Creative variations
OPENAI_EDITOR_MODEL=gpt-4.1-mini      # Premium polish
```

**Google Gemini (Simple):**
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key-here
```

### Agent Temperature Settings

```python
WRITER_TEMPERATURE = 0.7   # Balanced creativity
LLMON_TEMPERATURE = 0.8    # Higher for variation diversity
EDITOR_TEMPERATURE = 0.5   # Lower for consistency
```

---

## 💡 Usage Tips & Best Practices

### ✅ For Best Results

1. **Write Detailed Briefs** - More detail in `manual.md` = better output
2. **Use References Liberally** - Add data, examples, research to `references.md`
3. **Customize Templates** - Adjust `template.md` for your specific format
4. **Leverage Memory** - System improves over multiple sessions
5. **Monitor Quality Scores** - Use metrics to identify weak areas
6. **Iterate Strategically** - Use outline revisions for structure, feedback for content

### 📝 Example Use Cases

- **Blog Posts** - Optimized for engagement and SEO
- **Technical Articles** - Structured with clarity and accuracy
- **Marketing Content** - Persuasive with strong calls-to-action
- **Educational Guides** - Clear explanations with examples
- **Product Descriptions** - Benefit-focused with features
- **Industry Analyses** - Data-driven with insights

### ⚡ Performance Tips

- **Parallel processing** saves ~90 seconds per LLMON iteration
- **Outline approval** reduces wasted time on wrong structure
- **Quality scores** help identify issues before final polish
- **Memory system** reduces iterations after 2-3 sessions

---

## 🔧 Advanced Customization

### Modify Agent Behavior

**LLMON Variations:**
Edit `rules/llmon_rules.md`:
```markdown
# Variation 1: Professional
- Formal tone, executive audience
- Data-driven, authoritative

# Variation 2: Conversational
- Casual, friendly, relatable
- Story-driven, examples

# Variation 3: Technical
- Detailed, precise, expert-level
- Code examples, specifications
```

**Editor Standards:**
Edit `rules/editor_rules.md` to adjust polish criteria.

### Change Article Structure

Edit `templates/template.md`:
```markdown
# [Your Custom Structure]

## Introduction (100-150 words)
- Hook
- Context
- Thesis

## Main Sections (3-5 sections, 300-500 words each)
[Your requirements...]

## Conclusion (100-150 words)
- Summary
- Call-to-action
```

### Adjust Quality Thresholds

```python
# In quality_analyzer.py
MIN_VARIATION_DIFFERENCE = 0.3  # 30% minimum (0-1 scale)
```

---

## 💰 Cost Analysis

### OpenAI GPT-4o (Typical Usage)

| Metric | Estimate |
|--------|----------|
| **Input tokens per article** | ~50,000 |
| **Output tokens per article** | ~30,000 |
| **Input cost** | $0.125 ($2.50/1M) |
| **Output cost** | $0.300 ($10.00/1M) |
| **Total per article** | **~$0.43** |
| **Articles from $10** | **~23 articles** |

### Google Gemini (Free Tier)

- **Cost:** $0.00
- **Limit:** 15 requests/minute
- **Best for:** Testing, low-volume use

**💡 Tip:** Use cheaper models (gpt-5-nano) for Writer/LLMON, premium (gpt-4.1) for Editor only!

---

## 📚 Full Documentation

This README provides a comprehensive overview. For deeper details:

- 📖 **[Complete File Index](docs/INDEX.md)** - Navigate all project files
- 🚀 **[Quick Start Guide](docs/guides/QUICK_START.md)** - 5-minute setup
- 🔧 **[Setup Instructions](docs/setup/SETUP.md)** - Detailed configuration
- 📊 **[Workflow Diagrams](docs/guides/WORKFLOW_DIAGRAM.md)** - Visual guides
- ✨ **[Enhancements Guide](docs/guides/ENHANCEMENTS_GUIDE.md)** - Feature deep-dive
- 📝 **[Changelog](docs/project/CHANGELOG.md)** - Version history (v1.0 → v3.0)
- 🏗️ **[Project Summary](docs/project/PROJECT_SUMMARY.md)** - Technical overview
- 🤖 **[Agent Analysis](docs/project/AGENT_ANALYSIS.md)** - Agent architecture

---

## ✅ Testing & Verification

### Run Setup Verification

```bash
python test_setup.py
```

**Checks:**
- ✅ Python version (3.8+)
- ✅ All dependencies installed
- ✅ API keys configured
- ✅ Template files exist
- ✅ Directory structure

### Run Enhancement Tests

```bash
python test_enhancements.py
```

**Results:**
- ✅ 23 tests total
- ✅ 23 passing
- ✅ 0 failing
- 🕐 Execution: ~1 second

---

## ❓ Troubleshooting

### Common Issues

<details>
<summary><b>"API key not found"</b></summary>

**Solution:**
1. Check `.env` file exists in root directory
2. Verify variable name: `OPENAI_API_KEY` or `GEMINI_API_KEY`
3. No quotes needed around key value
4. Run `python setup_env.py` for interactive setup

</details>

<details>
<summary><b>"Missing model configuration"</b></summary>

**Solution (OpenAI):**
```env
OPENAI_WRITER_MODEL=gpt-5-nano
OPENAI_LLMON_MODEL=gpt-4o-mini
OPENAI_EDITOR_MODEL=gpt-4.1-mini
```

All three required for OpenAI provider.
</details>

<details>
<summary><b>"File not found" errors</b></summary>

**Solution:**
1. Check `templates/manual.md` exists and has content
2. Verify working directory: `cd ai-content-studio`
3. Copy from examples: `cp examples/example_manual.md templates/manual.md`

</details>

<details>
<summary><b>Poor output quality</b></summary>

**Solutions:**
- ✅ Add more detail to `templates/manual.md`
- ✅ Include data in `templates/references.md`
- ✅ Check quality scores for weak areas
- ✅ Provide specific feedback in revision loops
- ✅ Customize `template.md` for your needs

</details>

<details>
<summary><b>API rate limits</b></summary>

**Solutions:**
- **Gemini free tier:** 15 requests/minute
- **OpenAI:** Check limits at https://platform.openai.com/settings/organization/limits
- Wait briefly between runs or upgrade tier

</details>

---

## 🗺️ Roadmap & Future Enhancements

### Potential Future Features

- [ ] **Token usage tracking** - Real-time cost monitoring
- [ ] **Draft comparison tool** - Side-by-side version comparison
- [ ] **Template validation** - Automatic structure checking
- [ ] **AI-powered rule suggestions** - Smart rule generation
- [ ] **Batch processing mode** - Multiple articles in sequence
- [ ] **A/B testing support** - Variation performance tracking
- [ ] **SEO optimization agent** - Dedicated 4th agent
- [ ] **Export formats** - PDF, DOCX, HTML output
- [ ] **Web UI** - Browser-based interface
- [ ] **Claude/Anthropic support** - Additional AI provider

---

## 📄 License & Credits

**License:** MIT - Free to use and modify for your content creation needs.

**Credits:**
- Built with Python, OpenAI GPT-4o/4.1, Google Gemini
- Quality analysis: TextStat, scikit-learn
- CLI: Colorama

---

## 🆘 Support & Resources

### Getting Help

1. **Read the docs:** Start with [docs/INDEX.md](docs/INDEX.md)
2. **Check examples:** See `examples/` directory
3. **Run tests:** `python test_setup.py` to verify setup
4. **Review changelog:** [docs/project/CHANGELOG.md](docs/project/CHANGELOG.md)

### External Resources

- **OpenAI API Keys:** https://platform.openai.com/api-keys
- **OpenAI Pricing:** https://openai.com/api/pricing/
- **Gemini API Keys:** https://makersuite.google.com/app/apikey
- **Python Downloads:** https://www.python.org/downloads/

---

## 🎉 Get Started Now!

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up API access
python setup_env.py

# 3. Edit your content brief
# Open templates/manual.md and add your topic

# 4. Run the workflow
python main.py

# 🚀 Watch the magic happen!
```

---

**Built with ❤️ for efficient, intelligent, scalable content creation**

*AI-Content-Studio v3.0 - October 2025*


