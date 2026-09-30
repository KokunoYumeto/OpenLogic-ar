"""Bounded reading pages for the complete Arabic review; no rationale rewriting."""
from __future__ import annotations

import gzip
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'expert-review/2026-09-26-final-page-review'
PAGES = BASE / 'readable-review'
LIMIT = 130_000
PAYLOAD_LIMIT = 115_000
EAST = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
LINK = re.compile(r'(?<=\]\()([^\s)]+)(?=\))')
NOTICE = ('عرض القراءة وتقسيم الصفحات: OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra. '
          'لم تُعد صياغة التعليلات بهذا التقسيم، ولا يثبت سلامتها الدلالية أو المعجمية؛ '
          'لم تقع مراجعة بشرية شاملة، وكل اختيار قابل للتصحيح.\n')


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def relocate(text, original, destination):
    def link(match):
        url = match.group(1)
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url) or url.startswith(('#', '//')):
            return url
        file, marker, fragment = url.partition('#')
        target = (original.parent / file).resolve()
        target.relative_to(ROOT.resolve())
        return Path(os.path.relpath(target, destination.parent)).as_posix() + marker + fragment
    return LINK.sub(link, text)


def blocks(text):
    """Split at paragraph boundaries, never inside a fenced example."""
    result, pending, fence = [], [], None
    for line in text.splitlines(keepends=True):
        pending.append(line)
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = token[0]
            elif token[0] == fence:
                fence = None
        if not line.strip() and fence is None:
            result.append(''.join(pending)); pending = []
    assert fence is None, 'Unclosed source fence'
    if pending:
        result.append(''.join(pending))
    assert ''.join(result) == text
    return result


def chunks(text):
    result, pending, size = [], [], 0
    paragraphs = blocks(text)
    expanded = []
    for block in paragraphs:
        if len(block.encode('utf-8')) <= PAYLOAD_LIMIT:
            expanded.append(block)
        else:
            # Long occurrence lists are legal break points between complete
            # lines; do not divide a link or a fenced example.
            assert not re.search(r'^\s*(`{3,}|~{3,})', block, re.M)
            assert not any(line.startswith('|') for line in block.splitlines())
            expanded.extend(block.splitlines(keepends=True))
    for block in expanded:
        count = len(block.encode('utf-8'))
        assert count <= PAYLOAD_LIMIT, 'A single paragraph exceeds the reading-page bound'
        if pending and size + count > PAYLOAD_LIMIT:
            result.append(''.join(pending)); pending, size = [], 0
        pending.append(block); size += count
    if pending:
        result.append(''.join(pending))
    assert ''.join(result) == text
    return result


def write(path, text):
    data = text.encode('utf-8')
    assert len(data) < LIMIT, path
    path.write_bytes(data)
    return {'path': path.relative_to(BASE).as_posix(), 'bytes': len(data), 'sha256': digest(path)}


def generate():
    PAGES.mkdir(exist_ok=True)
    with gzip.open(BASE / 'DECISION_RECORD_AR.jsonl.gz', 'rt', encoding='utf-8') as stream:
        records = [json.loads(line) for line in stream]
    assert len(records) == len({r['decision_id'] for r in records}) == 1095
    source = BASE / 'DIRECTORY_AR.md'
    lines = source.read_text(encoding='utf-8').splitlines()
    rows = [line for line in lines if line.startswith('| ') and line.endswith(' |')]
    assert len(rows) == 1096
    files, card_entries, targets = [], [], {}
    cards = sorted({r['review_card'] for r in records} | {'SOL6_SOURCE_REFERENCES_AR.md'})
    for name in cards:
        original = BASE / name
        if original.stat().st_size < LIMIT:
            continue
        key = hashlib.sha256(name.encode()).hexdigest()[:12]
        landing = PAGES / f'card-{key}.md'
        destination = PAGES / f'card-{key}-01.md'
        normalized = original.read_text(encoding='utf-8')
        relocated = relocate(normalized, original, destination)
        parts = chunks(relocated)
        source_ids = set(re.findall(r'معرّف القرار: `([^`]+)`', normalized))
        related = [r for r in records if r['review_card'] == name or r['decision_id'] in source_ids]
        intro = ('# بطاقة المراجعة في صفحات قابلة للقراءة\n\n'
                 '[الدليل الكامل](../DIRECTORY_READABLE_AR.md) · [مدخل المراجعة](../INDEX_AR.md)\n\n'
                 f'[الملف الكامل المحفوظ]({relocate(f"]({name})", BASE / "dummy.md", landing)[2:-1]})\n\n'
                 'جميع فقرات الملف الكامل محفوظة بالترتيب؛ ينقل هذا العرض الروابط المحلية فقط '
                 'لتظل صالحة من موضع الصفحات الجديد. قد يمتد القرار الواحد على أكثر من صفحة.\n\n')
        for r in related:
            intro += f"- `{r['decision_id']}` — {r['chosen_arabic']}\n"
        intro += '\n'
        views = []
        preceding = ''
        for i, payload in enumerate(parts, 1):
            path = PAGES / f'card-{key}-{i:02}.md'
            links = [f'[فهرس هذه البطاقة]({landing.name})', '[الدليل الكامل](../DIRECTORY_READABLE_AR.md)']
            if i > 1:
                links.append(f'[السابق](card-{key}-{i-1:02}.md)')
            if i < len(parts):
                links.append(f'[التالي](card-{key}-{i+1:02}.md)')
            prior_headings = re.findall(r'^## (.+)$', preceding, re.M)
            context = ('استكمال القسم السابق: ' + prior_headings[-1] + '\n') if prior_headings else ''
            heading = '\n'.join(['# صفحة ' + str(i).translate(EAST) + ' من بطاقة المراجعة',
                                   '', ' · '.join(links), '', context, NOTICE, ''])
            text = heading + '\n<!-- BEGIN PRESERVED REVIEW TEXT -->\n' + payload
            text += '\n<!-- END PRESERVED REVIEW TEXT -->\n'
            files.append(write(path, text)); views.append(path.relative_to(BASE).as_posix())
            intro += f'- [الصفحة {str(i).translate(EAST)}]({path.name})\n'
            preceding += payload
        intro += '\n' + NOTICE
        files.append(write(landing, intro))
        targets[name] = landing
        card_entries.append({'source': name, 'source_sha256': digest(original), 'pages': views,
                             'landing': landing.relative_to(BASE).as_posix(),
                             'normalized_relocated_text_sha256': hashlib.sha256(relocated.encode()).hexdigest()})
    directory_pages = []
    index = ('# الدليل الكامل القابل للقراءة — ١٠٩٥ من ١٠٩٥\n\n'
             '[ابدأ من هنا](INDEX_AR.md) · [الجدول الكامل للتنزيل](DIRECTORY_AR.md) · '
             '[السجل الآلي الكامل](DECISION_RECORD_AR.jsonl.gz)\n\n'
             'اختر جزءًا من الجدول المرتب بالمصطلح الإنجليزي. في كل سطر اللفظ العربي، '
             'وموضع مثال، وسبب مختصر، ورابط البطاقة التي تحفظ جميع الوقوعات والتعليل الكامل '
             'وسؤال المراجع. صفحات الوحدة المعلَّمة بأنها تقريبية ليست صفحة وقوع دقيقة. '
             'لا يدل اكتمال الفهرسة على صحة كل اختيار أو اكتمال إعادة فحصه.\n\n')
    for start in range(0, len(records), 80):
        selected = records[start:start + 80]
        number = start // 80 + 1
        path = PAGES / f'directory-{number:02}.md'
        nav = '[الدليل الكامل](../DIRECTORY_READABLE_AR.md) · [ابدأ من هنا](../INDEX_AR.md)'
        if start:
            nav += f' · [السابق](directory-{number-1:02}.md)'
        if start + 80 < len(records):
            nav += f' · [التالي](directory-{number+1:02}.md)'
        text = '# قرارات المراجعة — الجزء ' + str(number).translate(EAST) + '\n\n' + nav + '\n\n'
        text += rows[0] + '\n|---|---|---|---|---|\n'
        for record, row in zip(selected, rows[start+1:start+1+len(selected)], strict=True):
            name = record['review_card']
            assert f']({name})' in row
            replacement = (targets[name].name if name in targets else '../' + name)
            text += row.replace(f']({name})', f']({replacement})') + '\n'
        text += '\n' + NOTICE
        files.append(write(path, text))
        directory_pages.append({'path': path.relative_to(BASE).as_posix(),
                                'decision_ids': [r['decision_id'] for r in selected]})
        index += (f"- [الجزء {str(number).translate(EAST)}: {selected[0]['english_term']} — "
                  f"{selected[-1]['english_term']}]({path.relative_to(BASE).as_posix()}) "
                  f"({str(len(selected)).translate(EAST)} قرارًا).\n")
    index += '\n' + NOTICE
    files.append(write(BASE / 'DIRECTORY_READABLE_AR.md', index))
    witness = targets['SOL6_SOURCE_REFERENCES_AR.md']
    value = {'status': 'PASS_BOUNDED_READING_PAGES_1095_COMPLETE',
             'model': 'GPT-6.1 Sol', 'effort': 'Ultra', 'directory_sha256': digest(source),
             'machine_record_sha256': digest(BASE / 'DECISION_RECORD_AR.jsonl.gz'),
             'source_reference_reading_entry': witness.relative_to(BASE).as_posix(),
             'directory_pages': directory_pages, 'card_pages': card_entries, 'files': files,
             'scope': 'Presentation, full row/text preservation and relocated links; not semantic/canon approval.'}
    (BASE / 'READABLE_REVIEW_RECEIPT_20260930.json').write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'status': value['status'], 'pages': len(files), 'decisions': len(records),
                      'source_reference_entry': value['source_reference_reading_entry']}))


if __name__ == '__main__':
    generate()
