---
type: check
layer: 1-universal
status: active
last-refreshed: 2026-06-18
source: the stop-ai-slop skill (structures.md). Anti-patterns structurels recurrents dans la prose generee par IA. Couvre FR et EN.
---

# Check: structural tells

Detect structural anti-patterns that betray AI-generated prose. These are not word-level tells (covered by the AI writing check) but sentence- and paragraph-level patterns that create a formulaic, predictable rhythm. Flag each instance with the exact quote and suggest the fix. FR and EN.

## Patterns

**1. Binary contrasts.** "Not X. It's Y." Artificial tension manufactured for impact.

Before: "Ce n'est pas un probleme de budget. C'est un probleme de priorites."
After: "Le budget est suffisant. La direction n'a pas encore arbitre."

Before: "This isn't about tools. It's about culture."
After: "Culture determines whether tools get adopted."

Fix: state Y directly. Remove the negation of X.

**2. Negative lists.** Listing what something is not before saying what it is.

Before: "Ce dispositif n'est pas un audit. Ce n'est pas un benchmark. Ce n'est pas une etude de marche. C'est un diagnostic operationnel qui..."
After: "Ce dispositif est un diagnostic operationnel qui..."

Fix: go straight to the positive definition.

**3. Dramatic fragmentation.** Very. Short. Sentences. For. Impact.

Before: "Le marche change. Vite. Trop vite pour les acteurs etablis."
After: "Le marche change plus vite que les acteurs etablis ne peuvent s'adapter."

Before: "The data is clear. Unambiguous. Undeniable."
After: "The data leaves no room for interpretation."

Fix: integrate into a normal sentence. Varied rhythm builds across the whole text, not through local fragmentation.

**4. Rhetorical setups.** Posing a rhetorical question before immediately answering it.

Before: "Pourquoi cette approche fonctionne-t-elle ? Parce qu'elle part du terrain."
After: "Cette approche fonctionne parce qu'elle part du terrain."

Before: "What makes this different? Three things: speed, trust, and data."
After: "Speed, trust, and data set this apart."

Fix: remove the question. The answer is enough.

**5. False agency.** Inanimate objects performing human actions.

Before: "L'analyse revele trois leviers."
After: "Trois leviers ressortent de l'analyse."

Before: "Les donnees suggerent un changement de cap."
After: "Les equipes terrain identifient un changement de cap."

Before: "Ce rapport propose de restructurer l'organisation."
After: "Nous recommandons de restructurer l'organisation."

Fix: name the person or team acting. Restructure the sentence around a human subject.

**6. Distant narrator voice.** Writing about "organizations", "teams", "leaders" from afar.

Before: "Les entreprises qui reussissent leur transformation adoptent une approche progressive."
After: "Si vous structurez la transformation en phases, chaque etape produit des resultats mesurables avant d'engager la suivante."

Before: "Leaders who navigate complexity tend to rely on structured frameworks."
After: "When you face competing priorities, a structured framework cuts decision time in half."

Fix: "vous" / "you" beats "les organisations" / "leaders". Address the reader directly.

**7. Formulaic bullets.** Every bullet starts with a bold noun followed by a colon.

Before:
- **Efficacite :** reduction des delais de traitement
- **Qualite :** amelioration du taux de conformite
- **Cout :** diminution de 15% des charges

After:
- Les delais de traitement reculent de X jours
- Le taux de conformite atteint Y%
- Les charges baissent de 15%

Fix: each bullet is an action sentence with a verb. Remove the bold label + colon. Rewrite in prose if three items or fewer.

**8. Punchy one-liner endings.** Every paragraph ends with a short, high-impact sentence.

Before: "Nous avons analyse les trois scenarios en detail. Le premier presente des risques d'execution eleves. Le second necessite une refonte organisationnelle majeure. **Le troisieme change la donne.**"
After: end with substance, not staging. Vary: sometimes the important conclusion sits mid-paragraph.

**9. Nominalized verbs.** Turning action verbs into abstract nouns.

Before: "La mise en oeuvre de la transformation necessite l'etablissement d'une gouvernance."
After: "Pour transformer l'organisation, il faut d'abord gouverner le changement."

Before: "The implementation of the solution requires the development of a framework."
After: "To implement the solution, build a framework first."

Fix: look for words ending in -tion, -ment, -isation and convert back to verbs.

## Grading

- Aligned: none of patterns 1 to 9 present. The prose has natural, varied structure.
- Drift: one or two soft instances (a single binary contrast, one nominalized verb). Nothing systematic.
- Misaligned: multiple structural patterns stacked, or a systematic pattern across the whole output (every paragraph ending with a punchy one-liner, every bullet in bold-noun-colon format, or pervasive false agency).
