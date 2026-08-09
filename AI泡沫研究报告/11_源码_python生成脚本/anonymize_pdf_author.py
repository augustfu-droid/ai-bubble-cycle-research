#!/usr/bin/env python3
"""Replace the real-name author token in explicitly selected PDF files.

This is a packaging-only transformation for public Git artifacts. It does not
change research facts, dates, scores, probabilities, tables, or conclusions.
Each input path must be given explicitly; the script never scans or rewrites a
directory by default.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import fitz


OLD_AUTHOR = "\u4ed8\u5f3a"
PUBLIC_AUTHOR = "大队长"
REPLACEMENTS = (
    (f"（{PUBLIC_AUTHOR}）", ""),
    (f"({PUBLIC_AUTHOR})", ""),
    (f"{PUBLIC_AUTHOR} （{OLD_AUTHOR}）", PUBLIC_AUTHOR),
    (f"{PUBLIC_AUTHOR}（{OLD_AUTHOR}）", PUBLIC_AUTHOR),
    (f"{PUBLIC_AUTHOR} ({OLD_AUTHOR})", PUBLIC_AUTHOR),
    (f"{PUBLIC_AUTHOR} （{PUBLIC_AUTHOR}）", PUBLIC_AUTHOR),
    (f"{PUBLIC_AUTHOR}（{PUBLIC_AUTHOR}）", PUBLIC_AUTHOR),
    (f"{PUBLIC_AUTHOR} ({PUBLIC_AUTHOR})", PUBLIC_AUTHOR),
    (OLD_AUTHOR, PUBLIC_AUTHOR),
)


def pdf_color(value: int) -> tuple[float, float, float]:
    """Convert PyMuPDF's packed sRGB integer to the PDF 0..1 RGB tuple."""
    return (
        ((value >> 16) & 255) / 255,
        ((value >> 8) & 255) / 255,
        (value & 255) / 255,
    )


def style_for(page: fitz.Page, rect: fitz.Rect) -> tuple[float, tuple[float, float, float]]:
    """Recover the nearest source span's size and color for a local replacement."""
    best: tuple[float, dict] | None = None
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                span_rect = fitz.Rect(span["bbox"])
                overlap = (span_rect & rect).get_area()
                if overlap <= 0:
                    continue
                score = overlap / max(rect.get_area(), 1)
                if best is None or score > best[0]:
                    best = (score, span)
    if best is None:
        return max(4.0, rect.height * 0.62), (0.12, 0.12, 0.12)
    span = best[1]
    return float(span.get("size", rect.height * 0.8)), pdf_color(int(span.get("color", 0)))


def replace_pdf(path: Path) -> tuple[int, int]:
    if not path.is_file() or path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF file: {path}")

    doc = fitz.open(path)
    page_count = doc.page_count
    link_count = sum(len(page.get_links()) for page in doc)
    toc_count = len(doc.get_toc())
    replacements = 0

    for page in doc:
        page_replacements = 0
        occupied: list[fitz.Rect] = []
        for old_text, new_text in REPLACEMENTS:
            for rect in page.search_for(old_text):
                if any((rect & prior).get_area() > 0 for prior in occupied):
                    continue
                source_size, color = style_for(page, rect)
                if not new_text:
                    font_size = source_size
                elif old_text == OLD_AUTHOR:
                    # Three public-name glyphs must fit into the two-glyph source box.
                    font_size = max(4.0, min(source_size * 0.68, rect.width / 3 * 0.95))
                else:
                    font_size = max(4.0, min(source_size, rect.width / 3 * 0.90))
                page.add_redact_annot(
                    rect,
                    text=new_text,
                    fontname="china-s",
                    fontsize=font_size,
                    align=0,
                    fill=None,
                    text_color=color,
                    cross_out=False,
                )
                occupied.append(rect)
                page_replacements += 1
                replacements += 1
        if page_replacements:
            page.apply_redactions(images=0, graphics=0, text=0)

    metadata = dict(doc.metadata or {})
    metadata_changes = 0
    for key, value in list(metadata.items()):
        if isinstance(value, str) and OLD_AUTHOR in value:
            metadata[key] = value.replace(OLD_AUTHOR, PUBLIC_AUTHOR)
            metadata_changes += 1
    if metadata_changes:
        doc.set_metadata(metadata)

    temp_path = path.with_name(f".{path.stem}.anonymizing.pdf")
    try:
        doc.save(temp_path, garbage=4, deflate=True)
    finally:
        doc.close()

    check = fitz.open(temp_path)
    try:
        if check.page_count != page_count:
            raise RuntimeError(f"Page count changed for {path}")
        if sum(len(page.get_links()) for page in check) != link_count:
            raise RuntimeError(f"Link count changed for {path}")
        if len(check.get_toc()) != toc_count:
            raise RuntimeError(f"TOC count changed for {path}")
        if any(OLD_AUTHOR in page.get_text() for page in check):
            raise RuntimeError(f"Real-name text remains in {path}")
        if OLD_AUTHOR in " ".join(str(value) for value in check.metadata.values()):
            raise RuntimeError(f"Real-name metadata remains in {path}")
    finally:
        check.close()

    os.replace(temp_path, path)
    return replacements, metadata_changes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdfs", nargs="+", type=Path, help="Explicit PDF paths to anonymize in place")
    args = parser.parse_args()
    for path in args.pdfs:
        text_changes, metadata_changes = replace_pdf(path.resolve())
        print(f"[OK] {path}: text={text_changes}, metadata={metadata_changes}")


if __name__ == "__main__":
    main()
