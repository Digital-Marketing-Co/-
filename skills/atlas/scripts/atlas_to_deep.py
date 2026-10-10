#!/usr/bin/env python3
"""Validate and adapt supplied spatial records to the existing deep renderer."""
from __future__ import annotations

import argparse
from copy import deepcopy
import html
import json
import math
from pathlib import Path

SCHEMA = Path(__file__).resolve().parents[1] / 'assets/schema/atlas.schema.json'


def validate_schema(value, schema: dict, definitions: dict, path: str = '$') -> None:
    """Validate the keywords used by the bundled schema, without dependencies.

    This is a validator for this schema only, not a general JSON Schema engine.
    """
    if '$ref' in schema:
        ref = schema['$ref']
        if not ref.startswith('#/$defs/'):
            raise ValueError('Unsupported schema reference')
        schema = definitions[ref.rsplit('/', 1)[1]]
    types = {'object': lambda v: isinstance(v, dict),
             'array': lambda v: isinstance(v, list),
             'string': lambda v: isinstance(v, str),
             'number': lambda v: type(v) in (int, float),
             'integer': lambda v: type(v) is int,
             'boolean': lambda v: isinstance(v, bool),
             'null': lambda v: v is None}
    if 'anyOf' in schema:
        for candidate in schema['anyOf']:
            try:
                validate_schema(value, candidate, definitions, path)
                break
            except ValueError:
                pass
        else:
            raise ValueError(f'{path}: no supported shape matched')
    if 'type' in schema:
        allowed = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        if not any(types[kind](value) for kind in allowed):
            raise ValueError(f'{path}: expected {allowed}')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: unsupported value')
    if isinstance(value, dict):
        for name in schema.get('required', []):
            if name not in value:
                raise ValueError(f'{path}: missing {name}')
        for name, item in value.items():
            if name in schema.get('properties', {}):
                validate_schema(item, schema['properties'][name], definitions, f'{path}.{name}')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            raise ValueError(f'{path}: too few records')
        for index, item in enumerate(value):
            if 'items' in schema:
                validate_schema(item, schema['items'], definitions, f'{path}[{index}]')
    if isinstance(value, str) and len(value.strip()) < schema.get('minLength', 0):
        raise ValueError(f'{path}: empty text')
    if type(value) in (int, float):
        if not math.isfinite(value):
            raise ValueError(f'{path}: require a finite number')
        if value < schema.get('minimum', float('-inf')) or value > schema.get('maximum', float('inf')):
            raise ValueError(f'{path}: value outside range')


def validate(data: dict) -> None:
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    validate_schema(data, schema, schema['$defs'])
    records = list(data.get('nodes') or []) + list(data.get('gazetteer') or [])
    if any(record.get('coordinates') for record in records) and not data.get('projection'):
        raise ValueError('Coordinates require a projection or coordinate-reference-system note')
    identifiers = [record['id'] for record in data.get('nodes', [])]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError('Node identifiers must be unique')
    for edge in data.get('edges', []):
        if edge['source'] not in identifiers or edge['target'] not in identifiers:
            raise ValueError('Edge endpoints must identify supplied nodes')


def display(value) -> str:
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return html.escape(str(value))


def record_paragraphs(record: dict) -> list[str]:
    """Render supplied fields in stable order; retain full records in deep JSON."""
    label = record.get('name') or record.get('title') or record['id']
    paragraphs = [f'<b>{display(label)}</b>']
    for key, value in record.items():
        if key in {'name', 'title'} or value in (None, '', [], {}):
            continue
        if key == 'paragraphs':
            paragraphs.extend(deepcopy(value))
        elif key == 'description':
            paragraphs.append(str(value))
        elif key == 'notes':
            paragraphs.append('Source notes: {{' + ', '.join(str(n) for n in value) + '}}')
        else:
            paragraphs.append(f'<b>{display(key.replace("_", " ").title())}:</b> {display(value)}')
    return paragraphs


def adapt(data: dict) -> dict:
    validate(data)
    result = deepcopy(data)
    # Deep prints bibliography text; keep original structured entries for handoff.
    result['atlas_bibliography'] = deepcopy(data.get('bibliography') or [])
    result['bibliography'] = [entry if isinstance(entry, str) else entry['text']
                              for entry in data.get('bibliography') or []]
    sections = result['sections']
    insertion = next((i for i, section in enumerate(sections)
                      if section.get('kind') in {'notes', 'bibliography'}), len(sections))
    additions = []
    if data.get('projection'):
        additions.append({'id':'atlas-reference-system', 'title':'Coordinate reference system',
                          'kind':'body', 'paragraphs':[display(data['projection'])]})
    for key, title in [('nodes','Node inventory'), ('gazetteer','Gazetteer')]:
        if data.get(key):
            paragraphs = [paragraph for record in data[key] for paragraph in record_paragraphs(record)]
            additions.append({'id':f'atlas-{key}', 'title':title, 'kind':'body', 'paragraphs':paragraphs})
    if data.get('edges'):
        additions.append({'id':'atlas-connections', 'title':'Connections', 'kind':'body',
                          'paragraphs':[display(edge) for edge in data['edges']]})
    sections[insertion:insertion] = additions
    for kind, title in [('notes','Notes'), ('bibliography','Bibliography')]:
        if result.get(kind) and not any(section.get('kind') == kind for section in sections):
            sections.append({'kind':kind, 'title':title, 'paragraphs':[]})
    return result


def convert(source: Path, out: Path | None = None) -> Path:
    source = source.expanduser().resolve()
    destination = out.expanduser().resolve() if out else source.with_name('deep.json')
    if destination == source:
        raise ValueError('Adapter output must differ from the atlas source')
    data = adapt(json.loads(source.read_text(encoding='utf-8')))
    # Resolve visual paths against the source, including when output is elsewhere.
    def resolve_visual_paths(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key == 'path' and isinstance(item, str) and item:
                    path = Path(item).expanduser()
                    value[key] = str((path if path.is_absolute() else source.parent / path).resolve())
                elif key not in {'nodes', 'gazetteer', 'edges', 'atlas_bibliography'}:
                    resolve_visual_paths(item)
        elif isinstance(value, list):
            for item in value:
                resolve_visual_paths(item)
    resolve_visual_paths(data['sections'])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('atlas_json', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    print(convert(args.atlas_json, args.out))


if __name__ == '__main__':
    main()
