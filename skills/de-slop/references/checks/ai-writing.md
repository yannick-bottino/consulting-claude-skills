---
type: check
layer: 1-universal
status: active
last-refreshed: 2026-06-10
source: full embed of the humanizer skill (blader/humanizer v2.1.1), based on Wikipedia "Signs of AI writing" (WikiProject AI Cleanup). All 24 patterns plus the soul check. Embedded here, not referenced.
---

# Check: AI writing tells

Detect signs of AI-generated text. Flag each instance with the exact quote and a natural rewrite suggestion. This is layer 1, the same for everyone. Flag and suggest, never rewrite on your own. The mechanical ones (em dashes, AI vocabulary, boldface, Title Case, emojis, curly quotes, filler) bundle into a single "clean the mechanical stuff" item.

Two jobs: catch the 24 patterns below, and make sure what is left has a pulse. Clean but soulless is still slop.

Why these patterns exist: LLMs guess the most statistically likely next words, which drifts toward what applies to the widest variety of cases. Specificity is the antidote in nearly every fix below.

## Content patterns

**1. Significance inflation.** Puffing up importance with claims about legacy and broader trends. Watch: stands/serves as, a testament/reminder, vital/significant/crucial/pivotal/key role or moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted.
Before: "established in 1989, marking a pivotal moment in the evolution of regional statistics."
After: "established in 1989 to collect and publish regional statistics."

**2. Notability name-dropping.** Hammering claims of importance via outlet lists. Watch: independent coverage, cited in [list of outlets], local/regional/national media outlets, written by a leading expert, active social media presence.
Before: "Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu."
After: "In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes."

**3. Superficial -ing analyses.** Present-participle phrases tacked on for fake depth. Watch: highlighting..., underscoring..., emphasizing..., ensuring..., reflecting..., symbolizing..., contributing to..., cultivating..., fostering..., encompassing..., showcasing...
Before: "a palette of blue, green, and gold, reflecting the community's deep connection to the land."
After: "uses blue, green, and gold. The architect said these reference local bluebonnets and the coast."

**4. Promotional language.** Watch: boasts a, vibrant, rich (figurative), profound, enhancing its, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning.
Before: "Nestled within the breathtaking region, the town stands as a vibrant hub with rich heritage."
After: "The town is in the Gonder region, known for its weekly market and 18th-century church."

**5. Vague attributions and weasel words.** Opinions assigned to unnamed authorities. Watch: experts believe/argue, observers have cited, industry reports, some critics argue, several publications, studies show (no named source).
Before: "Experts believe it plays a crucial role in the regional ecosystem."
After: "The river supports several endemic fish species, according to a 2019 Academy of Sciences survey."

**6. Formulaic challenges sections.** Watch: "Despite its... faces several challenges...", "Despite these challenges... continues to thrive," headings like "Challenges and Future Prospects," "Future Outlook."
Before: "Despite these challenges, Korattur continues to thrive as an integral part of the city's growth."
After: "Traffic congestion increased after 2015 when three new IT parks opened."

## Language and grammar patterns

**7. AI vocabulary.** Words that spiked in post-2023 text, they co-occur. Watch: additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant.
Fix: plain equivalents or cut. "Additionally" becomes "also." "Crucial" becomes "important" or nothing.

**8. Copula avoidance.** Elaborate constructions where "is" or "has" would do. Watch: serves as, stands as, marks, represents, boasts, features, offers.
Before: "Gallery 825 serves as the exhibition space and boasts over 3,000 square feet."
After: "Gallery 825 is the exhibition space. It has four rooms totaling 3,000 square feet."

**9. Negative parallelisms.** Watch: "not only X but also Y," "it's not just X, it's Y," "it's not merely X, it's a statement."
Before: "It's not just a song, it's a statement."
After: "The heavy beat adds to the aggressive tone."

**10. Rule of three overuse.** Ideas forced into triplets to look comprehensive.
Before: "Attendees can expect innovation, inspiration, and industry insights."
After: "The event includes talks and panels, with time for informal networking."

**11. Synonym cycling (elegant variation).** Repetition-penalty artifacts.
Before: "The protagonist faces challenges. The main character overcomes obstacles. The central figure triumphs."
After: "The protagonist faces many challenges but eventually triumphs."

**12. False ranges.** "From X to Y" where X and Y are not on a real scale.
Before: "from the singularity of the Big Bang to the enigmatic dance of dark matter."
After: "covers the Big Bang, star formation, and current theories about dark matter."

## Style patterns

**13. Em dashes.** The hard one for us: no em dashes at all, anywhere. Use commas, periods, or restructure.

**14. Boldface overuse.** Mechanically bolded terms mid-prose. Fix: remove the bolding.

**15. Inline-header lists.** "**Thing:** sentence about the thing" bullets. Fix: convert to prose or a clean list without the bolded label.

**16. Title Case in headings.** Every main word capitalized. Fix: sentence case.

**17. Emojis decorating headings or bullets.** Fix: remove them. (Channel exceptions live in the Voice check, not here.)

**18. Curly quotes.** Fix: straight quotes.

## Communication patterns

**19. Chatbot artifacts.** Correspondence pasted as content. Watch: "I hope this helps," "let me know if," "here is a/an...," "of course!," "certainly!," "would you like me to..."
Fix: remove entirely.

**20. Knowledge-cutoff disclaimers.** Watch: "as of my last update," "while specific details are limited in available sources," "based on available information."
Fix: find the fact or cut the sentence.

**21. Sycophantic tone.** Watch: "great question," "you're absolutely right," "excellent point."
Fix: respond directly to the substance.

## Filler and hedging

**22. Filler phrases.** "In order to" → "to." "Due to the fact that" → "because." "At this point in time" → "now." "In the event that" → "if." "Has the ability to" → "can." "It is important to note that" → delete.

**23. Excessive hedging.** Stacked qualifiers. "Could potentially possibly be argued that the policy might" → "The policy may."

**24. Generic positive conclusions.** Watch: "the future looks bright," "exciting times lie ahead," "a major step in the right direction," "journey toward excellence."
Fix: a specific plan or fact, or cut.

## The pulse check (soul)

Removing patterns is half the job. Also flag writing that is technically clean but dead. Signs: every sentence the same length and structure, no opinions (neutral reporting only), no acknowledgment of uncertainty or mixed feelings, no first person where it fits, no humor or edge, reads like a press release.

What gives writing a pulse: real opinions and reactions, varied rhythm (short punch, then a longer sentence that takes its time), acknowledged complexity ("impressive but also kind of unsettling"), first person where honest, a little mess (an aside, a tangent), specific feelings instead of generic ones. Grade dead-but-clean writing as Drift and suggest where to inject an opinion, varied rhythm, or a specific reaction.

## Grading

- Aligned: none of patterns 1 to 24, and it has a pulse.
- Drift: a few soft tells (a stray "additionally," one rule-of-three), or clean but soulless. No hard guardrail break.
- Misaligned: any em dash, AI-vocabulary cluster, chatbot artifact, knowledge-cutoff disclaimer, or sycophancy in something about to ship.
