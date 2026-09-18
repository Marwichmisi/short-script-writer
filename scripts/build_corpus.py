#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit le corpus condensé du skill « short-script-writer ».

Lit un dossier de transcriptions (fichiers .md produits par le pipeline AssemblyAI :
en-tête de métadonnées + section « ## Script ») puis écrit :

  references/corpus/<groupe>.md   transcriptions condensées, groupées par chaîne
  references/corpus-metrics.md    métriques de rythme par chaîne et par style

Usage :
    python3 build_corpus.py /chemin/vers/scripts_out
    python3 build_corpus.py /chemin/vers/scripts_out -o references/corpus --metrics references/corpus-metrics.md

Utilisez ce script pour AJOUTER de nouvelles transcriptions au corpus : relancez-le
sur un dossier scripts_out enrichi. Les fiches de style restent valides tant que les
nouveaux scripts ressemblent à ceux déjà analysés.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent

# Catégorie (link.txt) -> (fichier de sortie, titre du groupe)
# Plusieurs catégories peuvent partager un fichier (ex : tout le gaming ensemble).
GROUPES = {
    "Fitness muscu": ("curiosite-astuces.md", "Curiosité & Astuces"),
    "JeyEtMax": ("gaming.md", "Gaming"),
    "YstoRoblox": ("gaming.md", "Gaming"),
    "Jinskow": ("gaming.md", "Gaming"),
    "slimusic_off": ("actu-culture.md", "Actu & culture"),
    "y0us_tv": ("actu-culture.md", "Actu & culture"),
    "ShotaPrime": ("createurs-viral.md", "Créateurs & viral"),
    "LuK_Vidéos": ("createurs-viral.md", "Créateurs & viral"),
    "CieloTech": ("tech-setup.md", "Tech & setup"),
}

MOT = re.compile(r"[\w'\u2019-]+")
PHRASE = re.compile(r"(?<=[.!?])\s+")


def fr(n: float, dec: int = 2) -> str:
    """Formate un nombre à la française (virgule décimale)."""
    return f"{n:.{dec}f}".replace(".", ",")


def parse_transcription(path: Path) -> dict | None:
    """Extrait les métadonnées et le texte du script d'une transcription .md."""
    texte = path.read_text(encoding="utf-8")

    def cherche(motif: str, defaut: str = "") -> str:
        m = re.search(motif, texte, re.S)
        return m.group(1).strip() if m else defaut

    identifiant = cherche(r"ID vidéo :\*\* `([\w-]+)`")
    script = cherche(r"## Script[^\n]*\n\n(.+?)\n\n##")
    duree = int(cherche(r"Durée :\*\* (\d+)", "0") or 0)
    if not identifiant or not script or not duree:
        return None

    script = re.sub(r"\s+", " ", script).strip()
    return {
        "id": identifiant,
        "categorie": cherche(r"Catégorie \(link.txt\) :\*\* ([^\n]+)"),
        "chaine": cherche(r"Chaîne :\*\* (.+?) \(uploader"),
        "duree": duree,
        "vues": int(cherche(r"Vues / Likes :\*\* (\d+)", "0") or 0),
        "titre": texte.split("\n")[0].lstrip("# ").strip(),
        "texte": script,
        "mots": len(MOT.findall(script)),
        "hook": PHRASE.split(script)[0].strip(),
    }


def enrichir(t: dict) -> dict:
    """Ajoute les ratios de rythme (mots/s et caractères/s)."""
    t["mps"] = round(t["mots"] / t["duree"], 2)
    t["cps"] = round(len(t["texte"]) / t["duree"], 1)
    return t


def collecter(source: Path) -> list[dict]:
    if not source.is_dir():
        sys.exit(f"❌ Dossier introuvable : {source}")
    items = []
    for chemin in sorted(source.glob("*.md")):
        if chemin.name.upper() == "INDEX.MD":
            continue
        t = parse_transcription(chemin)
        if t is None:
            print(f"    ignoré (format inattendu) : {chemin.name}")
            continue
        items.append(enrichir(t))
    if not items:
        sys.exit(f"❌ Aucune transcription exploitable dans {source}")
    return items


def charger_styles() -> dict:
    """Charge la carte video_id -> identifiant de style (references/corpus-styles.json)."""
    carte = SKILL_DIR / "references" / "corpus-styles.json"
    if not carte.exists():
        return {}
    return json.loads(carte.read_text(encoding="utf-8")).get("videos", {})


def ecrire_corpus(items: list[dict], styles: dict, sortie: Path) -> dict:
    """Écrit une fiche markdown par groupe. Retourne {titre: (chemin, scripts)}."""
    sortie.mkdir(parents=True, exist_ok=True)
    par_fichier: dict[str, list[dict]] = {}
    for t in items:
        fichier = GROUPES.get(t["categorie"], ("autres.md", "Autres"))[0]
        par_fichier.setdefault(fichier, []).append(t)

    groupes, inconnus = {}, []
    for fichier, groupe in sorted(par_fichier.items()):
        titre = next((g[1] for g in GROUPES.values() if g[0] == fichier), "Autres")
        lignes = [
            f"# Corpus — {titre}",
            "",
            "Transcriptions réelles de YouTube Shorts (AssemblyAI), condensées pour servir de",
            "référence de style. **Ne jamais recopier ces textes mot pour mot** : s'en inspirer",
            "pour le rythme, la structure et les tournures, puis écrire un contenu original.",
            "",
        ]
        for t in sorted(groupe, key=lambda x: -x["duree"]):
            style = styles.get(t["id"], "non classé")
            if t["id"] not in styles:
                inconnus.append(t["id"])
            vues = f"{t['vues']:,}".replace(",", " ")
            lignes += [
                f"## {t['id']} — {t['titre']}",
                "",
                f"- Style : `{style}` · Durée : {t['duree']} s · {t['mots']} mots "
                f"({fr(t['mps'])} mots/s) · {vues} vues",
                f"- Chaîne : {t['chaine']}",
                f"- Hook : {t['hook']}",
                "",
                f"> {t['texte']}",
                "",
            ]
        chemin = sortie / fichier
        chemin.write_text("\n".join(lignes), encoding="utf-8")
        groupes[titre] = (chemin, groupe)

    if inconnus:
        apercu = ", ".join(inconnus[:12]) + (" …" if len(inconnus) > 12 else "")
        print(f"  ℹ  {len(inconnus)} script(s) sans style dans corpus-styles.json : {apercu}")
    return groupes


def ecrire_metriques(items: list[dict], styles: dict, groupes: dict, chemin: Path) -> None:
    """Écrit le tableau des métriques mesurées (rythme par groupe et par style)."""
    lignes = [
        "# Métriques du corpus (mesurées, non estimées)",
        "",
        f"Base : **{len(items)} transcriptions** YouTube Shorts, durée totale "
        f"{sum(t['duree'] for t in items) // 60} min.",
        "Généré par `scripts/build_corpus.py` — ne pas éditer à la main.",
        "",
        "## Rythme par groupe",
        "",
        "| Groupe | n | Durée moy. (s) | Mots moy. | Débit (mots/s) | Débit (car./s) |",
        "|---|---|---|---|---|---|",
    ]
    for titre in sorted(groupes):
        g = groupes[titre][1]
        lignes.append(
            f"| {titre} | {len(g)} | {fr(st.mean([t['duree'] for t in g]), 1)} | "
            f"{fr(st.mean([t['mots'] for t in g]), 0)} | "
            f"{fr(st.mean([t['mps'] for t in g]))} | {fr(st.mean([t['cps'] for t in g]), 1)} |"
        )

    par_style: dict[str, list[dict]] = {}
    for t in items:
        if t["id"] in styles:
            par_style.setdefault(styles[t["id"]], []).append(t)

    lignes += [
        "",
        "## Rythme par style",
        "",
        "| Style | n | Durée observée (s) | Mots observés | Débit |",
        "|---|---|---|---|---|",
    ]
    for style in sorted(par_style):
        g = par_style[style]
        lignes.append(
            f"| `{style}` | {len(g)} | {min(t['duree'] for t in g)}–{max(t['duree'] for t in g)} | "
            f"{min(t['mots'] for t in g)}–{max(t['mots'] for t in g)} | "
            f"{fr(st.mean([t['mps'] for t in g]))} mots/s "
            f"({fr(st.mean([t['cps'] for t in g]), 1)} car./s) |"
        )

    lignes += [
        "",
        "## Règle de calibrage",
        "",
    ]
    # Fourchette mesurée sur les styles ayant au moins 3 exemples (les styles à
    # 1 exemple — b3, c2 — sont trop fragiles pour cadrer le débit global).
    solides = [g for g in par_style.values() if len(g) >= 3]
    if solides:
        cps_min = min(st.mean([t["cps"] for t in g]) for g in solides)
        cps_max = max(st.mean([t["cps"] for t in g]) for g in solides)
        mps_min = min(st.mean([t["mps"] for t in g]) for g in solides)
        mps_max = max(st.mean([t["mps"] for t in g]) for g in solides)
        lignes += [
            f"Le débit des {len(items)} shorts est remarquablement stable : "
            f"**{fr(cps_min, 0)} à {fr(cps_max, 0)} caractères par seconde**",
            "(espaces compris), soit "
            f"**{fr(mps_min, 1)} à {fr(mps_max, 1)} mots par seconde**. "
            "Deux estimations équivalentes :",
        ]
    else:
        lignes += [
            "Le débit des shorts est remarquablement stable : **20 à 25 caractères par seconde**",
            "(espaces compris), soit **3,4 à 4,6 mots par seconde**. Deux estimations équivalentes :",
        ]
    lignes += [
        "",
        "- `durée voulue (s) × 22` ≈ nombre de caractères du script",
        "- `durée voulue (s) × 4` ≈ nombre de mots du script",
        "",
        "Exemples : 25 s → ~550 caractères (~100 mots) ; 60 s → ~1 300 caractères (~240 mots).",
        "",
        "> Mesures valables pour le français. Dans une autre langue, se caler sur la fourchette",
        "> de 20-25 caractères/seconde plutôt que sur le nombre de mots.",
        "",
    ]
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(lignes), encoding="utf-8")


def ecrire_index(items: list[dict], styles: dict, chemin: Path) -> None:
    """Écrit un index du corpus sans le texte brut (métadonnées + accroche).

    Utile pour publier le skill sans rediffuser les transcriptions d'origine : le script
    find_examples.py s'en sert comme solution de repli quand references/corpus/ est absent.
    """
    entrees = []
    for t in sorted(items, key=lambda x: (styles.get(x["id"], "zz"), -x["duree"])):
        entrees.append({
            "id": t["id"],
            "style": styles.get(t["id"], "non classe"),
            "titre": t["titre"],
            "chaine": t["chaine"],
            "categorie": t["categorie"],
            "duree": t["duree"],
            "mots": t["mots"],
            "mps": t["mps"],
            "cps": t["cps"],
            "vues": t["vues"],
            "hook": t["hook"],
        })
    donnees = {
        "_commentaire": (
            "Index du corpus : métadonnées mesurées et accroche de chaque short analysé. "
            "Les transcriptions complètes restent locales (references/corpus/) : elles "
            "appartiennent à leurs auteurs et ne sont pas redistribuées."
        ),
        "total": len(entrees),
        "exemples": entrees,
    }
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Construit le corpus condensé du skill.")
    ap.add_argument("source", help="Dossier des transcriptions .md (ex : scripts_out)")
    ap.add_argument("-o", "--out", default=str(SKILL_DIR / "references" / "corpus"),
                    help="Dossier de sortie du corpus (défaut : references/corpus)")
    ap.add_argument("--metrics", default=str(SKILL_DIR / "references" / "corpus-metrics.md"),
                    help="Fichier de métriques à écrire")
    ap.add_argument("--index", default=str(SKILL_DIR / "references" / "corpus-index.json"),
                    help="Index sans texte brut à écrire (défaut : references/corpus-index.json)")
    ap.add_argument("--dry-run", action="store_true",
                    help="N'écrit rien, affiche seulement le résumé ligne par ligne")
    args = ap.parse_args()

    items = collecter(Path(args.source).expanduser())
    styles = charger_styles()
    print(f"✅ {len(items)} transcriptions lues · {len(styles)} styles connus")

    if args.dry_run:
        for t in items:
            print(f"  {t['id']:14} {t['duree']:>3} s  {t['mots']:>3} mots  "
                  f"{fr(t['mps'])} mots/s  {styles.get(t['id'], 'non classé')}")
        return

    groupes = ecrire_corpus(items, styles, Path(args.out).expanduser())
    for titre in sorted(groupes):
        chemin, groupe = groupes[titre]
        print(f"   → {chemin} ({len(groupe)} scripts)")
    ecrire_metriques(items, styles, groupes, Path(args.metrics).expanduser())
    print(f"   → {args.metrics}")
    ecrire_index(items, styles, Path(args.index).expanduser())
    print(f"   → {args.index}")


if __name__ == "__main__":
    main()