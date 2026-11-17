#!/usr/bin/env python3
"""Independent frozen-source review of V1.9 publication numbering.

The expected edits below come from source line-by-line review, not from the
implementation's CHAPTERS, REFERENCE_RULES, or metadata. No report is rendered.
Run --artifacts after the publication build to compare all emitted MD bodies.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).resolve().parent
BASELINE = ROOT / '复审与版本记录/V1.9_章节编号独立评审基线_20261031.json'
RESULT = ROOT / '复审与版本记录/V1.9_章节编号独立评审结果_20261031.json'
CN = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三']
# The report's intended complete reading order, independently recorded.
ORDER = {'profit': [1], 'circular': [2], 'monetization': [3], 'video': [4],
         'coding': [5], 'applications': [6], 'agi': [7, 8], 'china': [9],
         'valuation': [10], 'conclusion': [11], 'crash': [12], 'delay': [13]}
LABELS = {'第一部分': 1, '第二部分': 2, '第三部分': 3, '专题三': 4,
          '专题四': 5, '专题五': 6, '第四部分': 7, '第五部分': 8,
          '第六部分': 9, '第七部分': 10, '第八部分': 11, '专题一': 12, '专题二': 13}
PREFIX = {1: {1: 1}, 2: {2: 2}, 3: {3: 3}, 4: {4: 7, 5: 8},
          6: {6: 9}, 7: {7: 10}, 8: {8: 11}, 18: {18: 4},
          19: {19: 5}, 20: {20: 6}}
# Exact source-line locations were recorded before opening the implementation.
# Mapping only these tokens avoids touching adjacent data, quoted old forecasts,
# model versions, URLs, page numbers, or formulas.
LINE_EDITS = {
    3: {129: [('19.1', '5.1'), ('19.4', '5.4')], 165: [('19.6', '5.6')],
        171: [('19.3', '5.3')], 177: [('19.8', '5.8'), ('19.9', '5.11—5.12')],
        215: [('19.10', '5.10'), ('19.13', '5.13')],
        253: [('20.7', '6.7'), ('20.9', '6.9')]},
    4: {3: [('5.10', '8.10')], 48: [('见5.1。', '见8.1。')],
        **{321+i: [(f'| 4.{i} ', f'| 7.{i} ')] for i in range(1, 7)},
        **{327+i: [(f'| 5.{i} ', f'| 8.{i} ')] for i in range(1, 10)}},
    13: {37: [('19.1', '5.1'), ('19.6', '5.6')],
         41: [('第三、四部分', '第三章、第七章、第八章')], 43: [('18.2', '4.2')],
         47: [('18.8', '4.8')], 49: [('18.12', '4.12'), ('18.19', '4.19')],
         53: [('19.9', '5.9'), ('19.10', '5.10')],
         55: [('19.11', '5.11'), ('19.14', '5.14')]},
    18: {389: [('18.12', '4.12')]},
    19: {344: [('19.5', '5.5')]},
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent_expected(file_name, original):
    n = int(file_name[:2])
    lines = original.splitlines(keepends=True)
    for row, edits in LINE_EDITS.get(n, {}).items():
        for old, new in edits:
            assert lines[row-1].count(old) == 1, (file_name, row, old)
            lines[row-1] = lines[row-1].replace(old, new)
    text = ''.join(lines)
    text = re.sub(r'^(#{3,6} )(\d+)(\.\d+(?:\.\d+)*)(?=\s)',
                  lambda m: m[1]+str(PREFIX[n][int(m[2])])+m[3], text, flags=re.M)
    if n in (14, 15):
        text = re.sub(r'^### ([一二三四五六七八])、',
                      lambda m: f'### {n-2}.{CN.index(m[1])} ', text, flags=re.M)
    # All named references found in this baseline are current-report references.
    text = text.replace('专题三、四', '第四章、第五章').replace('专题四、五', '第五章、第六章')
    for label, chapter in LABELS.items():
        text = text.replace(label, f'第{CN[chapter]}章')
    text = text.replace('第3章', '第三章')
    return text


def extract_source(key, text):
    # Independently reproduce only source selection, never numbering logic.
    if key.startswith('short:'):
        blocks = re.split(r'<!-- EDITION:(\w+) -->', text)
        return dict(zip(blocks[1::2], blocks[2::2]))[key.split(':')[1]].strip()
    if key in ('framework', 'shale'):
        boundary = text.index('## 附篇C：')
        text = text[:boundary] if key == 'framework' else text[boundary:]
    text = re.sub(r'^# (?!#).*\n', '', text, count=1)
    return text.strip()


def chapters(text):
    return [CN.index(x) if x in CN else int(x)
            for x in re.findall(r'^## 第([一二三四五六七八九十]+|\d+)章', text, re.M)]


def all_links(text):
    return re.findall(r'\]\(([^\n]+?)\)', text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts', action='store_true')
    args = parser.parse_args()
    sys.path.insert(0, str(SCRIPT))
    spec = importlib.util.spec_from_file_location('reviewed_builder', SCRIPT/'build_v19_current.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    baseline = json.loads(BASELINE.read_text(encoding='utf-8'))
    problems, rows = [], []
    source_files = {k: v for k, v in baseline.items() if 'text' in v}
    for path, entry in source_files.items():
        if sha(ROOT/path) != entry['sha256']:
            problems.append('Frozen source changed: '+path)
    keys = list(dict.fromkeys(k for item in builder.CATALOG for k in item[2]))
    expected, raw = {}, {}
    for key in keys:
        path = builder.source_path(key)
        entry = baseline[str(path.relative_to(ROOT))]
        raw[key] = extract_source(key, entry['text'])
        expected[key] = extract_source(key, independent_expected(path.name, entry['text']))
        actual = builder.render_numbered_source(key, builder.source(key))
        if builder.source(key) != raw[key]:
            problems.append('Raw source() API changed: '+key)
        if actual != expected[key]:
            diff = '\n'.join(difflib.unified_diff(expected[key].splitlines(), actual.splitlines(),
                                               fromfile=key+':expected', tofile=key+':actual'))
            problems.append(diff)
        if all_links(raw[key]) != all_links(actual):
            problems.append('Link or image destination changed: '+key)
        if re.findall(r'`[^`]+`', raw[key]) != re.findall(r'`[^`]+`', actual):
            problems.append('Code literal changed: '+key)
        rows.append({'key': key, 'changed_lines': sum(a != b for a, b in zip(raw[key].splitlines(), actual.splitlines())),
                     'source_line_count': len(raw[key].splitlines()),
                     'output_line_count': len(actual.splitlines()), 'exact_expected_match': actual == expected[key],
                     'url_image_destinations_preserved': all_links(raw[key]) == all_links(actual)})
    editions = []
    for slug, _, edition_keys, _ in builder.CATALOG:
        want = '\n\n'.join(expected[k] for k in edition_keys)
        want = want.replace('../../13_全景版配图/', 'assets/').replace('(../../V1.6.1主题阅读版/', '(../V1.6.1主题阅读版/')
        actual = builder.publication_body(edition_keys)
        numbers = chapters(actual)
        want_numbers = [n for k in edition_keys for n in ORDER.get(k, [])]
        if actual != want:
            problems.append('Assembled publication body differs: '+slug)
        if numbers != want_numbers:
            problems.append(f'{slug}: chapter order {numbers} != {want_numbers}')
        chapter = None
        for line in actual.splitlines():
            if line.startswith('## '):
                ids = chapters(line)
                chapter = ids[0] if ids else None
            m = re.match(r'^#{3,6} (\d+)\.', line)
            if m and int(m[1]) != chapter:
                problems.append(f'{slug}: section does not match active chapter: {line}')
        note = builder.numbering_note(edition_keys)
        if '完整报告' not in note or (numbers and numbers != list(range(1, 14)) and '章号沿用完整报告' not in note):
            problems.append('Missing edition boundary note: '+slug)
        if re.search(r'专题[一二三四五]|第[一二三四五六七八]部分|^#{2,6} (?:18|19|20)\.', actual, re.M):
            problems.append('Old publication chapter alias survived: '+slug)
        if slug == '13_超全景版':
            if numbers != list(range(1, 14)):
                problems.append('Full report is not chapters 1 through 13')
            if re.findall(r'^## 附篇([A-F])', actual, re.M) != list('ABCDEF'):
                problems.append('Full report appendix order differs from A through F')
            # Every reviewed section reference, including unchanged references,
            # resolves to an actual heading in the complete report.
            labels = set(re.findall(r'^#{3,6} (\d+(?:\.\d+)+)(?=\s)', actual, re.M))
            reference_targets = {'2.5.3', '2.7.2', '2.8', '3.2', '3.3', '3.4', '3.5', '3.7',
                                 '4.2', '4.8', '4.12', '4.19', '8.10'}
            reference_targets |= {f'5.{n}' for n in range(1, 15)}
            reference_targets |= {f'6.{n}' for n in range(7, 10)}
            reference_targets |= {f'7.{n}' for n in range(1, 7)}
            reference_targets |= {f'8.{n}' for n in range(1, 10)}
            if reference_targets - labels:
                problems.append('Missing referenced sections: '+str(sorted(reference_targets-labels)))
        artifact_ok = None
        if args.artifacts:
            file = builder.OUT/(slug+'.md')
            document = file.read_text(encoding='utf-8')
            emitted = document.split('<!-- BODY_START -->', 1)[1].split('<!-- REFERENCES_START -->', 1)[0].strip()
            artifact_ok = emitted == want
            if not artifact_ok:
                problems.append('Emitted Markdown differs: '+slug)
            if note not in document:
                problems.append('Emitted Markdown lacks edition note: '+slug)
        editions.append({'slug': slug, 'chapter_order': numbers, 'body_exact_match': actual == want,
                         'emitted_markdown_exact_match': artifact_ok})
    result = {'status': 'PASS' if not problems else 'FAIL', 'artifacts_checked': args.artifacts,
              'baseline_sha256': sha(BASELINE), 'frozen_file_count': len(source_files),
              'builder_sha256': sha(SCRIPT/'build_v19_current.py'),
              'numbering_sha256': sha(SCRIPT/'numbering_v19.py'),
              'reviewer_script_sha256': sha(__file__), 'source_checks': rows,
              'editions': editions, 'problems': problems,
              'scope': 'Independent expected source transformations, exact text equality, frozen sources, links, literals, global chapter order, appendix order and selection boundaries. No market fact re-verification.'}
    RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('status', 'frozen_file_count', 'artifacts_checked', 'builder_sha256', 'numbering_sha256')}, ensure_ascii=False))
    for problem in problems:
        print(problem)
    return bool(problems)


if __name__ == '__main__':
    raise SystemExit(main())
