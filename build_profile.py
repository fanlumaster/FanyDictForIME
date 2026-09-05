#!/usr/bin/env python3
"""Public dictionary product builds: desktop (all features), mobile (compact pinyin)."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile

import build_all
from profiles.compact import compact_dictionary

ROOT = Path(__file__).resolve().parent
FORMAT_VERSION = 1
MANIFEST = 'dictionary-manifest.json'


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def provenance() -> dict:
    commit = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = bool(subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain'], text=True).strip())
    return {'repository': 'metasequoiaime/MSIME-Dict', 'commit': commit, 'dirty': dirty}


def write_manifest(output: Path, profile: str, names: list[str], source_database: str | None = None, minimum_weight: int = 2000) -> dict:
    manifest = {
        'manifest_version': 1, 'profile': profile, 'format_version': FORMAT_VERSION,
        'engine_compatibility': {'dictionary_format': 1, 'japanese_model_magic': 'MSJPDT1' if profile == 'desktop' else None},
        'source': provenance(),
        'custom_dictionary_commit': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD:MetasequoiaImeCustomDict'], text=True).strip() if profile == 'desktop' else None,
        'references': {name: {'repository': repo, 'commit': revision}
                       for name, (repo, revision) in build_all.REFERENCES.items()} if profile == 'desktop' else {},
        'mozc_revision': build_all.MOZC_REVISION if profile == 'desktop' else None,
        'features': ['pinyin', 'wubi', 'quick_phrases', 'english', 'emoji', 'kaomoji', 'symbols', 'japanese']
                    if profile == 'desktop' else ['pinyin'],
        'files': {name: {'sha256': digest(output / name), 'size': (output / name).stat().st_size} for name in names},
    }
    if source_database:
        manifest['source_database_sha256'] = source_database
        manifest['compaction'] = {'minimum_phrase_weight': minimum_weight, 'keep_all_single_characters': True}
    (output / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (output / 'SHA256SUMS.txt').write_text(''.join(f'{digest(output / name)}  {name}\n' for name in [*names, MANIFEST]))
    return manifest


def verify(output: Path, expected_profile: str | None = None) -> dict:
    manifest = json.loads((output / MANIFEST).read_text())
    if manifest.get('manifest_version') != 1 or manifest.get('format_version') != FORMAT_VERSION:
        raise ValueError('Unsupported dictionary product format')
    profile = manifest.get('profile')
    if profile not in ('desktop', 'mobile') or (expected_profile and profile != expected_profile):
        raise ValueError('Dictionary product profile mismatch')
    required = set(build_all.SHIPPING_ARTIFACTS) if profile == 'desktop' else {'msime.db', 'msime.db.sha256'}
    if set(manifest['files']) != required:
        raise ValueError('Dictionary artifact set does not match its profile')
    for name, entry in manifest['files'].items():
        if Path(name).name != name or digest(output / name) != entry['sha256']:
            raise ValueError(f'Dictionary artifact changed: {name}')
    for name in required:
        if name.endswith('.db'):
            with sqlite3.connect((output / name).resolve().as_uri() + '?mode=ro', uri=True) as database:
                if database.execute('PRAGMA integrity_check').fetchone() != ('ok',):
                    raise ValueError(f'{name}: invalid SQLite database')
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['desktop', 'mobile'], default='desktop')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--source', type=Path, help='Use an existing full msime.db for the mobile profile')
    parser.add_argument('--fetch-references', action='store_true')
    parser.add_argument('--minimum-weight', type=int, default=2000)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    output = (args.output or ROOT / 'out' / args.profile).resolve()
    if args.verify:
        verify(output, args.profile)
        return
    if args.source and args.profile != 'mobile':
        parser.error('--source is only valid for the mobile profile')
    if args.minimum_weight < 0:
        parser.error("--minimum-weight must be nonnegative")
    if args.source and args.source.resolve() == output / "msime.db":
        parser.error("The mobile output must not overwrite its source database")
    if not args.source:
        command = [sys.executable, str(ROOT / 'build_all.py'), '--clean', '--require-all']
        if args.profile == 'mobile':
            command += ['--only', 'quanpin']
        if args.fetch_references:
            command += ['--fetch-references']
        subprocess.run(command, check=True)
    if args.profile == 'desktop':
        subprocess.run([sys.executable, str(ROOT / 'tools/verify_dictionaries.py')], check=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        incoming = Path(temporary)
        source_hash = None
        if args.profile == 'mobile':
            source = (args.source or ROOT / 'out/msime.db').resolve()
            source_hash = digest(source)
            compact_dictionary(source, incoming / 'msime.db', args.minimum_weight)
            names = ['msime.db', 'msime.db.sha256']
        else:
            names = list(build_all.SHIPPING_ARTIFACTS)
            for name in names:
                shutil.copyfile(ROOT / 'out' / name, incoming / name)
        write_manifest(incoming, args.profile, names, source_hash, args.minimum_weight)
        verify(incoming, args.profile)
        output.mkdir(parents=True, exist_ok=True)
        for name in [*names, MANIFEST, 'SHA256SUMS.txt']:
            shutil.copyfile(incoming / name, output / name)
    print(f'Verified {args.profile} dictionary product: {output}')


if __name__ == '__main__':
    main()
