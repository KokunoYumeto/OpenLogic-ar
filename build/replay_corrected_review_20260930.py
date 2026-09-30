"""One cold reconstruction of the actual corrected public-review source ZIP."""
import gzip
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import zipfile

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'expert-review/2026-09-26-final-page-review'
ARCHIVE=BASE/'90-ARABIC-REVIEW-COMPLETE-SOURCE.zip'
RECEIPT=BASE/'CORRECTED_REVIEW_SOURCE_COLD_REPLAY_20260930.json'
FILES=('SOL6_CORRECTIONS_AR.md','SOL6_SOURCE_REFERENCES_AR.md','SOL6_FUNCTION_DEFINITIONS_AR.md','SOL6_CONTEXTUAL_CHOICES_AR.md','SOL6_PROOF_QUANTIFICATION_AR.md','SOL6_FREE_BOUND_VARIABLE_AR.md','DIRECTORY_AR.md','DECISION_RECORD_AR.jsonl.gz')


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main(receipt_path=None):
    accepted=json.loads((BASE/'COMPLETE_SOURCE_PACKAGE_RECEIPT.json').read_bytes())
    assert digest(ARCHIVE).upper()==accepted['sha256']
    readable=json.loads((BASE/'READABLE_REVIEW_RECEIPT_20260930.json').read_bytes())
    names=FILES+tuple(r['path'] for r in readable['files'])
    expected={name:digest(BASE/name) for name in names}
    with TemporaryDirectory(prefix='arabic-review-cold-',dir=ROOT/'tmp') as temporary:
        destination=Path(temporary).resolve()
        destination.relative_to((ROOT/'tmp').resolve())
        with zipfile.ZipFile(ARCHIVE) as source:
            assert sum(i.file_size for i in source.infolist())<512*1024*1024
            for member in source.infolist():
                (destination/member.filename).resolve().relative_to(destination)
                assert not member.is_dir()
            source.extractall(destination)
        base=destination/BASE.relative_to(ROOT)
        index=destination/'tmp/expert-index-final-pages-20260926-r1/EXPERT_REVIEW_INDEX.json'
        index.parent.mkdir(parents=True)
        count=0
        with gzip.open(base/'EXPERT_REVIEW_INDEX.json.gz','rb') as source, index.open('xb') as sink:
            while block:=source.read(1048576):
                count+=len(block); assert count<512*1024*1024
                sink.write(block)
        assert digest(index).upper()=='FCBBA8B6F6EFEBA4C515B829843A19DC33750B587F10702898A6DD37BB4D4B12'
        for script,args in (
            ('correct_added_source_witnesses_20260930.py',['generate']),
            ('render_sol6_review_corrections_20260930.py',[]),
            ('render_function_definition_recheck_20260930.py',[]),
            ('render_contextual_recheck_20260930.py',[]),
            ('render_contextual_recheck_20260930.py',['--ledger','evidence/classical/terminology/SOL6_PROOF_QUANTIFICATION_RECHECK_20260930.json']),
            ('render_contextual_recheck_20260930.py',['--ledger','evidence/classical/terminology/SOL6_FREE_BOUND_VARIABLE_RECHECK_20260930.json']),
            ('assemble_complete_arabic_review.py',[]),
            ('verify_complete_arabic_review.py',[]),
            ('render_readable_review_20260930.py',[]),
            ('verify_readable_review_20260930.py',[]),
        ):
            result=subprocess.run([sys.executable,'-X','utf8','build/'+script,*args],cwd=destination,
                                  capture_output=True,text=True,encoding='utf-8',timeout=120)
            assert result.returncode==0,(script,result.stderr[-2000:])
        assert {name:digest(base/name) for name in names}==expected
    value={'status':'PASS_COLD_REPLAY_FROM_EXACT_CORRECTED_REVIEW_ZIP',
           'source_zip_sha256':digest(ARCHIVE),'source_zip_bytes':ARCHIVE.stat().st_size,
           'byte_identical_outputs':expected,'model':'GPT-6.1 Sol','effort':'Ultra'}
    with (receipt_path or RECEIPT).open('x',encoding='utf-8',newline='\n') as sink:
        sink.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(value))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    main(parser.parse_args().output)
