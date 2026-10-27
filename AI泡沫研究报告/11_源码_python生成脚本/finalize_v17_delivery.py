#!/usr/bin/env python3
"""Read back local files twice; do not infer external publication or full native QA."""
from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote
from zoneinfo import ZoneInfo
import markdown
from build_v17_current import ROOT,OUT,SRC,sha,identity
from qa_v17_current import Parser,check_local

RECEIPT=ROOT/'复审与版本记录/V1.7_最终回读_20261027.json'
NATIVE_REVIEW=ROOT/'复审与版本记录/V1.7_WPS抽检_20261027.json'

def main():
    q=json.loads((OUT/'qa.json').read_text())
    if q['status']!='PASS_LOCAL_STRUCTURE':raise RuntimeError('Structure QA not passed')
    files=set(p for p in OUT.rglob('*') if p.is_file())
    files|=set(p for p in SRC.rglob('*') if p.is_file())
    files|=set((ROOT/'复审与版本记录').glob('V1.7*.md'))
    if NATIVE_REVIEW.is_file():files.add(NATIVE_REVIEW)
    files|={ROOT/'复审与版本记录/V1.7_改版前历史文件哈希_20261027.json',ROOT/'12_增量素材/2026-10-27_证据台账.json'}
    files|={ROOT/p for p in ['README.md','00_使用说明/原339页完整版_权威与重建.md','00_使用说明/README_大队长_全量存档说明.md','00_使用说明/V1.7_当前文件总索引_2026-10-27.md','11_源码_python生成脚本/build_v17_current.py','11_源码_python生成脚本/qa_v17_current.py','11_源码_python生成脚本/finalize_v17_delivery.py']}
    files={p for p in files if '__pycache__' not in str(p) and p!=RECEIPT}
    errors=[];deferred=[]
    for p in sorted(files):
        if p.suffix not in ('.html','.md'):continue
        parser=Parser();parser.feed(p.read_text() if p.suffix=='.html' else markdown.markdown(p.read_text(),extensions=['tables']))
        for ref in parser.links+parser.images:
            if not ref or ref.startswith(('https://','http://','mailto:','#')):continue
            dest=(p.parent/unquote(ref.split('#')[0])).resolve()
            if dest==RECEIPT:deferred.append(str(p.relative_to(ROOT)));continue
            if not dest.is_file():errors.append(f'broken local link: {p.relative_to(ROOT)} -> {ref}')
    manifest=json.loads((OUT/'manifest.json').read_text())
    for row in manifest['reports']:
        for kind in ['pdf','html','md']:
            if sha(ROOT/row[kind]['path'])!=row[kind]['sha256']:errors.append('manifest mismatch '+row[kind]['path'])
    history=json.loads((ROOT/'复审与版本记录/V1.7_改版前历史文件哈希_20261027.json').read_text())
    drift=[p for p,h in history.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    if drift:errors.append('historical drift '+str(drift))
    first={str(p.relative_to(ROOT)):sha(p) for p in sorted(files)}
    second={str(p.relative_to(ROOT)):sha(p) for p in sorted(files)}
    if first!=second:errors.append('files changed between readbacks')
    native_status='NOT_VERIFIED_CURRENT_FILE'
    native_scope=[]
    if NATIVE_REVIEW.is_file():
        native=json.loads(NATIVE_REVIEW.read_text())
        native_pdf=ROOT/native['pdf']
        if native_pdf.is_file() and sha(native_pdf)==native['pdf_sha256']:
            native_status=native['status'];native_scope=native['pages_visually_inspected']
        else:errors.append('native sample review belongs to a different PDF hash')
    status='PASS_LOCAL_FILE_READBACK_CONTACT_PENDING' if identity()['contact_status']=='pending_user_confirmation' else 'PASS_LOCAL_FILE_READBACK'
    payload={'version':'V1.7','checked_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),'status':'FAIL' if errors else status,'scope':'content reconstruction, structural and sampled rendering checks, local file readback only','errors':errors,'files_read_twice':len(files),'all_hashes_stable':first==second,'pdf_count':len(q['reports']),'pdf_pages':sum(r['pages'] for r in q['reports']),'historical_files_unchanged':len(history)-len(drift),'reference_urls_full_edition':next(r['reference_count'] for r in q['reports'] if r['slug']=='13_超全景版'),'contact_status':identity()['contact_status'],'wps_final_watermarked_edition':'NOT_VERIFIED_MAC_LOCKED','wps_previous_unwatermarked_observation':'cover and page 4 only; not reused as final-edition acceptance','git_actions_this_turn':[],'external_publication_actions_this_turn':[],'receipt_links_resolved_on_write':deferred,'sha256':first}
    payload['wps_final_watermarked_edition']=native_status
    payload['wps_final_sample_pages']=native_scope
    RECEIPT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    reread=json.loads(RECEIPT.read_text())
    if reread!=payload:raise RuntimeError('Receipt readback mismatch')
    print(json.dumps({k:payload[k] for k in ['status','files_read_twice','all_hashes_stable','pdf_count','pdf_pages','historical_files_unchanged','reference_urls_full_edition','contact_status','errors']},ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
