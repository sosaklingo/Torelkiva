"""Betekenisbehoud en terugcompatibiliteit van Torelkiva 2.2."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vertaler import (to_nederlands, to_torelkiva, parse_torel, parse_nederlands,
                      UnsupportedSentenceError, SUBJECTS_TK, VERBS)

class ArticleAndPronounTests(unittest.TestCase):
    CASES = {
        'Ik lees een boek.': 'Mi laviem lona.',
        'Ik lees het boek.': 'Mi da laviem lona.',
        'Ik lees het nieuwe boek.': 'Mi da nori laviem lona.',
        'Ik lees een nieuw boek.': 'Mi nori laviem lona.',
        'Ik schrijf het bericht.': 'Mi da viroem mero.',
        'Ik schrijf een bericht.': 'Mi viroem mero.',
        'Ik spreek de geheime taal.': 'Mi sima ravoem vara.',
        'Ik spreek een taal.': 'Mi en ravoem vara.',
        'Ik zie de vriend.': 'Mi da lumaem fira.',
        'Ik zie een vriend.': 'Mi lumaem fira.',
        'Ik zie de grote vriend.': 'Mi da vala lumaem fira.',
        'Ik zie een grote vriend.': 'Mi vala lumaem fira.',
        'Zij slaapt.': 'Eli suri.',
        'Zij slapen.': 'Tira suri.',
        'Zij ging.': 'Eli na gala.',
        'Zij gingen.': 'Tira na gala.',
        'Zij zal slapen.': 'Eli sa suri.',
        'Zij zullen slapen.': 'Tira sa suri.',
        'Zij wil een boek.': 'Eli laviem laki.',
        'Zij willen een boek.': 'Tira laviem laki.',
        'Wil zij een boek?': 'Eli laviem laki ke?',
        'Slaapt zij?': 'Eli suri ke?',
        'Slapen zij?': 'Tira suri ke?',
        'Ik begrijp haar.': 'Mi eliem nela.',
        'Ik begrijp hem.': 'Mi elaem nela.',
        'Zij begrijpt haar.': 'Eli eliem nela.',
    }
    def test_concrete_phrases(self):
        for nl, tk in self.CASES.items():
            with self.subTest(nl=nl):
                self.assertEqual(to_torelkiva(nl),tk)
                self.assertEqual(to_nederlands(tk),nl)
    def test_legacy_11_and_21_still_readable(self):
        self.assertEqual(to_nederlands('Mi viroem sila.'),'Ik verberg een bericht.')
        self.assertEqual(to_nederlands('Ti viroem sa lona.'),'Jij zult een bericht lezen.')
        self.assertEqual(to_nederlands('Mi sima ravoem vara.'),'Ik spreek de geheime taal.')
    def test_bad_gender_articles(self):
        bad = ['Ik lees de boek.', 'Ik lees het taal.', 'Ik zie het vriend.',
               'Ik schrijf de bericht.', 'Ik schrijf geen het bericht.',
               'Ik zie de nieuw vriend.', 'Ik lees het nieuw boek.',
               'Ik zie het haar.', 'Ik zie de haar.', 'Ik zie een hem.']
        for nl in bad:
            with self.subTest(nl=nl), self.assertRaises(UnsupportedSentenceError):
                to_torelkiva(nl)
    def test_illegal_article_particles(self):
        bad = ['Mi da lona.', 'Mi en suri.', 'Mi da miem nela.',
               'Mi en torelkivaem vara.', 'Mi da laviem vo lona.',
               'Mi da en laviem lona.', 'Mi da laviem en lona.',
               'Mi en nori miem nela.']
        for tk in bad:
            with self.subTest(tk=tk), self.assertRaises(UnsupportedSentenceError):
                to_nederlands(tk)
    def test_12960_supported_sentence_roundtrips(self):
        from itertools import product
        from vertaler import SUBJECTS_TK, VERBS, NO_DIRECT_OBJECT
        examples=['', 'laviem', 'nori laviem', 'da laviem',
                  'da nori laviem', 'en ravoem', 'da vala lumaem',
                  'miem', 'eliem', 'elaem']
        count=0
        for subj,verb,obj,tense,neg,q in product(
                SUBJECTS_TK, VERBS, examples, ('','na','sa'), ('','vo'), (False,True)):
            if obj and verb in NO_DIRECT_OBJECT:
                continue
            if neg and obj.startswith(('da ', 'en ')):
                continue
            code=' '.join(x for x in (subj,obj,tense,neg,verb,'ke' if q else '') if x)
            code=code.capitalize()+('?' if q else '.')
            dutch=to_nederlands(code)
            self.assertEqual(to_torelkiva(dutch),code,code)
            count+=1
        self.assertEqual(count,12960)

    def test_new_words_in_dictionary(self):
        from taal import woorden
        rows=woorden()
        self.assertEqual(len(rows),373)
        for term in ('eli','da','en'):
            self.assertEqual(sum(x['torelkiva']==term for x in rows),1)
    def test_missing_word_handling(self):
        for bad in ['Ik begrijp het tafel.', 'Ik lees geen de boek.',
                    'Zij is een boek.', 'Zij wilt een boek.', 'Zij weten een boek.',
                    'Ik lees boek.', 'Ik zie nieuwe vriend.']:
            with self.subTest(bad=bad), self.assertRaises(UnsupportedSentenceError):
                to_torelkiva(bad)

if __name__=='__main__':
    unittest.main()
