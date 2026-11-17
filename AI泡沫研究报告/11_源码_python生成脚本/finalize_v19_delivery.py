#!/usr/bin/env python3
"""Update current entrypoints only after V1.9 structural, review and visual QA."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote
import markdown
from build_v19_current import ROOT, SRC, OUT, CATALOG, sha
from qa_v19_current import Parser, dependency_errors


def write(path, text):
    path.write_text(text.rstrip()+'\n', encoding='utf-8')


def main():
    repo = ROOT.parent
    manifest = json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    qa = json.loads((OUT/'qa.json').read_text(encoding='utf-8'))
    assert qa['status'] == 'PASS_LOCAL_STRUCTURE'
    assert not dependency_errors(manifest)
    assert qa.get('validator_sha256') == sha(ROOT/'11_源码_python生成脚本/qa_v19_current.py')
    assert next(r for r in qa['reports'] if r['slug']=='13_超全景版')['chapter_sequence'] == list(range(1,14))
    assert len(manifest['reports']) == len(CATALOG) == 20
    review = ROOT/'复审与版本记录/V1.9_复审与验收_20261031.md'
    assert '未解决阻断项：0' in review.read_text(encoding='utf-8')
    numbering_review = ROOT/'复审与版本记录/V1.9_章节编号独立评审_20261031.md'
    assert '未解决阻断项：0' in numbering_review.read_text(encoding='utf-8')
    numbering_result = json.loads((ROOT/'复审与版本记录/V1.9_章节编号独立评审结果_20261031.json').read_text(encoding='utf-8'))
    assert numbering_result['status']=='PASS' and numbering_result['artifacts_checked']
    assert numbering_result['builder_sha256']==manifest['builder_sha256']
    assert numbering_result['numbering_sha256']==sha(ROOT/'11_源码_python生成脚本/numbering_v19.py')
    visual_path = ROOT/'复审与版本记录/V1.9_视觉抽检_20261031.json'
    visual = json.loads(visual_path.read_text(encoding='utf-8'))
    assert visual['status'] == 'PASS_SAMPLED_VISUAL'
    for name, digest in visual['pdf_sha256'].items():
        assert sha(OUT/name) == digest, f'Visual review stale: {name}'
    reports = manifest['reports']
    by_slug = {r['slug']: r for r in reports}
    main_pages = by_slug['01_主报告']['pages']
    full_pages = by_slug['13_超全景版']['pages']
    video_pages = by_slug['18_AI视频短剧中美市场']['pages']
    coding_pages = by_slug['19_AI编程市场预测复盘']['pages']
    apps_pages = by_slug['20_AI应用商业化全景']['pages']
    total_pages = sum(r['pages'] for r in reports)
    refs = by_slug['13_超全景版']['reference_count']
    arithmetic = len(qa['arithmetic'])

    readme = (repo/'README.md').read_text(encoding='utf-8')
    readme = re.sub(r'\*\*最新版本\*\*：[^\n]*', '**最新版本**：V1.9 深化研究版（视频模型、短剧时长、编程人力与成本）', readme)
    readme = re.sub(r'\*\*资料截止\*\*：[^\n]*', '**资料截止**：2026-10-31（北京时间）；利率观察截至美国10月30日，各事实保留自身期间。', readme)
    current = f'''## 当前报告

[大完整报告（超全景）：{full_pages}页](AI泡沫研究报告/V1.9现行正文版/13_超全景版.pdf) · [主报告：{main_pages}页](AI泡沫研究报告/V1.9现行正文版/01_主报告.pdf) · [AI视频短剧中美专题：{video_pages}页](AI泡沫研究报告/V1.9现行正文版/18_AI视频短剧中美市场.pdf) · [全部20个版本](AI泡沫研究报告/V1.9现行正文版/index.html)

[AI编程：预测、人力与成本，{coding_pages}页](AI泡沫研究报告/V1.9现行正文版/19_AI编程市场预测复盘.pdf) · [其他AI应用商业化：{apps_pages}页](AI泡沫研究报告/V1.9现行正文版/20_AI应用商业化全景.pdf)

V1.9在V1.8基础上深化两个专题：短剧怎样转化为Seedance、MiniMax/海螺、可灵等视频模型的需求与利润；AI编程怎样从任务提效改变团队用工、招聘与实际现金成本。另追溯“短剧时长超过电影”的多种口径，区分累计片长、手机观看时长、市场收入和电影票房。既有财务、宏观与其他应用基线保留原核验范围。

当前证据显示需求与现金回收继续分化，应用端有新增收费证据，尚不足以确认全行业需求和融资同时崩塌，也不足以证明全部资本投入已获回报。关键结论经过非主笔交叉评审；单源、转存件、未核事项和条件算例继续明示，不发布未经校准的崩盘概率。

[更新说明](AI泡沫研究报告/复审与版本记录/V1.9_本次更新说明_20261031.md) · [复审与验收](AI泡沫研究报告/复审与版本记录/V1.9_复审与验收_20261031.md) · [主题覆盖](AI泡沫研究报告/复审与版本记录/V1.9_原339页主题覆盖表_20261031.md) · [文件清单](V1.9-publication-files.json) · [V1.8历史版](AI泡沫研究报告/V1.8现行正文版/index.html)

'''
    readme = re.sub(r'## 当前报告\n.*?(?=## 历史仓库目录)', lambda _: current, readme, flags=re.S)
    readme = readme.replace('默认阅读入口为上方V1.8', '默认阅读入口为上方V1.9')
    write(repo/'README.md', readme)

    entry = f'''## V1.9（2026-10-31）· 视频模型与编程人力、成本深化研究

- 深化Seedance、MiniMax/海螺与可灵等视频模型的产品、收费渠道、财务边界及短剧工作流。
- 追溯短剧时长说法，区别整剧片长、手机App使用时长与市场收入；播放不按观众数重复计为视频生成。
- 从成片、重试、投流与本地化推导模型付费用量，并区分价格、效率、需求弹性与利润归属。
- 更新编程任务与组织研究，拆解工时、产能、招聘、工资现金、返工与过渡成本，给出中美条件模型。
- 保留旧编程预测复盘及V1.8财务、宏观、其他应用证据，不把本次深化冒充所有旧事实重审。
- 研究主笔交叉评审并闭环关键修正；未核数据不补造，不新增崩盘概率或无完整模型的目标价。
- 修正合卷章号跳转：大完整报告正文连续编为第1—13章，短剧、编程、其他应用为第4—6章；同步目录、书签、节号和文内引用，专题选编沿用全景章号。
- 20册同源生成，共{total_pages}页；主报告{main_pages}页、超全景{full_pages}页、短剧专题{video_pages}页。通过结构和{arithmetic}项算式复算，另有明确范围的视觉抽检；不宣称全页人工审阅或所有旧来源重新验证。

详见[更新说明](AI泡沫研究报告/复审与版本记录/V1.9_本次更新说明_20261031.md)、[验收记录](AI泡沫研究报告/复审与版本记录/V1.9_复审与验收_20261031.md)和[交付清单](V1.9-publication-files.json)。V1.8及更早版本独立保留。本次本地文件更新不构成远程推送回执。

'''
    changelog = (repo/'CHANGELOG.md').read_text(encoding='utf-8')
    changelog = re.sub(r'\n## V1\.9.*?(?=\n## V1\.)', '', changelog, flags=re.S)
    changelog = changelog.replace('# 版本变更记录\n', '# 版本变更记录\n\n'+entry, 1)
    write(repo/'CHANGELOG.md', changelog)

    write(ROOT/'README.md', f'''# AI周期与泡沫研究报告

作者：大队长。当前为 **V1.9，2026年10月31日**。各数据保留自身财期、发布日期和观察日；个人研究，不构成投资建议。

联系邮箱：[fqsx@mail.ustc.edu.cn](mailto:fqsx@mail.ustc.edu.cn)。

[大完整报告（超全景）：{full_pages}页](V1.9现行正文版/13_超全景版.pdf) · [主报告：{main_pages}页](V1.9现行正文版/01_主报告.pdf) · [AI视频短剧中美专题：{video_pages}页](V1.9现行正文版/18_AI视频短剧中美市场.pdf) · [20册导航](V1.9现行正文版/index.html)

本版在V1.8基础上深化短剧对视频模型的影响、时长比较，以及编程对人力和成本的改变。模型收费、内容观看、净工时、可用产能和现金节省分别建账；以具名原件、条件算例与反方评审说明哪些机制可以成立、哪些仍待验证。

[编程复盘：{coding_pages}页](V1.9现行正文版/19_AI编程市场预测复盘.pdf) · [其他应用：{apps_pages}页](V1.9现行正文版/20_AI应用商业化全景.pdf)

[本次更新](复审与版本记录/V1.9_本次更新说明_20261031.md) · [主题覆盖](复审与版本记录/V1.9_原339页主题覆盖表_20261031.md) · [交叉复审与验收](复审与版本记录/V1.9_复审与验收_20261031.md) · [文件总索引](00_使用说明/V1.9_当前文件总索引_2026-10-31.md)

20册累计{total_pages}页，超全景按URL去重收录{refs}项参考资料。结构检查、{arithmetic}项算式复算与抽样视觉检查范围见验收记录；这不代表全历史事实重审或全部PDF逐页人工验收。单源、公司样本、转存件与未核缺口均保留。

旧[V1.8现行正文版](V1.8现行正文版/index.html)、[V1.7现行正文版](V1.7现行正文版/index.html)、[V1.6.1校注版](V1.6.1完整校注版/index.html)和[原339页冻结底本](09_历史冻结基线/超全景339页_20261009更新前.pdf)独立保留。新源码在`10_源码_markdown/V1.9_现行正文_20261031/`；[重建说明](11_源码_python生成脚本/README_v19_runtime.md)与构建、QA、复算脚本一同保存。本地完成状态与外部发布分别确认。
''')
    rows = '\n'.join(f'| {r["title"]} | {r["pages"]} | [PDF](../V1.9现行正文版/{r["slug"]}.pdf) · [网页](../V1.9现行正文版/{r["slug"]}.html) · [Markdown](../V1.9现行正文版/{r["slug"]}.md) |' for r in reports)
    write(ROOT/'00_使用说明/V1.9_当前文件总索引_2026-10-31.md', f'''# V1.9 当前文件总索引

大队长 · 2026年10月31日。20册来自同一组正文，实测合计{total_pages}页。第18—20册分别为AI视频短剧与模型、编程预测与人力成本、其他应用商业化专题。

| 版本 | 实测页数 | 文件 |
|---|---:|---|
{rows}

[更新说明](../复审与版本记录/V1.9_本次更新说明_20261031.md) · [复审与验收](../复审与版本记录/V1.9_复审与验收_20261031.md) · [旧V1.8](../V1.8现行正文版/index.html)
''')

    files = {repo/'README.md', repo/'CHANGELOG.md', ROOT/'README.md'}
    files.update(p for p in OUT.rglob('*') if p.is_file() and 'qa_visual' not in p.parts)
    files.update(p for p in SRC.rglob('*') if p.is_file())
    files.update((ROOT/'复审与版本记录').glob('V1.9*'))
    files.update((ROOT/'00_使用说明').glob('V1.9*'))
    files.update((ROOT/'11_源码_python生成脚本').glob('*v19*'))
    files = {p for p in files if p.is_file() and '__pycache__' not in p.parts}
    errors = []
    for p in files:
        if p.suffix not in ('.md', '.html'): continue
        text = p.read_text(encoding='utf-8')
        parser = Parser(); parser.feed(text if p.suffix == '.html' else markdown.markdown(text, extensions=['tables']))
        for ref in parser.links+parser.images:
            if not ref or ref.startswith(('https://','http://','mailto:','#')): continue
            target = (p.parent/unquote(ref.split('#')[0])).resolve()
            if target == repo/'V1.9-publication-files.json': continue
            if not target.is_file(): errors.append(f'{p.relative_to(repo)} -> {ref}')
    if errors: raise RuntimeError('Broken local links: '+str(errors))
    for r in reports:
        for ext in ('pdf','md','html'):
            assert sha(ROOT/r[ext]['path']) == r[ext]['sha256']
    changed = subprocess.check_output(['git','-c','core.quotepath=false','diff','--name-only'], cwd=repo).decode('utf-8').splitlines()
    allowed = {'README.md','CHANGELOG.md','AI泡沫研究报告/README.md'}
    assert not (set(changed)-allowed), f'Historical tracked files changed: {changed}'
    payload = {'version':'V1.9','cutoff':'2026-10-31 Asia/Shanghai','status':'PASS_LOCAL_DELIVERY',
               'pdf_count':20,'pdf_pages':total_pages,'full_edition_references':refs,
               'arithmetic_checks':arithmetic,'visual_scope':visual['scope'],
               'scope':'local research update; targeted multi-agent review, structural and sampled visual QA; no remote publication',
               'git_branch':subprocess.check_output(['git','branch','--show-current'],cwd=repo).decode().strip(),
               'historical_tracked_files_changed':[], 'remote_push_performed':False,
               'files':[{'path':p.relative_to(repo).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)]}
    write(repo/'V1.9-publication-files.json', json.dumps(payload,ensure_ascii=False,indent=2))
    print(json.dumps({k:payload[k] for k in ('status','pdf_count','pdf_pages','full_edition_references','arithmetic_checks','git_branch')}, ensure_ascii=False,indent=2))


if __name__ == '__main__': main()
