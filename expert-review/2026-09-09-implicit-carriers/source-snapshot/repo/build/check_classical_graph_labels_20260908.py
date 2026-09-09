"""Check label containment and the two live graph layouts, not general TikZ QA."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import pdfplumber


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def check_pdf(path, alphabet):
    with pdfplumber.open(path) as pdf:
        if len(pdf.pages) != 1:
            raise ValueError('Expected one-page two-graph specimen')
        page = pdf.pages[0]
        circles = [c for c in page.curves if 20 < c['width'] < 35 and
                   abs(c['height'] - c['width']) < .1]
        if len(circles) != 7:
            raise ValueError(f'Expected exactly 7 node circles, got {len(circles)}')
        nodes = []
        for circle in circles:
            labels = [c for c in page.chars if c['text'] in alphabet and
                      circle['x0'] < c['x0'] < c['x1'] < circle['x1'] and
                      circle['top'] < c['top'] < c['bottom'] < circle['bottom']]
            if len(labels) != 1:
                raise ValueError(f"Node circle at ({circle['x0']:.2f}, {circle['top']:.2f}) contains {len(labels)} labels")
            nodes.append({'label': alphabet.index(labels[0]['text']) + 1,
                          'x': (circle['x0'] + circle['x1']) / 2,
                          'y': (circle['top'] + circle['bottom']) / 2})
        if Counter(n['label'] for n in nodes) != Counter({1: 2, 2: 2, 3: 2, 4: 1}):
            raise ValueError('Graph node label inventory differs')
        # Source graph one has 4 nodes and graph two 3 nodes, with fixed 2cm
        # center spacing. Glyph changes may alter radii, not this geometry.
        nodes.sort(key=lambda n: n['y'])
        graphs = [nodes[:4], nodes[4:]]
        for index, graph in enumerate(graphs):
            by_label = {n['label']: n for n in graph}
            expected = {1, 2, 3, 4} if index == 0 else {1, 2, 3}
            if set(by_label) != expected:
                raise ValueError('Node assigned to wrong graph')
            one, two, three = [by_label[k] for k in [1, 2, 3]]
            if not (abs(two['x'] - one['x'] - 56.692913) < .1 and
                    abs(two['y'] - one['y']) < .1 and
                    abs(three['x'] - two['x']) < .1 and
                    abs(three['y'] - two['y'] - 56.692913) < .1):
                raise ValueError('Directed graph node layout differs from source')
            if index == 0:
                four = by_label[4]
                if not (abs(four['x'] - two['x'] - 56.692913) < .1 and
                        abs(four['y'] - two['y']) < .1):
                    raise ValueError('Isolated node 4 moved relative to source')
    return {'file': path.name, 'bytes': path.stat().st_size,
            'sha256': digest(path), 'contained_labels': 7, 'source_layouts_checked': 2,
            'nodes': nodes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', required=True, type=Path)
    args = parser.parse_args()
    result = {'status': 'PASS_SCOPED_GRAPH_LABELS_AND_LAYOUT', 'pdfs': [],
              'checker_sha256': digest(Path(__file__)),
              'scope': 'Seven circles in the two exact source graph examples; not full-reader or general diagram acceptance.'}
    try:
        for name, alphabet in [('control', '1234'), ('rtl', '١٢٣٤')]:
            result['pdfs'].append(check_pdf(args.directory / (name + '.pdf'), alphabet))
    except ValueError as error:
        result.update(status='FAIL', failure=str(error))
    with (args.directory / 'GRAPH_LABEL_GEOMETRY.json').open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    return 0 if result['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
