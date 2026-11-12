"""Vast referentiebericht uit het TK1-v1.1/1.2-formaat.

De test gebruikt dezelfde algoritmeparameters als het oude programma en
controleert dat ze niet per ongeluk worden veranderd in latere releases.
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from torelkiva import decrypt_text,encrypt_text,encrypt_bytes,decrypt_bytes, MAGIC,AAD,SALT_LEN,NONCE_LEN
PASS='historische testwachtzin uitsluitend voor fixtures!'
class LegacyTK1Tests(unittest.TestCase):
    def test_vector_oud_formaat(self):
        # Crypto-vector met vaste salt/nonce; nooit echte berichten zo coderen.
        with patch('torelkiva.os.urandom', side_effect=[bytes(range(SALT_LEN)),bytes(range(NONCE_LEN))]):
            token=encrypt_text('Vema! Mi viroem sila.',PASS)
        self.assertEqual(token,'TK1:VEsxAAECAwQFBgcICQoLDA0ODwABAgMEBQYHCAkKCwoPdFMLASlZrRWzB_nQ-3cEC3nIVYvOKlZI5y3MAf1j4RIbxt4')
        self.assertEqual(decrypt_text(token,PASS),'Vema! Mi viroem sila.')
    def test_magic_aad_ongewijzigd(self):
        self.assertEqual(MAGIC,b'TK1')
        self.assertEqual(AAD,b'Torelkiva-Encrypted-Message-v1')
        self.assertEqual(SALT_LEN,16)
        self.assertEqual(NONCE_LEN,12)
    def test_decrypt_malformed_token_fails(self):
        with self.assertRaises(ValueError):decrypt_text('TK1:aaaaaaaa',PASS)
