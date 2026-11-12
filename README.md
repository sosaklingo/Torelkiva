# TORELKIVA — geheime kunsttaal + eigen schrift + versleuteling

> **Ontwikkeld door Marco Beenen in samenwerking met ChatGPT (OpenAI)**  
> **Initiatiefnemer:** Marco Beenen  
> **Startdatum:** 12 november 2026  
> **Versie:** 1.2

**Torelkiva** is een creatieve, zelfontwikkelde kunsttaal met een groeiend woordenboek, eigen grammatica en het visuele Torel-schrift. Het project bevat daarnaast een **aparte Python-tool voor encryptie**. Taal en schrift alleen zijn niet veilig als cryptografische geheimhouding.

**English:** *Torelkiva is a constructed secret language initiated by Marco Beenen and developed in collaboration with ChatGPT (OpenAI), starting on 12 November 2026. It includes a vocabulary, grammar, original visual alphabet, and separate message encryption software.*

## Officiële projectvermelding

> **Torelkiva — ontwikkeld door Marco Beenen in samenwerking met ChatGPT (OpenAI), begonnen op 12 november 2026.**

Dit is een vermelding van de menselijke initiatiefnemer en het gebruik van AI als ontwikkelhulp. **OpenAI heeft het project niet officieel erkend of gecertificeerd.** GitHub-publicatie is geen merkregistratie of onafhankelijk bewijs van auteursrechten. [Lees de herkomstverklaring](HERKOMST.md).

## Wat kan versie 1.2?

- **149 basiswoorden**: raadpleeg het [woordenboek](WOORDENBOEK.md) en de bronlijst [WOORDENLIJST.tsv](WOORDENLIJST.tsv).
- **Consistente basisgrammatica**: lees [GRAMMATICA.md](GRAMMATICA.md).
- **Leren en oefenen**: gebruik [OEFENBOEK.md](OEFENBOEK.md) of `taal.py`.
- **Visueel schrift**: [Torel-alfabet](TOREL_ALFABET.svg), [voorbeeld](VOORBEELD_TOREL.svg), SVG-generator `schrift.py`.
- **Versleutelen**: `torelkiva.py` (AES-256-GCM met scrypt), compatibel met eerder gemaakte `TK1:`-berichten.
- **Windows en Linux**: eenvoudige startscripts en een terminalhandleiding.
- **Tests**: `python -m unittest discover -s tests -v`.

## Snelle voorbeelden

| Nederlands | Torelkiva |
|---|---|
| Hallo! | `Vema!` |
| Ik begrijp jou niet. | `Mi tiem vo nela.` |
| Wij spreken de geheime taal. | `Miva sima ravoem vara.` |
| Wij zullen een nieuw woord schrijven. | `Miva nori mevaem sa mero.` |

De taal is nog in ontwikkeling. De woordenboektool is **geen automatische vertaler voor complete zinnen**.

## Aan de slag

Installeer **Python 3.9+**. Voor de encryptietool:

```bash
python -m pip install -r requirements.txt
```

Woorden zoeken en oefenen:

```bash
python taal.py zoek geheim
python taal.py woord sima
python taal.py voorbeelden
python taal.py oefen
```

Versleutelen of ontsleutelen:

```bash
python torelkiva.py versleutel
python torelkiva.py ontsleutel
```

Schrift tekenen:

```bash
python schrift.py "Mi Torelkivaem vara."
```

Op Windows kun je ook `START_WINDOWS.bat` gebruiken; op Linux `bash START_LINUX.sh`. Zie [LEESMIJ.md](LEESMIJ.md) voor volledige instructies.

## Veiligheid

Voor het versleutelen wordt bewezen cryptografie gebruikt, maar deze toepassing is **niet onafhankelijk geaudit**. Gebruik een lange, willekeurige, geheime wachtzin en deel die niet via hetzelfde kanaal. Verlies je de wachtzin, dan is de inhoud doorgaans niet te herstellen. Het oorspronkelijke bestand wordt na versleutelen **niet verwijderd**. Zie [VEILIGHEID.md](VEILIGHEID.md).

## Documentatie

- [GRAMMATICA.md](GRAMMATICA.md) — taalregels
- [WOORDENBOEK.md](WOORDENBOEK.md) — volledige woordenlijst en voorbeeldzinnen
- [WOORDENLIJST.tsv](WOORDENLIJST.tsv) — zoekbare bronlijst
- [OEFENBOEK.md](OEFENBOEK.md) — lessen en oefeningen
- [LEESMIJ.md](LEESMIJ.md) — installatie en gebruik
- [HERKOMST.md](HERKOMST.md) — projectgeschiedenis
- [ONTWIKKELINGSVERKLARING.md](ONTWIKKELINGSVERKLARING.md) — particuliere verklaring
- [CHANGELOG.md](CHANGELOG.md) — veranderingen per versie
- [CITATION.cff](CITATION.cff) — bronvermelding op GitHub

## Rechten en status

**Geen officiële merkregistratie.** Wereldwijde uniciteit van naam en inhoud is niet bewezen. De repository heeft op dit moment geen open-sourcelicentie; gebruik binnen de toepasselijke rechten en vraag toestemming waar nodig. De software en documentatie worden verder onderhouden en uitgebreid.