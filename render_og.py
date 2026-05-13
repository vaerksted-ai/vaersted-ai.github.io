"""Render the Open Graph social-preview image for vaerksted.ai.

Output: og-image.png (1200x630, the standard size for Facebook/Twitter/LinkedIn).
"""
from PIL import Image, ImageDraw, ImageFont

# ─── Canvas ─────────────────────────────────────────
W, H = 1200, 630
PAPER = (242, 235, 224)
INK = (26, 22, 20)
INK_SOFT = (92, 83, 71)
FORGE = (168, 67, 31)
RULE = (26, 22, 20, 38)  # ~15% alpha

img = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(img, "RGBA")

# ─── Atmospheric tint (two soft radial highlights) ──
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
# Forge-red highlight, top-left
for r in range(600, 0, -20):
    a = int(8 * (1 - r / 600))
    od.ellipse(
        (216 - r, 138 - r, 216 + r, 138 + r),
        fill=(FORGE[0], FORGE[1], FORGE[2], a),
    )
# Ink shadow, bottom-right
for r in range(700, 0, -20):
    a = int(6 * (1 - r / 700))
    od.ellipse(
        (984 - r, 491 - r, 984 + r, 491 + r),
        fill=(INK[0], INK[1], INK[2], a),
    )
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

# ─── Fonts ──────────────────────────────────────────
SERIF_REG = "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-regular.otf"
SERIF_ITA = "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-italic.otf"
MONO_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

wordmark_font = ImageFont.truetype(SERIF_REG, 240)
ae_font = ImageFont.truetype(SERIF_ITA, 240)
tagline_font = ImageFont.truetype(SERIF_ITA, 44)
eyebrow_font = ImageFont.truetype(MONO_REG, 16)
footer_font = ImageFont.truetype(MONO_REG, 14)

# ─── Eyebrow ────────────────────────────────────────
EYEBROW_Y = 90
draw.line((80, EYEBROW_Y, 112, EYEBROW_Y), fill=FORGE, width=2)
draw.text(
    (128, EYEBROW_Y - 11),
    "A COMMUNITY OF BUILDERS",
    fill=FORGE,
    font=eyebrow_font,
    spacing=4,
)
# manual letter-spacing approximation with kerning via tracked rendering
def draw_tracked(xy, text, font, fill, track):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, fill=fill, font=font)
        bbox = font.getbbox(ch)
        x += (bbox[2] - bbox[0]) + track
    return x

# Redraw eyebrow with letter-spacing for that editorial caps feel
draw.rectangle((128, EYEBROW_Y - 11, 700, EYEBROW_Y + 11), fill=PAPER)
draw_tracked(
    (128, EYEBROW_Y - 11),
    "A COMMUNITY OF BUILDERS",
    eyebrow_font,
    FORGE,
    3,
)

# ─── Wordmark: V æ rksted ───────────────────────────
WORDMARK_Y = 130
x = 70

# "V"
draw.text((x, WORDMARK_Y), "V", fill=INK, font=wordmark_font)
v_bbox = wordmark_font.getbbox("V")
x += (v_bbox[2] - v_bbox[0]) - 4  # subtle tightening only

# "æ" italic, forge red
draw.text((x, WORDMARK_Y), "æ", fill=FORGE, font=ae_font)
ae_bbox = ae_font.getbbox("æ")
x += (ae_bbox[2] - ae_bbox[0])

# "rksted"
draw.text((x, WORDMARK_Y), "rksted", fill=INK, font=wordmark_font)

# ─── Tagline ────────────────────────────────────────
draw.text(
    (80, 440),
    "We build AI-native apps. On principle.",
    fill=INK,
    font=tagline_font,
)

# ─── Footer rule + meta ─────────────────────────────
draw.line((80, 540, 1120, 540), fill=(26, 22, 20, 38), width=1)
draw_tracked(
    (80, 570),
    "VAERKSTED.AI  ·  KØBENHAVN  ·  EST. MMXXVI",
    footer_font,
    INK_SOFT,
    2,
)

# ─── Save ───────────────────────────────────────────
img.save("/home/claude/vaerksted-site/og-image.png", "PNG", optimize=True)
print(f"OG image saved: 1200x630")
