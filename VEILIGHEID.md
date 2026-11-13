# Torelkiva 2.1 — beveiliging en beperkingen

## Drie verschillende onderdelen

1. **Torelkiva-taal:** woorden en grammatica; geen geheimhouding.
2. **Torel-schrift:** omzetting van letters naar eigen symbolen; geen cryptografische geheimhouding.
3. **Encryptieprogramma (`torelkiva.py`):** aparte versleutelsoftware. Alleen deze stap maakt inhoud cryptografisch onleesbaar zonder de juiste wachtzin.

## TK1-formaat (ongewijzigd vanaf 1.1)

- `TK1` (3 bytes): magic/version identifier.
- 16 bytes willekeurige **salt** en 12 bytes willekeurige **nonce**.
- **scrypt** KDF: N = 2^15, r = 8, p = 1, 32-byte sleutel.
- **AES-256-GCM** met vaste AAD `Torelkiva-Encrypted-Message-v1`.
- GCM-authenticatietag van 16 bytes aan het eind.
- Tekstvorm `TK1:` gevolgd door URL-safe base64 zonder padding.
- Een willekeurige salt en nonce worden per bericht opnieuw gegenereerd. Dit is belangrijk voor de veiligheid; gebruik geen handgemaakte salt of nonce.

De encoder houdt de bestaande indeling in stand zodat eerder uitgebrachte TK1-berichten (met correcte wachtzin) leesbaar blijven.

## Risico's en aanbevolen gebruik

- **Niet onafhankelijk beveiligingsgeaudit**. Geen garantie op foutloosheid of geschiktheid voor hooggevoelige gegevens.
- Gebruik een sterke, unieke wachtzin die niet op GitHub, in een screenshot of bij het bericht staat.
- Deel de wachtzin niet via hetzelfde berichtkanaal als de code.
- Verlies van de wachtzin betekent doorgaans verlies van toegang tot de inhoud. Er is geen herstelknop en geen server.
- De oorspronkelijke invoerbestanden worden **niet** automatisch verwijderd; ook het klembord en uitvoervakken kunnen gevoelige tekst blijven bevatten.
- Deze tool biedt geen bescherming tegen virussen, keyloggers, malware, een gehackte pc, screenshots of verkeerd verstuurde berichten.
- Maximaal 50 MiB invoer; geen streaming voor grote bestanden. De gehele invoer wordt in het werkgeheugen geladen.
- Bestaande uitvoerbestanden worden niet overschreven; ook geen automatische bestandsvernietiging.
- Er is geen account, synchronisatie, server, netwerkdienst of verborgen upload in de programma's.
- De offline HTML-pagina bevat **geen** encryptiefunctie.

## Testen

```bash
python -m unittest discover -s tests -v
```

Tests controleren onder andere rondreizen van tekst en binaire inhoud, verkeerde wachtzinnen, wijzigen van versleutelde inhoud, beschadigde en ongeldige tokens, compatibiliteit en bestandoverschrijving. Een geslaagde test is **geen onafhankelijke veiligheidsaudit**.

## Melding van beveiligingsproblemen

Plaats **geen geheime wachtzinnen, persoonlijke berichten of toegangscodes** in openbare GitHub-issues. Meld een probleem met alleen een synthetische demonstratie, zonder persoonsgegevens of geheime sleutels.
