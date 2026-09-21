# Analysis Framework

This file defines the analytical methodology for the personal-insights diagnostic.
Read it after data collection and before producing the diagnostic output.

## Conversation Pattern Classification

For each conversation in the sample, assign scores on five dimensions.
Use a 1-3 scale for each. Do not obsess over precision: the goal is to identify
patterns across the full sample, not to be precise about any single conversation.

### Dimension 1: Initiative Source (who drives the thinking?)

- **3 = User-driven**: User arrives with a hypothesis, a draft, a structured brief,
  or a clear mental model. Claude refines, challenges, or executes.
- **2 = Co-constructed**: User provides direction but the structure or framing
  emerges through dialogue. Both parties shape the output.
- **1 = Claude-driven**: User provides a vague prompt or delegates the framing.
  Claude determines the structure, priorities, and conclusions.

### Dimension 2: Review Rigor (does the user challenge the output?)

- **3 = Active challenge**: User corrects errors, pushes back on framing,
  requests alternatives, or rejects outputs. Visible engagement with substance.
- **2 = Light review**: User makes minor adjustments, accepts with small edits,
  or asks for tweaks that suggest they read the output but did not deeply interrogate it.
- **1 = Pass-through**: User accepts the output as-is, or only comments on
  formatting/cosmetic issues rather than substance.

### Dimension 3: Cognitive Stakes

- **3 = High stakes**: The task involves strategic decisions, client/stakeholder-facing
  content, financial analysis, or anything where getting it wrong has real consequences.
- **2 = Medium stakes**: Professional work that matters but is not make-or-break.
  Internal documents, routine analysis, operational tasks with some judgment involved.
- **1 = Low stakes**: Administrative tasks, formatting, data extraction, personal
  logistics, routine communications.

### Dimension 4: Delegation Depth

- **3 = Full delegation**: User provides input data and expects a finished output.
  No intermediate checkpoints visible in the conversation.
- **2 = Guided delegation**: User provides direction and reviews intermediate outputs.
  Some back-and-forth before accepting final result.
- **1 = Tool-assisted**: User maintains full control of the thinking. Claude is used
  for specific sub-tasks (search, calculation, formatting) within a larger user-driven process.

### Dimension 5: Skill Growth Signal

- **3 = Growing**: User demonstrates new techniques, explores new use cases,
  or explicitly builds reusable workflows (skills, templates, automation).
- **2 = Stable**: User applies established patterns competently. Neither
  expanding nor contracting their usage sophistication.
- **1 = Narrowing**: User repeatedly uses the same patterns, may be stuck in
  a comfort zone, or shows signs of decreasing engagement with the tool's capabilities.

## Pattern Detection Rules

After scoring the sample, look for these composite patterns:

### The Comfort Trap
**Signal**: High scores on Dimension 4 (full delegation) combined with low scores
on Dimension 2 (no review) and high Dimension 3 (high stakes).
**Meaning**: The user is delegating important work without adequate review.
This is the highest-priority risk to flag.

### The Execution Machine
**Signal**: Most conversations score 1 on Dimension 3 (low stakes) and 3 on
Dimension 4 (full delegation).
**Meaning**: The user primarily uses Claude for routine tasks. Not inherently
problematic, but suggests underutilization. The insight is about what's missing.

### The Thinking Partner
**Signal**: High scores on Dimension 1 (user-driven) and Dimension 2 (active challenge),
regardless of Dimension 3 and 4.
**Meaning**: Healthy pattern. The user maintains cognitive ownership. Reinforce this.

### The Creeping Dependency
**Signal**: Temporal trend where Dimension 1 scores decrease (less user initiative)
and Dimension 4 scores increase (more delegation) over time.
**Meaning**: The user is gradually ceding more cognitive ground. May not be aware.
This pattern is subtle and the most valuable to surface.

### The Silo Effect
**Signal**: All conversations cluster in one or two Dimension 3 categories
(e.g., only professional, never personal; or only execution, never reflection).
**Meaning**: The user has a fixed mental model of what Claude is for. Blind spot
analysis should focus on adjacent use cases they're missing.

### The Pseudo-Delegation
**Signal**: High Dimension 1 (user-driven) but the user is asking Claude to
validate decisions already made rather than genuinely seeking input.
**Meaning**: The user uses Claude for confirmation bias, not genuine challenge.
Subtle but worth noting if the pattern is clear.

## Temporal Analysis Method

If sufficient data spans multiple weeks/months:

1. Split the sample into thirds chronologically (early, middle, recent)
2. Compare average dimension scores across the three periods
3. Look for directional trends, not precise measurements
4. A shift of 0.5+ on any dimension across periods is worth noting
5. Stable patterns are also worth noting (positive: "you've maintained X";
   negative: "you've been stuck in Y")

If the sample only covers a short period (< 2 weeks), skip temporal analysis
and state this explicitly rather than forcing conclusions.

## Blind Spot Detection

Compare what the user DOES use Claude for against what their role/context
suggests they COULD use it for:

1. From the role profile in cognitive-risk-profiles.md, list the "Healthy delegation
   zone" activities
2. Compare with observed usage
3. Significant gaps between the two suggest blind spots or underutilization
4. Also look at the inverse: is the user using Claude for things in the "High-risk
   delegation patterns" list without apparent awareness?

## Calibration Notes

- A sample of 10-15 conversations is enough for directional insights.
  Below 10, caveat everything heavily.
- Conversation summaries (from recent_chats) give enough signal for pattern detection.
  Full transcripts are not needed.
- userMemories may reflect the user's self-image more than their actual behavior.
  When memories and observed patterns diverge, trust the observed patterns.
- Not every user needs a wake-up call. If the patterns are healthy, say so clearly
  and focus the output on reinforcement and expansion opportunities.
- The diagnostic should never feel like surveillance. Frame everything as
  "here's what I observe" not "here's what you're doing wrong."
