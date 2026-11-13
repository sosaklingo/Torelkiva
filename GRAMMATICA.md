# Torelkiva — normatieve basisgrammatica 2.2

**Start:** 12 november 2026. **Initiatiefnemer:** Marco Beenen; uitgewerkt met ChatGPT (OpenAI).

Dit is de **vastgelegde grammatica voor het basisdomein**, niet een belofte dat alle denkbare menselijke zinnen of dialecten al zijn uitgewerkt. De sectie *Vertaaldomein* geeft aan wat software automatisch kan verwerken.

## 1. Schrijfwijze en uitspraak

- De basiswoorden gebruiken kleine Latijnse letters; geen letter is stil. De klanken `a, e, i, o, u` worden duidelijk uitgesproken. De `r` is kort rollend.
- Klemtoon meestal op de voorlaatste lettergreep: `ve-ma`, `to-rel-ki-va`.
- Eigennamen mogen hoofdletters gebruiken. `Torelkivaem` krijgt dezelfde voorwerpsuitgang als gewone naamwoorden.
- Vraagzin eindigt op `ke?`, mededeling op `.`, groet op `!`.
- Het visuele Torel-schrift vervangt uitsluitend letters, niet de grammatica.

## 2. Basiszin

**Onderwerp + (bepalingen) + (lidwoorddeeltje + bijvoeglijk naamwoord + voorwerp) + (tijd) + (ontkenning) + werkwoord + (vraagpartikel).**

| Torelkiva | Nederlands |
|---|---|
| `Mi suri.` | Ik slaap. |
| `Mi viroem mero.` | Ik schrijf een bericht. |
| `Miva nori mevaem mero.` | Wij schrijven een nieuw woord. |
| `Mi viroem na mero.` | Ik schreef een bericht. |
| `Ti viroem sa lona.` | Jij zult een bericht lezen. |
| `Mi viroem na vo mero.` | Ik schreef geen bericht. |
| `Ti miem nela ke?` | Begrijp jij mij? |

Het werkwoord wordt niet vervoegd naar persoon of meervoud. De oude basis gebruikte geen lidwoorden; vanaf 2.2 zijn `da` en `en` **optionele lidwoorddeeltjes**. Daarnaast is `eli` beschikbaar voor de vrouwelijke enkelvoudsvorm, naast het oudere genderneutrale `ela`.

## 3. Naamwoorden en voornaamwoorden

- Enkelvoud: `viro` = bericht. Meervoud: `viroin` = berichten.
- Lijdend voorwerp: `viroem` = bericht als object. Meervoudig object: `viroinem`.
- Volgorde van uitgangen: **stam + `-in` + `-em`**.
- Bijvoeglijk naamwoord vóór de stam, zonder uitgang: `nori viroem` = nieuw bericht als object.
- Voornaamwoorden: `mi` (ik), `ti` (jij), `miva` (wij), `tira` (zij meervoud), `ela` (hij/zij/het, genderneutraal in oudere versies), `eli` (zij enkelvoud; vanaf 2.2).
- Voorwerpsvormen: `miem`, `tiem`, `mivaem`, `tiraem`, `elaem`, `eliem` (haar).
- De oude zinnen **zonder lidwoorddeeltje** blijven behouden en gebruiken een standaardlidwoord bij terugvertaling.
- Vanaf 2.2 kan een lidwoorddeeltje de nuance behouden: `da` = *de/het*, `en` = *een*. Gebruik dit vóór het bijvoeglijk naamwoord of voorwerp, bijvoorbeeld `Mi da nori laviem lona.` = *Ik lees het nieuwe boek.* en `Mi en ravoem vara.` = *Ik spreek een taal.* De juiste keuze tussen *de* en *het* volgt uit het Nederlandse zelfstandige naamwoord; foutieve combinaties worden geweigerd.
- Bij **geen** blijft de bestaande ontkenning `vo` in gebruik, zonder lidwoorddeeltje: `Mi laviem vo lona.` = *Ik lees geen boek.*

## 4. Tijd, ontkenning, vragen

- Tegenwoordige tijd: **geen markering**; `Mi viroem mero.`
- Verleden: `na` direct vóór eventuele ontkenning en het werkwoord; `Mi viroem na mero.`
- Toekomst: `sa` op dezelfde plek; `Mi viroem sa mero.`
- Ontkenning: `vo` direct vóór het werkwoord; `Mi viroem sa vo mero.`
- Ja/nee-vraag: `ke` aan het einde, vlak vóór `?`: `Ti miem nela ke?`
- Vraagwoorden in de woordenlijst zijn `meka`, `kiva`, `nera`, `toma`, `siva` en `navi`; hun volledige zinsbouw is **nog niet automatisch vertaald**.
- Voor een zinsdeel gebruik je maximaal één tijdsdeeltje. `na` en `sa` tegelijk is fout.

## 5. Bepalingen en achterzetsels

- `nori viro` = nieuw bericht.
- `Mi vado suri.` = Ik slaap nu.
- Achterzetsels volgen hun naamwoordgroep: `mora ri` = in huis, `mora la` = op het huis, `ti lo` = met jou, `nava ta` = naar de stad, `mi di` = van mij.
- Een bepaling staat vóór het lijdend voorwerp of vóór het werkwoord. Voorbeeld: `Mi mora ri suri.` = Ik slaap in huis.
- Een bezit kan met `di` worden omschreven: `mi di mora` = mijn huis (letterlijk: huis van mij), maar complex bezit en geneste zinnen blijven buiten de automatische vertaler.

## 6. Getallen 0–99 (nieuwe conventie)

| Waarde | Torelkiva |
|---|---|
| 0 | zena |
| 1 t/m 9 | una, duna, trina, karo, pema, sesa, seva, oka, nova |
| 10 | desa |
| 11 | desa-una |
| 19 | desa-nova |
| 20 | duna-desa |
| 21 | duna-desa-una |
| 90 | nova-desa |
| 99 | nova-desa-nova |

Het koppelteken maakt één telwoord van meerdere delen. Er bestaan in versie 2.2 **geen officiële vormen boven 99**. Getallen worden vóór een naamwoord geplaatst: `duna lumain` = twee vrienden. De vertaler herkent getallen nog niet in zinnen.

## 7. Meerdere zinnen, voegwoorden en grenzen

`e` = en, `o` = of, `ba` = maar. Hiermee kun je eenvoudige woordgroepen naast elkaar zetten, bijvoorbeeld `mi e ti` = ik en jij. De automatische vertaler ondersteunt **geen** zinnen met meer dan één persoonsvorm, bijzinnen, passieve vormen, samengestelde tijden, uitgebreide betrekkelijke voornaamwoorden of vrij gevormde vraagzinnen.

## 8. Vertaaldomein 2.2

De vertaler in `vertaler.py` accepteert:

- één zin met `mi/ti/miva/ela/eli/tira` of een ondersteund Nederlands onderwerp;
- een van de ingebouwde werkwoorden en nul of één lijdend voorwerp;
- optioneel één bijvoeglijk naamwoord;
- heden, eenvoudig verleden, toekomst, ontkenning en ja/nee-vraag;
- enkele bekende eigennamen, groeten en vaste woorden.

Niet-ondersteunde constructies geven **expliciet een fout**. De volledige woordenlijst van 373 woorden bevat ook woorden die de vertaler niet automatisch kan vervoegen of combineren. Zie [VERTALER.md](VERTALER.md). Deze beperking is belangrijk: een kunsttaal kan verder groeien zonder dat de software een foutieve automatische vertaling presenteert.

### Beperkingen bij werkwoorden

Werkwoorden zoals `suri` (slapen), `gala` (gaan) en `sira` (luisteren) krijgen in het gecontroleerde vertaaldomein **geen direct voorwerp**. Een zin als *Ik slaap een boek* wordt geweigerd. Constructies met een voorzetsel, zoals *ik luister naar muziek*, vragen een uitbreiding van de vertaler. Ook bij technisch juiste grammatica wordt niet elke betekenisinhoud automatisch gecontroleerd.

**Nederlandse lidwoordcontrole:** in gewone Nederlandse zinnen met een enkelvoudig telbaar voorwerp is `de`, `het`, `een` of `geen` verplicht. `Ik lees boek` wordt daarom afgewezen. In het oudere Torelkiva kan een lidwoorddeeltje wel ontbreken; dit blijft ondersteund.
