#!/usr/bin/env python3
"""Deterministic Pillow generator for news-image-20261123.

Draws a 1024x1024 PNG poster summarising 23 November 2026 world news.
PIL is imported inside build() so importing this module needs no third party.
"""
from __future__ import annotations

import os

# Palette
NAVY = "#0B1220"
CARD = "#151F33"
RULE = "#2A3A57"
BODY = "#D7DEEA"
WHITE = "#FFFFFF"
AMBER = "#F2B33D"
TEAL = "#4FD1C5"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1024, 1024
MARGIN = 36
RIGHT = W - MARGIN


def build(out_path: str | None = None) -> str:
    from PIL import Image, ImageDraw, ImageFont

    if out_path is None:
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render.png")

    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Fonts
    fb76 = ImageFont.truetype(FONT_BOLD, 76)
    fb52 = ImageFont.truetype(FONT_BOLD, 52)
    fb34 = ImageFont.truetype(FONT_BOLD, 34)
    fb26 = ImageFont.truetype(FONT_BOLD, 26)
    fb24 = ImageFont.truetype(FONT_BOLD, 24)
    fb20 = ImageFont.truetype(FONT_BOLD, 20)
    fr24 = ImageFont.truetype(FONT_REG, 24)
    fr22 = ImageFont.truetype(FONT_REG, 22)
    fr21 = ImageFont.truetype(FONT_REG, 21)

    # --- helpers ---
    def tw(text, font):
        return d.textlength(text, font=font)

    def fit_font(text, font_path, size, max_w, min_size=20):
        while size >= min_size:
            f = ImageFont.truetype(font_path, size)
            if tw(text, f) <= max_w:
                return f
            size -= 1
        return ImageFont.truetype(font_path, min_size)

    def draw_text(x, y, text, font, fill):
        d.text((x, y), text, font=font, fill=fill)
        bbox = d.textbbox((x, y), text, font=font)
        return bbox  # (x0,y0,x1,y1)

    def wrap_lines(text, font, max_w):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if cur and tw(trial, font) > max_w:
                lines.append(cur)
                cur = w
            else:
                cur = trial
        if cur:
            lines.append(cur)
        # if any single word still overflows, shrink font is caller's job; ensure we return lines
        return lines

    boxes = []  # collect all text boxes for overlap check

    def record_box(box):
        boxes.append(box)
        return box

    # ---------- HEADER ----------
    # "WORLD NEWS" small amber caps, letter-spaced ~26px
    wn = "WORLD NEWS"
    x = MARGIN
    y = 22
    spacing = 3
    for ch in wn:
        if ch == " ":
            x += 10
            continue
        b = draw_text(x, y, ch, fb26, AMBER)
        record_box(b)
        x = b[2] + spacing

    # Date - most legible thing
    date_text = "23 NOVEMBER 2026"
    date_font = fit_font(date_text, FONT_BOLD, 76, RIGHT - MARGIN, min_size=48)
    b = draw_text(MARGIN, 58, date_text, date_font, WHITE)
    record_box(b)

    # thin amber rule
    rule_y = 142
    d.line([(MARGIN, rule_y), (RIGHT, rule_y)], fill=AMBER, width=2)

    # ---------- LEAD CARD ----------
    lead_top = 160
    lead_bottom = 468
    lead_left = MARGIN
    lead_right = RIGHT
    d.rectangle([lead_left, lead_top, lead_right, lead_bottom], fill=CARD, outline=RULE, width=1)

    # chip
    chip = "GLOBAL  ·  COP31, ANTALYA"
    chip_font = fit_font(chip, FONT_BOLD, 24, (lead_right - lead_left) - 320, min_size=20)
    b = draw_text(lead_left + 20, lead_top + 16, chip, chip_font, AMBER)
    record_box(b)

    # headline - 3 lines, ~52px bold white, left side leaving room for pictogram
    headline_max_w = lead_right - lead_left - 340
    hl_lines = [
        "CLIMATE SUMMIT ENDS",
        "WITH NO DEAL AS FOSSIL",
        "FUEL FIGHT SINKS IT",
    ]
    hy = lead_top + 52
    hl_font = fb52
    # ensure each line fits
    for line in hl_lines:
        hl_font_candidate = fit_font(line, FONT_BOLD, 52, headline_max_w, min_size=34)
        if hl_font_candidate.size < hl_font.size:
            hl_font = hl_font_candidate
    for line in hl_lines:
        b = draw_text(lead_left + 20, hy, line, hl_font, WHITE)
        record_box(b)
        hy += hl_font.size + 8

    # body line
    body = "COP31 closes two days into overtime with no cover decision; the EU rejected the final text."
    body_max_w = lead_right - lead_left - 340
    body_font = fr24
    body_lines = wrap_lines(body, body_font, body_max_w)
    by = hy + 8
    for bl in body_lines[:2]:
        b = draw_text(lead_left + 20, by, bl, body_font, BODY)
        record_box(b)
        by += body_font.size + 6

    # pictogram: two smokestacks with rising arrow, right side ~290px wide
    pic_x = lead_right - 280
    pic_y = lead_top + 70
    pic_w = 250
    pic_h = 200
    # smokestack 1
    s1x = pic_x + 40
    s_base = pic_y + pic_h - 20
    s_top = pic_y + 50
    d.rectangle([s1x, s_top, s1x + 52, s_base], outline=BODY, width=3)
    # smoke puff
    d.arc([s1x - 10, s_top - 35, s1x + 30, s_top + 5], 200, 340, fill=RULE, width=2)
    # smokestack 2
    s2x = s1x + 80
    d.rectangle([s2x, s_top + 20, s2x + 52, s_base], outline=BODY, width=3)
    d.arc([s2x - 10, s_top - 15, s2x + 30, s_top + 25], 200, 340, fill=RULE, width=2)
    # rising arrow (fossil fuel fight / rising emissions)
    ax = pic_x + 190
    d.line([(ax, s_base), (ax, pic_y + 30)], fill=AMBER, width=5)
    d.polygon([(ax, pic_y + 18), (ax - 14, pic_y + 45), (ax + 14, pic_y + 45)], fill=AMBER)
    # ground line
    d.line([(pic_x + 20, s_base), (pic_x + pic_w - 10, s_base)], fill=RULE, width=2)

    # ---------- 2x2 GRID ----------
    grid_top = 488
    gutter = 20
    card_w = (RIGHT - MARGIN - gutter) // 2
    card_h = 210

    cards = [
        {
            "chip": "EUROPE  ·  KYIV REGION",
            "hl": ["DRONE KILLS NINE", "NEAR KYIV"],
            "body": "186 drones launched overnight; Polish sites hold Kh-101 missile debris.",
            "icon": "drone",
        },
        {
            "chip": "BUSINESS  ·  SEOUL",
            "hl": ["ASIA STOCKS SLIDE", "ON AI FEARS"],
            "body": "KOSPI -2.8% to a 10-month low; Anthropic falls 9% after its $81.3bn IPO.",
            "icon": "chart",
        },
        {
            "chip": "AMERICAS  ·  CALIFORNIA",
            "hl": ["NINE SHOT AT", "A CONCERT"],
            "body": "One in critical condition; Delta's outage delays Thanksgiving flights.",
            "icon": "burst",
        },
        {
            "chip": "AFRICA  ·  CONGO",
            "hl": ["FIGHTING STALLS", "EBOLA RESPONSE"],
            "body": "11,613 cases and 5,678 deaths; South Sudan attack kills 24.",
            "icon": "virus",
        },
    ]

    def draw_icon(kind, ix, iy, sz):
        # ix,iy is top-left of icon area
        cx, cy = ix + sz // 2, iy + sz // 2
        if kind == "drone":
            # body
            d.ellipse([cx - 10, cy - 6, cx + 10, cy + 6], outline=TEAL, width=2)
            # arms
            d.line([(cx - 20, cy - 10), (cx + 20, cy - 10)], fill=TEAL, width=2)
            d.line([(cx - 20, cy + 10), (cx + 20, cy + 10)], fill=TEAL, width=2)
            # rotors
            for rx in (cx - 20, cx + 20):
                for ry in (cy - 10, cy + 10):
                    d.ellipse([rx - 5, ry - 2, rx + 5, ry + 2], outline=TEAL, width=1)
            # falling shell
            d.line([(cx + 4, cy + 8), (cx + 10, cy + 24)], fill=AMBER, width=2)
            d.polygon([(cx + 10, cy + 24), (cx + 6, cy + 20), (cx + 14, cy + 20)], fill=AMBER)
        elif kind == "chart":
            # axes
            d.line([(ix + 6, iy + sz - 6), (ix + 6, iy + 6)], fill=TEAL, width=2)
            d.line([(ix + 6, iy + sz - 6), (ix + sz - 6, iy + sz - 6)], fill=TEAL, width=2)
            # falling candlestick arrow
            pts = [(ix + 10, iy + 12), (ix + 20, iy + 18), (ix + 28, iy + 14), (ix + 40, iy + 30)]
            for i in range(len(pts) - 1):
                d.line([pts[i], pts[i + 1]], fill=AMBER, width=2)
            d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 6, pts[-1][1] - 4), (pts[-1][0] - 2, pts[-1][1] - 8)], fill=AMBER)
        elif kind == "burst":
            # crowd line
            d.line([(ix + 4, iy + sz - 10), (ix + sz - 4, iy + sz - 10)], fill=TEAL, width=2)
            for px in (ix + 12, ix + 22, ix + 32):
                d.ellipse([px - 3, iy + sz - 18, px + 3, iy + sz - 12], outline=TEAL, width=1)
            # burst
            bc = (ix + sz - 14, iy + 16)
            for ang in range(0, 360, 45):
                import math
                r1, r2 = 4, 11
                x1 = bc[0] + int(r1 * math.cos(math.radians(ang)))
                y1 = bc[1] + int(r1 * math.sin(math.radians(ang)))
                x2 = bc[0] + int(r2 * math.cos(math.radians(ang)))
                y2 = bc[1] + int(r2 * math.sin(math.radians(ang)))
                d.line([(x1, y1), (x2, y2)], fill=AMBER, width=2)
        elif kind == "virus":
            d.ellipse([ix + 10, iy + 10, ix + sz - 10, iy + sz - 10], outline=TEAL, width=2)
            vc = (ix + sz // 2, iy + sz // 2)
            for ang in range(0, 360, 45):
                import math
                r1, r2 = (sz // 2 - 10), (sz // 2 - 2)
                x1 = vc[0] + int(r1 * math.cos(math.radians(ang)))
                y1 = vc[1] + int(r1 * math.sin(math.radians(ang)))
                x2 = vc[0] + int(r2 * math.cos(math.radians(ang)))
                y2 = vc[1] + int(r2 * math.sin(math.radians(ang)))
                d.line([(x1, y1), (x2, y2)], fill=TEAL, width=2)

    for i, card in enumerate(cards):
        row, col = divmod(i, 2)
        cx = MARGIN + col * (card_w + gutter)
        cy = grid_top + row * (card_h + gutter)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=CARD, outline=RULE, width=1)

        # chip
        chip_font = fit_font(card["chip"], FONT_BOLD, 20, card_w - 70, min_size=20)
        b = draw_text(cx + 14, cy + 12, card["chip"], chip_font, TEAL)
        record_box(b)

        # icon top-right
        icon_sz = 52
        draw_icon(card["icon"], cx + card_w - icon_sz - 10, cy + 8, icon_sz)

        # headline
        hy2 = cy + 42
        hl_f = fb34
        for line in card["hl"]:
            cand = fit_font(line, FONT_BOLD, 34, card_w - 28, min_size=24)
            if cand.size < hl_f.size:
                hl_f = cand
        for line in card["hl"]:
            b = draw_text(cx + 14, hy2, line, hl_f, WHITE)
            record_box(b)
            hy2 += hl_f.size + 4

        # body
        bf = fr21
        body_lines = wrap_lines(card["body"], bf, card_w - 28)
        by2 = hy2 + 6
        for bl in body_lines[:2]:
            # shrink if needed
            blf = fit_font(bl, FONT_REG, 21, card_w - 28, min_size=20)
            b = draw_text(cx + 14, by2, bl, blf, BODY)
            record_box(b)
            by2 += blf.size + 3

    # ---------- BOTTOM STRIP ----------
    strip_y = H - 58
    d.line([(MARGIN, strip_y - 10), (RIGHT, strip_y - 10)], fill=RULE, width=1)
    also = "ALSO TODAY"
    also_font = fb20
    b = draw_text(MARGIN, strip_y, also, also_font, AMBER)
    record_box(b)
    rest = "  Houthis hit Rabigh refinery · Hasina appeal stuck a year on · red fire ants found in Sydney"
    rest_x = b[2] + 6
    rest_max = RIGHT - rest_x
    rest_font = fit_font(rest.strip(), FONT_REG, 22, rest_max, min_size=20)
    # If still too wide at min size, wrap to two lines
    rest_text = rest.strip()
    if tw(rest_text, rest_font) > rest_max:
        # split into two lines
        words = rest_text.split(" · ")
        line1 = " · ".join(words[:2]) + " ·"
        line2 = words[2] if len(words) > 2 else ""
        f1 = fit_font(line1, FONT_REG, 20, rest_max, min_size=20)
        f2 = fit_font(line2, FONT_REG, 20, rest_max, min_size=20)
        b = draw_text(rest_x, strip_y - 2, line1, f1, "#9AA7BD")
        record_box(b)
        b = draw_text(rest_x, strip_y + f1.size + 2, line2, f2, "#9AA7BD")
        record_box(b)
    else:
        b = draw_text(rest_x, strip_y + (also_font.size - rest_font.size) // 2, rest_text, rest_font, "#9AA7BD")
        record_box(b)

    # ---------- VALIDATION ----------
    # No text under 20px - fonts were constructed with min_size>=20
    # Check no overflow beyond canvas
    for (x0, y0, x1, y1) in boxes:
        assert x0 >= 0 and y0 >= 0, f"text box out of bounds: {(x0,y0,x1,y1)}"
        assert x1 <= W + 2, f"text overflows right: {x1} > {W}"
        assert y1 <= H + 2, f"text overflows bottom: {y1} > {H}"

    # Overlap check: text boxes should not overlap in a way that makes them unreadable.
    # Allow small vertical adjacency but flag large area intersections.
    def _inter_area(a, b):
        ix0, iy0 = max(a[0], b[0]), max(a[1], b[1])
        ix1, iy1 = min(a[2], b[2]), min(a[3], b[3])
        if ix1 <= ix0 or iy1 <= iy0:
            return 0
        return (ix1 - ix0) * (iy1 - iy0)

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            area = _inter_area(boxes[i], boxes[j])
            # allow tiny overlaps from text metrics; flag significant ones
            if area > 200:
                raise AssertionError(f"text boxes overlap too much: {boxes[i]} vs {boxes[j]} area={area}")

    img.save(out_path, format="PNG", optimize=True)
    size = os.path.getsize(out_path)
    assert size <= 1048576, f"render.png too large: {size} bytes"
    return out_path


if __name__ == "__main__":
    p = build()
    size = os.path.getsize(p)
    from PIL import Image
    with Image.open(p) as im:
        print(f"{im.size[0]}x{im.size[1]} {im.mode} {size} bytes")
    print(f"OK {p}")