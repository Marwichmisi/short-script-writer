#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Propose tags & hashtags mesurés pour un script de short.

Applique les règles de `references/hashtags.md` (emplacement selon le style,
formule génériques-puis-sujet, forme minuscules sans accents) et affiche les
3 blocs prêts à copier : hashtags de titre, hashtags de description, tags YouTube.

Usage :
    python3 suggest_tags.py --style d2-top-suspense --sujet "Inoxtag Everest" --createur Inoxtag
    python3 suggest_tags.py --style d1-lore-enquete --sujet "Doors Rooms" --univers roblox --jeu Doors
    python3 suggest_tags.py --style b4-notation-verdict --sujet "claviers gamers" --univers pc
    python3 suggest_tags.py --style a3-fait-choc --sujet "record du monde" --univers gaming
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
CARTE = SKILL_DIR / "references" / "corpus-styles.json"

# Mots trop génériques pour faire des hashtags (ils restent dans les tags YouTube).
MOTS_VIDES = {
    "le", "la", "les", "de", "des", "du", "un", "une", "et", "en", "au", "aux",
    "ce", "ces", "ses", "son", "sa", "sur", "dans", "pour", "par", "plus",
    "pas", "est", "sont", "qui", "que", "quoi", "dont", "avec", "sans",
    "sous", "entre", "vers", "chez", "comment", "pourquoi", "quand", "quel",
    "quelle", "quels", "quelles", "top", "trucs", "truc", "choses", "chose",
    "video", "vidéo", "videos", "vidéos", "jeu", "jeux", "short", "shorts",
    "the", "of", "a", "to", "in", "on", "is", "are",
}

# Boosters mesurés : hashtags génériques placés EN TÊTE (titre) ou pas de hashtags.
# Seuls b4, d2 et la variante y0us de b2 portent des hashtags dans le titre.
BOOSTERS_TITRE = {
    "d2-top-suspense": ["pourtoi", "viral", "fyp"],
    "b4-notation-verdict": [],
    "b2-defi-chiffres": ["shorts"],  # variante y0us uniquement (univers cinema)
}
BOOSTERS_UNIVERS_TITRE = {
    "pc": ["pc"],
    "gaming": ["gaming"],
    "roblox": ["roblox", "gaming"],
    "cinema": ["cinema"],
    "musique": ["musique"],
    "defaut": ["shorts"],
}

# Tags YouTube mesurés par univers (génériques + place pour le sujet).
TAGS_UNIVERS = {
    "pc": ["pc", "hardware", "montage", "bon plan", "souris", "clavier", "build",
           "gaming", "pc gamer", "rtx", "amd", "ryzen", "4070", "4060", "rx",
           "pas cher", "pc gamer pas cher", "top pc", "top build", "config",
           "config gamer", "setup"],
    "gaming": ["jeu vidéo", "gaming", "shorts"],
    "roblox": ["roblox", "roblox fr", "shorts roblox", "roblox français",
               "histoire roblox", "shorts"],
    "cinema": ["cinema", "film", "shorts"],
    "musique": ["musique", "shorts"],
    "defaut": ["shorts", "viral"],
}

# Styles dont les vidéos portent des tags YouTube dans le corpus.
STYLES_SANS_TAGS = {"d2-top-suspense", "c1-actu-emotion", "c2-top-culturel"}


def normaliser(mot: str) -> str:
    """Minuscules, sans accents, alphanumérique uniquement (forme hashtag)."""
    mot = unicodedata.normalize("NFD", mot.lower())
    mot = "".join(c for c in mot if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", mot)


def mots_sujet(sujet: str, limite: int = 3) -> list[str]:
    """Extrait les mots porteurs du sujet, dans l'ordre, sans doublons."""
    vus, utiles = set(), []
    for mot in re.split(r"\s+", sujet):
        h = normaliser(mot)
        if not h or h in vus or h in MOTS_VIDES:
            continue
        if len(h) < 3 and not any(c.isdigit() for c in h):
            continue
        vus.add(h)
        utiles.append(h)
        if len(utiles) >= limite:
            break
    return utiles


def styles_connus() -> set[str]:
    if CARTE.exists():
        return set(json.loads(CARTE.read_text(encoding="utf-8"))["styles"])
    return set()


def construire(style: str, sujet: str, univers: str,
               createur: str = "", jeu: str = "") -> dict:
    sujets = mots_sujet(sujet)
    crea = [normaliser(createur)] if createur and normaliser(createur) else []
    jeu_h = [normaliser(jeu)] if jeu and normaliser(jeu) not in sujets else []

    # --- hashtags de titre (4 cas mesurés, sinon aucun) ---
    hashtags_titre: list[str] = []
    if style == "d2-top-suspense":
        hashtags_titre = BOOSTERS_TITRE[style] + crea + sujets + jeu_h + ["shorts"]
    elif style == "b4-notation-verdict":
        hashtags_titre = BOOSTERS_UNIVERS_TITRE.get(univers, ["shorts"]) + crea + sujets + jeu_h
    elif style == "b2-defi-chiffres" and univers == "cinema":
        hashtags_titre = ["shorts"]
    hashtags_titre = list(dict.fromkeys(hashtags_titre))[:9]

    # --- hashtags de description (d1, c1/c2 : sujet d'abord, communauté ensuite) ---
    hashtags_desc: list[str] = []
    if style in ("d1-lore-enquete", "c1-actu-emotion", "c2-top-culturel"):
        communautes = {"roblox": ["roblox"], "musique": [], "cinema": [],
                       "gaming": ["gaming"], "pc": ["pc"], "defaut": []}[univers]
        hashtags_desc = (sujets + jeu_h + crea + communautes)[:5]
        hashtags_desc = list(dict.fromkeys(hashtags_desc))

    # --- tags YouTube (suivent l'univers, pas le style) ---
    tags: list[str] = []
    if style not in STYLES_SANS_TAGS:
        extras: list[str] = []
        if jeu and normaliser(jeu) not in sujets + crea:
            extras.append(jeu)
        if createur and createur not in extras:
            extras.append(createur)
        for mot in sujet.split():
            if len(mot) > 3 and mot.lower() not in {t.lower() for t in extras}:
                extras.append(mot)
            if len(extras) >= 6:
                break
        base = TAGS_UNIVERS.get(univers, TAGS_UNIVERS["defaut"])
        vus = {t.lower() for t in base}
        tags = list(base)
        for t in extras:
            if t.lower() not in vus:
                vus.add(t.lower())
                tags.append(t)
        tags = tags[:15]

    return {"titre": hashtags_titre, "description": hashtags_desc, "tags": tags}


def afficher(style: str, sujet: str, res: dict) -> None:
    print(f"# Tags & hashtags — `{style}` — « {sujet} »\n")
    print("## Hashtags de titre")
    if res["titre"]:
        print(" ".join("#" + h for h in res["titre"]))
    else:
        print("(aucun — la convention du style veut un titre sans hashtag)")
    print("\n## Hashtags de description (fin de description)")
    if res["description"]:
        print(" ".join("#" + h for h in res["description"]))
    else:
        print("(aucun — la convention du style ne met pas de hashtags en description)")
    print("\n## Tags YouTube (champ Tags)")
    if res["tags"]:
        print(", ".join(res["tags"]))
    else:
        print("(aucun — les vidéos de ce style n'ont pas de tags dans le corpus)")
    print("\nRappel : vérifier à la main l'orthographe des noms propres et qu'aucun "
          "hashtag n'est hors sujet (voir `references/hashtags.md`).")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Propose tags & hashtags mesurés pour un style et un sujet.")
    ap.add_argument("--style", required=True, help="identifiant de style (ex : d2-top-suspense)")
    ap.add_argument("--sujet", required=True, help="sujet du short (ex : \"Inoxtag Everest\")")
    ap.add_argument("--univers", default="defaut",
                    choices=["gaming", "pc", "roblox", "musique", "cinema", "defaut"],
                    help="univers du sujet (défaut : defaut)")
    ap.add_argument("--createur", default="", help="créateur / artiste / jeu concerné")
    ap.add_argument("--jeu", default="", help="jeu concerné (si différent du sujet)")
    args = ap.parse_args()

    connus = styles_connus()
    if connus and args.style not in connus:
        print(f"❌ Style inconnu : {args.style}\n   Styles : {', '.join(sorted(connus))}")
        sys.exit(1)

    afficher(args.style, args.sujet,
             construire(args.style, args.sujet, args.univers, args.createur, args.jeu))


if __name__ == "__main__":
    main()
