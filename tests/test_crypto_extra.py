"""Randgevallen en compatibiliteit met het oorspronkelijke TK1-formaat."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from torelkiva import encrypt_bytes, decrypt_bytes, encrypt_text, decrypt_text, _save_new, HEADER_LEN, MAX_FILE_SIZE

P = 'een testwachtzin die nergens anders gebruikt wordt'
class CryptoExtraTests(unittest.TestCase):
    def test_lege_tekst(self):
        self.assertEqual(decrypt_text(encrypt_text('', P), P), '')
    def test_unicode_meerdere_regels(self):
        msg = 'Torelkiva\nHallo 🌍\nmi viroem sila.\n'
        self.assertEqual(decrypt_text(encrypt_text(msg, P), P), msg)
    def test_binaire_bestanden(self):
        data = bytes(range(256))
        self.assertEqual(decrypt_bytes(encrypt_bytes(data, P), P), data)
    def test_ongeldige_header(self):
        with self.assertRaises(ValueError):
            decrypt_bytes(b'BAD' + b'\x00' * (HEADER_LEN + 32), P)
    def test_ongeldige_base64(self):
        for code in ('TK1:', 'TK1:!', 'XXX:abc', 'TK1:AB+CD'):
            with self.subTest(code=code):
                with self.assertRaises(ValueError):
                    decrypt_text(code, P)
    def test_padded_token(self):
        code = encrypt_text('Hallo', P)
        # TK1 hoort zonder padding te worden uitgewisseld; extra '=' wordt afgekeurd.
        with self.assertRaises(ValueError):
            decrypt_text(code + '=', P)
    def test_maximum_binaire_invoer(self):
        with self.assertRaises(ValueError):
            encrypt_bytes(b'x' * (MAX_FILE_SIZE + 1), P)
    def test_afgebroken_ciphertekst(self):
        code = encrypt_bytes(b'Bericht', P)
        with self.assertRaises(ValueError):
            decrypt_bytes(code[:HEADER_LEN + 2], P)
    def test_overschrijven_niet_toegestaan(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'bericht.bin'
            _save_new(path, b'eerste')
            with self.assertRaises(FileExistsError):
                _save_new(path, b'tweede')
            self.assertEqual(path.read_bytes(), b'eerste')

if __name__ == '__main__':
    unittest.main()
