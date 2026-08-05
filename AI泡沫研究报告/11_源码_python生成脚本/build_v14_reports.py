#!/usr/bin/env python3
"""Build the current V1.4 report line without touching frozen submitted files.

Outputs:
  - main report V1.4
  - fact audit V1.4 (63-item frozen base + 25 new items, rolling checked through 2026-08-05)
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
from pypdf.annotations import Link
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
UPDATE_DATE = "2026/08/05"
DATA_DATE = "2026/08/05"
AUDIT_TOTAL = 88
AUDIT_NEW = 25
HISTORY_MARKER = "<!-- HISTORICAL_START -->"

MAIN_OUT = ARCHIVE / "02_主报告V1.4/00_AI周期与泡沫深度研究报告_主报告_V1.4.pdf"
AUDIT_OUT = ARCHIVE / "02_主报告V1.4/01_AI周期与泡沫_事实审计表_V1.4.pdf"
BRIEF_OUT = ARCHIVE / "05_简版与执行摘要/AI周期与泡沫_机构简版_V1.4_内部署名版.pdf"
PANO_OUT = ARCHIVE / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4完整重排版.pdf"
THICK_OUT = ARCHIVE / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4超全景版_300页级.pdf"
UPDATE_OUT = INCR / "2026-08-05_V1.4滚动更新模块.pdf"

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


LEGACY_CHARTS = {
    "section_map_01_profit.png": "链路图_第一部分_利润真实性.png",
    "section_map_02_circular.png": "链路图_第二部分_资本循环网络.png",
    "section_map_03_monetization.png": "链路图_第三部分_AI变现.png",
    "section_map_04_agi.png": "链路图_第四部分_AGI时间表.png",
    "section_map_05_geopolitics.png": "链路图_第五部分_国际格局.png",
    "section_map_06_china.png": "链路图_第六部分_中国投资者.png",
}


def bind_legacy_chart_placeholders(text: str) -> str:
    """Resolve frozen-source chart tokens without rewriting the frozen source."""
    def repl(match: re.Match[str]) -> str:
        token = match.group(1)
        caption = match.group(2).strip()
        actual = LEGACY_CHARTS.get(token)
        if actual is None:
            return match.group(0)
        return f"![{caption}](../13_全景版配图/{actual})"

    return re.sub(
        r"(?m)^\[\[CHART:([^\]]+)\]\]\s*图：([^\n]+)$",
        repl,
        text,
    )


def normalize_historical_v14(text: str) -> str:
    """Clarify historical language in current V1.4 derivatives without changing frozen inputs."""
    text = text.replace("【V1.2 起最新口径：", "【V1.2 当时口径：")
    text = text.replace("最新主概率框架", "V1.2当时主概率框架")
    text = text.replace("主概率请以 V1.2 最新口径为准", "该历史段落按V1.2当时口径阅读；当前以卷首V1.4为准")
    text = text.replace("主概率请以V1.2最新口径为准", "该历史段落按V1.2当时口径阅读；当前以卷首V1.4为准")
    text = text.replace("42% A 软着陆权重", "42% A 渐进幻灭权重")
    text = text.replace("**A. 渐进幻灭（软着陆）**", "**A. 渐进幻灭**")
    text = text.replace(
        "| Amazon | 835亿 | **1347亿** | **2000亿** | **97%** |",
        "| Amazon | 835亿 | **1347亿** | **2000亿（该历史时点前瞻）** | **97%** |",
    )
    text = text.replace(
        "**含义**：Amazon 未来 **三个连续季度** 50% 以上净利润将来自 Anthropic 重估这一非经营、非现金收益。",
        "**该历史版本预测**：Amazon未来三个连续季度50%以上净利润可能来自Anthropic重估这一非经营、非现金收益。"
        "**截至2026Q2的结算**：当季非经营收益为$53.415B，其中私营股权可观察价格上调约$50.5B；"
        "这只验证当季利润质量拆分，不能确认三个连续季度。",
    )
    text = text.replace(
        "| **破而重伤** | **Amazon** | -60% 至 -70% | AWS 增长依赖 Anthropic 重估（§1.2）；TTM FCF 已跌 95%；Capex 吞噬现金流。若 Anthropic IPO 折价，会反向计提 |",
        "| **破而重伤** | **Amazon** | -60% 至 -70% | AWS收入增长属于经营兑现，与Anthropic非经营重估分栏；截至2026Q1的历史快照显示TTM FCF显著下滑，当前V1.4覆盖值为-$7.604B。若Anthropic估值下修，合并利润可能反向计提 |",
    )
    text = text.replace("## 结语：六个核心判断", "## 历史版本结语：六个当时核心判断")
    text = text.replace("1. **当前AI巨头利润含有显著估值水分**", "1. **该历史版本观察时点的AI巨头利润含有显著估值水分**")
    return text


def historical_main_body(text: str) -> str:
    """Drop the stale current-version preamble but retain the version history and body."""
    text = normalize_historical_v14(bind_legacy_chart_placeholders(text))
    parts = re.split(r"\n## 版本变更说明\s*\n", text, maxsplit=1)
    if len(parts) == 2:
        return "## 历史版本沿革（V0.1—V1.3.4）\n\n" + parts[1]
    return "## V1.3.4 历史正文基线\n\n" + without_first_h1(text)


def rename_historical_changelog(text: str) -> str:
    """Clarify that the preserved table covers only the frozen pre-V1.4 history."""
    return re.sub(
        r"(?m)^## 版本变更说明\s*$",
        "## 历史版本沿革（V0.1—V1.3.4）",
        text,
        count=1,
    )


def assembled_main() -> str:
    return (
        "# AI周期与泡沫深度研究报告\n\n"
        + read(MASTER_MD)
        + f"\n\n---\n\n{HISTORY_MARKER}\n\n"
        + "> **历史正文阅读提示**：以下深度正文保留当时版本的日期、分数和概率，用于展示研究推演与证据链。"
          "凡属动态数值、当前结论与触发器状态，均以本报告卷首 V1.4 更新模块为准。\n\n"
        + historical_main_body(read(MAIN_MD))
    )


def assembled_audit() -> str:
    base = without_first_h1(read(AUDIT_BASE_MD))
    incr = without_first_h1(read(AUDIT_INCR_MD))
    return (
        f"# AI周期与泡沫 · 事实审计表 V1.4（{AUDIT_TOTAL} 项）\n\n"
        + incr
        + f"\n\n---\n\n{HISTORY_MARKER}\n\n"
        + "## V1.3.4a 冻结基表（63 项）\n\n"
        + "> 下列 63 项保持 V1.3.4a 原文，作为可回溯基表；其历史版本段落中的项数、分数与概率不是 V1.4 当前口径。\n\n"
        + base
    )


def assembled_panorama() -> str:
    base = normalize_historical_v14(rename_historical_changelog(read(PANO_BASE_MD)))
    base = without_first_h1(base)
    return (
        "# 2026年AI泡沫研究 · 全景版 V1.4完整重排版\n\n"
        + read(MASTER_MD)
        + f"\n\n---\n\n{HISTORY_MARKER}\n\n"
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
  @top-left {{ content:"大队长 · {title}"; font-family:NotoSansSC; font-size:7.2pt; color:#77756F; }}
  @top-right {{ content:"V1.4 · 滚动核验至 {DATA_DATE}"; font-family:NotoSansSC; font-size:7.2pt; color:#77756F; }}
  @bottom-left {{ content:"个人研究 · 基于公开信息 · 不构成投资建议"; font-family:NotoSansSC; font-size:7pt; color:#AAA8A2; }}
  @bottom-right {{ content:"第 " counter(page) " 页 / 共 " counter(pages) " 页"; font-family:NotoSansSC; font-size:7.2pt; color:#77756F; }}
}}
@page cover {{ margin:0; @top-left {{content:none}} @top-right {{content:none}} @bottom-left {{content:none}} @bottom-right {{content:none}} }}
@page historical {{ size:{size}; margin:{margin};
  @top-left {{ content:"历史冻结正文 · 仅供研究过程回溯"; font-family:NotoSansSC; font-size:7.2pt; color:#8A765E; }}
  @top-right {{ content:"当前口径见卷首 V1.4 · {DATA_DATE}"; font-family:NotoSansSC; font-size:7.2pt; color:#8A765E; }}
  @bottom-left {{ content:"历史数字不得冒充当前结论"; font-family:NotoSansSC; font-size:7pt; color:#AAA8A2; }}
  @bottom-right {{ content:"第 " counter(page) " 页 / 共 " counter(pages) " 页"; font-family:NotoSansSC; font-size:7.2pt; color:#77756F; }}
}}
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
.historical {{ page:historical; }}
.history-divider {{ page:historical; page-break-before:always; background:#F7F3ED; border:1px solid #D9C8B3; padding:1.2cm; margin-bottom:1cm; color:#6D5138; }}
.history-divider h1 {{ color:#6D5138; border-bottom-color:#B89B7A; }}
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
<div class="rule"></div><div class="brand">大队长 · 独立研究 · 研究维护版</div>
<div class="title">{title}</div><div class="sub">{subtitle}</div>
<div class="kpi"><b>综合崩盘指数</b>　77 / 100<br/>
<b>四情景</b>　A44 / B22 / C10 / D24（软着陆以外合计 76%）<br/>
<b>触发器</b>　严格执行 1/3 · 广义早期预警 2/3<br/>
<b>数据截止</b>　研究资料至2026-08-05 09:30；E判断A股结算至7/24，信用与波动率至8/3，SPCX收盘至8/4</div>
<div class="rev"><b>当前判断</b>：需求仍然满载，融资与估值侧裂缝扩大；严格执行触发仍为1/3，尚未达到系统性减仓或对冲的全面执行信号。<br/>
<b>阅读规则</b>：卷首V1.4为当前口径；后接历史冻结正文，仅用于展示研究过程。{extra}</div>
<div class="foot">V1.4 · 2026-08-05滚动核验｜历史发布材料与前瞻判断原件保持冻结｜不构成投资建议</div>
</section>"""


def add_ids_and_toc(html_body: str, *, prefix: str = "sec", include_toc: bool = True) -> tuple[str, str]:
    heads: list[tuple[int, str, str]] = []

    def repl(match: re.Match[str]) -> str:
        level = int(match.group(1))
        attrs = match.group(2)
        text = match.group(3)
        hid = f"{prefix}-{len(heads):04d}"
        plain = re.sub(r"<[^>]+>", "", text).strip()
        if level <= 3 and plain:
            heads.append((level, plain, hid))
        return f'<h{level} id="{hid}"{attrs}>{text}</h{level}>'

    tagged = re.sub(r"<h([1-6])([^>]*)>(.*?)</h\1>", repl, html_body, flags=re.S)
    if not include_toc:
        return tagged, ""
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
    extensions = ["tables", "fenced_code", "footnotes", "attr_list"]
    if HISTORY_MARKER in md_text:
        current_md, historical_md = md_text.split(HISTORY_MARKER, 1)
        current_html = markdown.markdown(current_md, extensions=extensions)
        historical_html = markdown.markdown(historical_md, extensions=extensions)
        current_html, toc_html = add_ids_and_toc(current_html, prefix="current")
        historical_html, _ = add_ids_and_toc(historical_html, prefix="history", include_toc=False)
        history_link = (
            '<div class="toc-row l2"><a href="#historical-start">'
            '历史冻结正文（附录，仅供回溯）</a></div>'
        )
        toc_html = toc_html.replace("</section>", history_link + "</section>")
        html_body = (
            current_html
            + '<section class="historical"><div id="historical-start" class="history-divider">'
            + '<h1>历史冻结正文</h1><p>本附录保留当时的数字、概率与文字，'
              '用于审计研究进化；当前分数、情景、触发器和市场快照一律以卷首V1.4为准。</p></div>'
            + historical_html
            + "</section>"
        )
    else:
        html_body = markdown.markdown(md_text, extensions=extensions)
        html_body, toc_html = add_ids_and_toc(html_body, prefix="current")
    full = (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="author" content="大队长">'
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
    c.drawString(36, height - 22, f"大队长 · {title}")
    c.drawRightString(width - 36, height - 22, "重要免责声明 · V1.4维护版")
    c.setStrokeColorRGB(0.84, 0.83, 0.80)
    c.setLineWidth(0.3)
    c.line(36, height - 28, width - 36, height - 28)
    c.save()
    packet.seek(0)
    page.merge_page(PdfReader(packet).pages[0])
    return page


def clean_current_cover_page(base_pdf: Path, cover_index: int, title: str):
    """Build a clean V1.4 cover instead of patching a crowded legacy cover."""
    source = PdfReader(str(base_pdf))
    width = float(source.pages[cover_index].mediabox.width)
    height = float(source.pages[cover_index].mediabox.height)
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    if "NotoSansSC" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("NotoSansSC", str(FONT_DIR / "NotoSansSC-Regular.ttf")))
        pdfmetrics.registerFont(TTFont("NotoSansSC-Bold", str(FONT_DIR / "NotoSansSC-Bold.ttf")))

    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    margin_x = width * 0.105
    content_w = width - 2 * margin_x

    c.setFillColorRGB(0.0, 0.25, 0.60)
    c.rect(margin_x, height - 82, min(118, content_w * 0.28), 8, fill=1, stroke=0)
    c.setFillColorRGB(0.48, 0.47, 0.44)
    c.setFont("NotoSansSC", 8.3)
    c.drawString(margin_x, height - 112, "大队长 · 独立研究 · 研究维护版")

    title_size = 24
    title_y = height - 205
    title_lines = [title]
    if pdfmetrics.stringWidth(title, "NotoSansSC-Bold", title_size) > content_w and "·" in title:
        left, right = title.split("·", 1)
        title_lines = [left.strip(), f"· {right.strip()}"]
    c.setFillColorRGB(0.0, 0.14, 0.32)
    c.setFont("NotoSansSC-Bold", title_size)
    for line in title_lines:
        c.drawString(margin_x, title_y, line)
        title_y -= 34

    c.setFillColorRGB(0.34, 0.33, 0.30)
    c.setFont("NotoSansSC", 10.3)
    c.drawString(margin_x, title_y - 10, "V1.4 · 当前维护版")

    kpi_top = title_y - 75
    c.setStrokeColorRGB(0.0, 0.25, 0.60)
    c.setLineWidth(3)
    c.line(margin_x, kpi_top + 8, margin_x, kpi_top - 76)
    kpis = (
        "综合崩盘指数　77 / 100",
        "四情景　A44 / B22 / C10 / D24（软着陆以外合计76%）",
        "触发器　严格执行1/3 · 广义早期预警2/3",
    )
    c.setFillColorRGB(0.18, 0.17, 0.15)
    c.setFont("NotoSansSC-Bold", 9.2)
    for idx, line in enumerate(kpis):
        c.drawString(margin_x + 16, kpi_top - idx * 27, line)

    box_y = kpi_top - 185
    c.setFillColorRGB(0.96, 0.97, 0.985)
    c.setStrokeColorRGB(0.82, 0.87, 0.93)
    c.setLineWidth(0.6)
    c.roundRect(margin_x, box_y, content_w, 92, 3, fill=1, stroke=1)
    c.setFillColorRGB(0.34, 0.26, 0.28)
    c.setFont("NotoSansSC", 8.5)
    cover_lines = (
        "当前判断：需求仍然满载，融资与估值侧裂缝扩大；",
        "严格执行触发仍为1/3，尚未达到系统性减仓或对冲的全面执行信号。",
        "阅读规则：卷首V1.4为当前口径；后接历史冻结正文，仅用于展示研究过程。",
    )
    for idx, line in enumerate(cover_lines):
        c.drawString(margin_x + 16, box_y + 64 - idx * 23, line)

    c.setFillColorRGB(0.43, 0.42, 0.39)
    c.setFont("NotoSansSC", 8.2)
    c.drawString(margin_x, box_y - 38, "版本　V1.4 · 2026/08/05滚动核验")
    c.drawString(
        margin_x,
        box_y - 61,
        "数据　研究资料至2026/08/05 09:30 · E判断A股结算至7/24 · 信用/波动率至8/3 · SPCX至8/4",
    )

    c.setStrokeColorRGB(0.84, 0.83, 0.80)
    c.setLineWidth(0.4)
    c.line(margin_x, 66, width - margin_x, 66)
    c.setFillColorRGB(0.60, 0.59, 0.56)
    c.setFont("NotoSansSC", 7.5)
    c.drawString(margin_x, 48, "大队长 · AI周期与泡沫研究")
    c.drawRightString(width - margin_x, 48, "基于公开信息 · 不构成投资建议")
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


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


def find_pdf_page(reader: PdfReader, *tokens: str, start: int = 0) -> int:
    """Return the first source-page index containing every requested token."""
    for page_index in range(start, len(reader.pages)):
        page_text = reader.pages[page_index].extract_text() or ""
        if all(token in page_text for token in tokens):
            return page_index
    raise ValueError(f"Could not locate PDF page containing: {tokens}")


def build_super_toc_page(
    width: float,
    height: float,
    total_pages: int,
    current_rows,
    history_rows,
):
    """Build the only active TOC for the 300+ page super-panorama.

    The source update PDF numbers itself independently, so reusing its TOC in
    the merged edition makes the displayed page numbers one page too small.
    This deterministic page links both the current V1.4 module and the frozen
    historical archive using the merged edition's actual page numbers.
    """
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    if "NotoSansSC" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("NotoSansSC", str(FONT_DIR / "NotoSansSC-Regular.ttf")))
        pdfmetrics.registerFont(TTFont("NotoSansSC-Bold", str(FONT_DIR / "NotoSansSC-Bold.ttf")))

    navy = (0.0, 0.14, 0.32)
    blue = (0.0, 0.25, 0.60)
    body = (0.16, 0.15, 0.13)
    muted = (0.47, 0.46, 0.43)
    rule = (0.83, 0.83, 0.81)
    margin = 52.8

    c.setFillColorRGB(*muted)
    c.setFont("NotoSansSC", 7.2)
    c.drawString(margin, height - 25, "大队长 · AI周期与泡沫研究 · V1.4超全景版")
    c.drawRightString(width - margin, height - 25, f"V1.4 · 滚动核验至 {DATA_DATE}")

    c.setFillColorRGB(*navy)
    c.setFont("NotoSansSC-Bold", 25)
    c.drawString(margin, height - 78, "总目录")
    c.setFillColorRGB(*body)
    c.setFont("NotoSansSC", 9.2)
    c.drawString(
        margin,
        height - 108,
        f"本页是超全景版唯一当前导航；页码为{total_pages}页合并版实际页码，条目可点击跳转。",
    )

    link_specs: list[tuple[tuple[float, float, float, float], int]] = []

    def section_label(text: str, y: float) -> float:
        c.setFillColorRGB(*blue)
        c.rect(margin, y - 2, 4, 13, fill=1, stroke=0)
        c.setFont("NotoSansSC-Bold", 10.2)
        c.drawString(margin + 11, y, text)
        return y - 21

    def draw_rows(rows, y: float) -> float:
        for label, printed_page, target_index, strong in rows:
            indent = 0 if strong else 10
            c.setFillColorRGB(*body)
            c.setFont("NotoSansSC-Bold" if strong else "NotoSansSC", 8.8)
            c.drawString(margin + indent, y, label)
            c.setFillColorRGB(*blue)
            c.setFont("NotoSansSC-Bold" if strong else "NotoSansSC", 8.8)
            c.drawRightString(width - margin, y, str(printed_page))
            c.setStrokeColorRGB(*rule)
            c.setLineWidth(0.28)
            c.line(margin, y - 5, width - margin, y - 5)
            link_specs.append(((margin, y - 6, width - margin, y + 10), target_index))
            y -= 18
        return y

    y = section_label("A｜当前有效口径", height - 142)
    y = draw_rows(current_rows, y)
    y -= 3
    y = section_label("B｜历史冻结研究（仅供回溯）", y)
    draw_rows(history_rows, y)

    c.setStrokeColorRGB(*rule)
    c.setLineWidth(0.4)
    c.line(margin, 66, width - margin, 66)
    c.setFillColorRGB(0.60, 0.59, 0.56)
    c.setFont("NotoSansSC", 7.2)
    c.drawString(margin, 48, "个人研究 · 基于公开信息 · 不构成投资建议")
    c.drawRightString(width - margin, 48, f"第 3 页 / 共 {total_pages} 页")
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0], link_specs


def history_navigation_overlay(width: float, height: float, kind: str):
    """Return a searchable ReportLab overlay for a relabeled history page."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    if "NotoSansSC" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("NotoSansSC", str(FONT_DIR / "NotoSansSC-Regular.ttf")))
        pdfmetrics.registerFont(TTFont("NotoSansSC-Bold", str(FONT_DIR / "NotoSansSC-Bold.ttf")))
    teal = (0.0, 0.43, 0.45)
    grey = (0.40, 0.40, 0.38)
    if kind == "structure":
        c.setFillColorRGB(*teal)
        c.setFont("NotoSansSC-Bold", 18)
        c.drawString(56.7, height - 138.5, "历史版本结构说明（V1.3.4修订版）")
        c.setFillColorRGB(*grey)
        c.setFont("NotoSansSC", 8.8)
        c.drawString(56.7, height - 152.0, "本页仅说明冻结版本结构与勘误位置；当前总目录见卷首第3页。")
        c.setFillColorRGB(0.12, 0.12, 0.11)
        c.setFont("NotoSansSC-Bold", 8.8)
        c.drawString(62.9, height - 259.0, "版本结构说明【新增 · 本页】")
    elif kind == "archive-index":
        c.setFillColorRGB(*teal)
        c.setFont("NotoSansSC-Bold", 21)
        c.drawString(57.0, height - 106.0, "历史原版索引（留档）")
        c.setStrokeColorRGB(*teal)
        c.setLineWidth(1.5)
        c.line(57, height - 115, 538, height - 115)
        c.setFillColorRGB(*grey)
        c.setFont("NotoSansSC", 9.0)
        c.drawString(57.0, height - 133.0, "保留原版详细跳转；不作为第二套当前目录。当前总目录见第3页。")
    else:
        raise ValueError(kind)
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def relabel_super_history_navigation(path: Path, history_start: int) -> None:
    """Demote legacy TOC furniture to searchable archive labels without breaking links."""
    try:
        import fitz
    except ImportError:
        print(f"[WARN] PyMuPDF unavailable; skipped historical navigation labels for {path.name}")
        return

    redacted_tmp = path.with_suffix(".navigation.redacted.tmp.pdf")
    final_tmp = path.with_suffix(".navigation.final.tmp.pdf")
    doc = fitz.open(path)

    structure_index = history_start + 1
    archive_index_index = history_start + 3
    structure = doc[structure_index]
    structure.add_redact_annot(fitz.Rect(49, 112, 548, 158), fill=(1, 1, 1))
    structure.add_redact_annot(fitz.Rect(60, 247, 310, 263), fill=(1, 1, 1))
    structure.apply_redactions(images=0, graphics=0)

    archive_index = doc[archive_index_index]
    archive_index.add_redact_annot(fitz.Rect(50, 74, 548, 140), fill=(1, 1, 1))
    archive_index.apply_redactions(images=0, graphics=0)

    doc.save(
        redacted_tmp,
        garbage=4,
        clean=False,
        deflate=True,
        deflate_images=True,
        deflate_fonts=True,
    )
    doc.close()

    reader = PdfReader(str(redacted_tmp))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    for page_index, kind in (
        (structure_index, "structure"),
        (archive_index_index, "archive-index"),
    ):
        page = writer.pages[page_index]
        page.merge_page(
            history_navigation_overlay(
                float(page.mediabox.width),
                float(page.mediabox.height),
                kind,
            )
        )
    with final_tmp.open("wb") as fh:
        writer.write(fh)
    redacted_tmp.unlink(missing_ok=True)
    final_tmp.replace(path)


def build_thick(update_pdf: Path, out: Path) -> int:
    """Build one total TOC, then join current V1.4 and frozen V1.3 material."""
    update_reader = PdfReader(str(update_pdf))
    base_reader = PdfReader(str(THICK_BASE_PDF))
    writer = PdfWriter()
    writer.add_page(clean_current_cover_page(THICK_BASE_PDF, 0, "2026年AI泡沫研究 · 全景版"))
    # Original page 2 is the full legal/risk disclaimer. Move it directly behind
    # the current cover so it no longer separates the V1.4 update from the V1.3
    # frozen revision record.
    writer.add_page(stamp_disclaimer_header(base_reader.pages[1], "AI周期与泡沫研究 · 全景版"))
    expected_pages = 3 + (len(update_reader.pages) - 2) + (len(base_reader.pages) - 2)
    history_start = len(update_reader.pages) + 1

    def update_row(label: str, *tokens: str, strong: bool = False):
        source_index = find_pdf_page(update_reader, *tokens, start=2)
        target_index = source_index + 1
        return (label, target_index + 1, target_index, strong)

    current_rows = (
        ("重要免责声明", 2, 1, True),
        update_row("V1.4 当前更新与勘误｜滚动核验至2026-08-05", "V1.4 更新模块", strong=True),
        update_row("0. V1.4滚动更新日志（7/20—8/5）", "V1.4滚动更新日志"),
        update_row("1. V1.4当前结论", "V1.4 当前结论"),
        update_row("2. 触发器治理：V1.4重新基准化", "触发器治理"),
        update_row("3. 本轮新增二十五项审计事实", "本轮新增二十五项审计事实"),
        update_row("4. 市场与事件快照", "市场与事件快照"),
        update_row("5. 证伪条件与下一观察窗口", "证伪条件与下一观察窗口"),
        update_row("6. 8/5复审与勘误结论", "8/5复审与勘误结论"),
        update_row("7. 本版具体更新位置", "本版具体更新位置"),
        update_row("8. 主要来源", "主要来源"),
        update_row("超全景整合说明", "超全景整合说明", strong=True),
    )
    history_rows = (
        ("V1.3.4修订记录", history_start + 1, history_start, False),
        ("历史版本结构说明", history_start + 2, history_start + 1, False),
        ("V1.3.4a勘误与增补", history_start + 3, history_start + 2, False),
        ("历史原版索引（留档）", history_start + 4, history_start + 3, True),
    )
    total_toc, total_toc_links = build_super_toc_page(
        float(update_reader.pages[1].mediabox.width),
        float(update_reader.pages[1].mediabox.height),
        expected_pages,
        current_rows,
        history_rows,
    )
    writer.add_page(total_toc)
    # Replace the standalone update module's TOC with the merged edition's total
    # TOC. Current content begins at source page 3 and historical page positions
    # stay unchanged.
    writer.append(update_reader, pages=(2, len(update_reader.pages)), import_outline=False)
    # The cover and disclaimer have moved to the front. Keep original pages
    # 3–310, which contain the revision record and every historical TOC target.
    writer.append(base_reader, pages=(2, len(base_reader.pages)), import_outline=True)
    front_count = len(update_reader.pages) + 1
    for page_index in range(front_count, len(writer.pages)):
        stamp_page(
            writer.pages[page_index],
            "历史冻结正文 · V1.3.4｜动态口径见卷首 V1.4",
        )
    for rect, target_index in total_toc_links:
        writer.add_annotation(
            page_number=2,
            annotation=Link(rect=rect, target_page_index=target_index),
        )
    writer.set_page_label(0, front_count - 1, style=PageLabelStyle.DECIMAL, start=1)
    writer.set_page_label(front_count, len(writer.pages) - 1, style=PageLabelStyle.DECIMAL, start=3)
    writer.add_outline_item("V1.4 当前封面", 0)
    writer.add_outline_item("重要免责声明", 1)
    writer.add_outline_item("总目录", 2)
    writer.add_outline_item("V1.4·8/5 更新与勘误", 3)
    writer.add_outline_item("V1.3.4 冻结历史正文（原页3–310）", front_count)
    writer.add_metadata({
        "/Title": "2026年AI泡沫研究 · 全景版 V1.4超全景版",
        "/Author": "大队长",
        "/Subject": "V1.4 cover, front disclaimer and update body plus frozen historical pages 3-310",
    })
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        writer.write(fh)
    optimize_pdf(out)
    relabel_super_history_navigation(out, history_start)
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
    writer.add_page(clean_current_cover_page(base_pdf, cover_index, title))
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
    writer.add_outline_item("V1.4·8/5 更新与勘误", 1)
    writer.add_outline_item(
        f"历史冻结正文（原封面已移至首页，共{len(base_reader.pages) - 1}页）",
        front_count,
    )
    writer.add_metadata(
        {
            "/Title": f"{title} · V1.4维护版",
            "/Author": "大队长",
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
        f"(clean V1.4 cover + {len(update_reader.pages) - 1} current pages + "
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
        extra_cover="本模块包含免责声明、当前结论、版本化Trigger ID、二十五项审计事实、市场快照、证伪条件、图表和更新位置。",
    )
    build_markdown_pdf(
        main_md, MAIN_OUT, "AI周期与泡沫深度研究报告", "主报告 V1.4 · 研究维护版",
        extra_cover="历史正文保留研究过程，动态口径以卷首更新模块为准。",
    )
    build_markdown_pdf(
        audit_md, AUDIT_OUT, "AI周期与泡沫 · 事实审计表", "V1.4 · 88 项（63 项冻结基表 + 25 项新增）",
        landscape=True, compact=True,
        extra_cover="新增13i–13ag；13z–13ag审计Amazon、Microsoft、Meta、Apple和SpaceX最新财报与监管文件。",
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
