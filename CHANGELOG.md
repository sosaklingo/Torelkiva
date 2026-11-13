# Torelkiva 2.2 — betekenisbehoud en foutdetectie (13 november 2026)

- Nieuwe optionele lidwoorddeeltjes `da` (de/het) en `en` (een), zonder de basiszinnen te wijzigen.
- Nederlands krijgt foutdetectie voor verkeerde lidwoorden, zoals *de boek*.
- `eli` = zij (enkelvoud), `eliem` = haar; oude `ela` en `tira` blijven intact.
- Het onderscheid *zij slaapt* versus *zij slapen* werkt nu via Nederlandse persoonsvorm.
- Woordenboek uitgebreid van 370 tot 373 lemmas, inclusief de nieuwe grammaticale deeltjes.
- Extra regressietests voor vertaalrondreizen en historische compatibiliteit.
- Valentiecontrole: werkwoorden zoals slapen, gaan en luisteren kunnen in het beperkte vertaalmodel geen direct voorwerp meer krijgen.
- Eerdere TK1-encryptie blijft byte-for-byte compatibel.

# Versie 2.1 — kwaliteitsupdate (13 november 2026)

- Toekomstige Nederlandse zinnen met een voorwerp worden nu correct herkend: *Ik zal een boek lezen* ↔ `Mi laviem sa lona.`
- Correcte Nederlandse adjectiefspelling (*grote* in plaats van *groote*), ook na *geen*.
- Foutieve dubbele ontkenning (*niet geen*), dubbele lidwoorden en onlogische bijvoeglijke woorden bij voornaamwoorden worden afgewezen.
- `elaem` gebruikt voortaan de canonieke Nederlandse objectvorm *hem*; *haar* wordt ook als invoer ondersteund.
- 100.000 representatieve zinscombinaties gecontroleerd; nieuwe vaste tests toegevoegd.
- Releasebuilder gebruikt een expliciete lijst met bronbestanden om onbedoeld meesturen van privébestanden te voorkomen.
- Oud `TK1:`-encryptieformaat blijft ongewijzigd.

# Wijzigingen — Torelkiva

## 2.0 — 13 november 2026

- Woordenschat van 149 naar **370** unieke lemmas, met stabiele originele basis.
- Uitspraak, objectmarkering, tijdsvormen, vraag- en getalsconventies vastgelegd.
- Gecontroleerde vertaler Nederlands ↔ Torelkiva voor gedocumenteerde eenvoudige zinnen; niet-ondersteunde input wordt expliciet geweigerd.
- Offline miniwoordenboek en voorbeeldzinnen toegevoegd; apart van encryptie.
- Grafisch desktopprogramma (`app.py`) met tabs voor woorden, vertalen, letterweergave en lokale encryptie.
- SVG-generator begrensd om ongewenst enorme bestanden te voorkomen.
- Extra taal-, vertaal-, bestands- en beveiligingstests en GitHub CI.
- Veiligheids- en installatiehandleidingen herzien.
- TK1-salt, nonce, sleutelafleiding en AES-256-GCM **ongewijzigd**: oudere berichten blijven compatibel.

## 1.2 — 12 november 2026

- 149 woorden, basisgrammatica, oefenboek en zoekprogramma.
- Verbeterde CLI, uitgebreidere tests en automatische CI.

## 1.1 — 12 november 2026

- Eerste openbare versie met woordenboek, Torel-schrift, projectherkomst en TK1-versleuteling.
