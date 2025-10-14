# Setup Instructions

Follow these steps to get AI-Content-Studio up and running.

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` - Google Gemini API client
- `python-dotenv` - Environment variable management
- `colorama` - Colored terminal output

## Step 2: Get Your Free Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

**Note:** Gemini API has a generous free tier that's perfect for testing this workflow.

## Step 3: Create Your .env File

Create a file named `.env` in the project root:

```bash
GEMINI_API_KEY=AIza...your_actual_key_here
```

**Important:** 
- Don't commit `.env` to git (it's in `.gitignore`)
- Keep your API key private

## Step 4: Fill Out Your Content Brief

Edit these files in the `templates/` folder:

### 1. templates/manual.md (REQUIRED)
This is your content brief. Fill it out with:
- Article topic
- Target audience
- Key objectives
- Main points to cover
- Tone/style preferences

See `examples/example_manual.md` for inspiration.

### 2. templates/references.md (RECOMMENDED)
Add any:
- Research and data
- Links to reference
- Examples to include
- Expert quotes
- Statistics

### 3. templates/template.md (OPTIONAL)
The default template works for most articles, but you can customize:
- Section structure
- Heading names
- Content organization

## Step 5: Review Agent Rules (OPTIONAL)

Check these files if you want to customize agent behavior:

- `rules/llmon_rules.md` - How variations are created
- `rules/editor_rules.md` - Editing standards

The defaults work well, but you can adjust them for your specific needs.

## Step 6: Run the Workflow

```bash
python main.py
```

The system will:
1. Generate an initial draft (WRITER)
2. Create 3 variations (LLMON)
3. Polish the final article (EDITOR)

You'll approve or revise at each stage.

## Verification Checklist

Before running, make sure:
- [ ] Python 3.8+ is installed
- [ ] Dependencies are installed (`pip install -r requirements.txt`)
- [ ] `.env` file exists with your `GEMINI_API_KEY`
- [ ] `templates/manual.md` is filled out
- [ ] You have at least some content in `templates/references.md`

## First Run Tips

For your first test run:

1. **Start with a simple topic** - Try something you know well
2. **Fill out manual.md thoroughly** - More detail = better results
3. **Add at least 3-5 references** - Gives the AI context
4. **Review all three LLMON variations** - See how style changes work
5. **Use the revision loops** - Test the feedback mechanism

## Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists in project root
- Check that the key is on a line like: `GEMINI_API_KEY=your_key`
- No quotes needed around the key

### "File not found: templates/manual.md"
- Make sure you're running from the project root directory
- Check that the `templates/` folder exists
- Verify `manual.md` is in the templates folder

### API Errors
- Check your API key is valid
- Ensure you have internet connection
- Verify you haven't exceeded free tier limits

### Import Errors
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.8 or higher

## What Happens During a Run

1. **Session Creation** - Creates a timestamped folder in `outputs/`
2. **Writer Stage** - Generates draft, saves to `01_writer_draft.md`
3. **LLMON Stage** - Creates 3 variations, saves each one
4. **Editor Stage** - Polishes selected variation
5. **Final Output** - Saves as `FINAL_ARTICLE.md`

All intermediate files are kept so you can review the progression.

## Next Steps

Once you've completed your first successful run:

1. **Experiment with manual.md** - Try different topics and styles
2. **Customize rules** - Adjust `llmon_rules.md` and `editor_rules.md`
3. **Test revision loops** - Practice giving feedback to agents
4. **Try rule editing** - Modify LLMON rules on-the-fly during iteration
5. **Plan your transition** - When ready, upgrade to Claude/Anthropic API

## Need Help?

- Check the main `README.md` for detailed documentation
- Review `brainstorm-session-result.md` for the design philosophy
- Look at example files in `examples/` folder
- Verify all checklist items above

Happy content creating! 🚀


