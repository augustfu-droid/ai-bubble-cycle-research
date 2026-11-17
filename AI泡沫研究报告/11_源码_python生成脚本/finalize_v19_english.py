#!/usr/bin/env python3
"""Finalize only the hash-matched, reviewed English translation."""
from pathlib import Path
import json,hashlib,re,subprocess
import build_v19_english as b

ROOT=b.ROOT;OUT=b.OUT;SOURCE=b.SOURCE
RECORDS=ROOT/'复审与版本记录/V1.9_English_20261031'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,text):Path(p).write_text(text.rstrip()+'\n',encoding='utf-8')

def main():
    manifest=read(OUT/'manifest.json');qa=read(OUT/'qa.json');structure=read(RECORDS/'translation-structure-check.json');spec=b.manifest()
    assert not manifest['preview'] and qa['status']=='PASS_ARTIFACT_STRUCTURE' and not qa['errors']
    assert qa['pdf_sha256']==sha(manifest['outputs']['pdf']['path'])
    assert qa['validator_sha256']==sha(ROOT/'11_源码_python生成脚本/qa_v19_english.py')
    assert structure['status']=='PASS_STRUCTURE_PENDING_SEMANTIC_REVIEW' and not structure['errors']
    assert structure['checker_sha256']==sha(ROOT/'11_源码_python生成脚本/check_v19_english_translation.py')
    assert len(structure['files'])==20 and not structure['residual_han'] and not structure['unusually_short_lines']
    expected={u['file']:u for u in spec['units']};reviewed={};closed=0;review_records=[]
    for group in 'abc':
        path=RECORDS/f'review_group_{group}.json';review=read(path)
        assert review['status']=='PASS'
        assert all(issue['status']=='CLOSED' for issue in review['issues'])
        closed+=len(review['issues'])
        for row in review['files']:
            name=row['file'];assert name not in reviewed
            assert sha(SOURCE/'translation_inputs'/name)==row['source_sha256']==expected[name]['source_sha256']
            assert sha(SOURCE/'parts'/name)==row['english_sha256']==manifest['source_parts'][name]
            count=row['lines_reviewed']
            if isinstance(count,dict):count=count.get('count',count['end']-count['start']+1)
            assert count==expected[name]['source_lines'],name
            reviewed[name]=row
        for row in review.get('supplementary_scope',[]):
            assert row['result']=='PASS'
            assert sha(row['file'])==row.get('english_sha256',row.get('sha256'))
            if row.get('source_sha256'):assert sha(row['source'])==row['source_sha256']
        review_records.append({'group':group,'path':str(path),'sha256':sha(path)})
    assert set(reviewed)==set(expected)
    for row in structure['files']:
        assert row['status']=='PASS_STRUCTURE' and row['english_sha256']==sha(SOURCE/'parts'/row['file'])
    for row in manifest['outputs'].values():assert sha(row['path'])==row['sha256']
    visual=read(RECORDS/'visual-review.json')
    assert visual['status']=='PASS_SAMPLED_VISUAL' and not visual['issues']
    assert visual['pdf_sha256']==qa['pdf_sha256']
    assert visual['sampled_pages']==len(set(visual['pages_reviewed']))
    prior_path=ROOT.parent/'V1.9-publication-files.json'
    assert sha(prior_path)==spec['chinese_publication_manifest_sha256']
    prior=read(prior_path)
    assert all(sha(ROOT.parent/f['path'])==f['sha256'] for f in prior['files'])
    corrections=read(RECORDS/'translation_corrections.json')
    lines=sum(u['source_lines'] for u in spec['units'])
    word_count=sum(len(re.findall(r'\b[A-Za-z]+(?:[-\'][A-Za-z]+)*\b',(SOURCE/'parts'/u['file']).read_text(encoding='utf-8'))) for u in spec['units'])
    acceptance=f'''# V1.9 English translation: acceptance record

Status: PASS_LOCAL_DELIVERY. Unresolved translation blockers: 0.

This is the full English translation of the corrected Chinese V1.9 complete report, with a research cutoff of 31 October 2026, Beijing time. It is not a new research update. The Chinese PDF and all {len(prior['files'])} previously delivered Chinese-publication files remain byte-identical.

The English PDF has {manifest['pages']} pages, 13 consecutively numbered chapters, Appendices A-F, the overview and closing note, 8 translated figures, and 342 references after exact-URL deduplication. The difference from the Chinese edition's 209 pages results from English text and pagination, not omitted or added research chapters. Editable Markdown and HTML are included.

## Translation and independent review

Three translation agents and three separate reviewers used gpt-6-astra with xhigh reasoning. The independent reviewers compared every source and English line in their assigned files: {lines} aligned lines across 20 publication units, including every table. Initial translation ledgers retain the draft hashes; the final peer-review records contain the current corrected hashes. Their scope is translation fidelity, not renewed verification of external financial or scientific claims.

{len(corrections)} prose corrections were applied and reread, addressing lost possibility qualifiers, charging versus collection, acquisition direction, evidence versus proof, completed versus required verification, partial versus total restrictions, energy-storage terminology, revenue-recognition timing, hidden labor costs, payment direction and the referent of a promotional end date. A separate chart-label clarification aligned Zhongji Innolight's name with the text. All {closed} recorded review items are closed.

The reviews checked all author-ledger quantity/date/numbering changes and the current {len(structure['numeric_differences'])} numeric-difference lines. Chinese ten-thousand, hundred-million and trillion units, table-header units, formula denominators, currencies, ranges and precision were independently checked. Automated token comparison alone was not treated as proof of economic equivalence. Preserved historical inconsistencies and rounding limitations are recorded in the peer reviews rather than silently repaired in the translation.

Records: [Group A](review_group_a.json), [Group B](review_group_b.json), [Group C](review_group_c.json), [corrections](translation_corrections.json), and [structural comparison](translation-structure-check.json). Front matter, all 18 reference-label overrides and all 81 translated chart-label mappings also received independent semantic review.

## Artifact checks

All chapter and subsection structure, table shape, blank-line alignment, source and output hashes, link/image destinations and reference URL coverage were checked. The final PDF was decoded page by page; its {qa['bookmarks_checked']} headings/bookmarks and {qa['toc_destinations_checked']} contents destinations were checked against the actual pages. No text exceeded the physical page bounds. The original chart geometry was preserved; text labels and their fit were translated.

{visual['scope']}

This is sampled visual inspection, not manual inspection of every page. No native WPS validation is claimed. External URLs were preserved, not all re-opened online for this translation. No remote push or publication was performed.
'''
    write(RECORDS/'translation-acceptance.md',acceptance)
    write(OUT/'README.md',f'''# {b.TITLE}

Daduizhang | V1.9 English | Research cutoff: 31 October 2026, Beijing time.

[Complete PDF ({manifest['pages']} pages)]({b.STEM}.pdf) | [Read online]({b.STEM}.html) | [Editable Markdown]({b.STEM}.md)

Complete translation of the corrected [Chinese report](../V1.9现行正文版/13_超全景版.pdf): 13 chapters, Appendices A-F, 8 English figures and 342 references after exact-URL deduplication. Research dates, assumptions and uncertainties follow the Chinese original. The English pagination differs from the original 209 pages.

[Translation review and acceptance](../复审与版本记录/V1.9_English_20261031/translation-acceptance.md) | [Artifact checks](qa.json) | [Build manifest](manifest.json)
''')
    files={p for p in SOURCE.rglob('*') if p.is_file()}
    files|={p for p in RECORDS.rglob('*') if p.is_file()}
    files|={p for p in OUT.rglob('*') if p.is_file() and 'qa_visual' not in p.parts}
    files|={p for p in (ROOT/'11_源码_python生成脚本').glob('*v19_english.py') if p.is_file()}
    files.add(ROOT/'11_源码_python生成脚本/README_v19_english.md')
    files={p for p in files if '__pycache__' not in p.parts}
    payload={'version':'V1.9 English','status':'PASS_LOCAL_DELIVERY','scope':'Full faithful English translation; no research refresh or remote publication',
             'pdf_pages':manifest['pages'],'source_chinese_pages':209,'chapters':13,'appendices':6,'figures':8,'unique_reference_urls':342,
             'translation_lines':lines,'approximate_english_words':word_count,'prose_corrections':len(corrections),'closed_review_items':closed,
             'review_records':review_records,'visual_sample_pages':visual['sampled_pages'],'chinese_publication_files_unchanged':len(prior['files']),
             'git_branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT.parent).decode().strip(),'remote_push_performed':False,
             'files':[{'path':str(p.relative_to(ROOT.parent)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)]}
    write(ROOT.parent/'V1.9-English-publication-files.json',json.dumps(payload,ensure_ascii=False,indent=2))
    for row in payload['files']:assert sha(ROOT.parent/row['path'])==row['sha256']
    subprocess.run(['git','diff','--check'],cwd=ROOT.parent,check=True)
    print(json.dumps({k:payload[k] for k in ['status','pdf_pages','translation_lines','prose_corrections','closed_review_items','visual_sample_pages','chinese_publication_files_unchanged','remote_push_performed']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
