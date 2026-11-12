#!/usr/bin/env python3
"""Maak controlebestand en reproduceerbaar Torelkiva ZIP-pakket (standaardbibliotheek)."""
from __future__ import annotations
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'Torelkiva_2_0_compleet.zip'
MANIFEST=ROOT/'SHA256SUMS.txt'

def sources():
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file():continue
        rel=path.relative_to(ROOT)
        if any(part in ('__pycache__','.pytest_cache','.git','.venv','.mypy_cache') for part in rel.parts):continue
        if path.name in ('.DS_Store','TOREL_BERICHT.svg','SHA256SUMS.txt') or path.suffix in ('.pyc','.tkv'):continue
        yield path,rel

def main():
    # Manifest: exact SHA256 van ieder bestand, behalve het manifest zelf.
    files=list(sources())
    lines=[f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel.as_posix()}' for path,rel in files]
    MANIFEST.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    files.append((MANIFEST,Path('SHA256SUMS.txt')))
    with ZipFile(OUT,'w',compression=ZIP_DEFLATED,compresslevel=9) as out:
        for path,rel in sorted(files,key=lambda item:item[1].as_posix()):
            info=ZipInfo('Torelkiva_2_0/'+rel.as_posix(),date_time=(2026,11,13,0,0,0))
            info.compress_type=ZIP_DEFLATED
            info.external_attr=(0o755 if path.suffix=='.sh' else 0o644)<<16
            out.writestr(info,path.read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=9)
    print(f'Bestanden: {len(files)}; manifest: {len(lines)}; ZIP: {OUT}; {OUT.stat().st_size:,} bytes')
if __name__=='__main__':main()
