#!/usr/bin/env python3
"""Accept reviewed paired editions and refresh local reading entrypoints."""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
import build_v192_pair as b


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    mf = load(b.OUT / 'manifest.json')
    qa = load(b.OUT / 'qa.json')
    assert qa['status'] == 'PASS_STRUCTURE', qa['errors']
    prior_count = qa['prior_artifacts_unchanged']
    zh_review = load(b.REVIEW / 'semantic_review_zh.json')
    en_review = load(b.REVIEW / 'semantic_review_en.json')
    assert zh_review['verdict'] == 'pass'
    assert en_review['status'] == 'PASS'
    for row in zh_review['reviewed_files']:
        assert b.sha(b.ROOT / row['file']) == row['sha256'], row['file']
    for name, digest in en_review['file_sha256'].items():
        assert b.sha(b.SRC / name) == digest, name
    rows = {r['key']: r for r in mf['reports']}
    visual = []
    for lang in ('zh', 'en'):
        record = load(b.REVIEW / f'visual_{lang}.json')
        assert record['status'] == 'PASS', record
        for item in record['reports']:
            assert item['pdf_sha256'] == rows[item['key']]['outputs']['pdf']['sha256']
            assert item['pages_reviewed'], item
        visual.append(record)
    for r in mf['reports']:
        for rec in r['outputs'].values():
            assert b.sha(b.REPO / rec['path']) == rec['sha256']
    for old in load(b.REVIEW / 'baseline.json')['files']:
        if not old['mutable_entrypoint']:
            assert b.sha(b.REPO / old['path']) == old['sha256']
    history_path = b.ROOT / '复审与版本记录/V1.9_拉取基线历史文件哈希_20261031.json'
    history = load(history_path)
    for name, row in history['files'].items():
        assert b.sha(b.REPO / name) == row['working_tree_sha256'], name
    folder = b.OUT.relative_to(b.ROOT).as_posix()
    rootfolder = b.OUT.relative_to(b.REPO).as_posix()

    def link(key, prefix='', ext='pdf', label=None):
        row = rows[key]
        label = label or {'full_zh': '中文详细版', 'brief_zh': '中文简版', 'full_en': 'English full report', 'brief_en': 'English brief'}[key]
        return f'[{label}：{row["pages"]}页]({prefix}{row["stem"]}.{ext})'

    local_links = ' · '.join(link(k) for k in ('full_zh', 'brief_zh', 'full_en', 'brief_en'))
    note = '编辑日期2026-11-01；研究资料截止仍为2026-10-31（北京时间），每项事实保留自身期间。'
    thesis = '作者把2027年上半年至2028年上半年列为AI资本泡沫较大范围破裂的主要风险窗口，并在开篇列出提前信用冲击、延后放大、逐步消化三条替代路径。时间窗沿用V1.9.1于11月1日重新登记的作者主观预测；到2028年6月底未兑现须明确结算，不能自动顺延计为正确。'
    scope = '两种语言的详细版都保留V1.9完整正文、13章、附篇A至F、图表和342个按URL去重的参考链接；扩充后的核心观点、时间情景和技术进展×付费回收矩阵置于封面后、版本说明和目录之前。简版可独立发送，保留12个已有原始来源链接。'
    (b.OUT / 'README.md').write_text(f'# AI周期与泡沫研究 · 配套发布版\n\n大队长 · V1.9.2\n\n{note}\n\n{local_links}\n\n{thesis}\n\n{scope}\n\n中英文两套各含PDF、HTML与可编辑Markdown。推荐同一语言的详细版和简版一起发送。\n\n已发布的Substack文章可在附件菜单选择Replace替换文件，再保存文章更新。该操作由作者另行处理；本地生成不代表附件已上传或已发布。平台机制见[附件说明](https://support.substack.com/hc/en-us/articles/4408381643156-How-can-I-attach-a-file-to-my-Substack-post)与[文章更新说明](https://support.substack.com/hc/en-us/articles/360039017132-How-do-I-edit-a-post-that-I-ve-published-on-Substack)。\n\n本地验收范围见[验收记录](../复审与版本记录/V1.9.2_20261101/acceptance.md)、[结构检查](qa.json)和[文件清单](manifest.json)。个人研究，不构成投资建议。\n', encoding='utf-8')
    htmlrows = ''.join(f'<tr><td>{html.escape({"full_zh":"中文详细版","brief_zh":"中文简版","full_en":"English full report","brief_en":"English brief"}[r["key"]])}</td><td>{r["pages"]}</td><td><a href="{r["stem"]}.pdf">PDF</a> · <a href="{r["stem"]}.html">HTML</a> · <a href="{r["stem"]}.md">Markdown</a></td></tr>' for r in mf['reports'])
    (b.OUT / 'index.html').write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI周期与泡沫研究 · V1.9.2</title><style>body{{font:17px/1.85 system-ui;max-width:980px;margin:40px auto;padding:24px;color:#28475e;background:#f8fbfd}}h1{{color:#315e7c}}a{{color:#356e93}}table{{width:100%;border-collapse:collapse}}td,th{{padding:13px;border-bottom:1px solid #cadce8;text-align:left}}.lead{{padding:20px;background:#eaf3f9;border-left:5px solid #91bdd5}}</style></head><body><h1>AI周期与泡沫研究 · V1.9.2</h1><p>大队长 · {note}</p><div class="lead">{thesis}</div><h2>详细版与简版配套发送</h2><table><thead><tr><th>版本</th><th>页数</th><th>格式</th></tr></thead><tbody>{htmlrows}</tbody></table><p>{scope}</p><p><a href="README.md">使用说明</a> · <a href="../复审与版本记录/V1.9.2_20261101/acceptance.md">复审与验收</a></p><p>本地文件已完成，Substack附件由作者另行替换。个人研究，不构成投资建议。</p></body></html>', encoding='utf-8')
    new_section = f'''## 当前报告

{link('full_zh', rootfolder+'/')} · {link('brief_zh', rootfolder+'/')}

{link('full_en', rootfolder+'/')} · {link('brief_en', rootfolder+'/')} · [全部格式与配套说明]({rootfolder}/index.html)

{thesis}

{scope} {note}

开篇进一步补齐利润质量、资本循环、技术突破的双向作用、企业分化、中国传导、政策与能源约束，以及技术价值与股东回报的区别。保留“延迟即放大”、现金回收、GPU折旧、短剧与编程判断。中文原稿与英文译文经过独立交叉审阅，时间预测的主观性质和改判条件明确标出。

[复审与验收](AI泡沫研究报告/复审与版本记录/V1.9.2_20261101/acceptance.md) · [交付清单](V1.9.2-publication-files.json) · [上一版V1.9.1](AI泡沫研究报告/V1.9.1_配套发布_20261101/index.html) · [V1.9原20册](AI泡沫研究报告/V1.9现行正文版/index.html) · [原英文完整报告](AI泡沫研究报告/V1.9_English_Full_Report/index.html)

'''
    root_readme = b.REPO / 'README.md'
    text = root_readme.read_text(encoding='utf-8')
    text = re.sub(r'\*\*最新版本\*\*：[^\n]+', '**最新版本**：V1.9.2 核心观点与双矩阵修订（2026-11-01）', text, count=1)
    text = re.sub(r'## 当前报告\n.*?(?=## 历史仓库目录)', new_section, text, count=1, flags=re.S)
    text = re.sub(r'默认阅读入口为上方V1\.9(?:\.\d+)?；', '默认阅读入口为上方V1.9.2；', text)
    root_readme.write_text(text, encoding='utf-8')
    (b.ROOT / 'README.md').write_text(f'# AI周期与泡沫研究报告\n\n大队长 · 当前版本 **V1.9.2（2026-11-01）**。{note}\n\n联系邮箱：[fqsx@mail.ustc.edu.cn](mailto:fqsx@mail.ustc.edu.cn)。\n\n{link("full_zh",folder+"/")} · {link("brief_zh",folder+"/")}\n\n{link("full_en",folder+"/")} · {link("brief_en",folder+"/")} · [全部格式]({folder}/index.html)\n\n{thesis}\n\n{scope}\n\n[复审与验收](复审与版本记录/V1.9.2_20261101/acceptance.md) · [构建说明](11_源码_python生成脚本/README_v192_pair.md) · [V1.9原20册](V1.9现行正文版/index.html) · [原英文完整报告](V1.9_English_Full_Report/index.html) · [V1.8存档](V1.8现行正文版/index.html)\n\n旧研究源码、历史预测、图表及已验收PDF独立保留。{prior_count}项旧交付文件与636项历史文件逐项核对；仅三份导航/变更说明文件允许随当前入口更新。本次为本地修订，不代表已推送GitHub或已替换Substack附件。个人研究，不构成投资建议。\n', encoding='utf-8')
    change_path = b.REPO / 'CHANGELOG.md'
    change = change_path.read_text(encoding='utf-8')
    heading = '## V1.9.2（2026-11-01）· 核心观点扩充与双矩阵'
    entry = f'''{heading}

- 在时间预测前置的基础上，补齐作者其他核心观点，保留可复查的旧观点来源与现行证据。
- 新增技术进展×付费回收矩阵，说明承压主体、相对缓冲与改判条件，不与时间路径相加成概率。
- 沿用V1.9.1登记的2027上半年至2028上半年的主观基准风险窗口；列明提前、延后和消化情景，以及2028年6月底未兑现的结算约束，不恢复旧概率或跌幅。
- 中英文详细版分别为{rows['full_zh']['pages']}、{rows['full_en']['pages']}页；独立简版分别为{rows['brief_zh']['pages']}、{rows['brief_en']['pages']}页，可配套发送。
- 两种语言的完整研究正文与既有342个参考URL保持不变；本次编辑不冒充11月新一轮财务研究。
- 完成中文独立语义审查、英文交叉校对与PDF结构/实际视觉验收；原研究与旧交付独立保留。

详见[配套阅读入口]({rootfolder}/index.html)、[验收记录](AI泡沫研究报告/复审与版本记录/V1.9.2_20261101/acceptance.md)及[交付清单](V1.9.2-publication-files.json)。Substack发布由作者另行处理。

'''
    if heading not in change:
        change = change.replace('# 版本变更记录\n\n', '# 版本变更记录\n\n'+entry, 1)
    change_path.write_text(change, encoding='utf-8')
    visual_pages = sum(len(x['pages_reviewed']) for rec in visual for x in rec['reports'])
    acceptance = f'''# V1.9.2 本地交付验收

状态：PASS_LOCAL_DELIVERY。编辑日期：2026-11-01；研究资料截止：2026-10-31。

{thesis}

本次扩充作者核心观点与技术进展/付费回收矩阵，沿用已登记时间预测，并同步独立简版。两种语言的详细报告完整研究正文逐字节比对旧版通过，继续保留13章、附篇A至F、图表与342个去重参考URL。两份简版各使用12个已有原始链接。

中文独立复审核对观点的历史来源、现行证据、两张矩阵与简版的一致性；英文非主笔审阅逐段核对译文。具体发现、闭环范围与最终哈希见semantic_review_zh.json和semantic_review_en.json；不沿用上一版审阅结果冒充本次审阅。

结构检查覆盖源/输出哈希、正文完整性、目录与书签的实际页码、章节连续性、引用与图片、全页文本边界。两位复审代理实际查看共{visual_pages}个PDF页面样本，其中简版全部页面；详细版覆盖新前言、说明、全部目录及选定正文过渡。此为明确范围的抽样视觉验收，不是对全部旧正文再做事实审计。

{prior_count}项原V1.9及V1.9.1交付文件保持不变，636项历史文件哈希通过；三份当前导航/变更说明文件按本版更新。未推送远程，未替换Substack附件，未发送邮件。

文件：{local_links.replace('](', '](' + '../../' + folder + '/')}
'''
    (b.REVIEW / 'acceptance.md').write_text(acceptance, encoding='utf-8')
    mf['status'] = 'PASS_LOCAL_DELIVERY'
    mf['qa_sha256'] = b.sha(b.OUT / 'qa.json')
    mf['semantic_and_visual_reviews'] = {name: b.sha(b.REVIEW / name) for name in ('semantic_review_zh.json', 'semantic_review_en.json', 'visual_zh.json', 'visual_en.json')}
    mf['historical_files_unchanged'] = len(history['files'])
    b.write_json(b.OUT / 'manifest.json', mf)
    paths = [p for directory in (b.OUT, b.SRC, b.REVIEW) for p in directory.rglob('*') if p.is_file() and p.suffix.lower() not in ('.png',)]
    paths += [b.REPO/'README.md', b.ROOT/'README.md', b.REPO/'CHANGELOG.md']
    paths += [Path(__file__), Path(b.__file__), Path(__file__).with_name('qa_v192_pair.py'), Path(__file__).with_name('README_v192_pair.md')]
    records = [{'path':p.relative_to(b.REPO).as_posix(), 'bytes':p.stat().st_size, 'sha256':b.sha(p)} for p in sorted(set(paths))]
    b.write_json(b.REPO/'V1.9.2-publication-files.json', {'version':b.VERSION, 'status':'PASS_LOCAL_DELIVERY', 'editorial_date':b.EDIT_DATE, 'research_cutoff':b.CUTOFF, 'scope':'Local editorial revision, paired full/brief reports in Chinese and English; no remote publication', 'pdf_count':4, 'pages':{k:r['pages'] for k,r in rows.items()}, 'prior_publication_files_unchanged':prior_count, 'historical_files_unchanged':len(history['files']), 'visual_pages_reviewed':visual_pages, 'remote_push_performed':False, 'substack_attachment_updated':False, 'files':records})
    print(json.dumps({'status':'PASS_LOCAL_DELIVERY','pages':{k:r['pages'] for k,r in rows.items()},'files':len(records),'visual_pages':visual_pages},ensure_ascii=False))


if __name__ == '__main__':
    main()
