#!/usr/bin/env python3
"""Build current-body editions from common prose; no original-PDF page copying."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import fitz
import markdown
from weasyprint import HTML

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'10_源码_markdown/V1.7_现行正文_20261027'
OUT=ROOT/'V1.7现行正文版'
DATE='2026-10-27'
IDENTITY_PATH=SRC/'出版标识.json'
REFERENCE_LABELS_PATH=SRC/'参考资料标签.json'

def identity():
    return json.loads(IDENTITY_PATH.read_text())

def contact_markup():
    text=html.escape(' · '.join(identity()['contact_lines']))
    return re.sub(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',lambda m:f'<a href="mailto:{m[0]}">{m[0]}</a>',text)

class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__();self.refs={};self.url=None;self.label=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            ref=dict(attrs).get('href','')
            if ref.startswith(('https://','http://')):self.url=ref;self.label=[]
    def handle_data(self,data):
        if self.url:self.label.append(data)
    def handle_endtag(self,tag):
        if tag=='a' and self.url:
            label=' '.join(''.join(self.label).split())
            if self.url not in self.refs or len(label)>len(self.refs[self.url]):self.refs[self.url]=label
            self.url=None;self.label=[]

def reference_entries(body):
    parser=ReferenceParser();parser.feed(markdown.markdown(body,extensions=['tables','footnotes']))
    return list(parser.refs.items())

def bibliography(body):
    refs=reference_entries(body)
    metadata=json.loads(REFERENCE_LABELS_PATH.read_text())
    preface=f'本册按URL去重收录{len(refs)}项参考资料，保留正文中的就近链接，下面按首次引用顺序集中列出完整网址，便于打印后追溯。名称采用已核对的公司、报告期与文档类型或正文来源简称，并非一律为官方原标题；资料的期间、核验程度和访问限制以对应段落为准，不表示全部旧引文都在本轮重新取得原件。'
    rows=[]
    for i,(url,label) in enumerate(refs,1):
        meta=metadata.get(url,{})
        safe=meta.get('title',label).replace('[','（').replace(']','）') or urlsplit(url).netloc
        host=urlsplit(url).netloc
        note=meta.get('note','')
        if host in ('www.marketscreener.com','www.globenewswire.com','www.businesswire.com'):
            note=('新闻分发或转载平台，不能视为新增独立经营证据。'+note)
        rows.append(f'{i}. [{safe}]({url}) · {host}'+('  '+note if note else '')+f'\n\n    <span class="ref-url">{html.escape(url)}</span>')
    if not rows:
        preface='本册为阅读导引，未单列外部引文。具体论据、来源及核验限制请见[超全景现行正文](13_超全景版.html)。'
    return '\n\n<!-- REFERENCES_START -->\n\n## 参考资料索引\n\n'+preface+'\n\n'+'\n\n'.join(rows)
PARTS={
 'profit':'01_利润真实性拆解.md','circular':'02_循环投资网络.md',
 'monetization':'03_AI变现与编程TAM.md','agi':'04_AGI与国际格局.md',
 'china':'06_中国投资者传导.md','valuation':'07_公司分化与估值.md',
 'conclusion':'08_风险与综合结论.md','framework':'09_框架与页岩油类比.md',
 'shale':'09_框架与页岩油类比.md','fusion':'10_聚变能源与资本回收.md',
 'alphabet':'11_Alphabet融资案例.md','audit':'13_事实审计处置表.md',
 'crash':'14_风险传导剧本.md','delay':'15_延迟与消化情景.md',
 'crossborder':'16_跨境渠道与工具边界.md','postscript':'17_研究结语.md'}
CORE=['profit','circular','monetization','agi','china','valuation','conclusion']
FULL=['short:institution']+CORE+['crash','delay','framework','crossborder','shale','alphabet','audit','fusion','postscript']
CATALOG=[
 ('01_主报告','AI周期与泡沫深度研究报告',['short:institution']+CORE,'经营、资本回收与金融条件的现行判断'),
 ('02_事实审计表','关键事实与证据边界',['audit'],'当前证据、沿用基线、算式与待核事项'),
 ('03_利润真实性拆解','利润真实性拆解',['profit'],'主营、重估、现金与资本投入分开核对'),
 ('04_循环投资网络','循环投资网络',['circular'],'沿法律实体与合同追踪资金和风险承担'),
 ('05_AI变现与编程TAM','AI变现与编程市场',['monetization'],'从真实收费到可持续经营回报'),
 ('06_AGI与国际格局','AGI与国际格局',['agi'],'能力、部署、能源和政策约束'),
 ('07_机构简版','AI周期与泡沫 · 机构简版',['short:institution'],'当前判断与公司研究入口'),
 ('08_公开精简版','AI周期与泡沫 · 公开选编',['short:public','profit','monetization','agi','china'],'按利润、商业化和产业约束阅读'),
 ('09_雪球公开版','AI周期与泡沫 · 投资者版',['short:snowball','valuation','china'],'把公司增长与估值要求放在一起'),
 ('10_摘要版','AI周期与泡沫 · 摘要',['short:summary'],'最重要的判断、证据和未知'),
 ('11_执行简版','AI周期与泡沫 · 研究执行清单',['short:execution'],'执行核验与模型更新，不是交易指令'),
 ('12_全景版','AI周期与泡沫 · 全景正文',['short:institution']+CORE+['crash','delay','framework','shale','alphabet','fusion'],'主线研究、两类情景与专题论证'),
 ('13_超全景版','AI周期与泡沫 · 超全景现行正文',FULL,'覆盖原339页研究主题，合并重复，不嵌入旧正文'),
 ('14_完整合集','AI周期与泡沫 · 核心专题合集',CORE+['framework','shale','alphabet','fusion','audit'],'核心研究与专题、当前事实核对合编'),
 ('15_延迟情景版','AI投资的延迟与消化',['delay','circular','framework','shale','fusion'],'区分延期放大资金压力与有序消化投资'),
 ('16_崩盘剧本','AI风险传导剧本',['crash','conclusion'],'触发条件、报表传导、反证和中止条件'),
 ('17_发布引流稿','AI周期与泡沫 · 阅读导引',['short:intro'],'从产业叙事进入公司现金与估值')]

CHANGES=[
 ('structure','把历史原页与校注叠加改为现行正文，原339页中的独有主题保留，重复分册合并；本册不嵌入旧版。'),
 ('profit','利润篇接入台积电、ASML、Meta三季报与中国存储数据，统一主营、投资重估、营运资本和现金建设口径。'),
 ('circular','融资和变现篇接入Anthropic公开S-1；合同最低采购、可取消上限、租赁及担保分列，递表不视为融资到账。'),
 ('china','中国传导区分正式报表、预告和经营公告；已发生事件退出未来日历，后续电话会采用北京时间。'),
 ('conclusion','综合判断采用9月通胀及修订值、10月26日国债观察，保留经营改善和融资可得的反方证据，不生成未经校准的新概率。'),
 ('scenarios','重写风险传导、延迟消化和跨境工具章节，撤下确定崩盘时间、自动踩踏系数及个人操作配比。'),
 ('audit','事实核对按当前论据重组，沿用基线和未核缺口单列；历史审计与预测记分只在独立档案追溯。'),
 ('layout','目录、书签和页码全部由本册正文重建；变更一条一段，集中列出参考资料，保留淡蓝色图表并加“大队长出品”水印。')]
DISCLAIMER='''## 免责声明

本报告为“大队长”基于公开资料形成的个人研究，不代表任何任职机构，不构成个性化投资建议、收益保证或交易指令。研究判断可能错误，公开信息可能随后修订。

资料核验截至2026年10月27日（北京时间），各财务、市场、技术与政策数据使用正文注明的报告期或观察日，并非全部是同日现值。公司指引、条件算例和已实现结果分开；没有证据的输入留空，未完成校准的情景不提供精确概率。

这是按现行判断重新组织的正文，不是历史原页加滚动校注。旧稿独立存档；原预测条件不倒改。段落中的核验范围以具体来源为准，不等于对全部历史事实重新审计。'''

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def source_path(key):return SRC/('12_各读者版本与情景.md' if key.startswith('short:') else PARTS[key])
def source(key):
    text=source_path(key).read_text()
    if key.startswith('short:'):
        blocks=re.split(r'<!-- EDITION:(\w+) -->',text)
        return dict(zip(blocks[1::2],blocks[2::2]))[key.split(':')[1]].strip()
    if key in ('framework','shale'):
        parts=re.split(r'(?=^## .*?(?:附篇\s*C|页岩油))',text,flags=re.M,maxsplit=1)
        if len(parts)!=2:raise ValueError('Missing reviewed shale split')
        text=parts[0] if key=='framework' else parts[1]
    text=re.sub(r'^# (?!#).*\n','',text,count=1)
    for marker in ['<!-- CHANGELOG_START -->','<!-- BODY_END -->','<!-- MONETIZATION_BODY_END -->']:
        if marker in text:raise ValueError('Historical changelog still present: '+key)
    return text.strip()

def prepare_body(keys):
    # Stable explicit chapter labels are shared across standalones and compendia.
    body='\n\n'.join(source(k) for k in keys)
    body=body.replace('../../13_全景版配图/','assets/')
    body=body.replace('(../../V1.6.1主题阅读版/','(../V1.6.1主题阅读版/')
    return body+bibliography(body)

def prepare_assets():
    """Copy used diagrams without changing their data periods or historical originals."""
    dest=OUT/'assets';dest.mkdir(parents=True,exist_ok=True)
    asset_map={}
    for md in SRC.glob('*.md'):
        for rel in re.findall(r'!\[[^\]]*\]\((../../13_全景版配图/[^)]+)\)',md.read_text()):
            origin=(SRC/rel).resolve();target=dest/origin.name
            content=origin.read_text()
            # Only visible text nodes: keep source URLs, observation dates, units and data.
            content=re.sub(r'(>)([^<>]*)(<)',lambda m:m[1]+re.sub(r'V1\.\d+(?:\.\d+)?','V1.7',m[2])+m[3],content)
            target.write_text(content)
            asset_map[str(target.relative_to(ROOT))]={'original':str(origin.relative_to(ROOT)),'original_sha256':sha(origin),'current_sha256':sha(target),'change':'visible report-version label only; observation dates and data unchanged'}
    (OUT/'asset-provenance.json').write_text(json.dumps(asset_map,ensure_ascii=False,indent=2)+'\n')

def front(keys):
    if keys==['short:intro']:
        return '## 免责声明\n\n个人公开资料研究，不代表任职机构，不构成投资建议。资料截止2026-10-27，各事实以自身期间为准。\n\n## 本次更新\n\n正文按最新证据重组，删除重复历史附页，目录与页码重新生成。'
    picks={'structure','layout'}
    if len(keys)>5:picks|={x[0] for x in CHANGES}
    else:
        picks|=set(keys)
        if any(k in keys for k in ['crash','delay','crossborder','framework','shale','fusion']):picks.add('scenarios')
        if 'monetization' in keys:picks.add('circular')
        if 'valuation' in keys:picks.add('conclusion')
    change='\n\n'.join(f'{i}. {t}' for i,(_,t) in enumerate([x for x in CHANGES if x[0] in picks],1))
    return DISCLAIMER+'\n\n## 本次更新\n\n'+change

def css(title):
    contact=' · '.join(identity()['contact_lines']).replace('"','\\"')
    return f'''@font-face{{font-family:Noto;src:url("../11_源码_python生成脚本/fonts/NotoSansSC-Regular.ttf")}}
@font-face{{font-family:Noto;src:url("../11_源码_python生成脚本/fonts/NotoSansSC-Bold.ttf");font-weight:700}}
@page{{size:A4;margin:20mm 18mm 20mm;@top-left{{content:"大队长 · {title}";font-family:Noto;font-size:7pt;color:#667f90}}@top-right{{content:"V1.7 · 2026-10-27";font-family:Noto;font-size:7pt;color:#667f90}}@bottom-left{{content:"大队长出品 · 独立研究";font-family:Noto;font-size:7pt;color:#6b8090}}@bottom-center{{content:"{contact}";font-family:Noto;font-size:6.8pt;color:#6b8090}}@bottom-right{{content:counter(page)" / "counter(pages);font-family:Noto;font-size:7pt;color:#667f90}}}}
@page cover{{margin:0;@top-left{{content:none}}@top-right{{content:none}}@bottom-left{{content:none}}@bottom-center{{content:none}}@bottom-right{{content:none}}}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Noto,sans-serif;font-size:10.5pt;line-height:1.8;color:#273e4d}}
.watermark{{position:fixed;left:0;right:0;top:37%;text-align:center;transform:rotate(-28deg);font-size:57pt;font-weight:700;letter-spacing:5pt;color:#7aa6c0;opacity:.09;z-index:10;pointer-events:none;white-space:nowrap}}
.references{{break-before:page}}.references p{{font-size:9pt}}.references ol{{font-size:8.8pt;line-height:1.65}}.references li{{margin:7pt 0;break-inside:avoid}}.references li p{{margin:3pt 0;font-size:8.8pt}}.ref-url{{font-size:7.5pt;color:#667f90;overflow-wrap:anywhere;word-break:break-all}}.contact{{font-size:9pt;color:#607b8e}}
.cover{{page:cover;height:296mm;background:#f8fbfd;padding:36mm 25mm;break-after:page;position:relative}}.cover .line{{width:45mm;height:3mm;background:#91bdd5;margin-bottom:15mm}}.brand{{color:#64839a;font-size:10pt;letter-spacing:1pt}}
.cover h1{{font-size:30pt;line-height:1.5;margin:30mm 0 12mm;color:#315e7c}}.subtitle{{font-size:13pt;color:#607b8e;line-height:1.9}}.cover .edition{{margin-top:24mm;font-size:12pt}}.cover .foot{{position:absolute;bottom:27mm;left:25mm;right:25mm;border-top:1pt solid #c7dce8;padding-top:6mm;font-size:9pt;color:#647f91}}
.front{{break-after:page}}.toc{{break-after:page}}.toc a{{display:block;color:#355f7b;text-decoration:none;border-bottom:.4pt dotted #bfd3df;padding:4pt 0;font-size:9.2pt;line-height:1.6;break-inside:avoid}}.toc .l2{{font-weight:700;margin-top:6pt}}.toc .l3{{padding-left:12pt}}.toc a:after{{content:target-counter(attr(href url),page);float:right}}
h1,h2,h3,h4{{color:#315e7c;line-height:1.5;break-after:avoid}}h1{{font-size:22pt}}h2{{font-size:17pt;border-bottom:1pt solid #9dbed2;padding-bottom:6pt;margin:22pt 0 12pt}}h3{{font-size:12.5pt;margin:17pt 0 8pt}}h4{{font-size:11pt;margin:14pt 0 7pt}}main h2{{bookmark-level:1}}main h3{{bookmark-level:2}}main h4{{bookmark-level:3}}
p{{margin:8pt 0;orphans:3;widows:3}}a{{color:#386b8c;text-decoration:none;overflow-wrap:anywhere}}blockquote{{border-left:3pt solid #a1c5db;background:#f0f7fb;padding:8pt 12pt;margin:12pt 0}}table{{border-collapse:collapse;width:100%;font-size:8.3pt;line-height:1.65;margin:12pt 0 16pt}}thead{{display:table-header-group}}tr{{break-inside:avoid}}td,th{{border:.5pt solid #c9dce7;padding:6pt 7pt;text-align:left;vertical-align:top}}th{{background:#e0eef7;color:#315e7c}}tr:nth-child(even) td{{background:#f7fafc}}
ul,ol{{padding-left:1.5em;margin:10pt 0}}li{{margin:7pt 0}}img{{display:block;max-width:100%;max-height:215mm;object-fit:contain;margin:14pt auto}}code{{font-family:Noto;background:#f0f5f8;font-size:.95em}}hr{{border:0;border-top:.6pt solid #c9dce7;margin:15pt 0}}
@media screen{{body{{max-width:1100px;margin:auto;padding:22px}}.cover{{height:auto;min-height:80vh;padding:42px 32px}}.cover h1{{margin-top:60px}}.cover .foot{{position:static;margin-top:60px}}.toc a:after{{content:none}}.front,.toc,main{{padding:12px}}table{{display:block;overflow:auto}}.watermark{{font-size:clamp(28px,5vw,72px)}}}}
'''

def tag_headings(text):
    headings=[]
    def tag(m):
        level=int(m[1]);title=html.unescape(re.sub('<[^>]+>','',m[2]));anchor=f'h-{len(headings):04d}'
        headings.append(dict(level=level,text=title,anchor=anchor))
        return f'<h{level} id="{anchor}">{m[2]}</h{level}>'
    return re.sub(r'<h([1-6])[^>]*>(.*?)</h\1>',tag,text,flags=re.S),headings

def build(item):
    slug,title,keys,subtitle=item
    body=prepare_body(keys);f=front(keys)
    OUT.mkdir(exist_ok=True)
    brand=identity();contact=' · '.join(brand['contact_lines'])
    contact_html=('<br>'+contact_markup()) if contact else ''
    md=f'# {title}\n\n大队长出品 · V1.7 · {DATE}\n\n'+(contact+'\n\n' if contact else '')+f'{f}\n\n<!-- BODY_START -->\n\n{body}\n'
    (OUT/f'{slug}.md').write_text(md)
    exts=['tables','fenced_code','footnotes','attr_list','sane_lists']
    rendered,headings=tag_headings(markdown.markdown(body,extensions=exts))
    rendered=rendered.replace('<!-- REFERENCES_START -->','<section class="references">')+'</section>'
    toc='<nav class="toc"><h1>目录</h1><p>本册统一目录，页码由当前正文生成；各篇采用全景统一章节标识，便于交叉核对。</p>'
    for h in headings:
        if h['level']<=3:toc+=f'<a class="l{h["level"]}" href="#{h["anchor"]}">{html.escape(h["text"])}</a>'
    toc+='</nav>'
    cover=f'<section class="cover"><div class="line"></div><p class="brand">大队长出品 · AI产业周期研究</p><h1>{html.escape(title)}</h1><p class="subtitle">{html.escape(subtitle)}</p><p class="edition">V1.7 · 现行正文<br>2026年10月27日</p><p class="foot">资料按各自报告期使用 · 事实与假设分列<br>个人研究 · 不构成投资建议{contact_html}</p></section>'
    styles=css(title)
    if len(keys)==1 and keys[0].startswith('short:'):
        cover=f'<header><p class="brand">大队长出品 · V1.7 · {DATE}{contact_html}</p><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></header>'
        styles+=' .front{font-size:8.8pt}.front,.toc,.references{break-after:auto;break-before:auto}.front h2,.toc h1{font-size:12pt;margin:13pt 0 6pt}.toc a{font-size:8.6pt}.toc p{display:none}'
    full=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="大队长"><title>{title} V1.7</title><style>{styles}</style></head><body><div class="watermark" aria-hidden="true">大队长出品</div>{cover}<section class="front">{markdown.markdown(f,extensions=exts)}</section>{toc}<main>{rendered}</main></body></html>'
    hp=OUT/f'{slug}.html';pp=OUT/f'{slug}.pdf';hp.write_text(full)
    HTML(string=full,base_url=OUT.as_uri()+'/').write_pdf(pp)
    with fitz.open(pp) as d:pages=len(d)
    assets={ROOT/'11_源码_python生成脚本/fonts/NotoSansSC-Regular.ttf',ROOT/'11_源码_python生成脚本/fonts/NotoSansSC-Bold.ttf'}
    assets|={(OUT/p).resolve() for p in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',body) if not p.startswith('http')}
    base_body=body.split('<!-- REFERENCES_START -->',1)[0]
    row=dict(slug=slug,title=title,keys=keys,pages=pages,headings=headings,reference_count=len(reference_entries(base_body)),identity_sha256=sha(IDENTITY_PATH),reference_labels_sha256=sha(REFERENCE_LABELS_PATH),source_sha256={str(source_path(k).relative_to(ROOT)):sha(source_path(k)) for k in keys},asset_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(assets)})
    for ext in ['md','html','pdf']:
        p=OUT/f'{slug}.{ext}';row[ext]={'path':str(p.relative_to(ROOT)),'sha256':sha(p)}
    print(f'{slug}: {pages} pages',flush=True)
    return row

def main():
    p=argparse.ArgumentParser();p.add_argument('--only',nargs='*');args=p.parse_args()
    prepare_assets()
    reports=[build(x) for x in CATALOG if not args.only or x[0] in args.only]
    mf=OUT/'manifest.json';old=json.loads(mf.read_text()) if mf.exists() else {'reports':[]}
    rows={r['slug']:r for r in old['reports']};rows.update({r['slug']:r for r in reports})
    result={'version':'V1.7','date':DATE,'scope':'current_body_reconstruction_no_original_pdf_append','builder_sha256':sha(__file__),'status':'BUILT_NOT_ACCEPTED','reports':[rows[x[0]] for x in CATALOG if x[0] in rows]}
    mf.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    links=''.join(f'<tr><td>{html.escape(r["title"])}</td><td>{r["pages"]}</td><td><a href="{r["slug"]}.pdf">PDF</a> · <a href="{r["slug"]}.html">网页</a> · <a href="{r["slug"]}.md">Markdown</a></td></tr>' for r in result['reports'])
    index=f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI泡沫研究 V1.7</title><style>body{{font:17px/1.85 system-ui;max-width:1050px;margin:auto;padding:30px;color:#2e495b;background:#f8fbfd}}a{{color:#316888}}table{{width:100%;border-collapse:collapse}}td,th{{padding:12px;border-bottom:1px solid #cbdfea;text-align:left}}h1,h2{{color:#315e7c}}.lead{{background:#eaf3f9;padding:22px;border-left:5px solid #9bc4dd}}</style><h1>AI周期与泡沫研究 · V1.7</h1><p>大队长 · 2026-10-27 · 现行正文</p><div class="lead"><strong>直接读当前报告，不再逐页寻找校注。</strong><p><a href="13_超全景版.pdf">超全景现行正文 PDF</a> · <a href="13_超全景版.html">完整网页</a> · <a href="01_主报告.pdf">主报告 PDF</a></p><p>原339页中的研究主题保留，重复合并；旧版独立存档，不再嵌进新报告。数据采用各自期间，尚待披露的财报不预填结果。</p></div><h2>阅读版本</h2><table><thead><tr><th>文件</th><th>实测页数</th><th>格式</th></tr></thead><tbody>{links}</tbody></table><h2>本次改动与覆盖</h2><p><a href="../复审与版本记录/V1.7_本次更新说明_20261027.md">本次更新</a> · <a href="../复审与版本记录/V1.7_原339页主题覆盖表_20261027.md">原主题覆盖与处置</a> · <a href="manifest.json">文件清单</a> · <a href="qa.json">结构核验</a></p><h2>历史档案</h2><p><a href="../V1.6.1完整校注版/index.html">V1.6.1校注存档</a> · <a href="../09_历史冻结基线/超全景339页_20261009更新前.pdf">原339页底本</a></p><p>个人公开资料研究，不代表任职机构，不构成投资建议。本地构建与外部发布分别确认。</p></html>'''
    brand=identity();contact=' · '.join(brand['contact_lines'])
    index=index.replace('大队长 · 2026-10-27','大队长出品 · 2026-10-27')
    index=index.replace('<h2>本次改动与覆盖</h2>','<h2>参考资料与作者标识</h2><p>各册保留正文就近引用，并在文末集中列出完整网址；PDF逐页加“大队长出品”淡水印。<a href="参考资料总索引.md">参考资料总索引</a></p>'+('<p>'+contact_markup()+'</p>' if contact else '')+'<h2>本次改动与覆盖</h2>')
    (OUT/'index.html').write_text(index)
    raw_body='\n\n'.join(source(k) for k in FULL)
    (OUT/'参考资料总索引.md').write_text('# AI周期与泡沫研究 · 参考资料\n\n大队长出品 · V1.7 · 2026-10-27\n\n'+(contact+'\n\n' if contact else '')+bibliography(raw_body)+'\n')
    (OUT/'reference-catalog.json').write_text(json.dumps({'date':DATE,'unique_urls':len(reference_entries(raw_body)),'scope':'exact URL deduplication, not full source re-verification','items':[{'url':u,'body_label':label} for u,label in reference_entries(raw_body)]},ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
