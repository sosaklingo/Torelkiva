#!/usr/bin/env bash
set -u
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3 is niet gevonden. Installeer eerst Python 3.9 of nieuwer.'
  exit 1
fi
while true; do
  printf '\n===== TORELKIVA 2.0 =====\n1. Open grafisch programma\n2. Vertaal een Nederlandse zin\n3. Zoek een woord\n4. Oefen Torelkiva\n5. Versleutel bericht\n6. Ontsleutel bericht\n7. Bekijk Torel-alfabet\n8. Afsluiten\n'
  read -r -p 'Kies een optie (1-8): ' keuze || exit 0
  case "$keuze" in
    1) python3 app.py ;;
    2) read -r -p 'Nederlandse zin: ' zin; python3 vertaler.py --van nl "$zin" ;;
    3) read -r -p 'Zoekwoord: ' woord; python3 taal.py zoek "$woord" ;;
    4) python3 taal.py oefen ;;
    5) python3 torelkiva.py versleutel ;;
    6) python3 torelkiva.py ontsleutel ;;
    7) if command -v xdg-open >/dev/null 2>&1; then
         xdg-open TOREL_ALFABET.svg 2>/dev/null || echo 'Open TOREL_ALFABET.svg handmatig.'
       else
         echo 'Open TOREL_ALFABET.svg in je browser.'
       fi ;;
    8) exit 0 ;;
    *) echo 'Kies een getal van 1 t/m 8.' ;;
  esac
done
