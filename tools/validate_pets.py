#!/usr/bin/env python3
"""Check pet package integrity and atlas structure, not visual animation quality."""
import hashlib
import json
import re
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6]


def child(base, relative):
    path = (base / relative).resolve()
    path.relative_to(base.resolve())
    return path


def validate(root=ROOT):
    errors = []
    seen = set()
    try:
        catalog = json.loads((root / 'catalog.json').read_text(encoding='utf-8'))
        if catalog.get('schemaVersion') != 1 or not catalog.get('pets'):
            raise ValueError('Catalog schema must be 1 and contain pets')
    except (OSError, ValueError) as exc:
        return [f'catalog: {exc}']
    for relative in catalog['pets']:
        try:
            path = child(root, relative)
            pet = json.loads(path.read_text(encoding='utf-8'))
            if pet.get('schemaVersion') != 1:
                raise ValueError('Unknown metadata schema')
            for field in ('id', 'name', 'author', 'version', 'license'):
                if not isinstance(pet.get(field), str) or not pet[field].strip():
                    raise ValueError(f'Missing or blank {field}')
            if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', pet['id']):
                raise ValueError('Invalid pet ID')
            if pet['id'] in seen:
                raise ValueError('Duplicate pet ID')
            seen.add(pet['id'])
            sheet = child(path.parent, pet['spritesheet'])
            preview = child(path.parent, pet['preview'])
            if not preview.is_file():
                raise ValueError('Preview is missing')
            data = sheet.read_bytes()
            if not 0 < len(data) <= 20 * 1024 * 1024:
                raise ValueError('Image must be between 1 byte and 20 MiB')
            if hashlib.sha256(data).hexdigest() != pet['sha256']:
                raise ValueError('SHA-256 mismatch')
            version = pet['spriteVersionNumber']
            if version not in (1, 2):
                raise ValueError('Sprite version must be 1 or 2')
            counts = COUNTS + ([8, 8] if version == 2 else [])
            with Image.open(sheet) as image:
                expected_format = {'.png': 'PNG', '.webp': 'WEBP'}.get(sheet.suffix.lower())
                if not expected_format or image.format != expected_format:
                    raise ValueError('Extension must match encoded PNG/WebP format')
                if image.size != (1536, len(counts) * 208):
                    raise ValueError('Image dimensions do not match sprite version')
                if 'A' not in image.getbands():
                    raise ValueError('Image has no alpha channel')
                alpha = image.getchannel('A')
                if alpha.getextrema()[0] != 0:
                    raise ValueError('Image has no fully transparent pixels')
                for row, count in enumerate(counts):
                    for column in range(8):
                        cell = alpha.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))
                        maximum = cell.getextrema()[1]
                        if column < count and maximum == 0:
                            errors.append(f'{relative}: missing artwork at row {row}, frame {column}')
                        elif column >= count and maximum != 0:
                            errors.append(f'{relative}: unused row {row}, frame {column} is not transparent')
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f'{relative}: {exc}')
    return errors


if __name__ == '__main__':
    errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        raise SystemExit(1)
    print('All pet packages passed metadata, hash, image and frame structure checks.')
