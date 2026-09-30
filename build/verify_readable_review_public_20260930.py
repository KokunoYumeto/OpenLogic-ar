"""One bounded actual-GitHub HTML check of every small Arabic reading page."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import requests
from render_readable_review_20260930 import BASE, ROOT, digest


class Article(HTMLParser):
    def __init__(self):
        super().__init__(); self.depth = 0; self.found = False; self.rows = 0; self.headings = []; self.text = []
    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            self.depth += 1; self.found = True
        if self.depth and tag == 'tr':
            self.rows += 1
    def handle_endtag(self, tag):
        if tag == 'article':
            self.depth -= 1
    def handle_data(self, data):
        if self.depth:
            self.text.append(data)


def main(tag, output):
    receipt_path = BASE / 'READABLE_REVIEW_RECEIPT_20260930.json'
    receipt = json.loads(receipt_path.read_bytes())
    entries = [r['path'] for r in receipt['files']] + ['INDEX_AR.md', 'SOL6_CORRECTIONS_AR.md']
    directory_counts = {r['path']: len(r['decision_ids']) for r in receipt['directory_pages']}
    checked = []
    with requests.Session() as session:
        session.trust_env = False
        for i, name in enumerate(entries, 1):
            local = BASE / name
            url = 'https://github.com/KokunoYumeto/OpenLogic-ar/blob/' + tag + '/' + local.relative_to(ROOT).as_posix()
            with session.get(url, stream=True, timeout=(20, 60)) as response:
                response.raise_for_status()
                parts, count = [], 0
                for block in response.iter_content(1048576):
                    count += len(block); assert count < 8 * 1024 * 1024
                    parts.append(block)
            html = b''.join(parts).decode('utf-8')
            parser = Article(); parser.feed(html)
            assert parser.found and parser.depth == 0, 'No rendered review article: ' + name
            rendered = ''.join(parser.text)
            heading = local.read_text(encoding='utf-8').splitlines()[0].lstrip('# ')
            assert heading in rendered, 'No actual rendered heading: ' + name
            if name in directory_counts:
                assert parser.rows == directory_counts[name] + 1, 'Rendered table rows differ: ' + name
            checked.append({'path': name, 'url': url, 'source_sha256': digest(local),
                            'html_bytes': count, 'rendered_article': True, 'rendered_table_rows': parser.rows})
            if i % 20 == 0:
                print(json.dumps({'rendered_pages_checked': i, 'total': len(entries)}), flush=True)
    value = {'status': 'PASS_ACTUAL_RENDERED_GITHUB_REVIEW_PAGES', 'tag': tag,
             'receipt_sha256': digest(receipt_path), 'pages': checked,
             'all_1095_directory_rows_rendered': True,
             'scope': 'Actual anonymous HTML article and complete table rendering; not semantic or typographic approval.'}
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': value['status'], 'pages': len(checked)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(); main(args.tag, args.output)
