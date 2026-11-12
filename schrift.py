#!/usr/bin/env python3
"""Torel-schrift: een eigen glyph per letter. Visuele omzetting, GEEN encryptie."""
from __future__ import annotations
import html
from pathlib import Path
import sys

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
MAX_SVG_TEXT = 2000


def paths(letter: str) -> str:
    idx = ALPHABET.find(letter.lower())
    if idx < 0:
        return ""
    branch_a = idx % 4
    branch_b = (idx // 4) % 4
    dot_idx = idx // 16
    # Een stam en twee gebroken armaturen. 26 verschillende combinaties.
    stroke = '<path d="M 14 3 L 14 33" />'
    for y, arm in [(10, branch_a), (25, branch_b)]:
        coords = [(3, y - 7), (3, y + 7), (25, y - 7), (25, y + 7)]
        ex, ey = coords[arm]
        stroke += f'<path d="M 14 {y} L {ex} {ey}" />'
    if dot_idx == 1:
        stroke += '<circle cx="22" cy="4" r="2" fill="#172638" stroke="none" />'
    return stroke


def draw_glyph(letter: str, x: int, y: int, width: int = 32) -> str:
    return f'<g transform="translate({x},{y})" fill="none" stroke="#172638" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{paths(letter)}</g>'


def alphabet_svg() -> str:
    lines = []
    for i, char in enumerate(ALPHABET):
        col, row = i % 7, i // 7
        x, y = 38 + col * 104, 92 + row * 92
        lines.append(draw_glyph(char, x, y))
        lines.append(f'<text x="{x+12}" y="{y+57}" font-size="18" text-anchor="middle" fill="#455264">{char.upper()}</text>')
    content = '\n'.join(lines)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="795" height="560" viewBox="0 0 795 560">
<rect width="795" height="560" fill="#f6f8fa"/>
<text x="38" y="40" font-family="sans-serif" font-size="25" font-weight="bold" fill="#172638">Torel-schrift — alfabet</text>
<text x="38" y="64" font-family="sans-serif" font-size="12" fill="#455264">Origineel visueel lettersysteem. Geen cryptografische versleuteling.</text>
{content}
</svg>'''


def sentence_svg(sentence: str) -> str:
    if len(sentence) > MAX_SVG_TEXT:
        raise ValueError("Maximaal 2.000 tekens voor één SVG-afbeelding.")
    x, y = 25, 70
    items = []
    maxx = 0
    for ch in sentence:
        if ch == '\n' or x > 900:
            maxx = max(maxx, x)
            x, y = 25, y + 57
            if ch == '\n':
                continue
        if ch.isspace():
            x += 21
        elif ch.lower() in ALPHABET:
            items.append(draw_glyph(ch, x, y))
            x += 31
        else:
            items.append(f'<text x="{x+8}" y="{y+32}" font-size="25" fill="#172638">{html.escape(ch if ch.isprintable() else "?")}</text>')
            x += 18
    maxx = max(maxx, x)
    h = y + 100
    w = max(500, min(960, maxx + 25))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect width="{w}" height="{h}" fill="#f6f8fa"/>
<text x="25" y="34" font-family="sans-serif" font-size="18" fill="#455264">Torelkiva — Torel-schrift (niet versleuteld)</text>
{''.join(items)}
</svg>'''


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]).strip() or "Mi Torelkivaem vara."
    Path("TOREL_BERICHT.svg").write_text(sentence_svg(text), encoding="utf-8")
    print("Torel-schrift gemaakt: TOREL_BERICHT.svg (geen encryptie)")
