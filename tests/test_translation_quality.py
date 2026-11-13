"""Nieuwe regressietests na de inhoudelijke audit van Torelkiva 2.1."""
import itertools
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vertaler import (to_torelkiva, to_nederlands, UnsupportedSentenceError,
                      VERBS, SUBJECTS_TK, NO_DIRECT_OBJECT)
from tools.build_release import FILES


class QualityTests(unittest.TestCase):
    def test_future_object_in_both_directions(self):
        cases = {
            'Ik zal een boek lezen.': 'Mi laviem sa lona.',
            'Jij zult een boek lezen.': 'Ti laviem sa lona.',
            'Zul jij een boek lezen?': 'Ti laviem sa lona ke?',
            'Wij zullen een boek lezen.': 'Miva laviem sa lona.',
            'Ik zal geen boek lezen.': 'Mi laviem sa vo lona.',
            'Zul jij geen boek lezen?': 'Ti laviem sa vo lona ke?',
            'Wij zullen een nieuw woord schrijven.': 'Miva nori mevaem sa mero.',
            'Ik zal niet slapen.': 'Mi sa vo suri.',
        }
        for dutch, torel in cases.items():
            with self.subTest(dutch=dutch):
                self.assertEqual(to_torelkiva(dutch), torel)
                self.assertEqual(to_torelkiva(to_nederlands(torel)), torel)

    def test_correct_adjective_spelling(self):
        self.assertEqual(to_nederlands('Mi vala ravoem vara.'), 'Ik spreek de grote taal.')
        self.assertEqual(to_nederlands('Mi nori simaem vo mero.'), 'Ik schrijf geen nieuw geheim.')
        self.assertEqual(to_nederlands('Mi vala lumaem vo fira.'), 'Ik zie geen grote vriend.')
        self.assertEqual(to_torelkiva('Ik zie geen grote vriend.'), 'Mi vala lumaem vo fira.')
        for sentence in ['Ik lees een groote boek.', 'Ik zie geen groot vriend.',
                         'Ik schrijf geen nieuwe geheim.']:
            with self.subTest(sentence=sentence):
                with self.assertRaises(UnsupportedSentenceError):
                    to_torelkiva(sentence)

    def test_invalid_negations_and_modifiers_rejected(self):
        invalid_dutch = [
            'Ik schrijf niet geen bericht.', 'Ik schrijf geen het boek.',
            'Ik begrijp mooie jou.', 'Ik lees geen mij.', 'Ik lees een jou.',
            'Ik lees een boek niet.', 'Ik lees niet een boek.',
            'Ik schrijf geen geen bericht.', 'Ik spreek niet niet.',
            'Ik lees de.', 'Ik schrijf geen.',
        ]
        invalid_torel = ['Mi nori miem nala.', 'Mi nori miem nela.',
                         'Mi nori torelkivaem vara.', 'Mi mooie tiem nela.']
        for sentence in invalid_dutch:
            with self.subTest(sentence=sentence):
                with self.assertRaises(UnsupportedSentenceError):
                    to_torelkiva(sentence)
        for sentence in invalid_torel:
            with self.subTest(sentence=sentence):
                with self.assertRaises(UnsupportedSentenceError):
                    to_nederlands(sentence)

    def test_canonical_hij_hem_and_haar(self):
        self.assertEqual(to_nederlands('Mi elaem nela.'), 'Ik begrijp hem.')
        self.assertEqual(to_torelkiva('Ik begrijp haar.'), 'Mi eliem nela.')
        self.assertEqual(to_torelkiva('Ik begrijp hem.'), 'Mi elaem nela.')

    def test_verb_object_question_negation_roundtrips(self):
        # Een vaste steekproef over verschillende zinstypen, naast de eerdere
        # audit van 100.000 verschillende zinnen; geschikt voor een snelle CI.
        objects = ['', 'viroem', 'nori mevaem', 'sima ravoem',
                   'vala lumaem', 'miem', 'elaem']
        count = 0
        for subject, verb, obj, tense, negated, question in itertools.product(
                SUBJECTS_TK, VERBS, objects, ('', 'na', 'sa'), ('', 'vo'), (False, True)):
            text = ' '.join(x for x in [subject, obj, tense, negated, verb,
                                      'ke' if question else ''] if x)
            text = text.capitalize() + ('?' if question else '.')
            with self.subTest(text=text):
                if verb in NO_DIRECT_OBJECT and obj:
                    with self.assertRaises(UnsupportedSentenceError):
                        to_nederlands(text)
                else:
                    self.assertEqual(to_torelkiva(to_nederlands(text)), text)
            count += 1
        self.assertEqual(count, len(SUBJECTS_TK)*len(VERBS)*len(objects)*3*2*2)

    def test_release_allowlist_excludes_private_filenames(self):
        self.assertEqual(len(FILES), len(set(FILES)))
        for item in FILES:
            self.assertFalse(item.endswith(('.env', '.key', '.tkv', '.zip', '.ontsleuteld')))
            self.assertFalse(Path(item).is_absolute())


if __name__ == '__main__':
    unittest.main()
