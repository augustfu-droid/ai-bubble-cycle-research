#!/usr/bin/env python3
"""Publication-only chapter numbering for the frozen V1.9 research sources.

Numbers in prose are deliberately NOT rewritten with a decimal-number regex.
Only heading labels, named chapter references, and the reviewed exact reference
fragments below may change. URLs, paths, code and the historical prediction
table are protected before any substitutions. source() remains the raw API.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

SCHEME = 'v19-contiguous-chapters-20261031'
CN = ('', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
      '十一', '十二', '十三')


@dataclass(frozen=True)
class Chapter:
    source_key: str
    old_label: str
    number: int
    old_section_prefix: str | None
    topic: str

    @property
    def label(self):
        return f'第{CN[self.number]}章'


CHAPTERS = (
    Chapter('profit', '第一部分', 1, '1', '利润真实性'),
    Chapter('circular', '第二部分', 2, '2', '循环投资网络'),
    Chapter('monetization', '第三部分', 3, '3', 'AI变现'),
    Chapter('video', '专题三', 4, '18', 'AI视频短剧'),
    Chapter('coding', '专题四', 5, '19', 'AI编程与软件劳动'),
    Chapter('applications', '专题五', 6, '20', '其他AI应用'),
    Chapter('agi', '第四部分', 7, '4', 'AGI'),
    Chapter('agi', '第五部分', 8, '5', '国际格局'),
    Chapter('china', '第六部分', 9, '6', '中国投资者传导'),
    Chapter('valuation', '第七部分', 10, '7', '公司分化与估值'),
    Chapter('conclusion', '第八部分', 11, '8', '综合结论'),
    Chapter('crash', '专题一', 12, None, '风险传导剧本'),
    Chapter('delay', '专题二', 13, None, '延迟与消化'),
)

# Shared references are resolved against the full report, even in a selection.
# Joint references must be matched as one unit before their individual aliases.
NAMED_REFERENCES = {
    '第三、四部分': '第三章、第七章',
    '专题三、四': '第四章、第五章',
    '专题四、五': '第五章、第六章',
    **{c.old_label: c.label for c in CHAPTERS},
    '第3章': '第三章',
}
NAMED_RE = re.compile('|'.join(map(re.escape, sorted(NAMED_REFERENCES, key=len, reverse=True))))


@dataclass(frozen=True)
class ReferenceRule:
    source_key: str
    old: str
    new: str
    targets: tuple[str, ...]
    kind: str = 'section_reference'


# Each entry was checked in its full paragraph. Longer fragments distinguish
# references from e.g. the old prediction's 19.5 billion, prices and versions.
REFERENCE_RULES = (
    ReferenceRule('monetization', '专题四19.1、19.4', '第五章5.1、5.4', ('5.1', '5.4')),
    ReferenceRule('monetization', '专题四19.6把专业付费人月', '第五章5.6把专业付费人月', ('5.6',)),
    ReferenceRule('monetization', '专题四19.3。', '第五章5.3。', ('5.3',)),
    ReferenceRule('monetization', '专题四19.8同时比较', '第五章5.8同时比较', ('5.8',)),
    ReferenceRule('monetization', '19.9再把人工复核和失败补救计入同质量交付成本',
                  '5.11—5.12再把人工复核和失败补救计入同质量交付成本', ('5.11', '5.12'),
                  'reference_target_correction'),
    ReferenceRule('monetization', '需求弹性见19.10—19.13', '需求弹性见5.10—5.13', ('5.10', '5.13')),
    ReferenceRule('monetization', '专题五20.7—20.9', '第六章6.7—6.9', ('6.7', '6.9')),
    ReferenceRule('agi', '5.10列明逐节观察范围', '8.10列明逐节观察范围', ('8.10',)),
    ReferenceRule('agi', '开放权重与许可边界见5.1。', '开放权重与许可边界见8.1。', ('8.1',)),
    ReferenceRule('audit', '市场证据见19.1—19.6', '市场证据见5.1—5.6', ('5.1', '5.6')),
    ReferenceRule('audit', '来源与许可原文见第三、四部分及技术更新记录',
                  '来源与许可原文见第三章、第七章、第八章及技术更新记录', ('3.7.1', '7.2', '8.1'),
                  'reference_target_correction'),
    ReferenceRule('audit', '来源与传播链详见18.2', '来源与传播链详见4.2', ('4.2',)),
    ReferenceRule('audit', '原件页码见18.8', '原件页码见4.8', ('4.8',)),
    ReferenceRule('audit', '18.12的120分钟', '4.12的120分钟', ('4.12',)),
    ReferenceRule('audit', '18.19价格减半', '4.19价格减半', ('4.19',)),
    ReferenceRule('audit', '19.9—19.10保留原始期间', '5.9—5.10保留原始期间', ('5.9', '5.10')),
    ReferenceRule('audit', '逐式复算见19.11—19.14', '逐式复算见5.11—5.14', ('5.11', '5.14')),
    ReferenceRule('video', '用18.12基准继续算', '用4.12基准继续算', ('4.12',)),
    ReferenceRule('coding', '与19.5的终端支出去重方法相容', '与5.5的终端支出去重方法相容', ('5.5',)),
    *(ReferenceRule('agi', f'| {old}.{n} {topic} |', f'| {new}.{n} {topic} |', (f'{new}.{n}',),
                    'section_index')
      for old, new, topics in (
          (4, 7, ('时间表', '任务能力与成本', '通用性与可用性', '供给与物理AI', '估值', '反证')),
          (5, 8, ('中美模型', '主权项目', '军事与安全', '就业', '电力', '制度', '硬件与生态', '出口', '反证')),
      ) for n, topic in enumerate(topics, 1)),
)

# Preserve each byte of destinations, code literals and raw HTML; only the
# visible label of a Markdown link remains eligible for reference rewriting.
# A balanced scan handles link destinations containing parentheses.
PROTECTED_RE = re.compile(
    r'(?P<fence>^[ \t]*(?P<mark>`{3,}|~{3,})[^\n]*\n.*?^[ \t]*(?P=mark)[ \t]*$)'
    r'|(?P<code>`+[^`\n]*`+)'
    r'|(?P<html><!--.*?-->|</?[A-Za-z][^>]*>)'
    r'|(?P<url>(?:https?://|mailto:)[^\s<>)\]）]+)'
    r'|(?P<path>(?:[A-Za-z]:[\\/]|\.\.?[/\\])[^\s<>)\]）]+)',
    re.M | re.S,
)
HISTORY_ROW_RE = re.compile(r'^\| (?:V1\.0|同分册|V1\.4合成源|V1\.5第3篇).*$', re.M)


def _protected_ranges(text: str, key: str):
    ranges = [(m.start(), m.end()) for m in PROTECTED_RE.finditer(text)]
    # Markdown inline-link destinations, including relative paths without ./.
    for match in re.finditer(r'\]\(', text):
        start = match.start() + 1
        i, depth = start + 1, 1
        while i < len(text) and depth:
            if text[i] == '\\':
                i += 2
                continue
            if text[i] == '(':
                depth += 1
            elif text[i] == ')':
                depth -= 1
            i += 1
        if depth == 0:
            ranges.append((start, i))
    if key == 'coding':
        ranges += [(m.start(), m.end()) for m in HISTORY_ROW_RE.finditer(text)]
    merged = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return merged


def _protect(text: str, key: str):
    if '\ue000' in text or '\ue001' in text:
        raise ValueError('Numbering placeholder characters already occur in source')
    protected = []
    parts, cursor = [], 0
    for start, end in _protected_ranges(text, key):
        parts.append(text[cursor:start])
        parts.append(f'\ue000{len(protected)}\ue001')
        protected.append(text[start:end])
        cursor = end
    parts.append(text[cursor:])
    return ''.join(parts), protected


def _restore(text: str, protected: list[str]):
    return re.sub('\ue000([0-9]+)\ue001', lambda m: protected[int(m[1])], text)


def render_numbered_source(key: str, source_text: str) -> str:
    """Convert one raw source() result; fail if a reviewed target has drifted."""
    text, protected = _protect(source_text, key)
    chapters = [c for c in CHAPTERS if c.source_key == key]
    for chapter in chapters:
        pattern = r'^## ' + re.escape(chapter.old_label) + r'(?=：)'
        text, count = re.subn(pattern, f'## {chapter.label}', text, flags=re.M)
        if count != 1:
            raise ValueError(f'{key}: expected one {chapter.old_label} heading, got {count}')

    prefixes = {c.old_section_prefix: str(c.number) for c in chapters if c.old_section_prefix}
    def section_heading(match):
        prefix = match['prefix']
        if prefix not in prefixes:
            raise ValueError(f'{key}: unreviewed numeric heading {match[0]}')
        return f'{match["hashes"]} {prefixes[prefix]}{match["rest"]}'
    text = re.sub(r'^(?P<hashes>#{3,6}) (?P<prefix>\d+)(?P<rest>\.\d+(?:\.\d+)*)(?=\s)',
                  section_heading, text, flags=re.M)
    if key in ('crash', 'delay'):
        number = chapters[0].number
        seen = []
        def scenario_heading(match):
            item = CN.index(match[1])
            seen.append(item)
            return f'### {number}.{item} '
        text = re.sub(r'^### ([一二三四五六七八])、', scenario_heading, text, flags=re.M)
        if seen != list(range(1, 9)):
            raise ValueError(f'{key}: scenario subsections changed: {seen}')

    for rule in REFERENCE_RULES:
        if rule.source_key != key:
            continue
        count = text.count(rule.old)
        if count != 1:
            raise ValueError(f'{key}: exact reference {rule.old!r} expected once, got {count}')
        text = text.replace(rule.old, rule.new)
    text = NAMED_RE.sub(lambda m: NAMED_REFERENCES[m[0]], text)
    return _restore(text, protected)


def rendered_chapters(keys):
    """Return chapter numbers in this edition's reading order, not file order."""
    return [c.number for key in keys for c in CHAPTERS if c.source_key == key]


def numbering_note(keys):
    numbers = rendered_chapters(keys)
    common = '本册章节采用完整报告统一编号，目录页码按本册正文生成。'
    if numbers == list(range(1, 14)):
        return common + '正文依次为第一章至第十三章，附篇沿用A—F标识。'
    if numbers:
        labels = '、'.join(f'第{CN[n]}章' for n in numbers)
        return common + f'本册按专题选编，收录{labels}，章号沿用完整报告；跳号表示未收录其余章节，阅读顺序依本册主题安排。跨章引用指向完整报告相应章节。'
    return common + '本册为导读或附篇，正文中的章号指向完整报告相应章节；附篇沿用A—F标识。'


def numbering_metadata():
    return {
        'scheme': SCHEME,
        'layer': 'publication_render_only; research source files and source() are unchanged',
        'selection_policy': 'all 20 editions share the complete report chapter numbers',
        'chapters': [{**asdict(c), 'published_label': c.label,
                      'published_section_prefix': str(c.number)} for c in CHAPTERS],
        'named_reference_map': dict(NAMED_REFERENCES),
        'exact_reference_rules': [asdict(r) for r in REFERENCE_RULES],
        'appendices': 'A-F unchanged',
        'protected_content': ['URLs and link destinations', 'paths', 'code literals',
                              'HTML', 'historical prediction table rows'],
        'decimal_policy': 'only numbered headings and reviewed exact reference fragments change',
    }
