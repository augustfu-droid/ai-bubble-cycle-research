# V2.0 主报告构建

V2.0 的中文底稿为 [V1.9 主报告](../V1.9现行正文版/01_主报告.md)。英文从 [V1.9 英文全本](../V1.9_English_Full_Report/AI_Cycles_and_Bubble_Full_Report_EN_2026-10-31.md) 中取对应的第 1 至 11 章。V2.0 新增第十二章资产回收试算和第十三章区域市场研究。报告的开篇、各章增量及旧状态的定点修订集中在 [V2.0 源稿](../10_源码_markdown/V2.0_20261121/)。

在仓库根目录运行以下命令。需要 Python、Markdown、PyMuPDF 和 WeasyPrint。Windows 独立版 WeasyPrint 可沿用原构建器的 `WEASYPRINT_EXECUTABLE` 环境变量。

```powershell
python -B 'AI泡沫研究报告/11_源码_python生成脚本/build_v20_main.py'
```

构建 Markdown、HTML、PDF 和产物清单，输出到 [V2.0 发布目录](../V2.0_配套发布_20261121/index.html)。目录、图表与页码从正文生成。使用 `--prepare-only` 可以仅生成可编辑文本和网页。第十三章保留 V1.9 的区域传导方法并链接原章。构建过程将正文的 Anthropic 融资状态同步到实际交割，保留其历史申报出处。

[复审与验收](../复审与版本记录/V2.0_20261121/acceptance.md)
