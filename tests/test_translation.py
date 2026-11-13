"""Functionele, fout- en regressietests voor de gecontroleerde vertaler."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vertaler import (to_torelkiva,to_nederlands,parse_torel,parse_nederlands,
                     UnsupportedSentenceError,VERBS)

class TranslationTests(unittest.TestCase):
    FIXTURES = {
        'Hallo!': 'Vema!',
        'Tot ziens!': 'Savo!',
        'Ik lees een boek.': 'Mi laviem lona.',
        'Ik schrijf een bericht.': 'Mi viroem mero.',
        'Ik begrijp jou niet.': 'Mi tiem vo nela.',
        'Ik begrijp jou.': 'Mi tiem nela.',
        'Wij spreken de geheime taal.': 'Miva sima ravoem vara.',
        'Wij schrijven een nieuw woord.': 'Miva nori mevaem mero.',
        'Ik verberg het bericht.': 'Mi da viroem sila.',
        'Begrijp jij mij?': 'Ti miem nela ke?',
        'Ik schreef een bericht.': 'Mi viroem na mero.',
        'Jij zult het bericht lezen.': 'Ti da viroem sa lona.',
        'Ik slaap.': 'Mi suri.',
        'Ik schrijf geen bericht.': 'Mi viroem vo mero.',
        'Zul jij mij begrijpen?': 'Ti miem sa nela ke?',
        'Begrijp jij een nieuw woord?': 'Ti nori mevaem nela ke?',
        'Ik spreek Torelkiva.': 'Mi torelkivaem vara.',
    }
    def test_voorbeelden_nl_naar_tk(self):
        for dutch,torel in self.FIXTURES.items():
            with self.subTest(dutch=dutch):
                self.assertEqual(to_torelkiva(dutch),torel)
    def test_terugvertalen_voorbeelden(self):
        for dutch,torel in self.FIXTURES.items():
            with self.subTest(dutch=dutch):
                self.assertTrue(to_nederlands(torel).endswith(('.', '!', '?')))
                self.assertEqual(to_torelkiva(to_nederlands(torel)),torel)
    def test_het_woord_verbuiging(self):
        self.assertEqual(to_nederlands('Miva nori mevaem mero.'),'Wij schrijven een nieuw woord.')
        self.assertEqual(to_nederlands('Mi nori laviem lona.'),'Ik lees een nieuw boek.')
        self.assertEqual(to_nederlands('Mi sima ravoem vara.'),'Ik spreek de geheime taal.')
    def test_oudere_v11_voorbeelden(self):
        self.assertEqual(to_nederlands('Mi viroem sila.'),'Ik verberg een bericht.')
        self.assertEqual(to_nederlands('Ti miem nela ke?'),'Begrijp jij mij?')
    def test_vraag_syntax(self):
        for item in ['Mi viroem mero?', 'Ti miem nela ke.', 'Ti miem ke?', 'Miva ke?']:
            with self.subTest(item=item):
                with self.assertRaises(UnsupportedSentenceError): parse_torel(item)
    def test_afwijzen_nederlandse_grammaticafouten(self):
        for sentence in ['Ik schrijft een boek.', 'Wij loopt.', 'Ik hebt een boek.', 'Wij gaat.',
                         'Jij schreefde een bericht.', 'Jij zal een bericht schrijven.',
                         'Zal jij mij begrijpen?']:
            with self.subTest(sentence=sentence):
                with self.assertRaises(UnsupportedSentenceError): to_torelkiva(sentence)
    def test_afwijzen_unsupported_constructies(self):
        for sentence in ['Hallo wereld!','Mijn computer is kapot.', 'Ik ga omdat ik wil.',
                         'Wij begrijpen de geheime oude taal.', 'Ik ren, jij loopt.',
                         '1234','', 'Ik spreek\nTorelkiva.', 'Ik schrijf bestanden en boeken.']:
            with self.subTest(sentence=sentence):
                with self.assertRaises(UnsupportedSentenceError): to_torelkiva(sentence)
    def test_torel_onbekende_term(self):
        for text in ['Mi xyzem mero.', 'Mi viroem xyz.', 'Mi ravo na sa mero.',
                     'Ni viroem mera.']:
            with self.subTest(text=text):
                with self.assertRaises(UnsupportedSentenceError): to_nederlands(text)
    def test_tijdaanduidingen(self):
        self.assertEqual(to_nederlands('Mi viroem na vo mero.'),'Ik schreef geen bericht.')
        self.assertEqual(to_nederlands('Mi viroem sa vo mero.'),'Ik zal geen bericht schrijven.')
        self.assertEqual(to_nederlands('Ti miem sa nela ke?'),'Zul jij mij begrijpen?')
    def test_naam_wordt_ook_herkend(self):
        self.assertEqual(to_nederlands('Mi Torelkivaem vara.'),'Ik spreek Torelkiva.')
    def test_alle_werkwoorden_zijn_in_oorspronkelijke_lijst(self):
        from taal import woorden
        allwords={w['torelkiva'] for w in woorden()}
        self.assertFalse(set(VERBS)-allwords)
        self.assertGreaterEqual(len(VERBS),30)

if __name__=='__main__':unittest.main()

class TranslationRoundtripProperties(unittest.TestCase):
    def test_1980_combination_roundtrips(self):
        from vertaler import SUBJECTS_TK
        count=0
        for subj in SUBJECTS_TK:
            for verb in VERBS:
                for tense in ('', 'na', 'sa'):
                    for neg in ('', 'vo'):
                        for question in (False, True):
                            words=[x for x in (subj,tense,neg,verb) if x]
                            if question: words.append('ke')
                            torel=' '.join(words).capitalize()+('?' if question else '.')
                            with self.subTest(sentence=torel):
                                self.assertEqual(to_torelkiva(to_nederlands(torel)),torel)
                            count+=1
        self.assertEqual(count, len(SUBJECTS_TK)*len(VERBS)*3*2*2)
