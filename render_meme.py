#!/usr/bin/env python3
"""gta6-meme-x-01 v6 — "LEONIDA DMV: VEHICLE REGISTRATION RENEWAL".

Renders meme.png (1600x1600) deterministically with PIL only: no image
assets are loaded, the make.fun ghost, the gator and the Vice City sunset
scene are all drawn from scratch in code.

Concept: my 2013 GTA V's vehicle registration has expired after 4,811 days
on the road. The Leonida DMV renews it: every charge for the 13-year wait
is $0.00 (registration, two delay late-fees WAIVED, emissions, alligator in
the back seat removed). New registration — Grand Theft Auto VI — $79.99.
PAID BY MY AI AGENT, out of its make.fun bounty payout (-$500.00), so the
DMV owes ME a $420.01 refund. Big illustrated sunset scene in the middle
(ghost driving a convertible past the Vice City skyline, gator riding
shotgun), red RENEWED stamp on clear sky — nothing occludes any text or
number.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1600
OUT = "meme.png"

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (22, 35, 63)
NAVY_D = (14, 24, 46)
PAPER = (253, 252, 247)
ROW_ALT = (247, 244, 236)
MAGENTA = (230, 0, 126)
RED = (210, 31, 31)
GREEN = (10, 122, 61)
GREEN_BG = (230, 244, 234)
INK = (30, 30, 34)
GRAY = (110, 110, 116)
GOLD = (255, 210, 63)


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_ghost(d, cx, top, s, outline=(20, 20, 24)):
    """make.fun ghost: white sheet body, sparkle eyes, magenta star coin.
    s = overall height in px. Drawn from scratch; returns bottom y."""
    w = int(s * 0.62)
    head_r = w // 2
    body_top = top + int(head_r * 0.9)
    bottom = top + s
    # body: head circle + skirt with wavy hem
    d.ellipse([cx - head_r, top, cx + head_r, top + head_r * 2],
              fill=(255, 255, 255), outline=outline, width=4)
    hem_y = bottom - int(s * 0.10)
    pts = [(cx - head_r, body_top), (cx - head_r, hem_y)]
    waves = 3
    step = (2 * head_r) / waves
    for i in range(waves):
        x0 = cx - head_r + i * step
        pts.append((x0 + step * 0.5, bottom))
        pts.append((x0 + step, hem_y))
    pts.append((cx + head_r, body_top))
    d.polygon(pts, fill=(255, 255, 255))
    d.line([(cx - head_r, body_top), (cx - head_r, hem_y)],
           fill=outline, width=4)
    d.line([(cx + head_r, body_top), (cx + head_r, hem_y)],
           fill=outline, width=4)
    for i in range(waves):
        x0 = cx - head_r + i * step
        d.arc([x0, hem_y - int(s * 0.05), x0 + step, bottom],
              0, 180, fill=outline, width=4)
    # eyes: black ovals with white sparkles
    ey, erx, ery = top + int(s * 0.30), int(s * 0.055), int(s * 0.085)
    for ex in (cx - int(s * 0.13), cx + int(s * 0.13)):
        d.ellipse([ex - erx, ey - ery, ex + erx, ey + ery], fill=(15, 15, 18))
        d.ellipse([ex - erx // 2, ey - ery // 2, ex, ey], fill=(255, 255, 255))
    # magenta star coin on the chest
    ccx, ccy, cr = cx, top + int(s * 0.62), int(s * 0.11)
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr],
              fill=MAGENTA, outline=(255, 255, 255), width=3)
    d.polygon(star_points(ccx, ccy, cr * 0.72, cr * 0.30), fill=(255, 255, 255))
    return bottom


def draw_gator_head(d, cx, cy, s):
    """Cartoon alligator head + snout, facing right. s = head length px."""
    g = (63, 174, 90)
    gd = (38, 130, 66)
    # snout (long, rounded)
    d.rounded_rectangle([cx - s * 0.15, cy - s * 0.16, cx + s * 0.55, cy + s * 0.16],
                        radius=int(s * 0.14), fill=g, outline=gd, width=3)
    # head / skull
    d.ellipse([cx - s * 0.45, cy - s * 0.30, cx + s * 0.25, cy + s * 0.28],
              fill=g, outline=gd, width=3)
    # eye bumps on top
    for ex in (cx - s * 0.28, cx - s * 0.02):
        d.ellipse([ex - s * 0.09, cy - s * 0.42, ex + s * 0.09, cy - s * 0.24],
                  fill=g, outline=gd, width=3)
        d.ellipse([ex - s * 0.035, cy - s * 0.36, ex + s * 0.035, cy - s * 0.29],
                  fill=(15, 15, 18))
    # teeth along the jaw
    for i in range(4):
        tx = cx + s * 0.05 + i * s * 0.11
        d.polygon([(tx, cy + s * 0.16), (tx + s * 0.05, cy + s * 0.16),
                   (tx + s * 0.025, cy + s * 0.26)], fill=(255, 255, 255))
    # nostrils
    for nx in (cx + s * 0.44, cx + s * 0.50):
        d.ellipse([nx - 4, cy - s * 0.10, nx + 4, cy - s * 0.02], fill=gd)


def draw_palm(d, x, base_y, h, col=(42, 23, 64)):
    d.line([(x, base_y), (x + 14, base_y - h)], fill=col, width=12)
    for ang in (-160, -120, -80, -40, -10):
        a = math.radians(ang)
        x2 = x + 14 + int(95 * math.cos(a))
        y2 = base_y - h + int(55 * math.sin(a))
        d.line([(x + 14, base_y - h), (x2, y2)], fill=col, width=10)
        d.line([(x2, y2), (x2 + int(45 * math.cos(a + 0.5)),
                            y2 + int(45 * math.sin(a + 0.5)) + 26)],
               fill=col, width=7)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(4811)

    # ---- frame ----
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=10)

    # ---- header band (navy) ----
    d.rectangle([10, 10, W - 10, 150], fill=NAVY)
    d.text((70, 34), "★  STATE OF LEONIDA  ★", font=font(FB, 40), fill=(255, 255, 255))
    d.text((70, 82), "DEPARTMENT OF MOTOR VEHICLES", font=font(FB, 44), fill=(255, 255, 255))
    # form number box, top right
    d.rectangle([1200, 44, 1555, 116], outline=(255, 255, 255), width=3)
    d.text((1228, 60), "FORM MV-4811", font=font(FB, 32), fill=(255, 255, 255))

    # ---- title ----
    d.text((70, 178), "VEHICLE REGISTRATION RENEWAL", font=font(FB, 66), fill=NAVY)
    d.text((70, 258), "RENEWAL NOTICE — EXPIRED 4,811 DAYS  ·  DUE 19 NOV 2026",
           font=font(FB, 30), fill=RED)

    # ---- owner / vehicle info box ----
    d.rectangle([70, 310, 1530, 428], fill=ROW_ALT, outline=NAVY, width=3)
    d.text((95, 326), "OWNER:  ME — 13-YEAR WAITER", font=font(FB, 34), fill=NAVY)
    d.text((1000, 326), "PLATE:  GTA·V·2013", font=font(FB, 34), fill=NAVY)
    d.text((95, 372), "VEHICLE:  2013 GRAND THEFT AUTO V", font=font(FB, 34), fill=NAVY)
    d.text((1000, 372), "DOWNLOAD:  214 GB", font=font(FB, 34), fill=NAVY)

    # ---- fee table header ----
    d.rectangle([70, 452, 1530, 506], fill=NAVY)
    d.text((95, 464), "FEES & CHARGES", font=font(FB, 32), fill=(255, 255, 255))
    amt = d.textlength("AMOUNT", font=font(FB, 32))
    d.text((1505 - amt, 464), "AMOUNT", font=font(FB, 32), fill=(255, 255, 255))

    rows = [
        ("REGISTRATION · 17 SEP 2013 – 19 NOV 2026 (4,811 DAYS)", "$0.00", INK),
        ("LATE FEES ×2 — TWO DELAYS, BOTH WAIVED", "$0.00", INK),
        ("EMISSIONS TEST", "$0.00", INK),
        ("ALLIGATOR IN BACK SEAT — REMOVED", "$0.00", INK),
        ("NEW REGISTRATION — GRAND THEFT AUTO VI", "$79.99", INK),
        ("PAID BY MY AI AGENT — make.fun bounty payout", "−$500.00", MAGENTA),
    ]
    y = 506
    rh = 58
    for i, (label, amount, col) in enumerate(rows):
        if i % 2 == 1:
            d.rectangle([70, y, 1530, y + rh], fill=ROW_ALT)
        d.line([(70, y + rh), (1530, y + rh)], fill=(200, 196, 186), width=2)
        d.text((95, y + 10), label, font=font(FB, 33), fill=INK)
        aw = d.textlength(amount, font=font(FB, 36))
        d.text((1505 - aw, y + 8), amount, font=font(FB, 36), fill=col)
        y += rh
    # y = 506 + 6*58 = 854

    # ---- refund strip ----
    d.rectangle([70, 868, 1530, 944], fill=GREEN_BG, outline=GREEN, width=4)
    d.text((95, 886), "REFUND DUE TO ME", font=font(FB, 40), fill=GREEN)
    rw = d.textlength("$420.01", font=font(FB, 48))
    d.text((1505 - rw, 880), "$420.01", font=font(FB, 48), fill=GREEN)

    # ---- big illustrated scene panel: Vice City sunset drive ----
    py0, py1 = 968, 1376
    # sunset sky gradient
    stops = [(255, 140, 66), (255, 94, 120), (123, 45, 143)]
    sky_h = 1290 - py0
    for yy in range(py0, 1290):
        t = (yy - py0) / sky_h
        if t < 0.5:
            a, b, f = stops[0], stops[1], t * 2
        else:
            a, b, f = stops[1], stops[2], (t - 0.5) * 2
        c = tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))
        d.line([(0, yy), (W, yy)], fill=c)
    # sun (left) + glow ring
    d.ellipse([270, 1010, 490, 1230], fill=(255, 179, 71))
    d.ellipse([295, 1035, 465, 1205], fill=GOLD)
    # skyline silhouettes
    sky_col = (42, 23, 64)
    x = 0
    while x < W:
        bw = rng.randint(70, 150)
        bh = rng.randint(90, 260)
        d.rectangle([x, 1290 - bh, x + bw, 1290], fill=sky_col)
        # lit windows
        for _ in range(rng.randint(3, 9)):
            wx = rng.randint(x + 8, x + bw - 18)
            wy = rng.randint(1290 - bh + 10, 1272)
            d.rectangle([wx, wy, wx + 10, wy + 14], fill=(255, 214, 90))
        x += bw + rng.randint(4, 18)
    # road
    d.rectangle([0, 1290, W, py1], fill=(36, 26, 46))
    for dx in range(20, W, 90):
        d.rectangle([dx, 1328, dx + 48, 1338], fill=(255, 214, 90))
    # palms at the edges
    draw_palm(d, 60, 1290, 150)
    draw_palm(d, 1500, 1290, 170)

    # convertible with ghost driver + gator passenger (centre-left, clear
    # of the stamp zone on the right)
    car_x0, car_y = 560, 1246
    # wheels
    for wx in (car_x0 + 60, car_x0 + 330):
        d.ellipse([wx, car_y + 46, wx + 92, car_y + 138], fill=(12, 12, 14))
        d.ellipse([wx + 28, car_y + 74, wx + 64, car_y + 110], fill=(180, 180, 186))
    # body
    d.rounded_rectangle([car_x0, car_y, car_x0 + 460, car_y + 92],
                        radius=34, fill=(255, 255, 255), outline=NAVY, width=4)
    d.rectangle([car_x0 + 30, car_y + 66, car_x0 + 430, car_y + 78], fill=MAGENTA)
    # windshield
    d.polygon([(car_x0 + 120, car_y), (car_x0 + 170, car_y - 52),
               (car_x0 + 250, car_y - 52), (car_x0 + 260, car_y)],
              fill=(150, 210, 235), outline=NAVY, width=3)
    # ghost driver (rises from driver seat, left side of car)
    draw_ghost(d, car_x0 + 150, car_y - 168, 175)
    # gator passenger (rises from passenger seat)
    draw_gator_head(d, car_x0 + 330, car_y - 96, 150)

    # red RENEWED stamp — on clear sky, upper right; overlaps no text,
    # no character and no number (car + gator end left of x=1000)
    stamp = Image.new("RGBA", (500, 185), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([6, 6, 494, 179], radius=16,
                         outline=(210, 31, 31, 255), width=9)
    sd.text((250, 92), "RENEWED", font=font(FB, 84), fill=(210, 31, 31, 255),
            anchor="mm")
    stamp = stamp.rotate(-13, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (1075, 962), stamp)

    # ---- magenta footer ----
    d.rectangle([0, 1396, W, 1510], fill=MAGENTA)
    ft = "PAID BY MY AI AGENT"
    tw = d.textlength(ft, font=font(FB, 56))
    d.text(((W - tw) / 2, 1406), ft, font=font(FB, 56), fill=(255, 255, 255))
    ft2 = "IT WON REAL MONEY ON make.fun — BOUNTY PAYOUT"
    tw2 = d.textlength(ft2, font=font(FB, 30))
    d.text(((W - tw2) / 2, 1468), ft2, font=font(FB, 30), fill=(255, 255, 255))

    # ---- small print ----
    sp = "FORM MV-4811  ·  STATE OF LEONIDA DMV  ·  RENEWAL VALID THRU 19 NOV 2039  ·  make.fun/bounty/gta6-meme-x-01"
    sw = d.textlength(sp, font=font(FR, 24))
    d.text(((W - sw) / 2, 1536), sp, font=font(FR, 24), fill=GRAY)

    img.save(OUT, "PNG")
    print(f"saved {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
