<!-- 8ac3d91e-7394-44db-b1e3-d4ce59302819 93909d44-56f5-490b-ab05-cb2c5a38a188 -->
# Tool Review Mode Implementation Plan

## Overview

Integrate tool review capabilities into the existing AI-Content-Studio workflow, allowing users to generate story-driven, personable tool reviews following the client's template specifications while maintaining the existing general article functionality.

## Implementation Approach

### Phase 1: Template Infrastructure

**Create new template files** in `templates/` directory:

1. **`templates/tool_review_brief.md`** - Structured brief template

   - 4 pre-writing questions (Title, Audience, Reader Motivation, Reader Benefit)
   - Tool details section (name, category, pricing model)
   - Quote collection area (6-10 quotes with sources and URLs)
   - Product-specific info (pricing tiers, migration notes, implementation)

2. **`templates/tool_review_structure.md`** - Fixed review structure

   - All required sections from client template: "What is [Tool]?", "How [Tool] Works", "How I Use [Tool]", "Why It Matters", "AI Features", "Who Should Use [Tool]?", "Pricing Plans", "Pros", "Cons", "Caveats", "Ratings & Reviews", "Sources"
   - Natural-query headers optimized for LLMs
   - Section-specific guidance (word counts, required elements)

3. **`templates/tool_review_writer_prompt.md`** - Tool review-specific writing instructions

   - Narrative voice requirements (first-person, story-driven)
   - Conditional framing patterns ("If you're X... if you're Y...")
   - Quote integration guidelines (inline citation + sources appendix)
   - Personable tone guidance inspired by Surfer example
   - 2-4 mini callouts requirement
   - Product-aware analysis expectations

### Phase 2: Rules for Tool Review Variations

**Create specialized rules** in `rules/` directory:

1. **`rules/llmon_tool_review_rules.md`** - Variation guidance for reviews

   - Maintain story-driven narrative across variations
   - Preserve first-person anecdotes
   - Adjust comparative guidance emphasis per variation
   - Keep product details (pricing, migration) factual across all

2. **`rules/editor_tool_review_rules.md`** - Polish rules for reviews

   - Verify no em dashes (client requirement)
   - Check no parenthetical text in headers
   - Ensure sources appendix at bottom
   - Validate quote attribution format
   - Confirm 900-1,400 word soft target
   - Remove divider lines

### Phase 3: Configuration & Mode Selection

**Update `config.py`:**

```python
# Content Mode Selection
CONTENT_MODE = os.getenv('CONTENT_MODE', 'article')  # 'article' or 'tool_review'

# Tool Review Settings
TOOL_REVIEW_MIN_QUOTES = 6
TOOL_REVIEW_MAX_QUOTES = 10
TOOL_REVIEW_TARGET_WORDS = (900, 1400)  # soft range
```

**Update `main.py`:**

- Add mode selection prompt at startup (if not set in .env)
- Display appropriate template file names based on mode
- Update checklist guidance for tool_review vs article mode

### Phase 4: Writer Agent Enhancement

**Update `agents/writer_agent.py`:**

**Add method** `_detect_content_mode(manual_path)`:

- Read manual file
- Check for tool review markers (interview questions section)
- Return 'tool_review' or 'article'

**Add method** `generate_draft_tool_review(...)`:

- Similar to `generate_draft()` but uses tool review prompt template
- Emphasizes narrative voice, conditional framing
- Integrates quote requirements
- Uses tool_review_structure.md

**Add method** `generate_outline_tool_review(...)`:

- Creates outline specific to tool review structure
- Plans quote placement
- Structures "How I Use" narrative
- Maps audience-specific callouts

**Modify** `write_from_outline()`:

- Detect mode from outline content
- Apply tool review-specific citation rules if in tool review mode

### Phase 5: LLMON Agent Adaptation

**Update `agents/llmon_agent.py`:**

**Add method** `generate_variations_tool_review(article, rules_path, differentiator=None)`:

- Uses `rules/llmon_tool_review_rules.md`
- Preserves story-driven elements across variations
- Maintains product facts consistency
- Varies tone while keeping first-person narrative

**Modify** `_create_variation_prompt()`:

- Add mode detection
- Apply tool review variation rules if appropriate
- Preserve quote sources appendix format

### Phase 6: Editor Agent Adaptation

**Update `agents/editor_agent.py`:**

**Add method** `polish_article_tool_review(article, rules_path)`:

- Uses `rules/editor_tool_review_rules.md`
- Multi-pass editing with tool review checklist
- Validates no em dashes, clean headers, sources appendix
- Checks word count against soft target

**Add validation pass** `_validate_tool_review_format()`:

- Confirms sources appendix exists
- Checks quote attribution format
- Verifies no divider lines
- Validates header cleanliness (no parentheticals)

### Phase 7: Workflow Orchestration

**Update `workflow.py`:**

**In `__init__`:**

- Detect content mode from config or manual.md
- Set template paths based on mode
- Display mode-specific guidance

**In `_writer_stage`:**

- Use tool review templates if mode == 'tool_review'
- Call `generate_outline_tool_review` or `generate_draft_tool_review`
- Apply tool review validation (quote count check)

**In `_llmon_stage`:**

- Use tool review rules if mode == 'tool_review'
- Validate product fact consistency across variations

**In `_editor_stage`:**

- Use tool review polish method if mode == 'tool_review'
- Apply format validation checks

### Phase 8: Documentation & Examples

**Create example files:**

1. **`examples/example_tool_review_brief.md`** - Sample completed brief

   - Filled-out interview questions
   - Sample quotes with sources (G2, Reddit, Capterra)
   - Pricing breakdown example

2. **`examples/example_tool_review_output.md`** - Sample final review

   - Based on Surfer-style from client template
   - Demonstrates all required sections
   - Shows proper quote integration and sources appendix

**Update documentation:**

- Add tool review mode section to README.md
- Create `docs/guides/TOOL_REVIEW_MODE.md` with detailed instructions
- Update QUICK_START.md with mode selection step

## Testing Strategy

1. **Manual test run** with example tool review brief
2. **Validate** output against client template requirements:

   - Story-driven narrative present
   - 6-10 quotes integrated with sources appendix
   - Conditional framing ("If you're...")
   - No em dashes, clean headers
   - 900-1,400 word range
   - All required sections present

3. **Compare** existing article mode still works unchanged

## File Changes Summary

**New Files (10):**

- `templates/tool_review_brief.md`
- `templates/tool_review_structure.md`
- `templates/tool_review_writer_prompt.md`
- `rules/llmon_tool_review_rules.md`
- `rules/editor_tool_review_rules.md`
- `examples/example_tool_review_brief.md`
- `examples/example_tool_review_output.md`
- `docs/guides/TOOL_REVIEW_MODE.md`

**Modified Files (6):**

- `config.py` - Add mode settings
- `main.py` - Add mode selection
- `agents/writer_agent.py` - Add tool review methods
- `agents/llmon_agent.py` - Add tool review variation logic
- `agents/editor_agent.py` - Add tool review polish logic
- `workflow.py` - Add mode detection and routing
- `README.md` - Add tool review documentation section

## Success Criteria

- User can select tool review mode
- System uses appropriate templates based on mode
- Output matches client template requirements
- Existing article mode continues working
- All 6 enhancements work in both modes
- Quote integration works correctly with sources appendix

### To-dos

- [ ] Create three new template files: tool_review_brief.md, tool_review_structure.md, and tool_review_writer_prompt.md with all client specifications
- [ ] Create two new rules files: llmon_tool_review_rules.md and editor_tool_review_rules.md with tool review-specific guidance
- [ ] Update config.py to add CONTENT_MODE and tool review settings
- [ ] Update writer_agent.py with tool review methods: generate_draft_tool_review, generate_outline_tool_review, and mode detection
- [ ] Update llmon_agent.py with tool review variation logic and story preservation
- [ ] Update editor_agent.py with tool review polish method and format validation
- [ ] Update workflow.py to detect mode and route to appropriate methods in each stage
- [ ] Update main.py to add mode selection prompt and display appropriate guidance
- [ ] Create example_tool_review_brief.md and example_tool_review_output.md in examples/ directory
- [ ] Create TOOL_REVIEW_MODE.md guide and update README.md with tool review mode section
- [ ] Run manual test with example tool review brief and validate output against all client requirements