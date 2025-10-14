# Quick Start Guide

Get up and running in 5 minutes!

## ⚡ Super Fast Setup

### 1. Install Dependencies (30 seconds)
```bash
pip install -r requirements.txt
```

### 2. Set Up API Key (2 minutes)

**Option A: OpenAI (Recommended for Quality)**
1. Get API key: https://platform.openai.com/api-keys
2. Copy `.env.example` to `.env`
3. Add your OpenAI key and models to `.env`:
   ```
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_key_here
   OPENAI_WRITER_MODEL=gpt-5-nano
   OPENAI_LLMON_MODEL=gpt-4o-mini
   OPENAI_EDITOR_MODEL=gpt-4.1-mini
   ```
   
   **Note**: Each agent can use a different model for specialized performance.
   You can also use the same model for all three agents.

**Option B: Gemini (Free Tier)**
1. Get free key: https://makersuite.google.com/app/apikey
2. Copy `.env.example` to `.env`
3. Add your Gemini key to `.env`:
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   ```

**Model Recommendations:**
- **GPT-4o**: Best cost/quality balance (~$0.43/article, ~23 articles per $10)
- **GPT-4-turbo**: Higher quality, more expensive (~$1.40/article)
- **GPT-3.5-turbo**: Most economical but lower quality (~$0.07/article)
- **Gemini 2.5 Flash**: Free tier, good quality

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

## 🔄 Switching AI Providers

The system supports both OpenAI and Gemini. To switch providers:

1. Open your `.env` file
2. Change the `AI_PROVIDER` setting:
   ```
   # For OpenAI
   AI_PROVIDER=openai
   
   # For Gemini
   AI_PROVIDER=gemini
   ```
3. Ensure you have the corresponding API key set
4. Run the workflow normally

**Cost Comparison (per complete article):**
- OpenAI (multi-model setup): Varies based on chosen models
  - Example: gpt-5-nano + gpt-4o-mini + gpt-4.1-mini
- OpenAI (single model for all agents): ~$0.43 with gpt-4o ⭐ Best balance
- Gemini 2.5 Flash: FREE (with daily limits)

**Note**: OpenAI allows you to configure different models for each agent (Writer, LLMON, Editor),
enabling you to optimize for cost and performance based on each agent's specific task.

## 🚀 Going to Production

Once you're happy with test results:

1. **Using OpenAI:** Monitor your usage at https://platform.openai.com/usage
   - Set spending limits in your OpenAI account
   - GPT-4o recommended for production (best cost/quality)

2. **Using Gemini:** Free tier is generous for moderate use
   - Upgrade to paid tier if you hit rate limits

The workflow logic stays the same - just different AI providers! 🎯

---

**Ready? Let's create some content!** 🎉

```bash
python main.py
```


