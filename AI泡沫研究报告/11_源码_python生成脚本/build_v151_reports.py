#!/usr/bin/env python3
"""Render thematic V1.5.1 bodies; never prepend the V1.4 rolling update or frozen PDFs."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from collections import Counter

import fitz
import markdown
from weasyprint import CSS, HTML
import edition_numbering_v151 as numbering

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '10_源码_markdown/V1.5.1正文修订'
OUT = ROOT / 'V1.5.1正文修订版'
FONTS = ROOT / '11_源码_python生成脚本/fonts'
DATE = '2026-10-09'
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
 "profit": "利润篇：新增APLD基础租金、装修收入与集团现金桥；三星Q3只列初步合并估计，期后交付、分部与集团口径分别处理。",
 "circular": "循环篇：补核SoftBank已执行出资、Jupiter完整回应；CoreWeave印度扩容仍是计划，不与旧承诺相加。",
 "monetization": "变现篇：新增Haiku 5.5按请求长度分档的价目及算例，更新Sonnet缓存费；视觉广告测试不当作已确认收入。",
 "agi": "AGI篇：补AMD预发布测试的方法和速度门槛，厂商吞吐比不外推成商业收入或投资回报。",
 "china": "中国传导：台积电9月月报结转，复算Q2/Q3月报加总；新增就业修订，并接续CPI、PPI、Q3电话会和FOMC北京时间。",
 "valuation": "公司与估值：基准接至10月8日财政部利率，注明边际略降与仍高的水平；不把国债利率直接当企业资金成本。",
 "conclusion": "风险结论：同时承认需求、交付和融资兑现与资本回收约束；纠正当期利率方向，9月会议纪要不冒充10月决议。历史评分不重校准。",
 "framework": "框架与历史类比：补月报加总、机房收入拆分、运营容量与API单请求计费的复算纪律。",
 "alphabet": "融资案例：更新利率观察日及方向，不据此更改原财季现金或融资执行状态。",
 "fusion": "能源专题：补Oracle有条件购电成本安排，现有核电、待批准承诺与已付现金分别列示。",
 "audit": "事实审计：新增或补核10月9日13组证据，旧附表按历史时点保留；原112项状态及E判断不倒改。"
}
DISCLAIMER = '''## 免责声明与阅读边界

本报告为“大队长”基于公开资料形成的个人研究，不代表任何任职机构观点，不构成个性化投资建议、收益保证或交易指令。技术和商业判断可能错误，信息也可能随后修订。

V1.5.1为V1.5基础上的增量正文修订版，增量资料检索截止2026年10月9日上午；各项财务、统计、行情与政策数据以正文明确的期间或观察日为准，不能全部理解为该日现值。公司指引、研究假设和已实现结果分开阅读；缺失的原始证据不以推测填补。

本版按主题重编，不沿用旧版分页；旧版与历史档案保留不改。历史评分和预测记录只用于追溯，未完成统计校准的数字不属于经过验证的崩盘概率。审计条目总数不等于本轮全部事实复核通过。'''

def audit_counts() -> dict[str,int]:
    raw=(SRC/PARTS['audit']).read_text()
    rows=re.findall(r'^\*\*ID ([0-9]+[a-z]*)｜(核验更新|部分核验|撤回|历史待复核)。\*\*',raw,re.M)
    states=[row[1] for row in rows]
    if len(states)!=112 or len({row[0] for row in rows})!=112:
        raise ValueError(f'Expected 112 unique original audit IDs; got {len(states)}')
    return dict(Counter(states))

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
    body='\n\n'.join(numbering.transform_body(k,source(k),keys) for k in keys)
    logs=[numbering.transform_log(k,revision_details(k),keys) for k in dict.fromkeys(keys)]
    logs=[x for x in logs if x]
    if logs:
        body+='\n\n## 本版逐项修订记录\n\n'+numbering.revision_note(keys)+'以下保留所选章节的V1.5基础修订记录，并将本轮变更标为V1.5.1；每条对应正文纠错或证据更新。\n\n'+'\n\n'.join(logs)
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
    if keys == ['short:intro']:
        return '''## 免责声明与阅读边界

本稿为“大队长”基于公开资料的个人研究，不代表任职机构，不构成投资建议、收益保证或交易指令。增量资料检索截至2026-10-09，各事实使用其自身报告期；公司计划、作者假设和已实现结果分开阅读。

## 本版修订说明

V1.5.1以客户付费与资产回收两条路径组织导读；10月9日主题正文接续台积电、APLD、三星、股权融资、模型费用及宏观观察，具体修改及证据边界见报告总索引。'''
    changes = [CHANGE[k] for k in keys if k in CHANGE]
    if any(k.startswith('short:') for k in keys):
        changes.insert(0,'本篇按目标读者重新组织结论和展开；更新写进相应论点，不以前置全景财报替代原正文。')
    detail_note='\n\n逐项勘误与修订见文末《本版逐项修订记录》，可从目录跳转。' if any(k in PARTS for k in keys) else ''
    return DISCLAIMER+'\n\n## 本版修订说明\n\n'+ '\n\n'.join(f'{i}. {c}' for i,c in enumerate(changes,1))+detail_note+numbering.notice(keys)

def style(title: str) -> str:
    title = title.replace('"','')
    return f'''@font-face{{font-family:Noto;src:url("../11_源码_python生成脚本/fonts/NotoSansSC-Regular.ttf")}}
@font-face{{font-family:Noto;src:url("../11_源码_python生成脚本/fonts/NotoSansSC-Bold.ttf");font-weight:700}}
@page{{size:A4;margin:18mm 17mm 19mm;@top-left{{content:"大队长 · {title}";font-family:Noto;font-size:7pt;color:#687888}}@top-right{{content:"V1.5.1 · 正文修订 · {DATE}";font-family:Noto;font-size:7pt;color:#687888}}@bottom-left{{content:"个人研究 · 公开资料 · 不构成投资建议";font-family:Noto;font-size:7pt;color:#687888}}@bottom-right{{content:counter(page)" / "counter(pages);font-family:Noto;font-size:7pt;color:#687888}}}}
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
table{{border-collapse:collapse;width:100%;margin:9pt 0 13pt;font-size:8.3pt;table-layout:auto}}thead{{display:table-header-group}}tr{{break-inside:avoid}}th{{background:#dcecf6;color:#244b66;font-weight:700;text-align:left}}th,td{{border:.5pt solid #c7d9e4;padding:5pt 6pt;vertical-align:top;line-height:1.55;overflow-wrap:normal;word-break:normal;hyphens:none}}td:first-child{{min-width:17mm}}tr:nth-child(even) td{{background:#f7fafc}}
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
    md=f'# {title}\n\nV1.5.1 · 正文修订 · {DATE}\n\n{changes}\n\n<!-- BODY_START -->\n\n{body}\n'
    OUT.mkdir(parents=True,exist_ok=True)
    md_path=OUT/f'{slug}.md';html_path=OUT/f'{slug}.html';pdf_path=OUT/f'{slug}.pdf'
    md_path.write_text(md)
    extensions=['tables','fenced_code','footnotes','attr_list']
    rendered,headings=tag_headings(markdown.markdown(body,extensions=extensions))
    # Keep the small, same-request tariff comparison intact; long tables may paginate.
    rendered=rendered.replace('<table>\n<thead>\n<tr>\n<th>模型及每条请求的条件</th>', '<table class="tariff-table">\n<thead>\n<tr>\n<th>模型及每条请求的条件</th>')
    rendered=re.sub(r'(<h2 id="[^"]+")(>本版逐项修订记录</h2>)',r'\1 class="revision-start"\2',rendered)
    if numbering.metadata(keys):rendered=numbering.keep_short_revision_blocks(rendered)
    rendered=re.sub(r'(<h2\b[^>]*>三、原E记分.*?)(?=<h2\b|\Z)',r'<section class="keep-together">\1</section>',rendered,flags=re.S)
    toc='<section class="toc"><h1>目录</h1><p>目录及页码依据本版正文生成；PDF内可点击跳转。</p>'
    for h in headings:
        if h['level']<=3:
            toc+=f'<a class="l{h["level"]}" href="#{h["anchor"]}">{html.escape(h["text"])}</a>'
    toc+='</section>'
    cover=f'<section class="cover"><div class="line"></div><div class="brand">大队长 · AI产业周期研究</div><div class="title">{html.escape(title)}</div><div class="subtitle">{html.escape(subtitle)}</div><div class="date">V1.5.1 · 正文修订<br>{DATE}</div><div class="foot">按本篇主题组织证据与分析<br>个人研究 · 基于公开信息 · 不构成投资建议</div></section>'
    css=style(title)+' .keep-together,.tariff-table{break-inside:avoid} .revision-start{break-before:page} '
    if numbering.metadata(keys):css+=' .revision-group{break-inside:avoid} '
    compact = len(keys)==1 and keys[0].startswith('short:')
    if compact:
        cover=f'<header><p class="brand">大队长 · V1.5.1正文修订 · {DATE}</p><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></header>'
        css+=' .front,.toc{break-after:auto}.front{font-size:8.8pt}.front h2,.toc h1{font-size:12pt;margin:12pt 0 5pt}.toc a{display:inline-block;border:0;margin:0 12pt 3pt 0;font-size:8.5pt}.toc a:after{content:none}.toc p{display:none} '
    full=f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="大队长"><title>{html.escape(title)} V1.5.1</title><style>{css}</style></head><body>{cover}<section class="front">{markdown.markdown(changes,extensions=extensions)}</section>{toc}<main>{rendered}</main></body></html>'
    html_path.write_text(full)
    HTML(string=full,base_url=str(OUT)).write_pdf(pdf_path)
    with fitz.open(pdf_path) as doc:
        pages=len(doc)
    print(f'{slug}: {pages} pages',flush=True)
    record=dict(slug=slug,title=title,sources=keys,source_sha256=source_digests(keys),asset_sha256=asset_digests(keys),pages=pages,headings=headings)
    if numbering.metadata(keys):record['numbering']=numbering.metadata(keys)
    for ext,path in [('md',md_path),('html',html_path),('pdf',pdf_path)]:
        record[ext]=dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return record

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--only',nargs='*');args=parser.parse_args()
    counts=audit_counts()
    records=[]
    for item in CATALOG:
        if args.only and item[0] not in args.only:continue
        records.append(build(item))
    manifest=OUT/'manifest.json'
    previous=json.loads(manifest.read_text()) if manifest.exists() else {'reports':[]}
    indexed={r['slug']:r for r in previous['reports']};indexed.update({r['slug']:r for r in records})
    result={'version':'V1.5.1','date':DATE,'audit_counts':counts,'status':'BUILT','qa_record':'qa.json','qa_boundary':'Build is not verification; consult fresh QA hashes and independent review record.','scope':'thematic_body_editions_no_frozen_pdf_append','builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'reports':[indexed[k[0]] for k in CATALOG if k[0] in indexed]}
    result['numbering_revision']=numbering.REVISION
    result['numbering_engine_sha256']=hashlib.sha256(Path(numbering.__file__).read_bytes()).hexdigest()
    result['numbering_review']='../复审与版本记录/V1.5.1_分册编号勘误与验收.md'
    manifest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    rows=''.join(f'<tr><td>{html.escape(r["title"])}</td><td>{r["pages"]}</td><td><a href="{r["slug"]}.html">网页</a> · <a href="{r["slug"]}.pdf">PDF</a> · <a href="{r["slug"]}.md">Markdown</a></td></tr>' for r in result['reports'])
    (OUT/'index.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V1.5.1正文修订索引</title><style>{style("报告索引")}</style><body><h1>V1.5.1 正文修订版</h1><p>增量检索截止2026年10月9日上午。各篇围绕自己的主题更新正文，不再统一前置全景财报；各数据按原报告期或观察日阅读。</p><p>本轮新增或补核台积电9月营收、APLD收入与现金、三星初步估计、SoftBank出资、CoreWeave扩容计划、Oracle完整回应与购电安排、模型费用和广告测试、AMD测试、利率、就业及FOMC纪要共13组。需求与交付仍有兑现，利率较9月底略降，资本回收仍待验证；历史评分及E记分不倒改。</p><p>9月8日编排勘误继续有效：独立分册与选编按收录顺序从第一章起排，目录及当前引用同步；主报告和全景合编保留母稿编号。事实审计表的落点明确使用超全景母稿编号。</p><p>本版按主题重编，不保留旧版逐页布局；原339页超全景档案保留，未声称其逐页全量复核。112项原审计中仍有{counts["历史待复核"]}项历史待复核，不能把生成或结构通过等同于全部事实通过。</p><p><a href="../复审与版本记录/版本变更说明_2026-10-09.md">10月9日版本变更</a> · <a href="../复审与版本记录/引用核验报告_2026-10-09.md">增量引用核验</a> · <a href="../复审与版本记录/专业复审报告_2026-10-09.md">专业复审</a> · <a href="../复审与版本记录/PDF与目录核验报告_2026-10-09.md">PDF与目录核验</a> · <a href="../复审与版本记录/发布清单_2026-10-09.md">发布清单</a></p><p><a href="qa.json">当前结构QA</a> · <a href="manifest.json">当前输入与产物哈希</a> · <a href="../复审与版本记录/V1.5.1_分册编号勘误与验收.md">分册编号勘误（9月8日）</a> · <a href="../00_使用说明/版本矩阵_V1.4_2026-09-08.md">V1.4历史矩阵</a></p><table><thead><tr><th>报告</th><th>PDF页数</th><th>阅读</th></tr></thead><tbody>{rows}</tbody></table><p>本轮仅维护研究报告；未执行Git推送或外部发布。</p></body></html>')
    md_rows='\n'.join(
        f'| {r["title"]} | {r["pages"]} | [PDF](<../V1.5.1正文修订版/{r["slug"]}.pdf>) · [网页](<../V1.5.1正文修订版/{r["slug"]}.html>) · [MD](<../V1.5.1正文修订版/{r["slug"]}.md>) |'
        for r in result['reports']
    )
    reading_index=f'''# 当前文件总索引｜2026-10-09

当前阅读版：**V1.5.1正文修订版**。[打开全部报告](../V1.5.1正文修订版/index.html)。

增量检索截止2026年10月9日上午。各数据仍按自己的财季、公告日或市场观察日阅读；截止日不是统一现值。9月8日的分册编号勘误继续有效，本轮在同一结构上更新证据、目录与产物。

## 全部17份报告

| 报告 | 实际PDF页数 | 文件 |
|---|---:|---|
{md_rows}

页数读取自当前manifest；每篇目录、书签及修订记录随本篇正文生成。长篇修订记录另起新页，简短导读采用紧凑题头；不靠缩小正文挤页。

## 本轮实质变化

1. 需求与现金：台积电9月营收同比+54.6%、环比−0.6%，Q3月报加总环比+17.62%；APLD租金、装修与成本回收分别列示，集团简单现金桥约−2.011B。三星Q3仅为初步估计。

2. 融资与建设：SoftBank第三笔10B已经执行，本轮30B全部完成；CoreWeave印度扩容仍是计划，Jupiter补入完整当事方回应，Oracle购电安排保留监管条件。

3. 模型与工程：Haiku 5.5按单次请求长度分档，Sonnet缓存费下调；广告测试不当收入，AMD测试保留模型、速度门槛和预发布属性。

4. 宏观与日历：财政部10月8日十年期5.22%，较9月29日低4bp；9月就业转弱、前两月下修。新发布的纪要描述9月会议，不是10月决议。北京时间下一轮为10月14日CPI、15日台积电电话会及PPI、29日FOMC。

## 核验与源文件

原112项审计仍为：核验更新29、部分核验19、撤回20、历史待复核44。10月9日新增或补核13组证据另列，10月1日12组、9月24日10组及9月15日8组保留历史记录，均不计入原112项。

- [版本变更说明](../复审与版本记录/版本变更说明_2026-10-09.md)
- [增量引用核验](../复审与版本记录/引用核验报告_2026-10-09.md)
- [专业复审](../复审与版本记录/专业复审报告_2026-10-09.md)
- [PDF与目录核验](../复审与版本记录/PDF与目录核验报告_2026-10-09.md)
- [发布清单](../复审与版本记录/发布清单_2026-10-09.md)
- [算式检查](../复审与版本记录/V1.5.1_算式复核.json)
- [输入与产物哈希](../V1.5.1正文修订版/manifest.json)
- [结构与目录QA](../V1.5.1正文修订版/qa.json)

人工源位于`10_源码_markdown/V1.5.1正文修订/`，导出MD、HTML、PDF由同一源生成。历史V1.5、V1.4及339页档案保留，未声称被本轮逐页重核。

本轮仅维护研究报告与核验记录；未执行Git推送或外部发布。
'''
    (ROOT/'00_使用说明/当前文件总索引_2026-10-09.md').write_text(reading_index)

if __name__=='__main__':main()
