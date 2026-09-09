"""Small source-addressed specimen, not a reader or complete notation audit."""
from pathlib import Path
import argparse
import json
import sys
import hashlib
import re

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'build'))
import materialize_classical_notation as m

CASES = [
    ('S01', r'a_1'), ('S02', r'a_n'), ('S03', r'x^2'), ('S04', r'x^\Gamma'),
    ('S05', r'x_12'), ('S06', r'x^23'), ('S07', r'x_{12}'), ('S08', r'a_{n_1}'),
    ('A01', r'\vec x'), ('A02', r'\bar n'), ('A03', r'\hat\alpha'),
    ('R01', r'\sqrt2'), ('R02', r'\sqrt12'), ('R03', r'\sqrt[12]34'),
    ('R04', r'\root12\of34'),
    ('F01', r'\frac12'), ('F02', r'\frac1{2}'), ('F03', r'\frac{1}2'),
    ('F04', r'\frac x2'), ('F05', r'\frac{12}{34}'), ('F06', r'\frac1234'),
    ('F07', r'\dfrac12'), ('F08', r'\tfrac12'), ('F09', r'\binom12'),
    ('F10', r'\cfrac[l]12'), ('N01', r'12+34'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{7,79}', args.run_id):
        raise ValueError('Invalid bounded specimen run ID')
    out = REPO / 'tmp/pdfs' / ('classical-math-token-fields-' + args.run_id)
    if out.exists():
        raise FileExistsError('Specimen output already exists; inspect it instead of overwriting')
    out.mkdir()
    policy = json.loads((REPO / m.DEFAULT_POLICY).read_bytes())
    greek = {r['key'] for r in json.loads((REPO / m.DEFAULT_LETTERS).read_bytes())['entries'] if r['family'] == 'greek-variable'}
    original = (REPO / 'tmp/pdfs/classical-rtl-math-probe/common.tex').read_text(encoding='utf-8')
    preamble = original.split(r'\begin{document}', 1)[0]
    preamble += '\n' + r'\input{../ar-classical/open-logic-numerals-ar-classical.tex}' + '\n'
    preamble += r'\input{../ar-classical/open-logic-letters-ar-classical.tex}' + '\n'
    rows, receipt = [], []
    for identifier, formula in CASES:
        source = '$' + formula + '$'
        occurrences, replacements, summary = m.classify_unit('OLP-0001', source, False, policy, greek)
        rendered, spans = m.apply_replacements(source, replacements)
        if m.inverse_reconstruct(rendered, replacements, spans) != source or summary['untreated_candidates']:
            raise ValueError('Specimen inverse/classification mismatch')
        # Display the real source tokens on the left and the generated formula
        # on the right; no hand-edited copy of a generated formula is used.
        rows += [rf'\ProbeID{{{identifier}}} \babelsublr{{\texttt{{\detokenize{{{formula}}}}}}}\par',
                 r'\begingroup\setbox0=\hbox{' + rendered + r'}' + '\n' +
                 rf'\typeout{{OLC-FIELD-{identifier}=wd:\the\wd0;ht:\the\ht0;dp:\the\dp0}}' + '\n' +
                 r'\noindent\box0\par\endgroup', r'\medskip']
        receipt.append({'id': identifier, 'source': source, 'presentation': rendered,
                        'inverse': 'PASS', 'replacements': len(replacements)})
    body = r'\begin{document}\selectlanguage{arabic}' + '\n' + '\n'.join(rows) + '\n' + r'\end{document}' + '\n'
    for name, install in (('control', ''), ('rtl', r'\def\OLCProbeInstallRTL{1}' + '\n')):
        (out / (name + '.tex')).write_text(install + preamble + body, encoding='utf-8', newline='\n')
    inputs = [Path(__file__), REPO / 'build/materialize_classical_notation.py',
              REPO / m.DEFAULT_POLICY, REPO / m.DEFAULT_LETTERS,
              REPO / 'tmp/pdfs/classical-rtl-math-probe/common.tex',
              REPO / 'source/locale/ar-classical/open-logic-numerals-ar-classical.tex',
              REPO / 'source/locale/ar-classical/open-logic-letters-ar-classical.tex',
              REPO / 'source/locale/ar-classical/open-logic-rtl-math.tex']
    identities = [{'path': p.relative_to(REPO).as_posix(), 'bytes': p.stat().st_size,
                   'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs]
    (out / 'SOURCE_SPECIMEN.json').write_text(json.dumps({'scope':'26 source-token-boundary/font-style cases, not full-reader QA',
        'inputs': identities, 'cases': receipt}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'PREPARED_EXACT_INVERSE_SPECIMEN', 'cases': len(CASES), 'output': str(out)}))


if __name__ == '__main__':
    main()
