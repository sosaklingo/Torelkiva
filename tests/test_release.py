"""Controle op openbare data, documentatie en offline app (zonder netwerk)."""
import csv
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ReleaseTests(unittest.TestCase):
    def test_geldige_projectmetadata(self):
        meta=json.loads((ROOT/'PROJECT.json').read_text(encoding='utf-8'))
        self.assertEqual(meta['version'],'2.0')
        self.assertEqual(meta['initiator'],'Marco Beenen')
        self.assertFalse(meta['security_audited'])
        self.assertEqual(meta['dictionary_entries'],370)
    def test_woordenboek_consistent(self):
        with (ROOT/'WOORDENLIJST.tsv').open(encoding='utf-8',newline='') as f:
            entries=list(csv.DictReader(f,delimiter='\t'))
        self.assertEqual(len(entries),370)
        self.assertEqual(len({x['torelkiva'] for x in entries}),370)
        markdown=(ROOT/'WOORDENBOEK.md').read_text(encoding='utf-8')
        for entry in entries:
            self.assertIn(f"| `{entry['torelkiva']}` | {entry['nederlands']} | {entry['soort']} |", markdown)
    def test_ontwikkelingsvermelding(self):
        for name in ('README.md','HERKOMST.md','WOORDENBOEK.md','ONTWIKKELINGSVERKLARING.md'):
            data=(ROOT/name).read_text(encoding='utf-8')
            self.assertIn('Marco Beenen',data)
            self.assertIn('ChatGPT',data)
            self.assertIn('12 november 2026',data)
    def test_offline_data_inbegrepen(self):
        data=(ROOT/'offline.html').read_text(encoding='utf-8')
        self.assertIn('370 woorden',data)
        self.assertIn('Marco Beenen',data)
        self.assertNotIn('<script src=',data)
        self.assertNotIn('fetch(',data)
        self.assertNotIn('XMLHttpRequest',data)
        self.assertNotIn('https://',data)
    def test_svg_limiet(self):
        import sys
        sys.path.insert(0,str(ROOT))
        from schrift import sentence_svg
        self.assertRaises(ValueError,sentence_svg,'X'*2001)
        self.assertIn('<svg',sentence_svg('X'*2000))
    def test_cli_interface(self):
        import subprocess,sys
        tests=[(['vertaler.py','--van','nl','Ik begrijp jou niet.'],'Mi tiem vo nela.'),
               (['vertaler.py','--van','tk','Mi tiem vo nela.'],'Ik begrijp jou niet.'),
               (['taal.py','woord','vema'],'hallo'),
               (['torelkiva.py','--versie'],'Torelkiva 2.0')]
        for args,part in tests:
            with self.subTest(args=args):
                p=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,timeout=20)
                self.assertEqual(p.returncode,0,p.stderr)
                self.assertIn(part,p.stdout)
    def test_missing_sentence_explained(self):
        import subprocess,sys
        p=subprocess.run([sys.executable,'vertaler.py','--van','nl','Ik denk omdat het regent.'],cwd=ROOT,capture_output=True,text=True,timeout=10)
        self.assertEqual(p.returncode,2)
        self.assertIn('Niet ondersteund',p.stderr)
    def test_sha256sum_manifest(self):
        import hashlib
        manifest=ROOT/'SHA256SUMS.txt'
        if not manifest.exists(): self.skipTest('Het ZIP-pakket is nog niet gebouwd.')
        lines=manifest.read_text(encoding='utf8').strip().splitlines()
        self.assertGreaterEqual(len(lines),30)
        for line in lines:
            digest,name=line.split('  ',1)
            with self.subTest(path=name):
                self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest)
    def test_geen_onbedoelde_zip_in_source(self):
        self.assertFalse(list(ROOT.glob('*.tkv')))
