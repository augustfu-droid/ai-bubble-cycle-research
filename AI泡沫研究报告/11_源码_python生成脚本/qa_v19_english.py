#!/usr/bin/env python3
"""Check final English artifact structure, links, headings, pages and provenance."""
from pathlib import Path
from collections import Counter
import json,re,hashlib
from urllib.parse import unquote
import fitz
import build_v19_english as b
import build_v19_current as zh
from assets_v19_english import NAMES
import markdown
from qa_v19_current import Parser

def norm(s):return re.sub(r'\s+','',s).replace('\u00ad','')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    out=b.OUT;root=b.ROOT
    mf=json.loads((out/'manifest.json').read_text(encoding='utf-8'));spec=b.manifest();errors=[]
    assert not mf['preview']
    for key,path in [('builder_sha256',Path(b.__file__)),('shared_builder_sha256',Path(zh.__file__)),
                     ('text_protection_sha256',root/'11_源码_python生成脚本/numbering_v19.py'),
                     ('front_matter_sha256',b.SOURCE/'front_matter.md'),('reference_labels_sha256',b.SOURCE/'reference_labels.json')]:
        if mf[key]!=sha(path):errors.append('Changed after build: '+key)
    for name,digest in mf['source_parts'].items():
        if sha(b.SOURCE/'parts'/name)!=digest:errors.append('Translation changed after build: '+name)
    for name,digest in mf['assets'].items():
        if sha(out/'assets'/name)!=digest:errors.append('Figure changed after build: '+name)
    for ext,rec in mf['outputs'].items():
        if sha(rec['path'])!=rec['sha256']:errors.append('Output hash differs: '+ext)
    # Every previously delivered Chinese file must remain byte-identical.
    original_manifest=root.parent/'V1.9-publication-files.json'
    if sha(original_manifest)!=spec['chinese_publication_manifest_sha256']:errors.append('Chinese publication manifest changed')
    prior=json.loads(original_manifest.read_text(encoding='utf-8'))
    drift=[r['path'] for r in prior['files'] if sha(root.parent/r['path'])!=r['sha256']]
    if drift:errors.append('Chinese publication drift: '+str(drift[:10]))
    if sha(spec['chinese_pdf'])!=spec['chinese_pdf_sha256']:errors.append('Chinese full PDF changed')
    body=b.translated_body(spec['units']);full=body+b.bibliography(body)
    actual=Path(mf['outputs']['md']['path']).read_text(encoding='utf-8').split('<!-- BODY_START -->',1)[1].strip()
    if actual!=full.strip():errors.append('Markdown differs from frozen translation parts')
    en_urls={u for u,_ in zh.reference_entries(body)}
    zh_urls={u for u,_ in zh.reference_entries(zh.publication_body(zh.FULL))}
    if en_urls!=zh_urls:errors.append('English/Chinese reference URL sets differ')
    if len(en_urls)!=342 or mf['reference_count']!=342:errors.append('Expected 342 unique reference URLs')
    if {u for u,_ in zh.reference_entries(b.bibliography(body))}!=en_urls:errors.append('Bibliography differs from body references')
    chapters=[int(n) for n in re.findall(r'^## Chapter (\d+):',body,re.M)]
    appendices=re.findall(r'^## Appendix ([A-F])',body,re.M)
    if chapters!=list(range(1,14)):errors.append('Chapter sequence must be 1-13')
    if appendices!=list('ABCDEF'):errors.append('Appendix sequence must be A-F')
    ht=Path(mf['outputs']['html']['path']).read_text(encoding='utf-8')
    p=Parser();p.feed(ht)
    if len(p.ids)!=len(set(p.ids)):errors.append('Duplicate HTML anchors')
    for ref in p.links+p.images:
        if not ref:continue
        if ref.startswith('#'):
            if unquote(ref[1:]) not in p.ids:errors.append('Missing anchor: '+ref)
        elif not ref.startswith(('http://','https://','mailto:')):
            if not (out/unquote(ref.split('#')[0])).resolve().is_file():errors.append('Missing local target: '+ref)
    original_images=Parser();original_images.feed(markdown.markdown(zh.publication_body(zh.FULL),extensions=['tables']))
    expected_images=['assets/'+NAMES[Path(src).name] for src in original_images.images]
    if Counter(p.images)!=Counter(expected_images):errors.append('Translated figure placement inventory differs from Chinese source')
    if len(set(p.images))!=8:errors.append(f'Expected 8 unique translated figures, got {len(set(p.images))}')
    heading_by_anchor={h['anchor']:h for h in mf['headings']}
    expected_toc={h['anchor'] for h in mf['headings'] if h['level']<=3}
    toc_seen=set();toc_numbers=0;internal_links=0;bounds=[];blank=[];samples={0,1,2};sample_reasons={}
    with fitz.open(mf['outputs']['pdf']['path']) as doc:
        if len(doc)!=mf['pages']:errors.append('PDF page count mismatch')
        if doc.metadata.get('author')!='Daduizhang':errors.append('PDF author metadata mismatch')
        texts=[page.get_text() for page in doc];bookmarks=doc.get_toc()
        alltext='\n'.join(texts)
        if '\ufffd' in alltext:errors.append('Replacement characters in PDF')
        for bad in ['付强','郭丽梅','郭利梅','郑诗韵','南方基金数智科技部']:
            if bad in alltext:errors.append('Unexpected private identity: '+bad)
        for h in mf['headings']:
            options=[row for row in bookmarks if norm(row[1])==norm(h['text'])]
            if not any(0<r[2]<=len(doc) and norm(h['text']) in norm(texts[r[2]-1]) for r in options):
                errors.append('Missing/misdirected bookmark: '+h['text'])
        for i,page in enumerate(doc):
            page.get_pixmap(matrix=fitz.Matrix(.2,.2),alpha=False)
            if 'DADUIZHANG' not in texts[i]:errors.append(f'Missing watermark on page {i+1}')
            if b.EMAIL not in texts[i]:errors.append(f'Missing contact on page {i+1}')
            if len(norm(texts[i]))<60:blank.append(i+1)
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        x0,y0,x1,y1=span['bbox']
                        if x0<-.8 or y0<-.8 or x1>page.rect.width+.8 or y1>page.rect.height+.8:
                            bounds.append({'page':i+1,'text':span['text']})
            for link in page.get_links():
                if link['kind'] not in (fitz.LINK_GOTO,fitz.LINK_NAMED):continue
                internal_links+=1;dest=link.get('page',-1)
                if not 0<=dest<len(doc):errors.append('Invalid internal PDF destination');continue
                anchor=link.get('nameddest')
                if anchor in heading_by_anchor and norm(heading_by_anchor[anchor]['text']) not in norm(texts[dest]):
                    errors.append('PDF destination misses heading: '+anchor)
                if anchor in expected_toc:
                    label=norm(page.get_textbox(link['from']));n=re.search(r'(\d+)$',label)
                    if n:
                        toc_seen.add(anchor);toc_numbers+=1
                        if int(n[1])!=dest+1:errors.append(f'Wrong TOC page: {label}')
        if toc_seen!=expected_toc:errors.append('Unverified TOC destinations: '+str(sorted(expected_toc-toc_seen)))
        if bounds:errors.append('Text outside page: '+str(bounds[:10]))
        if blank:errors.append('Near-blank pages: '+str(blank))
        # Current-PDF samples for actual visual review, not an automatic visual PASS.
        for row in bookmarks:
            if row[1].startswith(('Chapter ','Appendix ','Reference index','4.12 ','5.11 ','5.12 ','5.13 ')):
                samples.add(row[2]-1);sample_reasons.setdefault(row[2],[]).append(row[1])
            if row[1].startswith(('4.12 ','5.11 ','5.12 ','5.13 ')) and row[2]<len(doc):samples.add(row[2])
        first_body=next(row[2]-1 for row in bookmarks if row[1].startswith('Research Overview')) if any(row[1].startswith('Research Overview') for row in bookmarks) else next(row[2]-1 for row in bookmarks if row[1].startswith('Chapter 1:'))
        samples.update(range(3,first_body))
        figure_phrases=['Optical modules: half-year','APLD: revenue growth','CoreWeave: USD 4.2B','Oracle FY27Q1: read growth','Subtract the realized half','Micron: strong realized cash','Meta: positive operating cash','TSMC: quarterly revenue rises']
        figure_pages={}
        for phrase in figure_phrases:
            matches=[i for i,t in enumerate(texts) if norm(phrase) in norm(t)]
            if not matches:errors.append('Translated figure lettering missing from PDF: '+phrase)
            else:figure_pages[phrase]=matches[0]+1;samples.add(matches[0]);sample_reasons.setdefault(matches[0]+1,[]).append('Translated figure: '+phrase)
        samples.add(len(doc)-1)
        dest=out/'qa_visual';dest.mkdir(exist_ok=True)
        rendered=[]
        for i in sorted(samples):
            path=dest/f'page_{i+1:03d}.png';doc[i].get_pixmap(matrix=fitz.Matrix(1.35,1.35),alpha=False).save(path)
            rendered.append({'page':i+1,'image':str(path),'reasons':sample_reasons.get(i+1,[])})
    result={'status':'PASS_ARTIFACT_STRUCTURE' if not errors else 'FAIL','scope':'Machine artifact, page, link, chapter, source-protection and provenance checks. Separate semantic and actual visual reviews are required.',
            'pdf_sha256':mf['outputs']['pdf']['sha256'],'pages':mf['pages'],'reference_count':len(en_urls),'chapters':chapters,'appendices':appendices,
            'bookmarks_checked':len(mf['headings']),'toc_destinations_checked':len(toc_seen),'toc_page_numbers_checked':toc_numbers,'internal_pdf_links':internal_links,
            'figures':figure_pages,'figure_placements_checked':len(p.images),'unique_figures_checked':len(set(p.images)),'chinese_publication_files_unchanged':len(prior['files'])-len(drift),'validator_sha256':sha(Path(__file__)),
            'errors':errors,'visual_samples':rendered}
    (out/'qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','pages','reference_count','bookmarks_checked','toc_destinations_checked','chinese_publication_files_unchanged','errors']},ensure_ascii=False))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
