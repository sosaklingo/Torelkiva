"""Controles voor het Torelkiva woordenboek en schrift."""
import sys
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from taal import woorden, vind, VOORBEELDEN
from schrift import ALPHABET, paths, alphabet_svg, sentence_svg

class LanguageTests(unittest.TestCase):
    def test_woordenboek_uniek(self):
        rows = woorden()
        self.assertEqual(len(rows), 370)
        self.assertEqual(len(rows), len({r['torelkiva'] for r in rows}))
    def test_oudste_kernwoorden_bewaard(self):
        for word in ['mi','ti','miva','tira','ela','vema','savo','ravo','sima','viro','luma','tora','nori','kavi','vara','nela','sila','kiri','fira','mero','lona','gala','dara','vo','sa','na','ke']:
            self.assertEqual(len(vind(word, exact=True)), 1, word)
    def test_zoeken_nederlands(self):
        self.assertIn('sima', [r['torelkiva'] for r in vind('geheim')])
        self.assertEqual(vind('MI', exact=True)[0]['nederlands'], 'ik')
        self.assertEqual(vind('ONBEKEND!', exact=True), [])
    def test_minimum_voorbeelden(self):
        self.assertGreaterEqual(len(VOORBEELDEN), 10)
    def test_26_aparte_glyphs(self):
        self.assertEqual(len({paths(ch) for ch in ALPHABET}), 26)
    def test_svg_geldige_xml(self):
        ET.fromstring(alphabet_svg())
        ET.fromstring(sentence_svg('Mi viroem sila!'))
    def test_xml_escaped(self):
        s = sentence_svg('<script>&\x00')
        ET.fromstring(s)
        self.assertIn('&lt;', s)
        self.assertNotIn('<script>', s)

if __name__ == '__main__':
    unittest.main()
