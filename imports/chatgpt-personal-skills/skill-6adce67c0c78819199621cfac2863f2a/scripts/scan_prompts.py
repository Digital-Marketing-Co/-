#!/usr/bin/env python3
"""Find normalized repeated phrases and similar blobs in verified user JSONL."""
import argparse
import difflib
import json
import re
from collections import defaultdict
from pathlib import Path


def scan(records):
    messages, seen = [], set()
    for r in records:
        if r.get('role') != 'user':
            continue
        cid, mid, body = r.get('conversation_id'), r.get('message_id'), r.get('text')
        if not isinstance(cid, str) or not cid or not isinstance(mid, str) or not mid or not isinstance(body, str):
            raise ValueError('User records require conversation_id, message_id, and text strings')
        key = (cid, mid)
        if key in seen:
            continue
        if len(body) > 50000:
            raise ValueError('Message exceeds 50,000 characters; split with explicit provenance')
        seen.add(key)
        messages.append((cid, mid, body, re.findall(r'/?[\w-]+|[^\w\s]', body.casefold())))
    if len(messages) > 1000:
        raise ValueError('Limit 1,000 unique user messages per batch; report batch scope')
    phrases = defaultdict(set)
    for cid, mid, body, tokens in messages:
        for size in range(4, min(18, len(tokens)) + 1):
            for start in range(len(tokens) - size + 1):
                phrases[tuple(tokens[start:start+size])].add((cid, mid))
    candidates = []
    for phrase, refs in phrases.items():
        support = len({c for c, m in refs})
        if support >= 2:
            candidates.append({'normalized_phrase': ' '.join(phrase), 'conversations': support,
                               'messages': len(refs), 'sources': sorted(refs)})
    candidates.sort(key=lambda x: (-x['conversations'] * len(x['normalized_phrase']), x['normalized_phrase']))
    groups = []
    # Compare against each deterministic group representative; groups are not transitive claims.
    for cid, mid, body, tokens in sorted(messages, key=lambda m: (m[0], m[1])):
        if len(tokens) < 8:
            continue
        for g in groups:
            ratio = difflib.SequenceMatcher(None, g['_tokens'], tokens, autojunk=False).ratio()
            if ratio >= 0.82:
                g['members'].append({'conversation_id': cid, 'message_id': mid, 'similarity': round(ratio, 4)})
                break
        else:
            groups.append({'representative': body, '_tokens': tokens,
                           'members': [{'conversation_id': cid, 'message_id': mid, 'similarity': 1.0}]})
    fuzzy = []
    for g in groups:
        g.pop('_tokens')
        if len({m['conversation_id'] for m in g['members']}) >= 2:
            fuzzy.append(g)
    return {'verified_user_messages': len(messages), 'conversations': len({m[0] for m in messages}),
            'matching': 'casefolded token sequences; not byte-exact',
            'phrases': candidates[:100], 'similar_blobs': fuzzy,
            'limits': '4–18 token phrases; similarity >=0.82; representative grouping; input-only counts'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.input.stat().st_size > 5_000_000:
        p.error('Input exceeds 5 MB; split into explicitly scoped batches')
    try:
        records = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
        if not all(isinstance(r, dict) for r in records):
            raise ValueError('Every record must be an object')
        result = scan(records)
    except (ValueError, TypeError) as exc:
        p.error(str(exc))
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
