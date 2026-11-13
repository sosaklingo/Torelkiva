# Torelkiva 2.1 — installeren en gebruiken

## Benodigdheden

- **Windows 10/11** of een recente **Linux**-installatie.
- **Python 3.9+**. Voor het grafische programma is **Tkinter** nodig (bij sommige Linux-distributies: `sudo apt install python3-tk`).
- Voor versleuteling: `python -m pip install -r requirements.txt` (installeert de `cryptography`-bibliotheek).
- Internet is alleen nodig om software en bestanden te downloaden, **niet** om je eigen berichten te verwerken.

## 1. Programma openen

Windows: dubbelklik op `START_WINDOWS.bat` of voer `py -3 app.py` uit. Linux: `bash START_LINUX.sh` of `python3 app.py`.

```bash
python app.py
```

Het desktopprogramma bevat tabs **Vertalen**, **Woordenboek**, **Torel-schrift** en **Versleutelen**. Een wachtzin wordt niet in een bestand opgeslagen.

## 2. Op een iPhone of andere telefoon

De Python-desktopapp draait **niet** rechtstreeks in de standaard iPhone-apps. Het meegeleverde `offline.html` bevat een **offline woordenboek, voorbeeldzinnen en een schriftweergave** zonder server; open het HTML-bestand in een geschikte browser of webviewer. **Encryptie is bewust niet opgenomen in de browserpagina**; die functie blijft bij de lokale Python-tool.

## 3. Woordenboek en vertaler in terminal

```bash
python taal.py zoek geheim
python taal.py lijst
python taal.py oefen
python vertaler.py --van nl "Ik lees een boek."
python vertaler.py --van tk "Mi laviem lona."
```

De vertaler verwerkt een **beperkt, gecontroleerd zinstype**: zie `VERTALER.md`. Een melding *Niet ondersteund* betekent dat de zin buiten dat bereik valt, niet dat je geheim mislukt is.

## 4. Berichten versleutelen

```bash
python torelkiva.py versleutel
python torelkiva.py ontsleutel
```

Gebruik een unieke, lange wachtzin; laat die **niet** in een GitHub-bestand staan. De uitvoercode begint met `TK1:`. Voor oude 1.1/1.2-berichten gebruik je dezelfde wachtzin. De wachtzin kan niet worden teruggehaald als je hem vergeet.

Kleine bestanden (maximaal 50 MiB) via:

```bash
python torelkiva.py versleutel --bestand voorbeeld.txt
python torelkiva.py ontsleutel --bestand voorbeeld.txt.tkv
```

Originele bestanden blijven staan; de tool wist ze niet. Hij overschrijft bestaande uitvoerbestanden niet. Voor meerdere regels via terminal is `--stdin` beschikbaar, mits een interactieve terminal voor de wachtzin aanwezig is.

## 5. Het Torel-schrift als SVG

```bash
python schrift.py "Mi viroem sila."
```

Er verschijnt `TOREL_BERICHT.svg`, te openen in een browser. Maximaal 2.000 invoertekens per afbeelding.

## 6. Tests

```bash
python -m unittest discover -s tests -v
```

## Problemen oplossen

- `ModuleNotFoundError: cryptography`: voer `python -m pip install -r requirements.txt` uit met **dezelfde Python** die je gebruikt om het programma te starten.
- `No module named tkinter`: installeer Tkinter; onder Linux vaak `python3-tk`.
- `couldn't connect to display`: een grafisch desktopprogramma kan niet in een terminal zonder scherm geopend worden; gebruik de CLI-tools.
- `Niet ondersteund`: probeer een korte voorbeeldzin uit `VERTALER.md`.
- `Onjuiste wachtzin of beschadigd bericht`: controleer wachtzin en complete `TK1:`-code; brute force is niet bedoeld.
- `File exists`: de tool beschermt bestaande uitvoerbestanden tegen overschrijven.

Zie `VEILIGHEID.md` voor de beperkingen en waarschuwingen.

## Nieuwe PDF-handleiding (versie 2.1)

Open `Torelkiva_Handleiding_2_1.pdf` voor de actuele Nederlandstalige gids. De PDF met versie 2.0 blijft alleen beschikbaar als historische uitgave.
