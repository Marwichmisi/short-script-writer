---
name: short-script-writer
description: "Écrire des scripts de vidéos courtes (YouTube Shorts, TikTok, Reels) en s'inspirant de 8 styles issus d'un corpus de 35 shorts réels : astuce-si-tu, objet-mécanisme, fait-choc, top-vannes, défi-chiffres, quiz-score, actu-émotion, top-culturel. Utiliser quand l'utilisateur veut écrire, rédiger, améliorer, décliner ou critiquer un script de short ; quand il demande un style de script ou veut imiter une chaîne ; ou quand il fournit une transcription de référence. Demande toujours le style voulu, puis livre accroche, script calibré au débit réel, plan de tournage et titres. Mots-clés : script vidéo courte, short, shorts, tiktok, reels, hook, accroche, script youtube."
---

# Écrire des scripts de vidéo courte

Ce skill fait écrire un script de short **dans un style précis**, choisi par le créateur,
en s'appuyant sur un corpus de 35 transcriptions de shorts français réels (analyse :
`references/corpus-metrics.md`). Les styles ne sont pas des impressions : chacun a une
structure, un budget de mots, un lexique et des anti-patterns mesurés.

**Règle d'or : ne jamais commencer à écrire sans avoir fait choisir un style.**

## Ce que ce skill produit

1. **Une accroche** (les 5 premières secondes, mot pour mot)
2. **Le script complet**, calibré sur la durée demandée (débit réel du corpus : ~22
   caractères/seconde, soit ~4 mots/seconde)
3. **Un découpage beat par beat** avec indications de tournage ou de visuel
4. **Deux titres** conformes à la convention du style (emoji ou MAJUSCULES)
5. **Une auto-vérification** contre la checklist du style

Sortie par défaut : tout dans la conversation, en markdown. Si le créateur veut un
fichier, écrire `<slug-du-sujet>.md` à côté de son projet.

---

## Étape 1 — Faire choisir le style (obligatoire)

Si le créateur n'a pas déjà nommé un style, **présenter ce menu et attendre sa réponse**.
Ne pas choisir à sa place, ne pas écrire plusieurs styles d'office.

| # | Style | Pour quel sujet | Durée | Marqueur reconnaissable |
|---|---|---|---|---|
| 1 | `a1-astuce-si-tu` | une méthode ou une erreur à corriger | 18-33 s | « Si tu [situation]… » |
| 2 | `a2-objet-mecanisme` | un objet ou un phénomène à décoder | 19-24 s | « Est-ce que tu savais que… » |
| 3 | `a3-fait-choc` | un fait stupéfiant ou un récit réel | 19-54 s | « il va réaliser que… » (périphrase d'escalade) |
| 4 | `b1-top-vannes` | une liste drôle et vacharde | 60-64 s | « 9 trucs que… » + une vanne par item |
| 5 | `b2-defi-chiffres` | un exploit ou un contenu quasi introuvable | 60-71 s | « La majorité des joueurs ne verront jamais… » |
| 6 | `b3-quiz-score` | un auto-test en points | 60 s | « 10 questions, un point par… » |
| 7 | `c1-actu-emotion` | une actualité artistique qui touche | 61-75 s | « X a bouleversé tout le monde. » + CTA |
| 8 | `c2-top-culturel` | un classement culturel qui raconte une histoire | 70 s | « 3 chansons qui ont marqué l'histoire de… » |

Présenter le menu sous forme de question numérotée, avec deux ou trois mots d'exemple par
ligne pour que le créateur se projette. Si le créateur répond « je ne sais pas » ou donne
seulement un sujet :

1. lire `references/style-index.md` (arbre de décision par sujet) ;
2. **proposer les 2 styles les plus adaptés**, avec une phrase d'explication chacun, et
   demander lequel il préfère. Ne trancher seul que si le créateur l'autorise
   explicitement.

Il est aussi possible de demander un **mélange** (« un b1 avec l'énergie d'un a3 »). Dans ce
cas : prendre la structure du style principal et n'importer que les traits cités du second,
sans mélanger les CTA (un seul par script).

### Questions à poser en même temps que le style

- **Sujet** : de quoi parle le short ? (si absent : demander, ne pas inventer le fond)
- **Durée visée** : sinon appliquer la durée du style dans le tableau ci-dessus
- **Langue** : français par défaut (les budgets de mots sont mesurés en français ; dans une
  autre langue, garder la fourchette de 20-25 caractères/seconde)
- **Rapport au réel** : le créateur a-t-il la matière (tests, données, extraits) ou
  doit-on rester sur un sujet documentaire ?

Ne poser que les questions dont la réponse manque. Si le brief est complet, passer
directement à l'étape 2.

---

## Étape 2 — S'ancrer dans le style choisi (avant d'écrire)

Lire les fichiers suivants, dans cet ordre :

1. `references/styles/<style>.md` — **obligatoire** : signature, beats, accroches, lexique,
   anti-patterns, variantes. C'est le contrat de style.
2. `references/corpus/<groupe>.md` — lire **3 à 5 transcriptions du même style** pour
   entendre le rythme réel. Ne jamais recopier un passage : s'inspirer de la tournure, puis
   écrire un texte original (voir Garde-fous). Si ce dossier est absent (installation depuis
   le dépôt public), utiliser `references/corpus-index.json` : les accroches et les
   métriques y suffisent pour ancrer le style.
3. `references/corpus-metrics.md` — la ligne du style donne la durée et le nombre de mots à
   respecter pour la calibration.

Pour retrouver les exemples pertinents sans lire tout le corpus :

```bash
python3 scripts/find_examples.py a1-astuce-si-tu
python3 scripts/find_examples.py "erreur" --grep   # cherche un mot dans le corpus
```

Si le style demandé n'existe pas encore dans `references/styles/`, le dire clairement et
proposer soit un style proche, soit de l'analyser à partir de transcriptions fournies par
le créateur (voir « Ajouter un style » en fin de fichier).

---

## Étape 3 — Écrire le script

### 3.1 Calibrer avant de rédiger

Calculer la cible à partir de la durée, puis **la respecter au mot près** :

| Durée visée | Mots (~4/s) | Caractères (~22/s) |
|---|---|---|
| 20 s | ~80 | ~440 |
| 25 s | ~100 | ~550 |
| 30 s | ~120 | ~660 |
| 45 s | ~180 | ~990 |
| 60 s | ~240 | ~1 320 |
| 70 s | ~280 | ~1 540 |

Le débit est le point de contrôle le plus fiable : **trop court = silence gênant, trop long
= fin coupée sur la plateforme**. Cette fourchette est mesurée sur 35 shorts (20-25
car./s) ; ne pas la dépasser pour « faire plus complet ».

### 3.2 Écrire beat par beat

Suivre la table des beats de la fiche de style. Pour chaque beat :

- écrire les phrases dans l'ordre des beats, sans sauter la chute ;
- utiliser les formules d'accroche et les connecteurs listés dans la fiche (ils sont tirés
  du corpus, donc directement reconnaissables pour l'audience) ;
- garder la personne grammaticale du style (« tu » pour A et B, 3e personne + « vous » pour
  C) ;
- respecter le CTA du style : aucun pour A, B1, B2 ; question de score pour B3 ;
  question + abonnement pour C.

Pendant la rédaction : **ne jamais expliquer ce qu'on est en train de faire** (« dans cette
vidéo », « je vais vous montrer »). Le spectateur est dans le contenu.

### 3.3 Formater la sortie

Utiliser `assets/script-template.md`. Format attendu :

```
ACCROCHE (0-5 s) — mot pour mot
TEXTE (beat par beat) — lignes courtes, respirations marquées par `/`
TOURNAGE / VISUEL — ce qu'on voit à l'écran pour chaque beat
TITRE — 2 propositions conformes à la convention du style
```

Ajouter une ligne `Mots : X / cible Y` et `Durée estimée : Z s` pour prouver la calibration.

---

## Étape 4 — S'auto-vérifier (obligatoire avant de livrer)

Passer le script dans cette checklist et **corriger avant d'afficher le résultat** :

- [ ] Le style est nommé en tête de réponse et la fiche a bien été lue.
- [ ] L'accroche respecte la **longueur** du style (5 s max) et son gabarit.
- [ ] Tous les beats de la fiche sont présents, y compris le dernier (chute / CTA).
- [ ] Le nombre de mots est dans la fourchette cible ±10 %.
- [ ] La personne grammaticale du style est respectée du début à la fin.
- [ ] Un seul CTA, conforme au style — et absent si le style n'en a pas.
- [ ] Aucune phrase ne recopie le corpus (voir Garde-fous).
- [ ] Aucun fait inventé : les chiffres, dates et noms sont vérifiés ou marqués `[à vérifier]`.
- [ ] Le titre suit la convention : emoji + « … » (famille A), MAJUSCULES + « ! » (famille B),
      emoji final (famille C).

Si un point échoue, réécrire la partie concernée et refaire passer la checklist. Signaler au
créateur les compromis faits (par exemple : « le sujet ne permet pas de beat 5, je l'ai
retiré »).

---

## Étape 5 — Proposer la suite

Après livraison, proposer **une seule** relance utile :

- 2 variantes d'accroche testables, quand le créateur veut A/B tester le début ;
- une déclinaison du même sujet dans un autre style, pour comparer ;
- une série de 3 scripts du même style, si le créateur construit un rendez-vous régulier.

Ne pas noyer la livraison sous les options.

---

## Garde-fous

**Originalité.** Le corpus sert de référence de *style* (rythme, structure, tournures), pas
de banque de textes. Interdits : recopier une phrase entière d'une transcription, reprendre
son sujet en changeant deux mots, ou produire une paraphrase qui suit la même phrase
d'origine. La bonne manière : lire 3-5 exemples, puis écrire à partir de la structure et
des formules génériques listées dans la fiche.

**Exactitude.** Les styles A3, B2 et C1 reposent sur des faits (études, records, dates,
artistes). Ne jamais inventer un chiffre pour « faire style » : si l'information n'est pas
sûre, la marquer `[à vérifier]` et le signaler dans la réponse. Un chiffre faux ruine la
crédibilité du format entier.

**Sujets sensibles.** La famille C touche à la politique, à la guerre et au deuil
(voir `gkOQShSdE7A`). Règles : ne pas inventer de citation, ne pas attribuer de propos à un
artiste, ne pas transformer une tragédie en ressort comique, et laisser le beat de prise de
position au créateur (proposer, ne pas imposer).

**Code source et contenus tiers.** Ne pas produire de script qui invite à reprendre le
contenu vidéo d'un autre créateur sans le créditer.

**Santé.** Le style `b3-quiz-score` est un jeu : aucun critère médical ou diagnostique
(« tu es accro », « tu es malade ») ne doit être présenté comme réel.

---

## Plan des fichiers

| Fichier | Contenu |
|---|---|
| `SKILL.md` | Le workflow : choix du style, ancrage, écriture, vérification |
| `references/style-index.md` | Arbre de décision sujet → style |
| `references/styles/*.md` | 8 fiches de style (beats, accroches, lexique, anti-patterns) |
| `references/corpus/*.md` | 35 transcriptions réelles, groupées par chaîne (usage local) |
| `references/corpus-index.json` | Index publiable : métadonnées + accroche de chaque vidéo |
| `references/corpus-styles.json` | Carte `video_id` → style |
| `references/corpus-metrics.md` | Débits et budgets mesurés, règle de calibrage |
| `assets/script-template.md` | Gabarit de livraison |
| `scripts/build_corpus.py` | Régénère le corpus et les métriques depuis un dossier de transcriptions |
| `scripts/find_examples.py` | Retrouve les exemples d'un style (ou par mot-clé) |
| `scripts/validate.py` | Auto-vérification du skill (frontmatter, liens, cohérence des styles) |
| `README.md` | Installation, usage, maintenance du corpus |

## Ajouter des scripts au corpus (le créateur récupère d'autres shorts)

1. Placer les nouvelles transcriptions `.md` au format du pipeline existant (en-tête
   `ID vidéo`, `Durée`, `Vues / Likes`, `Catégorie (link.txt)`, section `## Script`).
2. Ajouter une entrée dans le fichier de catégorie approprié — si la chaîne est nouvelle,
   ajouter une ligne dans `GROUPES` de `scripts/build_corpus.py`.
3. Classer chaque nouvelle vidéo dans `references/corpus-styles.json` (`videos`).
4. Relancer :

```bash
python3 scripts/build_corpus.py /chemin/vers/scripts_out
python3 scripts/build_corpus.py /chemin/vers/scripts_out --dry-run   # vérifier avant d'écrire
```

5. Si plusieurs nouvelles vidéos ne rentrent dans aucun style existant, créer une fiche :
   dupliquer la structure d'une fiche de `references/styles/`, puis remplir la table des
   beats et les budgets avec les chiffres **mesurés** (durée, mots, car./s) — ne pas
   estimer à l'œil.

## Ajouter un style

Un style acceptable doit réunir **au moins 3 transcriptions** de la même famille. En
dessous, ce n'est pas un style mais une vidéo isolée : la classer dans `a3-fait-choc` ou
`b1-top-vannes` selon sa forme. Après création de la fiche, l'ajouter au menu de l'étape 1
et à `references/style-index.md`.

---

## Exemple de livraison attendue (extrait, style `a1-astuce-si-tu`, 25 s)

```
Style : a1-astuce-si-tu — 25 s, cible ~100 mots.

ACCROCHE (0-4 s)
« Si ton téléphone se décharge deux fois plus vite depuis une mise à jour,
ne le jette pas : c'est souvent une seule option à désactiver. »

TEXTE (beat par beat)
1. Situation — Si ton téléphone fond deux fois plus vite qu'avant, / tu n'es pas fou.
2. Fausse évidence — La plupart des gens pensent que la batterie est morte / et vont
   dépenser 80 euros pour la changer. / Mais dans 9 cas sur 10, ce n'est pas la batterie.
3. Méthode — Et donc à la place, va dans les réglages, / coupe la localisation en
   arrière-plan / et désactive le rafraîchissement des applis que tu n'ouvres jamais.
4. Résultat — ce qui va couper la consommation invisible / et te rendre une journée
   entière d'autonomie.

VISUEL : écran du téléphone en gros plan pour le réglage, avant/après sur la batterie.
Mots : 96 / cible 100 · Durée estimée : 25 s.
TITRE : « 😳 Ton téléphone se décharge trop vite… » / « 👀 Le réglage qui vide ta batterie… »
```

Ce qui rend cet exemple conforme : accroche « Si tu… », erreur commune écartée avant la
méthode, impératifs dans la méthode, un seul résultat, **aucun CTA**, titre à emoji
tronqué par « … ».