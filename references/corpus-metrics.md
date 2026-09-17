# Métriques du corpus (mesurées, non estimées)

Base : **35 transcriptions** YouTube Shorts, durée totale 25 min.
Généré par `scripts/build_corpus.py` — ne pas éditer à la main.

## Rythme par groupe

| Groupe | n | Durée moy. (s) | Mots moy. | Débit (mots/s) | Débit (car./s) |
|---|---|---|---|---|---|
| Actu & culture | 5 | 68,6 | 235 | 3,42 | 20,3 |
| Curiosité & Astuces | 19 | 27,0 | 110 | 4,08 | 22,8 |
| Gaming | 11 | 63,4 | 271 | 4,29 | 23,7 |

## Rythme par style

| Style | n | Durée observée (s) | Mots observés | Débit |
|---|---|---|---|---|
| `a1-astuce-si-tu` | 8 | 18–33 | 85–125 | 4,25 mots/s (23,4 car./s) |
| `a2-objet-mecanisme` | 4 | 19–24 | 71–99 | 4,03 mots/s (22,8 car./s) |
| `a3-fait-choc` | 7 | 19–54 | 74–231 | 3,93 mots/s (22,2 car./s) |
| `b1-top-vannes` | 5 | 60–64 | 248–309 | 4,56 mots/s (24,9 car./s) |
| `b2-defi-chiffres` | 5 | 60–71 | 229–272 | 3,86 mots/s (22,2 car./s) |
| `b3-quiz-score` | 1 | 60–60 | 301–301 | 5,02 mots/s (25,5 car./s) |
| `c1-actu-emotion` | 4 | 61–75 | 230–285 | 3,65 mots/s (21,4 car./s) |
| `c2-top-culturel` | 1 | 70–70 | 175–175 | 2,50 mots/s (15,8 car./s) |

## Règle de calibrage

Le débit des 35 shorts est remarquablement stable : **20 à 25 caractères par seconde**
(espaces compris), soit **3,4 à 4,6 mots par seconde**. Deux estimations équivalentes :

- `durée voulue (s) × 22` ≈ nombre de caractères du script
- `durée voulue (s) × 4` ≈ nombre de mots du script

Exemples : 25 s → ~550 caractères (~100 mots) ; 60 s → ~1 300 caractères (~240 mots).

> Mesures valables pour le français. Dans une autre langue, se caler sur la fourchette
> de 20-25 caractères/seconde plutôt que sur le nombre de mots.
