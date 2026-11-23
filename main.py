#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

PALETTE = {
    "bg": (11, 24, 48),
    "masthead_bg": (17, 34, 64),
    "masthead_text": (245, 245, 240),
    "lead_bg": (176, 28, 36),
    "lead_text": (255, 255, 255),
    "card_bg": (20, 40, 74),
    "card_kicker": (255, 210, 120),
    "card_text": (235, 240, 245),
    "footer_bg": (8, 18, 36),
    "footer_text": (200, 210, 220),
    "rules": [
        (230, 90, 70),
        (80, 170, 255),
        (255, 190, 70),
        (120, 220, 170),
    ],
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
FONT_REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, max_width):
    words = text.split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        candidate = current + " " + word
        if draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    for line in lines:
        assert draw.textlength(line, font=font) <= max_width + 0.01, (line, max_width)
    return lines


def rects_overlap(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return not (ax2 <= bx1 or bx2 <= ax1 or ay2 <= by1 or by2 <= ay1)


def rect_contains(outer, inner):
    ox1, oy1, ox2, oy2 = outer
    ix1, iy1, ix2, iy2 = inner
    return ox1 <= ix1 and oy1 <= iy1 and ix2 <= ox2 and iy2 <= oy2


def assert_no_overlaps(rects):
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            if rect_contains(a, b) or rect_contains(b, a):
                continue
            assert not rects_overlap(a, b), (a, b)


def draw_card(draw, rect, rule_color, kicker, body, fonts, palette, boxes):
    x1, y1, x2, y2 = rect
    boxes.append(rect)
    draw.rectangle(rect, fill=palette["card_bg"])
    rule_h = 8
    rule_rect = (x1, y1, x2, y1 + rule_h)
    draw.rectangle(rule_rect, fill=rule_color)
    boxes.append(rule_rect)

    pad = 24
    text_x = x1 + pad
    max_w = (x2 - x1) - pad * 2
    y = y1 + 28

    kicker_font = fonts["kicker"]
    body_font = fonts["body"]
    kicker_w = draw.textlength(kicker, font=kicker_font)
    assert kicker_w <= max_w
    kicker_h = kicker_font.size + 6
    kicker_box = (text_x, y, text_x + int(kicker_w) + 1, y + kicker_h)
    draw.text((text_x, y), kicker, fill=palette["card_kicker"], font=kicker_font)
    boxes.append(kicker_box)
    y += kicker_h + 14

    lines = wrap_text(draw, body, body_font, max_w)
    assert 2 <= len(lines) <= 3, lines
    line_h = body_font.size + 8
    for line in lines:
        lw = draw.textlength(line, font=body_font)
        assert lw <= max_w
        line_box = (text_x, y, text_x + int(lw) + 1, y + line_h)
        assert line_box[3] <= y2 - 16
        draw.text((text_x, y), line, fill=palette["card_text"], font=body_font)
        boxes.append(line_box)
        y += line_h


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")

    img = Image.new("RGB", (WIDTH, HEIGHT), PALETTE["bg"])
    draw = ImageDraw.Draw(img)

    fonts = {
        "masthead": load_font(FONT_BOLD, 64),
        "lead": load_font(FONT_BOLD, 46),
        "kicker": load_font(FONT_BOLD, 20),
        "body": load_font(FONT_REG, 24),
        "footer": load_font(FONT_REG, 20),
    }

    boxes = []

    masthead_rect = (0, 0, WIDTH, 120)
    draw.rectangle(masthead_rect, fill=PALETTE["masthead_bg"])
    boxes.append(masthead_rect)

    masthead_text = "23 NOVEMBER 2026"
    mt_font = fonts["masthead"]
    mt_w = draw.textlength(masthead_text, font=mt_font)
    mt_h = mt_font.size
    mt_x = (WIDTH - mt_w) / 2
    mt_y = (120 - mt_h) / 2 - 4
    mt_box = (int(mt_x), int(mt_y), int(mt_x + mt_w) + 1, int(mt_y + mt_h + 8))
    assert mt_box[0] >= 20 and mt_box[2] <= WIDTH - 20
    draw.text((mt_x, mt_y), masthead_text, fill=PALETTE["masthead_text"], font=mt_font)
    boxes.append(mt_box)

    footer_rect = (0, HEIGHT - 64, WIDTH, HEIGHT)
    draw.rectangle(footer_rect, fill=PALETTE["footer_bg"])
    boxes.append(footer_rect)

    lead_rect = (0, 120, WIDTH, 360)
    draw.rectangle(lead_rect, fill=PALETTE["lead_bg"])
    boxes.append(lead_rect)

    headline = "COP31 ends with no deal as fossil-fuel fight sinks the final text"
    lead_font = fonts["lead"]
    lead_max_w = WIDTH - 80
    lead_lines = wrap_text(draw, headline, lead_font, lead_max_w)
    assert len(lead_lines) <= 3, lead_lines
    line_h = lead_font.size + 12
    total_h = len(lead_lines) * line_h
    lead_y = 120 + (240 - total_h) / 2 - 4
    for line in lead_lines:
        lw = draw.textlength(line, font=lead_font)
        lx = (WIDTH - lw) / 2
        lbox = (int(lx), int(lead_y), int(lx + lw) + 1, int(lead_y + line_h))
        assert lbox[0] >= 20 and lbox[2] <= WIDTH - 20
        assert lbox[1] >= lead_rect[1] + 10 and lbox[3] <= lead_rect[3] - 10
        draw.text((lx, lead_y), line, fill=PALETTE["lead_text"], font=lead_font)
        boxes.append(lbox)
        lead_y += line_h

    stories = [
        ("KYIV REGION", "Kyiv region: Russian strikes kill 11, a supermarket hit in Vyshneve"),
        ("MARKETS", "Anthropic's record IPO falls 9% as investors question AI spending"),
        ("CALIFORNIA", "Nine shot at a concert in central California; one critical"),
        ("CONGO", "WHO: fighting near Congo's Ebola zone disrupts the response"),
    ]

    grid_top = 380
    grid_bottom = HEIGHT - 84
    gap = 20
    margin = 20
    card_w = (WIDTH - margin * 2 - gap) // 2
    card_h = (grid_bottom - grid_top - gap) // 2
    for idx, (kicker, body) in enumerate(stories):
        row = idx // 2
        col = idx % 2
        x1 = margin + col * (card_w + gap)
        y1 = grid_top + row * (card_h + gap)
        x2 = x1 + card_w
        y2 = y1 + card_h
        draw_card(draw, (x1, y1, x2, y2), PALETTE["rules"][idx], kicker, body, fonts, PALETTE, boxes)

    footer_text = "WORLD NEWS IN ONE IMAGE - sources: wire reports, 23 Nov 2026"
    ft_font = fonts["footer"]
    ft_w = draw.textlength(footer_text, font=ft_font)
    ft_h = ft_font.size
    ft_x = (WIDTH - ft_w) / 2
    ft_y = HEIGHT - 64 + (64 - ft_h) / 2 - 2
    ft_box = (int(ft_x), int(ft_y), int(ft_x + ft_w) + 1, int(ft_y + ft_h + 6))
    assert ft_box[0] >= 20 and ft_box[2] <= WIDTH - 20
    draw.text((ft_x, ft_y), footer_text, fill=PALETTE["footer_text"], font=ft_font)
    boxes.append(ft_box)

    assert_no_overlaps(boxes)

    img.save(out_path, format="PNG", optimize=True)
    size = os.path.getsize(out_path)
    if size >= 1048576:
        raise SystemExit(f"output too large: {size} bytes")
    with Image.open(out_path) as saved:
        dims = saved.size
    if dims != (1024, 1024):
        raise SystemExit(f"wrong dimensions: {dims}")


if __name__ == "__main__":
    main()
