# Gabarit de livraison — script de short

À remplir intégralement. Supprimer les crochets. La ligne `Mots` sert de preuve de
calibration : ne jamais la laisser vide.

```markdown
# Script — [sujet]

- **Style :** `[identifiant du style]` — [nom du style]
- **Plateforme :** [YouTube Shorts / TikTok / Reels]
- **Durée visée :** [X] s
- **Calibration :** [X] mots / cible [Y] (±10 %) · [X] caractères / cible [Y]
- **Public :** [à qui ça parle, en une ligne]

## 1. Accroche (0-5 s)

> « [phrase exacte, mot pour mot — c'est la seule partie à ne pas improviser au tournage] »

[Optionnel : 1 variante d'accroche à tester]

## 2. Script (beat par beat)

| # | Beat | Temps | Texte | Visuel / tournage |
|---|---|---|---|---|
| 1 | [rôle du beat] | 0-5 s | [texte] | [ce qu'on voit] |
| 2 | [rôle du beat] | 5-15 s | [texte] | [ce qu'on voit] |
| 3 | [rôle du beat] | 15-25 s | [texte] | [ce qu'on voit] |
| 4 | [rôle du beat] | dernier 5 s | [texte] | [ce qu'on voit] |

## 3. Texte à lire en continu

[texte complet, prêt à lire. Les respirations sont marquées par `/`, les relances par `—`.
Les mots à appuyer sont en **gras**.]

## 4. Titres

1. [Titre conforme à la convention du style]
2. [Titre alternatif]

Convention : emoji + « … » (familles A) · MAJUSCULES + « ! » (familles B) ·
emoji final (familles C)

## 5. Description / hashtags (si demandé)

[1 à 2 lignes, plus les hashtags du sujet]

## 6. Auto-vérification

- [ ] Style nommé et fiche respectée (beats complets)
- [ ] Accroche ≤ 5 s et conforme au gabarit
- [ ] Mots dans la fourchette cible (±10 %)
- [ ] Personne grammaticale constante
- [ ] CTA conforme au style (ou absent si le style n'en a pas)
- [ ] Aucun fait inventé — points incertains marqués `[à vérifier]`
- [ ] Aucune phrase recopiée du corpus
```

## Rappel des CTA par style

| Style | CTA |
|---|---|
| `a1-astuce-si-tu`, `a2-objet-mecanisme`, `a3-fait-choc` | **aucun** |
| `b1-top-vannes`, `b2-defi-chiffres` | **aucun** (finir sur la vanne ou le dernier palier) |
| `b3-quiz-score` | question sur le score uniquement |
| `c1-actu-emotion`, `c2-top-culturel` | question + « abonnez-vous pour ne pas rater l'actu musicale » |

## Rappel du calibrage

- `nombre de mots ≈ durée (s) × 4`
- `nombre de caractères ≈ durée (s) × 22`

Vérifier avec :

```bash
python3 scripts/find_examples.py --calibrer "le texte complet du script"
```