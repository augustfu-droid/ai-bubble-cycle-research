# V1.8 Windows 构建环境

构建器、结构核验均使用 Python 3.14、PyMuPDF 和 Markdown。文本读写固定为 UTF-8，不依赖 Windows 的默认代码页。

## PDF 渲染器

`build_v18_current.py` 延迟加载 WeasyPrint。设置 `WEASYPRINT_EXECUTABLE` 后，使用该独立可执行程序渲染已经写出的 HTML；未设置时，使用 Python WeasyPrint。结构核验只导入共享函数，不会加载 WeasyPrint 或 GTK/Pango DLL。

本机已验证的独立程序：

```powershell
$env:WEASYPRINT_EXECUTABLE = Join-Path $env:USERPROFILE '.cache\weasyprint\v70.0\onedir\weasyprint\weasyprint.exe'
& $env:WEASYPRINT_EXECUTABLE --info
& 'C:\Python314\python.exe' 'AI泡沫研究报告\11_源码_python生成脚本\build_v18_current.py'
& 'C:\Python314\python.exe' 'AI泡沫研究报告\11_源码_python生成脚本\qa_v18_current.py'
```

上述命令从仓库根目录执行。环境变量只影响当前 PowerShell 进程及其子进程，不写入系统设置。构建器支持原有的 `--only` 参数；不加参数才构建整个目录。正式构建必须在正文冻结后执行。

独立程序来自 [WeasyPrint 官方 v70.0 发布页](https://github.com/Kozea/WeasyPrint/releases/tag/v70.0)，文件为 `weasyprint-windows-onedir.zip`，SHA-256 为 `ab1151f210b4e6bb7aa7a79e91a67e8ddb760094c107bfda55241b6aaefe7d53`。归档及解压文件都放在用户缓存，不纳入仓库。换机时从该发布页取得相同归档，校验摘要后解压，并把变量指向实际的 `weasyprint.exe`。

[官方 Windows 安装说明](https://doc.courtbouillon.org/weasyprint/latest/first_steps.html#windows)推荐独立可执行程序；若直接使用 Python 库，则还需自行提供 Pango 等原生依赖。此配置无需安装 MSYS2 或修改安全防护设置。
