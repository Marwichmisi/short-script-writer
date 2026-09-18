# Métriques du corpus (mesurées, non estimées)

Base : **97 transcriptions** YouTube Shorts, durée totale 74 min.
Généré par `scripts/build_corpus.py` — ne pas éditer à la main.

## Rythme par groupe

| Groupe | n | Durée moy. (s) | Mots moy. | Débit (mots/s) | Débit (car./s) |
|---|---|---|---|---|---|
| Actu & culture | 10 | 68,5 | 289 | 4,21 | 24,4 |
| Créateurs & viral | 14 | 44,6 | 179 | 4,10 | 22,6 |
| Curiosité & Astuces | 19 | 27,0 | 110 | 4,08 | 22,8 |
| Gaming | 44 | 49,0 | 203 | 4,13 | 23,0 |
| Tech & setup | 10 | 47,3 | 188 | 3,96 | 21,2 |

## Rythme par style

| Style | n | Durée observée (s) | Mots observés | Débit |
|---|---|---|---|---|
| `a1-astuce-si-tu` | 13 | 18–45 | 85–200 | 4,38 mots/s (24,2 car./s) |
| `a2-objet-mecanisme` | 13 | 18–49 | 71–215 | 4,17 mots/s (23,0 car./s) |
| `a3-fait-choc` | 21 | 18–66 | 53–254 | 3,90 mots/s (21,7 car./s) |
| `b1-top-vannes` | 7 | 60–64 | 248–309 | 4,53 mots/s (24,9 car./s) |
| `b2-defi-chiffres` | 18 | 42–97 | 167–506 | 4,30 mots/s (24,3 car./s) |
| `b3-quiz-score` | 1 | 60–60 | 301–301 | 5,02 mots/s (25,5 car./s) |
| `b4-notation-verdict` | 7 | 41–66 | 183–249 | 4,12 mots/s (21,7 car./s) |
| `c1-actu-emotion` | 4 | 61–75 | 230–285 | 3,65 mots/s (21,4 car./s) |
| `c2-top-culturel` | 1 | 70–70 | 175–175 | 2,50 mots/s (15,8 car./s) |
| `d1-lore-enquete` | 8 | 33–75 | 115–262 | 3,68 mots/s (21,1 car./s) |
| `d2-top-suspense` | 4 | 35–61 | 149–200 | 3,98 mots/s (22,3 car./s) |

## Règle de calibrage

Le débit des 97 shorts est remarquablement stable : **21 à 25 caractères par seconde**
(espaces compris), soit **3,7 à 4,5 mots par seconde**. Deux estimations équivalentes :

- `durée voulue (s) × 22` ≈ nombre de caractères du script
- `durée voulue (s) × 4` ≈ nombre de mots du script

Exemples : 25 s → ~550 caractères (~100 mots) ; 60 s → ~1 300 caractères (~240 mots).

> Mesures valables pour le français. Dans une autre langue, se caler sur la fourchette
> de 20-25 caractères/seconde plutôt que sur le nombre de mots.
