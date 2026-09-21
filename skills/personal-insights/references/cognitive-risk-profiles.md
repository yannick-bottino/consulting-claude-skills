# Cognitive Risk Profiles by Role

This file maps professional archetypes within a consulting firm to their specific
AI delegation risks. The skill should match the user to the closest profile and
apply the corresponding risk lens. Users may straddle two profiles (e.g., a Manager
who still delivers consultant-level work).

These profiles are calibrated for strategy, data, and AI consulting firms.
They can be adapted to other professional services contexts.

## How to Use This File

1. Identify the user's role from userMemories or conversation history
2. Find the closest archetype(s) below
3. Apply the "Critical cognitive muscles" and "High-risk delegation patterns" as
   the lens for Section 4 of the diagnostic
4. Use the "Healthy delegation zone" to validate what the user is doing well
5. If the user straddles two profiles, apply both and note the tension

---

## Consultant Strategy / Marketing

**Typical scope**: Client-facing analyses, market studies, competitive benchmarks,
brand strategies, campaign performance reviews, pitch decks, client workshops.

**Core cognitive value**: Ability to translate data and market signals into
client-specific strategic recommendations. The client pays for judgment, not for slides.

**Critical cognitive muscles at risk**:
- **Strategic framing**: The ability to look at a messy client situation and
  decide what the real question is. If Claude frames the problem, the consultant
  loses the skill that differentiates them from a template.
- **Client empathy**: Knowing what will land with THIS client, what their internal
  politics require, what language their CEO responds to. Claude cannot have this.
- **Storyline construction**: A deck tells a story. Delegating slide-by-slide
  content produces locally coherent slides that can lack a strategic arc.
- **Synthesis under ambiguity**: Clients rarely provide clean briefs. The ability
  to produce structured output from unstructured input is a core muscle.

**High-risk delegation patterns**:
- Asking Claude to write the "so what" or recommendation of a slide
- Delegating executive summaries or key takeaways without forming the view first
- Using Claude to produce client emails where subtext matters more than text
- Accepting market research synthesis without reading primary sources
- Having Claude build the storyline of a pitch instead of sketching it by hand first

**Healthy delegation zone**:
- Data gathering, benchmark compilation, competitive landscape research
- First-draft slides when the consultant has defined the structure and key messages
- Formatting, template application, chart generation
- Meeting notes and internal communications
- Proofreading and language polishing (especially in non-native languages)

**Structural countermeasures for system prompt**:
- "For client-facing content, ask me for my key message before drafting anything"
- "Present 2-3 framing options for any strategic question before developing one"
- "Never write a recommendation section without me stating my hypothesis first"

---

## Consultant Data / IA

**Typical scope**: Data pipelines, dashboards, ML models, AI integration,
technical architecture, data quality audits, analytics deliverables, prompt
engineering, tool evaluation.

**Core cognitive value**: Bridging the gap between business questions and
technical implementation. The value is not in writing code but in knowing
which code to write and why.

**Critical cognitive muscles at risk**:
- **Debugging intuition**: The pattern-matching from having personally traced
  bugs. Copy-pasting AI-generated fixes skips the learning loop.
- **Architecture judgment**: Understanding WHY a system should be designed a
  certain way requires grappling with constraints, not generating options.
- **Code ownership**: If a consultant cannot explain every line of code they
  deliver to a client, the engagement becomes fragile.
- **Tool evaluation independence**: A data/AI consultant who uses Claude to
  evaluate AI tools has a circularity problem. Independent judgment matters.

**High-risk delegation patterns**:
- Accepting generated code without reading and understanding every line
- Delegating technical architecture decisions
- Using AI to debug without first forming a hypothesis about the root cause
- Generating tests without understanding what they verify
- Letting Claude choose libraries, frameworks, or approaches without independent evaluation
- Delivering AI-generated analyses to clients without manually verifying key outputs

**Healthy delegation zone**:
- Boilerplate code, repetitive patterns, migrations, formatting
- Documentation generation
- Research on libraries, APIs, and best practices
- Data processing and transformation scripts
- Refactoring suggestions (with manual review)
- Prototype/POC generation that will be rewritten for production

**Structural countermeasures for system prompt**:
- "When I paste an error, ask me what I think the cause is before suggesting a fix"
- "For any code you generate, explain WHY this approach, not just WHAT it does"
- "Never generate more than 50 lines without me reviewing first"
- "If I ask you to evaluate a tool or approach, give me the evaluation criteria
  first and let me score it myself before you weigh in"

---

## Manager

**Typical scope**: Leading 1-3 engagements simultaneously, supervising 2-5
consultants, contributing to proposals, starting to develop client relationships,
ensuring delivery quality, coaching junior team members.

**Core cognitive value**: Quality control, team orchestration, and the bridge
between consultant execution and director-level strategy. The Manager is the
guarantor that what goes out the door is solid.

**Critical cognitive muscles at risk**:
- **Quality judgment**: The Manager's review is the last line of defense before
  the client sees a deliverable. If the Manager uses AI to produce content that
  they then review less rigorously because "it looks polished," quality drops.
- **Coaching instinct**: Using AI to fix a junior's work instead of coaching
  them through the fix deprives both the junior and the Manager of a learning moment.
- **Scope management**: The ability to say "this is out of scope" or "this
  doesn't answer the client's question" requires deep engagement with the problem.
  AI-assisted production can create a "more is better" trap.
- **Proposal writing**: Proposals are where a Manager learns to sell. Delegating
  them too early stunts commercial development.

**High-risk delegation patterns**:
- Using Claude to rework a consultant's deliverable instead of coaching the
  consultant to improve it themselves
- Delegating proposal writing without having personally structured the argument
- Using AI to review other AI-generated content (the review loop becomes circular)
- Producing more polished content than the team would naturally produce, creating
  unsustainable quality expectations
- Sending AI-generated client communications without personalizing them

**Healthy delegation zone**:
- Meeting summaries and internal reporting
- Data analysis and research to feed into consultant work
- First drafts of internal documents (staffing, project plans, status updates)
- Formatting and template application for team deliverables
- Brainstorming structures for workshops or proposals

**Structural countermeasures for system prompt**:
- "When I paste a junior's work for improvement, ask me: should I coach them
  or fix it myself? If coaching, give me talking points, not a rewrite."
- "For proposals, ask me for the win strategy before drafting any content"
- "If I'm producing content that a consultant on my team should be producing,
  flag it and ask if this is a delegation opportunity"

---

## Directeur

**Typical scope**: P&L responsibility on a portfolio of clients, managing
Managers, senior client relationships, business development, methodological
innovation, firm-level strategy input.

**Core cognitive value**: Pattern recognition across engagements, ability to
connect client problems to firm capabilities, commercial judgment, and the
authority that comes from deep domain expertise.

**Critical cognitive muscles at risk**:
- **Cross-engagement pattern recognition**: Seeing that Client A's problem
  is similar to what worked for Client B requires being close to the work.
  If AI mediates all information, this cross-pollination weakens.
- **Commercial instinct**: Knowing when to push for an upsell, when to absorb
  a loss, when a client is testing you. This is experiential, not analytical.
- **Domain authority**: The Directeur's credibility comes from deep expertise.
  If AI produces their thought leadership content, the expertise becomes performative.
- **People development**: Knowing which Manager is ready for more responsibility
  requires direct observation, not AI-mediated assessment.

**High-risk delegation patterns**:
- Having Claude produce thought leadership pieces without personal intellectual investment
- Using AI summaries of engagement status instead of reading the actual deliverables
- Delegating client communication on sensitive topics (fee negotiations, scope disputes,
  team changes)
- Producing commercial proposals without personally understanding the client's business context
- Using AI to prepare for client meetings instead of reading the materials

**Healthy delegation zone**:
- Research and market intelligence for business development
- Internal reporting and firm-level documentation
- Analysis and data preparation for strategic decisions
- Presentation drafting when the Directeur has defined the narrative
- Administrative tasks, scheduling, and logistics coordination

**Structural countermeasures for system prompt**:
- "For any client-facing document, ask me what I want the client to DO after reading it"
- "For thought leadership content, interview me with tough questions before writing anything"
- "If I ask you to summarize an engagement's status, push back and ask me to read
  the latest deliverable instead"

---

## Partner

**Typical scope**: Firm strategy, key account management, P&L accountability,
new practice development, external visibility (conferences, publications, media),
hiring decisions, culture stewardship.

**Core cognitive value**: Vision, network, reputation, and the ability to
make high-stakes decisions with incomplete information. The Partner IS the
firm's intellectual capital in the market.

**Critical cognitive muscles at risk**:
- **Vision articulation**: If Claude helps articulate the firm's strategic
  direction, whose vision is it? The Partner must own the narrative.
- **Relationship depth**: Key client relationships are personal. AI-mediated
  communication erodes the authentic connection that generates trust and loyalty.
- **Hiring judgment**: Evaluating people requires human-to-human interaction.
  AI can assist with process, never with judgment.
- **Intellectual credibility**: A Partner who publishes AI-generated content
  risks credibility when pressed on details in live settings.

**High-risk delegation patterns**:
- Having Claude draft keynote speeches or conference presentations without
  deep personal engagement with the content
- Using AI for client relationship management communications
- Delegating strategic planning documents without personally wrestling with
  the hard choices
- Producing publications that the Partner cannot defend extemporaneously
- Using AI to prepare for board or partner meetings instead of thinking through
  the issues independently

**Healthy delegation zone**:
- Research and intelligence briefings before client or industry events
- Internal communications and operational updates
- Data analysis to support strategic decisions
- Administrative coordination and logistics
- Draft preparation that the Partner will substantially rewrite

**Structural countermeasures for system prompt**:
- "For any content published under my name, I must be able to defend every
  claim in a live Q&A. Flag anything I haven't personally validated."
- "For strategic decisions, play devil's advocate. Never agree with me too quickly."
- "Never draft a client email for a key account. At most, suggest talking points
  that I will write from."

---

## Fonctions Support (RH, Finance, Admin, Ops)

**Typical scope**: Recruitment, payroll, financial reporting, office management,
contract administration, internal tooling, compliance, event coordination.

**Core cognitive value**: Operational reliability, process rigor, institutional
knowledge about how things actually work, and the human touch in employee-facing
interactions.

**Critical cognitive muscles at risk**:
- **Process mastery**: Knowing why each step in a process exists (regulatory,
  historical, practical) is essential to adapt it intelligently. If AI handles
  the process, the understanding fades.
- **Interpersonal sensitivity**: HR communications, employee relations, and
  internal support require emotional intelligence. AI-generated responses can
  feel corporate and impersonal.
- **Institutional memory**: Support functions hold knowledge about why things
  are done a certain way. Over-automating can erase this context.
- **Compliance awareness**: Knowing when a seemingly simple request has
  regulatory implications requires active engagement, not autopilot.

**High-risk delegation patterns**:
- Using AI to draft sensitive HR communications (terminations, conflict resolution,
  performance issues) without heavy personalization
- Automating compliance-related documentation without expert review
- Delegating financial reporting without verifying calculations
- Using AI for employee-facing communications that require empathy and nuance
- Accepting AI-generated contract language without legal review

**Healthy delegation zone**:
- Template creation and standardization of recurring documents
- Data entry, consolidation, and reporting
- Research on regulations, best practices, and benchmarks
- Internal communication drafts for non-sensitive topics
- Process documentation and procedure manuals
- Event coordination and logistics planning

**Structural countermeasures for system prompt**:
- "For any employee-facing communication, ask me about the specific person's
  context before drafting"
- "For compliance-related documents, always flag which regulatory framework applies
  and recommend expert review"
- "Never produce a final version of a contract or legal document. Always mark as DRAFT."
