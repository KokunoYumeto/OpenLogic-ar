"""Replace a finite set of 59 comment-only pointers with read source passages.

Ranges below are explicit editorial selections, not keyword-ranked candidates.
This pass repairs references; it does not certify every lexical/canon choice.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import requests
import assemble_complete_arabic_review as assembly

ROOT=assembly.ROOT
BASE=assembly.BASE
TERM=assembly.TERM
ENGLISH=Path('C:/interlanguage-production/openlogic-interfarsi/repo/source/upstream')
SNAPSHOT=BASE/'reexamination-source'
if (SNAPSHOT/'english').is_dir():
    ENGLISH=SNAPSHOT/'english'
FINDINGS=Path('C:/interlanguage-task-state/openlogic-arabic-owner/sol6-rework-20260930/ADDED_SOURCE_WITNESS_FINDINGS.json')
PUBLIC_FINDINGS=TERM/'SOL6_COMMENT_ONLY_WITNESS_CENSUS_20260930.json'
MANIFEST=TERM/'SOL6_SOURCE_WITNESS_CORRECTIONS_20260930.json'
RECEIPT=BASE/'SOURCE_WITNESS_PUBLIC_READBACK_20260930.json'
CARD='SOL6_SOURCE_REFERENCES_AR.md'
COMMIT='9620cc73f9c8e0ad003c514a5d3748f29611c4c0'


def passage(path,start,end,relevance):
    return (path,start,end,relevance)


SELECTIONS={
 'compact:T-ARITHMETIZATION-SYNTAX':[
  passage('incompleteness/arithmetization-syntax/introduction.tex',12,28,'يبين الأصل تمثيل الأشياء النحوية وعملياتها وعلاقاتها بأعداد ودوال وعلاقات حسابية، لا مجرد تشغيل خوارزمية.')],
 'compact:T-ARITY-RANK-INDEX':[
  passage('incompleteness/representability-in-q/composition-representable.tex',71,78,'عدد المواضع هنا عدد حجج الدالة.'),
  passage('proof-theory/proof-search/search-algorithm.tex',30,38,'الفهرس هنا عدد يميز صيغة في خطة البحث.'),
  passage('model-theory/basics/partial-iso.tex',113,119,'رتبة الكم هنا أقصى عدد من الكمّيات المتداخلة في الصيغة.')],
 'ar-classical-0451-0500-axiomatic-derivation':[
  passage('intuitionistic-logic/introduction/axiomatic-derivations.tex',17,28,'يفصل تعريف الاشتقاق بين الفرض والمسلمة والنتيجة المتولدة بقاعدة الاستدلال.')],
 'TERM-AXIOMATIZABLE':[
  passage('incompleteness/theories-computability/computably-axiomatizable.tex',13,18,'قابلية حساب مجموعة البديهيات شرط في هذا التعريف؛ ليست قيدًا اختياريًا.')],
 'repair-0401-0500:TERM-BISIMULATION':[
  passage('applied-modal-logic/epistemic-logic/bisimulations.tex',29,47,'يتضمن التعريف اتفاق المتغيرات القضوية وشرطي الانتقال في الاتجاهين.')],
 'ar-classical-0451-0500-completeness':[
  passage('normal-modal-logic/tableaux/completeness.tex',14,27,'يشرح الأصل بناء نموذج مضاد عندما لا يوجد جدول مغلق، وهي جهة التمام البرهاني.')],
 'compact:T-CURRY-HOWARD--variant-afa5c16d':[
  passage('proof-theory/propositions-as-types/proof-terms.tex',13,33,'يسجل الحد في التتابعية كيفية البرهان؛ وتحدد قواعد الإدخال والحذف بناء حدود البرهان. هذا شاهد لهذا الجزء من المقابلة، لا مبرهنة كاملة وحده.')],
 'ar-classical-0451-0500-decidability':[
  passage('normal-modal-logic/filtrations/S5-decidable.tex',12,15,'يعرّف الموضع إجراء حسابيًا يقرر قابلية اشتقاق الصيغة أو عدمها.'),
  passage('normal-modal-logic/filtrations/S5-decidable.tex',22,31,'يبرهن توقف أحد البحثين المتوازيين: عن برهان أو عن نموذج منته مضاد.')],
 'ar-classical-0451-0500-euclidean':[
  passage('normal-modal-logic/frame-definability/properties-accessibility.tex',46,48,'يظهر شرط العلاقة صراحة: إذا كان Rwu وRwv كان Ruv؛ لا يتعلق بمسافة هندسية.')],
 'compact:T-PROOF-SEARCH-FAIRNESS':[
  passage('proof-theory/proof-search/search-algorithm.tex',20,24,'شرط الإنصاف في هذه الخطة يضمن معالجة كل صيغة بما يلزم من تطبيقات القواعد.')],
 'repair-0401-0500:TERM-FILTRATION':[
  passage('normal-modal-logic/filtrations/filtrations-def.tex',23,43,'يعين التعريف العوالم بوصفها فئات تكافؤ وشروط العلاقة والتقييم، مع إغلاق مجموعة الصيغ تحت الصيغ الجزئية.'),
  passage('normal-modal-logic/filtrations/filtrations-def.tex',55,59,'تنص المبرهنة على حفظ صدق الصيغ المختارة. لا يفترض التعريف العام وحده تناهي مجموعة الصيغ؛ يلزم هذا الفرض لاستنتاج نموذج منته.')],
 'ar-classical-0351-0400-fixed-point':[
  passage('lambda-calculus/lambda-definability/fixpoints.tex',48,59,'النقطة الثابتة في المثال اللامبدي تحقق المساواة بيتا، لا الهوية الكتابية بين الحدين.')],
 'compact:T-FRAKTUR':[
  passage('reference/fraktur-alphabet/fraktur-alphabet.tex',12,19,'يعرض الجدول مقابلات الحروف اللاتينية بحروف فراكتور. هذا شاهد لهيئة الحروف لا لتاريخ الخط أو ترجيح اسمه العربي.')],
 'TERM-ISOMORPHISM':[
  passage('sets-functions-relations/functions/isomorphic-functions.tex',26,33,'يتطلب التشاكل تقابلًا يحفظ العلاقة في الاتجاهين، لا مجرد دالة بين مجموعتين.')],
 'compact:T-MANY-SORTED':[
  passage('first-order-logic/beyond/many-sorted-logic.tex',13,26,'يحدد الأصل الأصناف ومتغيراتها وكمياتها والقيود على حجج الدوال والعلاقات.')],
 'locale-ar-chosen-5b8203c39e8d9ae8':[
  passage('first-order-logic/beyond/many-sorted-logic.tex',19,26,'يفصل النص بين الصنف وبين المجال الذي تنتمي إليه الأشياء، ويقيد أنواع حجج الرموز.')],
 'TERM-MATERIAL-STRICT-CONDITIONAL':[
  passage('counterfactuals/introduction/material-conditional.tex',21,27,'هذا شرط الصدق للشرط المادي.'),
  passage('counterfactuals/introduction/strict-conditional.tex',13,17,'يعرف الأصل الشرط الصارم بضرورة الشرط المادي، لا بجدول صدق الشرط المادي وحده.')],
 'compact:T-MAXIMALLY-CONSISTENT':[
  passage('first-order-logic/completeness/maximally-consistent-sets.tex',16,34,'تعني القصوى أن إضافة جملة جديدة تجعل المجموعة غير متسقة؛ ليست درجة عددية للاتساق.')],
 'ar-classical-0451-0500-modal':[
  passage('normal-modal-logic/syntax-and-semantics/introduction.tex',13,25,'يبين الأصل جهتي الضرورة والإمكان وأن الجهات الأخرى لا تقتصر عليهما.'),
  passage('normal-modal-logic/syntax-and-semantics/truth-at-w.tex',37,42,'يربط تعريف الصدق الضرورة بكل العوالم المتاحة والإمكان بوجود عالم متاح مناسب.')],
 'compact:T-NORMAL-MODAL-NECESSITATION':[
  passage('normal-modal-logic/syntax-and-semantics/normal-modal-logics.tex',39,50,'تطبق قاعدة الضرورة على صيغة في المنطق نفسه، أي مبرهنة فيه، لا على فرض محلي كيفما اتفق.')],
 'compact:T-OVERSPILL':[
  passage('model-theory/basics/overspill.tex',12,25,'هذه مبرهنة الانتقال من نماذج منتهية غير محدودة الكبر إلى وجود نموذج لا نهائي، ببرهان التراص.')],
 'compact:T-SEQUENT-MANY-VALUED':[
  passage('many-valued-logic/sequent-calculus/proof-theoretic-notions.tex',14,20,'تميز الفقرة المفاهيم البرهانية المعرفة بواسطة التتابعيات من المفاهيم الدلالية.'),
  passage('many-valued-logic/sequent-calculus/proof-theoretic-notions.tex',29,35,'يعرف الموضع قابلية الاشتقاق بواسطة تتابعية مشتقة من مجموعة جزئية منتهية.')],
 'compact:T-REDEX-REDUCT-CONFLUENCE':[
  passage('proof-theory/propositions-as-types/reduction.tex',55,63,'يميز الأصل الحد القابل للاختزال من ناتج اختزاله في حساب لامبدا المنمط.'),
  passage('lambda-calculus/introduction/church-rosser.tex',12,16,'تنص خاصية تشيرش–روسر على وجود حد مشترك يصل إليه فرعا الاختزال.')],
 'compact:T-REDUCT-EXPANSION':[
  passage('model-theory/basics/reducts-and-expansions.tex',24,39,'المختزَل والتوسيع هنا بنيتان للغتين مختلفتين، لهما المجال نفسه وتأويل الرموز المشتركة نفسه.')],
 'locale-ar-chosen-62c0c8a085b90bd0':[
  passage('model-theory/basics/reducts-and-expansions.tex',24,39,'يتعلق الرأس بتقييد لغة بنية أو توسيعها، لا بسهم اختزال حد لامبدي.')],
 'TERM-SEQUENT':[
  passage('proof-theory/sequent-calculus/rules-proofs.tex',15,36,'توضح الصيغ والمقدمات والنتيجة والسياق وظيفة التتابعية في حساب الاستدلال.')],
 'compact:T-SEQUENT-VS-SEQUENCE':[
  passage('computability/recursive-functions/sequences.tex',12,25,'هذه متتاليات من أعداد طبيعية مرمزة بأعداد؛ ليست أحكام استدلال.'),
  passage('proof-theory/sequent-calculus/rules-proofs.tex',15,36,'هذه تتابعيات بوصفها أحكامًا في قواعد استدلال، لا متتاليات عددية.')],
 'ar-classical-0451-0500-soundness':[
  passage('normal-modal-logic/tableaux/soundness.tex',23,28,'يحدد الأصل جهة السلامة: جدول مغلق يثبت اللزوم الدلالي.'),
  passage('normal-modal-logic/tableaux/more-soundness.tex',13,16,'يعين معنى سلامة قاعدة بالنسبة إلى فئة محددة من النماذج.')],
 'compact:T-SUBSTITUTION':[
  passage('incompleteness/arithmetization-syntax/substitution.tex',12,24,'يعرّف الأصل إحلال حد محل الوقوعات الحرة للمتغير، ويعين النظير الحسابي للعملية.'),
  passage('incompleteness/arithmetization-syntax/substitution.tex',42,47,'تفصل القضية التالية شرط حرية الحد للمتغير، فلا يسقط شرط تجنب الأسر.')],
 'locale-ar-chosen-3f8f1c687051a8f2':[
  passage('propositional-logic/syntax-and-semantics/introduction.tex',37,62,'يميز الأصل تعريف تركيب الصيغ بقواعد التكوين من إعطاء معناها وصدقها في تقييم.')],
 'ar-classical-0451-0500-tableau-token':[
  passage('normal-modal-logic/tableaux/introduction.tex',13,30,'يعرّف الجدول شجرة صيغ موقعة، ويبين الفروع وشروط إغلاقها.')],
 'repair-compact-0601-0700:0684-T1':[
  passage('proof-theory/proof-search/tableaux.tex',13,23,'يسمي الأصل طريقة البرهان جداول دلالية أو أشجار صدق، ويصفها بشجرة صيغ لا مصفوفة قيم صدق.')],
}


def local_binding(selection):
    path,start,end,relevance=selection
    logical='content/'+path
    raw=(ENGLISH/logical).read_bytes()
    lines=raw.decode('utf-8').splitlines()
    excerpt='\n'.join(lines[start-1:end])
    assert 0<start<=end<=len(lines) and excerpt.strip()
    assert any(line.strip() and not line.strip().startswith('%') for line in excerpt.splitlines())
    return {'logical_path':logical,'line_start':start,'line_end':end,
            'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'lf_sha256':hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),
            'exact_passage':excerpt,'relevance_ar':relevance,
            'url':f'https://github.com/OpenLogicProject/OpenLogic/blob/{COMMIT}/{logical}#L{start}-L{end}'}


def generate():
    findings=json.loads((PUBLIC_FINDINGS if PUBLIC_FINDINGS.exists() else FINDINGS).read_bytes())
    assert findings['comment_only_passages']==59 and findings['affected_decisions']==32
    assert {r['decision_id'] for r in findings['findings']}==set(SELECTIONS)
    PUBLIC_FINDINGS.write_text(json.dumps(findings,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    # Include exact narrow input files, so this public batch does not require
    # access to an owner's private checkout to regenerate its cards.
    paths={'content/'+s[0] for choices in SELECTIONS.values() for s in choices}
    correction=assembly.review_corrections()
    paths.update(b['logical_path'] for r in correction['records'] for b in r['source_bindings'])
    for path in sorted(paths):
        raw=(ENGLISH/path).read_bytes()
        output=SNAPSHOT/'english'/path
        output.parent.mkdir(parents=True,exist_ok=True)
        if output.exists():
            assert output.read_bytes()==raw
        else:
            output.write_bytes(raw)
    for r in correction['records']:
        for b in r['target_bindings']:
            output=SNAPSHOT/'repo'/b['logical_path']
            origin=ROOT/b['logical_path']
            raw=(origin if origin.exists() else output).read_bytes()
            assert (len(raw),hashlib.sha256(raw).hexdigest())==(b['bytes'],b['sha256'])
            output.parent.mkdir(parents=True,exist_ok=True)
            if output.exists():
                assert output.read_bytes()==raw
            else:
                output.write_bytes(raw)
    mapping=assembly.card_map(include_revisions=False)
    notes=assembly.note_map()
    with gzip.open(BASE/'DECISION_RECORD_AR.jsonl.gz','rt',encoding='utf-8') as stream:
        current={r['decision_id']:r for line in stream if (r:=json.loads(line))['decision_id'] in SELECTIONS}
    records=[]
    output=['# تصحيح إحالات الأصل إلى نصوص تدعم الشرح — ٣٠ سبتمبر ٢٠٢٦\n',
            '[مدخل المراجعة](INDEX_AR.md) · [الدليل الكامل](DIRECTORY_AR.md)\n',
            'كانت ٥٩ إحالة إضافية في ٣٢ قرارًا تشير إلى تعليقات أسماء الأقسام والفصول، لا إلى نص يشرح المفهوم. '
            'استُبدلت هنا بإحالات إلى مقاطع قرئت فعلًا في الأصل. تبقى البطاقات القديمة محفوظة لتاريخ التصحيح. '
            'التصحيح من عمل OpenAI Codex — GPT-6.1 Sol، بمستوى جهد Ultra؛ لا مراجعة بشرية شاملة.\n',
            'هذه مقابلة لمواضع الشاهد الرياضي؛ لا تثبت وحدها أن كل لفظ عربي هو الأفضل أو أن جميع شواهد المعجم قوبلت من جديد. '
            'التعليلات والأسئلة أدناه موروثة إلا الشروح الخمسة المصححة والمبينة في [بطاقة التصحيحات](SOL6_CORRECTIONS_AR.md). '
            'لا تنسب التعليلات اللاحقة إلى دافع المترجم الأول.\n']
    for identifier,selections in SELECTIONS.items():
        old_card=mapping[identifier]
        sections=(BASE/old_card).read_text(encoding='utf-8').split('\n## ')[1:]
        section=next(s for s in sections if '`'+identifier+'`' in s)
        marker='**كل وقوع مسجل لهذا القرار:**'
        assert section.count(marker)==1
        occurrences=marker+section.split(marker,1)[1]
        occurrences=occurrences.replace('— reducts and expansions','— المختزلات والتوسيعات')
        row=current[identifier]; note=notes[identifier]
        removed=[{k:r[k] for k in ('notes_file','logical_path','lines','passage','source_checkout_sha256')}
                 for r in findings['findings'] if r['decision_id']==identifier]
        bindings=[local_binding(s) for s in selections]
        records.append({'decision_id':identifier,'previous_card':old_card,
                        'removed_non_supporting_pointers':removed,'replacement_bindings':bindings})
        output.extend(['## '+row['chosen_arabic']+'\n',f"معرّف القرار: `{identifier}`.\n",
                       '**المعنى المقصود:** '+note['sense_ar']+'\n',
                       '**سبب الاختيار أو التصحيح:** '+note['rationale_ar']+'\n',
                       '**سؤال مفتوح للمختص:** '+note['expert_question_ar']+'\n',
                       '**الإحالات المقروءة البديلة:**\n'])
        for b in bindings:
            output.append(f"- [الأسطر {b['line_start']}–{b['line_end']}]({b['url']}): {b['relevance_ar']} تجزئة SHA-256 المحلية: `{b['sha256']}`؛ وبعد توحيد النهايات إلى LF: `{b['lf_sha256']}`.\n")
        output.extend([f"\n**ما استُبدل:** {len(removed)} إحالة لا تحوي إلا تعليق اسم الفصل أو القسم؛ [البطاقة القديمة]({old_card}) باقية بوصفها شاهدًا تاريخيًا.\n",
                       '**حدود هذه المقابلة:** قرئت المقاطع الرياضية أعلاه. الشاهد المعجمي وحدوده في البطاقة القديمة لم يكتسبا تصديقًا جديدًا بهذه العملية؛ تظل المفاضلة الاصطلاحية مفتوحة للتصحيح. جميع الوقوعات الموروثة محفوظة، وليست هذه الإحالات الجديدة ادعاء مقابلة كل وقوع من جديد.\n',occurrences])
    value={'schema':'openlogic-arabic-source-witness-corrections-v1','model':'GPT-6.1 Sol','effort':'Ultra',
           'source_index_sha256':assembly.EXPECTED,'english_source_commit':COMMIT,
           'review_card':CARD,'removed_comment_only_pointers':59,'affected_decisions':32,
           'scope_ar':'استبدال إحالات تعليقات المصدر بمقاطع رياضية مقروءة؛ لا تصديق شامل للمصطلحات أو شواهد المعجم.',
           'records':records}
    MANIFEST.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    (BASE/CARD).write_text('\n'.join(output),encoding='utf-8',newline='\n')
    print(json.dumps({'status':'PASS_EXPLICIT_59_POINTER_REPLACEMENT_LOCAL','decisions':len(records)}))


def verify_public():
    value=json.loads(MANIFEST.read_bytes())
    bindings={('source',b['logical_path']):b for r in value['records'] for b in r['replacement_bindings']}
    correction=assembly.review_corrections()
    for r in correction['records']:
        for kind in ('source_bindings','target_bindings'):
            for b in r[kind]:
                bindings[('source' if kind=='source_bindings' else 'target',b['logical_path'])]=b
    def fetch(item):
        (kind,path),b=item
        target=ROOT/path
        local=((ENGLISH/path) if kind=='source' else (target if target.exists() else SNAPSHOT/'repo'/path)).read_bytes()
        assert (len(local),hashlib.sha256(local).hexdigest())==(b['bytes'],b['sha256'])
        repo='OpenLogicProject/OpenLogic' if kind=='source' else 'KokunoYumeto/OpenLogic-ar'
        commit=COMMIT if kind=='source' else '86a4a7c11c0a0289ade28cb8f96acbacf9c01844'
        url=f'https://raw.githubusercontent.com/{repo}/{commit}/{path}'
        with requests.Session() as anonymous:
            anonymous.trust_env=False
            result=anonymous.get(url,timeout=(20,60)); result.raise_for_status()
        assert result.content==(local.replace(b'\r\n',b'\n') if kind=='source' else local),path
        return {'kind':kind,'logical_path':path,'url':url,'bytes':len(result.content),
                'sha256':hashlib.sha256(result.content).hexdigest(),'anonymous':True,
                'local_differs_only_by_crlf':kind=='source' and result.content!=local}
    with ThreadPoolExecutor(max_workers=3) as pool:
        checked=list(pool.map(fetch,sorted(bindings.items())))
    receipt={'status':'PASS_ANONYMOUS_EXACT_PINNED_SOURCE_READBACK',
             'manifest_sha256':hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
             'correction_sha256':hashlib.sha256(assembly.TERM.joinpath('SOL6_REEXAMINATION_CORRECTIONS_20260930.json').read_bytes()).hexdigest(),
             'files':checked,'model':'GPT-6.1 Sol','effort':'Ultra'}
    with RECEIPT.open('x',encoding='utf-8',newline='\n') as destination:
        destination.write(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'files':len(checked)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('generate','verify-public'))
    args=parser.parse_args()
    {'generate':generate,'verify-public':verify_public}[args.action]()
