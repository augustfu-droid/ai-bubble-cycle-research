# V1.9.1 配套报告重建

本版为2026年11月1日的作者观点与简版修订，研究资料截止仍为10月31日。作者时间预测重新登记，完整研究正文不改。中英文详细版及简版合计四份PDF，并生成HTML、Markdown。

源码位于 `10_源码_markdown/V1.9.1_观点与简版_20261101/`。两种语言的完整正文从已经验收的V1.9发布Markdown的 `BODY_START` 标记之后读取，必须与冻结正文逐字节一致。图表复制既有已验收文件。

Windows PowerShell，仓库根目录执行：

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:WEASYPRINT_EXECUTABLE='C:\Users\付强\.cache\weasyprint\v70.0\onedir\weasyprint\weasyprint.exe'
C:/Python314/python.exe 'AI泡沫研究报告/11_源码_python生成脚本/build_v191_pair.py'
C:/Python314/python.exe 'AI泡沫研究报告/11_源码_python生成脚本/qa_v191_pair.py'
```

构建可用 `--only full_zh brief_zh full_en brief_en` 选择实际变动的版本。仅生成文件不能视为已验收；最终需中文独立语义复审、英文独立忠实性复审和实际PDF视觉检查，均绑定最终源与输出SHA256。

复审JSON位于 `复审与版本记录/V1.9.1_20261101/`。视觉记录采用 `status: PASS` 与 `reports` 列表，每项包括 `key`、`pdf_sha256`、`pages_reviewed`。不得由文字抽取或渲染成功自动产生视觉PASS。

全部检查及独立复审完成后运行：

```powershell
C:/Python314/python.exe 'AI泡沫研究报告/11_源码_python生成脚本/finalize_v191_pair.py'
```

最终器复核历史文件，更新本地导航和文件清单。三份当前导航/变更说明允许变化，其余202项前次中英文交付文件保持不变。本流程不推送GitHub、不操作Substack、不发送邮件。附件由作者或其指定工具另行替换。
