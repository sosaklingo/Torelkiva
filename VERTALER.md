# Gecontroleerde vertaler — specificatie 2.1

## Waarom niet elke Nederlandse zin?

Een automatische vertaler zonder complete grammatica en betekenissen kan overtuigende **verkeerde** vertalingen produceren. Daarom ondersteunt `vertaler.py` alleen een expliciet afgebakend zinstype. Onbekende vormen leiden tot `UnsupportedSentenceError` (CLI-uitvoer: *Niet ondersteund*).

## Voorbeelden

```bash
python vertaler.py --van nl "Ik begrijp jou niet."
# Mi tiem vo nela.

python vertaler.py --van tk "Ti miem nela ke?"
# Begrijp jij mij?

python vertaler.py --van nl "Wij schrijven een nieuw woord."
# Miva nori mevaem mero.
```

De vertaler verwerkt een onderwerp, één vervoegd werkwoord, optioneel één bijvoeglijk naamwoord en één voorwerp, en optioneel tijdsmarkering/ontkenning/vraag. De ondersteunde werkwoorden staan expliciet in `vertaler.py` met hun Nederlandse vervoegingen.

**Niet ondersteund:** hele verhalen, meerdere zinnen tegelijk, volledige Nederlandse syntaxis, samengestelde tijden, variabele lidwoordbetekenissen, meerdere voorwerpen, bijzinnen, meervoudige voorwerpen en alle woorden uit het 370-woordenboek. Dit zijn expliciete grenzen, geen stilzwijgende aannames.

## Nederlands: lidwoorden en nuance

Torelkiva gebruikt geen de/het/een. Bijvoorbeeld: *het bericht* en *een bericht* worden allebei `viro`. Terugvertalen kan niet beide nuances herstellen. De vertaler toont daarom bij `viroem` standaard *een bericht*, ook wanneer de oorspronkelijke Nederlandse zin *het bericht* was. Bij ontkenning wordt vaak *geen bericht* gekozen. De betekenis blijft begrijpelijk, maar niet altijd letterlijk identiek.

## Technische API

- `to_torelkiva(zin: str) -> str`
- `to_nederlands(zin: str) -> str`
- `parse_nederlands(zin: str) -> Parsed`
- `parse_torel(zin: str) -> Parsed`
- `UnsupportedSentenceError` bij niet-ondersteunde invoer.

De code gebruikt alleen de standaardbibliotheek en werkt volledig offline.

## Correcties in versie 2.1

- Nederlandse toekomende tijd gebruikt het werkwoord aan het einde: `Ik zal een boek lezen.` ↔ `Mi laviem sa lona.`
- Vorm `groot` krijgt waar nodig `grote` (nooit `groote`).
- De gecontroleerde vertaler weigert dubbele ontkenningen en onlogische modifiers.
- `ela` is genderneutraal, maar de Nederlandse terugvertaler kiest canoniek `hij` of `hem`. Daardoor kan informatie over geslacht en artikelgebruik verloren gaan.
- De vertaler geeft **geen garantie van betekenisbehoud bij alle Nederlandse zinnen**, onder meer vanwege ontbrekende lidwoorden in Torelkiva.
