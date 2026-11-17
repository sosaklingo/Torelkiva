"""Tweerichtingscontrole voor het lossewoordenboek."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from taal import vind


class WordLookupTests(unittest.TestCase):
    def test_exact_lookup_from_both_languages(self):
        for term in ('vema', 'hallo', 'Hallo', ' HALLO '):
            with self.subTest(term=term):
                matches = vind(term, exact=True)
                self.assertTrue(any(row['torelkiva'] == 'vema' for row in matches))

    def test_partial_lookup_and_unknown_word(self):
        self.assertTrue(any(row['torelkiva'] == 'vema' for row in vind('hall')))
        self.assertEqual(vind('onbestaandwoord12345', exact=True), [])
        self.assertEqual(vind('   ', exact=True), [])

    def test_cli_word_lookup_and_version(self):
        for args, expected in [
            (['woord', 'hallo'], 'vema'),
            (['woord', 'vema'], 'hallo'),
            (['--versie'], '2.2'),
        ]:
            with self.subTest(args=args):
                result = subprocess.run(
                    [sys.executable, 'taal.py', *args], cwd=ROOT,
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(expected, result.stdout.casefold())


if __name__ == '__main__':
    unittest.main()
