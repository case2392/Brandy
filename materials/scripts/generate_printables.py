#!/usr/bin/env python3
"""Generate Brandy's homeschool printables:
  1. Letter-of-the-week tracing pages (big kid, 4-5) - all 26 letters
  2. Letter-of-the-week toddler pages (almost 3) - all 26 letters
  3. Weekly rhythm chart (one landscape page)
  4. Bible story activity sheets (4 stories x 2 levels)

Run from repo root:  python3 materials/scripts/generate_printables.py
"""
import os
import random
import string
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

W, H = letter  # 612 x 792
OUT = os.path.join(os.path.dirname(__file__), "..")

# soft, printer-friendly palette
INK = HexColor("#3d3d3d")
SOFT = HexColor("#9b9b9b")
TRACE = HexColor("#b8b8b8")
BLUE = HexColor("#5b8db8")
GOLD = HexColor("#d9a441")
GREEN = HexColor("#7a9e7e")
ROSE = HexColor("#c98a8a")
PALE_BLUE = HexColor("#e8f0f6")
PALE_GOLD = HexColor("#faf3e3")
PALE_GREEN = HexColor("#edf3ee")
PALE_ROSE = HexColor("#f8eded")

FONT = "Helvetica"
BOLD = "Helvetica-Bold"
ITAL = "Helvetica-Oblique"


def ctext(c, x, y, text, font=FONT, size=12, color=INK):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, text)


def ccenter(c, y, text, font=FONT, size=12, color=INK, cx=W / 2):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(cx, y, text)


def stroke_letter(c, x, y, ch, size, color=TRACE, dashed=True, width=1.3):
    """Draw a hollow (stroke-only) letter for tracing/coloring."""
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    if dashed:
        c.setDash([4, 3])
    t = c.beginText(x, y)
    t.setFont(BOLD, size)
    t.setTextRenderMode(1)  # stroke only
    t.textOut(ch)
    c.drawText(t)
    c.restoreState()


def solid_letter(c, x, y, ch, size, color=SOFT):
    c.setFillColor(color)
    c.setFont(BOLD, size)
    c.drawString(x, y, ch)


def header_footer(c, title, subtitle, accent=BLUE):
    c.setStrokeColor(accent)
    c.setLineWidth(3)
    c.line(54, H - 50, W - 54, H - 50)
    ctext(c, 54, H - 42, title, BOLD, 11, accent)
    c.setFillColor(SOFT)
    c.setFont(FONT, 9)
    c.drawRightString(W - 54, H - 42, subtitle)


def name_line(c, y):
    ctext(c, 54, y, "Name:", FONT, 10, SOFT)
    c.setStrokeColor(SOFT)
    c.setLineWidth(0.7)
    c.setDash([])
    c.line(90, y - 1, 300, y - 1)


def guide_lines(c, x0, x1, base, xheight, cap):
    """Handwriting guides: baseline solid, midline dashed, topline solid."""
    c.saveState()
    c.setLineWidth(0.7)
    c.setStrokeColor(HexColor("#d7e3ec"))
    c.setDash([])
    c.line(x0, base, x1, base)
    c.line(x0, base + cap, x1, base + cap)
    c.setDash([3, 3])
    c.line(x0, base + xheight, x1, base + xheight)
    c.restoreState()


# ---------------------------------------------------------------- big kid page
def big_kid_page(c, ch):
    up, lo = ch.upper(), ch.lower()
    header_footer(c, "LETTER OF THE WEEK", "Big Kid Page")
    name_line(c, H - 78)

    # display letters
    c.setFillColor(BLUE)
    c.setFont(BOLD, 110)
    pair = up + lo
    pw = stringWidth(pair, BOLD, 110) + 10
    c.drawCentredString(W / 2, H - 200, up + " " + lo)
    ccenter(c, H - 228, f"This week's letter is {up}!", ITAL, 12, SOFT)

    # tracing rows: uppercase then lowercase
    size = 64
    cap = size * 0.72
    xh = size * 0.52
    rows = [(up, H - 330), (lo, H - 430)]
    for glyph, base in rows:
        gw = stringWidth(glyph, BOLD, size)
        gap = 24
        n = 6
        total = n * gw + (n - 1) * gap
        x = (W - total) / 2
        guide_lines(c, x - 10, x + total + 10, base, xh, cap)
        for i in range(n):
            if i == 0:
                solid_letter(c, x, base, glyph, size)
            else:
                stroke_letter(c, x, base, glyph, size)
            x += gw + gap

    # letter hunt
    y = H - 520
    ctext(c, 54, y, f"Letter hunt!  Circle every  {up}  and  {lo}  you can find:",
          BOLD, 12, GREEN)
    rng = random.Random(ord(up))
    others = [l for l in string.ascii_uppercase if l != up]
    hunt = [up, up, lo, lo] + [rng.choice(others + [o.lower() for o in others])
                               for _ in range(8)]
    rng.shuffle(hunt)
    hx, step = 70, (W - 140) / 12
    for i, g in enumerate(hunt):
        c.setFillColor(INK)
        c.setFont(BOLD, 26)
        c.drawCentredString(hx + i * step, y - 40, g)

    # draw box
    top = y - 80
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.setDash([])
    c.roundRect(54, 80, W - 108, top - 80, 10)
    ctext(c, 66, top - 22, f"Draw something that starts with {up}:", BOLD, 12, GOLD)
    c.showPage()


# ---------------------------------------------------------------- toddler page
def toddler_page(c, ch):
    up, lo = ch.upper(), ch.lower()
    header_footer(c, "LETTER OF THE WEEK", "Little Sister Page", accent=ROSE)
    ccenter(c, H - 80, f"{up} is for little hands!", ITAL, 12, SOFT)

    # giant hollow uppercase letter to color / sticker / finger-trace
    size = 430
    gw = stringWidth(up, BOLD, size)
    stroke_letter(c, (W - gw) / 2, H - 560, up, size,
                  color=ROSE, dashed=False, width=2.2)

    # small hollow lowercase companion, tucked in the bottom-right corner
    size2 = 140
    gw2 = stringWidth(lo, BOLD, size2)
    stroke_letter(c, W - 58 - gw2, 148, lo, size2,
                  color=TRACE, dashed=False, width=1.6)

    # crayon-trace row
    tsize = 84
    gw3 = stringWidth(up, BOLD, tsize)
    x = 70
    for i in range(3):
        stroke_letter(c, x, 90, up, tsize)
        x += gw3 + 30

    ccenter(c, 52, "Color it, dot it with stickers, or trace it with a finger!",
            BOLD, 12, ROSE)
    c.showPage()


# ------------------------------------------------------------- rhythm chart
def rhythm_chart(path):
    LW, LH = landscape(letter)
    c = canvas.Canvas(path, pagesize=landscape(letter))

    ccenter(c, LH - 55, "Our Weekly Rhythm", BOLD, 26, BLUE, cx=LW / 2)
    ccenter(c, LH - 75, "Big sister (almost 5)   •   Little sister (almost 3)   •   Baby brother (along for the ride)",
            ITAL, 11, SOFT, cx=LW / 2)

    blocks = [
        ("Morning Basket", "15 min", PALE_GOLD, GOLD,
         "Bible story + song + prayer, all together on the couch."),
        ("Table Time 1 — Letters", "15–20 min", PALE_BLUE, BLUE,
         "Phonics & letter of the week.  Little sister: salt tray, playdough letters, or busy bag."),
        ("Wiggle Break + Snack", "20 min", PALE_ROSE, ROSE,
         "Music, dancing, or outside.  Everyone resets."),
        ("Table Time 2 — Numbers", "10–15 min", PALE_BLUE, BLUE,
         "Counting, patterns, simple math games.  Little sister: counting bears, stacking."),
        ("Hands-On Time", "20–30 min", PALE_GREEN, GREEN,
         "Science, nature walk, craft, or Bible activity — both girls, two levels."),
        ("Read-Aloud + Rest", "20+ min", PALE_GOLD, GOLD,
         "Books on the couch, then quiet play while baby naps."),
    ]
    x0, bw = 40, LW / 2 - 60
    y = LH - 110
    ctext(c, x0, y + 4, "DAILY RHYTHM  (follow the order, not the clock)", BOLD, 11, INK)
    for name, mins, fill, accent, desc in blocks:
        bh = 62
        y -= bh + 8
        c.setFillColor(fill)
        c.setStrokeColor(accent)
        c.setLineWidth(1)
        c.roundRect(x0, y, bw, bh, 8, stroke=1, fill=1)
        ctext(c, x0 + 12, y + bh - 20, name, BOLD, 12, accent)
        c.setFillColor(SOFT)
        c.setFont(FONT, 9)
        c.drawRightString(x0 + bw - 12, y + bh - 20, mins)
        c.setFillColor(INK)
        c.setFont(FONT, 9)
        for i, line in enumerate(simpleSplit(desc, FONT, 9, bw - 24)[:2]):
            c.drawString(x0 + 12, y + bh - 36 - i * 11, line)

    # right column: focus of the day
    rx = LW / 2 + 20
    rw = LW / 2 - 60
    y = LH - 110
    ctext(c, rx, y + 4, "FOCUS OF THE DAY", BOLD, 11, INK)
    days = [
        ("Monday", "New letter + Bible story of the week", PALE_BLUE, BLUE),
        ("Tuesday", "ENRICHMENT SCHOOL DAY, 9:00–12:00 — home is just read-alouds", PALE_GOLD, GOLD),
        ("Wednesday", "Letter practice + numbers", PALE_BLUE, BLUE),
        ("Thursday", "Numbers + science / nature", PALE_BLUE, BLUE),
        ("Friday", "Craft day + review + library trip", PALE_BLUE, BLUE),
    ]
    for day, focus, fill, accent in days:
        bh = 46
        y -= bh + 8
        c.setFillColor(fill)
        c.setStrokeColor(accent)
        c.setLineWidth(1)
        c.roundRect(rx, y, rw, bh, 8, stroke=1, fill=1)
        ctext(c, rx + 12, y + bh - 18, day, BOLD, 11, accent)
        c.setFillColor(INK)
        c.setFont(FONT, 9)
        for i, line in enumerate(simpleSplit(focus, FONT, 9, rw - 24)[:2]):
            c.drawString(rx + 12, y + bh - 32 - i * 10, line)

    y -= 78
    c.setFillColor(PALE_GREEN)
    c.setStrokeColor(GREEN)
    c.roundRect(rx, y, rw, 64, 8, stroke=1, fill=1)
    ctext(c, rx + 12, y + 48, "Remember", BOLD, 11, GREEN)
    tips = ("Total seat work is only ~45 min. Everything else is play, books, "
            "and life. A short day is still a school day.")
    c.setFillColor(INK)
    c.setFont(FONT, 9)
    for i, line in enumerate(simpleSplit(tips, FONT, 9, rw - 24)[:3]):
        c.drawString(rx + 12, y + 34 - i * 11, line)

    c.save()


# --------------------------------------------------------- bible story sheets
def story_header(c, title, verse, ref, accent):
    c.setStrokeColor(accent)
    c.setLineWidth(3)
    c.line(54, H - 50, W - 54, H - 50)
    ctext(c, 54, H - 42, "BIBLE STORY TIME", BOLD, 11, accent)
    ccenter(c, H - 100, title, BOLD, 26, accent)
    ccenter(c, H - 124, f'"{verse}"', ITAL, 12, INK)
    ccenter(c, H - 140, ref, FONT, 10, SOFT)


def story_text(c, y, lines_text, width=W - 130):
    c.setFillColor(INK)
    c.setFont(FONT, 11.5)
    for line in simpleSplit(lines_text, FONT, 11.5, width):
        c.drawString(65, y, line)
        y -= 16
    return y


def questions(c, y, qs, accent):
    ctext(c, 65, y, "Let's talk about it:", BOLD, 12, accent)
    y -= 20
    c.setFillColor(INK)
    c.setFont(FONT, 11)
    for q in qs:
        c.circle(72, y + 3.5, 2.5, stroke=0, fill=1)
        c.drawString(82, y, q)
        y -= 18
    return y


# --- simple vector art helpers ---
def draw_sun(c, x, y, r, color=GOLD):
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.setDash([])
    c.circle(x, y, r)
    import math
    for i in range(8):
        a = i * math.pi / 4
        x1 = x + (r + 6) * math.cos(a)
        y1 = y + (r + 6) * math.sin(a)
        x2 = x + (r + 18) * math.cos(a)
        y2 = y + (r + 18) * math.sin(a)
        c.line(x1, y1, x2, y2)


def draw_moon(c, x, y, r, color=BLUE):
    """Crescent moon opening to the right, drawn with two bezier arcs."""
    c.setStrokeColor(color)
    c.setLineWidth(2)
    c.setDash([])
    p = c.beginPath()
    p.moveTo(x + r * 0.3, y + r)
    p.curveTo(x - r * 1.2, y + r * 0.8, x - r * 1.2, y - r * 0.8,
              x + r * 0.3, y - r)
    p.curveTo(x - r * 0.25, y - r * 0.6, x - r * 0.25, y + r * 0.6,
              x + r * 0.3, y + r)
    c.drawPath(p)


def draw_star(c, x, y, r, color=GOLD):
    import math
    c.setStrokeColor(color)
    c.setLineWidth(2)
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.pi / 2 + i * math.pi / 5
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    c.drawPath(p)


def draw_rainbow(c, x, y, r0, colors, band=14):
    c.setDash([])
    for i, col in enumerate(colors):
        c.setStrokeColor(col)
        c.setLineWidth(band - 2)
        p = c.beginPath()
        r = r0 - i * band
        p.arc(x - r, y - r, x + r, y + r, 0, 180)
        c.drawPath(p)


def draw_ark(c, x, y, w, color=HexColor("#8a6d4f")):
    c.setStrokeColor(color)
    c.setLineWidth(2.5)
    c.setDash([])
    h = w * 0.28
    p = c.beginPath()
    p.moveTo(x - w / 2, y + h)
    p.lineTo(x - w / 2 + w * 0.12, y)
    p.lineTo(x + w / 2 - w * 0.12, y)
    p.lineTo(x + w / 2, y + h)
    p.close()
    c.drawPath(p)
    c.rect(x - w * 0.22, y + h, w * 0.44, h * 0.8)
    c.rect(x - w * 0.10, y + h * 1.25, w * 0.20, h * 0.55)
    # waves
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    p = c.beginPath()
    for i in range(6):
        wx = x - w / 2 - 20 + i * (w + 40) / 6
        p.moveTo(wx, y - 12)
        p.curveTo(wx + 8, y - 4, wx + 16, y - 4, wx + 24, y - 12)
    c.drawPath(p)


def draw_fish(c, x, y, w, color=BLUE):
    c.setStrokeColor(color)
    c.setLineWidth(2.5)
    c.setDash([])
    h = w * 0.45
    c.ellipse(x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    # tail
    p = c.beginPath()
    p.moveTo(x + w / 2 - 4, y)
    p.lineTo(x + w / 2 + w * 0.22, y + h * 0.4)
    p.lineTo(x + w / 2 + w * 0.22, y - h * 0.4)
    p.close()
    c.drawPath(p)
    # eye + smile
    c.circle(x - w * 0.28, y + h * 0.12, max(3, w * 0.03))
    p = c.beginPath()
    p.arc(x - w * 0.42, y - h * 0.25, x - w * 0.18, y + h * 0.05, 200, 120)
    c.drawPath(p)


def draw_sheep(c, x, y, w, color=INK):
    """Cloud-body sheep from overlapping circles."""
    import math
    c.setStrokeColor(color)
    c.setLineWidth(2.2)
    c.setDash([])
    body_r = w * 0.32
    for i in range(10):
        a = i * math.pi / 5
        c.circle(x + body_r * math.cos(a), y + body_r * math.sin(a), w * 0.13)
    c.circle(x, y, w * 0.18)
    c.circle(x - w * 0.16, y + w * 0.08, w * 0.12)
    c.circle(x + w * 0.15, y - w * 0.07, w * 0.12)
    # head
    hx, hy = x - w * 0.48, y + w * 0.18
    c.ellipse(hx - w * 0.13, hy - w * 0.16, hx + w * 0.13, hy + w * 0.16)
    c.circle(hx - w * 0.05, hy + w * 0.04, max(2, w * 0.015), stroke=0, fill=1)
    c.circle(hx + w * 0.05, hy + w * 0.04, max(2, w * 0.015), stroke=0, fill=1)
    # ears
    c.ellipse(hx - w * 0.20, hy + w * 0.06, hx - w * 0.10, hy + w * 0.13)
    c.ellipse(hx + w * 0.10, hy + w * 0.06, hx + w * 0.20, hy + w * 0.13)
    # legs
    for lx in (x - w * 0.18, x + w * 0.10):
        c.rect(lx, y - w * 0.32 - w * 0.22, w * 0.06, w * 0.22)


RAINBOW = [HexColor("#d66a6a"), HexColor("#dd9f5a"), HexColor("#d9c35e"),
           HexColor("#7a9e7e"), HexColor("#5b8db8"), HexColor("#8a7ab8")]


def bible_sheets(path):
    c = canvas.Canvas(path, pagesize=letter)

    # ---------------- 1. Creation — big kid
    story_header(c, "God Made Everything",
                 "In the beginning, God created the heavens and the earth.",
                 "Genesis 1:1", GOLD)
    y = story_text(c, H - 175,
        "Long, long ago there was nothing at all — until God spoke! God made light and "
        "dark, the sky and the sea, the sun, moon, and stars, every plant and every "
        "animal. Last of all, God made people, and He said it was very good.")
    y = questions(c, y - 14, [
        "What is your favorite thing God made?",
        "God made YOU! What is something special about you?",
        "What can we say thank You to God for today?"], GOLD)
    ctext(c, 65, y - 8, "Color what God made:", BOLD, 12, GOLD)
    draw_sun(c, 140, y - 85, 36)
    draw_moon(c, 300, y - 85, 38)
    draw_star(c, 440, y - 85, 38)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.setDash([])
    c.roundRect(54, 70, W - 108, y - 240, 10)
    ctext(c, 66, y - 192, "Draw your favorite thing God made:", BOLD, 11, GOLD)
    c.showPage()

    # ---------------- 1b. Creation — toddler
    story_header(c, "God Made Everything", "God made it all!", "Genesis 1", GOLD)
    ccenter(c, H - 170, "Color the sun, the moon, and the stars!", BOLD, 13, INK)
    draw_sun(c, W / 2, H - 320, 95)
    draw_moon(c, 170, 300, 75)
    draw_star(c, 440, 320, 85)
    draw_star(c, 350, 160, 45)
    draw_star(c, 150, 130, 35)
    ccenter(c, 60, "Say it together:  \"Thank You, God!\"", ITAL, 12, SOFT)
    c.showPage()

    # ---------------- 2. Noah — big kid
    story_header(c, "Noah and the Big Boat",
                 "I have set my rainbow in the clouds.", "Genesis 9:13", BLUE)
    y = story_text(c, H - 175,
        "God told Noah to build a big boat called an ark. Noah obeyed! The animals came "
        "two by two, the rain fell for forty days, and God kept everyone in the ark "
        "safe. Then God put a rainbow in the sky as His promise.")
    y = questions(c, y - 14, [
        "How did Noah show he trusted God?",
        "How many of each animal came? (Count: one... two!)",
        "What does the rainbow help us remember?"], BLUE)
    ctext(c, 65, y - 8, "Color the rainbow and the ark. Circle the pairs!", BOLD, 12, BLUE)
    draw_rainbow(c, 190, y - 160, 105, RAINBOW)
    draw_ark(c, 430, y - 160, 150)
    # pairs to circle
    for i, (fn, args) in enumerate([(draw_star, 26), (draw_star, 26)]):
        fn(c, 120 + i * 46, 105, args)
    draw_sun(c, 280, 105, 18)
    draw_sun(c, 336, 105, 18)
    draw_moon(c, 460, 105, 20)
    draw_moon(c, 512, 105, 20)
    ctext(c, 65, 62, "Trace the number of each animal:  ", BOLD, 11, BLUE)
    stroke_letter(c, 250, 52, "2  2  2", 34)
    c.showPage()

    # ---------------- 2b. Noah — toddler
    story_header(c, "Noah and the Big Boat", "God keeps His promises!",
                 "Genesis 6–9", BLUE)
    ccenter(c, H - 170, "Color the big rainbow and Noah's boat!", BOLD, 13, INK)
    draw_rainbow(c, W / 2, H - 430, 200, RAINBOW, band=24)
    draw_ark(c, W / 2, 150, 260)
    ccenter(c, 60, "Craft idea: glue cotton-ball clouds under the rainbow!", ITAL, 12, SOFT)
    c.showPage()

    # ---------------- 3. Jonah — big kid
    story_header(c, "Jonah and the Big Fish",
                 "I called to the Lord, and He answered me.", "Jonah 2:2", GREEN)
    y = story_text(c, H - 175,
        "God asked Jonah to go to Nineveh, but Jonah ran away on a boat instead. A storm "
        "came, Jonah went into the sea, and a big fish swallowed him up! Inside the fish "
        "Jonah prayed, and God gave him a second chance. This time, Jonah obeyed.")
    y = questions(c, y - 14, [
        "Where did Jonah pray? Can we pray anywhere?",
        "Did God stop loving Jonah when he ran away?",
        "Is there something hard God wants us to obey?"], GREEN)
    ctext(c, 65, y - 8, "Color the big fish, then trace the wavy sea:", BOLD, 12, GREEN)
    draw_fish(c, W / 2 - 30, y - 120, 240)
    # wavy trace line
    c.setStrokeColor(TRACE)
    c.setLineWidth(1.5)
    c.setDash([4, 3])
    p = c.beginPath()
    xx = 70
    p.moveTo(xx, 100)
    while xx < W - 90:
        p.curveTo(xx + 15, 118, xx + 30, 118, xx + 45, 100)
        p.curveTo(xx + 60, 82, xx + 75, 82, xx + 90, 100)
        xx += 90
    c.drawPath(p)
    c.setDash([])
    c.showPage()

    # ---------------- 3b. Jonah — toddler
    story_header(c, "Jonah and the Big Fish", "God hears us when we pray!",
                 "Jonah 2:2", GREEN)
    ccenter(c, H - 170, "Color the great big fish!", BOLD, 13, INK)
    draw_fish(c, W / 2 - 30, H - 400, 400)
    c.setStrokeColor(BLUE)
    c.setLineWidth(3)
    p = c.beginPath()
    xx = 60
    p.moveTo(xx, 150)
    while xx < W - 110:
        p.curveTo(xx + 20, 172, xx + 40, 172, xx + 60, 150)
        p.curveTo(xx + 80, 128, xx + 100, 128, xx + 120, 150)
        xx += 120
    c.drawPath(p)
    ccenter(c, 60, "Craft idea: glue on tissue-paper waves!", ITAL, 12, SOFT)
    c.showPage()

    # ---------------- 4. Lost sheep — big kid
    story_header(c, "The Lost Sheep", "The Lord is my shepherd.", "Psalm 23:1  •  Luke 15",
                 ROSE)
    y = story_text(c, H - 175,
        "Jesus told a story about a shepherd with one hundred sheep. One little sheep "
        "wandered off and got lost! The shepherd left the ninety-nine and searched until "
        "he found it, then carried it home rejoicing. Jesus loves each of us like that.")
    y = questions(c, y - 14, [
        "How do you think the lost sheep felt? And when it was found?",
        "Who takes care of us the way the shepherd cares for sheep?",
        "Does Jesus ever stop looking for the one who is lost?"], ROSE)
    ctext(c, 65, y - 8, "Count the sheep, color them, and trace the number:", BOLD, 12, ROSE)
    for i in range(5):
        draw_sheep(c, 105 + i * 108, y - 100, 62)
    ctext(c, W / 2 - 90, y - 245, "How many sheep?", FONT, 12, SOFT)
    stroke_letter(c, W / 2 + 20, y - 255, "5", 60)
    ctext(c, 66, 80, "Craft idea: glue a cotton ball onto each sheep!", ITAL, 11, SOFT)
    c.showPage()

    # ---------------- 4b. Lost sheep — toddler
    story_header(c, "The Lost Sheep", "Jesus loves ME!", "Luke 15", ROSE)
    ccenter(c, H - 170, "Glue cotton balls on the sheep to make it woolly!", BOLD, 13, INK)
    draw_sheep(c, W / 2 + 40, H - 420, 300)
    ccenter(c, 70, "While you glue, say:  \"Jesus loves me!\"", ITAL, 12, SOFT)
    c.showPage()

    c.save()


# ------------------------------------------------------------------- main
def main():
    low = os.path.join(OUT, "letter-of-the-week")
    bib = os.path.join(OUT, "bible-stories")
    os.makedirs(low, exist_ok=True)
    os.makedirs(bib, exist_ok=True)

    c = canvas.Canvas(os.path.join(low, "big-kid-tracing-pages-A-Z.pdf"), pagesize=letter)
    for ch in string.ascii_uppercase:
        big_kid_page(c, ch)
    c.save()

    c = canvas.Canvas(os.path.join(low, "toddler-pages-A-Z.pdf"), pagesize=letter)
    for ch in string.ascii_uppercase:
        toddler_page(c, ch)
    c.save()

    rhythm_chart(os.path.join(OUT, "weekly-rhythm-chart.pdf"))
    bible_sheets(os.path.join(bib, "bible-story-activity-sheets.pdf"))
    print("done")


if __name__ == "__main__":
    main()
