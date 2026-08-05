#!/usr/bin/env python3
"""Validate current V1.4 outputs, TOCs, links, images and semantic release gates."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PRIVATE_AUTHOR = "\u4ed8\u5f3a"
PUBLIC_AUTHOR = "大队长"
TEXT_SUFFIXES = {".md", ".py", ".txt", ".html", ".css", ".json", ".yml", ".yaml"}

PDFS = {
    ROOT / "12_增量素材/2026-08-05_V1.4滚动更新模块.pdf": 10,
    ROOT / "02_主报告V1.4/00_AI周期与泡沫深度研究报告_主报告_V1.4.pdf": 65,
    ROOT / "02_主报告V1.4/01_AI周期与泡沫_事实审计表_V1.4.pdf": 12,
    ROOT / "05_简版与执行摘要/AI周期与泡沫_机构简版_V1.4_内部署名版.pdf": 5,
    ROOT / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4完整重排版.pdf": 85,
}

THICK = ROOT / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4超全景版_300页级.pdf"

MAINTENANCE_PDFS = {
    ROOT / "04_分项报告/01_利润真实性拆解_V1.4维护版.pdf": (26, 0),
    ROOT / "04_分项报告/02_循环投资网络_V1.4维护版.pdf": (25, 1),
    ROOT / "04_分项报告/03_AI变现与编程TAM_V1.4维护版.pdf": (27, 0),
    ROOT / "04_分项报告/04_AGI与国际格局_V1.4维护版.pdf": (19, 0),
    ROOT / "05_简版与执行摘要/2026年AI泡沫研究 · 公开精简版_V1.4维护版.pdf": (74, 0),
    ROOT / "05_简版与执行摘要/2026年AI泡沫研究 · 雪球公开版_V1.4维护版.pdf": (74, 0),
    ROOT / "05_简版与执行摘要/2026年AI泡沫研究 · 摘要版_V1.4维护版.pdf": (13, 0),
    ROOT / "05_简版与执行摘要/AI周期与泡沫研究_执行简版_V1.4维护版.pdf": (7, 0),
    ROOT / "06_全景与剧本版/AI周期与泡沫_完整合集_V1.4维护版.pdf": (182, 1),
    ROOT / "06_全景与剧本版/AI泡沫全景研究_延迟即放大版_V1.4维护版.pdf": (139, 0),
    ROOT / "06_全景与剧本版/AI泡沫崩盘剧本_V1.4维护版.pdf": (19, 0),
    ROOT / "06_全景与剧本版/公众号00_发布引流稿_V1.4维护版.pdf": (4, 0),
}

REQUIRED_TEXT = (
    "2026-08-05",
    "DeepSeek",
    "Meta",
    "Microsoft",
)

CURRENT_REQUIRED_TEXT = (
    "规则内临界成立",
    "0.23元",
    "首发适配",
    "V4-Flash API",
    "43.785",
    "El Paso",
    "Trigger ID",
    "5条成立",
    "FY26Q4",
    "维谛技术",
    "Amazon",
    "SpaceX",
    "88项",
)

FORBIDDEN_CURRENT_TEXT = (
    "华为云完成V4系列零日适配",
    "可在ModelArts完成V4系列",
    "市场开始提高对CapEx与FCF错配的惩罚",
    "也未接近7/1阶段高点",
    "投递后维护版",
    "已投递",
    "203.28",
    "Form 10-Q 在本版截止时未找到",
    "Microsoft与Meta美东盘后发布，均属本版截止时的 PENDING",
    "完整官方Q&A文字稿待补",
    "北京时7/31凌晨Amazon",
    "[[CHART:",
    "TODO",
)

CURRENT_SOURCES = (
    ROOT / "12_增量素材/2026-07-20_V1.4更新模块_全报告统一口径.md",
    ROOT / "10_源码_markdown/AI周期与泡沫_事实审计表_V1.4_增量.md",
    ROOT / "10_源码_markdown/AI周期与泡沫_机构简版_V1.4.md",
)

CURRENT_METADATA = (
    ROOT / "00_使用说明/README_大队长_全量存档说明.md",
    ROOT / "00_使用说明/版本矩阵_V1.4_2026-08-05.md",
    ROOT / "复审与版本记录/版本变更说明_2026-08-05.md",
    ROOT / "复审与版本记录/引用核验报告_2026-08-05.md",
    ROOT / "复审与版本记录/专业复审报告_2026-08-05.md",
    ROOT / "复审与版本记录/PDF与目录核验报告_2026-08-05.md",
    ROOT / "复审与版本记录/发布清单_2026-08-05.md",
)

DERIVED_CURRENT_SOURCES = (
    ROOT / "10_源码_markdown/AI周期与泡沫深度研究报告_V1.4合成源.md",
    ROOT / "10_源码_markdown/AI周期与泡沫深度研究报告_全景版_V1.4合成源.md",
)


def validate_current_sources() -> None:
    texts = {path: path.read_text(encoding="utf-8") for path in CURRENT_SOURCES}
    joined = "\n".join(texts.values())
    for token in CURRENT_REQUIRED_TEXT:
        assert token in joined, ("current sources", token)
    for token in FORBIDDEN_CURRENT_TEXT:
        assert token not in joined, ("current sources", token)
    for path, source_text in texts.items():
        compact = re.sub(r"\s+", "", source_text)
        assert "77/100" in compact or "指数75→77" in compact, (path.name, "score")
        assert "A44/B22/C10/D24" in compact, (path.name, "scenario probabilities")
        assert "1/3" in source_text and "2/3" in source_text, (path.name, "trigger counts")
        for rel in re.findall(r"!\[[^\]]*\]\((\.\./13_全景版配图/[^)]+)\)", source_text):
            target = (path.parent / rel).resolve()
            assert target.exists(), (path.name, "missing local image", rel)

    audit_text = texts[ROOT / "10_源码_markdown/AI周期与泡沫_事实审计表_V1.4_增量.md"]
    ids = re.findall(r"^\| \*\*(13(?:[i-z]|a[a-g]))【V1\.4", audit_text, flags=re.M)
    expected_ids = [f"13{letter}" for letter in "ijklmnopqrstuvwxyz"] + [f"13a{letter}" for letter in "abcdefg"]
    assert len(ids) == 25 and len(set(ids)) == 25, ids
    assert ids == expected_ids, ids
    audit_rows = [
        line.strip().strip("|").split("|")
        for line in audit_text.splitlines()
        if re.match(r"^\| \*\*13(?:[i-z]|a[a-g])【V1\.4", line)
    ]
    assert all(len(row) == 8 for row in audit_rows), [
        (ids[index], len(row)) for index, row in enumerate(audit_rows)
    ]
    for item_id, row in zip(ids, audit_rows):
        assert "http" in row[3], (item_id, "missing source URL")
        assert re.search(r"2026[/.-]\d{2}", row[4]), (item_id, "missing source date")
        assert "★" in row[5], (item_id, "missing source grade")
        assert row[6].strip(), (item_id, "missing audit verdict")
        assert row[7].strip(), (item_id, "missing change note")
    assert "88 项" in audit_text and "★★★/★★" in audit_text, "audit count/source grade"
    for path in CURRENT_METADATA:
        metadata_text = path.read_text(encoding="utf-8")
        assert "2026-08-05" in metadata_text, (path.name, "release date")
        assert "14_面试准备/" not in metadata_text and "17_招聘Dashboard/" not in metadata_text, (
            path.name,
            "recruiting files must not enter release list",
        )
    for path in DERIVED_CURRENT_SOURCES:
        derived_text = path.read_text(encoding="utf-8")
        assert "42% A 软着陆权重" not in derived_text, (path.name, "scenario name")
        assert "AWS 增长依赖 Anthropic 重估" not in derived_text, (path.name, "operating/non-operating mix")
        assert "【V1.2 起最新口径" not in derived_text, (path.name, "stale latest label")
        assert "历史版本预测" in derived_text and "截至2026Q2的结算" in derived_text, (
            path.name,
            "historical forecast settlement",
        )
        assert "当前口径唯一入口" in derived_text, (path.name, "current-version override")
    print(
        "[PASS] Current Markdown sources: 25 unique V1.4 items, 8 fields per row, "
        "source URL/date/grade/verdict/change note and local images complete"
    )


def validate_public_identity() -> None:
    """Prevent the private author token from entering Git-bound report artifacts."""
    checked_text = 0
    checked_pdfs = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        assert PRIVATE_AUTHOR not in path.name, ("private author in path", path)
        if path.suffix.lower() in TEXT_SUFFIXES:
            content = path.read_text(encoding="utf-8", errors="ignore")
            assert PRIVATE_AUTHOR not in content, ("private author in text", path)
            checked_text += 1
        elif path.suffix.lower() == ".pdf":
            reader = PdfReader(str(path))
            metadata = " ".join(str(value) for value in (reader.metadata or {}).values())
            assert PRIVATE_AUTHOR not in metadata, ("private author in PDF metadata", path)
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                assert PRIVATE_AUTHOR not in text, ("private author in PDF", path, page_number)
            checked_pdfs += 1
    assert PUBLIC_AUTHOR in (ROOT / "README.md").read_text(encoding="utf-8")
    print(
        f"[PASS] Public identity: {checked_text} text files and {checked_pdfs} PDFs "
        f"contain no private author token; Git author is {PUBLIC_AUTHOR}"
    )


def named_toc_targets(reader: PdfReader, page_index: int) -> list[int]:
    """Return target page numbers from one generated TOC page, collapsing duplicate link rectangles."""
    names = reader.named_destinations
    dests: list[str] = []
    for ref in reader.pages[page_index].get("/Annots", []):
        dest = ref.get_object().get("/Dest")
        if isinstance(dest, str) and (not dests or dests[-1] != dest):
            dests.append(dest)
    return [reader.get_destination_page_number(names[dest]) + 1 for dest in dests]


def printed_toc_numbers(reader: PdfReader, page_index: int) -> list[int]:
    """Read the floated page-number column emitted by WeasyPrint."""
    values: list[int] = []

    def visitor(text, _cm, tm, _font, _size):
        clean = text.strip()
        if clean.isdigit() and tm[4] > 300:
            values.append(int(clean))

    reader.pages[page_index].extract_text(visitor_text=visitor)
    return values


def validate_generated_pdf(path: Path, minimum_pages: int) -> None:
    reader = PdfReader(str(path))
    assert (reader.metadata or {}).get("/Author") == PUBLIC_AUTHOR, (path.name, "PDF author metadata")
    assert len(reader.pages) >= minimum_pages, (path.name, len(reader.pages), minimum_pages)
    full_text = "\n".join((page.extract_text() or "") for page in reader.pages)
    normalized_text = re.sub(r"\s+", "", full_text)
    for token in REQUIRED_TEXT:
        assert token in full_text or re.sub(r"\s+", "", token) in normalized_text, (path.name, token)
    for token in CURRENT_REQUIRED_TEXT:
        assert token in full_text or re.sub(r"\s+", "", token) in normalized_text, (path.name, token)
    for token in FORBIDDEN_CURRENT_TEXT:
        assert token not in full_text, (path.name, token)
    compact_text = normalized_text
    assert "88项" in compact_text or "63→88" in compact_text, (path.name, "88项")
    assert "Alphabet" in full_text and "官方" in full_text, (path.name, "Alphabet官方")
    assert "V1.4" in full_text and "滚动核验至" in full_text, (path.name, "统一当前页眉")
    if path in {
        ROOT / "12_增量素材/2026-08-05_V1.4滚动更新模块.pdf",
        ROOT / "02_主报告V1.4/00_AI周期与泡沫深度研究报告_主报告_V1.4.pdf",
        ROOT / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4完整重排版.pdf",
    }:
        assert "V1.4滚动更新日志" in full_text, (path.name, "滚动更新日志")
        assert "版本变更说明（最新）" not in full_text, (path.name, "旧重复标题")
    cover_text = reader.pages[0].extract_text() or ""
    assert "当前判断" in cover_text and "阅读规则" in cover_text, (path.name, "统一首页")
    if path in {
        ROOT / "02_主报告V1.4/00_AI周期与泡沫深度研究报告_主报告_V1.4.pdf",
        ROOT / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4完整重排版.pdf",
    }:
        assert "历史版本沿革" in full_text, (path.name, "历史版本沿革")
        assert "历史数字不得冒充当前结论" in full_text, (path.name, "persistent historical footer")
        assert "42% A 软着陆权重" not in full_text, (path.name, "scenario name")
        assert "AWS 增长依赖 Anthropic 重估" not in full_text, (path.name, "operating/non-operating mix")
        assert "【V1.2 起最新口径" not in full_text, (path.name, "stale latest label")
        assert "截至2026Q2的结算" in normalized_text, (path.name, "historical forecast settlement")
    assert "[[CHART:" not in full_text and "TODO" not in full_text, (path.name, "raw placeholder")

    toc_pages = 0
    toc_rows = 0
    for page_index in range(1, len(reader.pages)):
        targets = named_toc_targets(reader, page_index)
        if not targets:
            break
        printed = printed_toc_numbers(reader, page_index)
        assert printed == targets, (path.name, page_index + 1, printed[:8], targets[:8])
        toc_pages += 1
        toc_rows += len(targets)
    assert toc_pages >= 1 and toc_rows >= 5, (path.name, toc_pages, toc_rows)
    print(f"[PASS] {path.name}: {len(reader.pages)} pages, {toc_pages} TOC pages, {toc_rows} exact TOC targets")


def validate_thick() -> None:
    reader = PdfReader(str(THICK))
    assert (reader.metadata or {}).get("/Author") == PUBLIC_AUTHOR, (THICK.name, "PDF author metadata")
    update_path = ROOT / "12_增量素材/2026-08-05_V1.4滚动更新模块.pdf"
    update_pages = len(PdfReader(str(update_path)).pages)
    front_count = update_pages + 1
    assert reader.page_labels[: front_count + 2] == [
        *[str(i) for i in range(1, front_count + 1)],
        "3",
        "4",
    ], reader.page_labels[: front_count + 2]

    first_page_text = reader.pages[0].extract_text() or ""
    assert (
        "V1.4" in first_page_text
        and "全景版" in first_page_text
        and "当前判断" in first_page_text
        and "阅读规则" in first_page_text
        and "V1.4 修订说明" not in first_page_text
    ), first_page_text[:300]
    disclaimer_text = reader.pages[1].extract_text() or ""
    assert "免责声明" in disclaimer_text and "V1.4维护版" in disclaimer_text, disclaimer_text[:200]
    update_text = reader.pages[2].extract_text() or ""
    assert (
        "总目录" in update_text
        and "当前有效口径" in update_text
        and "历史冻结研究" in update_text
        and "历史原版索引（留档）" in update_text
        and "滚动核验至" in update_text
    ), update_text[:400]
    actual_total_toc_targets = []
    for ref in reader.pages[2].get("/Annots", []):
        annotation = ref.get_object()
        dest = annotation.get("/Dest") or (annotation.get("/A") or {}).get("/D")
        if isinstance(dest, list) and dest and isinstance(dest[0], int):
            actual_total_toc_targets.append(dest[0] + 1)
    printed_total_toc_numbers = printed_toc_numbers(reader, 2)
    assert len(actual_total_toc_targets) == len(printed_total_toc_numbers) >= 16, actual_total_toc_targets
    assert actual_total_toc_targets == printed_total_toc_numbers, (
        actual_total_toc_targets,
        printed_total_toc_numbers,
    )
    front_text = "\n".join((page.extract_text() or "") for page in reader.pages[:front_count])
    assert "V1.4滚动更新日志" in front_text, "超全景卷首滚动日志"
    assert "版本变更说明（最新）" not in front_text, "超全景卷首旧重复标题"
    historical_text = reader.pages[front_count].extract_text() or ""
    assert "历史冻结正文" in historical_text and "卷首 V1.4" in historical_text, historical_text[:200]
    structure_text = reader.pages[front_count + 1].extract_text() or ""
    archive_index_text = reader.pages[front_count + 3].extract_text() or ""
    assert "历史版本结构说明" in structure_text and "当前总目录见卷首第3页" in structure_text, structure_text[:300]
    assert (
        "历史原版索引（留档）" in archive_index_text
        and "不作为第二套当前目录" in archive_index_text
    ), archive_index_text[:300]

    # Discover historical internal-link pages instead of relying on magic offsets.
    page_object_ids = {page.indirect_reference.idnum for page in reader.pages}
    checked = 0
    toc_pages = 0
    for page_index in range(front_count, len(reader.pages)):
        page_checked = 0
        for ref in reader.pages[page_index].get("/Annots", []):
            dest = ref.get_object().get("/Dest")
            if isinstance(dest, list) and dest and hasattr(dest[0], "idnum"):
                assert dest[0].idnum in page_object_ids, (page_index + 1, dest[0].idnum)
                checked += 1
                page_checked += 1
        if page_checked >= 5:
            toc_pages += 1
    assert checked >= 150, checked
    assert toc_pages >= 4, toc_pages
    print(
        f"[PASS] {THICK.name}: {len(reader.pages)} pages, one {len(actual_total_toc_targets)}-link dynamic total TOC with exact merged-page targets, "
        f"{checked} historical internal link rectangles resolve across {toc_pages} archive-index pages"
    )


def validate_maintenance(path: Path, base_pages: int, cover_index: int) -> None:
    reader = PdfReader(str(path))
    assert (reader.metadata or {}).get("/Author") == PUBLIC_AUTHOR, (path.name, "PDF author metadata")
    update_path = ROOT / "12_增量素材/2026-08-05_V1.4滚动更新模块.pdf"
    update_pages = len(PdfReader(str(update_path)).pages)
    assert len(reader.pages) == update_pages + base_pages - 1, (
        path.name,
        len(reader.pages),
        base_pages,
    )
    expected_tail = ["1", "3"] if cover_index else ["2", "3"]
    label_probe = reader.page_labels[: update_pages + 2]
    assert label_probe == [*[str(i) for i in range(1, update_pages + 1)], *expected_tail], (
        path.name,
        label_probe,
    )
    front_text = "\n".join((page.extract_text() or "") for page in reader.pages[:update_pages])
    historical_header = reader.pages[update_pages].extract_text() or ""
    assert (
        "V1.4" in (reader.pages[0].extract_text() or "")
        and "当前判断" in (reader.pages[0].extract_text() or "")
        and "阅读规则" in (reader.pages[0].extract_text() or "")
        and "V1.4 修订说明" not in (reader.pages[0].extract_text() or "")
        and "2026-08-05" in front_text
        and "DeepSeek" in front_text
        and "Alphabet" in front_text
        and "V1.4滚动更新日志" in front_text
        and "版本变更说明（最新）" not in front_text
        and "滚动核验至" in front_text
        and "历史冻结正文" in historical_header
        and "卷首 V1.4" in historical_header
    ), path.name

    names = reader.named_destinations
    page_object_ids = {page.indirect_reference.idnum for page in reader.pages}
    checked_named = 0
    checked_direct = 0
    for page in reader.pages:
        for ref in page.get("/Annots", []):
            dest = ref.get_object().get("/Dest")
            if isinstance(dest, str):
                assert dest in names, (path.name, dest)
                target = reader.get_destination_page_number(names[dest])
                assert 0 <= target < len(reader.pages), (path.name, dest, target)
                checked_named += 1
            elif isinstance(dest, list) and dest and hasattr(dest[0], "idnum"):
                assert dest[0].idnum in page_object_ids, (path.name, dest[0].idnum)
                checked_direct += 1
    print(
        f"[PASS] {path.name}: {len(reader.pages)} pages, dual page labels, "
        f"{checked_named} named and {checked_direct} direct internal link rectangles resolve"
    )


def main() -> None:
    validate_current_sources()
    for path, expected in PDFS.items():
        validate_generated_pdf(path, expected)
    validate_thick()
    for path, (base_pages, cover_index) in MAINTENANCE_PDFS.items():
        validate_maintenance(path, base_pages, cover_index)
    validate_public_identity()
    print("[PASS] All V1.4 PDF and TOC checks completed")


if __name__ == "__main__":
    main()
