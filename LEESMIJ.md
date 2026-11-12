# Torelkiva 1.2 — installatie en gebruik

## Wat heb je nodig?

- Windows 10/11 of een recente Linux-versie.
- Python **3.9 of nieuwer**. Op Windows: [python.org](https://www.python.org/downloads/) of je eigen pakketbeheerder.
- De Python-bibliotheek `cryptography` voor encryptie.

Download de projectbestanden via GitHub (**Code → Download ZIP**) en pak ze uit. Open een terminal in deze map.

Installeer de bibliotheek:

```bash
python -m pip install -r requirements.txt
```

Op sommige Windows-computers gebruik je `py -3` in plaats van `python`; op Linux `python3`.

## Onze taal leren

```bash
python taal.py lijst
python taal.py zoek begrijpen
python taal.py woord nela
python taal.py voorbeelden
python taal.py oefen
```

De zoekfunctie zoekt woorden, maar **vertaalt niet automatisch hele Nederlandse zinnen**. Gebruik de [grammatica](GRAMMATICA.md) en het [oefenboek](OEFENBOEK.md).

## Een bericht versleutelen

```bash
python torelkiva.py versleutel
```

Voer één regel tekst in, kies een lange geheime wachtzin en herhaal de wachtzin. Kopieer de `TK1:`-code voor de ontvanger. De ontvanger heeft dezelfde geheime wachtzin nodig.

Om te ontsleutelen:

```bash
python torelkiva.py ontsleutel
```

Plak de complete `TK1:`-code en geef dezelfde wachtzin op.

### Tekst met meerdere regels

Je kunt meerregelige tekst of codes via standaardinvoer aanleveren:

```bash
python torelkiva.py versleutel --stdin < brief.txt
python torelkiva.py ontsleutel --stdin < code.txt
```

Let op: de wachtzin wordt **niet** als commandoregelargument ingevoerd, maar wordt interactief gevraagd. Voor interactieve prompts is een terminal nodig; bij automatische scripts kan `getpass` daarom ontbreken.

### Kleine bestanden

```bash
python torelkiva.py versleutel --bestand bericht.txt
python torelkiva.py ontsleutel --bestand bericht.txt.tkv
```

Dat maakt `bericht.txt.tkv` en later `bericht.txt.ontsleuteld`. Bestanden zijn maximaal 50 MiB; bestaande bestanden worden nooit automatisch overschreven en oorspronkelijke bestanden blijven bestaan. Deel geen geheimen op GitHub.

## Schrift maken

```bash
python schrift.py "Mi Torelkivaem vara."
```

Daarna bestaat `TOREL_BERICHT.svg`. Dit bestand kun je openen in een webbrowser. Het schrift is een visuele lettercode en **geen encryptie**.

## Testen

```bash
python -m unittest discover -s tests -v
```

De basisversie `TK1:` uit versie 1.1 blijft leesbaar in deze versie. Bewaar je wachtzin veilig. Zie [VEILIGHEID.md](VEILIGHEID.md) voor beperkingen.