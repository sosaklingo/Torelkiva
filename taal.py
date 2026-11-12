#!/usr/bin/env python3
"""Torelkiva 2.0: zoek in het officiële woordenboek en oefen met voorbeelden.

Dit is een woordenboekhulp, geen automatische vertaler van complete zinnen.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import random
import sys

PATH = Path(__file__).with_name('WOORDENLIJST.tsv')
VOORBEELDEN = [
    ('Hallo!', 'Vema!'),
    ('Ik spreek Torelkiva.', 'Mi Torelkivaem vara.'),
    ('Ik begrijp jou.', 'Mi tiem nela.'),
    ('Ik begrijp jou niet.', 'Mi tiem vo nela.'),
    ('Wij spreken de geheime taal.', 'Miva sima ravoem vara.'),
    ('Ik verberg het bericht.', 'Mi viroem sila.'),
    ('Wij zullen het geheim beschermen.', 'Miva simaem sa kiri.'),
    ('Begrijp jij mij?', 'Ti miem nela ke?'),
    ('Ik schreef een bericht.', 'Mi viroem na mero.'),
    ('Ik lees een boek.', 'Mi laviem lona.'),
    ('Wij schrijven een nieuw woord.', 'Miva nori mevaem mero.'),
    ('Jij zult het bericht lezen.', 'Ti viroem sa lona.'),
]


def woorden() -> list[dict[str, str]]:
    with PATH.open('r', encoding='utf-8', newline='') as bestand:
        rows = list(csv.DictReader(bestand, delimiter='\t'))
    expected = {'torelkiva', 'nederlands', 'soort'}
    if not rows or any(set(row) != expected or not all(row.values()) for row in rows):
        raise ValueError('De woordenlijst heeft een foutieve indeling of lege velden.')
    terms = [row['torelkiva'] for row in rows]
    if len(terms) != len(set(terms)):
        raise ValueError('Het woordenboek bevat dubbele Torelkiva-woorden.')
    if any(not x.isascii() or not x.isalpha() or x != x.lower() for x in terms):
        raise ValueError('Ongeldige letters of hoofdletters in het woordenboek.')
    return rows


def vind(term: str, exact: bool = False) -> list[dict[str, str]]:
    needle = term.strip().casefold()
    if not needle:
        return []
    return [row for row in woorden() if (
        row['torelkiva'].casefold() == needle if exact else
        needle in row['torelkiva'].casefold() or needle in row['nederlands'].casefold()
    )]


def main() -> int:
    parser = argparse.ArgumentParser(description='Torelkiva 2.0 — woordenboek en oefenhulp (geen automatische vertaler)')
    parser.add_argument('--versie', action='version', version='Torelkiva taalhulp 1.2')
    sub = parser.add_subparsers(dest='opdracht', required=True)
    for name in ('zoek', 'woord'):
        p = sub.add_parser(name, help='Zoek een deel van een woord' if name == 'zoek' else 'Zoek een exact Torelkiva-woord')
        p.add_argument('term', help='Torelkiva of Nederlands zoekwoord')
    sub.add_parser('lijst', help='Laat alle woorden zien')
    sub.add_parser('voorbeelden', help='Laat voorbeeldzinnen zien')
    sub.add_parser('oefen', help='Oefen met vijf willekeurige woorden')
    args = parser.parse_args()
    try:
        if args.opdracht == 'voorbeelden':
            for nl, tk in VOORBEELDEN:
                print(f'{nl}\n  → {tk}')
        elif args.opdracht == 'oefen':
            rows = [row for row in woorden() if row['soort'] not in ('partikel', 'voegwoord')]
            for row in random.sample(rows, k=min(5, len(rows))):
                print(f'Wat is het Torelkiva-woord voor: {row["nederlands"]}?')
                input('Druk op Enter om het antwoord te zien... ')
                print('  →', row['torelkiva'])
        else:
            found = woorden() if args.opdracht == 'lijst' else vind(args.term, exact=args.opdracht == 'woord')
            if not found:
                print('Geen woord gevonden. Probeer een kortere zoekterm.')
                return 1
            for row in found:
                print(f'{row["torelkiva"]:<15} {row["nederlands"]:<32} ({row["soort"]})')
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'Fout: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
