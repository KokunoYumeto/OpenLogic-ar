"""Assemble eleven personally assessed relation choices with exact source witnesses.

The judgments below were written after reading the specified original pages
and current English/MSA/Classical contexts. This script only binds that authored
assessment to bytes and locations. It does not infer semantic correctness.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from validate_expert_review_snapshot import decisions, digest, verify_canon_amendment_v2

REPO=HERE.parent
ENGLISH=REPO.parents[1]/'openlogic-interfarsi/repo/source/upstream'
SNAPSHOT=Path('tmp/expert-index-integrated-20260913-corrected/EXPERT_REVIEW_INDEX.json')
SNAPSHOT_SHA='f51438240bb7c2d58ca885f572378c5621279cadca2f8dab16c81b7b89a41e22'
OUTPUT=Path('evidence/provenance/locale-ar/expert-review-amendments/canon-eleven-relation-choices-20260919.json')
DATE='2026-09-19'
PDF=Path('../sources/DAM2018ENAR/معجم مصطلحات الرياضيات.pdf')
PDF_SHA='6347572b0067fa84d8bdedfe9e33a4c63f7ae1cc650b44c658d12e3551f2d91e'
HISTORY=('alternatives','authority_checks','basis','chosen_arabic','confidence',
 'decision_id','edition','edition_reuse','english_term','expert_question',
 'expert_review_reason','expert_review_useful','global_source_bindings',
 'grammatical_realization','msa_arabic','occurrences','open_to_correction',
 'rationale','recording_mode','sense','source_record','source_records','status')

CANON={
 'anti':dict(page=42,printed='30',headword='antisymmetric relation',form='علاقة متناظرة متخالفة',
   relevance='The bottom-right relation entry requires a=b when both directed pairs belong. The adjacent antisymmetric matrix entry instead uses A=-A^T; that algebraic sign-reversal sense must not be imported into the relation definition.'),
 'asym':dict(page=52,printed='40',headword='asymmetric (adj)',form='لاتناظري',
   relevance='Sense 2, not geometric sense 1, defines a relation on A with no a,b for which aRb and bRa both hold. The feminine لاتناظرية occurs in its relation prose. This includes the diagonal a=b, unlike antisymmetry.'),
 'product':dict(page=91,printed='79',headword='Cartesian product of two sets',form='جداء ديكارتي لمجموعتين',
   relevance='The left-column set entry gives A×B={(x,y):x∈A,y∈B} and a two-by-three ordered-pair table. The surrounding ring, vector-space and topological products have extra structure that is not assumed for this set product.'),
 'connected':dict(page=138,printed='126',headword='connected relation',form='علاقة مترابطة',
   relevance='The left-column relation entry explicitly restricts the pair to distinct elements and requires at least one directed pair in R. Its strict-order example does not require reflexive diagonal pairs. Connected graph and connected space on the same page describe different notions.'),
 'equivalence':dict(page=228,printed='216',headword='equivalence relation',form='علاقة تكافؤ',
   relevance='The left-column entry gives exactly the conjunction of reflexivity, symmetry and transitivity, with modular equality as an example. The same page also uses متكافئان for equivalent elements in a ring; that specialized algebraic definition is not a definition of arbitrary R-equivalence.'),
}

# Context ranges are from the current source texts actually read. They include
# the complete definition or the recalled ordered-pair explanation, not a bare term.
ANTI={'english':(38,55),'msa':(36,51),'classical':(35,49)}
ASYM={'english':(74,83),'msa':(69,85),'classical':(68,83)}
CONNECTED={'english':(57,60),'msa':(53,56),'classical':(51,54)}
EQ={'english':(17,21),'msa':(16,20),'classical':(16,20)}
SPEC={
 '91e56faf5ecdc898':dict(canon='anti',ranges=ANTI,english_literal=r'anti-sym\-met\-ric',arabic_literal=r'مضادّة\- للتناظر\-',
   sense='Antisymmetric binary relation: Rxy and Ryx together imply x=y; diagonal pairs are permitted but not required.',
   rationale='Provisionally retain مضادّة للتناظر as the predicative adjective, while recording that the Damascus Academy prints علاقة متناظرة متخالفة (physical p.42 / printed p.30), not this chosen phrase. The current English, MSA and Classical definitions all allow both directions only at x=y, and the following explanation expressly allows a relation to be both symmetric and antisymmetric. Thus مضادّة must not be interpreted as simple negation of symmetry. The preposition لـ links the adjective to التناظر; discretionary source hyphens are not lexical material. Semantic support comes from the matching relational condition, not from an invented exact-form attestation. This is a fresh retrospective assessment.',
   question='OLP-0014: does مضادّة للتناظر remain clear beside لا تناظرية, or should the relational term be standardized to the academy’s متناظرة متخالفة? Preserve the allowance of diagonal pairs.',
   alternatives='متناظرة متخالفة is the attested relation-specific alternative. غير متناظرة merely negates symmetry and is not an equivalent definition. The matrix sense A=-A^T is irrelevant.',
   grammar='Feminine predicate agrees with العلاقة; the prepositional complement names the property being contrasted.',confidence='medium'),
 '609c2f0ce8adca0c':dict(canon='anti',ranges=ANTI,
   sense='Heading naming antisymmetry, not asymmetry and not merely failure of symmetry.',
   rationale='Provisionally retain مضادّة التناظر as the heading for the adjacent predicate مضادّة للتناظر. The academy’s physical p.42 / printed p.30 supplies the same implication from both relation directions to equality, but names the relation علاقة متناظرة متخالفة. It does not print this abstract heading. Here the immediately following definition and identity-relation example fix the heading’s technical meaning; the wording is therefore a source-defined editorial label, not an academy-attested noun. Keep this heading and its predicate linked in any later terminology revision. This is a fresh retrospective assessment.',
   question='OLP-0014 heading: should مضادّة التناظر be retained with its explicit definition, or replaced as a family with متناظرة متخالفة? Do not merge this heading with اللاتناظرية.',
   alternatives='The attested adjective متناظرة متخالفة describes a relation; turning it into an abstract noun would itself require an explicitly recorded editorial choice. اللاتناظرية denotes the stronger no-two-directions condition.',
   grammar='A definite property heading; unlike the running predicate, it omits the preposition لـ.',confidence='medium'),
 'a41652349417a154':dict(canon='asym',ranges=ASYM,
   sense='Asymmetric binary relation: no x,y, including x=y, satisfy both Rxy and Ryx.',
   rationale='Retain لا تناظرية in the defining predicate. Sense 2 of asymmetric on academy physical p.52 / printed p.40 defines a relation by exactly the absence of simultaneous aRb and bRa; the current three source contexts preserve that quantifier scope. The current spaced feminine form لا تناظرية differs typographically from the dictionary’s joined لاتناظرية in its relation prose, so the exact full spelling is not certified. It is not merely a relation that happens to lack symmetry: even a diagonal pair is prohibited. The following contrast with antisymmetry remains essential. This is a fresh retrospective assessment.',
   question='OLP-0014: retain لا تناظرية or join it as لاتناظرية? More importantly, does the reader see that every pair, including x=y, is covered and this is stronger than مضادّة التناظر?',
   alternatives='غير متناظرة is insufficient: failure of universal symmetry does not forbid every mutually related pair. مضادّة للتناظر permits diagonal pairs and is a different property.',
   grammar='Feminine adjective agrees with العلاقة; لا is part of the technical negative formation, not a separately quantified negation of the whole sentence.',confidence='high'),
 '825a846b9dd45920':dict(canon='asym',ranges=ASYM,
   sense='Abstract heading for the asymmetric-relation property, not general visual nonsymmetry.',
   rationale='Retain اللاتناظرية as the property heading paired with لا تناظرية in the definition. Academy physical p.52 / printed p.40 supports the relational adjective through sense 2, while sense 1 concerns a figure without geometric symmetry. Only the relational sense matches the following no-pair condition. The definite abstract heading is a grammatical editorial derivation, not a literal dictionary headword. The three current texts preserve the contrast that every asymmetric relation is antisymmetric but not conversely. This is a fresh retrospective assessment.',
   question='OLP-0014 heading: is اللاتناظرية a clear property name when the following predicate is spaced لا تناظرية? Check that it is not read as the weaker absence of symmetry.',
   alternatives='عدم التناظر risks the weaker everyday reading unless the full relational definition is retained; مضادّة التناظر is already reserved for the different diagonal-permitting property.',
   grammar='Definite abstract property name derived from the negative adjective; the dictionary supports its base and technical sense, not the whole heading literally.',confidence='high'),
 'aae883d44b7db318':dict(canon='connected',ranges=CONNECTED,
   sense='Connex/connected binary relation: for distinct x,y at least one of Rxy or Ryx holds; no diagonal condition is imposed.',
   rationale='Provisionally retain متصلة as the predicate because the adjacent definition fixes the relation-specific sense exactly: only x≠y is tested and at least one direction is required. Academy physical p.138 / printed p.126 instead prints علاقة مترابطة and illustrates it with a strict order, confirming the same distinct-elements restriction. It does not attest the chosen adjective متصلة for this entry. Do not import the graph-path or topological definitions printed nearby, and do not strengthen the condition to require xRx. This is a fresh retrospective assessment; the lexical mismatch stays visible.',
   question='OLP-0014: would مترابطة be clearer and better aligned with the academy than متصلة? Keep x≠y and the inclusive “at least one direction” condition unchanged.',
   alternatives='مترابطة is the attested relational alternative. A paraphrase saying every pair is related without excluding equality would incorrectly add reflexivity. Graph connectivity is not the intended definition.',
   grammar='Feminine predicate agrees with العلاقة. The phrase أحد ... على الأقل expresses inclusive disjunction, not exactly one direction.',confidence='medium'),
 '7ebacfd287239670':dict(canon='connected',ranges=CONNECTED,
   sense='Heading naming comparability of every distinct pair under a binary relation, not connectivity number or a topological property.',
   rationale='Provisionally retain الاتصالية as the heading tied to the source predicate متصلة. Academy physical p.138 / printed p.126 uses علاقة مترابطة for the matching relation definition; it does not print this abstract heading. The heading’s meaning is determined by the following explicit x≠y condition, so it is not licensed by the separate connectivity-number, graph or space entries on that page. A future lexical revision must change the heading and predicate together while preserving the distinct-pair scope. This is a fresh retrospective assessment, not a claim of official wording.',
   question='OLP-0014 heading: should الاتصالية and متصلة be standardized together to الترابط and مترابطة, while preserving the current distinct-pair definition?',
   alternatives='الترابط is a transparent heading associated with the attested predicate مترابطة, but that derived heading is an editorial construction rather than a literal headword quoted here. رقم الترابط is a different invariant.',
   grammar='Definite abstract heading paired with a feminine predicate; neither typography nor nominalization changes the quantified definition.',confidence='medium'),
 'f9b8162b180b0849':dict(canon='product',ranges={'english':(23,32),'msa':(22,30),'classical':(20,27)},english_literal='Cartesian\nproduct',
   sense='Recalled Cartesian product A×B consisting of ordered pairs with first coordinate in A and second coordinate in B, then specialized to A×A.',
   rationale='Provisionally retain الضرب الديكارتي in this recall paragraph, while explicitly noting that academy physical p.91 / printed p.79 uses جداء ديكارتي لمجموعتين. The complete local paragraph contrasts ordered with unordered pairs and then gives exactly the set-product condition shown in the dictionary’s formula and table. الديكارتي and the ordered-pair definition disambiguate الضرب from numerical multiplication; no ring, vector-space or topological structure is asserted. The current phrase is not literally attested by this page. This is a fresh retrospective assessment of this occurrence, not of every product in the book.',
   question='OLP-0012: should الضرب الديكارتي be standardized to الجداء الديكارتي? Check that A×B keeps the order of the two coordinates and the specialization A²=A×A.',
   alternatives='الجداء الديكارتي is the academy-aligned alternative. A set of unordered pairs would erase coordinate order; a numeric product would change the type of object.',
   grammar='A definite noun phrase naming the recalled construction; the adjective identifies which mathematical product is meant.',confidence='medium'),
 'f7c277e69d8cf7d5':dict(canon='product',ranges={'english':(52,66),'msa':(53,67),'classical':(49,63)},
   sense='Definition heading for the set Cartesian product, all ordered pairs from A and B; not multiplication of numbers.',
   rationale='Provisionally retain الضرب الديكارتي as the definition heading because both Arabic layers immediately define the full ordered-pair set and give the six-pair example corresponding to a two-element A and three-element B. Academy physical p.91 / printed p.79 gives the same construction and a two-by-three example under جداء ديكارتي لمجموعتين. This supports the mathematical interpretation but not the exact chosen noun ضرب; the stronger lexical evidence favors recording الجداء الديكارتي as the concrete alternative. This is a fresh retrospective assessment, keeping that lexical uncertainty visible.',
   question='OLP-0009 heading and definition: would الجداء الديكارتي be preferable to الضرب الديكارتي? Verify all six ordered pairs remain present and that the heading is consistent with OLP-0012.',
   alternatives='الجداء الديكارتي matches the academy’s noun family. Simply ضرب without الديكارتي would be less discriminating; replacing pairs by their arithmetic products is mathematically wrong.',
   grammar='Definite technical heading; both the modern possessive construction ضربهما and Classical الضرب ... للمجموعتين realize the same definition.',confidence='medium'),
 'da2be23f72d81e99':dict(canon='equivalence',ranges=EQ,
   sense='An equivalence relation on A: the conjunction of reflexivity, symmetry and transitivity.',
   rationale='Retain علاقة التكافؤ as the definition heading. Academy physical p.228 / printed p.216 prints علاقة تكافؤ and defines it by exactly the same three properties. The added article in the current heading is a contextual definite construction, not a verbatim headword. Both current Arabic definitions retain all three requirements; the later modular example explains that equivalence is relative to a relation and need not be identity. The same page’s alias equals relation does not justify replacing general equivalence by literal equality. This is a fresh retrospective assessment.',
   question='OLP-0015: does علاقة التكافؤ clearly preserve all three properties without implying the related elements must be identical?',
   alternatives='علاقة تكافؤ is the dictionary’s indefinite headword and is appropriate in an indefinite definition sentence. علاقة مساواة alone risks conflating an arbitrary equivalence with identity.',
   grammar='A definite construct phrase in the heading; the running modern definition also uses the indefinite علاقة تكافؤ.',confidence='high'),
 '7b0462c3fdfe278d':dict(canon='equivalence',ranges={'english':(11,21),'msa':(11,20),'classical':(11,20)},
   sense='Section heading covering equivalence relations as a class of reflexive, symmetric and transitive relations.',
   rationale='Retain علاقات التكافؤ as the section title. It is the regular plural construct corresponding to the academy’s singular علاقة تكافؤ on physical p.228 / printed p.216. The introductory identity example and following definition constrain the title to this technical class; the section then develops equivalence classes and modular examples rather than numerical equality alone. The plural definite title is grammatically justified but is not claimed as a literal printed dictionary phrase. This is a fresh retrospective assessment.',
   question='OLP-0015 section title: is علاقات التكافؤ consistent with the singular definition and clearly broader than equality of identical objects?',
   alternatives='علاقات المساواة could wrongly narrow the general relation. Keeping a singular title would change the discourse focus but not improve the attested technical family.',
   grammar='Sound feminine plural علاقات in a definite construct with التكافؤ; pluralization matches the chapter’s treatment of a class of relations.',confidence='high'),
 '3f36b6b993e1028e':dict(canon='equivalence',ranges=EQ,
   sense='Two elements x,y are equivalent relative to the specified equivalence relation R precisely when Rxy; they need not be equal.',
   rationale='Retain متكافئان وفق R, with R kept as the source formula. The dual متكافئان agrees with the explicitly paired x and y; وفق R makes the parameter of equivalence explicit and the following Rxy fixes its meaning. Academy physical p.228 / printed p.216 supports the relation family علاقة تكافؤ and uses متكافئان in its equivalent-elements entry, but that latter entry has a special ring-theoretic definition. Only its linguistic form, not its ring condition, is relevant here. The full qualified phrase is not literally attested. This is a fresh retrospective assessment.',
   question='OLP-0015: is متكافئان وفق R idiomatic, or is متكافئان بالنسبة إلى R clearer? In either case it must mean Rxy, not x=y or the specialized ring notion of equivalent elements.',
   alternatives='متكافئان بالنسبة إلى R is an explicit relation-relative paraphrase. متساويان would falsely strengthen arbitrary equivalence to identity; importing the ring definition would add absent structure.',
   grammar='Nominative dual predicate for x and y; the prepositional phrase qualifies the relation under which equivalence is asserted.',confidence='high'),
}


def identity(relative):
    path=(REPO/relative).resolve()
    return {'path':str(relative).replace('\\','/'),'bytes':path.stat().st_size,'sha256':digest(path)}


def build():
    if digest(REPO/SNAPSHOT)!=SNAPSHOT_SHA: raise ValueError('Retained review snapshot changed')
    if digest(REPO/PDF)!=PDF_SHA: raise ValueError('Consulted dictionary bytes changed')
    source={**identity(PDF),'title':'معجم مصطلحات الرياضيات','source_id':'DAM2018ENAR','url':'https://archive.org/details/DAM2018ENAR'}
    rows={r['decision_id'].rsplit(':',1)[-1]:r for r in decisions(REPO/SNAPSHOT)
          if r['decision_id'].rsplit(':',1)[-1] in SPEC}
    if set(rows)!=set(SPEC): raise ValueError('Missing or duplicate selected decision')
    amendments=[]
    for key,spec in SPEC.items():
        row=rows[key]
        if 'This is a present-tense retrospective justification' not in row['rationale']:
            raise ValueError('Selected record is no longer an unassessed template')
        if len(row['occurrences'])!=1: raise ValueError('Uninspected extra occurrence')
        occurrence=row['occurrences'][0]
        witnesses,locations=[],[]
        for kind in ('english','msa','classical'):
            old=occurrence[kind]; base=ENGLISH if kind=='english' else REPO
            path=base/old['path']; raw=path.read_bytes(); lines=raw.decode('utf-8-sig').splitlines()
            lo,hi=spec['ranges'][kind]
            if hi>len(lines): raise ValueError('Context exceeds actual source')
            excerpt='\n'.join(lines[lo-1:hi])
            phrase=spec.get('english_literal',row['english_term']) if kind=='english' else spec.get('arabic_literal',row['chosen_arabic'])
            if phrase.casefold() not in excerpt.casefold(): raise ValueError('Term not in inspected context: '+key+' '+kind)
            offset=excerpt.casefold().find(phrase.casefold())
            term_start=lo+excerpt[:offset].count('\n'); term_end=term_start+phrase.count('\n')
            sha=hashlib.sha256(raw).hexdigest()
            witnesses.append({'source_kind':kind,'path':old['path'],'line_start':lo,'line_end':hi,
                'file_sha256':sha,'excerpt':excerpt,'excerpt_sha256':hashlib.sha256(excerpt.encode()).hexdigest(),
                'semantic_basis':spec['sense']+' The actual complete local context was read before assessment.'})
            locations.append({'source_kind':kind,'path':old['path'],'sha256':sha,
                'line_start':term_start,'line_end':term_end})
        canon=CANON[spec['canon']]
        passage=canon['headword']+'\n'+canon['form']
        ev={'source':copy.deepcopy(source),'physical_page':canon['page'],'printed_page':canon['printed'],
            'entry':canon['headword'],'exact_passage':passage,'passage_sha256':hashlib.sha256(passage.encode()).hexdigest(),
            'transcription_mode':'manual-visual-transcription-diacritics-normalized',
            'page_image':identity(Path(f"tmp/pdfs/relation-canon-20260919/dam-{canon['page']:03d}.png")),
            'consulted_before_assessment':True,'consulted_on':DATE,'recording_mode':'retrospective-canon-check',
            'chosen_arabic_form':spec.get('arabic_literal',row['chosen_arabic']),
            'attested_arabic_form':canon['form'],'english_headword':canon['headword'],
            'english_source_phrase':spec.get('english_literal',row['english_term']),
            'english_sense':spec['sense'],'relation':'related-not-exact',
            'source_witness_indices':[1,2],'english_witness_indices':[0],
            'relevance':canon['relevance'],
            'limits':'The complete original page was personally read before this fresh retrospective assessment. Only the short bilingual headword is transcribed, with diacritics omitted; definitions are paraphrased, not quoted. This page supports the specified technical comparison, not an exact attestation of the current full phrase, medieval prose register, or whole-book correctness.'}
        entry={'decision_id':row['decision_id'],'assessed_on':DATE,
            'recording_mode':'new-independent-semantic-assessment','assessment_origin':'retrospective-reconstruction',
            'open_to_correction':True,'official_attestation_claimed':False,
            'expected':{k:row[k] for k in ('english_term','chosen_arabic','rationale')},
            'changes':{'sense':spec['sense'],'rationale':spec['rationale'],'expert_question':spec['question'],
                'expert_review_useful':True,'expert_review_reason':'Review the located lexical/register choice and the stated canon comparison; mathematical conditions must remain unchanged.'},
            'witnesses':witnesses,'canon_evidence':[ev],
            'checked_occurrences':[{'unit_id':occurrence['unit_id'],'locations':locations}],
            'contextual_coverage':{'supplied_occurrence_groups':1,'source_kinds':['english','msa','classical'],
                'all_supplied_occurrences_checked':True,
                'scope':'All supplied occurrences of this exact record checked. Same-lemma records and other corpus occurrences are not silently certified.'},
            'grammatical_realization_assessment':spec['grammar'],
            'current_editorial_assessment':{'status':'source-grounded-provisional-retention',
                'confidence':{'level':spec['confidence'],'reason':'Current mathematical contexts and personally read canon support the comparison; exact lexical attestation is explicitly limited. This is editorial confidence, not a calibrated probability.'},
                'alternative_comparison':spec['alternatives'],'expert_review_useful':True,'source_edit_applied':False},
            'proposed_source_edits':[],
            'historical_fields':{k:copy.deepcopy(row[k]) for k in HISTORY if k in row},
            'historical_metadata_note':'Previous OCR checks, source records and templated motivation are preserved as history. The present judgment is retrospective; no earlier canon consultation is invented.'}
        if 'arabic_literal' in spec:
            entry['observed_arabic_forms']=[{'form':spec['arabic_literal'],'source_witness_indices':[1,2],
                'note':'Literal source spelling includes discretionary TeX hyphenation; the normalized chosen Arabic remains unchanged.'}]
        verify_canon_amendment_v2(REPO,entry,ENGLISH)
        amendments.append(entry)
    pages=[{**identity(Path(f'tmp/pdfs/relation-canon-20260919/dam-{p:03d}.png')),
            'physical_page':p,'printed_page':str(p-12)} for p in (42,52,91,138,228)]
    return {'schema':'openlogic-ar-expert-review-amendments-v2','assessed_on':DATE,
        'retained_index':{'path':SNAPSHOT.as_posix(),'sha256':SNAPSHOT_SHA},
        'english_source_commit':'9620cc73f9c8e0ad003c514a5d3748f29611c4c0',
        'scope':'Eleven real pending template records in four units, with all33 current English/MSA/Classical occurrence locations checked. No translated source wording was changed. This is not the complete translation audit.',
        'canon_inventory':{'source':source,'edition':'First edition, Damascus Academy, 1439 AH / 2018 CE; original cover and imprint personally read in this pass.',
            'pages':pages,'identity_pages':[identity(Path(f'tmp/pdfs/eight-template-canon-99848725/dam-{p:03d}.png')) for p in (1,3)],
            'read_method':'OCR/XML located the entries; each complete original page image was personally read before writing the judgments.',
            'limits':'All full chosen phrases are conservatively classified related-not-exact. Academy mathematical terminology is not evidence of medieval phrasing.'},
        'amendments':amendments}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=REPO/OUTPUT)
    args=parser.parse_args()
    if args.output.exists(): raise ValueError('Do not overwrite an existing assessment ledger')
    payload=build()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'amendments':len(payload['amendments']),'sha256':digest(args.output),'translated_source_edits':0}))


if __name__=='__main__': main()
