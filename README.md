# Skill `short-script-writer`

[![skills.sh](https://skills.sh/b/Marwichmisi/short-script-writer)](https://skills.sh/Marwichmisi/short-script-writer)

Écrire des scripts de vidéos courtes (YouTube Shorts, TikTok, Reels) **dans un style choisi
par le créateur**, en s'inspirant d'un corpus de 35 transcripts de shorts français
performants (1,4 M vues de médiane pour le groupe principal).

## Principe

Chaque style n'est pas une impression : il a été **mesuré** sur les transcripts d'origine
(durée, nombre de mots, débit, présence de CTA, personne grammaticale, marqueurs de
vocabulaire). Le skill demande d'abord le style au créateur, puis écrit en respectant le
contrat du style (beats, budget de mots, lexique, anti-patterns).

## Installation

### Avec le CLI skills (tous les agents)

```bash
npx skills add Marwichmisi/short-script-writer
```

Le CLI détecte l'agent utilisé (Cline, Claude Code, Cursor, Codex…) et installe le skill
dans son dossier, en projet (`.agents/skills/`) ou en global (`-g`). L'accroche de ce
dépôt est un `SKILL.md` à la racine : c'est ce que le CLI cherche en premier.

### Manuellement

```bash
git clone https://github.com/Marwichmisi/short-script-writer.git \
  ~/.agents/skills/short-script-writer

# variantes
cp -r short-script-writer ~/.claude/skills/        # Claude Code
mkdir -p .github/skills && cp -r short-script-writer .github/skills/   # Copilot
```

Aucun paquet à installer : les scripts n'utilisent que la bibliothèque standard Python 3.9+.

## Utilisation

Une fois le skill actif, il suffit de demander un script de short ; le skill présente le
menu des 8 styles et attend le choix.

```
Écris-moi un script de short sur les erreurs de débutant en musculation, style au choix.
→ le skill affiche le menu, le créateur répond « 1 », le script est écrit et calibré.

Je veux un script de 45 s dans le style b2-defi-chiffres sur le boss le plus long de
l'histoire du jeu vidéo.
```

### Les 8 styles

| # | Identifiant | Sujet type | Durée | CTA |
|---|---|---|---|---|
| 1 | `a1-astuce-si-tu` | une méthode, une erreur à corriger | 18-33 s | aucun |
| 2 | `a2-objet-mecanisme` | décoder un objet ou un phénomène | 19-24 s | aucun |
| 3 | `a3-fait-choc` | un fait stupéfiant, un récit réel | 19-54 s | aucun |
| 4 | `b1-top-vannes` | une liste drôle et vacharde | 60-64 s | aucun |
| 5 | `b2-defi-chiffres` | un record, un contenu quasi introuvable | 60-71 s | aucun |
| 6 | `b3-quiz-score` | un auto-test en points | 60 s | score en commentaire |
| 7 | `c1-actu-emotion` | une actualité artistique qui touche | 61-75 s | question + abonnement |
| 8 | `c2-top-culturel` | un classement culturel raconté | 70 s | question + abonnement |

Détail complet de chaque style : `references/styles/`. Aide au choix :
`references/style-index.md`.

## Outils en ligne de commande

```bash
# Exemples réels d'un style (hook + texte + stats)
python3 scripts/find_examples.py a3-fait-choc -n 3

# Texte entier d'un exemple
python3 scripts/find_examples.py b1-top-vannes -n 1 --complet

# Statistiques seules d'un style
python3 scripts/find_examples.py c1-actu-emotion --stats

# Chercher une tournure dans tout le corpus
python3 scripts/find_examples.py "la plupart des gens"

# Vérifier la calibration d'un script avant livraison
python3 scripts/find_examples.py --calibrer "le texte complet du script"

# Reconstruire le corpus et les métriques depuis un dossier de transcripts
python3 scripts/build_corpus.py /home/marwane/Documents/Game/inspire-scripte/scripts_out
python3 scripts/build_corpus.py /chemin/vers/scripts_out --dry-run

# Vérifier l'intégrité du skill (frontmatter, liens, styles, index)
python3 scripts/validate.py
```

## Règle de calibrage (mesurée sur le corpus)

Le débit des 35 shorts est très stable : **20 à 25 caractères par seconde** (espaces
compris), soit **3,4 à 4,6 mots par seconde**. Donc :

- `nombre de mots ≈ durée (s) × 4`
- `nombre de caractères ≈ durée (s) × 22`

Cibles usuelles : 20 s → ~80 mots · 25 s → ~100 mots · 30 s → ~120 mots · 60 s → ~240 mots ·
70 s → ~280 mots.

## Structure du dossier

```
short-script-writer/
├── SKILL.md                     workflow : style → ancrage → écriture → vérification
├── README.md                    ce fichier
├── LICENSE                      MIT (hors corpus tiers)
├── assets/
│   └── script-template.md       gabarit de livraison
├── references/
│   ├── style-index.md           arbre de décision sujet → style
│   ├── corpus-metrics.md        débits et budgets mesurés (généré)
│   ├── corpus-styles.json       carte video_id → style
│   ├── corpus-index.json        index publiable : métadonnées + accroche (généré)
│   ├── styles/                  8 fiches de style
│   │   ├── a1-astuce-si-tu.md
│   │   ├── a2-objet-mecanisme.md
│   │   ├── a3-fait-choc.md
│   │   ├── b1-top-vannes.md
│   │   ├── b2-defi-chiffres.md
│   │   ├── b3-quiz-score.md
│   │   ├── c1-actu-emotion.md
│   │   └── c2-top-culturel.md
│   └── corpus/                  transcripts complets — LOCAL, non publié (généré)
│       ├── curiosite-astuces.md
│       ├── gaming.md
│       └── actu-culture.md
└── scripts/
    ├── build_corpus.py          régénère corpus/, corpus-index.json et corpus-metrics.md
    ├── find_examples.py         recherche d'exemples + calibrage
    └── validate.py              auto-vérification (frontmatter, liens, cohérence)
```

L'intégrité du dépôt est vérifiée à chaque `push` par GitHub Actions
(`.github/workflows/validate.yml`). En local :

```bash
python3 scripts/validate.py            # code de sortie 0 = dépôt cohérent
```

## Corpus : ce qui est publié et ce qui reste local

Le skill a été construit en analysant 35 YouTube Shorts. Leur contenu parlé appartient à
leurs auteurs :

| Fichier | Publié | Contenu |
|---|---|---|
| `references/corpus-index.json` | oui | style, chaîne, durée, mots, débit, vues et **accroche** de chaque vidéo |
| `references/corpus-metrics.md` | oui | statistiques agrégées (aucun texte de tiers) |
| `references/styles/*.md` | oui | analyse originale + courtes citations d'accroches |
| `references/corpus/*.md` | non (`.gitignore`) | transcriptions complètes, pour un usage local |

Conséquence pratique : `find_examples.py` fonctionne dans les deux cas. Sans corpus local,
il affiche les métadonnées et l'accroche ; avec le corpus local, il affiche le texte
complet. Pour obtenir le corpus complet :

```bash
python3 scripts/build_corpus.py /chemin/vers/le/dossier/des/transcriptions
```

## Maintenance du corpus

Pour enrichir le corpus avec d'autres shorts récupérés :

1. transcrire les vidéos au format existant (`ID vidéo`, `Durée`, `Vues / Likes`,
   `Catégorie (link.txt)`, section `## Script`) ;
2. classer chaque vidéo dans `references/corpus-styles.json` ;
3. relancer `scripts/build_corpus.py` sur le dossier de transcripts.

Les fiches de style restent valides tant que les nouveaux scripts ressemblent à ceux déjà
analysés. Si un nouveau style apparaît (au moins 3 vidéos), créer la fiche correspondante
en copiant la structure d'une fiche existante et en y mettant les chiffres mesurés.

## Garde-fous

Le corpus est une référence de **style**, jamais une banque de textes : aucun passage ne
doit être recopié. Les styles factuels (`a3`, `b2`, `c1`) interdisent d'inventer des
chiffres, des dates ou des citations — un fait non vérifié est marqué `[à vérifier]`.