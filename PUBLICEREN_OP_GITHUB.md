# Torelkiva op GitHub — publicatie en onderhoud

Torelkiva staat openbaar op **https://github.com/sosaklingo/Torelkiva**.

## Herkomst

Initiatiefnemer: **Marco Beenen**. Ontwikkeld in samenwerking met **ChatGPT (OpenAI)** sinds **12 november 2026**. Deze vermelding staat ook in `README.md`, `HERKOMST.md` en `CITATION.cff`.

## Een nieuwe versie publiceren

1. Bewaar eerst een kopie van de huidige code en documentatie.
2. Wijzig de bestanden en verhoog het projectversienummer in `PROJECT.json`, `CITATION.cff` en `CHANGELOG.md`.
3. Controleer of woordenschat en grammatica elkaar niet tegenspreken.
4. Draai lokaal `python -m unittest discover -s tests -v`.
5. Commit en publiceer de wijzigingen met GitHub. De workflow `.github/workflows/tests.yml` voert ook online tests uit.
6. Vernieuw `SHA256SUMS.txt` na het wijzigen van bestanden, omdat oude controlesommen anders niet meer kloppen. Dit bestand bevat geen hash van zichzelf.

## Privacy en rechten

Zet **nooit** wachtwoorden, geheime sleutels, privégesprekken of persoonlijke informatie in een openbare GitHub-repository. De taal en de code zijn openbaar. GitHub-publicatie is **geen** officiële merkregistratie, en de software is niet onafhankelijk beveiligingsgeaudit.