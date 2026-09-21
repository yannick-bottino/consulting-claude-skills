#!/usr/bin/env python3
"""
file-naming-standard — assemblage déterministe du nom de fichier.

Convention :
    <Client> x <Cabinet>_<Mission> - <Livrable>_YYYYMMDD.<ext>

Livrable interne (sans client) :
    <Cabinet>_<Mission> - <Livrable>_YYYYMMDD.<ext>

Le nom du cabinet se configure une fois, via --firm ou la variable
environnement FIRM_NAME.

Usage :
    FIRM_NAME="Mon Cabinet" python build_filename.py \
        --client "Meridian Retail" \
        --mission "Transformation IA" \
        --deliverable "Diagnostic de maturité" \
        --ext pptx
        [--date 20260616] [--ascii] [--collision-dir /mnt/user-data/outputs]
"""
import argparse
import datetime
import os
import re
import sys
import unicodedata

# Séparateur entre Mission et Livrable.
# Le ":" de la spec d'origine est INTERDIT (illégal Windows + SharePoint/OneDrive),
# remplacé ici par " - " (trait d'union simple, PAS un em-dash).
# Pour changer de séparateur, le faire UNIQUEMENT ici.
SEP_MISSION_LIVRABLE = " - "

# Caractères interdits : réservés Windows + SharePoint/OneDrive, + caractères de contrôle.
ILLEGAL = r'[<>:"/\\|?*\x00-\x1f]'
MAX_COMPONENT = 255  # limite d'un composant de chemin (Windows)
# Nom du cabinet insere dans chaque nom de fichier. Surchargeable par --firm.
DEFAULT_FIRM = os.environ.get("FIRM_NAME", "Firm")
INTERNAL_ALIASES = {"interne", "internal", ""}


def sanitize(text, ascii_fold=False):
    """Nettoie un composant : retire les caractères illégaux, normalise les espaces."""
    if text is None:
        text = ""
    text = str(text).strip()
    if ascii_fold:
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(ILLEGAL, " ", text)        # illégaux -> espace
    text = re.sub(r"\s+", " ", text).strip()  # espaces multiples -> simple
    text = text.rstrip(". ")                  # pas de point/espace en fin
    return text


def build(client, mission, deliverable, date=None, ext=None, ascii_fold=False,
          firm=None):
    firm = sanitize(firm or DEFAULT_FIRM, ascii_fold)
    client = sanitize(client, ascii_fold)
    mission = sanitize(mission, ascii_fold)
    deliverable = sanitize(deliverable, ascii_fold)

    if not mission or not deliverable:
        raise ValueError("Mission et livrable sont obligatoires.")

    if date is None:
        date = datetime.date.today().strftime("%Y%m%d")
    else:
        date = re.sub(r"\D", "", str(date))
        if len(date) != 8:
            raise ValueError("Date invalide : %r (attendu YYYYMMDD)." % date)

    interne = client.lower() in INTERNAL_ALIASES or client.lower() == firm.lower()
    prefix = firm if interne else ("%s x %s" % (client, firm))

    stem = "%s_%s%s%s_%s" % (prefix, mission, SEP_MISSION_LIVRABLE, deliverable, date)

    ext = (ext or "").lstrip(".").strip()
    name = "%s.%s" % (stem, ext) if ext else stem

    if len(name) > MAX_COMPONENT:
        sys.stderr.write(
            "[warn] nom de fichier > %d caracteres (%d). "
            "Raccourcir l'intitule du livrable.\n" % (MAX_COMPONENT, len(name))
        )
    return name, stem, ext


def resolve_collision(stem, ext, directory):
    """Retourne un nom non collisionnant en suffixant _v2, _v3, ... si besoin."""
    def make(n):
        s = stem if n == 1 else "%s_v%d" % (stem, n)
        return "%s.%s" % (s, ext) if ext else s

    n = 1
    while os.path.exists(os.path.join(directory, make(n))):
        n += 1
    return make(n)


def main():
    p = argparse.ArgumentParser(description="Nommage standard des livrables.")
    p.add_argument("--client", default="", help="nom du client (vide = interne)")
    p.add_argument("--firm", default=None,
                   help="nom du cabinet (defaut : $FIRM_NAME, sinon Firm)")
    p.add_argument("--mission", required=True)
    p.add_argument("--deliverable", required=True)
    p.add_argument("--date", default=None, help="YYYYMMDD (defaut : aujourd'hui)")
    p.add_argument("--ext", default=None, help="extension, ex. pptx")
    p.add_argument("--ascii", action="store_true", help="replier les accents en ASCII")
    p.add_argument("--collision-dir", default=None,
                   help="dossier ou verifier les collisions et suffixer _vN")
    args = p.parse_args()

    name, stem, ext = build(
        args.client, args.mission, args.deliverable,
        date=args.date, ext=args.ext, ascii_fold=args.ascii, firm=args.firm,
    )
    if args.collision_dir and os.path.isdir(args.collision_dir):
        name = resolve_collision(stem, ext, args.collision_dir)
    print(name)


if __name__ == "__main__":
    main()
