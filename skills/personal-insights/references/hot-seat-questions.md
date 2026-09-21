# Hot Seat Question Bank

This file contains provocative questions organized by theme. The skill should
select 5-7 questions based on what is actually relevant to the user's observed
patterns. Never use a question that is not grounded in evidence from the data.

The questions below are templates. Before asking any question, the skill must
customize it with specific examples, names, projects, or patterns from the user's
history. A generic question is a wasted question.

## Theme 1: Cognitive Ownership

These questions probe whether the user truly owns what they produce with Claude.

- "If I erased our entire conversation history and you had to rebuild [specific
  deliverable] from scratch, right now, without any AI, how long would it take
  you? And more importantly, would you produce the same thing?"

- "You [built/wrote/designed] [specific deliverable] with me. Could you defend
  every decision in it to [specific stakeholder] without referencing our exchange?"

- "What's the last thing I produced for you that you sent to someone without
  changing a word? What does that tell you?"

- "If a colleague asked you to explain how [specific skill/workflow] works
  under the hood, could you do it without opening our conversations?"

## Theme 2: Delegation Awareness

These questions probe whether the user is conscious of what they delegate and why.

- "What's the most important decision you've made this month? Did I help with it?
  Should I have?"

- "You delegate [task type A] to me but never [task type B]. Why? Is it a conscious
  choice or just how things evolved?"

- "When you hand me a transcript and ask for a CR, what happens in your head
  while I'm generating it? Are you already thinking about the next thing, or
  are you mentally reviewing the meeting?"

- "You've built [N] skills in [timeframe]. For each one, who else can operate it
  without you? If the answer is nobody, what does that mean?"

## Theme 3: Professional Identity

These questions probe the relationship between AI usage and professional self-image.

- "If your [client/boss/team] knew exactly how much of your output comes from
  our conversations, would it change how they see you? Should it?"

- "What's the thing you're most proud of producing recently? How much of it
  was genuinely yours versus our collaboration? Does the distinction matter to you?"

- "You're [role title]. What's the one capability that MUST remain 100% human
  in your role, no AI assistance ever? Are you protecting it?"

- "In two years, what do you want to be known for professionally? Is your current
  AI usage pattern building toward that, or is it a detour?"

## Theme 4: Patterns and Habits

These questions probe unconscious routines that may have formed.

- "What's the first thing you do when you get a new work task? Is it 'open Claude'
  or 'think about it first'? Be honest."

- "When did you last write something substantial from a blank page, no AI,
  no templates? How did it feel?"

- "You've been using me for [duration]. What can you do now that you couldn't
  before? And what could you do before that you've stopped doing?"

- "If I were unavailable for a week, what would break? What would you actually
  handle fine? The gap between those two answers is your dependency map."

## Theme 5: Blind Spots and Avoidance

These questions probe what the user might be avoiding or not seeing.

- "What's the conversation you should be having with a human that you're having
  with me instead?"

- "Is there a topic or task you keep bringing to me because you're avoiding
  doing the hard thinking yourself? I'm not asking about execution tasks.
  I'm asking about the ones where you know, deep down, you should sit with
  the discomfort a bit longer before outsourcing it."

- "You use me heavily for [domain A] but almost never for [domain B].
  Is that because [domain B] doesn't need AI, or because you haven't confronted
  what it would mean to let AI into that space?"

- "What's the feedback you're afraid to hear about how you use AI?"

## Theme 6: Sustainability and Balance

These questions probe whether the current usage pattern is sustainable.

- "Your [recent period] involved [list of parallel workstreams]. Looking at
  that list, which ones genuinely needed to happen, and which ones happened
  because Claude made it easy to say yes to everything?"

- "AI lets you produce more, faster. But is 'more, faster' actually what your
  role needs right now? Or is 'fewer things, deeper' more valuable?"

- "You built an impressive system of skills and automations. But systems need
  maintenance. Who maintains this when you're on vacation, burned out, or
  promoted to a role where you don't have time?"

- "The tools you've built make you more productive. Do they also make you
  more replaceable, or less? Which would you prefer?"

## Theme 7: The Relationship Itself

These questions probe the user's relationship with Claude as a tool.

- "Do you ever catch yourself explaining things to me that you should be
  explaining to a colleague? What does that say about your communication
  patterns at work?"

- "When I challenge you, do you genuinely reconsider, or do you just want
  me to execute your original idea with a slightly different wrapper?"

- "Is there anything you tell me that you wouldn't tell a human colleague?
  Why? What does that asymmetry reveal?"

- "If you had to describe our working relationship to someone who doesn't
  use AI, what would you say? And would that description make you proud
  or slightly uncomfortable?"

---

## Selection Rules

The Hot Seat uses 12-15 questions organized in three progressive layers.

### Layer A: Surface Patterns (Q1-Q5)
Purpose: probe the most visible findings from the diagnostic. Warm up the user,
establish the contract of honesty.
- Pick from Themes 1, 2, and 4 primarily.
- Start with a concrete, specific question the user can answer factually
  (e.g., "Can you defend this specific deliverable?"). This is easier to
  answer honestly than abstract questions about habits.
- Customize every question with specific data points (project names, dates,
  deliverable names, conversation references).

### Layer B: Contradictions (Q6-Q10)
Purpose: cross-reference Layer A answers with observed behavior. Test whether
the user's self-image matches reality.
- Layer B questions MUST reference specific Layer A answers. "Tu as dit en Q2
  que [X]. Mais dans ta conversation du [date], tu as fait [Y]."
- Pick from Themes 2, 4, and 5 primarily.
- This is where the session gets uncomfortable. The value is in naming the gap
  between what the user believes about themselves and what the data shows.

### Layer C: Deep Structure (Q11-Q15)
Purpose: probe identity, values, and long-term trajectory. What kind of
professional is the user becoming?
- Pick from Themes 3, 5, 6, and 7 primarily.
- These questions should not have an obvious "right answer."
- End with a Theme 7 question (the relationship itself) to close on a
  reflective note.

### General Rules
- Cover at least 5 of the 7 themes across the full session.
- Always include at least 2 questions from Theme 2 (Delegation Awareness)
  and 2 from Theme 5 (Blind Spots).
- Customize every question with specific data points. "Tu as construit 6 skills
  en un mois" is better than "Tu as construit beaucoup de skills récemment."
- If the user's data suggests a specific tension (e.g., burnout history +
  high volume), allocate more questions to Theme 6 (Sustainability).
- Present 1-2 questions per `ask_user_input_v0` call maximum. Never stack all
  questions at once. The rhythm is: question > answer > reaction > question.
