# Dimension Library — Sector-Specific Benchmark Axes

This file is loaded by the skill during Phase 0 Q4 to propose dimensions adapted to the
detected market sector. Read the sector that matches Q1's answer, then present its dimensions
to the consultant.

## How to use
1. After Q1 (market + client), identify the sector from the table below.
2. Present the matched sector's dimensions with their rationale.
3. If no sector matches precisely, combine the closest + the Default framework.
4. Always offer the consultant the option to modify, add, or remove dimensions.

## Sector Detection Keywords

| Keywords | Sector entry |
|----------|-------------|
| LMD, location moyenne durée, abonnement auto, car subscription, leasing auto | -> Location Véhicule |
| assurance emprunteur, assurance vie, mutuelle santé, prévoyance, couverture | -> Assurance |
| télécom, mobile, forfait, B2B telecom, opérateur, réseau, 4G/5G | -> Télécom B2B |
| coworking, flex office, bureau partagé, espaces de travail, immobilier entreprise | -> Coworking / Flex Office |
| néobanque, fintech, banking, compte pro, paiement, carte, neobank | -> Banque & Fintech |
| mobilité électrique, EV, véhicule électrique, LLD électrique, flotte | -> Mobilité Électrique |
| logistique, livraison, last mile, urbain, transport, messagerie | -> Logistique Urbaine |
| SIRH, RH, ressources humaines, paie, gestion des talents, HR tech | -> RH & SIRH |
| santé au travail, bien-être, QVT, médecine du travail, prévention | -> Santé au Travail |
| financement PME, crédit, lending, dette, invoice, trésorerie | -> Financement PME |
| SaaS, logiciel, plateforme, B2B software, API, intégration | -> SaaS / Software |
| retail, e-commerce, marketplace, marque, distribution, omnicanal | -> Retail & Distribution |

---

## Location Véhicule (LMD, Abonnement Auto, LCD)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Offre & Conditions** | Durées disponibles (1/3/6/12 mois), type de contrat, résiliation anticipée, frais de fin | La flexibilité durée est le critère de différenciation n°1 sur LMD |
| 2 | **Contenu du service** | Assurance incluse (RC/tous risques), entretien, assistance, pneumatiques, livraison/reprise | Le "tout inclus" vs le "à la carte" structure l'offre et impacte la comparaison de prix |
| 3 | **Cibles & Tone of Voice** | B2B/B2C, segments (jeunes actifs, nomades, entreprises), ton de marque, canaux | Les acteurs adressent des segments très différents avec des messaging opposés |
| 4 | **Pricing & Véhicule** | Tarif par durée, par segment de véhicule, km inclus, frais au km dépassé, transparence | La grille tarifaire est le premier critère de décision — la transparence est un différenciant |
| 5 | **Expérience & Digital** *(optionnel)* | Réservation/souscription en ligne, app mobile, délai de livraison, NPS/avis clients | Le digital est devenu un critère d'hygiène — lag ici = perte de prospects |

*Adapter selon le périmètre : si focus uniquement B2B fleet, remplacer dim 3 par "Fleet & Services Entreprise".*

---

## Assurance (Emprunteur, Vie, Santé, Prévoyance)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Garanties & Couverture** | Garanties incluses (DC, PTIA, IPT, ITT, chômage), exclusions, plafonds | La nature et l'étendue des garanties est le facteur d'achat n°1 — différences majeures entre acteurs |
| 2 | **Conditions d'accès & Souscription** | Âge limite, questionnaire médical, délai de carence, process de souscription | L'accès est un critère de segmentation fort (senior, maladie préexistante, indépendant) |
| 3 | **Tarification** | Taux (% CRD ou capital initial), mode de calcul, dégressivité, cotisation mensuelle estimée | Le pricing est opaque dans ce secteur — la transparence tarifaire est un différenciant |
| 4 | **Expérience client & Gestion sinistre** | Canal de souscription (en ligne, courtier, bancaire), délai remboursement, avis clients | Le moment de vérité = le sinistre — les acteurs digitaux se différencient ici |
| 5 | **Positionnement & Distribution** *(optionnel)* | Bancassurance vs pure player vs insurtech, canal de distribution, B2B/B2C/B2B2C | Le canal définit souvent le pricing et l'expérience perçue |

---

## Télécom B2B (Mobile, Fixe, Internet Entreprise)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Offres & Forfaits** | Gammes (voix+data, data seule, international), volume data, débit garanti, options | La clarté et la modularité des offres est un critère de décision pour les DSI |
| 2 | **Couverture & Qualité Réseau** | Couverture 4G/5G, zones blanches, roaming Europe/international, SLA | La qualité réseau est un critère rédhibitoire pour les entreprises multi-sites |
| 3 | **Services B2B & Gestion de Flotte** | Portail de gestion, rapports de consommation, MDM, APIs, support dédié | Les services autour de l'offre distinguent les opérateurs pro des offres grand public |
| 4 | **Tarification & Engagement** | Prix par ligne, dégressivité volume, durée d'engagement, migration/résiliation, frais cachés | Les contrats pluriannuels avec engagement sont la norme — la flexibilité est un différenciant |
| 5 | **Support & SLA** *(optionnel)* | Interlocuteur dédié, temps de réponse garanti, SLA résolution, support technique 24/7 | Les PME/ETI valorisent fortement l'accompagnement — c'est là que les opérateurs se différencient |

---

## Coworking / Flex Office

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Offre & Formats** | Postes flexibles, bureaux privatifs, salles de réunion, abonnements, locations journalières | La gamme de formats définit à qui l'espace s'adresse (freelance vs scale-up vs grand compte) |
| 2 | **Localisation & Réseau** | Nombre de sites, villes, accessibilité transport, réseau multi-villes | La densité du réseau est un critère clé pour les entreprises avec des équipes nomades |
| 3 | **Services & Équipements** | Internet, salles incluses, print, cuisine, réception, services conciergerie, communauté | Les services périphériques sont des leviers de fidélisation — différencient les pure players premium |
| 4 | **Cibles & Communauté** | Freelance / startup / PME / grand compte, événements, networking, verticalisation sectorielle | Certains acteurs misent sur la communauté comme différenciant vs simple commodité de bureau |
| 5 | **Pricing & Flexibilité** *(optionnel)* | Tarif par poste/mois, mensualisation vs engagement, transparence tarifaire | L'absence d'engagement long terme est une promesse centrale du coworking |

---

## Banque & Fintech (Néobanque, Compte Pro, Paiement)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Offre de compte & Fonctionnalités** | Compte courant, IBAN, cartes, virements instantanés, multi-devises, sous-comptes | La richesse fonctionnelle baseline distingue les néobanques entre elles |
| 2 | **Services financiers complémentaires** | Crédit, épargne, assurance, gestion de trésorerie, facturation, comptabilité | Les acteurs qui sortent du compte vers les services adjacents créent des écosystèmes |
| 3 | **Expérience & UX** | App mobile, onboarding (délai ouverture), tableau de bord, notifications, open banking | L'expérience est le critère de rétention n°1 — les traditionnels sont systématiquement en retard |
| 4 | **Cibles & Positionnement** | Particuliers / travailleurs indépendants / PME / ETI, segments géographiques, freemium vs premium | Chaque acteur adresse un segment précis — la promesse doit être cohérente avec la cible |
| 5 | **Tarification & Modèle économique** *(optionnel)* | Frais mensuels, à l'acte (virement, carte), taux de change, conditions gratuité | La structure tarifaire est complexe — la transparence et la comparabilité sont des enjeux forts |

---

## Mobilité Électrique B2B (LLD Electrique, Flotte EV)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Gamme de véhicules & Motorisation** | Véhicules disponibles (VUL, VP, 2 roues), autonomie, bornes de recharge incluses | La disponibilité de modèles pertinents et l'autonomie réelle conditionnent l'adoption |
| 2 | **Services de recharge** | Borne à domicile installée, carte réseau public, remboursement recharge domicile, infrastructure entreprise | La recharge est la principale friction — les acteurs qui la résolvent end-to-end ont un avantage |
| 3 | **Offre contractuelle & Flexibilité** | Durée LLD, kilométrage, résiliation, reprise anticipée, mise à jour technologique | La vitesse d'évolution des véhicules EV crée un besoin de flexibilité que les leasers gèrent différemment |
| 4 | **Services aux flottes** | Reporting CO2, portail de gestion flotte, accompagnement transition, formations conducteurs | Les entreprises cherchent à piloter leur transition énergétique — les acteurs qui outillent ça gagnent |
| 5 | **Pricing & Aides** *(optionnel)* | Mensualité LLD, intégration bonus écologique, TCO vs thermique, devis personnalisé | Le TCO vs thermique est le calcul clé pour décider — les acteurs qui le simplifient convertissent mieux |

---

## Logistique Urbaine (Livraison, Last Mile)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Offre de services** | B2B / B2C, express, same-day, J+1, vrac vs colis, retours | La diversité de l'offre définit les marchés adressables — les pure players last mile vs intégrateurs |
| 2 | **Couverture géographique** | Zones couvertes, densité urbaine vs périurbain, points relais, hubs | La capillarité du réseau est le principal levier de différenciation opérationnelle |
| 3 | **Tracking & Expérience destinataire** | Suivi temps réel, notifications, créneaux horaires, gestion de l'absent | L'expérience destinataire conditionne la satisfaction e-commerçant — les retards/absents sont coûteux |
| 4 | **Durabilité & Empreinte carbone** | Flotte verte (vélo cargo, EV), offre bas-carbone, reporting CO2, labellisation | La pression réglementaire (ZFE) et les engagements RSE des expéditeurs poussent vers la logistique verte |
| 5 | **Pricing & Modèle contractuel** *(optionnel)* | Tarif au colis/kg/km, contrat volume, engagement, SLA livraison, pénalités | La structure de prix impacte directement la marge des e-commerçants — la transparence est rare |

---

## RH & SIRH (HR Tech, Gestion RH, Paie)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Fonctionnalités core RH** | Paie, gestion des temps (GTA), congés, notes de frais, gestion administrative | Le périmètre fonctionnel de base conditionne la sélection — certains acteurs sont spécialisés, d'autres full-suite |
| 2 | **Modules avancés & Talents** | Recrutement (ATS), formation (LMS), évaluation de performance, onboarding, GPEC | Les modules talents différencient les SIRH complets des solutions de paie uniquement |
| 3 | **Expérience utilisateur & Adoption** | Interface DRH / manager / salarié, app mobile, self-service RH, ergonomie | L'adoption par les managers de terrain est l'enjeu clé — une mauvaise UX tue le ROI |
| 4 | **Intégrations & Ecosystème** | Connecteurs ERP (SAP, Oracle), API, marketplace partenaires, SSO | Les SIRH vivent dans un écosystème — la capacité d'intégration conditionne le choix pour les ETI |
| 5 | **Pricing & Modèle SaaS** *(optionnel)* | Tarif par salarié/mois, modules optionnels, implémentation, support, engagement | Le TCO à 3 ans (licence + implémentation + formation) est souvent sous-estimé |

---

## Santé au Travail / Mutuelle Entreprise

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Garanties & Couverture** | Remboursements santé (optique, dentaire, hospitalisation), prévoyance (IJ, invalidité, décès) | La qualité et l'étendue des garanties est le premier critère de choix par les DRH |
| 2 | **Services prévention & QVT** | Programmes de prévention, accompagnement psychologique, téléconsultation, soutien RPS | La prévention est devenue un critère RH fort — les acteurs qui proposent des services au-delà du remboursement se différencient |
| 3 | **Expérience adhérent** | Application mobile, espace personnel, délais de remboursement, carte tiers payant | L'expérience numérique est devenue un critère d'hygiène — les organismes traditionnels souffrent ici |
| 4 | **Tarification & Portabilité** | Cotisations (part employeur/salarié), modulation familiale, portabilité Evin, devis entreprise | La structure de cotisation et l'obligation de portabilité créent des contraintes spécifiques |
| 5 | **Services entreprise & Reporting** *(optionnel)* | Portail RH, statistiques santé, aide au choix contrat, accompagnement mise en conformité | Les grands comptes cherchent un partenaire RH, pas juste un assureur |

---

## Financement PME (Crédit, Lending, Dette Alternative)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Types de financement** | Prêt amortissable, crédit revolving, affacturage, financement de factures, equity, revenue-based | La nature du produit financier définit le profil de client adressé |
| 2 | **Conditions d'accès & Eligibilité** | Ancienneté requise, CA minimum, secteur, notation interne, scoring, documents requis | L'accessibilité est le différenciant n°1 vs les banques — les fintech revendiquent l'inclusion |
| 3 | **Rapidité & Expérience** | Délai de réponse, délai de déblocage des fonds, process en ligne, interface | Le speed-to-cash est le principal argument des acteurs alternatifs vs banques |
| 4 | **Pricing & Transparence** | Taux (TEG/TAEG), frais de dossier, coût total du crédit, pénalités de remboursement anticipé | Le coût réel du financement est souvent opaque — la transparence convertit mieux les PME avisées |
| 5 | **Accompagnement & Services** *(optionnel)* | Conseiller dédié, outils de simulation, tableau de bord dette, accompagnement croissance | Les PME cherchent un partenaire financier, pas un distributeur de produits |

---

## SaaS / Software B2B (Générique)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Fonctionnalités & Périmètre** | Core features, modules disponibles, roadmap, verticalisations sectorielles | Le périmètre fonctionnel conditionne l'adéquation besoin — première étape de la sélection |
| 2 | **Expérience & Adoption** | Onboarding, formation, UX/UI, self-service vs accompagné | L'adoption des utilisateurs finaux est le KPI n°1 des DSI — un outil non utilisé = ROI nul |
| 3 | **Intégrations & Ecosystème** | APIs, connecteurs natifs (CRM, ERP, BI), marketplace, webhooks | Le SaaS vit dans un stack — la capacité d'intégration est souvent bloquante |
| 4 | **Support & SLA** | Temps de réponse, canaux (chat/email/tel), base de connaissances, CSM dédié | Le support post-vente est le principal facteur de satisfaction et de renouvellement |
| 5 | **Pricing & Modèle** *(optionnel)* | Tarif par utilisateur/mois, modules optionnels, tier Enterprise, implementation fees | Le pricing SaaS est complexe — les coûts cachés augmentent le TCO réel |

---

## Retail & Distribution (Marque, E-commerce, Omnicanal)

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé sur ce marché |
|---|-----------|-------------------|--------------------------------------|
| 1 | **Offre & Assortiment** | Gamme produits, profondeur, exclusivités, marques propres, nouveautés | La richesse et le renouvellement de l'assortiment est le levier de trafic et de différenciation |
| 2 | **Expérience client omnicanale** | Web, app, magasin, click & collect, retours, personnalisation, fidélité | La cohérence omnicanale est l'enjeu structurant — les silos online/offline créent de la friction |
| 3 | **Logistique & Délais** | Délai de livraison, options (J+1, express, point relais), frais de livraison, retours gratuits | La logistique est devenue une promesse client — Amazon a établi un standard difficile à ignorer |
| 4 | **Pricing & Promotions** | Prix catalogue, fréquence des promotions, politique de prix bas quotidien vs pricing dynamique | La perception prix est un pilier de positionnement — discount vs premium ont des stratégies opposées |
| 5 | **Marque & Communication** *(optionnel)* | Identité, valeurs, engagements RSE, ton, influenceurs, communauté | Dans un marché commoditisé, l'image et les valeurs créent de la préférence |

---

## Default / Secteur non reconnu

> Utiliser quand aucun keyword de Q1 ne correspond aux 12 secteurs ci-dessus (marché de niche, B2B exotique, secteur émergent).

| # | Dimension | Ce qu'elle couvre | Pourquoi elle est clé |
| --- | --------- | ----------------- | --------------------- |
| 1 | **Offre, Conditions & Promesse** | Nature de l'offre, durée, flexibilité, contrat, promesse client headline | Définit le périmètre de ce que l'acteur vend et comment il se positionne vis-à-vis du client |
| 2 | **Contenu du service** | Ce qui est inclus (garanties, support, options), ce qui est exclu, frais additionnels | L'écart entre promesse et contenu réel est souvent la source des surprises client — et des différenciants |
| 3 | **Cibles & Tone of Voice** | Segments adressés (B2B/B2C/mixte), messaging, canaux, ton de marque | Comprendre à qui chaque acteur parle oriente la stratégie de positionnement du client |
| 4 | **Pricing & Choix** | Grille tarifaire, logique de dégressivité, transparence, frais cachés | Le pricing est le signal de positionnement le plus lisible — et souvent le critère de décision final |

**Comment adapter :** si une dimension standard ne s'applique pas (ex : "Contenu du service" pour un acteur sans garanties), renommer ou fusionner avec une dimension adjacente. Documenter l'adaptation dans le bloc "Pourquoi ces axes ?" de Q4.
