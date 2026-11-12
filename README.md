# TORELKIVA 2.0 — kunsttaal, schrift en versleuteling

> **Torelkiva — ontwikkeld op initiatief van Marco Beenen in samenwerking met ChatGPT (OpenAI), begonnen op 12 november 2026.**  
> Versie **2.0** — openbare projecteditie; volledig lokaal bruikbaar op Windows en Linux.  
> **Geen officiële OpenAI-goedkeuring, merkregistratie of onafhankelijke beveiligingsaudit.**

**Torelkiva** is een fictieve, ontworpen kunsttaal met een originele woordenlijst, vaste basisgrammatica en een grafisch letterschrift. De optionele encryptietool is een apart programma: een geheim alfabet is geen cryptografie.

**English:** *Torelkiva is a constructed language initiated by Marco Beenen and developed with the assistance of ChatGPT (OpenAI), starting 12 November 2026. It has its own vocabulary, grammar, visual writing system and a separate local encryption tool.*

## Dit zit in versie 2.0

- **370 unieke woorden** in `WOORDENLIJST.tsv`; 149 oorspronkelijke woorden zijn behouden.
- Een gedocumenteerde **basisgrammatica**, controle van vervoegingen en een systematische uitspraakgids.
- **Gecontroleerde vertaler** `vertaler.py`: Nederlands ↔ Torelkiva voor eenvoudige, ondersteunde zinsvormen. Geen vertaler voor willekeurige Nederlandse tekst; onbekende zinnen leveren een duidelijke foutmelding.
- **Desktopprogramma met knoppen** `app.py`: vertalen, zoeken, Torel-schrift als SVG, en TK1-berichten versleutelen/ontsleutelen.
- **Eigen letterschrift** voor a–z, inclusief voorbeeld, letteroverzicht en SVG-generator `schrift.py`.
- **Offline miniwoordenboek** `offline.html`, lokaal in een browser te openen. Geen mobiele encryptie in deze pagina.
- **Echte optionele encryptie** `torelkiva.py` (AES-256-GCM + scrypt); bestaande TK1-berichten uit 1.1/1.2 blijven compatibel met dezelfde wachtzin.
- Documentatie, oefenboek, technische tests en controlehashes.

## Snel beginnen

Installeer Python 3.9+ en, voor versleuteling:

```bash
python -m pip install -r requirements.txt
```

**Desktopprogramma (Windows / Linux met Tkinter):**

```bash
python app.py
```

Op Windows kun je `START_WINDOWS.bat` openen. Op Linux: `bash START_LINUX.sh`.

**Vertaler (gecontroleerde zinnen):**

```bash
python vertaler.py --van nl "Ik begrijp jou niet."
python vertaler.py --van tk "Mi tiem vo nela."
```

**Woordenboek:**

```bash
python taal.py zoek geheim
python taal.py oefen
```

**Versleutelen:**

```bash
python torelkiva.py versleutel
python torelkiva.py ontsleutel
```

**Tests:**

```bash
python -m unittest discover -s tests -v
```

## De taal: enkele voorbeelden

| Nederlands | Torelkiva |
|---|---|
| Hallo! | `Vema!` |
| Ik begrijp jou niet. | `Mi tiem vo nela.` |
| Wij spreken de geheime taal. | `Miva sima ravoem vara.` |
| Wij schrijven een nieuw woord. | `Miva nori mevaem mero.` |
| Begrijp jij mij? | `Ti miem nela ke?` |

Kernregel: **onderwerp → voorwerp → tijd → ontkenning → werkwoord**. `-em` markeert het voorwerp, `-in` het meervoud, `na` het verleden en `sa` de toekomst. Zie [GRAMMATICA.md](GRAMMATICA.md).

## Belangrijke grenzen

- Een woordenboek van 370 woorden is **geen volledige menselijke spreektaal**. De zinsvertaler ondersteunt een veel kleinere, expliciet vastgelegde deelverzameling; hij gebruikt niet elk woord uit de lijst automatisch.
- Het schrift is een **letteromzetting**. Alleen de aparte encryptietool versleutelt berichten. Deze software is **niet onafhankelijk geaudit**: gebruik haar niet als enige beveiligingsmaatregel voor hooggevoelige informatie.
- Er is **geen open-sourcelicentie** toegevoegd: GitHub-publicatie betekent niet automatisch dat alle rechten worden vrijgegeven.
- Een GitHub-commit registreert publicatie en versies, maar is geen officiële merkregistratie of juridisch sluitend eigendomsbewijs.

## Documentatie

- [LEESMIJ.md](LEESMIJ.md) — installatie en bediening
- [GRAMMATICA.md](GRAMMATICA.md) — grammatica, getallen, zinsvormen
- [WOORDENBOEK.md](WOORDENBOEK.md) — 370 woorden en hun betekenissen
- [OEFENBOEK.md](OEFENBOEK.md) — voorbeelden en opdrachten
- [VERTALER.md](VERTALER.md) — wat de gecontroleerde vertaler precies ondersteunt
- [VEILIGHEID.md](VEILIGHEID.md) — bedreigingsmodel en cryptografie
- [HERKOMST.md](HERKOMST.md) — oorsprong van het project
- [ONTWIKKELINGSVERKLARING.md](ONTWIKKELINGSVERKLARING.md) — particuliere verklaring
- [CHANGELOG.md](CHANGELOG.md) — versiegeschiedenis
- [CITATION.cff](CITATION.cff) — projectvermelding

**Gemaakt om mee te spelen, te leren en verder te ontwikkelen.**
