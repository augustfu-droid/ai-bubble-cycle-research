#!/usr/bin/env python3
"""Build the V2.0 main reports on the frozen V1.9 main-report chapters."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
from urllib.parse import unquote

import fitz
import markdown

import build_v19_current as zh_renderer
import build_v19_english as en_renderer


REPORT = Path(__file__).resolve().parents[1]
REPO = REPORT.parent
SRC = REPORT / "10_源码_markdown/V2.0_20261121"
OUT = REPORT / "V2.0_配套发布_20261121"
VERSION = "V2.0"
DATE = "2026-11-21"
BASE_CUTOFF = "2026-10-31"
BASES = {
    "zh": REPORT / "V1.9现行正文版/01_主报告.md",
    "en": REPORT / "V1.9_English_Full_Report/AI_Cycles_and_Bubble_Full_Report_EN_2026-10-31.md",
}
STEMS = {
    "zh": "AI周期与泡沫研究_主报告_V2.0_20261121",
    "en": "AI_Cycles_and_Bubble_Main_Report_EN_V2.0_2026-11-21",
}
TITLES = {
    "zh": "AI 周期与泡沫深度研究报告",
    "en": "AI Cycles and the Bubble: Main Research Report",
}
CHAPTER_PATTERNS = {
    "zh": r"^## 第([一二三四五六七八九十]+)章[：: ]",
    "en": r"^## Chapter (\d+):",
}
CHINESE_NUMBERS = "一 二 三 四 五 六 七 八 九 十 十一 十二 十三".split()
CHAPTER_COUNT = 13
FULL_CHAPTER_UPDATES = {9, 12, 13}
UPDATED_CHAPTERS = {1, 2, 3, 6, 8, 10, 11} | FULL_CHAPTER_UPDATES
ARCHIVED_SECTIONS = {"1.2.4", "1.2.11", "4.4", "4.16"}
LOCAL_MARKET_CASES = re.compile(
    r"中际旭创|新易盛|天孚通信|江波龙|兆易创新|澜起科技|中文在线|兑吧|快手|"
    r"\b(?:InnoLight|Eoptolink|Longsys|COL Group|Dui Ba|Duiba|Kuaishou|TFC Optical)\b|"
    r"\b\d{4,6}\.(?:HK|SZ|SH)\b|cninfo\.com\.cn|stockid=\d{6}|"
    r"A股|港股通|QDII|China A[- ]shares|Cross-boundary Wealth|Stock Connect",
    re.I,
)
LINKS = re.compile(r"!?\[[^\]\n]*\]\(([^)\s]+)\)")
IMAGE_LINKS = re.compile(r"!\[[^\]\n]*\]\((assets/[^)\s]+)\)")
MARKDOWN_EXTENSIONS = ["tables", "fenced_code", "footnotes", "attr_list", "sane_lists"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def baseline_chapters(lang):
    text = BASES[lang].read_text(encoding="utf-8")
    body = text.split("<!-- BODY_START -->", 1)[1].split("<!-- REFERENCES_START -->", 1)[0]
    headings = list(re.finditer(r"^## .+$", body, re.M))
    chapters = {}
    for i, heading in enumerate(headings):
        match = re.match(CHAPTER_PATTERNS[lang], heading[0])
        if match is None:
            continue
        number = CHINESE_NUMBERS.index(match[1]) + 1 if lang == "zh" else int(match[1])
        if number <= 11:
            end = headings[i + 1].start() if i + 1 < len(headings) else len(body)
            chapters[number] = body[heading.start():end].strip()
    if list(chapters) != list(range(1, 12)):
        raise ValueError(f"{lang}: V1.9 main-report chapters 1-11 are required")
    return chapters


def retire_legacy_cases(chapter):
    """Keep research mechanisms while directing dated local-market cases to V1.9."""
    headings = list(re.finditer(r"^(#{3,6}) (.+)$", chapter, re.M))
    removed = []
    for i, heading in enumerate(headings):
        section = heading[2].split()[0]
        if section in ARCHIVED_SECTIONS:
            end = next((later.start() for later in headings[i + 1:]
                        if len(later[1]) <= len(heading[1])), len(chapter))
            removed.append((heading.start(), end))
    for start, end in reversed(removed):
        chapter = chapter[:start] + chapter[end:]
    blocks = []
    for block in chapter.split("\n\n"):
        if LOCAL_MARKET_CASES.search(block) is None:
            blocks.append(block)
        elif block.startswith("|"):
            lines = [line for line in block.splitlines() if LOCAL_MARKET_CASES.search(line) is None]
            if len(lines) > 2:
                blocks.append("\n".join(lines))
    result = "\n\n".join(blocks)
    # Keep parent headings even if they lead straight into child headings.
    remaining = list(re.finditer(r"^(#{3,6}) .+$", result, re.M))
    empty = [(a.start(), b.start()) for a, b in zip(remaining, remaining[1:])
             if len(b[1]) <= len(a[1]) and not result[a.end():b.start()].strip()]
    for start, end in reversed(empty):
        result = result[:start] + result[end:]
    return result.strip()


def updates(lang):
    text = (SRC / f"updates_{lang}.md").read_text(encoding="utf-8-sig")
    parts = re.split(r"^## (\d+)\s*$", text, flags=re.M)
    result = {int(parts[i]): parts[i + 1].strip() for i in range(1, len(parts), 2)}
    if set(result) != UPDATED_CHAPTERS or len(parts) != 1 + 2 * len(result):
        raise ValueError(f"{lang}: missing or repeated update containers")
    for n, content in result.items():
        if n in FULL_CHAPTER_UPDATES:
            heading = re.match(CHAPTER_PATTERNS[lang], content)
            if heading is None or len(re.findall(r"^## ", content, flags=re.M)) != 1:
                raise ValueError(f"{lang}: chapter {n} requires one chapter heading")
        elif not content.startswith("### ") or re.search(r"^#{1,2} ", content, flags=re.M):
            raise ValueError(f"{lang}: chapter {n} updates require subsection headings")
    return result


def compose(lang):
    old = baseline_chapters(lang)
    new = updates(lang)
    edits = json.loads((SRC / "baseline_edits.json").read_text(encoding="utf-8"))[lang]
    for chapter, before, after in edits:
        if old[chapter].count(before) != 1:
            raise ValueError(f"{lang}: revision location in chapter {chapter}: {before[:60]}")
        old[chapter] = old[chapter].replace(before, after, 1)
    chapters = []
    for n in range(1, CHAPTER_COUNT + 1):
        if n in FULL_CHAPTER_UPDATES:
            chapters.append(new[n])
            continue
        chapter = retire_legacy_cases(old[n])
        if n in new:
            heading, content = chapter.split("\n", 1)
            chapter = f"{heading}\n\n{new[n]}\n\n{content.strip()}"
        chapters.append(chapter)
    body = "\n\n".join(chapters)
    headings = re.findall(CHAPTER_PATTERNS[lang], body, re.M)
    expected = CHINESE_NUMBERS[:CHAPTER_COUNT] if lang == "zh" else [str(n) for n in range(1, CHAPTER_COUNT + 1)]
    if headings != expected:
        raise ValueError(f"{lang}: unexpected chapter order")
    bibliography = zh_renderer.bibliography(body) if lang == "zh" else en_renderer.bibliography(body)
    return body + bibliography


def edition_note(lang):
    if lang == "zh":
        return (
            "## 版本与资料日期\n\n"
            "V2.0 直接采用 2026 年 10 月 31 日的 V1.9 主报告作为正文基础。"
            "基础研究的财期和原始证据日期保留。增量截至北京时间 2026 年 11 月 21 日，"
            "本周市场观察截至美东 11 月 20 日常规收盘。"
            "带日期的章节内容记录了本轮新查证的事实、既有证据的复用和作者算例。\n\n"
            "第九章为供电与验收，第十二章为五年资产回收，第十三章写区域市场与现金传导。"
            "第十三章沿用 V1.9 原区域章节的分析框架，并使用北美、欧洲、韩国和日本的公开案例。英文选用 V1.9 英文全文中与原中文主报告对应的章节，"
            "两版均编为十三章。V1.9.1 与 V1.9.2 的后续观点及登记时点见第十一章。\n\n"
            "[V1.9 主报告存档](../V1.9现行正文版/01_主报告.md)\n"
        )
    return (
        "## Edition and evidence dates\n\n"
        "V2.0 builds directly on the October 31, 2026 V1.9 main report. The underlying research retains its "
        "original periods and evidence dates. The additions run through November 21, 2026 in Beijing. "
        "This week's market observations end at the November 20 regular U.S. close. Dated updates identify "
        "new checks, inherited evidence and illustrative calculations.\n\n"
        "Chapter 9 follows power delivery and service acceptance. Chapter 12 covers five-year asset recovery. "
        "Chapter 13 applies V1.9's regional framework to public cases in North America, Europe, South Korea and Japan. The English edition uses "
        "the chapters of the V1.9 English full report corresponding to the Chinese main report. Both editions "
        "now have thirteen chapters. Chapter 11 identifies the distinct dates of the V1.9.1 and V1.9.2 records.\n\n"
        "[V1.9 English archive](../V1.9_English_Full_Report/AI_Cycles_and_Bubble_Full_Report_EN_2026-10-31.md)\n"
    )


def footer(lang):
    if lang == "zh":
        return (
            "## 说明\n\n"
            "本报告为非工作时间写作的个人研究笔记。资料均来自公网公开来源。"
            "文稿与任何金融机构、任职单位无关。新研究以美国市场与公开的算力产业信息为范围，"
            "有关中国境内与香港证券或基金的历史案例见原版本。"
            "本报告不构成投资建议，读者独立判断并自行承担风险。\n"
        )
    return (
        "## Disclosure\n\n"
        "This is personal research prepared outside working hours, using publicly available sources. "
        "It represents no employer or financial institution. The new research covers U.S. market observations "
        "and public compute-industry information. The original edition archives historical regional securities "
        "cases. This report does not provide investment advice. Readers make their own judgments and assume their own risk.\n"
    )


def copy_assets(documents):
    copied = {}
    for lang, markdown_text in documents.items():
        for relative in set(IMAGE_LINKS.findall(markdown_text)):
            original = BASES[lang].parent / unquote(relative)
            target = OUT / unquote(relative)
            if original.suffix.lower() != ".svg" or not original.is_file():
                raise FileNotFoundError(original)
            content = sha256(original)
            if relative in copied and content != copied[relative]:
                raise ValueError(f"Language editions reference different contents at {relative}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original, target)
            copied[relative] = content
    return copied


def relative_css(lang):
    css = zh_renderer.css(TITLES[lang]) if lang == "zh" else en_renderer.css()
    css = re.sub(r"@bottom-center\{[^}]*\}", "", css)
    css = css.replace("V1.9 · 2026-10-31", f"{VERSION} · {DATE}")
    css = css.replace("V1.9 English | 2026-10-31", f"{VERSION} | {DATE}")
    for weight in ("Regular", "Bold"):
        name = f"NotoSansSC-{weight}.ttf"
        embedded = (Path(__file__).resolve().parent / "fonts" / name).as_uri()
        css = css.replace(embedded, f"../11_源码_python生成脚本/fonts/{name}")
    return css + """
.author-view{break-after:page}
.author-view h2{bookmark-level:1}
.author-view p{margin:9pt 0}
.edition-note{font-size:9.4pt;break-after:page}
.edition-note p{margin:8pt 0}
.cover .thesis{font-size:15pt;font-weight:700;color:#315e7c;margin-top:15mm;line-height:1.48}
.cover .edition{margin-top:15mm}
.checked-disclosure{break-before:page}
.checked-disclosure h2{bookmark-level:1}
.report-body h4{bookmark-level:3}
"""


def tagged(text, prefix):
    markup, headings = zh_renderer.tag_headings(markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS))
    markup = re.sub(r'id="h-(\d+)"', rf'id="{prefix}-\1"', markup)
    for heading in headings:
        heading["anchor"] = heading["anchor"].replace("h-", prefix + "-", 1)
    return markup, headings


def write_report(lang, body):
    opening_path = SRC / f"opening_{lang}.md"
    opening = opening_path.read_text(encoding="utf-8-sig").strip()
    note = edition_note(lang)
    ending = footer(lang)
    author = "大队长" if lang == "zh" else "Daduizhang"
    subtitle = "从客户回款、合同付款到设备资本回收" if lang == "zh" else "Customer cash, contractual payments and asset recovery"
    cover_line = (
        "客户净回款能赶上付款日吗？设备还能用多久？"
        if lang == "zh" else "Will cash arrive by the payment date? How long will the equipment earn?"
    )
    contents = "目录" if lang == "zh" else "Contents"
    main, headings = tagged(body, "chapter")
    main = main.replace("<!-- REFERENCES_START -->", '<section class="references">') + "</section>"
    start, starts = tagged(opening, "opening")
    nav = f'<nav class="toc"><h1>{contents}</h1>'
    for h in starts + headings:
        if h["level"] <= 3:
            nav += f'<a class="l{h["level"]}" href="#{h["anchor"]}">{html.escape(h["text"])}</a>'
    nav += "</nav>"
    cover = (
        f'<section class="cover"><div class="rule"></div><div class="brand">{author} · {VERSION}</div>'
        f'<h1>{TITLES[lang]}</h1><p class="subtitle">{subtitle}</p><p class="thesis">{cover_line}</p>'
        f'<p class="edition">{VERSION} · {DATE}</p><div class="foot">{author}</div></section>'
    )
    head = (
        f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta name="author" content="{author}"><title>{TITLES[lang]} · {VERSION}</title>'
        f'<style>{relative_css(lang)}</style>'
    )
    final_note, _ = tagged(ending, "disclosure")
    edition_html, _ = tagged(note, "edition")
    html_text = (
        f'<!doctype html><html lang="{lang}"><head>{head}</head><body>'
        f'<div class="watermark" aria-hidden="true">{author}</div>{cover}'
        f'<section class="author-view">{start}</section><section class="edition-note">{edition_html}</section>'
        f'{nav}<main class="report-body">{main}</main><section class="checked-disclosure">{final_note}</section>'
        f'</body></html>\n'
    )
    markdown_text = (
        f'# {TITLES[lang]} · {VERSION}\n\n{author} · {DATE}\n\n{opening}\n\n{note.strip()}\n\n'
        f'<!-- BODY_START -->\n\n{body}\n\n{ending}'
    )
    if len(set(re.findall(r'\bid="([^"]+)"', html_text))) != len(re.findall(r'\bid="([^"]+)"', html_text)):
        raise ValueError(f"{lang}: duplicate HTML IDs")
    for target in LINKS.findall(markdown_text):
        if target.startswith(("https://", "http://", "#", "mailto:")):
            continue
        if not (OUT / unquote(target.split("#", 1)[0])).is_file():
            raise FileNotFoundError(f"{lang}: invalid relative link {target}")
    prefix = OUT / STEMS[lang]
    for suffix, content in ((".md", markdown_text), (".html", html_text)):
        Path(str(prefix) + suffix).write_text(content, encoding="utf-8", newline="\n")
    return {
        "language": lang,
        "stem": STEMS[lang],
        "baseline": BASES[lang].relative_to(REPO).as_posix(),
        "baseline_sha256": sha256(BASES[lang]),
        "opening_sha256": sha256(opening_path),
        "updates_sha256": sha256(SRC / f"updates_{lang}.md"),
        "references": len(zh_renderer.reference_entries(body)),
        "sections_in_contents": sum(h["level"] <= 3 for h in starts + headings),
    }


def build_pdf(row):
    language, stem = row["language"], row["stem"]
    path = OUT / (stem + ".pdf")
    zh_renderer.render_pdf(OUT / (stem + ".html"), path)
    with fitz.open(path) as pdf:
        if len(pdf) < 100 or len(pdf.get_toc()) < row["sections_in_contents"]:
            raise ValueError(f"{language}: incomplete main report or PDF outline")
        if any(page < 1 or page > len(pdf) for _, _, page in pdf.get_toc()):
            raise ValueError(f"{language}: invalid PDF outline destination")
        row["pages"] = len(pdf)
    row["formats"] = {
        ext: {"file": stem + "." + ext, "sha256": sha256(OUT / (stem + "." + ext))}
        for ext in ("md", "html", "pdf")
    }
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-only", action="store_true", help="assemble Markdown and HTML without printing PDFs")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    docs = {lang: compose(lang) for lang in BASES}
    assets = copy_assets(docs)
    rows = [write_report(lang, content) for lang, content in docs.items()]
    if not args.prepare_only:
        with ThreadPoolExecutor(max_workers=2) as pool:
            rows = list(pool.map(build_pdf, rows))
        manifest = {
            "version": VERSION,
            "editorial_date": DATE,
            "base_version": "V1.9",
            "base_cutoff": BASE_CUTOFF,
            "chapters": CHAPTER_COUNT,
            "market_cutoff_et": "2026-11-20 regular close",
            "builder_sha256": sha256(Path(__file__)),
            "baseline_edits_sha256": sha256(SRC / "baseline_edits.json"),
            "reports": rows,
            "assets": assets,
        }
        (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps({key: row.get(key) for key in ("language", "sections_in_contents", "references", "pages")}))


if __name__ == "__main__":
    main()
