#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retrouve des exemples dans le corpus du skill « short-script-writer ».

Trois usages :

    python3 find_examples.py a1-astuce-si-tu
        Affiche les exemples d'un style (hook + texte + metriques).

    python3 find_examples.py "ballon de 15 étages"
        Cherche une expression dans tout le corpus et montre la phrase autour.

    python3 find_examples.py --calibrer "le texte du script à vérifier"
        Mesure un script candidat et le compare aux cibles de duree.

    python3 find_examples.py b2-defi-chiffres --top
        Exemples du style triés par vues décroissantes (les plus performants d'abord).

Options :
    -n 3        nombre d'exemples a afficher (defaut : 3)
    --complet   affiche le texte entier plutot qu'un extrait
    --stats     affiche seulement les statistiques du style
    --top       trie les exemples par vues décroissantes
"""

from __future__ import annotations

import argparse
import json
import re
import statistics as st
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
CORPUS = SKILL_DIR / "references" / "corpus"
INDEX = SKILL_DIR / "references" / "corpus-index.json"
CARTE = SKILL_DIR / "references" / "corpus-styles.json"

MOT = re.compile(r"[\w'\u2019-]+")
BLOC = re.compile(r"## ([\w-]+) — (.+?)\n\n- Style : `(.+?)` · Durée : (\d+) s · "
                  r"(\d+) mots \(([\d,]+) mots/s\) · ([\d ]+) vues\n"
                  r"[^\n]*\n- Hook : (.+?)\n\n> (.+?)\n", re.S)


def charger() -> list[dict]:
    """Charge les exemples du corpus complet s'il est présent, sinon de l'index.

    `references/corpus/` contient les transcriptions complètes (usage local).
    `references/corpus-index.json` ne contient que les métadonnées et l'accroche : c'est
    la version publiable, sans redistribution du contenu des auteurs.
    """
    exemples = []
    for chemin in sorted(CORPUS.glob("*.md")):
        for m in BLOC.finditer(chemin.read_text(encoding="utf-8")):
            exemples.append({
                "id": m.group(1),
                "titre": m.group(2),
                "style": m.group(3),
                "duree": int(m.group(4)),
                "mots": int(m.group(5)),
                "mps": m.group(6),
                "vues": m.group(7).strip(),
                "hook": m.group(8),
                "texte": m.group(9),
                "dossier": chemin.name,
            })
    if exemples:
        return exemples

    if INDEX.exists():
        for e in json.loads(INDEX.read_text(encoding="utf-8"))["exemples"]:
            exemples.append({
                "id": e["id"],
                "titre": e["titre"],
                "style": e["style"],
                "duree": e["duree"],
                "mots": e["mots"],
                "mps": str(e["mps"]).replace(".", ","),
                "vues": f"{e['vues']:,}".replace(",", " "),
                "hook": e["hook"],
                "texte": "",
                "dossier": "corpus-index.json",
            })
    return exemples


def sans_accents(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t)
                   if unicodedata.category(c) != "Mn").lower()


SANS_TEXTE = ("(transcription non publiée — elle reste locale ; lancer "
              "`python3 scripts/build_corpus.py <dossier scripts_out>` pour l'obtenir)")


def afficher(e: dict, complet: bool) -> None:
    print(f"── {e['id']} — {e['titre']}")
    print(f"   style {e['style']} · {e['duree']} s · {e['mots']} mots "
          f"({e['mps']} mots/s) · {e['vues']} vues · {e['dossier']}")
    print(f"   HOOK : {e['hook']}")
    if not e["texte"]:
        print(f"   TEXTE : {SANS_TEXTE}\n")
        return
    corps = e["texte"] if complet else (e["texte"][:420] + " […]")
    print(f"   TEXTE : {corps}\n")


def vues_int(e: dict) -> int:
    """Convertit le compteur de vues (int ou '1 234 567') en entier triable."""
    v = e.get("vues", 0)
    if isinstance(v, int):
        return v
    chiffres = re.sub(r"\D", "", str(v))
    return int(chiffres) if chiffres else 0


def par_style(style: str, n: int, complet: bool, top: bool = False) -> int:
    exemples = [e for e in charger() if e["style"] == style]
    if not exemples:
        dispo = sorted({e["style"] for e in charger()})
        print(f"❌ Style inconnu : {style}\n   Styles disponibles : {', '.join(dispo)}")
        return 1

    if top:
        exemples = sorted(exemples, key=vues_int, reverse=True)
    print(f"# {len(exemples)} exemple(s) pour `{style}`"
          + (" (triés par vues décroissantes)" if top else "") + "\n")
    for e in exemples[:n]:
        afficher(e, complet)

    if len(exemples) > n:
        print(f"({len(exemples) - n} autre(s) — augmenter -n pour les voir)\n")

    print(f"## Statistiques du style `{style}`")
    d = [e["duree"] for e in exemples]
    m = [e["mots"] for e in exemples]
    print(f"- Durée : {min(d)}-{max(d)} s (moyenne {st.mean(d):.0f} s)")
    print(f"- Mots : {min(m)}-{max(m)} (moyenne {st.mean(m):.0f})")
    print(f"- Débit moyen : {st.mean([e['mots'] / e['duree'] for e in exemples]):.2f} mots/s")
    print(f"- Cible pour une durée donnée : `durée × 4` mots, `durée × 22` caractères")
    return 0


def par_motif(motif: str, n: int, complet: bool) -> int:
    cible = sans_accents(motif)
    tous = charger()
    trouves = [e for e in tous if cible in sans_accents(e["texte"])]
    if not trouves and not any(e["texte"] for e in tous):
        # corpus non publié : on cherche dans les accroches, seules disponibles
        trouves = [e for e in tous if cible in sans_accents(e["hook"])]
        portee = "les accroches (corpus complet non présent)"
    else:
        portee = "le corpus complet"
    if not trouves:
        print(f"❌ Aucune occurrence de « {motif} » dans {portee}.")
        return 1
    print(f"# {len(trouves)} script(s) contenant « {motif} » dans {portee}\n")
    for e in trouves[:n]:
        afficher(e, complet)
    if len(trouves) > n:
        print(f"({len(trouves) - n} autre(s) — augmenter -n pour les voir)")
    return 0


def statistiques(style: str) -> int:
    """Affiche uniquement les statistiques d'un style."""
    exemples = [e for e in charger() if e["style"] == style]
    if not exemples:
        dispo = sorted({e["style"] for e in charger()})
        print(f"❌ Style inconnu : {style}\n   Styles disponibles : {', '.join(dispo)}")
        return 1
    d = [e["duree"] for e in exemples]
    m = [e["mots"] for e in exemples]
    print(f"# Statistiques de `{style}` ({len(exemples)} scripts)\n")
    print(f"- Durée : {min(d)}-{max(d)} s (moyenne {st.mean(d):.0f} s)")
    print(f"- Mots : {min(m)}-{max(m)} (moyenne {st.mean(m):.0f})")
    print(f"- Débit moyen : {st.mean([e['mots'] / e['duree'] for e in exemples]):.2f} mots/s")
    print("- Cible : `durée × 4` mots, `durée × 22` caractères")
    print("\nExemples : " + ", ".join(e["id"] for e in exemples))
    return 0


def calibrer(texte: str) -> int:
    texte = texte.strip()
    if not texte:
        print("❌ Aucun texte fourni à --calibrer.")
        return 1
    mots = len(MOT.findall(texte))
    car = len(texte)
    print("# Calibrage du script candidat\n")
    print(f"- Mots : {mots}")
    print(f"- Caractères : {car}")
    print(f"- Durée estimée : {mots / 4:.1f} s (à 4 mots/s) · {car / 22:.1f} s (à 22 car./s)\n")
    print("| Durée visée | Mots cibles | Écart | Car. cibles | Écart |")
    print("|---|---|---|---|---|")
    for duree in (20, 25, 30, 45, 60, 70):
        ecart_m = mots - duree * 4
        ecart_c = car - duree * 22
        print(f"| {duree} s | {duree * 4} | {ecart_m:+d} | {duree * 22} | {ecart_c:+d} |")
    print("\nRappel : viser ±10 % par rapport à la cible de la durée voulue.")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Retrouve des exemples du corpus et calibre un script.")
    ap.add_argument("requete", nargs="?", help="identifiant de style ou mot-clé à chercher")
    ap.add_argument("-n", type=int, default=3, help="nombre d'exemples affichés (défaut 3)")
    ap.add_argument("--complet", action="store_true", help="afficher les textes entiers")
    ap.add_argument("--stats", action="store_true",
                    help="afficher seulement les statistiques du style")
    ap.add_argument("--top", action="store_true",
                    help="trier les exemples par vues décroissantes")
    ap.add_argument("--calibrer", metavar="TEXTE", help="mesurer un script candidat")
    args = ap.parse_args()

    if args.calibrer:
        sys.exit(calibrer(args.calibrer))
    if not args.requete:
        ap.error("fournir un style, un mot-clé, ou --calibrer TEXTE")

    styles = set(json.loads(CARTE.read_text(encoding="utf-8"))["styles"]) if CARTE.exists() else set()
    if args.requete in styles:
        if args.stats:
            sys.exit(statistiques(args.requete))
        sys.exit(par_style(args.requete, args.n, args.complet, args.top))
    if re.match(r"^[a-z]\d(-|$)", args.requete):
        # ressemble à un identifiant de style (a1-…, b2-…, c3-…) : message dédié
        sys.exit(par_style(args.requete, args.n, args.complet, args.top))
    if args.stats:
        sys.exit(statistiques(args.requete))
    sys.exit(par_motif(args.requete, args.n, args.complet))


if __name__ == "__main__":
    main()