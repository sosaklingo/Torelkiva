#!/usr/bin/env python3
"""Bouw een herhaalbaar Torelkiva 2.1-archief uit ALLEEN goedgekeurde bestanden.

De expliciete allowlist voorkomt dat nieuwe .env-, privé- of sleutelbestanden
per ongeluk openbaar worden gemaakt via de release.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / 'Torelkiva_2_1_definitief.zip'
MANIFEST = ROOT / 'SHA256SUMS.txt'
FILES = (
    '.github/workflows/tests.yml', '.gitignore', 'CHANGELOG.md', 'CITATION.cff',
    'CONTRIBUTING.md', 'GRAMMATICA.md', 'HERKOMST.md', 'LEESMIJ.md',
    'OEFENBOEK.md', 'ONTWIKKELINGSVERKLARING.md', 'ONTWIKKELINGSVERKLARING.pdf',
    'PROJECT.json', 'PUBLICEREN_OP_GITHUB.md', 'README.md',
    'START_LINUX.sh', 'START_WINDOWS.bat', 'TOREL_ALFABET.svg',
    'Torelkiva_Handleiding_2_1.pdf', 'VEILIGHEID.md', 'VERTALER.md',
    'VERIFICATIE.md', 'VOORBEELD_TOREL.svg', 'WOORDENBOEK.md', 'WOORDENLIJST.tsv',
    'app.py', 'assets/Torel_alfabet_preview.png', 'offline.html', 'requirements.txt',
    'schrift.py', 'taal.py', 'tests/test_crypto.py', 'tests/test_crypto_extra.py',
    'tests/test_language.py', 'tests/test_legacy_compat.py',
    'tests/test_release.py', 'tests/test_translation.py',
    'tests/test_translation_quality.py', 'tools/build_release.py',
    'torelkiva.py', 'vertaler.py',
)


def sources():
    if len(FILES) != len(set(FILES)):
        raise ValueError('De allowlist bevat dubbele bestandsnamen.')
    for name in sorted(FILES):
        rel = Path(name)
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Onveilig bestandspad in de allowlist.')
        path = ROOT / rel
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f'Goedkeurd projectbestand ontbreekt of is een symlink: {name}')
        yield path, rel


def main():
    files = list(sources())
    lines = [f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel.as_posix()}'
             for path, rel in files]
    MANIFEST.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    files.append((MANIFEST, Path('SHA256SUMS.txt')))
    with ZipFile(OUT, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path, rel in sorted(files, key=lambda item: item[1].as_posix()):
            info = ZipInfo('Torelkiva_2_1/' + rel.as_posix(),
                           date_time=(2026, 11, 13, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = (0o755 if path.suffix == '.sh' else 0o644) << 16
            archive.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED,
                             compresslevel=9)
    print(f'Bestanden: {len(files)}, checksums: {len(lines)}, ZIP: {OUT}')


if __name__ == '__main__':
    main()
