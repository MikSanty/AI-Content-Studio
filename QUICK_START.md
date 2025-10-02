# Quick Start Guide

Get up and running in 5 minutes!

## ⚡ Super Fast Setup

### 1. Install Dependencies (30 seconds)
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key (2 minutes)

**Option A: Automated Setup**
```bash
python setup_env.py
```

**Option B: Manual Setup**
1. Get free key: https://makersuite.google.com/app/apikey
2. Create `.env` file with: `GEMINI_API_KEY=your_key_here`

### 3. Fill Content Brief (2 minutes)

Edit `templates/manual.md`:
```markdown
## Article Topic
[Your topic here]

## Target Audience
[Who are you writing for?]

## Key Objectives
- Point 1
- Point 2
- Point 3
```

See `examples/example_manual.md` for a complete example.

### 4. Run It! (30 seconds to start)
```bash
python main.py
```

That's it! Follow the interactive prompts.

---

## 📝 Your First Article

Try this minimal example to test the system:

**templates/manual.md:**
```markdown
# Content Brief

## Article Topic
Benefits of Remote Work for Small Businesses

## Target Audience
Small business owners considering remote work policies

## Key Objectives
- Explain cost benefits of remote work
- Show productivity improvements
- Address common concerns

## Main Points to Cover
1. Cost savings (office space, utilities)
2. Access to wider talent pool
3. Employee satisfaction and retention
4. Tools and best practices

## Tone and Style
Professional but friendly, practical advice

## Word Count Target
1000 words
```

**templates/references.md:**
```markdown
# Reference Materials

## Key Statistics
- 77% of remote workers report increased productivity (FlexJobs)
- Average savings of $11,000 per employee annually (Global Workplace Analytics)
- 74% of workers say remote options would make them less likely to leave (OWL Labs)

## Tools to Mention
- Slack, Zoom, Asana, Google Workspace
```

Now run `python main.py` and watch it create your article!

---

## 🎯 Workflow Quick Reference

```
START → WRITER → Approve? → LLMON → Select? → EDITOR → Approve? → DONE
           ↓                  ↓                  ↓
        Revise            Iterate           Minor Edits
```

### At Each Stage:

**WRITER** (makes draft)
- ✓ = Move to LLMON
- ✎ = Give feedback, revise
- ✗ = Stop

**LLMON** (makes 3 versions)
- Select 1/2/3 = Move to EDITOR
- ↻ = Edit rules, regenerate
- ✗ = Stop

**EDITOR** (polishes)
- ✓ = Done! 
- ✎ = Request changes
- ✗ = Stop

---

## 📂 Where Are My Files?

All outputs go to: `outputs/[timestamp]/`

- `01_writer_draft.md` - Initial draft
- `02_llmon_variation1.md` - First style
- `02_llmon_variation2.md` - Second style
- `02_llmon_variation3.md` - Third style
- `03_editor_polished.md` - Polished version
- `FINAL_ARTICLE.md` - **Your final article!** ✨

---

## 🔧 Common Commands

```bash
# Install
pip install -r requirements.txt

# Setup API key
python setup_env.py

# Run workflow
python main.py

# Check Python version (need 3.8+)
python --version
```

---

## ❓ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "GEMINI_API_KEY not found" | Run `python setup_env.py` |
| "File not found: templates/manual.md" | You're in wrong directory, cd to project root |
| "ImportError" | Run `pip install -r requirements.txt` |
| API errors | Check internet connection and API key |

---

## 💡 Pro Tips

1. **Start Simple** - Test with a topic you know well
2. **Use Examples** - Copy from `examples/` folder
3. **Add References** - More context = better output
4. **Try Revisions** - Test the feedback loops
5. **Compare Variations** - LLMON's 3 styles show different approaches

---

## 📚 Next Steps

- ✅ Complete your first article
- 📖 Read full `README.md` for details
- 🎨 Customize `rules/` files for your style
- 🔄 Try the iteration features
- 📊 Review all output files to see the progression

---

## 🚀 Going to Production

Once you're happy with test results:

1. **Keep using Gemini** (free tier is generous)
   
   OR

2. **Upgrade to Claude/Anthropic:**
   - Get API key from anthropic.com
   - Install: `pip install anthropic`
   - Update `api_client.py` to use Anthropic
   - Add to `.env`: `ANTHROPIC_API_KEY=your_key`

The workflow logic stays the same - just better AI! 🎯

---

**Ready? Let's create some content!** 🎉

```bash
python main.py
```


