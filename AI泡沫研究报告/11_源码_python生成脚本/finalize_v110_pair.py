#!/usr/bin/env python3
"""Accept reviewed V1.10 reports and prepare repository publication entrypoints."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
import build_v110_pair as b


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    mf, qa = load(b.OUT/'manifest.json'), load(b.OUT/'qa.json')
    assert qa['status'] == 'PASS_STRUCTURE', qa['errors']
    rows = {r['key']: r for r in mf['reports']}
    qa_rows = {r['key']: r for r in qa['reports']}
    assert set(rows) == {'full_zh', 'brief_zh', 'full_en', 'brief_en'}
    review_names = []
    visual_pages = 0
    for lang in ('zh', 'en'):
        name = f'semantic_review_{lang}.json'
        review = load(b.REVIEW/name)
        assert review['status'] == 'PASS', name
        expected = {f'author_view_{lang}.md', f'brief_{lang}.md', f'event_chapter_{lang}.md', f'body_updates_{lang}.json'}
        assert set(review['file_sha256']) == expected, name
        for filename, digest in review['file_sha256'].items():
            assert b.sha(b.SRC/filename).lower() == digest.lower(), filename
        review_names.append(name)
        name = f'visual_{lang}.json'
        visual = load(b.REVIEW/name)
        assert visual['status'] == 'PASS', name
        assert {r['key'] for r in visual['reports']} == {f'full_{lang}', f'brief_{lang}'}
        for item in visual['reports']:
            assert item['pdf_sha256'].lower() == rows[item['key']]['outputs']['pdf']['sha256'].lower()
            assert item['pages_reviewed'], item
            expected_pages = {sample['page'] for sample in qa_rows[item['key']]['visual_samples']}
            assert expected_pages.issubset(set(item['pages_reviewed'])), item['key']
            assert all(1 <= page <= rows[item['key']]['pages'] for page in item['pages_reviewed'])
            visual_pages += len(set(item['pages_reviewed']))
        review_names.append(name)
    calc = load(b.REVIEW/'calculations_review.json')
    assert calc['status'] == 'PASS'
    assert calc['calculation_sha256'].lower() == b.sha(b.REVIEW/'calculations.json').lower()
    review_names.append('calculations_review.json')
    for row in mf['reports']:
        for output in row['outputs'].values():
            assert b.sha(b.REPO/output['path']) == output['sha256']
    for old in load(b.REVIEW/'baseline.json')['files']:
        if not old['mutable_entrypoint']:
            assert b.sha(b.REPO/old['path']) == old['sha256'], old['path']
    history = load(b.ROOT/'复审与版本记录/V1.9_拉取基线历史文件哈希_20261031.json')
    for name, row in history['files'].items():
        assert b.sha(b.REPO/name) == row['working_tree_sha256'], name
    folder = b.OUT.relative_to(b.ROOT).as_posix()
    rootfolder = b.OUT.relative_to(b.REPO).as_posix()
    labels = {'full_zh':'中文详细版', 'brief_zh':'中文简版', 'full_en':'English full report', 'brief_en':'English brief'}

    def link(key, prefix=''):
        row = rows[key]
        return f'[{labels[key]}：{row["pages"]}页]({prefix}{row["stem"]}.pdf)'

    note = '编辑日期2026-11-17；基础研究截至2026-10-31，黄仁勋离任及相关融资、治理、监管专题增量截至2026-11-17（北京时间）。各事实保留自身财期与观察日。'
    thesis = '作者保留2027年上半年至2028年上半年的主观基准风险窗口，提高对原提前信用冲击路径的关注。辞职本身不等于融资停止、技术失效或泡沫破裂；判断须由新增支持、合同履行、回款与跨主体传导验证。2028年6月底未兑现仍须结算，不自动顺延计命中。'
    scope = '保留原13章、附篇A至F、图表和342个原有去重参考URL；新增第14章深度研究，并在第1、2、8、10、12、13章加入明确日期的更新。开篇核心观点与两张原矩阵保留并同步事件判断。中英文详细版与简版均更新，包含可复算的纯假设现金压力算例及相反路径。'
    reviewfolder = '复审与版本记录/V1.10_20261117'
    links = ' · '.join(link(k) for k in labels)
    (b.OUT/'README.md').write_text(f'# AI周期与泡沫研究 · V1.10\n\n大队长\n\n{note}\n\n{links}\n\n{thesis}\n\n{scope}\n\n每版均含PDF、HTML和Markdown。同一语言的详细版与简版可配套发送。\n\n[验收记录](../{reviewfolder}/acceptance.md) · [结构检查](qa.json) · [文件清单](manifest.json) · [上一版V1.9.2](../V1.9.2_配套发布_20261101/index.html)\n\n本版不包含北京时间11月18日才计划公布的NVIDIA FY27Q3业绩；监管规则按11月17日已知状态登记。Substack附件仍由作者另行替换。\n', encoding='utf-8')
    htmlrows = ''.join(f'<tr><td>{html.escape(labels[r["key"]])}</td><td>{r["pages"]}</td><td><a href="{r["stem"]}.pdf">PDF</a> · <a href="{r["stem"]}.html">HTML</a> · <a href="{r["stem"]}.md">Markdown</a></td></tr>' for r in mf['reports'])
    (b.OUT/'index.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI周期与泡沫研究 · V1.10</title><style>body{{font:17px/1.85 system-ui;max-width:980px;margin:40px auto;padding:24px;color:#28475e;background:#f8fbfd}}h1{{color:#315e7c}}a{{color:#356e93}}table{{width:100%;border-collapse:collapse}}td,th{{padding:13px;border-bottom:1px solid #cadce8;text-align:left}}.lead{{padding:20px;background:#eaf3f9;border-left:5px solid #91bdd5}}</style></head><body><h1>AI周期与泡沫研究 · V1.10</h1><p>大队长 · {note}</p><div class="lead">{thesis}</div><h2>中英文详细版与简版</h2><table><thead><tr><th>版本</th><th>页数</th><th>格式</th></tr></thead><tbody>{htmlrows}</tbody></table><p>{scope}</p><p><a href="README.md">使用说明</a> · <a href="../{reviewfolder}/acceptance.md">复审与验收</a> · <a href="../V1.9.2_配套发布_20261101/index.html">V1.9.2存档</a></p></body></html>', encoding='utf-8')
    current = f'''## 当前报告

{link('full_zh',rootfolder+'/')} · {link('brief_zh',rootfolder+'/')}

{link('full_en',rootfolder+'/')} · {link('brief_en',rootfolder+'/')} · [全部格式与说明]({rootfolder}/index.html)

{thesis}

{scope}

{note}

[复审与验收](AI泡沫研究报告/{reviewfolder}/acceptance.md) · [交付清单](V1.10-publication-files.json) · [上一版V1.9.2](AI泡沫研究报告/V1.9.2_配套发布_20261101/index.html) · [V1.9原20册](AI泡沫研究报告/V1.9现行正文版/index.html)

'''
    p = b.REPO/'README.md'; text = p.read_text(encoding='utf-8')
    text, n = re.subn(r'\*\*最新版本\*\*：[^\n]+','**最新版本**：V1.10 黄仁勋离任与AI融资深度更新（2026-11-17）',text,count=1); assert n == 1
    text, n = re.subn(r'\*\*资料截止\*\*：[^\n]+','**资料截止**：基础研究2026-10-31；本次专题增量2026-11-17（北京时间），各事实保留自身期间。',text,count=1); assert n == 1
    text, n = re.subn(r'## 当前报告\n.*?(?=## 历史仓库目录)',current,text,count=1,flags=re.S); assert n == 1
    text = re.sub(r'默认阅读入口为上方V[\d.]+；','默认阅读入口为上方V1.10；',text)
    p.write_text(text, encoding='utf-8')
    (b.ROOT/'README.md').write_text(f'# AI周期与泡沫研究报告\n\n大队长 · 当前版本 **V1.10（2026-11-17）**\n\n{note}\n\n{link("full_zh",folder+"/")} · {link("brief_zh",folder+"/")}\n\n{link("full_en",folder+"/")} · {link("brief_en",folder+"/")} · [全部格式]({folder}/index.html)\n\n{thesis}\n\n{scope}\n\n[复审与验收]({reviewfolder}/acceptance.md) · [构建说明](11_源码_python生成脚本/README_v110_pair.md) · [上一版V1.9.2](V1.9.2_配套发布_20261101/index.html) · [V1.9原20册](V1.9现行正文版/index.html) · [原英文完整报告](V1.9_English_Full_Report/index.html) · [V1.8存档](V1.8现行正文版/index.html)\n\n联系邮箱：[fqsx@mail.ustc.edu.cn](mailto:fqsx@mail.ustc.edu.cn)。旧版本保留原预测、资料时点和复审记录；不以新证据改写旧版历史。\n', encoding='utf-8')
    heading = '## V1.10（2026-11-17）· 黄仁勋离任与AI融资深度更新'
    entry = f'''{heading}

- 新增第14章，研究个人协调作用与技术组织、融资合同与资本承诺、客户现金回收、GPU资产及跨境监管传导。
- 同步开篇观点、情景矩阵及第1、2、8、10、12、13章，并更新中英文简版。
- 分开自用研发承诺和客户支持、已交割资金和或有义务；加入纯假设现金压力算例与反证。
- 保留原预测登记日和2028年6月底结算条件；不以辞职或单一股价变化认定预测命中。
- 中英文详细版分别{rows['full_zh']['pages']}、{rows['full_en']['pages']}页；简版分别{rows['brief_zh']['pages']}、{rows['brief_en']['pages']}页。完成跨代理语义、计算与实际视觉验收。
- 基础研究仍截至10月31日，本专题增量截至11月17日；保留旧版和原有正文。

详见[配套阅读入口]({rootfolder}/index.html)、[验收记录](AI泡沫研究报告/{reviewfolder}/acceptance.md)及[交付清单](V1.10-publication-files.json)。

'''
    p = b.REPO/'CHANGELOG.md'; change = p.read_text(encoding='utf-8')
    if heading in change:
        change = re.sub(re.escape(heading)+r'\n.*?(?=\n## |\Z)',entry.rstrip(),change,count=1,flags=re.S)
    else:
        assert '# 版本变更记录\n\n' in change
        change = change.replace('# 版本变更记录\n\n','# 版本变更记录\n\n'+entry,1)
    p.write_text(change, encoding='utf-8')
    (b.REVIEW/'acceptance.md').write_text(f'# V1.10 交付验收\n\n状态：PASS_REVIEWED_ARTIFACTS。{note}\n\n{thesis}\n\n{scope}\n\n中文、英文分别由非该语言主笔代理进行语义复核，绑定最终四份源文件；计算另有独立复核。PDF结构检查覆盖页码、目录、锚点、原正文可逆保留、源与输出哈希、引用与图片。实际视觉查看共{visual_pages}页样本，范围与最终PDF哈希见visual_zh.json、visual_en.json；不冒充逐页重审全部旧正文事实。\n\n{qa["prior_artifacts_unchanged"]}项前次交付文件、{len(history["files"])}项历史文件通过本轮冻结检查。旧预测不因新事件改写；旧报告仍保留旧时点。\n\n本记录验收文档，不代表已上传Substack。远程Git提交及推送以仓库实际记录为准。\n', encoding='utf-8')
    mf['status'] = 'PASS_REVIEWED_ARTIFACTS'
    mf.pop('remote_push_performed', None)
    mf['remote_publication_record'] = 'Repository Git commit and remote refs are authoritative; this manifest attests artifact content.'
    mf['qa_sha256'] = b.sha(b.OUT/'qa.json')
    mf['reviews'] = {name:b.sha(b.REVIEW/name) for name in review_names}
    b.write_json(b.OUT/'manifest.json',mf)
    archive_dirs = (b.ROOT/'专题更新_20261117', b.ROOT/'复审与版本记录/20261117_黄仁勋辞职专题')
    paths = [p for directory in (b.OUT,b.SRC,b.REVIEW,*archive_dirs) for p in directory.rglob('*') if p.is_file() and p.suffix.lower() not in {'.png','.jpg','.jpeg','.webp','.pyc'} and '__pycache__' not in p.parts and 'qa_visual' not in p.parts]
    paths += [b.REPO/'README.md',b.ROOT/'README.md',b.REPO/'CHANGELOG.md',Path(__file__),Path(b.__file__),Path(__file__).with_name('qa_v110_pair.py'),Path(__file__).with_name('README_v110_pair.md')]
    records = [{'path':p.relative_to(b.REPO).as_posix(),'bytes':p.stat().st_size,'sha256':b.sha(p)} for p in sorted(set(paths))]
    b.write_json(b.REPO/'V1.10-publication-files.json',{'version':b.VERSION,'status':'PASS_REVIEWED_ARTIFACTS','editorial_date':b.EDIT_DATE,'original_research_cutoff':'2026-10-31','topic_update_cutoff':'2026-11-17','scope':'Integrated event update in Chinese and English full and brief editions; original research retained with explicit dates','pdf_count':4,'pages':{k:r['pages'] for k,r in rows.items()},'prior_publication_files_unchanged':qa['prior_artifacts_unchanged'],'historical_files_unchanged':len(history['files']),'visual_pages_reviewed':visual_pages,'remote_publication_record':'Repository Git commit and remote refs are authoritative; this manifest attests artifact content.','substack_attachment_updated':False,'files':records})
    print(json.dumps({'status':'PASS_REVIEWED_ARTIFACTS','pages':{k:r['pages'] for k,r in rows.items()},'files':len(records),'visual_pages':visual_pages},ensure_ascii=False))


if __name__ == '__main__':
    main()
