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


def main() -> None:
    for path, expected in PDFS.items():
        validate_generated_pdf(path, expected)
    validate_thick()
    print("[PASS] All V1.4 PDF and TOC checks completed")


if __name__ == "__main__":
    main()
