# AI-Content-Studio - File Index

Quick navigation guide to all project files.

## 🚀 Getting Started (Start Here!)

| File | Purpose | When to Use |
|------|---------|-------------|
| **`README.md`** (root) | Complete documentation | Full reference |
| **`docs/guides/QUICK_START.md`** | 5-minute setup guide | First time setup |
| **`docs/FEATURES.md`** | Complete features guide | Feature overview & config |
| **`docs/setup/SETUP.md`** | Detailed setup instructions | Step-by-step help |

## ⚙️ Setup & Configuration

| File | Purpose |
|------|---------|
| `setup_env.py` | Interactive API key setup |
| `test_setup.py` | Verify installation |
| `requirements.txt` | Python dependencies |
| `.env` | API keys (create this!) |
| `.gitignore` | Git ignore rules |

## 🏃 Running the Application

| File | Purpose | Platform |
|------|---------|----------|
| `main.py` | Main entry point | All |
| `run.bat` | Quick launch script | Windows |
| `run.sh` | Quick launch script | Linux/Mac |

**How to run:**
- Windows: `python main.py` or double-click `run.bat`
- Linux/Mac: `python3 main.py` or `./run.sh`

## 📝 Templates (YOU FILL THESE OUT)

Location: `templates/` directory

### General Article Mode

| File | Purpose | Required? |
|------|---------|-----------|
| **`manual.md`** | Your content brief | ✅ Yes |
| `template.md` | Article structure | Optional* |
| `references.md` | Research & data | Recommended |
| `writer_prompt.md` | Writer instructions | Optional* |

### Tool Review Mode

| File | Purpose | Required? |
|------|---------|-----------|
| **`tool_review_brief.md`** | Tool review input | ✅ Yes (for reviews) |
| `tool_review_structure.md` | Review section structure | Optional* |
| `tool_review_writer_prompt.md` | Review writer instructions | Optional* |

*Default versions work well, but customize if needed

## 📏 Rules (Agent Behavior)

Location: `rules/` directory

### General Article Mode

| File | Controls | When to Edit |
|------|----------|--------------|
| `llmon_rules.md` | Style variations | Customize variation styles |
| `editor_rules.md` | Polish standards | Adjust editing criteria |

### Tool Review Mode

| File | Controls | When to Edit |
|------|----------|--------------|
| `llmon_tool_review_rules.md` | Review style variations | Customize review variations |
| `editor_tool_review_rules.md` | Review polish standards | Adjust review editing |

## 🤖 Core Application

Location: Root directory

| File | Purpose |
|------|---------|
| `main.py` | Application entry point |
| `workflow.py` | Orchestrates 3-agent pipeline |
| `config.py` | Settings & configuration |
| `api_client.py` | Multi-provider API integration (OpenAI/Gemini) |
| `utils.py` | Helper functions |

## 🧠 Intelligence Modules

Location: Root directory

| File | Purpose |
|------|---------|
| `quality_analyzer.py` | Multi-dimensional content quality scoring |
| `workflow_memory.py` | Cross-stage learning and preference extraction |
| `variation_differentiator.py` | Ensures LLMON variations are distinct |
| `citation_validator.py` | Citation & hyperlink validation |

## 🧠 Agent Modules

Location: `agents/` directory

| File | Agent | Stage |
|------|-------|-------|
| `writer_agent.py` | WRITER | Stage 1: Draft |
| `llmon_agent.py` | LLMON | Stage 2: Variations |
| `editor_agent.py` | EDITOR | Stage 3: Polish |
| `__init__.py` | Package setup | - |

## 💡 Examples

Location: `examples/` directory

### General Article Examples

| File | Purpose |
|------|---------|
| `example_manual.md` | Sample content brief |
| `example_references.md` | Sample references |
| `template_manual.md` | Blank template for briefs |
| `template_references.md` | Blank template for references |

### Tool Review Examples

| File | Purpose |
|------|---------|
| `example_tool_review_brief.md` | Complete tool review example |
| `example_tool_review_output.md` | Sample generated review |
| `template_tool_review_brief.md` | Blank template for tool reviews |

**Use these as templates for your own content!**

## 📚 Documentation

Location: `docs/` directory

### Getting Started

| File | Audience | Content |
|------|----------|---------|
| `README.md` (root) | Everyone | Complete project guide |
| `docs/guides/QUICK_START.md` | New users | 5-minute setup |
| `docs/setup/SETUP.md` | First-time users | Detailed setup instructions |
| `docs/setup/OPENAI_SETUP_INSTRUCTIONS.md` | OpenAI users | OpenAI-specific setup |

### Feature Guides

| File | Topic | Content |
|------|-------|---------|
| `docs/FEATURES.md` | All features | Complete feature reference |
| `docs/guides/ENHANCEMENTS_GUIDE.md` | Enhancements | Feature deep-dive & usage |
| `docs/guides/TOOL_REVIEW_MODE.md` | Tool reviews | Complete tool review guide |
| `docs/guides/WORKFLOW_DIAGRAM.md` | Visual workflow | Flow diagrams & architecture |

### Project Documentation

| File | Audience | Content |
|------|----------|---------|
| `docs/project/PROJECT_SUMMARY.md` | Developers | System overview & architecture |
| `docs/project/CHANGELOG.md` | All users | Version history & changes |
| `docs/project/AGENT_ANALYSIS.md` | Developers | Technical agent analysis |

### Navigation

| File | Purpose |
|------|---------|
| `docs/INDEX.md` | This file - Complete file reference |

## 🧪 Testing

Location: Root directory

| File | Purpose |
|------|---------|
| `test_setup.py` | Verify installation and API configuration |
| `test_enhancements.py` | Unit tests for all enhancement modules |
| `test_citation_validator.py` | Citation validation tests |

## 📂 Output Files

Location: `outputs/[timestamp]/` (auto-created)

| File | Content | Stage |
|------|---------|-------|
| `01_writer_outline.md` | Article outline | After outline phase |
| `01_writer_draft.md` | Initial draft | After Writer |
| `02_llmon_variation1_iter0.md` | Style variation 1 | After LLMON |
| `02_llmon_variation2_iter0.md` | Style variation 2 | After LLMON |
| `02_llmon_variation3_iter0.md` | Style variation 3 | After LLMON |
| `03_editor_polished.md` | Polished article | After Editor |
| **`FINAL_ARTICLE.md`** | **Final output** | **Complete!** |

*Note: Files may have quality scores and iteration numbers appended*

## 🎯 Quick Reference

### First Time Setup
```bash
1. pip install -r requirements.txt
2. python setup_env.py
3. Edit templates/manual.md
4. python main.py
```

### Daily Use
```bash
1. Edit templates/manual.md (new brief)
2. python main.py
3. Follow prompts
```

### Verify Setup
```bash
python test_setup.py
```

## 📖 Reading Order for New Users

1. **Start:** `QUICK_START.md` (5 minutes)
2. **Setup:** Follow quick start instructions
3. **First Run:** Use example from quick start
4. **Learn More:** `README.md` (when needed)
5. **Understand Flow:** `WORKFLOW_DIAGRAM.md` (optional)
6. **Deep Dive:** `PROJECT_SUMMARY.md` (optional)

## 🔍 Common Tasks

### How do I...

**...get started?**
→ Read `QUICK_START.md`

**...set up my API key?**
→ Run `python setup_env.py`

**...create my first article?**
→ Edit `templates/manual.md`, then run `python main.py`

**...customize article structure?**
→ Edit `templates/template.md`

**...change how variations work?**
→ Edit `rules/llmon_rules.md`

**...test if everything is set up?**
→ Run `python test_setup.py`

**...find my output files?**
→ Check `outputs/[timestamp]/FINAL_ARTICLE.md`

**...see the workflow visually?**
→ Read `WORKFLOW_DIAGRAM.md`

**...understand the design?**
→ Read `brainstorm-session-result.md`

**...upgrade to Claude API?**
→ See "Transitioning" section in `README.md`

## 🎨 Customization Guide

### Beginner Level
- Edit `templates/manual.md` for each article
- Use examples as starting points
- Stick with default rules

### Intermediate Level
- Customize `templates/template.md` for your format
- Modify `rules/llmon_rules.md` for your style
- Adjust `rules/editor_rules.md` for standards

### Advanced Level
- Edit `config.py` for AI settings
- Modify agent modules for behavior
- Switch API provider in `api_client.py`

## 📊 File Status Quick View

### ✅ Ready to Use (Don't Need to Touch)
- All agent files
- Core application files
- Documentation files
- Example files
- Default rules and templates

### ⚠️ Must Configure
- `.env` file (API key)
- `templates/manual.md` (your content)

### 🎨 Optional to Customize
- `templates/template.md` (structure)
- `templates/references.md` (data)
- `rules/llmon_rules.md` (variations)
- `rules/editor_rules.md` (polish)

## 🆘 Troubleshooting Guide

**Problem:** Don't know where to start
**Solution:** → Read `QUICK_START.md`

**Problem:** Setup not working
**Solution:** → Run `python test_setup.py`

**Problem:** API errors
**Solution:** → Check `.env` file, re-run `python setup_env.py`

**Problem:** Bad output quality
**Solution:** → Add more detail to `templates/manual.md` and `references.md`

**Problem:** Want different style variations
**Solution:** → Edit `rules/llmon_rules.md` or use iteration feature

**Problem:** Need help understanding workflow
**Solution:** → Read `WORKFLOW_DIAGRAM.md`

## 🔗 External Resources

- Get Gemini API Key: https://makersuite.google.com/app/apikey
- Python Downloads: https://www.python.org/downloads/
- Anthropic API (future): https://www.anthropic.com/api

---

**Quick Links:**
- 🚀 [Quick Start](guides/QUICK_START.md)
- 📖 [Full Documentation](../README.md)
- 🔧 [Setup Guide](setup/SETUP.md)
- 📊 [Workflow Diagram](guides/WORKFLOW_DIAGRAM.md)
- 📋 [Project Summary](project/PROJECT_SUMMARY.md)
- 📝 [Changelog](project/CHANGELOG.md)

---

**Everything you need is in this directory!** 🎉


