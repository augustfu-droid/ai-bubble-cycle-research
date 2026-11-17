#!/usr/bin/env python3
"""Add scoped V1.10 research to the frozen V1.9 corpus without renumbering anchors."""
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
SRC = ROOT / '10_源码_markdown/V1.10_20261117'
OUT = ROOT / 'V1.10_配套发布_20261117'
REVIEW = ROOT / '复审与版本记录/V1.10_20261117'
VERSION = 'V1.10'
EDIT_DATE = '2026-11-17'
CUTOFF = '2026-10-31'
EMAIL = 'fqsx@mail.ustc.edu.cn'
EXTS = ['tables', 'fenced_code', 'footnotes', 'attr_list', 'sane_lists']
CATALOG = [
    ('full_zh', 'AI周期与泡沫研究_详细版_V1.10_20261117', 'zh', True),
    ('brief_zh', 'AI周期与泡沫研究_简版_V1.10_20261117', 'zh', False),
    ('full_en', 'AI_Cycles_and_Bubble_Full_Report_EN_V1.10_2026-11-17', 'en', True),
    ('brief_en', 'AI_Cycles_and_Bubble_Brief_EN_V1.10_2026-11-17', 'en', False),
]
PRIOR = {
    'zh': ROOT / 'V1.9现行正文版/13_超全景版.md',
    'en': en.OUT / (en.STEM + '.md'),
}
ENTRYPOINTS = {'README.md', 'CHANGELOG.md', 'AI泡沫研究报告/README.md'}
UPDATE_CHAPTERS = {1, 2, 8, 10, 12, 13}
CHINESE_NUMBERS = dict(enumerate(['一','二','三','四','五','六','七','八','九','十','十一','十二','十三','十四'], 1))
INSERT_RE = re.compile(r'\n\n<!-- V110_INSERT_START:([a-z0-9-]+) -->\n(.*?)\n<!-- V110_INSERT_END:\1 -->\n\n', re.S)
HISTORY = ROOT / '复审与版本记录/V1.9_拉取基线历史文件哈希_20261031.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def source_body(lang):
    return PRIOR[lang].read_text(encoding='utf-8').split('<!-- BODY_START -->', 1)[1].strip()


def required_sources(lang, full=True):
    names = [f'author_view_{lang}.md', f'event_chapter_{lang}.md', f'body_updates_{lang}.json'] if full else [f'brief_{lang}.md']
    return [SRC / name for name in names] + ([PRIOR[lang]] if full else [])


def chapter_bounds(body, lang):
    """Locate exact top-level headings, refusing missing, repeated or reordered chapters."""
    heads = list(re.finditer(r'^## (.+)$', body, re.M))
    result = {}
    sequence = []
    for i, h in enumerate(heads):
        title = h[1]
        m = re.match(r'^第([一二三四五六七八九十]+)章[：:]', title) if lang == 'zh' else re.match(r'^Chapter (\d+):', title)
        if m:
            n = next((k for k, v in CHINESE_NUMBERS.items() if v == m[1]), None) if lang == 'zh' else int(m[1])
            assert n is not None and n not in result, 'Invalid/duplicate chapter: ' + title
            result[n] = (h.start(), heads[i+1].start() if i+1 < len(heads) else len(body))
            sequence.append(n)
    assert sequence == list(range(1, 14)), f'Expected frozen chapters 1-13: {sequence}'
    appendix = '附篇A' if lang == 'zh' else 'Appendix A'
    boundary = result[13][1]
    assert body[boundary:].startswith('## ' + appendix), 'Chapter 13 must immediately precede Appendix A'
    return result


def inserted_block(key, text):
    assert 'V110_INSERT_' not in text, 'Reserved insertion marker in author input'
    return f'\n\n<!-- V110_INSERT_START:{key} -->\n{text.strip()}\n<!-- V110_INSERT_END:{key} -->\n\n'


def strip_insertions(body):
    return INSERT_RE.sub('', body)


def compose_body(lang):
    original = source_body(lang)
    assert 'V110_INSERT_' not in original
    bounds = chapter_bounds(original, lang)
    updates = json.loads((SRC / f'body_updates_{lang}.json').read_text(encoding='utf-8-sig'))
    assert isinstance(updates, list) and len(updates) == len(UPDATE_CHAPTERS)
    assert {r['chapter'] for r in updates} == UPDATE_CHAPTERS, 'Expected one update for chapters 1/2/8/10/12/13'
    additions = {}
    for row in updates:
        assert set(row) == {'chapter', 'heading', 'markdown'} and type(row['chapter']) is int
        heading, content = row['heading'].strip(), row['markdown'].strip()
        assert heading and content and '\n' not in heading
        assert not re.match(r'^(?:#|\d+[.、 ])', heading), 'Update heading must be unnumbered plain text'
        assert not re.search(r'^#{1,3} ', content, re.M), 'Update content may use only h4 or lower headings'
        assert ('11月17日' in heading if lang == 'zh' else re.search(r'(?:17 November|November 17)', heading)), 'Date-scope update heading required'
        additions[bounds[row['chapter']][1]] = inserted_block(f'chapter-{row["chapter"]}', f'### {heading}\n\n{content}')
    event = (SRC / f'event_chapter_{lang}.md').read_text(encoding='utf-8').strip()
    required = r'^## 第十四章[：:]' if lang == 'zh' else r'^## Chapter 14:'
    assert re.match(required, event), 'Event source must begin with chapter 14 heading'
    assert len(re.findall(r'^## ', event, re.M)) == 1 and not re.search(r'^# ', event, re.M)
    boundary = bounds[13][1]
    additions[boundary] += inserted_block('chapter-14', event)
    body = original
    for pos in sorted(additions, reverse=True):
        body = body[:pos] + additions[pos] + body[pos:]
    assert strip_insertions(body) == original, 'Insertion round trip altered original corpus'
    assert len(INSERT_RE.findall(body)) == 7
    return body


def full_body_html(body, lang):
    """Tag the complete render, retaining every original h-* ID and cross-reference."""
    rendered = render_md(body)
    counter, new_counter, active = 0, 0, False
    headings = []
    token = re.compile(r'<!-- V110_INSERT_(START|END):([a-z0-9-]+) -->|<h([1-6])[^>]*>(.*?)</h\3>', re.S)
    def tag(m):
        nonlocal counter, new_counter, active
        if m[1]:
            assert active != (m[1] == 'START'), 'Invalid insertion nesting'
            active = m[1] == 'START'
            return m[0]
        level, inner = int(m[3]), m[4]
        anchor = f'update-{new_counter:04d}' if active else f'h-{counter:04d}'
        if active:
            new_counter += 1
        else:
            counter += 1
        headings.append({'level': level, 'text': html.unescape(re.sub('<[^>]+>', '', inner)), 'anchor': anchor})
        return f'<h{level} id="{anchor}">{inner}</h{level}>'
    rendered = token.sub(tag, rendered)
    assert not active
    if lang == 'en' and '<!-- V110_INSERT_START:chapter-14 -->' in body:
        # Scope the layout fix to Chapter 14.4's one uniquely headed new table.
        table_start = '<table>\n<thead>\n<tr>\n<th>Purpose of commitment</th>'
        assert rendered.count(table_start) == 1, 'Expected exactly one new commitments table'
        rendered = rendered.replace(table_start, '<table class="event-commitments"><colgroup>'
            '<col style="width:48%"><col style="width:16%"><col style="width:8%">'
            '<col style="width:8%"><col style="width:12%"><col style="width:8%">'
            '</colgroup>\n<thead>\n<tr>\n<th>Purpose of commitment</th>', 1)
    _, prior_headings = numbered_html(source_body(lang))
    assert [h for h in headings if h['anchor'].startswith('h-')] == prior_headings, 'Original anchors drifted'
    return rendered, headings


def freeze_baseline():
    REVIEW.mkdir(parents=True, exist_ok=True)
    path = REVIEW / 'baseline.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    manifests = ['V1.8-publication-files.json', 'V1.9-publication-files.json', 'V1.9-English-publication-files.json', 'V1.9.1-publication-files.json', 'V1.9.2-publication-files.json']
    rows = []
    for name in manifests:
        old = json.loads((REPO / name).read_text(encoding='utf-8'))
        for row in old['files']:
            if row['path'] not in ENTRYPOINTS:
                assert sha(REPO / row['path']) == row['sha256'], 'Prior publication has changed: ' + row['path']
            rows.append(dict(row, source_manifest=name, mutable_entrypoint=row['path'] in ENTRYPOINTS))
    result = {
        'scope': 'Preserve all previous research, translations, artifacts and review records. Only three repository navigation/change-log files may be updated.',
        'manifests': {name: sha(REPO / name) for name in manifests},
        'files': rows,
        'full_bodies': {lang: {'source': str(path.relative_to(REPO)), 'source_sha256': sha(path), 'body_sha256': digest(source_body(lang))} for lang, path in PRIOR.items()},
        'historical_baseline_sha256': sha(HISTORY),
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
    text = text.replace('V1.9 · 2026-10-31', 'V1.10 · 2026-11-17')
    text = text.replace('V1.9 English | 2026-10-31', 'V1.10 | 2026-11-17')
    text += '''
.author-view{break-after:page}.author-view h2{margin-top:10pt}.author-view h3{font-size:11.5pt;margin:11pt 0 5pt}.author-view p{margin:6pt 0}
.author-view h2{bookmark-level:1}.author-view h3{bookmark-level:2}
.author-view table:nth-of-type(2),.brief-body table:nth-of-type(2){table-layout:fixed}
.author-view table:nth-of-type(2) th:first-child,.brief-body table:nth-of-type(2) th:first-child{min-width:0;width:16%}
.author-view table:nth-of-type(2) th:not(:first-child),.brief-body table:nth-of-type(2) th:not(:first-child){width:42%}
.edition-note{break-after:page;font-size:9.4pt;line-height:1.65}.edition-note h2{font-size:14pt}.edition-note p{margin:9pt 0}
.cover .thesis{font-size:16pt;font-weight:700;color:#315e7c;margin-top:15mm;line-height:1.5}
.cover h1{margin-top:18mm}.cover .edition{margin-top:14mm}
.toc a{position:relative;padding-right:3.4em}.toc a:after{position:absolute;right:0;bottom:4pt;float:none}
.brief-header{padding-bottom:8pt;border-bottom:1pt solid #9dbed2;margin-bottom:13pt}.brief-header h1{margin:0 0 8pt;font-size:24pt}.brief-header p{font-size:9pt;color:#607b8e;margin:4pt 0}
.brief-note{font-size:8.5pt;color:#607b8e;border-top:.6pt solid #c9dce7;padding-top:8pt;margin-top:18pt}
'''
    if not full:
        text += 'main h2{font-size:15pt;margin-top:17pt}main h3{font-size:11.6pt;margin-top:13pt}main p{margin:7pt 0}'
    if lang == 'en':
        text += '.author-view table:nth-of-type(2) th:first-child,.brief-body table:nth-of-type(2) th:first-child{width:20%}.author-view table:nth-of-type(2) th:not(:first-child),.brief-body table:nth-of-type(2) th:not(:first-child){width:40%}'
        if full:
            text += '.event-commitments{table-layout:fixed}.event-commitments th{overflow-wrap:normal}.event-commitments th:nth-child(3),.event-commitments th:nth-child(4),.event-commitments th:nth-child(6){white-space:nowrap}.event-commitments td:not(:first-child){white-space:nowrap}'
    return text


def note(lang):
    if lang == 'zh':
        return '''## 版本与阅读说明

本版编辑日期为2026年11月17日（北京时间）。原研究资料范围仍截至2026年10月31日；11月17日新增专题、对应章节更新及开篇判断另行标明资料日期。这是按主题增加的研究，不代表全报告财务数据与全部旧来源都在11月17日重新核查。各事实保留自身报告期、观察日与证据限制。

本版保留V1.9完整报告的原13章、附篇A至F、全部原图表与参考资料，在第1、2、8、10、12、13章末追加有日期标记的更新，并在附篇A之前新增第14章。原参考目录342项保留；新增19个去重来源链接列于本次更新段落，当前全文共361个去重引用网址。开篇保留风险时间窗与两张矩阵；时间窗仍为作者主观判断，沿用V1.9.1于2026年11月1日重新登记的预测及结算约束，不恢复已撤回的概率或跌幅。原有预测复盘、事实限制与反方证据保留；旧正文所述“本轮”及V1.9资料范围按原文理解。

读者可先看作者观点，再按目录查阅第14章与相关章节更新，并回查现金回收、GPU折旧、短剧、编程及其他专题的原有依据。简版与详细版同步表达判断及资料边界，篇幅不同。

## 免责声明

本报告为“大队长”基于公开资料形成的个人研究，不代表任何任职机构，不构成个性化投资建议、收益保证或交易指令。作者判断可能错误；公司指引、作者算例与已实现结果分别标明。完整证据与限制以正文对应段落为准。
'''
    return '''## Edition and reading note

The editorial date is 17 November 2026, Beijing time. The original research scope remains through 31 October 2026. The new topic, dated chapter updates and related opening judgments use separately identified evidence through 17 November. This is a topic-specific addition, not a claim that all financial data or historical sources have been checked again on 17 November. Each fact retains its reporting period, observation date and evidentiary limitations.

The original 13 chapters, Appendices A-F, figures and references of V1.9 are retained. Dated updates are appended to Chapters 1, 2, 8, 10, 12 and 13, and a new Chapter 14 precedes Appendix A. The original reference index retains its 342 entries; 19 additional unique source links appear in the dated additions, bringing the full report to 361 unique cited URLs. The opening retains the risk window and both matrices. The timing window remains the author's subjective judgment, with the forecast registered in V1.9.1 on 1 November 2026 and its settlement condition preserved; withdrawn probabilities or drawdown estimates are not reinstated. Earlier forecast reviews, limitations and counterevidence remain in place. References in the original body to this research round or to V1.9 keep their original scope.

Read the author's views first, then use the contents to examine Chapter 14, the dated updates and the original evidence on capital recovery, GPU depreciation, microdramas, coding and other topics. The brief and full report share the same judgments and evidence boundaries.

## Disclaimer

This is Daduizhang's personal research based on public information. It does not represent an employer or provide personalized investment advice, a return guarantee or a trading instruction. The author's judgments may be wrong. Company guidance, author-constructed examples and realized results are identified separately; the relevant passages govern the evidence and its limitations.
'''


def build(item):
    key, stem, lang, full = item
    author = '大队长' if lang == 'zh' else 'Daduizhang'
    title = ('AI周期与泡沫研究 · ' + ('详细版' if full else '简版')) if lang == 'zh' else ('AI Cycles and the Bubble: ' + ('Full Research Report' if full else 'Brief'))
    preface = (SRC / f'author_view_{lang}.md').read_text(encoding='utf-8').strip() if full else ''
    body = compose_body(lang) if full else (SRC / f'brief_{lang}.md').read_text(encoding='utf-8').strip()
    if not full:
        body = re.sub(r'^# (?!#)[^\n]*\n+', '', body, count=1)
    rendered, headings = full_body_html(body, lang) if full else numbered_html(body)
    if full:
        rendered = rendered.replace('<!-- REFERENCES_START -->', '<section class="references">') + '</section>'
    intro, intro_headings = numbered_html(preface, 'view') if full else ('', [])
    toc = ''
    if full:
        toc_title = '目录' if lang == 'zh' else 'Contents'
        toc_note = '正文连续编为第1至14章，附篇保留A至F；有日期标记的小节为本次增量更新。页码与链接对应本次详细版。' if lang == 'zh' else 'Chapters run from 1 to 14, followed by Appendices A-F. Dated sections identify this edition’s additions. Page numbers and links refer to this revised full edition.'
        toc = f'<nav class="toc"><h1>{toc_title}</h1><p>{toc_note}</p>'
        toc += ''.join(f'<a class="l{h["level"]}" href="#{h["anchor"]}">{html.escape(h["text"])}</a>' for h in intro_headings + headings if h['level'] <= 3) + '</nav>'
    contact = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    if lang == 'zh':
        subtitle = '核心观点、时间情景与领导层事件和融资传导专题'
        thesis = '延迟即放大：回款追不上持续投入时，风险会继续累积。'
        metadata = 'V1.10 · 专题增量修订<br>编辑：2026年11月17日<br>原研究：截至2026年10月31日<br>本次专题增量：截至2026年11月17日'
        foot = '大队长 · 独立研究<br>资料按各自报告期使用 · 作者判断与事实分别说明<br>' + contact
        brief_note = '编辑：2026-11-17；原研究截至2026-10-31，新增专题与相关判断截至2026-11-17，不代表全报告重核。与详细版配套阅读。个人研究，不构成投资建议。'
    else:
        subtitle = 'Core judgments, timing scenarios, leadership events and financing transmission'
        thesis = 'Delay amplifies risk when cash receipts fail to catch up with continuing investment.'
        metadata = 'V1.10 | Topic-specific research update<br>Edited: 17 November 2026<br>Original research: through 31 October 2026<br>New topic: through 17 November 2026'
        foot = 'Daduizhang | Independent research<br>Reporting periods and evidence limitations are preserved.<br>' + contact
        brief_note = 'Edited: 17 November 2026. Original research through 31 October; new topic and related judgments through 17 November. This is not a whole-report recheck. Companion to the full report. Personal research; not investment advice.'
    if full:
        cover = f'<section class="cover"><div class="line rule"></div><div class="brand">{author} | {VERSION}</div><h1>{html.escape(title)}</h1><p class="subtitle">{subtitle}</p><p class="thesis">{thesis}</p><p class="edition">{metadata}</p><div class="foot">{foot}</div></section>'
        front = f'<section class="author-view">{intro}</section><section class="edition-note">{render_md(note(lang))}</section>'
    else:
        cover = f'<header class="brief-header"><h1>{html.escape(title)}</h1><p>{author} | {VERSION} | {EDIT_DATE} | {contact}</p><p>{subtitle}</p></header>'
        front = ''
    water = '大队长出品' if lang == 'zh' else 'DADUIZHANG'
    main = rendered + ('' if full else f'<p class="brief-note">{brief_note}</p>')
    page = f'<!doctype html><html lang="{"zh-CN" if lang == "zh" else "en"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="{author}"><title>{html.escape(title)}</title><style>{styles(lang,full)}</style></head><body><div class="watermark" aria-hidden="true">{water}</div>{cover}{front}{toc}<main class="{"report-body" if full else "brief-body"}">{main}</main></body></html>'
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
        'body_sha256': digest(body), 'prior_body_preserved': full and strip_insertions(body) == source_body(lang),
        'inserted_blocks': len(INSERT_RE.findall(body)) if full else 0,
        'original_anchor_count': sum(h['anchor'].startswith('h-') for h in headings) if full else 0,
        'source_files': {str(p.relative_to(REPO)): sha(p) for p in required_sources(lang, full)},
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
    missing = sorted({str(p) for item in CATALOG if args.only is None or item[0] in args.only for p in required_sources(item[2], item[3]) if not p.is_file()})
    if missing:
        raise SystemExit('Missing author inputs; no placeholder artifacts generated:\n' + '\n'.join(missing))
    OUT.mkdir(parents=True, exist_ok=True)
    prepare_assets()
    path = OUT / 'manifest.json'
    rows = {r['key']: r for r in json.loads(path.read_text(encoding='utf-8'))['reports']} if path.exists() else {}
    for item in CATALOG:
        if args.only is None or item[0] in args.only:
            rows[item[0]] = build(item)
    record = {
        'version': VERSION, 'editorial_date': EDIT_DATE, 'original_research_cutoff': CUTOFF, 'topic_update_cutoff': EDIT_DATE,
        'scope': 'Topic-specific additions in Chapters 1/2/8/10/12/13 and new Chapter 14, synchronized author views and briefs. Removing exactly seven marked additions restores the frozen V1.9 body verbatim. Original h-* anchors, figures and references are retained. No claim of a whole-report 17 November recheck.',
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
