#!/usr/bin/env python3
"""Validate V1.4 PDF outputs, generated TOCs, links, page counts and key text."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]

PDFS = {
    ROOT / "12_增量素材/2026-07-24_V1.4滚动更新模块.pdf": 7,
    ROOT / "02_主报告V1.4/00_AI周期与泡沫深度研究报告_主报告_V1.4.pdf": 70,
    ROOT / "02_主报告V1.4/01_AI周期与泡沫_事实审计表_V1.4.pdf": 13,
    ROOT / "05_简版与执行摘要/AI周期与泡沫_机构简版_V1.4_内部署名版.pdf": 5,
    ROOT / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4完整重排版.pdf": 90,
}

THICK = ROOT / "06_全景与剧本版/2026年AI泡沫研究 · 全景版_V1.4超全景版_300页级.pdf"

MAINTENANCE_PDFS = {
    ROOT / "04_分项报告/01_利润真实性拆解_V1.4维护版.pdf": 26,
    ROOT / "04_分项报告/02_循环投资网络_V1.4维护版.pdf": 25,
    ROOT / "04_分项报告/03_AI变现与编程TAM_V1.4维护版.pdf": 27,
    ROOT / "04_分项报告/04_AGI与国际格局_V1.4维护版.pdf": 19,
    ROOT / "05_简版与执行摘要/2026年AI泡沫研究 · 公开精简版_V1.4维护版.pdf": 74,
    ROOT / "05_简版与执行摘要/2026年AI泡沫研究 · 雪球公开版_V1.4维护版.pdf": 74,
    ROOT / "05_简版与执行摘要/2026年AI泡沫研究 · 摘要版_V1.4维护版.pdf": 13,
    ROOT / "05_简版与执行摘要/AI周期与泡沫研究_执行简版_V1.4维护版.pdf": 7,
    ROOT / "06_全景与剧本版/AI周期与泡沫_完整合集_V1.4维护版.pdf": 182,
    ROOT / "06_全景与剧本版/AI泡沫全景研究_延迟即放大版_V1.4维护版.pdf": 139,
    ROOT / "06_全景与剧本版/AI泡沫崩盘剧本_V1.4维护版.pdf": 19,
    ROOT / "06_全景与剧本版/公众号00_发布引流稿_V1.4维护版.pdf": 4,
}

REQUIRED_TEXT = (
    "2026-07-24",
    "DeepSeek",
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


def validate_generated_pdf(path: Path, expected_pages: int) -> None:
    reader = PdfReader(str(path))
    assert len(reader.pages) == expected_pages, (path.name, len(reader.pages), expected_pages)
    full_text = "\n".join((page.extract_text() or "") for page in reader.pages)
    for token in REQUIRED_TEXT:
        assert token in full_text, (path.name, token)
    compact_text = full_text.replace(" ", "")
    assert "73项" in compact_text or "63→73" in compact_text, (path.name, "73项")
    assert "Alphabet" in full_text and "官方" in full_text, (path.name, "Alphabet官方")

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
    assert len(reader.pages) == 317, len(reader.pages)
    assert reader.page_labels[:9] == ["1", "2", "3", "4", "5", "6", "7", "1", "2"], reader.page_labels[:9]

    # Current update module TOC is on physical page 2 and must match its own 1–7 page labels.
    assert printed_toc_numbers(reader, 1) == named_toc_targets(reader, 1)

    # Historical TOC occupies original pages 6–9, now physical pages 13–16.
    page_object_ids = {page.indirect_reference.idnum for page in reader.pages}
    checked = 0
    for page_index in range(12, 16):
        for ref in reader.pages[page_index].get("/Annots", []):
            dest = ref.get_object().get("/Dest")
            if isinstance(dest, list) and dest and hasattr(dest[0], "idnum"):
                assert dest[0].idnum in page_object_ids, (page_index + 1, dest[0].idnum)
                checked += 1
    assert checked >= 150, checked
    print(
        f"[PASS] {THICK.name}: 317 pages, dual page labels reset correctly, "
        f"{checked} historical TOC link rectangles resolve"
    )


def validate_maintenance(path: Path, base_pages: int) -> None:
    reader = PdfReader(str(path))
    update_pages = PDFS[ROOT / "12_增量素材/2026-07-24_V1.4滚动更新模块.pdf"]
    assert len(reader.pages) == update_pages + base_pages, (path.name, len(reader.pages), base_pages)
    assert reader.page_labels[:9] == ["1", "2", "3", "4", "5", "6", "7", "1", "2"], (
        path.name,
        reader.page_labels[:9],
    )
    front_text = "\n".join((page.extract_text() or "") for page in reader.pages[:update_pages])
    assert "2026-07-24" in front_text and "DeepSeek" in front_text and "Alphabet" in front_text, path.name

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
    for path, expected in PDFS.items():
        validate_generated_pdf(path, expected)
    validate_thick()
    for path, base_pages in MAINTENANCE_PDFS.items():
        validate_maintenance(path, base_pages)
    print("[PASS] All V1.4 PDF and TOC checks completed")


if __name__ == "__main__":
    main()
