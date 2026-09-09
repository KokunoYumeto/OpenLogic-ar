"""Read-only geometry checks for the small typed-math diagnostic specimen.

This does not certify radical glyph orientation, full-reader layout, or all
formula semantics. It binds concrete script/font/fraction/digit-order checks
to the generated specimen and the actual PDF bytes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

import pdfplumber


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def character(rows, identifier, text):
    matches = [c for c in rows[identifier] if c['text'] == text]
    if len(matches) != 1:
        raise ValueError(f'{identifier}: expected one {text}, found {len(matches)}')
    return matches[0]


def measure(path, ids):
    anchors, chars = [], []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            anchors.extend((w['doctop'], w['text']) for w in page.extract_words()
                           if re.fullmatch(r'[SAFRN]\d\d', w['text']))
            # Only output glyphs, excluding the ASCII source captions/footer.
            chars.extend(c for c in page.chars if c['text'] and
                         (0x660 <= ord(c['text'][0]) <= 0x669 or
                          0x1EE00 <= ord(c['text'][0]) <= 0x1EEFF))
    anchors.sort()
    if [identifier for _, identifier in anchors] != ids:
        raise ValueError('Missing, reordered, duplicate or unexpected case captions')
    rows = {identifier: [c for c in chars if top < c['doctop'] < next_top]
            for (top, identifier), (next_top, _) in
            zip(anchors, anchors[1:] + [(float('inf'), '')])}
    facts = []
    def require(condition, name):
        if not condition:
            raise ValueError(path.name + ': ' + name)
        facts.append(name)
    for identifier, base, sub in [('S01', '𞸀', '١'), ('S02', '𞸀', '𞸍')]:
        a, b = character(rows, identifier, base), character(rows, identifier, sub)
        require(a['size'] > b['size'] + 2, identifier + '-script-font-smaller')
        require(b['doctop'] > a['doctop'] + 1, identifier + '-subscript-lowered')
    for identifier, power, outside in [('S05', '١', '٢'), ('S06', '٢', '٣')]:
        a = character(rows, identifier, '𞸗')
        b, c = character(rows, identifier, power), character(rows, identifier, outside)
        require(a['size'] > b['size'] + 2 and abs(a['size'] - c['size']) < .02,
                identifier + '-only-one-token-in-script')
        require(abs(a['doctop'] - c['doctop']) < .02,
                identifier + '-following-digit-at-baseline')
    a, b, c = [character(rows, 'S07', t) for t in ['𞸗', '١', '٢']]
    require(a['size'] > b['size'] + 2 and abs(b['size'] - c['size']) < .02
            and abs(b['doctop'] - c['doctop']) < .02, 'S07-entire-group-in-script')
    a, b, c = [character(rows, 'S08', t) for t in ['𞸀', '𞸍', '١']]
    require(a['size'] > b['size'] + 2 and b['size'] > c['size'] + 2,
            'S08-base-script-scriptscript-sizes-descend')
    for identifier in ['F01', 'F02', 'F03', 'F07', 'F08', 'F09', 'F10']:
        a, b = [character(rows, identifier, t) for t in ['١', '٢']]
        require(a['doctop'] < b['doctop'], identifier + '-numerator-above-denominator')
    for identifier in ['S07', 'R03', 'R04', 'F05', 'N01']:
        a, b = [character(rows, identifier, t) for t in ['١', '٢']]
        require(a['x0'] < b['x0'], identifier + '-12-keeps-digit-order')
    for identifier in ['F05', 'F06', 'N01']:
        a, b = [character(rows, identifier, t) for t in ['٣', '٤']]
        require(a['x0'] < b['x0'], identifier + '-34-keeps-digit-order')
    sizes = {t: round(character(rows, 'S08', t)['size'], 6) for t in ['𞸀', '𞸍', '١']}
    return {'file': path.name, 'bytes': path.stat().st_size, 'sha256': digest(path),
            'checks': facts, 'observed_S08_sizes_pdf_points': sizes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    args = parser.parse_args()
    spec_path = args.directory / 'SOURCE_SPECIMEN.json'
    spec = json.loads(spec_path.read_bytes())
    ids = [r['id'] for r in spec['cases']]
    if len(ids) != 26 or len(set(ids)) != 26:
        raise ValueError('Expected exact 26-case source fixture')
    guard_path = args.directory / 'TEX_MUTEX_RECEIPT.json'
    guard = json.loads(guard_path.read_bytes())
    if not (guard['Status'] == 'PASS' and guard['Acquired'] and
            guard['ExitCode'] == 0 and guard['Tree']['DrainVerified'] and
            guard['Tree']['FinalActiveProcesses'] == 0):
        raise ValueError('Specimen TeX transaction not terminal and drained')
    result = {'status': 'PASS_SCOPED_SCRIPT_FONT_FRACTION_DIGIT_CHECKS',
              'source_specimen_sha256': digest(spec_path),
              'guard_sha256': digest(guard_path), 'checker_sha256': digest(Path(__file__)),
              'limits': 'Not radical-face, whole-formula, full-reader or visual-layout acceptance.',
              'pdfs': [measure(args.directory / (n + '.pdf'), ids) for n in ['control', 'rtl']]}
    target = args.directory / 'TYPED_FIELD_GEOMETRY.json'
    with target.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
