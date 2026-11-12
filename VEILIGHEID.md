# Beveiliging en privacy

Torelkiva bestaat uit drie aparte onderdelen:

1. **De kunsttaal**: bedoeld voor creatieve communicatie; op zichzelf niet geheim zodra het woordenboek openbaar is.
2. **Torel-schrift**: symbolen voor letters; eenvoudig te ontcijferen met het alfabet. Dit is geen cryptografie.
3. **Encryptietool**: gebruikt het bestaande AES-256-GCM-algoritme en scrypt-wachtwoordafleiding. Dit biedt echte technische versleuteling, maar is niet onafhankelijk geaudit.

## Gebruik

- Neem een lange, unieke, willekeurige wachtzin. Deel die niet via hetzelfde kanaal als het bericht.
- Publiceer **nooit** wachtzinnen, privésleutels, tokens, persoonlijke chatlogs of geheime berichten in GitHub.
- De originele bestanden blijven bestaan na versleutelen; ze worden niet automatisch gewist.
- De encryptietool biedt geen afzenderidentiteit, sleuteluitwisseling of perfect forward secrecy.
- Een geïnfecteerd of gedeeld apparaat kan de inhoud of wachtzin onderscheppen.
- Gebruik voor zeer vertrouwelijke communicatie bij voorkeur een gerenommeerde end-to-end versleutelde berichtenapp.

## Techniek van bestandsformaat TK1

- AES-256-GCM voor authenticatie en versleuteling.
- scrypt N=32768, r=8, p=1, sleutel 32 bytes.
- Willekeurige salt van 16 bytes en nonce van 12 bytes per bericht.
- Binaire opbouw `TK1 || salt || nonce || ciphertext+tag`, als tekst met `TK1:` en URL-veilige base64.
- Maximaal 50 MiB bij bestanden.

## Rapporteren

Vermeld bij meldingen over fouten de betrokken softwareversie en een minimale reproductie zonder echte wachtzinnen of gevoelige inhoud.