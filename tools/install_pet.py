#!/usr/bin/env python3
"""Open the documented Codex pet installation flow; does not bypass app approval."""
import argparse
import json
import re
import subprocess
import sys
import webbrowser
from pathlib import Path
from urllib.parse import quote, urlencode

ROOT = Path(__file__).resolve().parents[1]


def build_url(pet_id):
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
    repository = catalog['repository']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('Invalid repository owner/name')
    for relative in catalog['pets']:
        path = (ROOT / relative).resolve()
        path.relative_to(ROOT)
        pet = json.loads(path.read_text(encoding='utf-8'))
        if pet['id'] != pet_id:
            continue
        sheet = (path.parent / pet['spritesheet']).resolve()
        sheet.relative_to(path.parent)
        if pet['spriteVersionNumber'] not in (1, 2):
            raise ValueError('Unsupported sprite version')
        if not pet['name'].strip():
            raise ValueError('Pet name must not be blank')
        asset_path = sheet.relative_to(ROOT).as_posix()
        image_url = f"https://raw.githubusercontent.com/{repository}/{quote(catalog['branch'], safe='')}/{quote(asset_path, safe='/')}"
        return 'codex://pets/install?' + urlencode({
            'name': pet['name'],
            'imageUrl': image_url,
            'description': pet.get('description', ''),
            'spriteVersionNumber': pet['spriteVersionNumber'],
        })
    raise ValueError(f'Unknown pet: {pet_id}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pet_id')
    parser.add_argument('--print-url', action='store_true', help='Print URL without opening the app')
    args = parser.parse_args()
    try:
        url = build_url(args.pet_id)
        if args.print_url:
            print(url)
            return 0
        if sys.platform == 'darwin':
            subprocess.run(['open', url], check=True)
        elif not webbrowser.open(url):
            raise RuntimeError('No app/browser accepted the URL; use --print-url and open it manually')
        print('Opened the Codex install flow. Complete installation in the app, then select the pet in Settings > Pets.')
        return 0
    except (ValueError, KeyError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f'Installation flow could not be opened: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
