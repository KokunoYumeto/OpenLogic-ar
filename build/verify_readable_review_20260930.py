"""Verify every bounded review page against complete source text and rows."""
import gzip
import hashlib
import json
from pathlib import Path
import re

from render_readable_review_20260930 import BASE, LIMIT, ROOT, relocate, digest


def main():
    receipt = json.loads((BASE / 'READABLE_REVIEW_RECEIPT_20260930.json').read_bytes())
    assert receipt['directory_sha256'] == digest(BASE / 'DIRECTORY_AR.md')
    assert receipt['machine_record_sha256'] == digest(BASE / 'DECISION_RECORD_AR.jsonl.gz')
    with gzip.open(BASE / 'DECISION_RECORD_AR.jsonl.gz', 'rt', encoding='utf-8') as stream:
        records = [json.loads(line) for line in stream]
    original_rows = [line for line in (BASE / 'DIRECTORY_AR.md').read_text(encoding='utf-8').splitlines()
                     if line.startswith('| ') and line.endswith(' |')][1:]
    assert len(records) == len(original_rows) == 1095
    targets = {c['source']: BASE / c['landing'] for c in receipt['card_pages']}
    all_ids, actual_rows = [], []
    for section in receipt['directory_pages']:
        path = BASE / section['path']
        rows = [line for line in path.read_text(encoding='utf-8').splitlines()
                if line.startswith('| ') and line.endswith(' |')][1:]
        assert len(rows) == len(section['decision_ids'])
        all_ids.extend(section['decision_ids']); actual_rows.extend(rows)
    assert all_ids == [r['decision_id'] for r in records]
    for record, expected, actual in zip(records, original_rows, actual_rows, strict=True):
        name = record['review_card']
        target = targets[name].name if name in targets else '../' + name
        assert actual == expected.replace(f']({name})', f']({target})')
    for card in receipt['card_pages']:
        original = BASE / card['source']
        assert digest(original) == card['source_sha256']
        parts = []
        for name in card['pages']:
            text = (BASE / name).read_text(encoding='utf-8')
            before, marker, after = text.partition('\n<!-- BEGIN PRESERVED REVIEW TEXT -->\n')
            assert marker
            payload, end, tail = after.rpartition('\n<!-- END PRESERVED REVIEW TEXT -->\n')
            assert end and tail == ''
            parts.append(payload)
        text = ''.join(parts)
        assert text == relocate(original.read_text(encoding='utf-8'), original, BASE / card['pages'][0])
        assert hashlib.sha256(text.encode()).hexdigest() == card['normalized_relocated_text_sha256']
    for entry in receipt['files']:
        path = BASE / entry['path']
        assert path.stat().st_size == entry['bytes'] < LIMIT
        assert digest(path) == entry['sha256']
        text = path.read_text(encoding='utf-8')
        for url in re.findall(r'(?<=\]\()([^\s)]+)(?=\))', text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url) or url.startswith(('#', '//')):
                continue
            file = url.partition('#')[0]
            target = (path.parent / file).resolve()
            target.relative_to(ROOT.resolve())
            assert target.is_file(), (path, url)
    value = {'status': 'PASS_ALL_READABLE_ROWS_TEXT_LINKS_AND_BOUNDS',
             'decisions': len(records), 'files': len(receipt['files']),
             'receipt_sha256': digest(BASE / 'READABLE_REVIEW_RECEIPT_20260930.json'),
             'all_original_rows_preserved': True, 'all_card_text_preserved': True,
             'scope': 'Deterministic presentation verification, not linguistic approval.'}
    path = BASE / 'READABLE_REVIEW_VERIFICATION_20260930.json'
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(value))


if __name__ == '__main__':
    main()
