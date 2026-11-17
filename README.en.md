# Torelkiva 2.2 — English user guide

[Nederlandse handleiding / Dutch guide](README.md)

**Torelkiva — developed by Marco Beenen in collaboration with ChatGPT (OpenAI), started on 12 November 2026.**

Torelkiva is an original constructed language with a word list, grammar, a visual writing system and a separate, optional local encryption program. It is a creative project, not an official OpenAI product or a professionally audited security tool.

## What is included?

- **373 unique Torelkiva words** in the word list.
- A documented basic grammar and examples for learning.
- A controlled Dutch-to-Torelkiva and Torelkiva-to-Dutch sentence translator.
- Word lookup in either language, including partial-word searches.
- A desktop application for Windows and Linux (Python with Tkinter).
- A standalone offline HTML word dictionary for use in a browser.
- A custom alphabet and SVG rendering tool.
- Optional password-based encryption that is separate from the language and alphabet.

The sentence translator supports **only documented, simple sentence patterns**. It does not automatically translate every possible Dutch sentence or every dictionary entry. Unsupported patterns produce an error rather than an invented translation.

## Getting started on Windows or Linux

Install Python 3.9 or newer. If you want to use encryption, install the Python dependencies from the project directory:

~~~sh
python -m pip install -r requirements.txt
~~~

Open the graphical desktop application:

~~~sh
python app.py
~~~

On Windows, you can also use START_WINDOWS.bat; on Linux, run START_LINUX.sh with Bash. The offline.html file opens directly in a browser and does not require an account.

## Translate sentences

For a supported Dutch sentence:

~~~sh
python vertaler.py --van nl "Ik begrijp jou niet."
~~~

Output: **Mi tiem vo nela.**

For the other direction:

~~~sh
python vertaler.py --van tk "Mi tiem vo nela."
~~~

Output: **Ik begrijp jou niet.**

The translator supports basic subjects, known verbs, a limited set of nouns and adjectives, simple negation, questions, past tense and future tense. For the exact rules and restrictions, see [VERTALER.md](VERTALER.md) and [GRAMMATICA.md](GRAMMATICA.md); those detailed references are currently in Dutch.

## Look up individual words

You can search by an entire word in either Dutch or Torelkiva:

~~~sh
python taal.py woord hallo
python taal.py woord vema
~~~

Both commands find the dictionary entry for **vema = hallo**. For partial matches, use:

~~~sh
python taal.py zoek geheim
python taal.py lijst
python taal.py voorbeelden
python taal.py oefen
~~~

Partial search can return multiple results. The word dictionary is broader than the controlled sentence translator.

## Learn the basic grammar

The basic word order is **subject — object — tense — negation — verb**.

- **-em** marks a direct object.
- **-in** marks plural in the language's grammar, although plural objects are not yet supported by the sentence translator.
- **na** indicates past tense.
- **sa** indicates future tense.
- **vo** marks negation.
- **ke?** marks a question.

Examples:

| Dutch | Torelkiva |
| --- | --- |
| Hallo! | Vema! |
| Ik begrijp jou niet. | Mi tiem vo nela. |
| Wij spreken de geheime taal. | Miva sima ravoem vara. |
| Wij schrijven een nieuw woord. | Miva nori mevaem mero. |
| Begrijp jij mij? | Ti miem nela ke? |

See [OEFENBOEK.md](OEFENBOEK.md), [WOORDENBOEK.md](WOORDENBOEK.md) and [Torelkiva_Handleiding_2_2.pdf](Torelkiva_Handleiding_2_2.pdf) for Dutch learning material.

## Encryption: important safety limits

The custom alphabet only changes how text looks; it is **not encryption**. The separate torelkiva.py program uses AES-256-GCM and scrypt with a password:

~~~sh
python torelkiva.py versleutel
python torelkiva.py ontsleutel
~~~

Use a strong unique password and share it separately. Losing the password usually means losing access to the encrypted message. Plaintext files are not automatically deleted. The encryption tool has **not been independently security audited**, so do not rely on it as the sole safeguard for highly sensitive information. The browser word dictionary does not encrypt messages.

Read [VEILIGHEID.md](VEILIGHEID.md) for details about compatibility, file limits and the threat model.

## Testing and maintenance

Run the complete test suite:

~~~sh
python -m unittest discover -s tests -v
~~~

To rebuild the deterministic release ZIP and integrity manifest:

~~~sh
python tools/build_release.py
~~~

The build uses an explicit allowlist of public files so that new private keys or other local files are not automatically included. See [VERIFICATIE.md](VERIFICATIE.md) for test methodology and limits.

## Project origins and rights

The project began on **12 November 2026** and was initiated by **Marco Beenen in collaboration with ChatGPT (OpenAI)**. The development history is documented in [HERKOMST.md](HERKOMST.md).

No open-source license has been selected. Public visibility on GitHub does not automatically grant unrestricted permission to reuse or redistribute the work. This publication is not a trademark registration, independent security certification or endorsement by OpenAI.
