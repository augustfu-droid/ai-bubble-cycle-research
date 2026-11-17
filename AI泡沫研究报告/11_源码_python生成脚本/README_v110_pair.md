# V1.10 中英文详细版与简版构建

本次是 2026-11-17 的专题增量修订。原 V1.9 研究资料范围仍截至 2026-10-31；新增专题和相关判断另行标注 11 月 17 日，不宣称全报告重核。

源码目录：`../10_源码_markdown/V1.10_20261117/`。每种语言各有四份作者源文件：

- `author_view_zh.md`、`author_view_en.md`：开篇作者观点，先风险时间窗，保留时间情景与技术/现金回收两张矩阵。
- `brief_zh.md`、`brief_en.md`：独立简版。
- `event_chapter_zh.md`、`event_chapter_en.md`：分别以 `## 第十四章：` / `## Chapter 14:` 开头，仅一个二级标题；子节编号使用 `14.x`。
- `body_updates_zh.json`、`body_updates_en.json`：数组，恰好包含第 1、2、8、10、12、13 章各一条；字段严格为 `chapter`（整数）、`heading`（不带井号、不编号，明确含“11月17日”/“17 November”/“November 17”）、`markdown`（正文，可含四级及以下标题）。

构建器从冻结 V1.9 发布 Markdown 的 `BODY_START` 之后读取正文，以精确章边界追加更新，并在第 13 章后、附篇 A 前插入第 14 章。七段新增内容均有成对 `V110_INSERT_START/END` 注释；移除这七段后须逐字符恢复原正文。旧标题全部保留原 `h-*` 锚点，新增标题使用 `update-*`，作者观点使用 `view-*`，因此旧正文交叉链接不会因新标题而偏移。

沿用 V1.9.2 的字体、页面样式、封面结构、可点击目录、书签和图资产。旧研究正文、13 章、附篇 A-F、342 个原有去重来源 URL 和图表均保留。缺少作者源文件时停止，不生成占位报告。

英文详细版仅为第 14.4 节唯一表头 `Purpose of commitment` 的承诺表添加 `event-commitments` 类和专用列宽，保持 FY28、FY29、Total 表头完整；不改变其他表或作者 Markdown。中英文版本说明另区分原索引 342 项与更新段落新增 19 个去重网址，当前详细版总计 361 个。

在仓库根目录使用 PowerShell：

```powershell
$env:WEASYPRINT_EXECUTABLE = 'C:\Users\付强\.cache\weasyprint\v70.0\onedir\weasyprint\weasyprint.exe'
C:/Python314/python.exe 'AI泡沫研究报告/11_源码_python生成脚本/build_v110_pair.py' --freeze-only
C:/Python314/python.exe 'AI泡沫研究报告/11_源码_python生成脚本/build_v110_pair.py'
C:/Python314/python.exe 'AI泡沫研究报告/11_源码_python生成脚本/qa_v110_pair.py'
```

可用 `--only full_zh brief_zh` 等参数按版本重建。完整交付必须生成四份 PDF，以及各自 HTML、Markdown。输出目录为 `../V1.10_配套发布_20261117/`；复审目录为 `../复审与版本记录/V1.10_20261117/`。

`baseline.json` 冻结 V1.8、V1.9、英文 V1.9、V1.9.1、V1.9.2 的发布清单及其非导航文件，并复核原 636 项历史文件。仅仓库 `README.md`、`CHANGELOG.md` 和报告根 `README.md` 允许作为当前导航更新。V1.7 旧清单已有先前版本造成的差异，本次不把它伪称为与最早发布状态一致。

`qa.json` 包含来源及输出哈希、旧正文还原、旧锚点映射、章节顺序、图表、来源、全页文字边界、PDF 书签、可点击目录和实际页码检查。`qa_visual/` 渲染全部新增段落及其跨页边界、开篇、目录、简版全部页面和选定旧正文页；它仍须由审阅者实际看图，自动检查不能替代视觉验收。最终导航、语义复审、视觉验收及 Git 发布由独立流程完成，构建器不自动发布。
