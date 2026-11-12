#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
while true; do
  printf '\n--- TORELKIVA 1.1 ---\n1. Tekst versleutelen\n2. Tekst ontsleutelen\n3. Alfabet bekijken\n4. Stoppen\n'
  read -r -p 'Kies 1-4: ' keuze
  case "$keuze" in
    1) python3 torelkiva.py versleutel ;;
    2) python3 torelkiva.py ontsleutel ;;
    3) xdg-open TOREL_ALFABET.svg 2>/dev/null || echo "Open TOREL_ALFABET.svg in de browser" ;;
    4) exit 0 ;;
    *) echo 'Ongeldige keuze.' ;;
  esac
done
