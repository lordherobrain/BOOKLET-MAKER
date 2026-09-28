import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation, PageObject

A4W, A4H = 841.8898, 595.2756
HALFW = A4W / 2

def add_fitted(dst, src, x, y, w, h):
    sw, sh = float(src.mediabox.width), float(src.mediabox.height)
    s = min(w / sw, h / sh)
    nw, nh = sw*s, sh*s
    tx, ty = x + (w-nw)/2, y + (h-nh)/2
    dst.merge_transformed_page(src, Transformation().scale(s).translate(tx, ty))

def make_booklet(src, out):
    pages = list(PdfReader(str(src)).pages)
    while len(pages) % 4:
        pages.append(None)
    writer = PdfWriter()

    for i in range(0, len(pages), 4):
        l, r = len(pages)-1-i, i
        # Front: last | first
        front = PageObject.create_blank_page(width=A4W, height=A4H)
        if pages[l]: add_fitted(front, pages[l], 0, 0, HALFW, A4H)
        if pages[r]: add_fitted(front, pages[r], HALFW, 0, HALFW, A4H)
        writer.add_page(front)

        # Back: second | second-last
        back = PageObject.create_blank_page(width=A4W, height=A4H)
        if pages[r+1]: add_fitted(back, pages[r+1], 0, 0, HALFW, A4H)
        if pages[l-1]: add_fitted(back, pages[l-1], HALFW, 0, HALFW, A4H)
        writer.add_page(back)

    with open(out, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Drag a PDF onto this file.")
        input("Press Enter to exit...")
        raise SystemExit
    src = Path(sys.argv[1])
    if src.suffix.lower() != ".pdf":
        print("Only PDF files are supported.")
        input("Press Enter to exit...")
        raise SystemExit
    out = src.with_name(src.stem + "_A4_BOOKLET.pdf")
    try:
        make_booklet(src, out)
        print("Created:", out)
        print("\nPrint: A4, Landscape, Duplex, Flip on SHORT EDGE, 100%/Actual Size.")
    except Exception as e:
        print("ERROR:", e)
    input("\nPress Enter to exit...")
