---
name: personal-insights
description: >
  Analyse les patterns d'utilisation de Claude via l'historique des conversations, la memoire native et les memoires de projets. Pipeline sequentiel en 3 phases : (1) Diagnostic cognitif structure (forces, faiblesses, biais de delegation, risques d'atrophie) ; (2) Hot Seat interactif ou Claude pose des questions provocantes adaptees aux findings via AskUserQuestions ; (3) Plan d'action correctif + ajustements de system prompt enrichis par les reponses du Hot Seat. Declencher des qu'un utilisateur demande "/insights", "analyse mon utilisation", "mes patterns", "diagnostic cognitif", "suis-je trop dependant", "audit de mon usage", "blind spots", "AI dependency check", "personal insights", "bilan", "hot seat", "challenge me", "sois brutal", "trusted advisor", "pose-moi des questions difficiles", ou toute demande d'introspection sur sa facon d'utiliser Claude. Meme un simple "bilan" en contexte peut declencher ce skill.
---

# Personal Insights

## Purpose

This skill produces a structured cognitive diagnostic of how a person uses Claude.
It goes beyond usage statistics to analyze the *quality* of the human-AI collaboration:
delegation patterns, cognitive autonomy signals, blind spots, and evolution over time.

The output is not a report card. It is a mirror designed to help the user become more
intentional about what they delegate, what they keep, and how their AI usage shapes
their thinking over time.

## Execution Flow

The skill runs as a single sequential pipeline in three phases.
All three phases execute in the same conversation, without interruption.

### Phase 1: Data Collection + Diagnostic (sections 1-6)
Collect data from all memory layers, score conversations, detect patterns,
and produce diagnostic sections 1 through 6. Deliver this analysis to the user
as a written debrief. Do NOT include the corrective action plan yet.

### Phase 2: Hot Seat (interactive Q&A)
Immediately after delivering the diagnostic, transition into an interactive
Q&A session. The questions are selected and customized based on the specific
findings from Phase 1. Use the `ask_user_input_v0` tool to present questions.

**Hot Seat Protocol:**

1. Read `references/hot-seat-questions.md` for the question bank.
2. Based on Phase 1 findings, select 12-15 questions organized in three layers:
   - **Layer A (Q1-Q5) : Surface patterns.** Probe the most visible findings from
     the diagnostic. These warm up the user and establish the contract of honesty.
   - **Layer B (Q6-Q10) : Contradictions.** Cross-reference Layer A answers with
     observed behavior. "Tu as dit X en Q2, mais dans ta conversation du [date]
     tu as fait Y." These questions test whether the user's self-image matches reality.
   - **Layer C (Q11-Q15) : Deep structure.** Probe identity, values, and long-term
     trajectory. What kind of professional is the user becoming? What is the
     relationship between their AI usage and their ambitions? These are the
     questions that stay with the user after the session.
   Every question must reference specific patterns or examples from the data.
   Do NOT use generic questions.
3. Present questions using `ask_user_input_v0`. For each question, provide 3-4
   response options that represent genuinely different postures (not just
   agree/disagree). Include options that are honest/uncomfortable alongside
   comfortable ones. The options should be designed to reveal something about
   the user's self-awareness.
4. After each answer, deliver a candid reaction (2-4 sentences max) that either
   validates, challenges, or reframes. Then present the next question.
5. Layer B questions MUST reference specific Layer A answers. This creates a
   feeling of progressive depth, not just a list of unrelated questions.
6. After all questions, move to Phase 3.

**Question design for ask_user_input_v0:**
- The question text should be direct and personal ("Tu as co-construit le
  chiffrage Latour avec moi. Si un associe te challenge sur une ligne,
  tu reponds de tete ?")
- Options should NOT be yes/no. They should expose different levels of
  self-awareness or different strategic postures. Example:
  - "Oui, je maitrise chaque ligne"
  - "Globalement oui, mais pas le detail jour par jour"
  - "Honnetement, je devrais relire nos echanges avant"
  - "Je n'y avais pas pense"
- Never present more than 2 questions per `ask_user_input_v0` call. The rhythm
  should be: question > answer > reaction > question > answer > reaction.
  Do not stack all questions at once.

**Hot Seat tone rules:**
- No preamble. No "great question" or "that's interesting." Just the reaction.
- If the user picks the comfortable/evasive option, call it out directly.
  "Tu choisis la reponse rassurante. Mais dans la conversation du [date],
  tu as fait exactement l'inverse de ce que tu viens de dire."
- If the user picks the honest/vulnerable option, acknowledge briefly and
  move on. Do not over-praise.
- Use the user's own words and examples from their history to ground the challenge.
- Keep each exchange tight. The value is in accumulation, not monologues.

### Phase 3: Synthesis + Corrective Action Plan
After the Hot Seat, produce the final section 7 (Corrective Action Plan).
This plan is now informed by BOTH the diagnostic analysis AND the user's
own answers during the Hot Seat. Reference specific Hot Seat moments.

The synthesis should:
- Connect dots across Hot Seat answers ("Tu as dit X en Q2 mais ton choix
  en Q4 montre le contraire")
- Name gaps between stated awareness and observed behavior
- Produce the behavioral recommendations AND system prompt corrections
  as defined in section 7 of the diagnostic framework

## Data Collection Phase

Before any analysis, gather data from all three available memory layers.
Execute these steps in order, adapting to what is available in the current context.

### Layer 1: Native Memory (userMemories)

The userMemories block is already in context. Extract from it:
- Professional role, seniority, domain
- Known preferences, constraints, recurring topics
- Any stated self-awareness about AI usage patterns

### Layer 2: Conversation History

Run the following data collection sequence:

1. `recent_chats` with n=20, sort_order=desc (most recent conversations)
2. `recent_chats` with n=20, sort_order=asc (oldest available conversations)
3. Based on themes found in Layer 1, run 3-5 targeted `conversation_search` queries
   to fill gaps. Good queries target: the user's core work domain, personal/life topics,
   creative or strategic tasks, and any area where delegation risk is highest.

For each conversation retrieved, classify it along these dimensions:
- **Task type**: execution (formatting, code, data) | analysis (research, synthesis) |
  reflection (strategy, decision-making, opinion) | creation (writing, design, ideation)
- **Delegation depth**: full (user gives input, accepts output) | collaborative
  (user provides draft, iterates with Claude) | supervised (user drives, Claude assists)
- **Cognitive load retained by user**: high (user makes key decisions, challenges output) |
  medium (user reviews and adjusts) | low (user accepts with minimal review)
- **Domain**: professional | personal | mixed

### Layer 3: Project Memories

If the user is inside a project, the project's memory and instructions are in context.
Extract any patterns specific to that project scope.

If the user is outside projects, note this and focus on Layers 1 and 2.

## Analysis Framework

After data collection, apply the framework defined in `references/analysis-framework.md`.
Read that file before proceeding.

The analysis produces seven diagnostic sections:

### 1. Usage Profile
A factual summary: what the user uses Claude for, how often, across which domains.
No judgment here, just the map.

### 2. Delegation Pattern Analysis
Where the user falls on the delegation spectrum for each task type.
The key question is not "how much" but "what kind" of work is being delegated.

Healthy delegation: execution, formatting, data processing, first-draft generation,
research synthesis.

Watch zone: strategic framing, client communication tone, financial modeling assumptions,
decision rationale construction.

Risk zone: accepting strategic recommendations without challenge, delegating opinion
formation, outsourcing the "thinking before the doing."

### 3. Cognitive Autonomy Signals
Positive signals to identify and reinforce:
- User arrives with their own draft or hypothesis before asking for help
- User challenges or corrects Claude's output
- User makes course corrections mid-conversation
- User explicitly separates "help me think" from "help me execute"
- User asks Claude to play devil's advocate rather than validate

Negative signals to flag:
- Repeated pattern of empty prompts ("do X for me") without context or constraints
- Accepting first output without iteration
- Delegating communication that carries relational stakes (emails to boss, client tensions)
- Asking Claude to form opinions the user should form themselves
- Increasing delegation depth over time without corresponding increase in review rigor

### 4. Role-Based Risk Profile
Read `references/cognitive-risk-profiles.md` for role-specific risk matrices.
Match the user's profile to the closest archetype and apply the corresponding risk lens.

The risk is not the same for a consultant, a CFO, a creative director, or a founder.
A consultant who delegates slide content loses client credibility differently than a
CFO who delegates financial model assumptions.

### 5. Blind Spot Analysis
Identify what the user is NOT doing with Claude that they could be, given their role
and context. Sometimes the most important insight is about underutilization, not
over-delegation.

Also identify topics or domains where the user might be over-confident in Claude's
output (e.g., legal, medical, financial advice) without appropriate verification.

### 6. Temporal Evolution
Compare early conversations to recent ones. Look for:
- Increasing sophistication in prompting (positive)
- Increasing delegation without increasing review (risk)
- Narrowing of use cases over time (missed opportunity)
- Growing reliance for emotional or relational support (boundary concern)

If not enough historical data is available, state this clearly rather than speculating.

### 7. Corrective Action Plan
This section must produce three concrete outputs, informed by both the diagnostic
analysis AND the Hot Seat answers. Reference specific Hot Seat moments.

**A. Contrat Cognitif (global posture)**
Before any task-specific corrections, define the user's overall cognitive contract
with Claude. This is a meta-rule that governs ALL interactions, not specific use cases.
It should answer: "What is the fundamental relationship between this user's thinking
and Claude's output?" Format it as a single paragraph (max 5 sentences) that the
user can paste at the top of their system prompt as a governing principle.

The Contrat Cognitif should be personalized based on the user's specific risk profile.
For example, a user who over-delegates strategic framing needs a different contract
than one who under-utilizes Claude for research. The contract should name the user's
core cognitive value (what they MUST protect) and the boundary rule (what Claude should
always check before proceeding).

**B. Behavioral recommendations (5-8, structured by horizon)**
Organize recommendations in three tiers:

*Immediate (this week):* 1-2 micro-habits that require zero setup. Things the user
can do starting with their next conversation. Each must include a concrete trigger
("when X happens, do Y") and a success indicator ("you'll know it works when Z").

*Short-term (this month):* 2-3 structural changes to the user's workflow. These
require some setup (creating a new routine, modifying a process, having a conversation
with a colleague). Each must include: what to do, why it matters (tied to a specific
diagnostic finding), what success looks like, and what failure looks like (so the
user can self-diagnose if the change is not working).

*Medium-term (next quarter):* 2-3 strategic shifts that change the nature of
the user's relationship with Claude. These might involve team dynamics, skill
transfer, new use cases to explore, or use cases to deliberately stop using
Claude for. Each must include a "what good looks like" description and a
"what to watch for" warning sign.

Every recommendation must be:
- Specific and actionable (not "be more careful" but "before sending any
  client-facing email drafted by Claude, read it aloud and ask: would I have
  written this myself?")
- Tied to a specific pattern identified in the analysis or a specific Hot Seat answer
- Include a concrete success indicator

**C. System prompt / preferences corrections**
Produce two levels of corrections:

*Level 1: Contrat Cognitif* (the global posture paragraph from section A above,
formatted as a copy-paste block for the top of the user's system prompt).

*Level 2: Task-specific guardrails* (4-6 specific rules for the task types
where the diagnostic identified the highest risk). Each guardrail must:
- Name the task type it applies to
- Describe what Claude should do differently (ask a question, refuse to proceed,
  present alternatives, request the user's input first)
- Explain why (tied to a specific finding)

Format all corrections as copy-paste-ready text blocks the user can add to their
preferences. Use the user's language and register.

## Output Format

### Phase 1 Output (Diagnostic)
Structure the output as a conversation, not a formal report. Use direct, honest language.
No hedging, no flattery. The user is asking for a mirror, not a compliment.

Use plain text with minimal formatting. No bullet-point walls. Write in the language
the user communicates in (detect from conversation history and current context).

Start with the most important finding, not with a preamble.

Deliver sections 1-6. End by transitioning to the Hot Seat:
"Voila pour le diagnostic. Maintenant, quelques questions pour aller plus loin."
Then immediately call `ask_user_input_v0` with the first Hot Seat question(s).

### Phase 2 Output (Hot Seat)
Each cycle: question via `ask_user_input_v0` > user answers > candid reaction
(2-4 sentences) > next question via `ask_user_input_v0`.

No filler between cycles. No recaps mid-session. Just the rhythm of
question-answer-reaction.

### Phase 3 Output (Synthesis + Action Plan)
After the last Hot Seat reaction, deliver the synthesis and corrective action plan.

The synthesis should connect dots across the diagnostic AND the Hot Seat answers.
Reference specific moments: "Tu as admis en Q3 que tu ne relis pas les CRs en détail.
Voici un ajustement de system prompt pour ça."

The corrective action plan follows the enriched format defined in section 7:
1. Contrat Cognitif (global posture, 1 paragraph)
2. Behavioral recommendations (5-8, structured by horizon: immediate/short/medium)
3. System prompt corrections (Level 1 global + Level 2 task-specific guardrails)

## Important Constraints

- **Language and orthography**: All output must be in the user's language with
  complete orthography including accents, cedillas, and diacritics. For French:
  é, è, ê, ë, à, â, ù, û, ô, î, ï, ç are mandatory. Writing "memoire" instead
  of "mémoire" or "delegue" instead of "délégué" is a quality failure.
- Never invent patterns that are not supported by observed data. If the sample is too
  small to draw a conclusion, say so.
- Do not assume the user's emotional state from their usage patterns. Stick to
  behavioral observations.
- The diagnostic should be useful even with limited data (10-15 conversations).
  Adapt depth to available evidence.
- Be direct but not brutal for the sake of being brutal. The goal is to help,
  not to perform toughness.
- Never use this analysis to encourage the user to use Claude less overall.
  The goal is smarter usage, not less usage.
- Respect the user's stated preferences (e.g., no em-dashes) in the output.
