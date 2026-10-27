#!/usr/bin/env python3
"""Render thematic V1.5 bodies; never prepend the V1.4 rolling update or frozen PDFs."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path

import fitz
import markdown
from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '10_源码_markdown/V1.5正文修订'
OUT = ROOT / 'V1.5正文修订版'
FONTS = ROOT / '11_源码_python生成脚本/fonts'
DATE = '2026-09-08'
PARTS = {
 'profit':'01_利润真实性拆解.md', 'circular':'02_循环投资网络.md',
 'monetization':'03_AI变现与编程TAM.md', 'agi':'04_AGI与国际格局.md',
 'china':'06_中国投资者传导.md', 'valuation':'07_公司分化与估值.md',
 'conclusion':'08_风险与综合结论.md', 'framework':'09_框架与页岩油类比.md',
 'fusion':'10_聚变能源与资本回收.md', 'alphabet':'11_Alphabet融资案例.md',
 'audit':'13_事实审计处置表.md',
}
CORE = ['profit','circular','monetization','agi','china','valuation','conclusion']
ANNEXES = ['framework','alphabet','fusion']
CATALOG = [
 ('01_主报告','AI周期与泡沫深度研究报告',CORE,'把经营、资本回收与金融条件分别判断。'),
 ('02_事实审计表','AI周期与泡沫 · 事实审计处置表',['audit'],'按原条目逐项记录本轮处置，不把条目数当作复核通过数。'),
 ('03_利润真实性拆解','利润真实性拆解',['profit'],'营业利润、投资重估、回款和资产投入分别核对。'),
 ('04_循环投资网络','循环投资网络',['circular'],'区分投资、采购、承诺与担保，沿合同寻找最终付款来源。'),
 ('05_AI变现与编程TAM','AI变现与编程TAM',['monetization'],'收费如何形成收入，收入又怎样转成可持续现金。'),
 ('06_AGI与国际格局','AGI与国际格局',['agi'],'技术能力、算力与能源、出口规则和国际竞争。'),
 ('07_机构简版','AI周期与泡沫 · 机构简版',['short:institution'],'核心判断、证据分歧和下一轮核验。'),
 ('08_公开精简版','AI周期与泡沫 · 公开精简版',['short:public','profit','monetization','agi','china'],'以经营、商业化和国际约束为主线的专题选编。'),
 ('09_雪球公开版','AI周期与泡沫 · 雪球公开版',['short:snowball','valuation','china'],'从产业增长落到公司现金与估值，保留反方条件。'),
 ('10_摘要版','AI周期与泡沫 · 摘要版',['short:summary'],'保留最重要的结论、证据与未知。'),
 ('11_执行简版','AI周期与泡沫 · 研究执行简版',['short:execution'],'执行的是核验与模型更新，不是交易指令。'),
 ('12_全景版','2026年AI泡沫研究 · 全景版',CORE+ANNEXES,'完整主题正文及框架、历史类比、融资与能源专题。'),
 ('13_超全景版','2026年AI泡沫研究 · 超全景版',CORE+ANNEXES+['audit'],'主题正文、专题附篇与逐条证据处置合卷；不拼接旧版凑页数。'),
 ('14_完整合集','AI周期与泡沫 · 完整合集',['short:institution']+CORE+ANNEXES,'机构导读与主题研究合编，导读不替代正文。'),
 ('15_延迟情景版','AI泡沫研究 · 延迟情景版',['short:delay','circular','framework','fusion'],'延迟何时放大资本缺口，何时有助于消化供给。'),
 ('16_崩盘剧本','AI泡沫研究 · 风险传导剧本',['short:crash','conclusion'],'条件、传导、反证与中止；不预告确定崩盘日期。'),
 ('17_发布引流稿','AI泡沫研究 · 发布导读',['short:intro'],'问题导读，不用确定性崩盘标题替代研究结论。'),
]
CHANGE = {
 'profit':'利润篇：按财季重建经营与投资收益、现金流、折旧和租赁；纠正把非现金收益等同虚假利润的表述。',
 'circular':'循环篇：逐笔分开股权、采购与担保；纠正CoreWeave投资月份，拆开Alphabet计划、到账和未用额度。',
 'monetization':'变现篇：重建收费版图，纠正编程TAM单位和IRR误用，补入按量计费及新增商业化证据。',
 'agi':'AGI篇：更新能力评测、技术路线、电力、出口规则与国际竞争；撤回确定AGI年份和无依据的估值冲击。',
 'china':'中国传导：用正式半年报替换光模块待披露状态，补足产品、份额、现金和估值链条；纠正跨境额度表述。',
 'valuation':'公司与估值：去除确定输赢和固定跌幅，按盈利、倍数、净债务及现金回收展开。',
 'conclusion':'风险结论：区分主观权重与统计概率，更新就业修订和信用截点，保留事前记分边界与反证。',
 'framework':'方法与类比：分开收入、投资和回报，纠正线性爬坡算法及页岩油历史类比。',
 'alphabet':'融资案例：把计划额度、实际发行与资本用途分开，不再用一笔融资直接证明市场见顶。',
 'fusion':'能源专题：更新聚变工程目标，区分Q值和商业供电，加入成本基数清楚的毛利敏感性。',
 'audit':'事实审计：逐项保留原ID与历史记录，另列更新、撤回、部分复核和未复核，不延续旧勾选为本轮通过。',
}
DISCLAIMER = '''## 免责声明与阅读边界

本报告为“大队长”基于公开资料形成的个人研究，不代表任何任职机构观点，不构成个性化投资建议、收益保证或交易指令。技术和商业判断可能错误，信息也可能随后修订。

V1.5为正文修订版，资料检索截止2026年9月8日；各项财务、统计、行情与政策数据以正文明确的期间或观察日为准，不能全部理解为该日现值。公司指引、研究假设和已实现结果分开阅读；缺失的原始证据不以推测填补。

本版按主题重编，不沿用旧版分页；旧版与原投递件保留不改。历史评分和预测记录只用于追溯，未完成统计校准的数字不属于经过验证的崩盘概率。审计条目总数不等于本轮全部事实复核通过。'''

def source(key: str) -> str:
    if key.startswith('short:'):
        text = (SRC/'12_各读者版本与情景.md').read_text()
        target = key.split(':',1)[1]
        blocks = re.split(r'<!-- EDITION:(\w+) -->',text)
        return dict(zip(blocks[1::2],blocks[2::2]))[target].strip()
    raw = (SRC/PARTS[key]).read_text()
    body = re.split(r'<!--\s*(?:CHANGELOG_START|MONETIZATION_BODY_END|BODY_END)\s*-->',raw)[0].strip()
    if key == 'agi':
        body = body[body.index('## 第四部分'):]
    return body

def revision_details(key: str) -> str:
    if key.startswith('short:'):
        return ''
    raw=(SRC/PARTS[key]).read_text()
    pieces=re.split(r'<!--\s*(?:CHANGELOG_START|MONETIZATION_BODY_END|BODY_END)\s*-->',raw,maxsplit=1)
    if len(pieces)<2:return ''
    tail=re.sub(r'^\s*#{1,6}[^\n]*\n','',pieces[1],count=1).strip()
    # AGI's standalone source index is not a second change record; its citations
    # already appear at the claims. Keep all actual numbered corrections.
    tail=re.split(r'^#{1,3} ',tail,maxsplit=1,flags=re.M)[0].strip()
    name=re.sub(r'^\d+_','',Path(PARTS[key]).stem)
    return f'### {name}：逐项修订\n\n{tail}'

def compose_body(keys: list[str]) -> str:
    body='\n\n'.join(source(k) for k in keys)
    logs=[revision_details(k) for k in dict.fromkeys(keys)]
    logs=[x for x in logs if x]
    if logs:
        body+='\n\n## 本版逐项修订记录\n\n这里只列本报告实际采用章节的修订；每条对应原文纠错或证据更新，不是全景财报前言。\n\n'+'\n\n'.join(logs)
    return body.replace('../../13_全景版配图/','../13_全景版配图/')

def input_paths(keys: list[str]) -> list[Path]:
    return sorted({SRC/('12_各读者版本与情景.md' if k.startswith('short:') else PARTS[k]) for k in keys})

def source_digests(keys: list[str]) -> dict[str,str]:
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths(keys)}

def asset_digests(keys: list[str]) -> dict[str,str]:
    paths={FONTS/'NotoSansSC-Regular.ttf',FONTS/'NotoSansSC-Bold.ttf'}
    for key in keys:
        for link in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',source(key)):
            if not link.startswith(('https://','http://')):paths.add((SRC/link).resolve())
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}

def front(keys: list[str]) -> str:
    changes = [CHANGE[k] for k in keys if k in CHANGE]
    if any(k.startswith('short:') for k in keys):
        changes.insert(0,'本篇按目标读者重新组织结论和展开；更新写进相应论点，不以前置全景财报替代原正文。')
    detail_note='\n\n逐项勘误与修订见文末《本版逐项修订记录》，可从目录跳转。' if any(k in PARTS for k in keys) else ''
    return DISCLAIMER+'\n\n## 本版修订说明\n\n'+ '\n\n'.join(f'{i}. {c}' for i,c in enumerate(changes,1))+detail_note

def style(title: str) -> str:
    title = title.replace('"','')
    return f'''@font-face{{font-family:Noto;src:url("../11_源码_python生成脚本/fonts/NotoSansSC-Regular.ttf")}}
@font-face{{font-family:Noto;src:url("../11_源码_python生成脚本/fonts/NotoSansSC-Bold.ttf");font-weight:700}}
@page{{size:A4;margin:18mm 17mm 19mm;@top-left{{content:"大队长 · {title}";font-family:Noto;font-size:7pt;color:#687888}}@top-right{{content:"V1.5 · 正文修订 · {DATE}";font-family:Noto;font-size:7pt;color:#687888}}@bottom-left{{content:"个人研究 · 公开资料 · 不构成投资建议";font-family:Noto;font-size:7pt;color:#687888}}@bottom-right{{content:counter(page)" / "counter(pages);font-family:Noto;font-size:7pt;color:#687888}}}}
@page cover{{margin:0;@top-left{{content:none}}@top-right{{content:none}}@bottom-left{{content:none}}@bottom-right{{content:none}}}}
*{{box-sizing:border-box}}body{{font-family:Noto,sans-serif;font-size:10pt;line-height:1.7;color:#263643;margin:0}}
.cover{{page:cover;height:296mm;padding:34mm 25mm;position:relative;break-after:page;background:#fbfdff}}
.cover .line{{width:52mm;height:3mm;background:#86b8d5;margin-bottom:14mm}}.brand{{font-size:10pt;color:#637b8e;letter-spacing:1px}}
.cover .title{{font-size:29pt;line-height:1.5;color:#28516e;margin:25mm 0 12mm;font-weight:700}}
.cover .subtitle{{font-size:13pt;line-height:1.9;max-width:150mm;color:#526878}}.cover .date{{margin-top:23mm;font-size:11pt;color:#506f85}}
.cover .foot{{position:absolute;bottom:27mm;left:25mm;right:25mm;padding-top:5mm;border-top:1px solid #d8e7ef;font-size:9pt;color:#647b8e}}
.front{{break-after:page}}.toc{{break-after:page}}.toc a{{display:block;border-bottom:.4pt dotted #bfd2df;padding:3pt 0;color:#365a72;text-decoration:none;font-size:9pt}}
.toc .l3{{padding-left:12pt;font-weight:400}}.toc .l2{{font-weight:700;margin-top:3pt}}.toc a:after{{content:target-counter(attr(href url),page);float:right;color:#315e7c}}
h1,h2,h3,h4{{line-height:1.45;break-after:avoid;color:#315e7c}}h1{{font-size:21pt}}h2{{font-size:16pt;border-bottom:1.2pt solid #95bbd3;padding-bottom:5pt;margin:18pt 0 10pt}}h3{{font-size:12pt;margin:15pt 0 7pt}}h4{{font-size:10.8pt;margin:12pt 0 6pt}}main h2{{bookmark-level:1}}main h3{{bookmark-level:2}}main h4{{bookmark-level:3}}
p{{margin:7pt 0;orphans:3;widows:3}}a{{color:#315e7c;text-decoration:none;overflow-wrap:anywhere}}blockquote{{border-left:3pt solid #8ab8d4;background:#f2f7fb;padding:6pt 10pt;margin:8pt 0;color:#536776}}
table{{border-collapse:collapse;width:100%;margin:9pt 0 13pt;font-size:8.3pt;table-layout:auto}}thead{{display:table-header-group}}tr{{break-inside:avoid}}th{{background:#dcecf6;color:#244b66;font-weight:700;text-align:left}}th,td{{border:.5pt solid #c7d9e4;padding:5pt 6pt;vertical-align:top;line-height:1.55;overflow-wrap:anywhere}}tr:nth-child(even) td{{background:#f7fafc}}
ul,ol{{padding-left:1.5em;margin:8pt 0}}li{{margin:6pt 0}}img{{display:block;max-width:100%;max-height:210mm;object-fit:contain;margin:12pt auto}}figure{{break-inside:avoid}}code{{font-family:Noto;font-size:.95em;background:#edf3f7;padding:1pt 3pt}}hr{{border:0;border-top:.5pt solid #cadbe5;margin:14pt 0}}
@media screen{{body{{max-width:960px;margin:0 auto;padding:20px;background:white}}.cover{{height:auto;min-height:75vh;padding:40px 28px}}.cover .foot{{position:static;margin-top:45px}}.front,.toc,main{{padding:10px 12px}}.toc a:after{{content:none}}table{{display:block;overflow-x:auto}}}}'''

def tag_headings(text: str) -> tuple[str,list]:
    headings=[]
    def tag(m):
        serial=len(headings);level=int(m[1]);name=re.sub('<[^>]+>','',m[2]);anchor=f'h-{serial:04d}'
        headings.append(dict(level=level,text=html.unescape(name),anchor=anchor))
        return f'<h{level} id="{anchor}">{m[2]}</h{level}>'
    return re.sub(r'<h([1-6])[^>]*>(.*?)</h\1>',tag,text,flags=re.S),headings

def build(item):
    slug,title,keys,subtitle=item
    body=compose_body(keys)
    assert 'HISTORICAL_START' not in body and '[[CHART:' not in body
    # Export resources relative to the edition directory, not the authoring directory.
    body=body.replace('../../13_全景版配图/','../13_全景版配图/')
    changes=front(keys)
    md=f'# {title}\n\nV1.5 · 正文修订 · {DATE}\n\n{changes}\n\n<!-- BODY_START -->\n\n{body}\n'
    OUT.mkdir(parents=True,exist_ok=True)
    md_path=OUT/f'{slug}.md';html_path=OUT/f'{slug}.html';pdf_path=OUT/f'{slug}.pdf'
    md_path.write_text(md)
    extensions=['tables','fenced_code','footnotes','attr_list']
    rendered,headings=tag_headings(markdown.markdown(body,extensions=extensions))
    rendered=re.sub(r'(<h2\b[^>]*>三、原E记分.*?)(?=<h2\b|\Z)',r'<section class="keep-together">\1</section>',rendered,flags=re.S)
    toc='<section class="toc"><h1>目录</h1><p>目录及页码依据本版正文生成；PDF内可点击跳转。</p>'
    for h in headings:
        if h['level']<=3:
            toc+=f'<a class="l{h["level"]}" href="#{h["anchor"]}">{html.escape(h["text"])}</a>'
    toc+='</section>'
    cover=f'<section class="cover"><div class="line"></div><div class="brand">大队长 · AI产业周期研究</div><div class="title">{html.escape(title)}</div><div class="subtitle">{html.escape(subtitle)}</div><div class="date">V1.5 · 正文修订<br>{DATE}</div><div class="foot">按本篇主题组织证据与分析<br>个人研究 · 基于公开信息 · 不构成投资建议</div></section>'
    css=style(title)+' .keep-together{break-inside:avoid} '
    compact = len(keys)==1 and keys[0].startswith('short:')
    if compact:
        cover=f'<header><p class="brand">大队长 · V1.5正文修订 · {DATE}</p><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></header>'
        css+=' .front,.toc{break-after:auto}.front{font-size:8.8pt}.front h2,.toc h1{font-size:12pt;margin:12pt 0 5pt}.toc a{display:inline-block;border:0;margin:0 12pt 3pt 0;font-size:8.5pt}.toc a:after{content:none}.toc p{display:none} '
    full=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="大队长"><title>{html.escape(title)} V1.5</title><style>{css}</style></head><body>{cover}<section class="front">{markdown.markdown(changes,extensions=extensions)}</section>{toc}<main>{rendered}</main></body></html>'
    html_path.write_text(full)
    HTML(string=full,base_url=str(OUT)).write_pdf(pdf_path)
    with fitz.open(pdf_path) as doc:
        pages=len(doc)
    print(f'{slug}: {pages} pages',flush=True)
    record=dict(slug=slug,title=title,sources=keys,source_sha256=source_digests(keys),asset_sha256=asset_digests(keys),pages=pages,headings=headings)
    for ext,path in [('md',md_path),('html',html_path),('pdf',pdf_path)]:
        record[ext]=dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return record

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='*');args=parser.parse_args()
    records=[]
    for item in CATALOG:
        if args.only and item[0] not in args.only:continue
        records.append(build(item))
    manifest=OUT/'manifest.json'
    previous=json.loads(manifest.read_text()) if manifest.exists() else {'reports':[]}
    indexed={r['slug']:r for r in previous['reports']};indexed.update({r['slug']:r for r in records})
    result={'version':'V1.5','date':DATE,'status':'BUILT','qa_record':'qa.json','qa_boundary':'Build is not verification; consult fresh QA hashes and independent review record.','scope':'thematic_body_editions_no_frozen_pdf_append','builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'reports':[indexed[k[0]] for k in CATALOG if k[0] in indexed]}
    manifest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    rows=''.join(f'<tr><td>{html.escape(r["title"])}</td><td>{r["pages"]}</td><td><a href="{r["slug"]}.html">网页</a> · <a href="{r["slug"]}.pdf">PDF</a> · <a href="{r["slug"]}.md">Markdown</a></td></tr>' for r in result['reports'])
    (OUT/'index.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V1.5正文修订索引</title><style>{style("报告索引")}</style><body><h1>V1.5 正文修订版</h1><p>各篇围绕自己的主题更新正文，不再统一前置全景财报。各数据按原报告期或观察日阅读。</p><p>本版按主题重编，不保留旧版逐页布局；原339页超全景档案保留，未声称其逐页全量复核。112项原审计中仍有53项历史待复核，不能把生成或结构通过等同于全部事实通过。</p><p><a href="../复审与版本记录/V1.5_交叉复审与排版验收.md">交叉复审与视觉抽查记录</a> · <a href="qa.json">结构QA</a> · <a href="manifest.json">输入与产物哈希</a> · <a href="../00_使用说明/版本矩阵_V1.4_2026-09-08.md">V1.4历史矩阵</a></p><table><thead><tr><th>报告</th><th>PDF页数</th><th>阅读</th></tr></thead><tbody>{rows}</tbody></table><p>仅本地研究维护，未执行Git推送或外部发布；不包含招聘材料。</p></body></html>')

if __name__=='__main__':main()
