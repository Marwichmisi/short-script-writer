#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto-vérification du skill (utilisable en local et en CI).

Contrôle ce qui casse silencieusement un skill publié :

1. `SKILL.md` : frontmatter YAML valide, `name` en kebab-case identique au dossier,
   `description` non vide, sans chevrons et sous 1024 caractères ;
2. les chemins cités dans `SKILL.md` et `README.md` existent réellement ;
3. chaque style de `references/corpus-styles.json` a sa fiche dans `references/styles/`
   et figure dans le menu de `SKILL.md` ;
4. `references/corpus-index.json` est cohérent avec la carte des styles ;
5. les scripts Python compilent et leur `--help` répond.

Usage : python3 scripts/validate.py     (code de sortie 0 = tout est bon)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
erreurs: list[str] = []
avertissements: list[str] = []


def erreur(message: str) -> None:
    erreurs.append(message)


def avertir(message: str) -> None:
    avertissements.append(message)


def verifier_frontmatter() -> None:
    skill = RACINE / "SKILL.md"
    if not skill.exists():
        erreur("SKILL.md absent à la racine")
        return
    texte = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
    if not m:
        erreur("SKILL.md : frontmatter YAML absent ou mal formé")
        return

    bloc = m.group(1)
    nom = re.search(r"^name:\s*(.+)$", bloc, re.M)
    desc = re.search(r"^description:\s*(.+)$", bloc, re.M)
    if not nom:
        erreur("frontmatter : clé `name` manquante")
    else:
        valeur = nom.group(1).strip().strip('"')
        if valeur != RACINE.name:
            erreur(f"`name: {valeur}` ne correspond pas au dossier `{RACINE.name}`")
        if not re.fullmatch(r"[a-z0-9-]+", valeur):
            erreur(f"`name: {valeur}` doit être en kebab-case")
    if not desc:
        erreur("frontmatter : clé `description` manquante")
    else:
        valeur = desc.group(1).strip().strip('"')
        if len(valeur) > 1024:
            erreur(f"description trop longue ({len(valeur)} > 1024 caractères)")
        if "<" in valeur or ">" in valeur:
            erreur("description : les chevrons (< >) sont interdits")
        if len(valeur) < 80:
            avertir("description très courte : le skill risque de mal se déclencher")


def verifier_chemins() -> None:
    """Chaque chemin de fichier cité dans la doc doit exister."""
    motif = re.compile(r"`((?:references|assets|scripts)/[\w./-]+)`")
    for doc in ("SKILL.md", "README.md"):
        chemin = RACINE / doc
        if not chemin.exists():
            erreur(f"{doc} absent")
            continue
        for cite in sorted(set(motif.findall(chemin.read_text(encoding="utf-8")))):
            if cite.endswith("/") or "*" in cite:
                continue
            if not (RACINE / cite).exists():
                # le corpus complet est local par conception : simple avertissement
                (avertir if cite.startswith("references/corpus/") else erreur)(
                    f"{doc} cite `{cite}` qui n'existe pas")


def charger_styles() -> dict:
    carte = RACINE / "references" / "corpus-styles.json"
    if not carte.exists():
        erreur("references/corpus-styles.json absent")
        return {}
    return json.loads(carte.read_text(encoding="utf-8"))


def verifier_styles(carte: dict) -> None:
    styles = carte.get("styles", {})
    if len(styles) < 2:
        erreur("corpus-styles.json : moins de 2 styles déclarés")
    menu = RACINE / "SKILL.md"
    texte_menu = menu.read_text(encoding="utf-8") if menu.exists() else ""
    index_style = RACINE / "references" / "style-index.md"
    texte_index = index_style.read_text(encoding="utf-8") if index_style.exists() else ""

    for identifiant in styles:
        fiche = RACINE / "references" / "styles" / f"{identifiant}.md"
        if not fiche.exists():
            erreur(f"style `{identifiant}` : fiche references/styles/{identifiant}.md manquante")
        if f"`{identifiant}`" not in texte_menu:
            erreur(f"style `{identifiant}` absent du menu de SKILL.md")
        if f"`{identifiant}`" not in texte_index:
            avertir(f"style `{identifiant}` non mentionné dans style-index.md")

    # fiches orphelines (présentes sans être déclarées)
    dossier = RACINE / "references" / "styles"
    if dossier.is_dir():
        for fiche in dossier.glob("*.md"):
            if fiche.stem not in styles:
                erreur(f"fiche references/styles/{fiche.name} sans entrée dans corpus-styles.json")


def verifier_index(carte: dict) -> None:
    index = RACINE / "references" / "corpus-index.json"
    if not index.exists():
        erreur("references/corpus-index.json absent (lancer scripts/build_corpus.py)")
        return
    donnees = json.loads(index.read_text(encoding="utf-8"))
    exemples = donnees.get("exemples", [])
    if not exemples:
        erreur("corpus-index.json : aucun exemple")
        return
    if donnees.get("total") != len(exemples):
        erreur(f"corpus-index.json : total={donnees.get('total')} mais {len(exemples)} exemples")
    connus = set(carte.get("videos", {}).values())
    styles_index = {e.get("style") for e in exemples}
    inconnus = styles_index - connus
    if inconnus:
        erreur(f"corpus-index.json : styles inconnus {sorted(inconnus)}")
    manquants = connus - styles_index
    if manquants:
        erreur(f"styles déclarés sans exemple dans l'index : {sorted(manquants)}")
    for e in exemples:
        if len(e.get("hook", "")) < 10:
            avertir(f"{e.get('id')} : accroche absente ou trop courte dans l'index")


def verifier_scripts() -> None:
    for script in sorted((RACINE / "scripts").glob("*.py")):
        compilation = subprocess.run([sys.executable, "-m", "py_compile", str(script)],
                                     capture_output=True, text=True)
        if compilation.returncode != 0:
            erreur(f"{script.name} ne compile pas : {compilation.stderr.strip()[:200]}")
            continue
        aide = subprocess.run([sys.executable, str(script), "--help"],
                              capture_output=True, text=True, timeout=30)
        if aide.returncode != 0:
            erreur(f"{script.name} --help échoue : {aide.stderr.strip()[:200]}")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Auto-vérification du skill.")
    ap.add_argument("--quiet", action="store_true",
                    help="n'afficher que les erreurs et le verdict")
    args = ap.parse_args()

    verifier_frontmatter()
    verifier_chemins()
    carte = charger_styles()
    if carte:
        verifier_styles(carte)
        verifier_index(carte)
    verifier_scripts()

    if not args.quiet:
        for message in avertissements:
            print(f"⚠  {message}")
    for message in erreurs:
        print(f"❌ {message}")
    if erreurs:
        print(f"\n{len(erreurs)} erreur(s), {len(avertissements)} avertissement(s)")
        return 1
    if not args.quiet:
        print(f"✅ Skill valide ({len(avertissements)} avertissement(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())