# Onafhankelijk na te lopen kwaliteitscontrole — Torelkiva 2.1

**Oorsprong:** Marco Beenen in samenwerking met ChatGPT (OpenAI), begonnen op 12 november 2026.

## Uitgevoerde controles

1. Unittests: `python -m unittest discover -s tests -v` vanuit de projectmap.
2. Python-syntax: `python -m compileall -q .`.
3. Functionele controles van verleden, heden, toekomst, ontkenning, vraagzin, voorwerpen, bijvoeglijke naamwoorden, aanspreekvormen en eigennamen.
4. Handmatige zoekcontrole op 100.000 verschillende canonieke Torelkiva-zinnen: `TK → NL → TK` bleef identiek.
5. Encryptieregressie: het oorspronkelijke `TK1:`-testbericht met vaste salt en nonce blijft ontsleutelbaar.
6. Bestandscontrole: SHA-256-checksums voor alle releasebestanden in `SHA256SUMS.txt`.

## Afbakening en bekende beperkingen

- Er zijn 370 woorden in het woordenboek, maar niet alle woorden kunnen vrij in alle grammaticale constructies worden vertaald.
- Sommige informatie gaat verloren bij vertaling, vooral lidwoorden (*de, het, een*) en het genderneutrale `ela`. Daarom is een exacte Nederlands↔Torelkiva↔Nederlands-rondreis **niet altijd mogelijk**.
- De app gebruikt Tkinter: niet bedoeld voor iOS of Android. Het bestand `offline.html` is wel een offline browserwoordenboek, zonder versleuteling.
- Encryptie gebruikt `AES-256-GCM` en `scrypt` uit `cryptography`, maar het programma is **niet onafhankelijk geaudit**. Een lange, unieke, geheime wachtzin is cruciaal.
- `Torelkiva_Handleiding_2_1.pdf` is de actuele Nederlandstalige handleiding. De oude `Torelkiva_Handleiding_2_0.pdf` blijft op GitHub beschikbaar als versiehistorie, maar zit niet in het ZIP-pakket met versie 2.1.
- Er bestaat geen methode om wiskundig te garanderen dat deze toepassing of kunsttaal absoluut foutloos, volledig of onveranderlijk is.

## Zelf testen

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m compileall -q .
python tools/build_release.py
```

Het buildscript pakt alleen expliciet goedgekeurde bronbestanden in. Zet nooit persoonlijke sleutels, wachtzinnen of berichten in deze openbaar bedoelde projectmap.
