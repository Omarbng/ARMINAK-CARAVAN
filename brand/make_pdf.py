#!/usr/bin/env python3
"""print-en.html / print-ru.html → A4 PDF, for sending to the client.

Chrome does the printing: it is the renderer the pages were designed against,
it honours `print-color-adjust: exact` so the navy plates and the sand ground
survive, and it is already installed. The page geometry comes entirely from the
@page rule in the document, so nothing about the paper is decided here.

    python3 brand/make_pdf.py
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

EDITIONS = [
    ("print-en.html", "ARMINAK-CARAVAN-Identity-EN.pdf"),
    ("print-ru.html", "ARMINAK-CARAVAN-Identity-RU.pdf"),
]


def pages(pdf):
    """Page count straight out of the PDF, so the report is not a guess."""
    n = pdf.read_bytes().count(b"/Type /Page") + pdf.read_bytes().count(b"/Type/Page")
    return max(1, n - pdf.read_bytes().count(b"/Type /Pages")
                    - pdf.read_bytes().count(b"/Type/Pages"))


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")

    for src_name, out_name in EDITIONS:
        src = HERE / src_name
        if not src.exists():
            sys.exit(f"{src_name} missing — run build_presentation.py first")
        out = HERE / out_name

        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
             # Without this Chrome stamps its own header and footer — the file
             # path down one margin and a page number down the other.
             "--no-pdf-header-footer",
             # The fonts come from Google Fonts over the network; without a
             # budget Chrome prints before they arrive and falls back to
             # Times, which is not the brand serif.
             "--virtual-time-budget=12000",
             f"--print-to-pdf={out}", src.as_uri()],
            check=True, capture_output=True)

        print(f"  {out_name:<38}{out.stat().st_size // 1024:>5} kB   "
              f"{pages(out)} pages")

    print(f"\n→ {HERE.relative_to(HERE.parent)}/")


if __name__ == "__main__":
    main()
