"""Finite source-bound intake of three explicitly defined printed-math carriers.

Does not translate, modify presentation, parse the large occurrence ledger,
expand arbitrary macros, or count TikZ keys as printed mathematics.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'build'))
import materialize_classical_notation as m

CONTRACTS = {'mTrue': 1, 'mFalse': 1, 'TMtrans': 3}
CONFIG_SHA = 'ab19be71b50b415738603290317b504d9fa6b82850fe640d585c62db1540ced3'
NOTATION_SHA = 'c593b7549a5a02c27862ef8701b7d811fe8e17853c2118a7422060de5661c5e2'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def calls(text):
    analysis = m.analyze(text)
    if analysis.errors:
        raise ValueError('Source parser anomalies')
    result = []
    for pos, token in enumerate(analysis.tokens):
        if token.kind != 'command' or token.value[1:] not in CONTRACTS:
            continue
        name = token.value[1:]
        _, arguments, _ = m.argument_sequence(analysis.tokens, pos + 1,
                                              optional=0, required=CONTRACTS[name], allow_star=False)
        if len(arguments) != CONTRACTS[name]:
            raise ValueError('Known printed-math carrier lacks its required arguments')
        result.append({'command': name, 'line': text.count('\n', 0, token.start) + 1,
                       'offset': token.start,
                       'inside_opaque_program': any(a <= token.start < b for a, b in analysis.opaque_spans),
                       'arguments': [''.join(t.value for t in arg).strip() for arg in arguments]})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = (REPO / args.output).resolve()
    if not out.is_relative_to(REPO / 'evidence/classical/repairs') or out.exists():
        raise ValueError('Use a new exact technical-review directory')
    config = REPO / 'source/open-logic-config.sty'
    receipt_path = REPO / 'evidence/classical/NOTATION_MATERIALIZATION_RECEIPT.json'
    if digest(config) != CONFIG_SHA or digest(receipt_path) != NOTATION_SHA:
        raise ValueError('Pinned macro definitions or current presentation receipt changed')
    receipt = json.loads(receipt_path.read_bytes())
    findings, captured, scanned = [], [], 0
    for unit in receipt['units']:
        source, target = [REPO / unit[k]['path'] for k in ('source', 'presentation')]
        raw = source.read_bytes()
        text, _ = m.decode_exact(raw)
        if r'\begin{tikzpicture}' not in text:
            continue
        scanned += 1
        if digest(source) != unit['source']['sha256'].lower() or digest(target) != unit['presentation']['sha256'].lower():
            raise ValueError('Source or presentation no longer matches current receipt')
        rendered, _ = m.decode_exact(target.read_bytes())
        originals, presentations = calls(text), calls(rendered)
        if len(originals) != len(presentations):
            raise ValueError('Carrier call inventory changed between source and presentation')
        for ordinal, (original, presentation) in enumerate(zip(originals, presentations), 1):
            if original['command'] != presentation['command']:
                raise ValueError('Carrier call order changed')
            for argument, (before, after) in enumerate(zip(original['arguments'], presentation['arguments']), 1):
                # Deliberately finite: only plainly written scalar/name/script
                # tokens, no inference through command names or styled macros.
                if before != after or not re.fullmatch(r'[A-Za-z0-9_]+', before) or not re.search(r'[A-Za-z0-9]', before):
                    continue
                direction_constant = original['command'] == 'TMtrans' and argument == 3 and before in ('R', 'L', 'N')
                findings.append({'id': f"{unit['id']}-IMPLICIT-{ordinal:03d}-{argument}",
                    'unit': unit['id'], 'source_path': unit['source']['path'],
                    'presentation_path': unit['presentation']['path'],
                    'source_line': original['line'], 'presentation_line': presentation['line'],
                    'source_offset': original['offset'], 'command': original['command'],
                    'argument': argument, 'source_argument': before, 'presentation_argument': after,
                    'inside_opaque_program': original['inside_opaque_program'],
                    'finding': ('Direction constant needs an explicit notation/exemption decision' if direction_constant else
                                'Plain printed math argument remains unlocalized'),
                    'reason': ('This is a defined machine-direction constant, not an arbitrary variable. Do not automatically rename it as a letter; record its intended notation policy.' if direction_constant else
                               'The pinned source macro places this argument inside ensuremath; the argument is visible math, not a diagram key.'),
                    'status': ('OPEN_SYMBOL_POLICY_REVIEW_NOT_AUTOMATIC_LETTER_MISS' if direction_constant else
                               'CONFIRMED_SOURCE_LEVEL_GAP_NOT_YET_CORRECTED'),
                    'open_to_correction': True})
        captured.append({'unit': unit['id'], 'source': unit['source'], 'presentation': unit['presentation']})
    out.mkdir(parents=True)
    result = {'status': 'COMPLETED_BOUNDED_INTAKE_WITH_CONFIRMED_GAPS',
        'scope': 'Three known ensuremath carriers in the 37 canonical units containing literal tikzpicture. Includes prose-side calls in those same units; not an exhaustive macro or diagram audit.',
        'config': {'path': 'source/open-logic-config.sty', 'sha256': CONFIG_SHA,
                   'definitions': {'mTrue': 859, 'mFalse': 860, 'TMtrans': 1041}},
        'notation_receipt_sha256': NOTATION_SHA, 'auditor_sha256': digest(Path(__file__)),
        'units_scanned': scanned, 'plain_argument_records': len(findings),
        'confirmed_conversion_gaps': sum(r['status'].startswith('CONFIRMED') for r in findings),
        'direction_symbol_policy_reviews': sum(r['status'].startswith('OPEN_SYMBOL') for r in findings),
        'by_command': dict(Counter(r['command'] for r in findings)),
        'captured_units': captured, 'findings': findings,
        'production_sources_changed': False, 'tex_launched': False, 'large_ledger_parsed': False}
    if scanned != 37:
        raise ValueError('Current finite TikZ source inventory differs')
    (out / 'IMPLICIT_MATH_FINDINGS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# Printed mathematics missed inside notation macros', '',
             'This source-level intake identifies unchanged literal math arguments in three explicitly defined macros. '
             'It does not report TikZ node names, coordinates or direction-command bodies as missing translations. '
             'No correction has yet been applied; findings remain open to correction.', '',
             f"Scoped units: {scanned}. Confirmed conversion gaps: {result['confirmed_conversion_gaps']}. "
             f"Separate direction-symbol policy reviews: {result['direction_symbol_policy_reviews']}. "
             'A multi-argument call can occupy several rows; direction constants are not automatic letter-conversion errors.', '',
             '| Decision ID | Source file and line | Printed macro argument | Why check it |',
             '| --- | --- | --- | --- |']
    for row in findings:
        rel = row['source_path'].removeprefix('source/locale/ar-classical/content/')
        lines.append(f"| {row['id']} | `{rel}:{row['source_line']}` | `\\{row['command']}` argument {row['argument']}: `{row['source_argument']}` | {row['reason']} |")
    lines += ['', 'Primary definitions: `source/open-logic-config.sty`, lines 859–860 and 1041; '
              'exact file and presentation identities are recorded in the JSON companion. These are notation findings, '
              'not additional Arabic lexical decisions or a complete-book acceptance claim.', '']
    (out / 'IMPLICIT_MATH_FINDINGS.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'units_scanned': scanned,
                      'confirmed_conversion_gaps': result['confirmed_conversion_gaps'],
                      'direction_symbol_policy_reviews': result['direction_symbol_policy_reviews'],
                      'by_command': result['by_command']}))


if __name__ == '__main__':
    main()
