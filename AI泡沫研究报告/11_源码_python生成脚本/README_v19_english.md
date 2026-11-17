# Rebuilding the V1.9 English full report

The English edition is a complete translation of the corrected Chinese V1.9 full report. It does not refresh the underlying research. The reviewed English parts and frozen numbered Chinese inputs are in `../10_源码_markdown/V1.9_English_20261031/`. Preserve their line alignment so that paragraph, table, link and numeric differences remain reviewable.

The build shares the existing Python 3.14, Markdown, PyMuPDF, Noto font files and standalone WeasyPrint environment described in [the V1.9 runtime notes](README_v19_runtime.md). From the repository root:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
$env:WEASYPRINT_EXECUTABLE = Join-Path $env:USERPROFILE '.cache\weasyprint\v70.0\onedir\weasyprint\weasyprint.exe'
& 'C:\Python314\python.exe' 'AI泡沫研究报告\11_源码_python生成脚本\assets_v19_english.py'
& 'C:\Python314\python.exe' 'AI泡沫研究报告\11_源码_python生成脚本\check_v19_english_translation.py'
& 'C:\Python314\python.exe' 'AI泡沫研究报告\11_源码_python生成脚本\build_v19_english.py'
& 'C:\Python314\python.exe' 'AI泡沫研究报告\11_源码_python生成脚本\qa_v19_english.py'
```

The text checker inventories numeric changes; it does not infer semantic equivalence from equal numbers. Three independent peer-review records tie every final English part to its input and output hashes. Chart generation translates lettering while checking that plotted geometry is unchanged. The final PDF has eight unique charts in ten placements, matching the Chinese report.

`finalize_v19_english.py` requires current source/output hashes, all three semantic reviews, artifact checks, and a real visual-review record for the exact final PDF. Changing prose, reference labels, chart mappings or rendering invalidates the corresponding review evidence; update that evidence before finalizing. The original Chinese publication manifest and all of its listed files must remain unchanged.

Final English artifacts are written to `../V1.9_English_Full_Report/`. The separate root manifest `V1.9-English-publication-files.json` records this local delivery. The workflow does not commit or push to GitHub.
