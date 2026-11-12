#!/usr/bin/env python3
"""Torelkiva 1.2: berichten en (kleine) bestanden versleutelen.

Beveiliging: scrypt (N=2^15, r=8, p=1) + AES-256-GCM met een verse
willekeurige salt en nonce per bericht. Vereist: cryptography.
"""
from __future__ import annotations

import argparse
import base64
import binascii
from getpass import getpass
import os
from pathlib import Path
import sys

try:
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
except ImportError:
    print("Deze tool heeft 'cryptography' nodig. Installeer met: python -m pip install cryptography", file=sys.stderr)
    sys.exit(2)

MAGIC = b"TK1"
PREFIX = "TK1:"
SALT_LEN = 16
NONCE_LEN = 12
HEADER_LEN = len(MAGIC) + SALT_LEN + NONCE_LEN
AAD = b"Torelkiva-Encrypted-Message-v1"
MAX_FILE_SIZE = 50 * 1024 * 1024  # kleine bestanden; houdt geheugengebruik beheersbaar
MAX_ENCRYPTED_SIZE = MAX_FILE_SIZE + HEADER_LEN + 16
MAX_TOKEN_SIZE = len(PREFIX) + ((MAX_ENCRYPTED_SIZE + 2) // 3) * 4


def _key(passphrase: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**15, r=8, p=1)
    return kdf.derive(passphrase.encode("utf-8"))


def encrypt_bytes(data: bytes, passphrase: str) -> bytes:
    if len(data) > MAX_FILE_SIZE:
        raise ValueError("Invoer te groot (maximaal 50 MiB).")
    if len(passphrase) < 12:
        raise ValueError("Gebruik een wachtzin van minimaal 12 tekens (liefst vijf willekeurige woorden).")
    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)
    encrypted = AESGCM(_key(passphrase, salt)).encrypt(nonce, data, AAD)
    return MAGIC + salt + nonce + encrypted


def decrypt_bytes(blob: bytes, passphrase: str) -> bytes:
    if len(blob) > MAX_ENCRYPTED_SIZE:
        raise ValueError("Versleutelde invoer te groot (maximaal 50 MiB).")
    if not blob.startswith(MAGIC) or len(blob) < HEADER_LEN + 16:
        raise ValueError("Ongeldig Torelkiva-bericht of onvolledige code.")
    offset = len(MAGIC)
    salt = blob[offset:offset + SALT_LEN]
    nonce = blob[offset + SALT_LEN:HEADER_LEN]
    ciphertext = blob[HEADER_LEN:]
    try:
        return AESGCM(_key(passphrase, salt)).decrypt(nonce, ciphertext, AAD)
    except InvalidTag as exc:
        raise ValueError("Ontsleutelen mislukt: onjuiste wachtzin of gewijzigde/beschadigde inhoud.") from exc


def encrypt_text(text: str, passphrase: str) -> str:
    raw = encrypt_bytes(text.encode("utf-8"), passphrase)
    return PREFIX + base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decrypt_text(token: str, passphrase: str) -> str:
    token = token.strip()
    if len(token) > MAX_TOKEN_SIZE:
        raise ValueError("Versleutelde tekst te groot (maximaal 50 MiB).")
    if not token.startswith(PREFIX):
        raise ValueError("De code moet beginnen met TK1:.")
    encoded = token[len(PREFIX):]
    if not encoded or any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for c in encoded):
        raise ValueError("Ongeldige versleutelde tekst.")
    try:
        raw = base64.b64decode(encoded + "=" * (-len(encoded) % 4), altchars=b"-_", validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError("Ongeldige base64-code.") from exc
    return decrypt_bytes(raw, passphrase).decode("utf-8")


def _save_new(path: Path, data: bytes) -> None:
    # Maakt een nieuw bestand aan, overschrijft niets, beperkt toegangsrechten waar ondersteund.
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(str(path), flags, 0o600)
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(data)
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
        raise


def run() -> int:
    parser = argparse.ArgumentParser(description="Torelkiva 1.2 – versleutel en ontsleutel berichten of bestanden")
    parser.add_argument("--versie", action="version", version="Torelkiva 1.2 (bestandsformaat TK1)")
    parser.add_argument("actie", choices=["versleutel", "ontsleutel"], help="Kies je actie")
    parser.add_argument("--bestand", type=Path, help="Optioneel: werk met een tekstbestand of ander klein bestand")
    parser.add_argument("--stdin", action="store_true", help="Lees tekst/een TK1-code van standaardinvoer (ondersteunt meerdere regels)")
    args = parser.parse_args()
    if args.bestand and args.stdin:
        parser.error("Kies --bestand OF --stdin, niet allebei.")

    try:
        if args.actie == "versleutel":
            if args.bestand:
                if not args.bestand.is_file():
                    raise ValueError("Bestand niet gevonden.")
                if args.bestand.stat().st_size > MAX_FILE_SIZE:
                    raise ValueError("Bestand te groot (maximaal 50 MiB).")
                data = args.bestand.read_bytes()
            elif args.stdin:
                data = sys.stdin.buffer.read(MAX_FILE_SIZE + 1)
            else:
                data = input("Tekst die je wilt versleutelen: ").encode("utf-8")
            password = getpass("Kies een lange geheime wachtzin: ")
            password2 = getpass("Herhaal je wachtzin: ")
            if password != password2:
                raise ValueError("De twee wachtzinnen komen niet overeen.")
            if args.bestand:
                output = Path(str(args.bestand) + ".tkv")
                _save_new(output, encrypt_bytes(data, password))
                print(f"Versleuteld bestand: {output}")
                print("Let op: het originele bestand is NIET verwijderd.")
            else:
                print("\nJe versleutelde code:\n")
                print(encrypt_text(data.decode("utf-8"), password))
        else:
            if args.bestand:
                if not args.bestand.is_file():
                    raise ValueError("Bestand niet gevonden.")
                if args.bestand.stat().st_size > MAX_FILE_SIZE + 128:
                    raise ValueError("Bestand te groot (maximaal 50 MiB).")
                blob = args.bestand.read_bytes()
            elif args.stdin:
                token = sys.stdin.read(MAX_TOKEN_SIZE + 1)
            else:
                token = input("Plak hier je versleutelde TK1-code: ")
            password = getpass("Geheime wachtzin: ")
            if args.bestand:
                data = decrypt_bytes(blob, password)
                base = str(args.bestand)
                if base.endswith(".tkv"):
                    base = base[:-4]
                output = Path(base + ".ontsleuteld")
                _save_new(output, data)
                print(f"Ontsleuteld bestand: {output}")
            else:
                result = decrypt_text(token, password)
                print("\nJe oorspronkelijke tekst:\n")
                print(result)
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print(f"Fout: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run())
