#!/usr/bin/env python3
"""Update current entrypoints only after V1.8 structural, review and visual QA."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from urllib.parse import unquote
import markdown
from build_v18_current import ROOT, SRC, OUT, CATALOG, sha
from qa_v18_current import Parser


def write(path, text):
    path.write_text(text.rstrip()+'\n', encoding='utf-8')


def main():
    repo = ROOT.parent
    manifest = json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
    qa = json.loads((OUT/'qa.json').read_text(encoding='utf-8'))
    assert qa['status'] == 'PASS_LOCAL_STRUCTURE'
    assert len(manifest['reports']) == len(CATALOG) == 20
    review = ROOT/'复审与版本记录/V1.8_复审与验收_20261031.md'
    assert '未解决阻断项：0' in review.read_text(encoding='utf-8')
    visual_path = ROOT/'复审与版本记录/V1.8_视觉抽检_20261031.json'
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
    readme = re.sub(r'\*\*最新版本\*\*：[^\n]*', '**最新版本**：V1.8 现行正文版（短剧、编程预测复盘与其他应用全面更新）', readme)
    readme = re.sub(r'\*\*资料截止\*\*：[^\n]*', '**资料截止**：2026-10-31（北京时间）；利率观察截至美国10月30日，各事实保留自身期间。', readme)
    current = f'''## 当前报告

[AI视频短剧中美专题：{video_pages}页](AI泡沫研究报告/V1.8现行正文版/18_AI视频短剧中美市场.pdf) · [主报告：{main_pages}页](AI泡沫研究报告/V1.8现行正文版/01_主报告.pdf) · [超全景：{full_pages}页](AI泡沫研究报告/V1.8现行正文版/13_超全景版.pdf) · [全部20个版本](AI泡沫研究报告/V1.8现行正文版/index.html)

[AI编程旧预测复盘：{coding_pages}页](AI泡沫研究报告/V1.8现行正文版/19_AI编程市场预测复盘.pdf) · [其他AI应用商业化：{apps_pages}页](AI泡沫研究报告/V1.8现行正文版/20_AI应用商业化全景.pdf)

V1.8接入云厂及中韩美供应链新财报，更新融资、宏观、模型、能源与国际约束，新增AI视频短剧、AI编程旧预测复盘和其他应用三个专题。编程旧席位算术有条件成立，固定低价上限应撤回，实际全市场规模仍缺去重证据；其他应用逐项检验付款、利润和现金，保留重组等反例。

当前证据显示需求与现金回收继续分化，应用端有新增收费证据，尚不足以确认全行业需求和融资同时崩塌，也不足以证明全部资本投入已获回报。关键结论经过非主笔交叉评审；单源、转存件、未核事项和条件算例继续明示，不发布未经校准的崩盘概率。

[更新说明](AI泡沫研究报告/复审与版本记录/V1.8_本次更新说明_20261031.md) · [复审与验收](AI泡沫研究报告/复审与版本记录/V1.8_复审与验收_20261031.md) · [主题覆盖](AI泡沫研究报告/复审与版本记录/V1.8_原339页主题覆盖表_20261031.md) · [文件清单](V1.8-publication-files.json) · [V1.7历史版](AI泡沫研究报告/V1.7现行正文版/index.html)

'''
    readme = re.sub(r'## 当前报告\n.*?(?=## 历史仓库目录)', lambda _: current, readme, flags=re.S)
    readme = readme.replace('默认阅读入口为上方V1.7', '默认阅读入口为上方V1.8')
    write(repo/'README.md', readme)

    entry = f'''## V1.8（2026-10-31）· 短剧、编程预测复盘及AI商业化全面更新

- 更新三家云厂、中国供应链及维谛的财务与现金桥；新分部、租赁、重估和季度/TTM口径分列。
- 更新融资执行与已公布FOMC/PCE/GDP/ECI、10月30日国债观察，撤下已发生事件的未来日历。
- 新增AI视频短剧中美专题，区分整体短剧与AI子集、预测与实绩、运营商样本与行业结论，核查完整成本、获客和版权。
- 新增AI编程旧预测复盘，从Git历史核对原命题、单位和期限，保留V1.5已纠偏的事实；条件模型不升级为新市场预测。
- 新增其他应用商业化专题，覆盖办公、CRM、知识服务、陪伴、教育、医疗和实体应用，区分整体产品收入与AI增量；更新技术、开放许可和部署范围。
- 研究主笔交叉评审并闭环关键修正；未核数据不补造，不新增崩盘概率或无完整模型的目标价。
- 20册同源生成，共{total_pages}页；主报告{main_pages}页、超全景{full_pages}页、短剧专题{video_pages}页。通过结构和{arithmetic}项算式复算，另有明确范围的视觉抽检；不宣称全页人工审阅或所有旧来源重新验证。

详见[更新说明](AI泡沫研究报告/复审与版本记录/V1.8_本次更新说明_20261031.md)、[验收记录](AI泡沫研究报告/复审与版本记录/V1.8_复审与验收_20261031.md)和[交付清单](V1.8-publication-files.json)。V1.7及更早版本独立保留。本次本地文件更新不构成远程推送回执。

'''
    changelog = (repo/'CHANGELOG.md').read_text(encoding='utf-8')
    changelog = re.sub(r'\n## V1\.8.*?(?=\n## V1\.)', '', changelog, flags=re.S)
    changelog = changelog.replace('# 版本变更记录\n', '# 版本变更记录\n\n'+entry, 1)
    write(repo/'CHANGELOG.md', changelog)

    write(ROOT/'README.md', f'''# AI周期与泡沫研究报告

作者：大队长。当前为 **V1.8，2026年10月31日**。各数据保留自身财期、发布日期和观察日；个人研究，不构成投资建议。

联系邮箱：[fqsx@mail.ustc.edu.cn](mailto:fqsx@mail.ustc.edu.cn)。

[AI视频短剧中美专题：{video_pages}页](V1.8现行正文版/18_AI视频短剧中美市场.pdf) · [主报告：{main_pages}页](V1.8现行正文版/01_主报告.pdf) · [超全景：{full_pages}页](V1.8现行正文版/13_超全景版.pdf) · [20册导航](V1.8现行正文版/index.html)

本版更新财报、宏观、技术与国际约束，新增AI视频短剧、编程旧预测复盘和其他应用三个专题。核心判断是需求与现金回收继续分化；旧编程固定席位上限应撤回，应用收费证据增加，但市场扩大不自动形成股东回报。

[编程复盘：{coding_pages}页](V1.8现行正文版/19_AI编程市场预测复盘.pdf) · [其他应用：{apps_pages}页](V1.8现行正文版/20_AI应用商业化全景.pdf)

[本次更新](复审与版本记录/V1.8_本次更新说明_20261031.md) · [主题覆盖](复审与版本记录/V1.8_原339页主题覆盖表_20261031.md) · [交叉复审与验收](复审与版本记录/V1.8_复审与验收_20261031.md) · [文件总索引](00_使用说明/V1.8_当前文件总索引_2026-10-31.md)

20册累计{total_pages}页，超全景按URL去重收录{refs}项参考资料。结构检查、{arithmetic}项算式复算与抽样视觉检查范围见验收记录；这不代表全历史事实重审或全部PDF逐页人工验收。单源、公司样本、转存件与未核缺口均保留。

旧[V1.7现行正文版](V1.7现行正文版/index.html)、[V1.6.1校注版](V1.6.1完整校注版/index.html)和[原339页冻结底本](09_历史冻结基线/超全景339页_20261009更新前.pdf)独立保留。新源码在`10_源码_markdown/V1.8_现行正文_20261031/`；[重建说明](11_源码_python生成脚本/README_v18_runtime.md)与构建、QA、复算脚本一同保存。本地完成状态与外部发布分别确认。
''')
    rows = '\n'.join(f'| {r["title"]} | {r["pages"]} | [PDF](../V1.8现行正文版/{r["slug"]}.pdf) · [网页](../V1.8现行正文版/{r["slug"]}.html) · [Markdown](../V1.8现行正文版/{r["slug"]}.md) |' for r in reports)
    write(ROOT/'00_使用说明/V1.8_当前文件总索引_2026-10-31.md', f'''# V1.8 当前文件总索引

大队长 · 2026年10月31日。20册来自同一组正文，实测合计{total_pages}页。第18—20册分别为AI视频短剧、编程旧预测复盘和其他应用商业化专题。

| 版本 | 实测页数 | 文件 |
|---|---:|---|
{rows}

[更新说明](../复审与版本记录/V1.8_本次更新说明_20261031.md) · [复审与验收](../复审与版本记录/V1.8_复审与验收_20261031.md) · [旧V1.7](../V1.7现行正文版/index.html)
''')

    files = {repo/'README.md', repo/'CHANGELOG.md', ROOT/'README.md'}
    files.update(p for p in OUT.rglob('*') if p.is_file() and 'qa_visual' not in p.parts)
    files.update(p for p in SRC.rglob('*') if p.is_file())
    files.update((ROOT/'复审与版本记录').glob('V1.8*'))
    files.update((ROOT/'00_使用说明').glob('V1.8*'))
    files.update((ROOT/'11_源码_python生成脚本').glob('*v18*'))
    files = {p for p in files if p.is_file() and '__pycache__' not in p.parts}
    errors = []
    for p in files:
        if p.suffix not in ('.md', '.html'): continue
        text = p.read_text(encoding='utf-8')
        parser = Parser(); parser.feed(text if p.suffix == '.html' else markdown.markdown(text, extensions=['tables']))
        for ref in parser.links+parser.images:
            if not ref or ref.startswith(('https://','http://','mailto:','#')): continue
            target = (p.parent/unquote(ref.split('#')[0])).resolve()
            if target == repo/'V1.8-publication-files.json': continue
            if not target.is_file(): errors.append(f'{p.relative_to(repo)} -> {ref}')
    if errors: raise RuntimeError('Broken local links: '+str(errors))
    for r in reports:
        for ext in ('pdf','md','html'):
            assert sha(ROOT/r[ext]['path']) == r[ext]['sha256']
    changed = subprocess.check_output(['git','-c','core.quotepath=false','diff','--name-only'], cwd=repo).decode('utf-8').splitlines()
    allowed = {'README.md','CHANGELOG.md','AI泡沫研究报告/README.md'}
    assert not (set(changed)-allowed), f'Historical tracked files changed: {changed}'
    payload = {'version':'V1.8','cutoff':'2026-10-31 Asia/Shanghai','status':'PASS_LOCAL_DELIVERY',
               'pdf_count':20,'pdf_pages':total_pages,'full_edition_references':refs,
               'arithmetic_checks':arithmetic,'visual_scope':visual['scope'],
               'scope':'local research update; targeted multi-agent review, structural and sampled visual QA; no remote publication',
               'git_branch':subprocess.check_output(['git','branch','--show-current'],cwd=repo).decode().strip(),
               'historical_tracked_files_changed':[], 'remote_push_performed':False,
               'files':[{'path':p.relative_to(repo).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)]}
    write(repo/'V1.8-publication-files.json', json.dumps(payload,ensure_ascii=False,indent=2))
    print(json.dumps({k:payload[k] for k in ('status','pdf_count','pdf_pages','full_edition_references','arithmetic_checks','git_branch')}, ensure_ascii=False,indent=2))


if __name__ == '__main__': main()
