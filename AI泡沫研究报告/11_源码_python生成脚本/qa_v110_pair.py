#!/usr/bin/env python3
"""Check preserved V1.9 research, scoped additions, PDF navigation and visual samples."""
from __future__ import annotations
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote
import fitz
import build_v110_pair as b
from qa_v19_current import Parser, CHINESE_CHAPTERS


def norm(text):
    return re.sub(r'\s+', '', text).replace('\u00ad', '')


def main():
    mf = json.loads((b.OUT / 'manifest.json').read_text(encoding='utf-8'))
    baseline = json.loads((b.REVIEW / 'baseline.json').read_text(encoding='utf-8'))
    errors = []
    unchanged = []
    entrypoints = []
    for row in baseline['files']:
        path = b.REPO / row['path']
        if row['mutable_entrypoint']:
            entrypoints.append(row['path'])
        elif b.sha(path) != row['sha256']:
            errors.append('Prior artifact changed: ' + row['path'])
        else:
            unchanged.append(row['path'])
    for name, digest in baseline['manifests'].items():
        if b.sha(b.REPO / name) != digest:
            errors.append('Prior publication manifest changed: ' + name)
    history = json.loads(b.HISTORY.read_text(encoding='utf-8'))
    if b.sha(b.HISTORY) != baseline['historical_baseline_sha256']:
        errors.append('Historical baseline manifest changed')
    for path, row in history['files'].items():
        if b.sha(b.REPO / path) != row['working_tree_sha256']:
            errors.append('Historical file changed: ' + path)
    if len(history['files']) != 636:
        errors.append('Expected 636 historical files')
    if b.sha(b.REVIEW / 'baseline.json') != mf['baseline_sha256']:
        errors.append('Frozen baseline changed after build')
    if b.sha(b.__file__) != mf['builder_sha256']:
        errors.append('Builder changed after build')
    for path, digest in mf['dependencies'].items():
        if b.sha(b.REPO / path) != digest:
            errors.append('Builder dependency changed: ' + path)
    for name, digest in mf['assets'].items():
        if b.sha(b.OUT / 'assets' / name) != digest:
            errors.append('Figure changed: ' + name)
    expected_keys = {item[0] for item in b.CATALOG}
    if {r['key'] for r in mf['reports']} != expected_keys:
        errors.append('Missing paired edition')
    reports = []
    for row in mf['reports']:
        local_errors = []
        key, lang, full = row['key'], row['language'], row['full']
        for path, digest in row['source_files'].items():
            if b.sha(b.REPO / path) != digest:
                local_errors.append('Source changed after build: ' + path)
        for ext, rec in row['outputs'].items():
            if b.sha(b.REPO / rec['path']) != rec['sha256']:
                local_errors.append('Output changed after build: ' + ext)
        actual_md = (b.REPO / row['outputs']['md']['path']).read_text(encoding='utf-8')
        body = actual_md.split('<!-- BODY_START -->', 1)[1].strip()
        expected_body = b.source_body(lang)
        preserved = b.strip_insertions(body) if full else ''
        if full and preserved != expected_body:
            local_errors.append('Removing marked updates does not restore the exact frozen research body')
        if full and body != b.compose_body(lang):
            local_errors.append('Published body does not match current reviewed insertion inputs')
        if full and len(b.INSERT_RE.findall(body)) != 7:
            local_errors.append('Expected exactly seven bounded insertions')
        if full and b.digest(preserved) != baseline['full_bodies'][lang]['body_sha256']:
            local_errors.append('Frozen body digest differs')
        refs = {url for url, _ in b.zh.reference_entries(body)}
        prior_refs = {url for url, _ in b.zh.reference_entries(expected_body)}
        if full and not prior_refs.issubset(refs):
            local_errors.append('An original full-report source URL was lost')
        if full and len(prior_refs) != 342:
            local_errors.append('Expected 342 frozen source URLs')
        if not full:
            full_sources = {url for url, _ in b.zh.reference_entries(b.compose_body(lang))}
            full_sources.update(url for url, _ in b.zh.reference_entries((b.SRC / f'author_view_{lang}.md').read_text(encoding='utf-8')))
            if not refs.issubset(full_sources):
                local_errors.append('Brief source absent from full report: ' + str(refs - full_sources))
        if full:
            if lang == 'zh':
                chapter_numbers = {v:k for k,v in b.CHINESE_NUMBERS.items()}
                chapters = [chapter_numbers[n] for n in re.findall(r'^## 第([一二三四五六七八九十]+)章', body, re.M)]
                appendices = re.findall(r'^## 附篇([A-F])', body, re.M)
            else:
                chapters = [int(n) for n in re.findall(r'^## Chapter (\d+):', body, re.M)]
                appendices = re.findall(r'^## Appendix ([A-F])', body, re.M)
            if chapters != list(range(1, 15)) or appendices != list('ABCDEF'):
                local_errors.append('Chapter/appendix sequence differs')
            _, previous_headings = b.numbered_html(expected_body)
            retained_headings = [h for h in row['headings'] if h['anchor'].startswith('h-')]
            if retained_headings != previous_headings:
                local_errors.append('Original h-* anchor-to-heading mapping changed')
        ht = (b.REPO / row['outputs']['html']['path']).read_text(encoding='utf-8')
        published_styles = re.search(r'<style>(.*?)</style>', ht, re.S)
        if not published_styles or published_styles[1] != b.styles(lang, full):
            local_errors.append('Published styles differ from the current language/edition layout')
        changed_text = (b.SRC / (f'author_view_{lang}.md' if full else f'brief_{lang}.md')).read_text(encoding='utf-8')
        changed_html = b.render_md(changed_text)
        if changed_html.count('<table>') < 2:
            local_errors.append('Expected the timing table and the technology/cash-recovery matrix')
        all_new_text = '\n'.join(p.read_text(encoding='utf-8') for p in b.required_sources(lang, full) if p.parent == b.SRC)
        if lang == 'en' and re.search(r'[\u4e00-\u9fff]', re.sub(r'https?://[^\s)]+', '', all_new_text)):
            local_errors.append('Untranslated Chinese text in new English prose')
        parser = Parser(); parser.feed(ht)
        if len(parser.ids) != len(set(parser.ids)):
            local_errors.append('Duplicate HTML anchors')
        for target in parser.links + parser.images:
            if target.startswith('#') and unquote(target[1:]) not in parser.ids:
                local_errors.append('Missing anchor: ' + target)
            elif target and not target.startswith(('#', 'http://', 'https://', 'mailto:')):
                if not (b.OUT / unquote(target.split('#')[0])).resolve().is_file():
                    local_errors.append('Missing local target: ' + target)
        if full:
            prior_html = Parser()
            prior_html.feed(b.render_md(expected_body))
            if Counter(parser.images) != Counter(prior_html.images):
                local_errors.append('Full figure placements changed')
        headings = {h['anchor']: h for h in row['headings']}
        expected_toc = {h['anchor'] for h in row['headings'] if h['level'] <= 3} if full else set()
        seen_toc = set()
        bounds = []
        with fitz.open(b.REPO / row['outputs']['pdf']['path']) as doc:
            texts = [p.get_text() for p in doc]
            bookmarks = doc.get_toc()
            if len(doc) != row['pages']:
                local_errors.append('Page count mismatch')
            if not full and len(doc) > 18:
                local_errors.append('Brief exceeds 18 pages')
            for h in row['headings']:
                matches = [r for r in bookmarks if norm(r[1]) == norm(h['text'])]
                if not any(0 < r[2] <= len(doc) and norm(h['text']) in norm(texts[r[2]-1]) for r in matches):
                    local_errors.append('Missing or wrong bookmark: ' + h['text'])
            early = norm(texts[1] if full else texts[0])
            if '2027' not in early or '2028' not in early:
                local_errors.append('Forecast is not on the first reading page')
            forecast_end = r'2028年6月30日' if lang == 'zh' else r'(?:30June2028|June30,?2028)'
            if not re.search(forecast_end, norm('\n'.join(texts[:5]))):
                local_errors.append('Forecast settlement deadline missing from opening')
            for i, page in enumerate(doc):
                if '\ufffd' in texts[i]:
                    local_errors.append(f'Replacement character on page {i+1}')
                if b.EMAIL not in texts[i]:
                    local_errors.append(f'Contact missing on page {i+1}')
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines', []):
                        for span in line['spans']:
                            x0, y0, x1, y1 = span['bbox']
                            if x0 < -.8 or y0 < -.8 or x1 > page.rect.width + .8 or y1 > page.rect.height + .8:
                                bounds.append({'page': i+1, 'text': span['text']})
                for link in page.get_links():
                    if link['kind'] not in (fitz.LINK_GOTO, fitz.LINK_NAMED):
                        continue
                    dest, anchor = link.get('page', -1), link.get('nameddest')
                    if not 0 <= dest < len(doc):
                        local_errors.append('Invalid PDF internal destination'); continue
                    if anchor in headings and norm(headings[anchor]['text']) not in norm(texts[dest]):
                        local_errors.append('PDF anchor misses its heading: ' + anchor)
                    if anchor in expected_toc:
                        label = norm(page.get_textbox(link['from']))
                        number = re.search(r'(\d+)$', label)
                        if number:
                            seen_toc.add(anchor)
                            if int(number[1]) != dest + 1:
                                local_errors.append('Wrong printed contents page: ' + label)
            if bounds:
                local_errors.append('Text outside page: ' + str(bounds[:6]))
            if seen_toc != expected_toc:
                local_errors.append('Unverified contents destinations: ' + str(sorted(expected_toc - seen_toc)))
            if full:
                overview = '研究总览' if lang == 'zh' else 'Research Overview'
                first_body = next(r[2] for r in bookmarks if r[1].startswith(overview))
                samples = set(range(first_body))
                for r in bookmarks:
                    if re.match(r'^(?:第[三四五]|第十三)章|^Chapter (?:3|4|5|13):|^Reference index|^参考资料', r[1]):
                        samples.add(r[2] - 1)
                # Review every newly added passage, including continuation pages and boundaries.
                for index, heading in enumerate(row['headings']):
                    if not heading['anchor'].startswith('update-'):
                        continue
                    matching = [r[2] - 1 for r in bookmarks if norm(r[1]) == norm(heading['text'])]
                    if not matching:
                        continue
                    first = min(matching)
                    following = row['headings'][index+1:]
                    end = len(doc) - 1
                    if following:
                        next_pages = [r[2] - 1 for r in bookmarks if norm(r[1]) == norm(following[0]['text'])]
                        if next_pages:
                            end = min(next_pages)
                    samples.update(range(max(0, first-1), min(len(doc), end+2)))
                samples.add(len(doc) - 1)
            else:
                samples = set(range(len(doc)))
            dest = b.OUT / 'qa_visual' / key
            dest.mkdir(parents=True, exist_ok=True)
            visual = []
            for i in sorted(samples):
                path = dest / f'page_{i+1:03d}.png'
                doc[i].get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False).save(path)
                visual.append({'page': i+1, 'image': str(path)})
        reports.append({'key': key, 'pages': row['pages'], 'pdf_sha256': row['outputs']['pdf']['sha256'], 'original_body_preserved': full and preserved == expected_body, 'references': len(refs), 'original_references_preserved': len(prior_refs) if full else None, 'bookmarks_checked': len(row['headings']), 'contents_destinations_checked': len(seen_toc), 'visual_samples': visual, 'errors': local_errors})
        errors.extend(key + ': ' + e for e in local_errors)
    result = {'status': 'PASS_STRUCTURE' if not errors else 'FAIL', 'scope': 'Artifact hashes; exact restoration of V1.9 bodies after removing seven marked additions; original anchors, figures and references; chapters 1-14 and Appendices A-F; all-page text bounds; PDF navigation; rendered samples covering all added passages and complete briefs. Independent semantic and actual visual review required.', 'prior_artifacts_unchanged': len(unchanged), 'prior_unique_files_unchanged': len(set(unchanged)), 'historical_files_unchanged': len(history['files']), 'allowed_navigation_edits': sorted(set(entrypoints)), 'validator_sha256': b.sha(__file__), 'reports': reports, 'errors': errors}
    b.write_json(b.OUT / 'qa.json', result)
    print(json.dumps({'status': result['status'], 'prior_artifacts_unchanged': len(unchanged), 'reports': [{k: r[k] for k in ('key', 'pages', 'references', 'contents_destinations_checked')} for r in reports], 'errors': errors}, ensure_ascii=False), flush=True)
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
