# Tags & hashtags (mesurés sur 97 shorts)

Règles tirées du corpus : **où** mettre les hashtags (titre ou description), **lesquels**
et **combien**. En résumé : seuls 4 cas mettent des hashtags dans le titre ; tout le
reste les met en description — ou n'en met aucun.

## Règle n° 1 : hashtags dans le titre OU en description, jamais les deux

| Style | Hashtags dans le titre | Hashtags en description | Tags YouTube |
|---|---|---|---|
| `b4-notation-verdict` | **oui**, 3-5 (`#pc #gaming` + sujet) | non | 22 tags fixes hardware |
| `d2-top-suspense` | **oui**, 6-9 (`#pourtoi #viral #fyp` + sujet) | non | aucun |
| `b2-defi-chiffres` var. y0us | **oui**, `#shorts` seul | non | 10-12 tags (univers + acteurs + sujet) |
| `a3-fait-choc` var. Shota | parfois, `\| #sujet #sujet` (3 vidéos sur 7) | non | aucun |
| `d1-lore-enquete` | **non** (titre nu) | **oui**, 4-5 (`#sujet #créateur #univers`) | 15-35 tags (génériques + spécifiques) |
| `c1-actu-emotion`, `c2-top-culturel` | non | **oui**, 3-4 (`#artiste #sujet`) | aucun |
| `a1`, `a2`, `a3` (hors Shota), `b1`, `b2` (hors y0us), `b3` | non | non | `b2` Jey & Max : 3-7 tags (jeu + mécanique) |

## Règle n° 2 : la formule par emplacement

**Hashtags de titre** (b4, d2, y0us, Shota) : toujours **génériques d'abord, sujet
ensuite**. Exemples réels :

- d2 : `#pourtoi #viral #fyp #mrbeast #triste #argent #shorts` (toujours ce trio en tête)
- b4 : `#pc #polo #tiboinshape #fuze #setup` (domaine + noms propres du sujet)
- y0us : `#shorts` seul, collé au titre
- Shota : `… | #Inoxtag #BackRooms #48h` (barre verticale + noms propres)

**Hashtags de description** (d1, c1/c2, Jinskow) : **sujet d'abord, communauté ensuite**,
en fin de description après le résumé et les liens. Exemples réels :

- d1 : `#R6 #AvatarClassique #ysto #Roblox #R15` / `#roblox #bloxburg #ysto #robloxfr #shorts`
- c1 : `#bigfloetOli #zevent #palestine` / `#Angele #nightcall #kavinsky`
- Jinskow : `#jinskow #gta #gta6` (pseudo + jeu + sujet, toujours 3)

**Tags YouTube** (champ Tags, 5 au minimum quand le style en met) : 2-3 génériques
(univers, `shorts`, langue) + 3-5 spécifiques (jeu, nom, mécanique) + 1-2
créateur/communauté. Cas mesurés :

- Jey & Max (`b1`/`b2`) : `jeu vidéo, gaming` + jeu (`undertale`, `metal gear 3`) + mécanique (`boss`, `storytelling`, `secret`)
- Ysto (`d1`) : génériques fixes (`ysto, roblox fr, shorts roblox…`) + sujet (`doors`, `bloxburg`, `r6 supprimé…`)
- Jinskow : pseudo + variantes (`jinskow, jins, jinsko, jinksow`) + jeu + sujet
- CieloTech (`b4`) : **liste fixe de 22 tags** recopiée telle quelle (`pc, hardware, montage, bon plan… config gamer`)
- y0us (`b2`) : univers (`spiderman, marvel, français, shorts`) + acteurs (`tobey maguire…`) + sujet (`méchant, vilain`)

## Règle n° 3 : forme des hashtags

- Minuscules, sans accents, sans espaces : `#pourtoi`, `#pcgamer`, `#leboncoin`.
  Pour un nom propre, la casse d'origine est tolérée (`#BackRooms`, `#Inoxtag`) mais
  jamais d'accents ni d'espaces.
- 1 à 2 mots par hashtag maximum. Au-delà, découper (`#tierlist #ram`, pas
  `#tierlistdesram`).
- Bannir les hashtags vides de sens seuls (`#viral` sans hashtag sujet ne sert à rien :
  dans le corpus, les génériques accompagnent TOUJOURS au moins un hashtag sujet).

## Génération automatique

```bash
python3 scripts/suggest_tags.py --style d2-top-suspense --sujet "Inoxtag Everest" --createur Inoxtag
python3 scripts/suggest_tags.py --style d1-lore-enquete --sujet "Doors Rooms" --univers roblox
python3 scripts/suggest_tags.py --style b4-notation-verdict --sujet "claviers gamers" --univers pc
```

Le script applique les trois règles (emplacement selon le style, formule, forme) et
affiche les 3 blocs prêts à copier : hashtags de titre, hashtags de description, tags
YouTube. Vérifier ensuite à la main : aucun hashtag inventé hors sujet, aucun nom
propre mal orthographié.
