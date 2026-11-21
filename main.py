#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Saturday 21 November 2026.

A code-drawn 1024x1024 newspaper front-page infographic summing up the
day's world news. No network access, no randomness, no clock reads: the
same run always produces the same bytes.

Every story was verified on 21 November 2026 against at least two
independent news sources (Reuters, AP, CNN, Al Jazeera, The Wall Street
Journal, India Meteorological Department, GFZ). Events are labelled with
the day they happened where that matters ("on Friday" = 20 November);
this is a Saturday paper, so Friday's news is today's news.

Stories carried:
  * Russian missiles land in Poland (AP, Reuters, BBC, Tribune)
  * AI rout: Anthropic -8.5%, Nasdaq -5.3% (WSJ, CNN)
  * COP31 climate talks into overtime, draft drops fossil fuels
    (Al Jazeera, Reuters, Straits Times)
  * Cyclone Akvan crosses the Odisha coast near Gopalpur
    (Times of India, New Indian Express, The Statesman, IMD)
  * Denmark expels Russia's defence attache over a foiled plot to
    kill rapper Kyivstoner (Al Jazeera, Reuters, WSJ, CNN)
  * Bolsonaro taken to hospital in Brasilia (Reuters, CNN,
    Straits Times)
  * Magnitude 6.8 earthquake shakes central Peru (Reuters, GFZ,
    Xinhua/Bernama)

Usage: python3 main.py [output_path]   (default: /output/entry.png)
Requires: Pillow (PIL) and DejaVu fonts (standard on most Linux systems).
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
INK = (26, 26, 26)
PAPER = (248, 244, 233)
RED = (179, 38, 30)
NAVY = (31, 58, 95)
GREY = (90, 86, 76)
LIGHT_RULE = (200, 192, 172)

FONT_PATHS = {
    "serif_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
}

_cache = {}


def font(kind, size):
    """Load a truetype font, falling back to PIL's built-in bitmap font."""
    key = (kind, size)
    if key in _cache:
        return _cache[key]
    for path in FONT_PATHS[kind]:
        if os.path.exists(path):
            f = ImageFont.truetype(path, size)
            _cache[key] = f
            return f
    f = ImageFont.load_default()
    _cache[key] = f
    return f


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill, spacing=None):
    """Draw wrapped text; returns the y just below the last line."""
    if spacing is None:
        spacing = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += spacing
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, size=15):
    fnt = font("sans_bold", size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 8


# ---------------------------------------------------------------- pictures

def draw_lead_picture(draw, x, y, w, h):
    """Night sky over the Polish border: missile trail, impact burst."""
    sky = (22, 35, 63)
    draw.rectangle([x, y, x + w, y + h], fill=sky)
    # Fixed stars (deterministic positions).
    stars = [(18, 14), (52, 40), (96, 10), (150, 34), (210, 12), (262, 44),
             (330, 16), (388, 38), (440, 12), (500, 30), (548, 10),
             (70, 62), (300, 66), (470, 58), (580, 44)]
    for sx, sy in stars:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                     fill=(240, 240, 220))
    # Moon removed: it overlapped the UKRAINE label.
    # Dashed border between Poland (left) and Ukraine (right).
    bx = x + 330
    for yy in range(y + 8, y + h - 46, 12):
        draw.line([(bx, yy), (bx, yy + 7)], fill=(255, 255, 255), width=2)
    lab = font("sans_bold", 16)
    draw.text((x + 16, y + 10), "POLAND", font=lab, fill=(255, 255, 255))
    draw.text((x + w - 108, y + 10), "UKRAINE", font=lab, fill=(255, 255, 255))
    # Missile trail: fixed quadratic-bezier dots from Ukraine to Poland.
    p0 = (x + w - 40, y + 52)
    p1 = (x + 380, y + 8)
    p2 = (x + 168, y + 108)
    for i in range(15):
        t = i / 14.0
        px = int((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0])
        py = int((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
        r = 4 if i % 3 == 0 else 2
        draw.ellipse([px - r, py - r, px + r, py + r], fill=(245, 166, 38))
    # Impact burst at Nowy Lipowiec.
    cx, cy = x + 168, y + 108
    spikes = []
    for i in range(24):
        ang = 3.141592653589793 * 2 * i / 24
        r = 36 if i % 2 == 0 else 15
        spikes.append((cx + r * _cos(ang), cy + r * _sin(ang)))
    draw.polygon(spikes, fill=(245, 166, 38), outline=(211, 84, 0))
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 224, 138))
    # Ground silhouette with pines.
    gy = y + h - 34
    draw.rectangle([x, gy, x + w, y + h], fill=(13, 21, 38))
    for tx in (40, 90, 250, 300, 420, 480, 560):
        draw.polygon([(x + tx, gy), (x + tx - 12, gy + 26),
                      (x + tx + 12, gy + 26)], fill=(13, 21, 38),
                     outline=(52, 74, 52))
    small = font("sans_bold", 12)
    draw.text((x + 212, y + 120), "Nowy Lipowiec", font=small,
              fill=(255, 255, 255))


def _cos(a):
    import math
    return math.cos(a)


def _sin(a):
    import math
    return math.sin(a)


def draw_chart(draw, x, y, w, h):
    """Three red bars: Anthropic, Nasdaq, S&P 500 Friday falls."""
    values = [("ANTHROPIC", "8.5%", 8.5), ("NASDAQ", "5.3%", 5.3),
              ("S&P 500", "3.7%", 3.7)]
    base = y + h - 20
    bw = 84
    gap = (w - 3 * bw) // 4
    val_fnt = font("sans_bold", 15)
    name_fnt = font("sans_bold", 11)
    for i, (name, pct, val) in enumerate(values):
        bx = x + gap + i * (bw + gap)
        bh = int(val / 8.5 * (h - 44))
        draw.rectangle([bx, base - bh, bx + bw, base], fill=RED)
        tw = text_w(draw, "-" + pct, val_fnt)
        draw.text((bx + (bw - tw) / 2, base - bh - 22), "-" + pct,
                  font=val_fnt, fill=RED)
        nw = text_w(draw, name, name_fnt)
        draw.text((bx + (bw - nw) / 2, base + 4), name, font=name_fnt, fill=INK)
    rule(draw, x, base, x + w, width=2)


def draw_clock(draw, cx, cy, r):
    """A clock past midnight: the talks have run into overtime."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=INK, width=3)
    for ang, ln in ((0, 8), (90, 8), (180, 8), (270, 8)):
        import math
        a = math.radians(ang)
        x1 = cx + (r - ln) * math.sin(a)
        y1 = cy - (r - ln) * math.cos(a)
        x2 = cx + r * math.sin(a)
        y2 = cy - r * math.cos(a)
        draw.line([(x1, y1), (x2, y2)], fill=INK, width=3)
    # Hour hand just past 12, minute hand on 1: 00:05, past the deadline.
    import math
    hx = cx + 0.45 * r * math.sin(math.radians(2))
    hy = cy - 0.45 * r * math.cos(math.radians(2))
    draw.line([(cx, cy), (hx, hy)], fill=INK, width=4)
    mx = cx + 0.8 * r * math.sin(math.radians(30))
    my = cy - 0.8 * r * math.cos(math.radians(30))
    draw.line([(cx, cy), (mx, my)], fill=RED, width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)
    tag = font("sans_bold", 12)
    tw = text_w(draw, "OVERTIME", tag)
    draw.text((cx - tw / 2, cy + r + 6), "OVERTIME", font=tag, fill=RED)


def draw_spiral(draw, x, y, size):
    """Cyclone spiral with rain slashes."""
    cx, cy = x + size // 2, y + size // 2
    col = (31, 90, 140)
    for i, r in enumerate((8, 14, 20, 26, 32)):
        draw.arc([cx - r, cy - r, cx + r, cy + r],
                 start=i * 40, end=i * 40 + 300, fill=col, width=3)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col)
    for rx, ry in ((4, 62), (22, 70), (44, 66), (58, 74), (12, 78), (34, 80)):
        draw.line([(x + rx, y + ry), (x + rx - 5, y + ry + 12)],
                  fill=(90, 130, 180), width=2)


def draw_denmark_flag(draw, x, y, w, h):
    """Danish flag. (The seven-day deadline is in the story text.)"""
    draw.rectangle([x, y, x + w, y + h], fill=(198, 12, 48))
    draw.rectangle([x + 18, y, x + 26, y + h], fill=(255, 255, 255))
    draw.rectangle([x, y + h // 2 - 4, x + w, y + h // 2 + 4],
                   fill=(255, 255, 255))


def draw_hospital(draw, x, y, w, h):
    """Hospital building with a green cross."""
    draw.rectangle([x + 6, y, x + w - 6, y + h], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.rectangle([x + 6, y, x + w - 6, y + 16], fill=(26, 122, 58))
    cx = x + w // 2
    cy = y + h // 2 + 4
    draw.rectangle([cx - 5, cy - 16, cx + 5, cy + 16], fill=(26, 122, 58))
    draw.rectangle([cx - 16, cy - 5, cx + 16, cy + 5], fill=(26, 122, 58))
    draw.rectangle([x + w // 2 - 8, y + h - 18, x + w // 2 + 8, y + h],
                   fill=INK)


# ---------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # Double border.
    draw.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    draw.rectangle([20, 20, W - 20, H - 20], outline=INK, width=1)

    # ---- Masthead ------------------------------------------------------
    name = font("serif_bold", 62)
    tw = text_w(draw, "THE WORLD TODAY", name)
    draw.text(((W - tw) / 2, 30), "THE WORLD TODAY", font=name, fill=INK)
    rule(draw, MARGIN, 104, W - MARGIN, width=3)
    date_fnt = font("sans_bold", 30)
    date = "SATURDAY 21 NOVEMBER 2026"
    tw = text_w(draw, date, date_fnt)
    draw.text(((W - tw) / 2, 114), date, font=date_fnt, fill=INK)
    deck = font("sans", 16)
    deck_text = "The world in one page \u2014 every story verified from today\u2019s wires"
    tw = text_w(draw, deck_text, deck)
    draw.text(((W - tw) / 2, 152), deck_text, font=deck, fill=GREY)
    rule(draw, MARGIN, 176, W - MARGIN, width=2)

    # ---- Lead story: Poland --------------------------------------------
    y = 188
    y = kicker(draw, MARGIN, y, "EUROPE \u00b7 WAR IN UKRAINE")
    head = font("serif_bold", 44)
    draw.text((MARGIN, y), "MISSILES LAND IN POLAND", font=head, fill=INK)
    y = 256
    y = draw_wrapped(
        draw, MARGIN, y,
        "Warsaw calls it a likely deliberate provocation as Russian weapons "
        "fall on NATO soil during a major overnight strike on Ukraine.",
        font("sans", 16), W - 2 * MARGIN, GREY)
    pic_y = 302
    draw_lead_picture(draw, MARGIN, pic_y, 612, 176)
    body_x = MARGIN + 612 + 16
    draw_wrapped(
        draw, body_x, pic_y,
        "A Russian Kh-101 cruise missile came down near Nowy Lipowiec, "
        "about 50 km from the Ukrainian border, early on Friday. A second "
        "suspected missile and a jet-powered drone hit two other sites. "
        "No one was hurt. NATO called it a grave violation of Polish "
        "airspace.",
        font("sans", 15), W - MARGIN - body_x, INK)
    rule(draw, MARGIN, 494, W - MARGIN, width=2)

    # ---- Row 2: markets + climate --------------------------------------
    col_w = 472
    y0 = 508
    # Markets (left).
    y = kicker(draw, MARGIN, y0, "MARKETS")
    draw.text((MARGIN, y), "AI ROUT DEEPENS", font=font("serif_bold", 30),
              fill=INK)
    draw_wrapped(
        draw, MARGIN, 574,
        "Anthropic fell 8.5% to $88.91 on its second day listed. The "
        "Nasdaq fell 5.3%, wiping out its gains for 2026.",
        font("sans", 14), col_w, INK)
    draw_chart(draw, MARGIN, 616, col_w, 88)
    # Climate (right).
    rx = W - MARGIN - col_w
    draw.line([(W // 2, y0), (W // 2, 706)], fill=LIGHT_RULE, width=1)
    y = kicker(draw, rx, y0, "CLIMATE \u00b7 ANTALYA")
    draw.text((rx, y), "CLIMATE TALKS RUN OVER",
              font=font("serif_bold", 30), fill=INK)
    draw_wrapped(
        draw, rx, 574,
        "COP31 went into overtime on Friday as nearly 200 nations stayed "
        "deadlocked. The draft deal drops every mention of fossil fuels. "
        "A third draft is due today.",
        font("sans", 14), col_w - 132, INK)
    draw_clock(draw, rx + col_w - 58, 636, 40)
    rule(draw, MARGIN, 714, W - MARGIN, width=2)

    # ---- Row 3: three small stories ------------------------------------
    panels = [
        ("WEATHER \u00b7 INDIA", "AKVAN HITS ODISHA",
         "Cyclone Akvan crossed the coast near Gopalpur on Friday, winds "
         "70\u201380 km/h. No major damage or deaths reported; it has "
         "weakened to a low-pressure area.", "spiral"),
        ("EUROPE \u00b7 ESPIONAGE", "DENMARK EXPELS RUSSIAN ENVOY",
         "Copenhagen ordered Russia\u2019s defence attach\u00e9 out within "
         "seven days over a foiled September plot to kill rapper "
         "Kyivstoner. Two men face formal investigation.", "flag"),
        ("BRAZIL", "BOLSONARO IN HOSPITAL",
         "Brazil\u2019s ex-president, 71, was taken to hospital in "
         "Bras\u00edlia on Friday with a near-complete intestinal "
         "obstruction. Doctors say he is stable.", "hospital"),
    ]
    pw = 308
    gap = (W - 2 * MARGIN - 3 * pw) // 2
    py = 728
    ph = 178
    for i, (kick, headline, body, icon) in enumerate(panels):
        px = MARGIN + i * (pw + gap)
        if i:
            draw.line([(px - gap // 2, py), (px - gap // 2, py + ph)],
                      fill=LIGHT_RULE, width=1)
        # Icon column on the left, text on the right.
        ix, iy = px, py + 34
        if icon == "spiral":
            draw_spiral(draw, ix, iy, 72)
        elif icon == "flag":
            draw_denmark_flag(draw, ix, iy + 4, 64, 44)
        else:
            draw_hospital(draw, ix, iy + 2, 64, 72)
        tx = px + 84
        tw_ = px + pw - tx
        kicker(draw, tx, py + 2, kick, size=12)
        hy = py + 24
        for line in wrap(draw, headline, font("serif_bold", 20), tw_):
            draw.text((tx, hy), line, font=font("serif_bold", 20), fill=INK)
            hy += 25
        draw_wrapped(draw, tx, hy + 4, body, font("sans", 13), tw_, INK)
    rule(draw, MARGIN, 914, W - MARGIN, width=2)

    # ---- Peru strip ------------------------------------------------------
    strip = font("sans_bold", 15)
    draw.text((MARGIN, 926),
              "ALSO:  6.8 QUAKE SHAKES PERU", font=strip, fill=RED)
    draw_wrapped(
        draw, MARGIN, 950,
        "A magnitude 6.8 earthquake struck central Peru; people in Lima "
        "rushed into the streets. No casualties were reported.",
        font("sans", 14), W - 2 * MARGIN, INK)
    rule(draw, MARGIN, 982, W - MARGIN, width=1, fill=LIGHT_RULE)

    # ---- Footer: one centred line (two lines overlapped the border) -----
    foot = font("sans", 11)
    line1 = ("Sources: Reuters \u00b7 AP \u00b7 CNN \u00b7 Al Jazeera \u00b7 "
             "WSJ \u00b7 IMD \u00b7 GFZ \u2014 verified 21 November 2026 "
             "\u00b7 Drawn entirely in code, no photographs.")
    tw = text_w(draw, line1, foot)
    draw.text(((W - tw) / 2, 988), line1, font=foot, fill=GREY)
    return img


def main(argv):
    out = argv[1] if len(argv) > 1 else "/output/entry.png"
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    img = build()
    img.save(out, format="PNG")
    size = os.path.getsize(out)
    print(f"wrote {out} {img.size[0]}x{img.size[1]} {size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
