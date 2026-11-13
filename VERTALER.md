# Gecontroleerde vertaler — specificatie 2.2

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

**Niet ondersteund:** hele verhalen, meerdere zinnen tegelijk, volledige Nederlandse syntaxis, samengestelde tijden, variabele lidwoordbetekenissen, meerdere voorwerpen, bijzinnen, meervoudige voorwerpen en alle woorden uit het 373-woordenboek. Dit zijn expliciete grenzen, geen stilzwijgende aannames.

## Lidwoorden en persoonlijke voornaamwoorden sinds 2.2

De eerdere vertaler verloor het verschil tussen *een boek* en *het boek*. Vanaf versie 2.2 zijn er twee **optionele** Torelkiva-deeltjes:

- `da` = bepaald lidwoord *de/het*: `Mi da laviem lona.` = *Ik lees het boek.*
- `en` = onbepaald lidwoord *een*: `Mi en ravoem vara.` = *Ik spreek een taal.*

Oude zinnen zonder deeltjes blijven geldig. De vertaler voegt een deeltje toe wanneer het Nederlandse lidwoord afwijkt van het oudere standaardlidwoord. Daarom blijft `Mi laviem lona.` *Ik lees een boek.* Ook grammaticale fouten als *de boek* worden geweigerd. Bij *geen boek* gebruik je nog steeds `vo`, zonder lidwoorddeeltje.

`eli` staat nu voor *zij (enkelvoud)* en `eliem` voor *haar*. De oude vormen `ela`/`elaem` blijven ondersteund en worden standaard *hij*/*hem*; hierdoor behouden oudere berichten hun leesbaarheid. `tira` blijft *zij (meervoud)*. De software leidt de betekenis van Nederlands *zij* af uit de persoonsvorm, bijvoorbeeld *zij slaapt* versus *zij slapen*.

Let op: de vertaler blijft beperkt tot één eenvoudige zin en een klein gedefinieerd vertaaldomein. Het is geen vertaler voor alle 373 woorden.

## Technische API

- `to_torelkiva(zin: str) -> str`
- `to_nederlands(zin: str) -> str`
- `parse_nederlands(zin: str) -> Parsed`
- `parse_torel(zin: str) -> Parsed`
- `UnsupportedSentenceError` bij niet-ondersteunde invoer.

De code gebruikt alleen de standaardbibliotheek en werkt volledig offline.

## Correcties in versie 2.2

- Nederlandse toekomende tijd gebruikt het werkwoord aan het einde: `Ik zal een boek lezen.` ↔ `Mi laviem sa lona.`
- Vorm `groot` krijgt waar nodig `grote` (nooit `groote`).
- De gecontroleerde vertaler weigert dubbele ontkenningen en onlogische modifiers.
- `ela` blijft historisch genderneutraal maar wordt canoniek met `hij`/`hem` weergegeven. Nieuwe zinnen kunnen met `eli`/`eliem` en `da`/`en` beter onderscheid maken.
- De vertaler geeft **geen garantie van betekenisbehoud bij alle Nederlandse zinnen**, onder meer vanwege ontbrekende lidwoorden in Torelkiva.

### Beperkingen bij werkwoorden

Werkwoorden zoals `suri` (slapen), `gala` (gaan) en `sira` (luisteren) krijgen in het gecontroleerde vertaaldomein **geen direct voorwerp**. Een zin als *Ik slaap een boek* wordt geweigerd. Constructies met een voorzetsel, zoals *ik luister naar muziek*, vragen een uitbreiding van de vertaler. Ook bij technisch juiste grammatica wordt niet elke betekenisinhoud automatisch gecontroleerd.

**Nederlandse lidwoordcontrole:** in gewone Nederlandse zinnen met een enkelvoudig telbaar voorwerp is `de`, `het`, `een` of `geen` verplicht. `Ik lees boek` wordt daarom afgewezen. In het oudere Torelkiva kan een lidwoorddeeltje wel ontbreken; dit blijft ondersteund.
