#!/usr/bin/env bash
set -u
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is niet gevonden. Installeer eerst Python 3.9 of nieuwer."
  exit 1
fi
while true; do
  printf '\n===== TORELKIVA 1.2 =====\n1. Zoek woorden\n2. Oefen Torelkiva\n3. Versleutel tekst\n4. Ontsleutel tekst\n5. Bekijk Torel-alfabet\n6. Afsluiten\n'
  read -r -p 'Kies een optie (1-6): ' keuze || exit 0
  case "$keuze" in
    1) read -r -p 'Zoekwoord: ' woord; python3 taal.py zoek "$woord" ;;
    2) python3 taal.py oefen ;;
    3) python3 torelkiva.py versleutel ;;
    4) python3 torelkiva.py ontsleutel ;;
    5) if command -v xdg-open >/dev/null 2>&1; then
         xdg-open TOREL_ALFABET.svg 2>/dev/null || echo 'Open TOREL_ALFABET.svg handmatig.'
       else
         echo 'Open TOREL_ALFABET.svg in je browser.'
       fi ;;
    6) exit 0 ;;
    *) echo 'Kies een getal van 1 t/m 6.' ;;
  esac
done
