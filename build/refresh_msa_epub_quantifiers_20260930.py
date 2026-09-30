"""Propagate the exact published OLP-0087 corrections into two frozen EPUBs.

Render only this source unit with the existing native-MathML renderer. Keep
every other body, original ID, proof tree and native formula intact. This is
a finite source successor, not an override of the historical full-body freeze.
Fresh EPUB checkers and exact current source packaging remain release gates.
"""
import argparse
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import zipfile

from lxml import etree

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from review_sol6_epub_20260930 import identity, pack, require, validate_xhtml
import rebind_msa_closure_manifest as authority

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tmp/epub/sol6-independent-review-20260930-r1'
BODY = 'OEBPS/modern-reader-3-7-3.xhtml'
X = 'http://www.w3.org/1999/xhtml'
M = 'http://www.w3.org/1998/Math/MathML'
E = 'http://www.idpf.org/2007/ops'
EXPECTED = {
    'international': '66cb56114ba101bd8e5f8648f1adae60807d5e860fb989bef6e711e8bbfde17c',
    'machrek': '69e074961e9633ff786f392cdaea73359ca5bbff7cf9e1f51148e232f1bcc057',
}
DISCLOSURE = (
    'الترجمة الموروثة: OpenAI Codex — GPT-5.6 Sol، جهد Ultra. تحويل EPUB '
    'الموروث وتجميعه: OpenAI Codex — GPT-6 Sol، جهد Ultra. المقابلة وتصحيح '
    'عبارتي شروط التكميم في OLP-0087 ونقلهما إلى هذين الكتابين: OpenAI Codex — '
    'GPT-6.1 Sol، جهد Ultra. تشمل النسخة استثناء الفرض الذي يسقطه حذف '
    'الوجودي وإغلاق حد الاستبدال، مع هامش التصحيح. بقي سائر متن EPUB '
    'وصِيَغه كما في النسخة المحفوظة؛ لا يدعي هذا العمل مراجعة دلالية للكتاب '
    'كله أو مطابقة تنضيد PDF. لم تقع مراجعة بشرية شاملة.'
)


def canonical(node):
    return etree.tostring(node, method='c14n', exclusive=True)


def visible(node):
    node = copy.deepcopy(node)
    for annotation in node.xpath('.//*[local-name()="annotation"]'):
        annotation.getparent().remove(annotation)
    return re.sub(r'\s+', ' ', ''.join(node.itertext())).strip()


def terms(node):
    return node.xpath('.//x:span[contains(concat(" ",normalize-space(@class)," ")," formula ")]',
                      namespaces={'x': X})


def expression(span):
    annotations = span.xpath('.//m:annotation[@encoding="application/x-openlogic-source-tex"]',
                            namespaces={'m': M})
    require(len(annotations) == 1, 'Formula source annotation is ambiguous')
    return annotations[0].text.strip()


def native(span):
    node = copy.deepcopy(span.find('{'+M+'}math'))
    require(node is not None, 'Native MathML is absent')
    for annotation in node.xpath('.//*[local-name()="annotation"]'):
        annotation.getparent().remove(annotation)
    for element in node.iter():
        for key in list(element.attrib):
            if key.startswith('data-'):
                del element.attrib[key]
    return canonical(node)


def paragraphs(root):
    result = []
    for start in ('يسمى الشرط', 'لا توجد قيود'):
        matches = [p for p in root.xpath('.//x:p', namespaces={'x': X})
                   if visible(p).startswith(start)]
        require(len(matches) == 1, 'Correction paragraph is not unique: '+start)
        result.append(matches[0])
    return result


def render(raw, profile):
    for folder in ('full_book', '', 'expansion'):
        path = ROOT / 'build/epub' / folder
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    from section_reader import SectionRenderer
    from arithmetic_math import convert_math
    renderer = SectionRenderer(profile, convert_math)
    renderer.begin_chapter(20)
    renderer.section_number = 2
    result = renderer.render_section('OLP-0087', raw,
        source_path='first-order-logic/natural-deduction/quantifier-rules.tex',
        context_id='modern-reader-3-7-3', initial_tags={}, defined_labels=set())
    require(len(renderer.bare_proof_records) == 4, 'Source proof-tree census differs')
    return etree.fromstring(result['html'].encode())


def corrected_body(raw, before, after, profile):
    original = etree.fromstring(raw)
    previous = render(before, profile)
    current = render(after, profile)
    original_paragraphs = paragraphs(original)
    previous_paragraphs = paragraphs(previous)
    new_paragraphs = paragraphs(current)
    for actual, rendered in zip(original_paragraphs, previous_paragraphs):
        require(visible(actual) == visible(rendered), 'Frozen prose is not the source preimage')
    before_ids = {n.get('id') for n in original.iter() if n.get('id')}
    before_proofs = [canonical(n) for n in original.xpath('.//*[@data-proof-root]')]
    skeleton = copy.deepcopy(original)
    for p in paragraphs(skeleton):
        p.getparent().replace(p, etree.Element('{'+X+'}p'))
    added = 0
    pool = terms(original)
    for old, new in zip(original_paragraphs, new_paragraphs):
        old_formulas = terms(old)
        new_formulas = terms(new)
        cursor = 0
        for candidate in new_formulas:
            if cursor < len(old_formulas) and expression(candidate) == expression(old_formulas[cursor]):
                witness = old_formulas[cursor]
                cursor += 1
                identifier = witness.get('id')
            else:
                require(expression(candidate) == '!A(a)', 'Unadmitted extra formula')
                witnesses = [n for n in pool if expression(n) == '!A(a)' and native(n) == native(candidate)]
                require(witnesses, 'Added assumption formula lacks its existing native witness')
                witness = witnesses[0]
                added += 1
                identifier = 'modern-reader-3-7-3-sol6-added-math-'+str(added)
            require(native(candidate) == native(witness), 'Existing mathematical rendering differs')
            replacement = copy.deepcopy(witness)
            replacement.set('id', identifier)
            replacement.tail = candidate.tail
            candidate.getparent().replace(candidate, replacement)
        require(cursor == len(old_formulas), 'An existing formula was lost')
        new = copy.deepcopy(new)
        new.tail = old.tail
        old.getparent().replace(old, new)
    require(added == 1, 'Expected one explicit discharged-assumption formula')
    new_notes = current.xpath('.//x:aside', namespaces={'x': X})
    require(len(new_notes) == 2, 'New corrective footnote is missing')
    note = copy.deepcopy(new_notes[-1])
    note_id = note.get('id')
    identifier = 'modern-reader-3-7-3-note-2'
    references = original.xpath('.//x:a[@href="#'+note_id+'"]', namespaces={'x': X})
    require(len(references) == 1, 'New footnote reference is ambiguous')
    reference = references[0]
    reference.set('href', '#'+identifier)
    reference.set('id', identifier+'-ref')
    reference.set('role', 'doc-noteref')
    reference.set('data-footnote-source-id', identifier)
    reference.find('{'+X+'}sup').text = '٢' if profile == 'machrek' else '2'
    note.set('id', identifier)
    note.set('role', 'doc-footnote')
    backlinks = note.xpath('.//x:a', namespaces={'x': X})
    require(len(backlinks) == 1, 'Corrective note backlink differs')
    backlinks[0].set('href', '#'+identifier+'-ref')
    containers = original.xpath('.//x:section[@class="footnotes"]', namespaces={'x': X})
    require(len(containers) == 1, 'Original footnote container differs')
    containers[0].append(note)
    after_ids = [n.get('id') for n in original.iter() if n.get('id')]
    require(len(after_ids) == len(set(after_ids)) and before_ids <= set(after_ids),
            'An original ID was lost or an ID was duplicated')
    require(before_proofs == [canonical(n) for n in original.xpath('.//*[@data-proof-root]')],
            'A proof tree changed')
    stripped = copy.deepcopy(original)
    for p in paragraphs(stripped):
        p.getparent().replace(p, etree.Element('{'+X+'}p'))
    notes = stripped.xpath('.//x:aside[@id="'+identifier+'"]', namespaces={'x': X})
    notes[0].getparent().remove(notes[0])
    require(canonical(skeleton) == canonical(stripped), 'Content outside the two paragraphs and new note changed')
    return etree.tostring(original, encoding='utf-8', xml_declaration=True), {
        'corrected_paragraphs': 2, 'corrective_footnotes_added': 1,
        'explicit_assumption_formulas_added': 1, 'all_original_ids_preserved': True,
        'all_four_proof_trees_identical': True, 'outside_correction_subtrees_identical': True}


def run(output, runtime):
    require(not output.exists(), 'Refusing to overwrite an existing successor stage')
    os.environ['OPENLOGIC_ENGLISH_READER_ROOT'] = str(runtime.resolve())
    closure = json.loads((ROOT/authority.DEFAULT_AUTHORITY).read_bytes())
    unit = next(u for u in closure['units'] if u['id'] == 'OLP-0087')
    authority.proof_successor(ROOT, ROOT/authority.PROOF_LEDGER, unit)
    ledger = json.loads((ROOT/authority.PROOF_LEDGER).read_bytes())
    transition = ledger['source_transitions'][0]
    after = (ROOT/authority.PROOF_SOURCE).read_text(encoding='utf-8')
    before = after
    for edit in transition['edits']:
        before = before.replace(edit['after_text'], edit['before_text'], 1)
    output.mkdir(parents=True)
    rows = []
    for profile, expected in EXPECTED.items():
        name = 'OpenLogic-Arabic-Complete-722-'+profile+'.epub'
        old = BASE/name
        require(identity(old)['sha256'] == expected, 'Frozen EPUB identity differs')
        with zipfile.ZipFile(old) as archive:
            members = {n: archive.read(n) for n in archive.namelist()}
        successor = dict(members)
        successor[BODY], checks = corrected_body(members[BODY], before, after, profile)
        opf = etree.fromstring(members['OEBPS/package.opf'])
        declarations = opf.xpath('//*[local-name()="meta"][@property="dcterms:provenance"]')
        require(len(declarations) == 1, 'Provenance declaration differs')
        previous = html.escape(declarations[0].text, quote=False).encode()
        for meta in ('OEBPS/package.opf', 'OEBPS/provenance.xhtml'):
            require(members[meta].count(previous) == 1, 'Provenance is not uniquely bound')
            successor[meta] = members[meta].replace(previous, html.escape(DISCLOSURE, quote=False).encode())
        changed = {n for n in members if members[n] != successor[n]}
        require(changed == {BODY, 'OEBPS/package.opf', 'OEBPS/provenance.xhtml'}, 'Member change scope differs')
        checks.update(validate_xhtml(successor))
        destination = output/name
        pack(successor, destination)
        replay = output/('COLD-REPLAY-'+name)
        pack(successor, replay)
        require(identity(destination)['sha256'] == identity(replay)['sha256'], 'Cold packaging replay differs')
        rows.append({'profile': profile, 'preimage': identity(old), 'successor': identity(destination),
                     'changed_members': sorted(changed), 'unchanged_members': len(members)-3,
                     'checks': checks, 'cold_packaging_byte_identical': True})
    receipt = {'schema': 'openlogic-msa-epub-exact-quantifier-successor-v1',
               'status': 'BODY_SUCCESSORS_PENDING_FRESH_CHECKERS_AND_EXACT_CURRENT_SOURCE_PACKAGE',
               'model': 'GPT-6.1 Sol', 'effort': 'Ultra',
               'source': identity(ROOT/authority.PROOF_SOURCE),
               'choice_ledger': identity(ROOT/authority.PROOF_LEDGER), 'profiles': rows,
               'classical_epub_unchanged': True, 'publication_performed': False}
    (output/'BODY_SUCCESSOR_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status': receipt['status'], 'profiles': len(rows)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--english-runtime', type=Path, required=True)
    args = parser.parse_args()
    run(args.output, args.english_runtime)
