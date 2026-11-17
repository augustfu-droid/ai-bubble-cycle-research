#!/usr/bin/env python3
"""Publish an editorial revision and a standalone brief from the reviewed V1.9 corpus."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

import fitz
import markdown
import build_v19_current as zh
import build_v19_english as en

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
SRC = ROOT / '10_源码_markdown/V1.9.1_观点与简版_20261101'
OUT = ROOT / 'V1.9.1_配套发布_20261101'
REVIEW = ROOT / '复审与版本记录/V1.9.1_20261101'
VERSION = 'V1.9.1'
EDIT_DATE = '2026-11-01'
CUTOFF = '2026-10-31'
EMAIL = 'fqsx@mail.ustc.edu.cn'
EXTS = ['tables', 'fenced_code', 'footnotes', 'attr_list', 'sane_lists']
CATALOG = [
    ('full_zh', 'AI周期与泡沫研究_详细版_20261101', 'zh', True),
    ('brief_zh', 'AI周期与泡沫研究_简版_20261101', 'zh', False),
    ('full_en', 'AI_Cycles_and_Bubble_Full_Report_EN_2026-11-01', 'en', True),
    ('brief_en', 'AI_Cycles_and_Bubble_Brief_EN_2026-11-01', 'en', False),
]
PRIOR = {
    'zh': ROOT / 'V1.9现行正文版/13_超全景版.md',
    'en': en.OUT / (en.STEM + '.md'),
}
ENTRYPOINTS = {'README.md', 'CHANGELOG.md', 'AI泡沫研究报告/README.md'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def source_body(lang):
    return PRIOR[lang].read_text(encoding='utf-8').split('<!-- BODY_START -->', 1)[1].strip()


def freeze_baseline():
    REVIEW.mkdir(parents=True, exist_ok=True)
    path = REVIEW / 'baseline.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    manifests = ['V1.9-publication-files.json', 'V1.9-English-publication-files.json']
    rows = []
    for name in manifests:
        old = json.loads((REPO / name).read_text(encoding='utf-8'))
        for row in old['files']:
            assert sha(REPO / row['path']) == row['sha256'], 'Prior publication has changed: ' + row['path']
            rows.append(dict(row, source_manifest=name, mutable_entrypoint=row['path'] in ENTRYPOINTS))
    result = {
        'scope': 'Preserve all previous research, translations, artifacts and review records. Only three repository navigation/change-log files may be updated.',
        'manifests': {name: sha(REPO / name) for name in manifests},
        'files': rows,
        'full_bodies': {lang: {'source': str(path.relative_to(REPO)), 'source_sha256': sha(path), 'body_sha256': digest(source_body(lang))} for lang, path in PRIOR.items()},
    }
    write_json(path, result)
    return result


def prepare_assets():
    dest = OUT / 'assets'
    dest.mkdir(parents=True, exist_ok=True)
    for origin in (zh.OUT / 'assets', en.OUT / 'assets'):
        for p in origin.glob('*.svg'):
            target = dest / p.name
            if target.exists():
                assert target.read_bytes() == p.read_bytes(), 'Conflicting figure names'
            else:
                shutil.copy2(p, target)


def render_md(text):
    return markdown.markdown(text, extensions=EXTS)


def numbered_html(text, prefix='h'):
    rendered, headings = zh.tag_headings(render_md(text))
    if prefix != 'h':
        rendered = re.sub(r'id="h-(\d+)"', rf'id="{prefix}-\1"', rendered)
        for h in headings:
            h['anchor'] = h['anchor'].replace('h-', prefix + '-', 1)
    return rendered, headings


def styles(lang, full):
    text = zh.css('AI周期与泡沫研究') if lang == 'zh' else en.css()
    text = text.replace('V1.9 · 2026-10-31', 'V1.9.1 · 2026-11-01')
    text = text.replace('V1.9 English | 2026-10-31', 'V1.9.1 | 2026-11-01')
    text += '''
.author-view{break-after:page}.author-view h2{margin-top:10pt}.author-view h3{font-size:11.5pt;margin:11pt 0 5pt}.author-view p{margin:6pt 0}
.author-view h2{bookmark-level:1}.author-view h3{bookmark-level:2}
.edition-note{break-after:page;font-size:9.4pt;line-height:1.65}.edition-note h2{font-size:14pt}.edition-note p{margin:9pt 0}
.cover .thesis{font-size:16pt;font-weight:700;color:#315e7c;margin-top:15mm;line-height:1.5}
.cover h1{margin-top:18mm}.cover .edition{margin-top:14mm}
.toc a{position:relative;padding-right:3.4em}.toc a:after{position:absolute;right:0;bottom:4pt;float:none}
.brief-header{padding-bottom:8pt;border-bottom:1pt solid #9dbed2;margin-bottom:13pt}.brief-header h1{margin:0 0 8pt;font-size:24pt}.brief-header p{font-size:9pt;color:#607b8e;margin:4pt 0}
.brief-note{font-size:8.5pt;color:#607b8e;border-top:.6pt solid #c9dce7;padding-top:8pt;margin-top:18pt}
'''
    if not full:
        text += 'main h2{font-size:15pt;margin-top:17pt}main h3{font-size:11.6pt;margin-top:13pt}main p{margin:7pt 0}'
    return text


def note(lang):
    if lang == 'zh':
        return '''## 版本与阅读说明

这次修订将作者的核心观点放到最前面，并重写一份可以独立阅读、与详细版配套发送的简版。编辑日期为2026年11月1日；研究资料仍截止2026年10月31日（北京时间），各事实保留自身报告期与观察日。

本版沿用V1.9大完整报告的13章、附篇A至F、图表和参考资料。新增开篇是作者对现有证据的综合判断，并于2026年11月1日重新登记主观时间预测；这不是新一轮财报更新。第12、13章继续提供原有机制与压力测试，并未建立日期预测模型。新增时间窗由作者判断承担，不恢复旧稿已撤回的概率、跌幅或前提。原有预测复盘、事实限制与反方证据继续保留；正文所述“本轮”及V1.9研究范围仍按原文理解。

读者可先看作者观点，再按目录查阅现金回收、GPU折旧、短剧、编程及其他专题的依据。简版与详细版采用相同立场和资料时点，篇幅不同。

## 免责声明

本报告为“大队长”基于公开资料形成的个人研究，不代表任何任职机构，不构成个性化投资建议、收益保证或交易指令。作者判断可能错误；公司指引、作者算例与已实现结果分别标明。完整证据与限制以正文对应段落为准。
'''
    return '''## Edition and reading note

This revision brings the author's central thesis to the front and adds a self-contained brief for distribution alongside the full report. The editorial date is 1 November 2026. The research cutoff remains 31 October 2026, Beijing time; each fact retains its own reporting period or observation date.

The 13 chapters, Appendices A-F, figures and references of the complete V1.9 report are retained. The new opening synthesizes the existing evidence and registers a new subjective timing forecast on 1 November 2026; it is not a fresh earnings update. Chapters 12 and 13 retain their mechanism analysis and stress tests, without a model that predicts dates. The timing windows are the author's judgment and do not reinstate withdrawn probabilities, drawdown estimates or assumptions. Earlier forecast reviews, evidence limitations and counterevidence remain in place. References within the body to this research round or to V1.9 retain their original scope.

Read the author's views first, then use the contents to examine the evidence on capital recovery, GPU depreciation, microdramas, coding and other topics. The brief and full report share the same thesis and research cutoff.

## Disclaimer

This is Daduizhang's personal research based on public information. It does not represent an employer or provide personalized investment advice, a return guarantee or a trading instruction. The author's judgments may be wrong. Company guidance, author-constructed examples and realized results are identified separately; the relevant passages govern the evidence and its limitations.
'''


def build(item):
    key, stem, lang, full = item
    author = '大队长' if lang == 'zh' else 'Daduizhang'
    title = ('AI周期与泡沫研究 · ' + ('详细版' if full else '简版')) if lang == 'zh' else ('AI Cycles and the Bubble: ' + ('Full Research Report' if full else 'Brief'))
    preface = (SRC / f'author_view_{lang}.md').read_text(encoding='utf-8').strip() if full else ''
    body = source_body(lang) if full else (SRC / f'brief_{lang}.md').read_text(encoding='utf-8').strip()
    if not full:
        body = re.sub(r'^# (?!#)[^\n]*\n+', '', body, count=1)
    rendered, headings = numbered_html(body)
    if full:
        rendered = rendered.replace('<!-- REFERENCES_START -->', '<section class="references">') + '</section>'
    intro, intro_headings = numbered_html(preface, 'view') if full else ('', [])
    toc = ''
    if full:
        toc_title = '目录' if lang == 'zh' else 'Contents'
        toc_note = '正文连续编为第1至13章，附篇保留A至F；页码与链接对应本次详细版。' if lang == 'zh' else 'Chapters run from 1 to 13, followed by Appendices A-F. Page numbers and links refer to this revised full edition.'
        toc = f'<nav class="toc"><h1>{toc_title}</h1><p>{toc_note}</p>'
        toc += ''.join(f'<a class="l{h["level"]}" href="#{h["anchor"]}">{html.escape(h["text"])}</a>' for h in intro_headings + headings if h['level'] <= 3) + '</nav>'
    contact = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    if lang == 'zh':
        subtitle = '资本回收、GPU折旧与AI应用的真实进展'
        thesis = '延迟即放大：回款追不上持续投入时，风险会继续累积。'
        metadata = 'V1.9.1 · 作者观点修订<br>编辑：2026年11月1日<br>资料截止：2026年10月31日'
        foot = '大队长 · 独立研究<br>资料按各自报告期使用 · 作者判断与事实分别说明<br>' + contact
        brief_note = '编辑：2026-11-01；资料截止：2026-10-31。与详细版配套阅读。个人研究，不构成投资建议。'
    else:
        subtitle = 'Capital recovery, GPU depreciation and the progress of AI applications'
        thesis = 'Delay amplifies risk when cash receipts fail to catch up with continuing investment.'
        metadata = 'V1.9.1 | Author-thesis revision<br>Edited: 1 November 2026<br>Research cutoff: 31 October 2026'
        foot = 'Daduizhang | Independent research<br>Reporting periods and evidence limitations are preserved.<br>' + contact
        brief_note = 'Edited: 1 November 2026. Research cutoff: 31 October 2026. Companion to the full report. Personal research; not investment advice.'
    if full:
        cover = f'<section class="cover"><div class="line rule"></div><div class="brand">{author} | {VERSION}</div><h1>{html.escape(title)}</h1><p class="subtitle">{subtitle}</p><p class="thesis">{thesis}</p><p class="edition">{metadata}</p><div class="foot">{foot}</div></section>'
        front = f'<section class="author-view">{intro}</section><section class="edition-note">{render_md(note(lang))}</section>'
    else:
        cover = f'<header class="brief-header"><h1>{html.escape(title)}</h1><p>{author} | {VERSION} | {EDIT_DATE} | {contact}</p><p>{subtitle}</p></header>'
        front = ''
    water = '大队长出品' if lang == 'zh' else 'DADUIZHANG'
    main = rendered + ('' if full else f'<p class="brief-note">{brief_note}</p>')
    page = f'<!doctype html><html lang="{"zh-CN" if lang == "zh" else "en"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="{author}"><title>{html.escape(title)}</title><style>{styles(lang,full)}</style></head><body><div class="watermark" aria-hidden="true">{water}</div>{cover}{front}{toc}<main>{main}</main></body></html>'
    md = f'# {title}\n\n{author} | {VERSION} | {EDIT_DATE}\n\n' + (preface + '\n\n' + note(lang) + '\n\n' if full else '') + '<!-- BODY_START -->\n\n' + body + '\n'
    if not full:
        md += '\n' + brief_note + '\n'
    hp, mp, pdf = (OUT / (stem + ext) for ext in ('.html', '.md', '.pdf'))
    mp.write_text(md, encoding='utf-8')
    hp.write_text(page, encoding='utf-8')
    zh.render_pdf(hp, pdf)
    with fitz.open(pdf) as doc:
        pages = len(doc)
    result = {
        'key': key, 'stem': stem, 'language': lang, 'full': full, 'pages': pages,
        'headings': intro_headings + headings, 'reference_count': len(zh.reference_entries(body)),
        'body_sha256': digest(body), 'prior_body_identical': full and body == source_body(lang),
        'source_files': {str(p.relative_to(REPO)): sha(p) for p in ([SRC / f'author_view_{lang}.md', PRIOR[lang]] if full else [SRC / f'brief_{lang}.md'])},
        'outputs': {p.suffix[1:]: {'path': str(p.relative_to(REPO)), 'sha256': sha(p)} for p in (mp, hp, pdf)},
    }
    print(json.dumps({'report': key, 'pages': pages, 'references': result['reference_count']}, ensure_ascii=False), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', nargs='*', choices=[r[0] for r in CATALOG])
    parser.add_argument('--freeze-only', action='store_true')
    args = parser.parse_args()
    baseline = freeze_baseline()
    if args.freeze_only:
        print(f'Frozen {len(baseline["files"])} prior publication entries.')
        return
    OUT.mkdir(parents=True, exist_ok=True)
    prepare_assets()
    path = OUT / 'manifest.json'
    rows = {r['key']: r for r in json.loads(path.read_text(encoding='utf-8'))['reports']} if path.exists() else {}
    for item in CATALOG:
        if args.only is None or item[0] in args.only:
            rows[item[0]] = build(item)
    record = {
        'version': VERSION, 'editorial_date': EDIT_DATE, 'research_cutoff': CUTOFF,
        'scope': 'Author thesis restored to the front; a standalone brief in each language. Full research bodies are byte-identical to the prior reviewed publication after the BODY_START marker.',
        'status': 'BUILT_PENDING_REVIEW', 'remote_push_performed': False,
        'builder_sha256': sha(__file__),
        'dependencies': {str(p.relative_to(REPO)): sha(p) for p in (Path(zh.__file__), Path(en.__file__))},
        'baseline_sha256': sha(REVIEW / 'baseline.json'),
        'assets': {p.name: sha(p) for p in (OUT / 'assets').glob('*.svg')},
        'reports': [rows[item[0]] for item in CATALOG if item[0] in rows],
    }
    write_json(path, record)


if __name__ == '__main__':
    main()
