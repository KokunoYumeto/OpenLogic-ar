"""Bind and present three personally assessed definitions; no translation rewrite."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

from stream_expert_review_decisions import iter_decisions

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'expert-review/2026-09-26-final-page-review'
LEDGER = ROOT / 'evidence/classical/terminology/SOL6_FUNCTION_DEFINITIONS_RECHECK_20260930.json'
INDEX = ROOT / 'tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json'
ENGLISH = ROOT.parents[1] / 'openlogic-interfarsi/repo/source/upstream'
EAST = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def bind(data: dict, records: list[dict], english: Path = ENGLISH,
         root: Path = ROOT) -> dict:
    """Fail closed on changed bodies or missing/unmapped supplied occurrences."""
    out = copy.deepcopy(data)
    if out['model'] != 'GPT-6.1 Sol' or out['effort'] != 'Ultra':
        raise ValueError('Unexpected assessment attribution')
    frozen = {r['decision_id']: r for r in records}
    ids = [r['decision_id'] for r in out['records']]
    if len(ids) != len(set(ids)) or len(ids) != 3 or set(ids) != set(frozen):
        raise ValueError('This finite assessment has exactly three frozen decisions')
    for row in out['records']:
        old = frozen[row['decision_id']]
        frozen_display = old.get('review_display', {}).get('chosen_arabic') or old['chosen_arabic']
        if row['surface_ar'] != frozen_display:
            raise ValueError('Retention cannot silently substitute source wording')
        occurrences = old['index_metadata']['occurrences']
        if len(occurrences) != row['contextual_coverage']['occurrence_groups'] or len(occurrences) != 1:
            raise ValueError('Unexpected occurrence-group count')
        if row['contextual_coverage']['source_locations'] != 3:
            raise ValueError('Unexpected finite occurrence scope')
        bindings = []
        for field, source_root, kind in (
                ('source_bindings', english, 'english'),
                ('target_bindings', root, None)):
            for witness in row[field]:
                source_path = source_root / witness['logical_path']
                if not source_path.is_file():
                    source_path = root / 'expert-review/2026-09-26-final-page-review/reexamination-source' / ('english' if kind == 'english' else 'repo') / witness['logical_path']
                raw = source_path.read_bytes()
                if (len(raw), digest(raw)) != (witness['bytes'], witness['sha256']):
                    raise ValueError('Changed source bytes: ' + witness['logical_path'])
                lines = raw.decode('utf-8-sig').splitlines()
                start, end = witness['line_start'], witness['line_end']
                if not 1 <= start <= end <= len(lines):
                    raise ValueError('Invalid passage extent')
                passage = '\n'.join(lines[start - 1:end])
                if witness.get('exact_passage', passage) != passage:
                    raise ValueError('Changed exact definition passage')
                witness['exact_passage'] = passage
                witness['passage_sha256'] = digest(passage.encode())
                if field == 'source_bindings':
                    witness['public_lf_sha256'] = digest(raw.replace(b'\r\n', b'\n'))
                actual_kind = kind or ('classical' if '/ar-classical/' in witness['logical_path'] else 'msa')
                bindings.append((actual_kind, witness))
        if sorted(k for k, _ in bindings) != ['classical', 'english', 'msa']:
            raise ValueError('Must bind both Arabic source bodies and English')
        checked = []
        locations = occurrences[0]['locations']
        if len(locations) != 3:
            raise ValueError('Uninspected additional location')
        for loc in locations:
            kind = loc['source_kind']
            matches = [w for k, w in bindings if k == kind and w['logical_path'] == loc['logical_path']]
            if len(matches) != 1:
                raise ValueError('Frozen occurrence lacks exact body witness')
            witness = matches[0]
            current = loc['line_reconciliation']
            a, b = current['current_line_start'], current['current_line_end']
            if not current['resolved'] or not witness['line_start'] <= a <= b <= witness['line_end']:
                raise ValueError('Frozen occurrence not contained in consulted passage')
            full = (english if kind == 'english' else root) / loc['logical_path']
            if not full.is_file():
                full = root / 'expert-review/2026-09-26-final-page-review/reexamination-source' / ('english' if kind == 'english' else 'repo') / loc['logical_path']
            excerpt = '\n'.join(full.read_text(encoding='utf-8-sig').splitlines()[a-1:b])
            if loc['excerpt'].strip() != excerpt.strip():
                raise ValueError('Frozen exact occurrence no longer matches')
            checked.append({'location_id': loc['location_id'], 'source_kind': kind,
                'logical_path': loc['logical_path'], 'line_start': a, 'line_end': b,
                'exact_passage': excerpt, 'file_sha256': witness['sha256'],
                'page_evidence': copy.deepcopy(loc['page_evidence'])})
        row['checked_occurrences'] = checked
        row['original_occurrences'] = copy.deepcopy(occurrences)
    return out


def render(data: dict) -> str:
    lines = ['# مقابلة ثلاثة تعريفات للدوال — ٣٠ سبتمبر ٢٠٢٦', '',
        '[مدخل المراجعة](INDEX_AR.md) · [الدليل المقروء](DIRECTORY_READABLE_AR.md)', '',
        data['scope_ar'], '',
        'OpenAI Codex — GPT-6.1 Sol، جهد Ultra: المقابلة الجديدة والتعليل اللاحق. '
        'التعليلات السابقة لـOpenAI Codex — GPT-6 Sol، جهد Ultra، محفوظة ولا يُنسب '
        'إليها هذا الدليل اللاحق. لم تقع مراجعة بشرية شاملة. لا تغيير في متن الكتاب، '
        'وكل اختيار مفتوح للتصحيح.', '',
        'انظر أولًا إلى الكلمة والصفحة والسؤال. روابط الأسطر أدناه تثبت نص '
        'التعريف نفسه، لا تعليق اسم القسم. الصفحات أرقام صفحات ملف PDF؛ قد يختلف '
        'عنها الرقم المطبوع كما تبينه إحالات الوقوع.', '']
    for row in data['records']:
        lines += ['## ' + row['surface_ar'], '',
            'معرّف القرار: `' + row['decision_id'] + '`؛ الوحدة `OLP-0022`.', '']
        pages = []
        for loc in row['checked_occurrences']:
            for p in loc['page_evidence']:
                label = p['reader'] + ': PDF ص ' + '، '.join(str(n).translate(EAST) for n in p['pdf_pages'])
                printed = p.get('printed_pages') or []
                if printed:
                    label += '؛ المطبوع ' + '، '.join(str(v['printed_page']).translate(EAST) for v in printed)
                pages.append(label)
        lines += ['**أين؟** ' + ' · '.join(pages), '',
            '**ما الذي يستحق المراجعة؟** ' + row['expert_question_ar'], '',
            '**المعنى:** ' + row['sense_ar'], '', '**لماذا أُبقي؟** ' + row['rationale_ar'], '',
            '**البدائل:** ' + '؛ '.join(row['alternatives_ar']), '',
            '**الثقة وحدودها:** ' + row['confidence_ar'], '',
            '**حد الشاهد:** ' + row['canon_limit_ar'], '', '**الشواهد المقروءة:**', '']
        for evidence in row['canon_evidence']:
            source = data['canon_sources'][evidence['source_id']]
            place = evidence.get('section_ar') or ('PDF ص ' + str(evidence['physical_pdf_page']).translate(EAST)
                + '؛ المطبوع ' + str(evidence['printed_page']).translate(EAST) + '؛ ' + evidence['entry'])
            lines.append('- [' + source['title_ar'] + '](' + source['url'] + ')، ' + place
                + ': «' + evidence['short_quote_ar'] + '». ' + evidence['relation_ar'])
        lines += ['', '**نصوص التعريف المقابلة (كل المواضع الثلاثة المسجلة):**', '']
        for field in ('source_bindings', 'target_bindings'):
            for w in row[field]:
                is_en = field == 'source_bindings'
                label = 'الأصل الإنجليزي' if is_en else ('التراثية' if '/ar-classical/' in w['logical_path'] else 'المعيارية للطبعتين الدولية والمشرق')
                repository = 'OpenLogicProject/OpenLogic' if is_en else 'KokunoYumeto/OpenLogic-ar'
                commit = data['english_source_commit'] if is_en else data['arabic_source_commit']
                url = f"https://github.com/{repository}/blob/{commit}/{w['logical_path']}#L{w['line_start']}-L{w['line_end']}"
                lines += ['- [' + label + '، الأسطر ' + str(w['line_start']).translate(EAST) + '–'
                    + str(w['line_end']).translate(EAST) + '](' + url + ')؛ SHA-256: `'
                    + (w.get('public_lf_sha256') or w['sha256']) + '`.', '',
                    '```tex', w['exact_passage'], '```', '']
        lines += ['[التعليل السابق المحفوظ](BATCH_31_38_AR.md). لا تعمم هذه المقابلة '
                  'على سائر استعمالات الأسرة الاصطلاحية في الكتاب.', '']
    lines += ['## هوية المصادر وحدود المقارنة', '']
    for source in data['canon_sources'].values():
        lines += ['- [' + source['title_ar'] + '](' + source['url'] + ')؛ '
            + source['edition_ar'] + '. ' + source['limits_ar']]
    lines += ['', data['source_identity_note_ar'], '',
        'مقارنة الأسلوب: [رَصائف](' + data['register_comparison']['corpus_url'] + ')؛ '
        + data['register_comparison']['relevance_ar'] + ' '
        + data['register_comparison']['limits_ar'], '',
        'الصيغ والمؤلفات المنقولة للشواهد محفوظة في مصادرها، لا يعاد ترخيصها '
        'بوصفها نصًا لـOpenLogic. سجل القرارات يثبت مواضع الفقرات وتجزئات '
        'النسخ المقروءة، ولا يحتوي الأزواج التراثية الكاملة أو صفحة الموسوعة الكاملة.', '']
    return '\n'.join(lines)


def capture_public_sources(data: dict) -> None:
    """Three anonymous pinned downloads, no retries or remote writes."""
    inventory = {}
    for row in data['records']:
        for field in ('source_bindings', 'target_bindings'):
            for witness in row[field]:
                inventory[(field, witness['logical_path'])] = witness
    files = []
    for (field, relative), witness in sorted(inventory.items()):
        is_en = field == 'source_bindings'
        repository = 'OpenLogicProject/OpenLogic' if is_en else 'KokunoYumeto/OpenLogic-ar'
        commit = data['english_source_commit'] if is_en else data['arabic_source_commit']
        url = f'https://raw.githubusercontent.com/{repository}/{commit}/{relative}'
        with urlopen(Request(url, headers={'User-Agent': 'OpenLogic-Ar source verification'}), timeout=30) as response:
            raw = response.read(65537)
        if len(raw) > 65536:
            raise ValueError('Narrow source download unexpectedly large')
        expected = witness.get('public_lf_sha256') or witness['sha256']
        if digest(raw) != expected:
            raise ValueError('Public source identity mismatch: ' + relative)
        local = (ENGLISH if is_en else ROOT) / relative
        local_raw = local.read_bytes()
        if digest(local_raw) != witness['sha256'] or (local_raw.replace(b'\r\n', b'\n') if is_en else local_raw) != raw:
            raise ValueError('Public source is not the inspected local text')
        captured = BASE / 'reexamination-source' / ('english' if is_en else 'repo') / relative
        if captured.exists() and captured.read_bytes() != local_raw:
            raise ValueError('Do not overwrite a different source witness')
        captured.parent.mkdir(parents=True, exist_ok=True)
        captured.write_bytes(local_raw)
        files.append({'url': url, 'public_bytes': len(raw), 'public_sha256': digest(raw),
            'snapshot_path': captured.relative_to(ROOT).as_posix(),
            'snapshot_bytes': len(local_raw), 'snapshot_sha256': digest(local_raw),
            'only_crlf_lf_difference': is_en and local_raw != raw})
    receipt = BASE / 'FUNCTION_DEFINITION_SOURCE_READBACK_20260930.json'
    payload = (json.dumps({'status': 'PASS_THREE_ANONYMOUS_PINNED_SOURCE_FILES',
        'files': files, 'ledger_sha256': digest(LEDGER.read_bytes())},
        ensure_ascii=False, indent=2) + '\n').encode()
    if receipt.exists() and receipt.read_bytes() != payload:
        raise ValueError('Different historical source readback exists')
    receipt.write_bytes(payload)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--capture-public-sources', action='store_true')
    args = parser.parse_args()
    data = json.loads(LEDGER.read_bytes())
    if digest(INDEX.read_bytes()).upper() != data['source_index_sha256']:
        raise ValueError('Frozen index identity changed')
    ids = {r['decision_id'] for r in data['records']}
    selected = [r for r in iter_decisions(INDEX) if r['decision_id'] in ids]
    bound = bind(data, selected)
    machine = (json.dumps(bound, ensure_ascii=False, indent=2) + '\n').encode()
    card = render(bound).encode()
    card_path = BASE / bound['review_card']
    if args.check:
        if LEDGER.read_bytes() != machine or not card_path.exists() or card_path.read_bytes() != card:
            raise ValueError('Fresh assessment/card not reproducible')
    else:
        LEDGER.write_bytes(machine)
        card_path.write_bytes(card)
    if args.capture_public_sources:
        capture_public_sources(bound)
    print(json.dumps({'status': 'PASS_THREE_DEFINITION_BINDINGS_AND_ARABIC_PRESENTATION',
        'decisions': len(bound['records']), 'source_locations': 9, 'body_changes': 0,
        'ledger_sha256': digest(machine), 'card_sha256': digest(card),
        'scope': 'Three named definitions only, not full interval or term-family completion'}))


if __name__ == '__main__':
    main()
