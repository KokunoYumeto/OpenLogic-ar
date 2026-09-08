"""Render the exact live graph example after reversible notation conversion."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import re

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'build'))
import materialize_classical_notation as m


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{7,79}', args.run_id):
        raise ValueError('Invalid specimen run ID')
    candidate = None
    if args.candidate is not None:
        candidate = (REPO / args.candidate).resolve()
        if not candidate.is_relative_to(REPO / 'tmp/pdfs') or not candidate.is_file():
            raise ValueError('Candidate must be an existing isolated PDF-fixture input')
    out = REPO / 'tmp/pdfs' / ('classical-math-token-fields-' + args.run_id)
    if out.exists():
        raise FileExistsError('Inspect the existing graph specimen instead of overwriting it')
    source_path = REPO / 'source/locale/ar-classical/content/sets-functions-relations/relations/graphs.tex'
    source, bom = m.decode_exact(source_path.read_bytes())
    policy = json.loads((REPO / m.DEFAULT_POLICY).read_bytes())
    greek = {r['key'] for r in json.loads((REPO / m.DEFAULT_LETTERS).read_bytes())['entries']
             if r['family'] == 'greek-variable'}
    _, replacements, summary = m.classify_unit('OLP-0001', source, bom, policy, greek)
    target, spans = m.apply_replacements(source, replacements)
    if m.encode_exact(m.inverse_reconstruct(target, replacements, spans), bom) != source_path.read_bytes() or summary['untreated_candidates']:
        raise ValueError('Live graph source failed inverse/coverage checks')
    start, end = r'\begin{align*}', r'\end{align*}'
    def excerpt(text):
        if text.count(start) != 1 or text.count(end) != 1:
            raise ValueError('Graph example is not the expected single align block')
        return start + text.split(start, 1)[1].split(end, 1)[0] + end
    original = (REPO / 'tmp/pdfs/classical-rtl-math-probe/common.tex').read_text(encoding='utf-8')
    preamble = original.split(r'\begin{document}', 1)[0]
    preamble += '\n' + r'\input{../ar-classical/open-logic-numerals-ar-classical.tex}' + '\n'
    preamble += r'\input{../ar-classical/open-logic-letters-ar-classical.tex}' + '\n'
    out.mkdir()
    for name, install, block in [('control', '', excerpt(source)),
                                 ('rtl', r'\def\OLCProbeInstallRTL{1}' + '\n', excerpt(target))]:
        body = r'\begin{document}\selectlanguage{arabic}' + '\n' + block + '\n'
        body += r'\typeout{OLC-FIELD-G01=two-live-graphs-complete}\end{document}' + '\n'
        addition = ''
        if name == 'rtl' and candidate is not None:
            addition = r'\input{../../../' + candidate.relative_to(REPO).as_posix() + '}' + '\n'
        (out / (name + '.tex')).write_text(install + preamble + addition + body, encoding='utf-8', newline='\n')
    inputs = [Path(__file__), source_path, REPO / 'build/materialize_classical_notation.py',
              REPO / m.DEFAULT_POLICY, REPO / m.DEFAULT_LETTERS,
              REPO / 'tmp/pdfs/classical-rtl-math-probe/common.tex',
              REPO / 'source/locale/ar-classical/open-logic-numerals-ar-classical.tex',
              REPO / 'source/locale/ar-classical/open-logic-letters-ar-classical.tex',
              REPO / 'source/locale/ar-classical/open-logic-rtl-math.tex']
    if candidate is not None:
        inputs.append(candidate)
    identities = [{'path': p.relative_to(REPO).as_posix(), 'bytes': p.stat().st_size,
                   'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs]
    (out / 'SOURCE_SPECIMEN.json').write_text(json.dumps({'scope': 'Exact two live graph diagrams; not full reader QA',
        'inputs': identities, 'cases': [{'id': 'G01', 'source': excerpt(source), 'presentation': excerpt(target),
                                       'inverse': 'PASS_FULL_CANONICAL_GRAPH_UNIT'}]}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'PREPARED_EXACT_GRAPH_SPECIMEN', 'output': str(out)}))


if __name__ == '__main__':
    main()
