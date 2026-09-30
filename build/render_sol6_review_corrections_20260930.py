"""Render source-checked corrections, retaining old cards as witnesses."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'expert-review/2026-09-26-final-page-review'
CORRECTIONS = ROOT / 'evidence/classical/terminology/SOL6_REEXAMINATION_CORRECTIONS_20260930.json'
ENGLISH = Path('C:/interlanguage-production/openlogic-interfarsi/repo/source/upstream')
if (BASE / 'reexamination-source/english').is_dir():
    ENGLISH = BASE / 'reexamination-source/english'


def render() -> None:
    data = json.loads(CORRECTIONS.read_bytes())
    assert data['model'] == 'GPT-6.1 Sol' and data['effort'] == 'Ultra'
    output = ['# تصحيح شروح قابلية المحورة والتجاوز والمختزلات — ٣٠ سبتمبر ٢٠٢٦\n',
              '[مدخل المراجعة](INDEX_AR.md) · [الدليل الكامل](DIRECTORY_AR.md)\n', data['scope_ar'] + '\n',
              'أُنجزت إعادة المقابلة وتصحيح الشرح بواسطة OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra. '
              'البطاقات السابقة محفوظة للشهادة على تاريخ التصحيح، وليست تعليلاتها القديمة مرجع النسخة الحالية. '
              'لم تقع مراجعة بشرية شاملة.\n']
    for row in data['records']:
        prior_card = row.get('previous_card', 'arabic-decisions-545-574/CARDS-7.md')
        old = (BASE / prior_card).read_text(encoding='utf-8')
        headings = old.split('\n## ')[1:]
        section = next(s for s in headings if '`' + row['decision_id'] + '`' in s)
        marker = '**كل وقوع مسجل لهذا القرار:**'
        assert section.count(marker) == 1
        occurrences = (marker + section.split(marker, 1)[1]).replace('— النظريات Axiomatizable', '— النظريات القابلة للمحورة').replace('— reducts and expansions', '— المختزلات والتوسيعات')
        output.extend(['## ' + section.splitlines()[0], '\nمعرّف القرار: `' + row['decision_id'] + '`.\n',
                       '**المعنى المصحح:** ' + row['sense_ar'] + '\n',
                       '**سبب التصحيح والاختيار المؤقت:** ' + row['rationale_ar'] + '\n',
                       '**سؤال مفتوح للمختص:** ' + row['expert_question_ar'] + '\n',
                       '**حدود الشاهد الاصطلاحي:** ' + row['canon_limit_ar'] + '\n',
                       '**البدائل:** ' + '؛ '.join(row['alternatives_ar']) + '\n',
                       '**تقدير الثقة (ليس احتمالًا إحصائيًا):** ' + row['confidence_ar'] + '\n',
                       '**المواضع المقروءة في هذه المقابلة:**\n'])
        for kind, root, repository, commit in (
            ('source_bindings', ENGLISH, 'OpenLogicProject/OpenLogic', data['english_source_commit']),
            ('target_bindings', ROOT, 'KokunoYumeto/OpenLogic-ar', '86a4a7c11c0a0289ade28cb8f96acbacf9c01844')):
            for b in row[kind]:
                source_path = root / b['logical_path']
                if kind == 'target_bindings' and not source_path.exists():
                    source_path = BASE / 'reexamination-source/repo' / b['logical_path']
                raw = source_path.read_bytes()
                assert (len(raw), hashlib.sha256(raw).hexdigest()) == (b['bytes'], b['sha256'])
                lines = raw.decode('utf-8').splitlines()
                passage = '\n'.join(lines[b['line_start']-1:b['line_end']])
                assert passage and (not b.get('exact_passage') or b['exact_passage'] == passage)
                url = f"https://github.com/{repository}/blob/{commit}/{b['logical_path']}#L{b['line_start']}-L{b['line_end']}"
                label = 'الأصل الإنجليزي' if kind == 'source_bindings' else 'الترجمة العربية'
                if kind == 'source_bindings':
                    public_raw = raw.replace(b'\r\n', b'\n')
                    public_sha = hashlib.sha256(public_raw).hexdigest()
                    output.append(f"- {label}: [الأسطر {b['line_start']}–{b['line_end']}]({url})؛ SHA-256 لنسخة GitHub ذات نهايات LF: `{public_sha}`؛ ولنسخة المقابلة المحلية ذات نهايات CRLF: `{b['sha256']}`. النص والأسطر متطابقان بعد توحيد نهايات الأسطر.\n")
                else:
                    output.append(f"- {label}: [الأسطر {b['line_start']}–{b['line_end']}]({url})؛ SHA-256: `{b['sha256']}`.\n")
        history = f'\n**تاريخ التصحيح:** [البطاقة السابقة]({prior_card}) تحوي الشرح المستبدل. '
        if row['decision_id']=='TERM-AXIOMATIZABLE':
            history += 'إحالة السطر ٣ في OLP-0306 كانت إلى تعليق اسم القسم لا إلى التعريف؛ إحالة التعريف أعلاه هي ١٣–١٨. '
        output.extend([history+'\n', occurrences])
    (BASE / data['review_card']).write_text('\n'.join(output), encoding='utf-8', newline='\n')


if __name__ == '__main__':
    render()
