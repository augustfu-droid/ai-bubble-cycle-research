#!/usr/bin/env python3
"""Build the post-submission V1.4 report line without touching submitted files.

Outputs:
  - main report V1.4
  - fact audit V1.4 (63-item frozen base + 10 new items, rolling checked through 2026-07-24)
  - institutional brief V1.4
  - complete panorama V1.4 (source re-render)
  - 300+ page super-panorama V1.4 (integrated update module + complete frozen legacy edition)
  - public, Snowball, summary and execution maintenance editions
  - four component-report maintenance editions
  - complete compilation, delayed-amplification, crash-script and public-intro maintenance editions

The submitted ZIP and every historical PDF remain read-only inputs. Maintenance
editions prepend the current update module and retain the complete historical
layout, page links and source text behind an explicit frozen-edition divider.
"""
from __future__ import annotations

import io
import re
from pathlib import Path

import markdown
from pypdf import PdfReader, PdfWriter
from pypdf.constants import PageLabelStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from weasyprint import CSS, HTML


ARCHIVE = Path(__file__).resolve().parents[1]
SRC = ARCHIVE / "10_源码_markdown"
INCR = ARCHIVE / "12_增量素材"
FONT_DIR = ARCHIVE / "11_源码_python生成脚本/fonts"

VERSION = "V1.4"
UPDATE_DATE = "2026/07/24"
DATA_DATE = "2026/07/24"

V14_CHANGELOG_ROW = (
    "| **V1.4·7/24 滚动** | **2026/07/24** | **投递后研究维护版**：在 V1.4 首发基础上补入 Alphabet 官方 CEO "
    "书面发言、7/23 市场反应和 DeepSeek 一手资料复核；事实审计表 63→73 项，并显式勘误“DeepSeek V4-Pro 完全运行于"
    "华为芯片/DeepSeek R2 32B”旧口径。**综合崩盘指数维持 77，四情景维持 A44/B22/C10/D24；"
    "严格触发 1/3、广义预警 2/3；主时间窗不变。** |"
)

MAIN_OUT = ARCHIVE / "02_主报告V1.4/00_AI周期与泡沫深度研究报告_主报告_V1.4.pdf"
AUDIT_OUT = ARCHIVE / "02_主报告V1.4/01_AI周期与泡沫_事实审计表_V1.4.pdf"
BRIEF_OUT = ARCHIVE / "05_简版与执行摘要/AI周期与泡沫_机构简版_V1.4_内部署名版.pdf"
PANO_OUT = ARCHIVE / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4完整重排版.pdf"
THICK_OUT = ARCHIVE / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4超全景版_300页级.pdf"
UPDATE_OUT = INCR / "2026-07-24_V1.4滚动更新模块.pdf"

MASTER_MD = INCR / "2026-07-20_V1.4更新模块_全报告统一口径.md"
MAIN_MD = SRC / "AI周期与泡沫深度研究报告.md"
AUDIT_BASE_MD = SRC / "AI周期与泡沫_事实审计表_V1.3.4.md"
AUDIT_INCR_MD = SRC / "AI周期与泡沫_事实审计表_V1.4_增量.md"
BRIEF_MD = SRC / "AI周期与泡沫_机构简版_V1.4.md"
PANO_BASE_MD = SRC / "AI周期与泡沫深度研究报告_全景版_V1.3.4重排合成源.md"
THICK_BASE_PDF = ARCHIVE / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.3.4修订版.pdf"

LEGACY_VARIANTS = (
    (
        ARCHIVE / "09_历史冻结基线/04_分项报告/01_利润真实性拆解_历史冻结版.pdf",
        ARCHIVE / "04_分项报告/01_利润真实性拆解_V1.4维护版.pdf",
        "分项报告01 · 利润真实性拆解",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/04_分项报告/02_循环投资网络_V1.3.4勘误附页冻结版.pdf",
        ARCHIVE / "04_分项报告/02_循环投资网络_V1.4维护版.pdf",
        "分项报告02 · 循环投资网络",
        1,
    ),
    (
        ARCHIVE / "09_历史冻结基线/04_分项报告/03_AI变现与编程TAM_历史冻结版.pdf",
        ARCHIVE / "04_分项报告/03_AI变现与编程TAM_V1.4维护版.pdf",
        "分项报告03 · AI变现与编程TAM",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/04_分项报告/04_AGI与国际格局_历史冻结版.pdf",
        ARCHIVE / "04_分项报告/04_AGI与国际格局_V1.4维护版.pdf",
        "分项报告04 · AGI与国际格局",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/05_简版与执行摘要/公开精简版_V1.3.4冻结版.pdf",
        ARCHIVE / "05_简版与执行摘要/2026年AI泡沫研究 · 公开精简版_V1.4维护版.pdf",
        "2026年AI泡沫研究 · 公开精简版",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/05_简版与执行摘要/雪球公开版_V1.3.4冻结版.pdf",
        ARCHIVE / "05_简版与执行摘要/2026年AI泡沫研究 · 雪球公开版_V1.4维护版.pdf",
        "2026年AI泡沫研究 · 雪球公开版",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/05_简版与执行摘要/摘要版_历史冻结版.pdf",
        ARCHIVE / "05_简版与执行摘要/2026年AI泡沫研究 · 摘要版_V1.4维护版.pdf",
        "2026年AI泡沫研究 · 摘要版",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/05_简版与执行摘要/执行简版_历史冻结版.pdf",
        ARCHIVE / "05_简版与执行摘要/AI周期与泡沫研究_执行简版_V1.4维护版.pdf",
        "AI周期与泡沫研究 · 执行简版",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/06_全景与剧本版/完整合集_V1.3.4勘误附页冻结版.pdf",
        ARCHIVE / "06_全景与剧本版/AI周期与泡沫_完整合集_V1.4维护版.pdf",
        "AI周期与泡沫 · 完整合集",
        1,
    ),
    (
        ARCHIVE / "09_历史冻结基线/06_全景与剧本版/延迟即放大版_历史冻结版.pdf",
        ARCHIVE / "06_全景与剧本版/AI泡沫全景研究_延迟即放大版_V1.4维护版.pdf",
        "AI泡沫全景研究 · 延迟即放大版",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/06_全景与剧本版/AI泡沫崩盘剧本_历史冻结版.pdf",
        ARCHIVE / "06_全景与剧本版/AI泡沫崩盘剧本_V1.4维护版.pdf",
        "AI泡沫崩盘剧本",
        0,
    ),
    (
        ARCHIVE / "09_历史冻结基线/06_全景与剧本版/公众号00_发布引流稿_历史冻结版.pdf",
        ARCHIVE / "06_全景与剧本版/公众号00_发布引流稿_V1.4维护版.pdf",
        "公众号00 · 发布引流稿",
        0,
    ),
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def without_first_h1(text: str) -> str:
    return re.sub(r"(?m)^# .+\n+", "", text, count=1)


def historical_main_body(text: str) -> str:
    """Drop the stale current-version preamble but retain the version history and body."""
    parts = re.split(r"\n## 版本变更说明\s*\n", text, maxsplit=1)
    if len(parts) == 2:
        history = insert_v14_changelog(parts[1])
        return "## 完整版本变更记录（V1.4 最新）\n\n" + history
    return "## V1.3.4 历史正文基线\n\n" + without_first_h1(text)


def insert_v14_changelog(text: str) -> str:
    """Insert V1.4 as the newest row in the first version-history table."""
    if V14_CHANGELOG_ROW in text:
        return text
    marker = "|---|---|---|\n"
    if marker in text:
        return text.replace(marker, marker + V14_CHANGELOG_ROW + "\n", 1)
    return text


def assembled_main() -> str:
    return (
        "# AI周期与泡沫深度研究报告\n\n"
        + read(MASTER_MD)
        + "\n\n---\n\n"
        + "> **历史正文阅读提示**：以下深度正文保留当时版本的日期、分数和概率，用于展示研究推演与证据链。"
          "凡属动态数值、当前结论与触发器状态，均以本报告卷首 V1.4 更新模块为准。\n\n"
        + historical_main_body(read(MAIN_MD))
    )


def assembled_audit() -> str:
    base = without_first_h1(read(AUDIT_BASE_MD))
    incr = without_first_h1(read(AUDIT_INCR_MD))
    return (
        "# AI周期与泡沫 · 事实审计表 V1.4（73 项）\n\n"
        + incr
        + "\n\n---\n\n"
        + "## V1.3.4a 冻结基表（63 项）\n\n"
        + "> 下列 63 项保持 V1.3.4a 原文，作为可回溯基表；其历史版本段落中的项数、分数与概率不是 V1.4 当前口径。\n\n"
        + base
    )


def assembled_panorama() -> str:
    base = insert_v14_changelog(read(PANO_BASE_MD))
    base = without_first_h1(base)
    return (
        "# 2026年AI泡沫研究 · 全景版 V1.4完整重排版\n\n"
        + read(MASTER_MD)
        + "\n\n---\n\n"
        + "# 全景深度正文（V1.3.4 结构基线，V1.4 动态口径已在卷首同步）\n\n"
        + "> **阅读规则**：历史章节保留其原始时点，便于审计研究过程；涉及当前分数、概率、市场价、触发状态与未来观察日，"
          "统一以卷首 V1.4 更新模块为准。\n\n"
        + base
    )


FONT_FACE = f"""
@font-face {{ font-family:'NotoSansSC'; src:url('file://{FONT_DIR}/NotoSansSC-Regular.ttf'); font-weight:400; }}
@font-face {{ font-family:'NotoSansSC'; src:url('file://{FONT_DIR}/NotoSansSC-Bold.ttf'); font-weight:700; }}
"""


def css_for(title: str, landscape: bool = False, compact: bool = False) -> str:
    size = "A4 landscape" if landscape else "A4"
    body_size = "8.1pt" if compact else "9.2pt"
    margin = "1.35cm 1.25cm 1.55cm" if landscape else "1.75cm 1.65cm 1.8cm"
    return FONT_FACE + f"""
@page {{ size:{size}; margin:{margin};
  @top-left {{ content:"付强 · {title}"; font-family:NotoSansSC; font-size:7.2pt; color:#77756F; }}
  @top-right {{ content:"V1.4 · 滚动核验至 {DATA_DATE}"; font-family:NotoSansSC; font-size:7.2pt; color:#77756F; }}
  @bottom-left {{ content:"个人研究 · 基于公开信息 · 不构成投资建议"; font-family:NotoSansSC; font-size:7pt; color:#AAA8A2; }}
  @bottom-right {{ content:"第 " counter(page) " 页 / 共 " counter(pages) " 页"; font-family:NotoSansSC; font-size:7.2pt; color:#77756F; }}
}}
@page cover {{ margin:0; @top-left {{content:none}} @top-right {{content:none}} @bottom-left {{content:none}} @bottom-right {{content:none}} }}
body {{ font-family:NotoSansSC,sans-serif; font-size:{body_size}; line-height:1.55; color:#28251D; }}
#cover {{ page:cover; height:29.7cm; box-sizing:border-box; padding:3.2cm 2.4cm; position:relative; page-break-after:always; }}
#cover .rule {{ width:4.6cm; height:.34cm; background:#004098; margin-bottom:1.0cm; }}
#cover .brand {{ color:#7A7974; font-size:9pt; letter-spacing:1px; }}
#cover .title {{ color:#002451; font-size:27pt; line-height:1.3; font-weight:700; margin-top:2.4cm; }}
#cover .sub {{ color:#55524A; font-size:11pt; line-height:1.8; margin-top:.8cm; }}
#cover .kpi {{ border-left:4px solid #004098; padding-left:.55cm; margin-top:1.5cm; font-size:10.5pt; line-height:1.9; }}
#cover .rev {{ background:#F5F8FC; border:1px solid #D3DFEE; padding:.5cm .6cm; margin-top:1.0cm; color:#70464B; font-size:9pt; line-height:1.65; }}
#cover .foot {{ position:absolute; bottom:2cm; left:2.4cm; right:2.4cm; border-top:.5pt solid #D4D1CA; padding-top:.35cm; color:#9B9992; font-size:8.2pt; }}
.toc {{ page-break-after:always; }}
.toc h1 {{ border:none; color:#002451; }}
.toc-row a {{ display:block; color:#28251D; text-decoration:none; border-bottom:.4pt dotted #CCC; padding:2px 0; }}
.toc-row a::after {{ content:target-counter(attr(href url), page); float:right; color:#004098; }}
.toc-row.l2 {{ font-weight:700; margin-top:3px; }}
.toc-row.l3 {{ padding-left:1.1em; font-size:8.5pt; }}
h1 {{ color:#004098; font-size:19pt; margin:.2em 0 .45em; padding-bottom:.2em; border-bottom:2px solid #004098; page-break-after:avoid; }}
h2 {{ color:#004098; font-size:13pt; margin:1.2em 0 .4em; padding-left:.3em; border-left:4px solid #004098; page-break-after:avoid; }}
h3 {{ color:#003070; font-size:10.8pt; margin:1em 0 .3em; page-break-after:avoid; }}
h4 {{ color:#003070; font-size:9.8pt; margin:.8em 0 .25em; page-break-after:avoid; }}
p {{ margin:.48em 0; }}
table {{ border-collapse:collapse; width:100%; margin:.45em 0 .8em; font-size:{'7.1pt' if compact else '7.8pt'}; }}
.keep-table {{ height:0; margin:0; padding:0; page-break-after:avoid; }}
.keep-table + table {{ page-break-inside:avoid; }}
thead {{ display:table-header-group; }} tr {{ page-break-inside:avoid; }}
th {{ background:#004098; color:white; border:1px solid #004098; padding:4px 6px; text-align:left; }}
td {{ border:.5px solid #D4D1CA; padding:4px 6px; vertical-align:top; line-height:1.4; overflow-wrap:anywhere; }}
tr:nth-child(even) td {{ background:#FAF9F7; }}
blockquote {{ border-left:3px solid #004098; background:#F7F9FC; margin:.5em 0; padding:.35em .8em; color:#55524A; }}
a {{ color:#004098; text-decoration:none; overflow-wrap:anywhere; }}
ul,ol {{ margin:.55em 0; padding-left:1.5em; }} li {{ margin:.45em 0; }}
hr {{ border:0; border-top:.5px solid #D4D1CA; margin:1em 0; }}
img {{ max-width:100%; max-height:21cm; object-fit:contain; }}
figure {{ page-break-inside:avoid; text-align:center; }}
code {{ background:#F4F3EF; padding:1px 3px; }}
"""


def cover_html(title: str, subtitle: str, extra: str = "") -> str:
    return f"""<section id="cover">
<div class="rule"></div><div class="brand">付强 · 独立研究 · 投递后维护版</div>
<div class="title">{title}</div><div class="sub">{subtitle}</div>
<div class="kpi"><b>综合崩盘指数</b>　77 / 100<br/>
<b>四情景</b>　A44 / B22 / C10 / D24（软着陆以外合计 76%）<br/>
<b>触发器</b>　严格执行 1/3 · 广义早期预警 2/3<br/>
<b>数据截止</b>　公司与研究资料核验至2026-07-24，市场收盘至2026-07-23</div>
<div class="rev">V1.4 核心更新：Oracle BBB- · TSMC Q2 · SPCX 跌破发行价 · 超大厂 CapEx 增速降档 · Alphabet 经营兑现与现金流裂缝双验证 · DeepSeek 一手资料勘误。{extra}</div>
<div class="foot">V1.4 · 2026-07-24滚动核验｜已投递材料与前瞻判断原件保持冻结｜不构成投资建议</div>
</section>"""


def add_ids_and_toc(html_body: str) -> tuple[str, str]:
    heads: list[tuple[int, str, str]] = []

    def repl(match: re.Match[str]) -> str:
        level = int(match.group(1))
        attrs = match.group(2)
        text = match.group(3)
        hid = f"sec-{len(heads):04d}"
        plain = re.sub(r"<[^>]+>", "", text).strip()
        if level <= 3 and plain:
            heads.append((level, plain, hid))
        return f'<h{level} id="{hid}"{attrs}>{text}</h{level}>'

    tagged = re.sub(r"<h([1-6])([^>]*)>(.*?)</h\1>", repl, html_body, flags=re.S)
    rows = []
    for level, plain, hid in heads:
        if level < 2 or len(plain) > 95:
            continue
        rows.append(f'<div class="toc-row l{level}"><a href="#{hid}">{plain}</a></div>')
    toc = '<section class="toc"><h1>目录</h1><p>页码为本版实际页码，条目可点击跳转。</p>' + "".join(rows) + "</section>"
    return tagged, toc


def build_markdown_pdf(md_text: str, out: Path, title: str, subtitle: str, *, landscape: bool = False,
                       compact: bool = False, toc: bool = True, extra_cover: str = "") -> int:
    out.parent.mkdir(parents=True, exist_ok=True)
    html_body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "footnotes", "attr_list"])
    html_body, toc_html = add_ids_and_toc(html_body)
    full = (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        f'<title>{title} V1.4</title></head><body>'
        + cover_html(title, subtitle, extra_cover)
        + (toc_html if toc else "")
        + html_body
        + "</body></html>"
    )
    HTML(string=full, base_url=str(SRC)).write_pdf(str(out), stylesheets=[CSS(string=css_for(title, landscape, compact))])
    pages = len(PdfReader(str(out)).pages)
    print(f"[OK] {out.name}: {pages} pages")
    return pages


def stamp_page(page, label: str):
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    if "NotoSansSC" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("NotoSansSC", str(FONT_DIR / "NotoSansSC-Regular.ttf")))
        pdfmetrics.registerFont(TTFont("NotoSansSC-Bold", str(FONT_DIR / "NotoSansSC-Bold.ttf")))
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.setFont("NotoSansSC", 6.2)
    c.drawRightString(width - 18, height - 12, label)
    c.setStrokeColorRGB(0.82, 0.82, 0.82)
    c.setLineWidth(0.25)
    c.line(18, height - 15, width - 18, height - 15)
    c.save()
    packet.seek(0)
    overlay = PdfReader(packet).pages[0]
    page.merge_page(overlay)
    return page


def stamp_disclaimer_header(page, title: str):
    """Replace a stale legacy header on the promoted full disclaimer page."""
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    if "NotoSansSC" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("NotoSansSC", str(FONT_DIR / "NotoSansSC-Regular.ttf")))
        pdfmetrics.registerFont(TTFont("NotoSansSC-Bold", str(FONT_DIR / "NotoSansSC-Bold.ttf")))
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, height - 42, width, 42, fill=1, stroke=0)
    c.setFillColorRGB(0.48, 0.47, 0.44)
    c.setFont("NotoSansSC", 6.7)
    c.drawString(36, height - 22, f"付强 · {title}")
    c.drawRightString(width - 36, height - 22, "重要免责声明 · V1.4维护版")
    c.setStrokeColorRGB(0.84, 0.83, 0.80)
    c.setLineWidth(0.3)
    c.line(36, height - 28, width - 36, height - 28)
    c.save()
    packet.seek(0)
    page.merge_page(PdfReader(packet).pages[0])
    return page


def stamp_current_cover(page, title: str):
    """Promote a legacy formal cover into the visible V1.4 front cover."""
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    if "NotoSansSC" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("NotoSansSC", str(FONT_DIR / "NotoSansSC-Regular.ttf")))
        pdfmetrics.registerFont(TTFont("NotoSansSC-Bold", str(FONT_DIR / "NotoSansSC-Bold.ttf")))
    c.setFillColorRGB(1, 1, 1)
    c.rect(18, height - 67, width - 36, 48, fill=1, stroke=0)
    c.setFillColorRGB(0.0, 0.25, 0.60)
    c.rect(18, height - 63, 70, 7, fill=1, stroke=0)
    c.setFont("NotoSansSC-Bold", 15)
    c.drawString(102, height - 57, "V1.4")
    c.setFont("NotoSansSC", 8.5)
    c.drawString(153, height - 56, "2026/07/24 当前维护版")
    c.setFillColorRGB(0.34, 0.34, 0.34)
    c.setFont("NotoSansSC", 6.8)
    c.drawRightString(
        width - 18,
        height - 55,
        "历史正文保留原时点；当前结论、事实与勘误以随后更新模块为准",
    )
    c.setStrokeColorRGB(0.78, 0.82, 0.88)
    c.setLineWidth(0.35)
    c.line(18, height - 68, width - 18, height - 68)
    c.save()
    packet.seek(0)
    page.merge_page(PdfReader(packet).pages[0])
    return page


def promoted_cover_page(base_pdf: Path, cover_index: int, title: str):
    """Extract the legacy formal cover and update only its visible edition/date marks."""
    import fitz

    source = fitz.open(base_pdf)
    cover_doc = fitz.open()
    cover_doc.insert_pdf(source, from_page=cover_index, to_page=cover_index)
    source.close()
    page = cover_doc[0]

    replacements: list[tuple[str, str]] = []
    for old_version in ("V1.3.4", "V0.8.2", "V0.6.0", "V1.1"):
        if page.search_for(old_version):
            replacements.append((old_version, "V1.4"))
            break
    for old_date in ("2026/07/07", "2026/06/14", "2026/06/03", "2026/05/21"):
        if page.search_for(old_date):
            replacements.append((old_date, "2026/07/24"))
            break

    queued: list[tuple[fitz.Rect, str]] = []
    for old, new in replacements:
        for rect in page.search_for(old):
            box = fitz.Rect(rect.x0 - 0.5, rect.y0 - 0.5, rect.x1 + 2.0, rect.y1 + 0.5)
            page.add_redact_annot(box, fill=(1, 1, 1))
            queued.append((box, new))
    if queued:
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
        for box, new in queued:
            page.insert_text(
                (box.x0, box.y1 - 1.2),
                new,
                fontname="helv",
                fontsize=max(6.0, min(9.5, box.height * 0.72)),
                color=(0.0, 0.25, 0.60),
            )

    payload = cover_doc.tobytes(garbage=4, clean=True, deflate=True)
    cover_doc.close()
    return stamp_current_cover(PdfReader(io.BytesIO(payload)).pages[0], title)


def optimize_pdf(path: Path) -> None:
    """Deduplicate appended PDF objects while preserving links and page labels."""
    try:
        import fitz
    except ImportError:
        print(f"[WARN] PyMuPDF unavailable; skipped object deduplication for {path.name}")
        return
    tmp = path.with_suffix(".optimized.tmp.pdf")
    doc = fitz.open(path)
    doc.save(
        tmp,
        garbage=4,
        clean=True,
        deflate=True,
        deflate_images=True,
        deflate_fonts=True,
    )
    doc.close()
    tmp.replace(path)


def build_thick(update_pdf: Path, out: Path) -> int:
    """Place the full disclaimer up front, then join V1.4 and V1.3 revision material."""
    update_reader = PdfReader(str(update_pdf))
    base_reader = PdfReader(str(THICK_BASE_PDF))
    writer = PdfWriter()
    writer.add_page(promoted_cover_page(THICK_BASE_PDF, 0, "2026年AI泡沫研究 · 全景版"))
    # Original page 2 is the full legal/risk disclaimer. Move it directly behind
    # the current cover so it no longer separates the V1.4 update from the V1.3
    # frozen revision record.
    writer.add_page(stamp_disclaimer_header(base_reader.pages[1], "AI周期与泡沫研究 · 全景版"))
    writer.append(update_reader, pages=(1, len(update_reader.pages)), import_outline=False)
    # The cover and disclaimer have moved to the front. Keep original pages
    # 3–310, which contain the revision record and every historical TOC target.
    writer.append(base_reader, pages=(2, len(base_reader.pages)), import_outline=True)
    front_count = len(update_reader.pages) + 1
    for page_index in range(front_count, len(writer.pages)):
        stamp_page(
            writer.pages[page_index],
            "历史冻结正文 · V1.3.4｜动态口径见卷首 V1.4",
        )
    writer.set_page_label(0, front_count - 1, style=PageLabelStyle.DECIMAL, start=1)
    writer.set_page_label(front_count, len(writer.pages) - 1, style=PageLabelStyle.DECIMAL, start=3)
    writer.add_outline_item("V1.4 当前封面", 0)
    writer.add_outline_item("重要免责声明", 1)
    writer.add_outline_item("V1.4·7/24 更新与勘误", 2)
    writer.add_outline_item("V1.3.4 冻结历史正文（原页3–310）", front_count)
    writer.add_metadata({
        "/Title": "2026年AI泡沫研究 · 全景版 V1.4超全景版",
        "/Author": "付强",
        "/Subject": "V1.4 cover, front disclaimer and update body plus frozen historical pages 3-310",
    })
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    optimize_pdf(out)
    pages = len(PdfReader(str(out)).pages)
    print(f"[OK] {out.name}: {pages} pages")
    return pages


def build_maintenance_edition(
    update_pdf: Path,
    base_pdf: Path,
    out: Path,
    title: str,
    cover_index: int,
) -> int:
    """Create a current wrapper without silently rewriting a legacy-layout PDF.

    ``append`` (rather than page-by-page reconstruction) is intentional: it
    preserves named destinations and internal TOC links in the old public
    editions. The two sections use independent printed page-label ranges.
    """
    update_reader = PdfReader(str(update_pdf))
    base_reader = PdfReader(str(base_pdf))
    writer = PdfWriter()
    writer.add_page(promoted_cover_page(base_pdf, cover_index, title))
    writer.append(update_reader, pages=(1, len(update_reader.pages)), import_outline=False)

    # Move (rather than duplicate) the old formal cover. Errata pages that
    # preceded a legacy cover remain at the start of the frozen section.
    if cover_index:
        writer.append(base_reader, pages=(0, cover_index), import_outline=False)
    if cover_index + 1 < len(base_reader.pages):
        writer.append(
            base_reader,
            pages=(cover_index + 1, len(base_reader.pages)),
            import_outline=True,
        )

    front_count = len(update_reader.pages)
    for page_index in range(front_count, len(writer.pages)):
        stamp_page(
            writer.pages[page_index],
            "历史冻结正文｜动态口径见卷首 V1.4",
        )

    writer.set_page_label(0, front_count - 1, style=PageLabelStyle.DECIMAL, start=1)
    if cover_index:
        writer.set_page_label(
            front_count,
            front_count + cover_index - 1,
            style=PageLabelStyle.DECIMAL,
            start=1,
        )
    post_cover_start = front_count + cover_index
    if post_cover_start < len(writer.pages):
        writer.set_page_label(
            post_cover_start,
            len(writer.pages) - 1,
            style=PageLabelStyle.DECIMAL,
            start=cover_index + 2,
        )
    writer.add_outline_item("V1.4 当前封面", 0)
    writer.add_outline_item("V1.4·7/24 更新与勘误", 1)
    writer.add_outline_item(
        f"历史冻结正文（原封面已移至首页，共{len(base_reader.pages) - 1}页）",
        front_count,
    )
    writer.add_metadata(
        {
            "/Title": f"{title} · V1.4维护版",
            "/Author": "付强",
            "/Subject": (
                "Current V1.4 update module plus complete frozen historical layout; "
                "the update module governs all dynamic facts and conclusions"
            ),
        }
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    optimize_pdf(out)
    pages = len(PdfReader(str(out)).pages)
    print(
        f"[OK] {out.name}: {pages} pages "
        f"(promoted cover + {len(update_reader.pages) - 1} current pages + "
        f"{len(base_reader.pages) - 1} frozen pages)"
    )
    return pages


def main() -> None:
    # Save assembled sources for auditability; these are derived build artifacts.
    main_md = assembled_main()
    audit_md = assembled_audit()
    pano_md = assembled_panorama()
    (SRC / "AI周期与泡沫深度研究报告_V1.4合成源.md").write_text(main_md, encoding="utf-8")
    (SRC / "AI周期与泡沫_事实审计表_V1.4合成源.md").write_text(audit_md, encoding="utf-8")
    (SRC / "AI周期与泡沫深度研究报告_全景版_V1.4合成源.md").write_text(pano_md, encoding="utf-8")

    build_markdown_pdf(
        read(MASTER_MD) + "\n\n## 超全景整合说明\n\n"
        "在超全景版中，完整免责声明置于当前封面之后，本模块随后呈现；其后衔接 V1.3.4 "
        "冻结历史正文原第3—310页，并保留原目录和内部链接。卷首当前部分与冻结历史正文独立计页；"
        "动态分数、概率、价格、触发状态与观察日全部以本模块为准。",
        UPDATE_OUT,
        "AI周期与泡沫研究 · V1.4更新模块",
        "全报告统一动态口径 · 用于主报告、审计表、完整全景版与 300+ 页超全景版",
        toc=True,
        extra_cover="本模块不是单页勘误，而是包含结论、触发器对账、八项硬事实、Alphabet官方书面发言、DeepSeek口径勘误、市场快照、证伪条件和更新位置的完整动态正文。",
    )
    build_markdown_pdf(
        main_md, MAIN_OUT, "AI周期与泡沫深度研究报告", "主报告 V1.4 · 投递后研究维护版",
        extra_cover="历史正文保留研究过程，动态口径以卷首更新模块为准。",
    )
    build_markdown_pdf(
        audit_md, AUDIT_OUT, "AI周期与泡沫 · 事实审计表", "V1.4 · 73 项（63 项冻结基表 + 10 项新增）",
        landscape=True, compact=True,
        extra_cover="新增13i–13r；13q审计Alphabet官方书面发言，13r审计DeepSeek V4与昇腾适配边界。日度市场价格单列快照。",
    )
    build_markdown_pdf(
        read(BRIEF_MD), BRIEF_OUT, "AI周期与泡沫研究 · 机构简版", "V1.4 · 10 分钟投委阅读",
        compact=True,
        extra_cover="结论、反方证据与证伪条件同页呈现。",
    )
    build_markdown_pdf(
        pano_md, PANO_OUT, "2026年AI泡沫研究 · 全景版", "V1.4完整重排版 · 全量正文与更新模块一体化",
        compact=True,
        extra_cover="全量历史正文重新排版输出；卷首更新模块统一所有动态口径。",
    )
    build_thick(UPDATE_OUT, THICK_OUT)
    for base_pdf, out, title, cover_index in LEGACY_VARIANTS:
        build_maintenance_edition(UPDATE_OUT, base_pdf, out, title, cover_index)


if __name__ == "__main__":
    main()
