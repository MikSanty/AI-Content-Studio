# AI-Content-Studio Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI-Content-Studio                              │
│                   3-Agent Workflow Pipeline                      │
└─────────────────────────────────────────────────────────────────┘

                              START
                                │
                                ▼
                    ┌───────────────────────┐
                    │   USER PREPARATION    │
                    ├───────────────────────┤
                    │ • Fill manual.md      │
                    │ • Add references.md   │
                    │ • Review template.md  │
                    └───────────┬───────────┘
                                │
                                ▼
╔═══════════════════════════════════════════════════════════════╗
║                      STAGE 1: WRITER                           ║
╠═══════════════════════════════════════════════════════════════╣
║  INPUTS:                                                       ║
║  • manual.md (content brief)                                  ║
║  • template.md (structure)                                    ║
║  • references.md (research)                                   ║
║  • writer_prompt.md (instructions)                            ║
║                                                                ║
║  PROCESS:                                                      ║
║  → Generate complete article draft                            ║
║                                                                ║
║  OUTPUT:                                                       ║
║  → 01_writer_draft.md                                        ║
╚═══════════════════════════════════════════════════════════════╝
                                │
                                ▼
                    ┌───────────────────────┐
                    │  APPROVAL GATE #1     │
                    ├───────────────────────┤
                    │ 1. ✓ Approve          │
                    │ 2. ✎ Revise (feedback)│◄────┐
                    │ 3. ✗ Reject & Stop    │     │
                    └───────────┬───────────┘     │
                                │                  │
                        ┌───────┴───────┐         │
                        │               │          │
                    Approve          Revise        │
                        │               │          │
                        │               └──────────┘
                        │                (with feedback)
                        ▼
╔═══════════════════════════════════════════════════════════════╗
║                      STAGE 2: LLMON                            ║
╠═══════════════════════════════════════════════════════════════╣
║  INPUTS:                                                       ║
║  • Approved article from Stage 1                              ║
║  • llmon_rules.md (stylistic rules)                          ║
║                                                                ║
║  PROCESS:                                                      ║
║  → Generate 3 distinct variations                             ║
║    • Variation 1: Clear & Accessible                          ║
║    • Variation 2: Deep & Authoritative                        ║
║    • Variation 3: Engaging & Story-driven                     ║
║                                                                ║
║  OUTPUT:                                                       ║
║  → 02_llmon_variation1.md                                    ║
║  → 02_llmon_variation2.md                                    ║
║  → 02_llmon_variation3.md                                    ║
╚═══════════════════════════════════════════════════════════════╝
                                │
                                ▼
                    ┌───────────────────────┐
                    │  APPROVAL GATE #2     │
                    ├───────────────────────┤
                    │ 1-3. Select Variation │
                    │ 4. ↻ Iterate (edit    │◄────┐
                    │      rules on-the-fly)│     │
                    │ 5. ✗ Reject & Stop    │     │
                    └───────────┬───────────┘     │
                                │                  │
                        ┌───────┴────────┐        │
                        │                │         │
                    Select          Iterate        │
                  Variation            │           │
                        │              └───────────┘
                        │             (modify rules)
                        ▼
╔═══════════════════════════════════════════════════════════════╗
║                      STAGE 3: EDITOR                           ║
╠═══════════════════════════════════════════════════════════════╣
║  INPUTS:                                                       ║
║  • Selected article from Stage 2                              ║
║  • editor_rules.md (polish guidelines)                        ║
║                                                                ║
║  PROCESS:                                                      ║
║  → Apply final polish and refinement                          ║
║  → Fix grammar, improve flow                                  ║
║  → Ensure consistency and quality                             ║
║                                                                ║
║  OUTPUT:                                                       ║
║  → 03_editor_polished.md                                     ║
╚═══════════════════════════════════════════════════════════════╝
                                │
                                ▼
                    ┌───────────────────────┐
                    │  APPROVAL GATE #3     │
                    ├───────────────────────┤
                    │ 1. ✓ Approve (FINAL)  │
                    │ 2. ✎ Minor Revisions  │◄────┐
                    │ 3. ✗ Reject & Stop    │     │
                    └───────────┬───────────┘     │
                                │                  │
                        ┌───────┴───────┐         │
                        │               │          │
                    Approve         Revise         │
                        │               │          │
                        │               └──────────┘
                        │           (specific changes)
                        ▼
                ┌───────────────────┐
                │   FINAL OUTPUT    │
                ├───────────────────┤
                │ FINAL_ARTICLE.md  │
                │                   │
                │ ✅ Ready to       │
                │    publish!       │
                └───────────────────┘
                        │
                        ▼
                      END


═══════════════════════════════════════════════════════════════

KEY FEATURES:

🔄 Intelligent Revision Loops
   • Writer: Feedback-based revisions
   • LLMON: Rule editing for iterations
   • Editor: Minor polish adjustments

👤 User Control Gates
   • Approve, revise, or reject at each stage
   • Full control over the creative process
   • Save all versions for comparison

💾 Session Management
   • Timestamped output folders
   • All drafts and variations saved
   • Easy to track progression

🤖 Three Specialized Agents
   • WRITER: Content creation
   • LLMON: Style variations
   • EDITOR: Final polish

═══════════════════════════════════════════════════════════════

WORKFLOW PRINCIPLES:

1. Sequential Processing
   Each stage builds on the previous one

2. Human-in-the-Loop
   User approval required to advance

3. Iterative Refinement
   Revision loops at each stage

4. Quality Gates
   Multiple checkpoints ensure quality

5. Flexibility
   Customize rules and templates

═══════════════════════════════════════════════════════════════
```

## Revision Loop Details

### Writer Revision Loop
```
Initial Draft → User Reviews → Provides Feedback → Revised Draft
      ↑                                                    │
      └────────────────────────────────────────────────────┘
                    (Repeats until approved)
```

### LLMON Iteration Loop
```
3 Variations → User Reviews → Edits Rules → New 3 Variations
      ↑                                              │
      └──────────────────────────────────────────────┘
                (Repeats until one selected)
```

### Editor Revision Loop
```
Polished Article → User Reviews → Requests Changes → Updated Article
       ↑                                                     │
       └─────────────────────────────────────────────────────┘
                    (Repeats until approved)
```

## File Flow Diagram

```
INPUT FILES                  PROCESS                    OUTPUT FILES
───────────────────────────────────────────────────────────────────

manual.md          ┐
template.md        ├──► WRITER ──────► 01_writer_draft.md
references.md      │                   01_writer_draft_rev1.md
writer_prompt.md   ┘                   ...

Approved Draft     ┐
llmon_rules.md     ├──► LLMON ───────► 02_llmon_variation1.md
                   ┘                   02_llmon_variation2.md
                                       02_llmon_variation3.md
                                       02_llmon_custom_rules.md
                                       ...

Selected Variation ┐
editor_rules.md    ├──► EDITOR ──────► 03_editor_polished.md
                   ┘                   03_editor_polished_rev1.md
                                       ...
                                       
                                       FINAL_ARTICLE.md ✓
```


