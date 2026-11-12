# TORELKIVA 1.1 — taal + echte berichtversleuteling

Deze map bevat:

- `WOORDENBOEK.md` – originele woorden, grammatica en voorbeelden.
- `torelkiva.py` – versleutelen / ontsleutelen van berichten en bestanden.
- `schrift.py` – letters tekenen in een eigen visueel Torel-schrift (SVG).
- `TOREL_ALFABET.svg` – overzicht van het nieuwe schrift.
- `VOORBEELD_TOREL.svg` – voorbeeldzin in dat schrift.
- `START_WINDOWS.bat` en `START_LINUX.sh` – eenvoudig startmenu.

## Installatie

Python 3.9+ nodig. Voor de **versleuteling** is één extra Python-bibliotheek nodig:

```bash
python -m pip install cryptography
```

Op Linux gebruik je eventueel `python3` en `python3 -m pip`.

## Gebruik (Windows en Linux)

Dubbelklik op `START_WINDOWS.bat` op Windows of start `bash START_LINUX.sh`
op Linux. Of werk direct in een terminal:

```bash
python torelkiva.py versleutel
python torelkiva.py ontsleutel
```

De tool vraagt daarna de tekst en je geheime wachtzin. De tool **slaat die
wachtzin nergens op**. Om hetzelfde bericht te lezen moet de ontvanger
precies dezelfde wachtzin kennen.

### Bestanden versleutelen

```bash
python torelkiva.py versleutel --bestand bericht.txt
python torelkiva.py ontsleutel --bestand bericht.txt.tkv
```

De versleutelde file heet `bericht.txt.tkv`. Bij ontsleuteling ontstaat
`bericht.txt.ontsleuteld`. De originele file wordt nooit automatisch verwijderd.
De bestandsmodus is bedoeld voor kleine bestanden (maximaal 50 MiB).

### Nieuw eigen schrift tekenen

```bash
python schrift.py "Mi Torelkivaem vara"
```

Er ontstaat `TOREL_BERICHT.svg`. De omvormer gebruikt zelf ontworpen vormen;
niet ieder teken is leesbaar zonder het alfabet. Toch is dit **slechts een
schrift**, géén veilige versleuteling.

## Hoe veilig is de versleuteling?

De code gebruikt **AES-256-GCM** voor versleuteling én bescherming tegen
gewijzigde berichten, en **scrypt** om uit een wachtzin een sleutel af te leiden.
Elk bericht krijgt een verse willekeurige salt (16 bytes) en nonce (12 bytes).
Formaat `TK1:` gevolgd door URL-safe base64 van versie + salt + nonce + ciphertext.
De GCM-tag en een vaste context worden mee geauthenticeerd.

Dit is een toepassing van bestaande, publiek beoordeelde cryptografie – er
wordt **geen eigen cryptografisch algoritme** bedacht. Er is geen garantie
dat het totaal als programma onafhankelijk geaudit is.

**Belangrijk:**

- Gebruik een **lange, unieke wachtzin** (bij voorkeur 5–6 willekeurige woorden).
- Deel de wachtzin **niet via hetzelfde kanaal** als het versleutelde bericht.
- Vergeet je wachtzin? Dan kan deze tool de tekst niet herstellen.
- De taal en het schrift zijn voor geheimhouding door obscuriteit, de
  versleuteling is de echte technische beveiliging.
- Op een geïnfecteerd apparaat kan de tekst vóór of na versleuteling uitlekken.
- Tekst uit een chat kan elders opgeslagen blijven. En het originele
  tekstbestand blijft bestaan tot je het zelf veilig opruimt.
- Er is geen automatische sleuteluitwisseling, perfect forward secrecy
  of afzenderverificatie. Gebruik voor bijzonder gevoelige communicatie een
  gerenommeerde end-to-end versleutelde berichtenapp.

## Ontwikkeling

Torelkiva is een experimentele kunsttaal (versie 1.1). Uniciteit is niet
wereldwijd te garanderen. De naam werd op 12 november 2026 als exacte
zoekterm bekeken zonder duidelijke match.