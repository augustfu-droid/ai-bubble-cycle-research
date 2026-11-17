#!/usr/bin/env python3
"""Validate regenerated current prose, directory links, page destinations and history."""
from __future__ import annotations
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
import fitz
from check_v18_calculations import calc_checks
from build_v18_current import ROOT,SRC,OUT,CATALOG,prepare_body,source_path,sha,IDENTITY_PATH,identity,reference_entries,REFERENCE_LABELS_PATH

class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.images=[]
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if t=='a':self.links.append(a.get('href',''))
        if t=='img':self.images.append(a.get('src',''))

def norm(s):return re.sub(r'\s+','',s)
def check_local(base,refs,ids):
    errors=[]
    for ref in refs:
        if not ref:continue
        if ref.startswith('#'):
            if unquote(ref[1:]) not in ids:errors.append('missing anchor '+ref)
        elif not ref.startswith(('https://','http://','mailto:')):
            path=(base/unquote(ref.split('#')[0])).resolve()
            if path==OUT/'qa.json':continue
            if not path.is_file():errors.append('missing local file '+str(path))
    return errors

def history_state():
    baseline=json.loads((ROOT/'复审与版本记录/V1.8_拉取基线历史文件哈希_20261031.json').read_text(encoding='utf-8'))
    files=baseline['files']
    drift=[p for p,v in files.items() if not (ROOT.parent/p).is_file() or sha(ROOT.parent/p)!=v['working_tree_sha256']]
    return baseline,drift

def recheck_history_only():
    """Reuse completed page checks only for the identified legacy-history-baseline failure."""
    path=OUT/'qa.json';result=json.loads(path.read_text(encoding='utf-8'))
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    assert result['status']=='FAIL' and len(result['global_errors'])==1
    assert result['global_errors'][0].startswith('historical files changed ')
    assert len(result['reports'])==len(manifest['reports'])==len(CATALOG)
    prior={r['slug']:r for r in result['reports']}
    assert all(r['status']=='PASS' and not r['errors'] for r in prior.values())
    assert manifest['builder_sha256']==sha(ROOT/'11_源码_python生成脚本/build_v18_current.py')
    for row in manifest['reports']:
        assert prior[row['slug']]['pdf_sha256']==row['pdf']['sha256']
        assert {str(source_path(k).relative_to(ROOT)):sha(source_path(k)) for k in row['keys']}==row['source_sha256']
        assert row['identity_sha256']==sha(IDENTITY_PATH)
        assert row['reference_labels_sha256']==sha(REFERENCE_LABELS_PATH)
        for rel,digest in row['asset_sha256'].items(): assert sha(ROOT/rel)==digest
        for ext in ('pdf','md','html'): assert sha(ROOT/row[ext]['path'])==row[ext]['sha256']
    parser=Parser();parser.feed((OUT/'index.html').read_text(encoding='utf-8'))
    assert not check_local(OUT,parser.links,parser.ids)
    baseline,drift=history_state();assert not drift,drift
    maths=calc_checks();assert all(x['pass'] for x in maths)
    result.update(status='PASS_LOCAL_STRUCTURE',global_errors=[],arithmetic=maths,
                  historical_files_checked=len(baseline['files']),historical_files_unchanged=len(baseline['files']),
                  historical_base_commit=baseline['base_commit'],validator_sha256=sha(__file__),
                  validation_reuse_note='All 20 page/structure checks passed before the sole legacy history-list failure. Reused only after rechecking every output/source/asset/identity/builder hash and navigation; replaced pre-V1.7 untracked-preview list with Git-blob-verified clone baseline, then checked all historical working-tree hashes.')
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(result['status'],len(baseline['files']),'historical tracked files unchanged',flush=True)

def main():
    qa_dir=OUT/'qa_visual';qa_dir.mkdir(exist_ok=True)
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'));results=[];errors=[]
    if manifest['builder_sha256']!=sha(ROOT/'11_源码_python生成脚本/build_v18_current.py'):errors.append('builder changed after render')
    if {r['slug'] for r in manifest['reports']}!={x[0] for x in CATALOG}:errors.append('20 edition catalog mismatch')
    for row in manifest['reports']:
        e=[];hp=ROOT/row['html']['path'];ht=hp.read_text(encoding='utf-8');p=Parser();p.feed(ht)
        if ht.count('<nav class="toc">')!=1:e.append('must have one contents navigation')
        if ht.count('<h2>本次更新</h2>')!=1:e.append('must have one update section')
        if len(p.ids)!=len(set(p.ids)):e.append('duplicate ids')
        e+=check_local(OUT,p.links+p.images,p.ids)
        if ht.index('免责声明')>ht.index('本次更新'):e.append('disclaimer out of order')
        expected=prepare_body(row['keys']).strip()
        actual=(ROOT/row['md']['path']).read_text(encoding='utf-8').split('<!-- BODY_START -->',1)[1].strip()
        if actual!=expected:e.append('MD body differs from sources')
        if row.get('identity_sha256')!=sha(IDENTITY_PATH):e.append('publication identity changed after render')
        if row.get('reference_labels_sha256')!=sha(REFERENCE_LABELS_PATH):e.append('reference labels changed after render')
        if '<div class="watermark"' not in ht or '大队长出品' not in ht:e.append('watermark missing in HTML')
        parts=actual.split('<!-- REFERENCES_START -->')
        if len(parts)!=2:e.append('reference section count mismatch')
        else:
            in_body={u for u,_ in reference_entries(parts[0])}
            in_refs={u for u,_ in reference_entries(parts[1])}
            if in_body!=in_refs:e.append('bibliography differs from body references')
            if len(in_body)!=row.get('reference_count'):e.append('reference count mismatch')
            ref_html=ht.split('<section class="references">',1)[1].split('</section>',1)[0]
            if in_body and (ref_html.count('<ol>')!=1 or ref_html.count('<li>')!=len(in_body)):
                e.append('reference list numbering or item count mismatch')
        if {str(source_path(k).relative_to(ROOT)):sha(source_path(k)) for k in row['keys']}!=row['source_sha256']:e.append('source hashes changed')
        for rel,digest in row['asset_sha256'].items():
            if sha(ROOT/rel)!=digest:e.append('asset hash changed '+rel)
        for ext in ['pdf','md','html']:
            if sha(ROOT/row[ext]['path'])!=row[ext]['sha256']:e.append(ext+' hash changed')
        for marker in ['CHANGELOG_START','MONETIZATION_BODY_END','HISTORICAL_START','本篇变更说明','本版逐项修订记录','V1.6.1本篇修订']:
            if marker in actual:e.append('history stack leaked '+marker)
        count_links=0;checked_bookmarks=0;blank=[];bounds=[];toc_checked=set();toc_number_checks=0
        heading_by_anchor={h['anchor']:h for h in row['headings']}
        expected_toc={h['anchor'] for h in row['headings'] if h['level']<=3}
        with fitz.open(ROOT/row['pdf']['path']) as d:
            if len(d)!=row['pages']:e.append('page count mismatch')
            if d.metadata.get('author')!='大队长':e.append('author metadata mismatch')
            texts=[x.get_text() for x in d];alltext='\n'.join(texts)
            for bad in ['\u4ed8\u5f3a','\u90ed\u4e3d\u6885','\u90ed\u5229\u6885','\u90d1\u8bd7\u97f5','南方基金数智科技部','南方基金 · 新程计划','\ufffd']:
                if bad in alltext:e.append('unwanted public text '+bad)
            # A fund manager can still appear as the issuer of a cited public filing.
            # Prohibit author/affiliation leakage, not legitimate source attribution.
            bookmarks=d.get_toc()
            for h in row['headings']:
                candidates=[b for b in bookmarks if norm(b[1])==norm(h['text'])]
                if not any(0<b[2]<=len(d) and norm(h['text']) in norm(texts[b[2]-1]) for b in candidates):e.append('bookmark missing or wrong '+h['text'])
                checked_bookmarks+=1
            for i,page in enumerate(d):
                page.get_pixmap(matrix=fitz.Matrix(.22,.22),alpha=False)
                if '大队长出品' not in texts[i]:e.append(f'watermark missing on PDF page {i+1}')
                for contact in identity()['contact_lines']:
                    if norm(contact) not in norm(texts[i]):e.append(f'contact missing on PDF page {i+1}')
                if len(norm(texts[i]))<30:blank.append(i+1)
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines',[]):
                        for span in line['spans']:
                            x0,y0,x1,y1=span['bbox']
                            if x0<-.8 or y0<-.8 or x1>page.rect.width+.8 or y1>page.rect.height+.8:bounds.append(i+1)
                for link in page.get_links():
                    # WeasyPrint emits named destinations, which PyMuPDF exposes as
                    # LINK_NAMED with a resolved page, not necessarily LINK_GOTO.
                    if link['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED):
                        count_links+=1
                        dest=link.get('page',-1)
                        if not 0<=dest<len(d):
                            e.append('invalid internal PDF link');continue
                        anchor=link.get('nameddest')
                        if anchor in heading_by_anchor:
                            h=heading_by_anchor[anchor]
                            if norm(h['text']) not in norm(texts[dest]):e.append('named destination misses heading '+anchor)
                        # TOC contains the generated physical page number; compare it with the destination.
                        if anchor in expected_toc:
                            label=norm(page.get_textbox(link['from']))
                            n=re.search(r'(\d+)$',label)
                            if n:
                                toc_number_checks+=1;toc_checked.add(anchor)
                                if int(n[1])!=dest+1:e.append(f'TOC page number mismatch on {i+1}: {label}')
            if toc_checked!=expected_toc:e.append('TOC destinations not checked '+str(sorted(expected_toc-toc_checked)))
            if count_links==0:e.append('no internal PDF links checked')
            if bounds:e.append('out of page text '+str(sorted(set(bounds))))
            if blank:e.append('near blank pages '+str(blank))
            sample={0,min(1,len(d)-1),min(3,len(d)-1),len(d)-1}
            if row['slug']=='13_超全景版':
                sample|={b[2]-1 for b in bookmarks if b[0]==1}
                for needle in ['Meta的现金','成本与现金','F01｜','延期','跨境']:
                    for i,t in enumerate(texts):
                        if needle in t:sample.add(i);break
            if row['slug'] in ('13_超全景版','01_主报告','02_事实审计表','15_延迟情景版','16_崩盘剧本','18_AI视频短剧中美市场','19_AI编程市场预测复盘','20_AI应用商业化全景'):
                for i in sorted(sample):d[i].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(qa_dir/f'{row["slug"]}_{i+1:03d}.png')
        results.append({'slug':row['slug'],'pages':row['pages'],'pdf_sha256':row['pdf']['sha256'],'reference_count':row.get('reference_count'),'watermark_pages_checked':row['pages'],'contact_status':identity()['contact_status'],'bookmarks_checked':checked_bookmarks,'internal_pdf_links':count_links,'unique_toc_destinations_checked':len(toc_checked),'toc_page_numbers_checked':toc_number_checks,'errors':e,'status':'PASS' if not e else 'FAIL'})
        print(row['slug'],results[-1]['status'],e[:3],flush=True)
    ip=Parser();ip.feed((OUT/'index.html').read_text(encoding='utf-8'));errors+=check_local(OUT,ip.links,ip.ids)
    baseline,drift=history_state();snapshot=baseline['files']
    if drift:errors.append('historical files changed '+str(drift[:5]))
    maths=calc_checks()
    if not maths or not all(x['pass'] for x in maths):errors.append('arithmetic check failed')
    result={'version':'V1.8','status':'PASS_LOCAL_STRUCTURE' if not errors and all(x['status']=='PASS' for x in results) else 'FAIL','scope':'structural checks and machine arithmetic; separate visual and independent review required','reports':results,'global_errors':errors,'arithmetic':maths,'historical_files_unchanged':len(snapshot)-len(drift),'historical_files_checked':len(snapshot),'native_wps':'NOT_VERIFIED_IN_THIS_SCRIPT'}
    (OUT/'qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(result['status'],errors,flush=True)
    if result['status']=='FAIL':raise SystemExit(1)

if __name__=='__main__':
    if sys.argv[1:]==['--recheck-history-only']: recheck_history_only()
    else: main()


