#!/usr/bin/env python3
"""Artifact checks, exact heading destinations and representative PDF renders."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import fitz
from build_v151_reports import DATE,CATALOG,compose_body,source_digests,asset_digests,audit_counts
import edition_numbering_v151 as numbering

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'V1.5.1正文修订版'

class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.images=[];self.headings={};self.heading=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='img':self.images.append(a.get('src',''))
        if re.fullmatch('h[1-6]',tag) and 'id' in a:
            self.heading=a['id'];self.headings[self.heading]=''
    def handle_data(self,data):
        if self.heading:self.headings[self.heading]+=data
    def handle_endtag(self,tag):
        if re.fullmatch('h[1-6]',tag):self.heading=None

def norm(s):return re.sub(r'\s+','',s)

def main():
    p=argparse.ArgumentParser();p.add_argument('--render-dir',required=True);args=p.parse_args()
    render=Path(args.render_dir);render.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((OUT/'manifest.json').read_text());results=[];global_errors=[]
    if manifest.get('date')!=DATE:global_errors.append('manifest date not equal current build date')
    if manifest.get('audit_counts')!=audit_counts():global_errors.append('audit counts not equal source')
    expected={x[0] for x in CATALOG};actual=[x['slug'] for x in manifest['reports']]
    if len(actual)!=len(expected) or set(actual)!=expected:global_errors.append('17-edition catalog incomplete or duplicated')
    builder=ROOT/'11_源码_python生成脚本/build_v151_reports.py'
    if manifest.get('builder_sha256')!=hashlib.sha256(builder.read_bytes()).hexdigest():global_errors.append('builder changed after render')
    if manifest.get('numbering_engine_sha256')!=hashlib.sha256(Path(numbering.__file__).read_bytes()).hexdigest():global_errors.append('numbering engine changed after render')
    index_parser=Parser();index_parser.feed((OUT/'index.html').read_text())
    for link in index_parser.links:
        if not link.startswith(('https://','http://','#')) and not (OUT/unquote(link.split('#')[0])).resolve().is_file():
            global_errors.append('index target missing '+link)
    for rel in ['README.md','00_使用说明/README_大队长_全量存档说明.md','00_使用说明/当前文件总索引_2026-10-09.md']:
        page_path=ROOT/rel
        for link in re.findall(r'\]\(([^)]+)\)',page_path.read_text()):
            link=link.strip('<>')
            if not link.startswith(('https://','http://','#')) and not (page_path.parent/unquote(link.split('#')[0])).resolve().is_file():
                global_errors.append('reading entry target missing '+rel+' '+link)
    reading_index=(ROOT/'00_使用说明/当前文件总索引_2026-10-09.md').read_text()
    index_pages={slug:int(pages) for pages,slug in re.findall(r'^\|[^|\n]+\|\s*(\d+)\s*\|.*?/([^/]+)\.pdf>',reading_index,re.M)}
    if index_pages!={r['slug']:r['pages'] for r in manifest['reports']}:
        global_errors.append('reading index page counts differ from manifest')
    for item in manifest['reports']:
        errors=[];parser=Parser();html_text=(ROOT/item['html']['path']).read_text();parser.feed(html_text)
        if html_text.count('<section class="toc">')!=1:errors.append('expected exactly one actual contents section')
        disclaimer=html_text.find('免责声明与阅读边界')
        revision=html_text.find('本版修订说明')
        if disclaimer<0 or revision<disclaimer:errors.append('disclaimer must precede revision notice')
        if len(parser.ids)!=len(set(parser.ids)):errors.append('duplicate HTML ids')
        for link in parser.links:
            if link.startswith('#') and unquote(link[1:]) not in parser.ids:errors.append('broken anchor '+link)
            elif link and not link.startswith(('https://','http://','#')):
                target=(OUT/unquote(link.split('#')[0])).resolve()
                if not target.is_file():errors.append('missing local reference '+link)
        for img in parser.images:
            if not (OUT/unquote(img)).resolve().is_file():errors.append('missing image '+img)
        if item.get('source_sha256')!=source_digests(item['sources']):errors.append('source changed after render')
        if item.get('asset_sha256')!=asset_digests(item['sources']):errors.append('image or font changed after render')
        if item.get('numbering',{})!=numbering.metadata(item['sources']):errors.append('numbering policy not equal current edition policy')
        exported=(ROOT/item['md']['path']).read_text().split('<!-- BODY_START -->',1)[1].strip()
        expected_body=compose_body(item['sources']).strip()
        if exported!=expected_body:errors.append('exported body does not equal current thematic source')
        for kind in ['pdf','md','html']:
            path=ROOT/item[kind]['path']
            if hashlib.sha256(path.read_bytes()).hexdigest()!=item[kind]['sha256']:errors.append(kind+' hash mismatch')
        with fitz.open(ROOT/item['pdf']['path']) as doc:
            if doc.metadata.get('author')!='大队长':errors.append('unexpected public PDF author')
            if len(doc)!=item['pages']:errors.append('page count differs from manifest')
            texts=[page.get_text() for page in doc]
            alltext='\n'.join(texts)
            if DATE not in texts[0]:errors.append('cover or compact header date not current')
            for forbidden in ['\ufffd','\u4ed8\u5f3a','\u90ed\u4e3d\u6885','\u90ed\u5229\u6885','\u90d1\u8bd7\u97f5','南方基金','原投递件','HISTORICAL_START','[[CHART:']:
                if forbidden in alltext:errors.append('unwanted text '+forbidden)
            bounds=0
            for page in doc:
                for b in page.get_text('dict')['blocks']:
                    for line in b.get('lines',[]):
                        for span in line['spans']:
                            x0,y0,x1,y1=span['bbox']
                            if x0 < -1 or y0 < -1 or x1>page.rect.width+1 or y1>page.rect.height+1:bounds+=1
            if bounds:errors.append(f'out of bounds spans {bounds}')
            toc=doc.get_toc(simple=False);checked=0
            # PDF outline levels may include front matter; every HTML heading must
            # have a matching PDF outline title and actual target-page heading.
            for h in item['headings']:
                matching=[row for row in toc if norm(row[1])==norm(h['text'])]
                if not matching:
                    errors.append('missing PDF bookmark '+h['text']);continue
                valid=False
                for row in matching:
                    n=row[2]-1
                    if 0<=n<len(doc) and norm(h['text']) in norm(texts[n]):valid=True;break
                if not valid:errors.append('wrong PDF destination '+h['text'])
                checked+=1
            internal=0
            for page in doc:
                for link in page.get_links():
                    if link['kind'] in (fitz.LINK_GOTO,fitz.LINK_NAMED) and 'page' in link:
                        internal+=1
                        if not 0<=link['page']<len(doc):errors.append('invalid PDF internal page')
                        dest=link.get('nameddest')
                        if dest:
                            expected=parser.headings.get(dest)
                            if expected is None:errors.append('unknown named destination '+dest)
                            elif norm(expected) not in norm(texts[link['page']]):errors.append('named link wrong heading '+dest)
            if any(h['level']<=3 for h in item['headings']) and internal==0:errors.append('PDF contents links absent')
            samples={0,min(1,len(doc)-1),len(doc)-1}
            # Render beginning of body, topic tables/figures and a middle page.
            main_title=item['headings'][0]['text']
            for row in toc:
                if norm(row[1])==norm(main_title):samples.add(row[2]-1);break
            samples.add(len(doc)//2)
            for n in sorted(samples):
                doc[n].get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(render/f'{item["slug"]}_p{n+1:03d}.png')
            results.append(dict(slug=item['slug'],pages=len(doc),headings_checked=checked,internal_links=internal,errors=errors,rendered_pages=[n+1 for n in sorted(samples)]))
    report={'status':'PASS_STRUCTURAL' if not global_errors and not any(x['errors'] for x in results) else 'FAIL','checked_at_utc':datetime.now(timezone.utc).isoformat(),'manifest_sha256':hashlib.sha256((OUT/'manifest.json').read_bytes()).hexdigest(),'qa_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'render_dir':str(render.resolve()),'global_errors':global_errors,'limitations':['Structural tests do not independently verify all facts.','Rendered images require human/agent visual inspection.','No external publication or Git push.'],'reports':results}
    (OUT/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
