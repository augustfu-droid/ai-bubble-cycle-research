#!/usr/bin/env python3
"""Build the full English translation without altering the Chinese publication."""
from __future__ import annotations
import argparse,hashlib,html,json,re
from pathlib import Path
from urllib.parse import urlsplit
import fitz,markdown
import build_v19_current as zh
from assets_v19_english import NAMES
from numbering_v19 import _protect, _restore

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'10_源码_markdown/V1.9_English_20261031'
OUT=ROOT/'V1.9_English_Full_Report'
STEM='AI_Cycles_and_Bubble_Full_Report_EN_2026-10-31'
TITLE='AI Cycles and the Bubble: Full Research Report'
AUTHOR='Daduizhang'
EMAIL='fqsx@mail.ustc.edu.cn'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def manifest():return json.loads((SOURCE/'translation-manifest.json').read_text(encoding='utf-8'))

def translated_body(units):
    pieces=[]
    for unit in units:
        original=SOURCE/'translation_inputs'/unit['file']
        assert sha(original)==unit['source_sha256'],f'Frozen input changed: {original}'
        path=SOURCE/'parts'/unit['file']
        text=path.read_text(encoding='utf-8')
        assert len(text.splitlines())==unit['source_lines'],f'Incomplete/unaligned translation: {path}'
        pieces.append(text.strip())
    body='\n\n'.join(pieces)
    for old,new in NAMES.items():body=body.replace('(assets/'+old+')','(assets/'+new+')')
    # Normalize visible typography while preserving URLs, code and math minus.
    protected_text,protected=_protect(body,'__english_translation__')
    protected_text=protected_text.replace('\u2011','-').replace('\u2010','-').replace('\u2013','-').replace('\u2014',' - ')
    body=_restore(protected_text,protected)
    return body

def bibliography(body):
    refs=zh.reference_entries(body)
    labels=json.loads((SOURCE/'reference_labels.json').read_text(encoding='utf-8'))
    rows=[]
    for i,(url,label) in enumerate(refs,1):
        meta=labels.get(url,{})
        title=meta.get('title',label).replace('[','(').replace(']',')') or urlsplit(url).netloc
        note=meta.get('note','')
        host=urlsplit(url).netloc
        if host in ('www.marketscreener.com','www.globenewswire.com','www.businesswire.com'):
            note='News-distribution or republication platform; not an additional independent item of operating evidence. '+note
        rows.append(f'{i}. [{title}]({url}) | {host}'+('  '+note if note else '')+f'\n\n    <span class="ref-url">{html.escape(url)}</span>')
    return '\n\n<!-- REFERENCES_START -->\n\n## Reference index\n\n'+(
        f'This edition contains {len(refs)} references after exact-URL deduplication. The links beside the relevant passages are retained, and full URLs are listed below in order of first citation for use in print. Titles use the checked company, reporting period and document type, or the source shorthand used in the text; they are not invariably official titles. The period, verification limits and access restrictions stated in the relevant passages govern. This list does not mean that every historical source was obtained anew during this research round.\n\n')+'\n\n'.join(rows)

def css():
    regular=(ROOT/'11_源码_python生成脚本/fonts/NotoSansSC-Regular.ttf').as_uri()
    bold=(ROOT/'11_源码_python生成脚本/fonts/NotoSansSC-Bold.ttf').as_uri()
    return f'''@font-face{{font-family:Noto;src:url("{regular}")}}@font-face{{font-family:Noto;src:url("{bold}");font-weight:700}}
@page{{size:A4;margin:19mm 18mm 19mm;@top-left{{content:"Daduizhang | AI Cycles and the Bubble";font:7pt Noto;color:#627b8e}}@top-right{{content:"V1.9 English | 2026-10-31";font:7pt Noto;color:#627b8e}}@bottom-left{{content:"Independent research | Daduizhang";font:6.6pt Noto;color:#627b8e}}@bottom-center{{content:"{EMAIL}";font:6.6pt Noto;color:#627b8e}}@bottom-right{{content:counter(page)" / "counter(pages);font:7pt Noto;color:#627b8e}}}}
@page cover{{margin:0;@top-left{{content:none}}@top-right{{content:none}}@bottom-left{{content:none}}@bottom-center{{content:none}}@bottom-right{{content:none}}}}
*{{box-sizing:border-box}}body{{font:10.3pt/1.58 Noto,sans-serif;color:#273e4d;margin:0}}
.cover{{page:cover;height:296mm;background:#f8fbfd;padding:32mm 24mm;position:relative;break-after:page}}
.cover .rule{{height:3mm;width:45mm;background:#92bdd4;margin-bottom:16mm}}
.cover h1{{font-size:30pt;line-height:1.36;margin:25mm 0 10mm;color:#315e7c;max-width:155mm}}
.cover .subtitle{{font-size:13pt;line-height:1.7;color:#607b8e}}
.cover .edition{{font-size:12pt;margin-top:22mm}}
.cover .foot{{position:absolute;left:24mm;right:24mm;bottom:24mm;border-top:1pt solid #c7dce8;padding-top:6mm;font-size:9pt;color:#647f91}}
.watermark{{position:fixed;top:40%;left:0;right:0;text-align:center;transform:rotate(-28deg);font:700 49pt Noto;color:#8ab1c8;opacity:.055;z-index:10;pointer-events:none}}
.front,.updates{{break-after:page;font-size:9.7pt;line-height:1.55}}.front p,.updates p{{margin:7pt 0}}.updates li{{margin:6pt 0;break-inside:avoid}}
.toc{{break-after:page}}.toc>p{{font-size:9pt;line-height:1.5}}
.toc a{{display:block;position:relative;color:#355f7b;text-decoration:none;border-bottom:.4pt dotted #bfd3df;padding:4pt 3.4em 4pt 0;font-size:9pt;line-height:1.5;break-inside:avoid}}
.toc a:after{{content:target-counter(attr(href url),page);position:absolute;right:0;bottom:4pt}}
.toc .l2{{font-weight:700;margin-top:5pt}}.toc .l3{{padding-left:12pt}}
h1,h2,h3,h4,h5{{color:#315e7c;line-height:1.35;break-after:avoid}}h1{{font-size:23pt}}h2{{font-size:16pt;border-bottom:.8pt solid #9dbed2;padding-bottom:6pt;margin:20pt 0 11pt}}h3{{font-size:12.3pt;margin:16pt 0 8pt}}h4{{font-size:10.8pt;margin:13pt 0 6pt}}h5{{font-size:10.3pt}}
main h2{{bookmark-level:1}}main h3{{bookmark-level:2}}main h4{{bookmark-level:3}}main h5{{bookmark-level:4}}
p{{margin:8pt 0;orphans:3;widows:3}}a{{color:#386b8c;text-decoration:none;overflow-wrap:anywhere}}
blockquote{{border-left:3pt solid #a1c5db;background:#f0f7fb;padding:8pt 12pt;margin:12pt 0}}
table{{border-collapse:collapse;width:100%;table-layout:auto;font-size:8.1pt;line-height:1.45;margin:12pt 0 16pt}}
thead{{display:table-header-group}}tr{{break-inside:avoid}}td,th{{border:.5pt solid #c9dce7;padding:5pt 6pt;text-align:left;vertical-align:top;overflow-wrap:anywhere}}th{{background:#e0eef7;color:#315e7c}}th:first-child{{min-width:75pt}}tr:nth-child(even) td{{background:#f7fafc}}
ul,ol{{padding-left:1.5em;margin:10pt 0}}li{{margin:6pt 0}}img{{display:block;width:100%;max-height:215mm;object-fit:contain;margin:14pt auto}}
code{{font-family:Noto,sans-serif;background:#f0f5f8;font-size:.94em;overflow-wrap:anywhere}}pre{{white-space:pre-wrap}}hr{{border:0;border-top:.6pt solid #c9dce7;margin:15pt 0}}
.references{{break-before:page}}.references p{{font-size:9pt}}.references ol{{font-size:8.5pt;line-height:1.5}}.references li{{margin:7pt 0;break-inside:avoid}}.references li p{{margin:3pt 0;font-size:8.5pt}}.ref-url{{font-size:7.4pt;color:#667f90;overflow-wrap:anywhere;word-break:break-all}}
@media screen{{body{{max-width:1120px;margin:auto;padding:22px}}.cover{{height:auto;min-height:80vh;padding:42px 32px}}.cover h1{{margin-top:50px}}.cover .foot{{position:static;margin-top:45px}}.toc a:after{{content:none}}.front,.updates,.toc,main{{padding:12px}}table{{display:block;overflow:auto}}.watermark{{font-size:clamp(28px,5vw,55px)}}}}
'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',nargs='*');args=parser.parse_args()
    spec=manifest();units=spec['units']
    preview=args.preview is not None
    if preview:units=[u for u in units if u['file'] in args.preview]
    assert units
    body=translated_body(units)
    refs=zh.reference_entries(body)
    if not preview:
        assert len(units)==20
        assert [int(n) for n in re.findall(r'^## Chapter (\d+):',body,re.M)]==list(range(1,14))
        assert re.findall(r'^## Appendix ([A-F])',body,re.M)==list('ABCDEF')
        assert {url for url,_ in refs}=={url for url,_ in zh.reference_entries(zh.publication_body(zh.FULL))}
    body+=bibliography(body)
    front=(SOURCE/'front_matter.md').read_text(encoding='utf-8')
    first,updates=front.split('<!-- UPDATES_START -->')
    exts=['tables','fenced_code','footnotes','attr_list','sane_lists']
    rendered,headings=zh.tag_headings(markdown.markdown(body,extensions=exts))
    rendered=rendered.replace('<!-- REFERENCES_START -->','<section class="references">')+'</section>'
    toc='<nav class="toc"><h1>Contents</h1><p>Chapter and subsection numbers match the complete Chinese report. Page numbers and links refer to this English edition.</p>'
    toc+=''.join(f'<a class="l{h["level"]}" href="#{h["anchor"]}">{html.escape(h["text"])}</a>' for h in headings if h['level']<=3)+'</nav>'
    subtitle='Earnings, capital recovery, microdramas, AI coding and the economics of adoption'
    if preview:subtitle='LAYOUT PROOF - selected translated chapters; not the complete report'
    contact=f'Contact: <a href="mailto:{EMAIL}">{EMAIL}</a>'
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="author" content="{AUTHOR}"><title>{TITLE}</title><style>{css()}</style></head><body><div class="watermark">DADUIZHANG</div><section class="cover"><div class="rule"></div><div>DADUIZHANG | INDEPENDENT RESEARCH</div><h1>AI Cycles and<br>the Bubble</h1><p class="subtitle">{subtitle}</p><p class="edition">Full research report<br>V1.9 | English edition<br>Research cutoff: 31 October 2026, Beijing time</p><div class="foot">A full translation of the corrected Chinese V1.9 report.<br>Reporting periods, assumptions and evidence limitations are preserved.<br>{contact}</div></section><section class="front">{markdown.markdown(first,extensions=exts)}</section><section class="updates">{markdown.markdown(updates,extensions=exts)}</section>{toc}<main>{rendered}</main></body></html>'''
    dest=ROOT.parent/'tmp/english_preview' if preview else OUT
    dest.mkdir(parents=True,exist_ok=True)
    if preview:page=page.replace('src="assets/','src="'+(OUT/'assets').as_uri()+'/')
    stem='layout_proof' if preview else STEM
    md=dest/(stem+'.md');hp=dest/(stem+'.html');pdf=dest/(stem+'.pdf')
    md.write_text(f'# {TITLE}\n\nDaduizhang | V1.9 English | 2026-10-31\n\n'+front+'\n\n<!-- BODY_START -->\n\n'+body+'\n',encoding='utf-8')
    hp.write_text(page,encoding='utf-8');zh.render_pdf(hp,pdf)
    with fitz.open(pdf) as doc:pages=len(doc)
    record={'version':'V1.9 English','scope':spec['translation_scope'],'preview':preview,'pages':pages,
            'source_chinese_pdf_sha256':spec['chinese_pdf_sha256'],'reference_count':len(refs),'headings':headings,
            'source_parts':{u['file']:sha(SOURCE/'parts'/u['file']) for u in units},
            'builder_sha256':sha(__file__),'shared_builder_sha256':sha(zh.__file__),'text_protection_sha256':sha(ROOT/'11_源码_python生成脚本/numbering_v19.py'),
            'front_matter_sha256':sha(SOURCE/'front_matter.md'),'reference_labels_sha256':sha(SOURCE/'reference_labels.json'),
            'assets':{name:sha(OUT/'assets'/name) for name in NAMES.values()},
            'outputs':{p.suffix[1:]:{'path':str(p),'sha256':sha(p)} for p in (md,hp,pdf)}}
    (dest/'manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not preview:
        index=f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{TITLE}</title><style>body{{font:18px/1.7 system-ui;max-width:900px;margin:50px auto;padding:24px;color:#28475e}}a{{color:#356e93}}</style><h1>{TITLE}</h1><p>Daduizhang | V1.9 English | Research cutoff: 31 October 2026</p><p>Complete translation: 13 chapters, Appendices A-F, 8 translated figures and {len(refs)} references after exact-URL deduplication.</p><p><a href="{stem}.pdf">Read the PDF ({pages} pages)</a> | <a href="{stem}.html">Read online</a> | <a href="{stem}.md">Editable Markdown</a></p><p><a href="../V1.9现行正文版/13_超全景版.pdf">Chinese original (209 pages)</a></p><p>Evidence periods, assumptions and uncertainties follow the Chinese source. Translation is not a new research update.</p></html>'''
        (dest/'index.html').write_text(index,encoding='utf-8')
    print(json.dumps({'preview':preview,'pages':pages,'references':len(refs),'pdf':str(pdf)},ensure_ascii=False))

if __name__=='__main__':main()
