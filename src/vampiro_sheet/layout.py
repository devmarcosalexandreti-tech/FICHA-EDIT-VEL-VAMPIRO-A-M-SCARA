"""Drawing helpers and constants for the PDF layout."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

PAGE_SIZE = A4
PAGE_W, PAGE_H = A4
MARGIN = 12 * mm
GAP = 4 * mm
RED = colors.HexColor("#6f1d1b")
INK = colors.HexColor("#222222")
MID = colors.HexColor("#666666")
LIGHT = colors.HexColor("#e7e1dd")
PALE = colors.HexColor("#f7f5f3")


def section(c, title, x, y, w, h):
    c.setStrokeColor(LIGHT)
    c.setFillColor(PALE)
    c.roundRect(x, y - h, w, h, 3, stroke=1, fill=1)
    c.setFillColor(RED)
    c.rect(x, y - 15, w, 15, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 6, y - 10.5, title.upper())
    c.setFillColor(INK)


def title(c, page_title, page_no):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 17)
    c.drawString(MARGIN, PAGE_H - 13 * mm, "Ficha de Personagem")
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 12.5 * mm, page_title)
    c.setStrokeColor(RED)
    c.setLineWidth(1.2)
    c.line(MARGIN, PAGE_H - 16 * mm, PAGE_W - MARGIN, PAGE_H - 16 * mm)
    c.setFillColor(MID)
    c.setFont("Helvetica", 7)
    c.drawRightString(PAGE_W - MARGIN, 8 * mm, f"Vampiro: A Mascara 3e - pagina {page_no}")


def label(c, text, x, y, size=6.7):
    c.setFillColor(MID)
    c.setFont("Helvetica", size)
    c.drawString(x, y, text)
    c.setFillColor(INK)


def small_note(c, text, x, y, w=None, size=6):
    c.setFillColor(MID)
    c.setFont("Helvetica", size)
    if w is None:
        c.drawString(x, y, text)
    else:
        words = text.split()
        line = ""
        yy = y
        for word in words:
            trial = f"{line} {word}".strip()
            if c.stringWidth(trial, "Helvetica", size) > w and line:
                c.drawString(x, yy, line)
                yy -= size + 1.5
                line = word
            else:
                line = trial
        if line:
            c.drawString(x, yy, line)
    c.setFillColor(INK)


def columns(n=3):
    total = PAGE_W - 2 * MARGIN - (n - 1) * GAP
    w = total / n
    return [(MARGIN + i * (w + GAP), w) for i in range(n)]
