"""Eenvoudige Torelkiva-tests met unittest (zonder echte geheimen)."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from torelkiva import encrypt_text, decrypt_text, encrypt_bytes, decrypt_bytes

PASS = 'een heel lange testwachtzin voor ontwikkeling alleen'
class TorelkivaTests(unittest.TestCase):
    def test_roundtrip_text(self):
        text = 'Mi viroem sila. Torelkiva 🔒'
        token = encrypt_text(text, PASS)
        self.assertTrue(token.startswith('TK1:'))
        self.assertEqual(decrypt_text(token, PASS), text)
    def test_randomized(self):
        self.assertNotEqual(encrypt_text('Vema.',PASS),encrypt_text('Vema.',PASS))
    def test_wrong_password(self):
        with self.assertRaises(ValueError):
            decrypt_text(encrypt_text('Test',PASS),'onjuiste wachtzin')
    def test_tamper(self):
        blob = bytearray(encrypt_bytes(b'Test',PASS))
        blob[-1] ^= 1
        with self.assertRaises(ValueError):
            decrypt_bytes(bytes(blob),PASS)
    def test_short_passphrase(self):
        with self.assertRaises(ValueError):
            encrypt_text('Test','kort')
if __name__ == '__main__':
    unittest.main()
