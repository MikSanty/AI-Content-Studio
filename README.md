# AI-Content-Studio

**A 3-Agent AI Workflow for Scalable Content Creation**

This system implements an intelligent, multi-agent content creation pipeline that transforms a content brief into a polished, publication-ready article through three specialized AI agents:

1. **WRITER** - Creates initial article drafts
2. **LLMON** - Generates multiple stylistic variations
3. **EDITOR** - Applies final polish and refinement

## 🌟 Key Features

- **Intelligent Revision Loops** - Provide feedback at each stage to guide the AI
- **Dynamic Rule Editing** - Adjust stylistic rules on-the-fly for better results
- **User Control Gates** - Approve, revise, or reject at each stage
- **Session Management** - All drafts and variations are saved for review
- **Free API Integration** - Uses Google Gemini (free tier) for initial setup

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download this repository
cd ai-content-studio

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory:

```bash
GEMINI_API_KEY=your_api_key_here
```

**Get your free API key:** https://makersuite.google.com/app/apikey

### 3. Prepare Your Content Brief

Edit the following files in the `templates/` directory:

- **`manual.md`** - Your content brief (topic, objectives, key points)
- **`template.md`** - Article structure and format (customize as needed)
- **`references.md`** - Reference materials, data, and research

### 4. Run the Workflow

```bash
python main.py
```

Follow the interactive prompts to guide your content through each stage!

## 📁 Project Structure

```
AI-Content-Studio/
├── main.py                 # Entry point
├── workflow.py             # Workflow orchestrator
├── config.py               # Configuration settings
├── api_client.py           # API integration
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── .env                    # API keys (create this)
├── agents/                 # AI agent modules
│   ├── writer_agent.py     # Stage 1: Initial draft
│   ├── llmon_agent.py      # Stage 2: Variations
│   └── editor_agent.py     # Stage 3: Polish
├── templates/              # Input templates
│   ├── manual.md           # Content brief (FILL THIS OUT)
│   ├── template.md         # Article structure
│   ├── references.md       # Reference materials
│   └── writer_prompt.md    # Writer instructions
├── rules/                  # Agent behavior rules
│   ├── llmon_rules.md      # LLMON stylistic rules
│   └── editor_rules.md     # Editor polish rules
└── outputs/                # Generated content (auto-created)
    └── [session_id]/       # Each run creates a session folder
        ├── 01_writer_draft.md
        ├── 02_llmon_variation1.md
        ├── 03_editor_polished.md
        └── FINAL_ARTICLE.md
```

## 🔄 Workflow Stages

### Stage 1: WRITER Agent

**Inputs:**
- `templates/manual.md` - Your content brief
- `templates/template.md` - Article structure
- `templates/references.md` - Reference materials
- `templates/writer_prompt.md` - Writing instructions

**Process:**
- Generates initial article draft based on your brief

**User Approval Gate:**
- ✓ **Approve** - Continue to LLMON
- ✎ **Revise with feedback** - Provide feedback for revision
- ✗ **Reject** - Stop workflow

### Stage 2: LLMON Agent

**Inputs:**
- Approved article from Stage 1
- `rules/llmon_rules.md` - Stylistic transformation rules

**Process:**
- Creates 3 distinct variations with different styles/approaches

**User Approval Gate:**
- **Select Variation 1/2/3** - Choose your favorite
- ↻ **Iterate with edited rules** - Modify rules and regenerate
- ✗ **Reject all** - Stop workflow

### Stage 3: EDITOR Agent

**Inputs:**
- Selected article from Stage 2
- `rules/editor_rules.md` - Editing guidelines

**Process:**
- Applies final polish, fixes grammar, improves flow

**User Approval Gate:**
- ✓ **Approve as final** - Complete workflow
- ✎ **Request minor revisions** - Provide specific changes
- ✗ **Reject** - Stop workflow

## 🎯 Usage Tips

### For Best Results:

1. **Be Specific in manual.md** - The more detailed your brief, the better the output
2. **Use References** - Add relevant data, examples, and research
3. **Customize the Template** - Adjust article structure to match your needs
4. **Iterate Thoughtfully** - Use revision loops when close to desired output
5. **Edit Rules on-the-fly** - In LLMON stage, adjust rules for better variations

### Example Content Brief Topics:

- Blog posts
- Technical articles
- Marketing content
- Educational guides
- Product descriptions
- Industry analyses

## 🔧 Customization

### Modify Agent Behavior

Edit the rules files:
- `rules/llmon_rules.md` - Change how variations are created
- `rules/editor_rules.md` - Adjust editing standards

### Change Article Structure

Edit `templates/template.md` to define your preferred article format

### Adjust AI Creativity

In `config.py`, modify temperature settings:
```python
WRITER_TEMPERATURE = 0.7   # Higher = more creative
LLMON_TEMPERATURE = 0.8    # Higher for more variation
EDITOR_TEMPERATURE = 0.5   # Lower for consistency
```

## 🔄 Transitioning to Better APIs

Currently using Google Gemini (free tier). To upgrade to Claude/Anthropic:

1. Install anthropic SDK: `pip install anthropic`
2. Update `api_client.py` to use Anthropic API
3. Add `ANTHROPIC_API_KEY` to `.env`

The agent logic remains the same - only the API client changes.

## 📊 Output Management

Each workflow run creates a session folder in `outputs/`:
- All drafts, variations, and revisions are saved
- Easy to compare versions and iterations
- Final article is marked as `FINAL_ARTICLE.md`

## ❓ Troubleshooting

### "GEMINI_API_KEY not found"
- Create a `.env` file with your API key
- Get free key: https://makersuite.google.com/app/apikey

### "File not found" errors
- Ensure you've filled out templates before running
- Check that template files exist in `templates/` directory

### API rate limits
- Gemini free tier has generous limits
- If you hit limits, wait a few minutes or upgrade to paid tier

## 📝 Example Workflow

```bash
$ python main.py

╔══════════════════════════════════════════════════════════╗
║              AI-Content-Studio WORKFLOW                     ║
╚══════════════════════════════════════════════════════════╝

Stage 1: WRITER AGENT
→ Generating initial draft...
→ Draft saved!

What would you like to do?
  1. ✓ Approve and continue
  2. ✎ Revise with feedback
  3. ✗ Reject and stop

> 1

Stage 2: LLMON AGENT
→ Generating 3 variations...

[Shows 3 different versions]

What would you like to do?
  1. Select Variation 1
  2. Select Variation 2
  3. Select Variation 3
  4. ↻ Iterate with edited rules
  5. ✗ Reject all

> 2

Stage 3: EDITOR AGENT
→ Polishing article...

[Shows final polished version]

What would you like to do?
  1. ✓ Approve as final
  2. ✎ Request minor revisions
  3. ✗ Reject

> 1

✓ WORKFLOW COMPLETE!
Final article saved to: outputs/20251002_143022/FINAL_ARTICLE.md
```

## 🤝 Contributing

This is based on the brainstorming session documented in `brainstorm-session-result.md`.

## 📄 License

Free to use and modify for your content creation needs.

---

**Built with ❤️ for efficient, scalable content creation**


