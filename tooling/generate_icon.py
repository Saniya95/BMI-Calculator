from PIL import Image, ImageDraw, ImageFilter, ImageFont

SIZE = 1024
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Gradient background (top-left to bottom-right)
c1 = (109, 40, 217)
c2 = (147, 51, 234)
c3 = (79, 20, 163)
for y in range(SIZE):
    t = y / (SIZE - 1)
    r = int(c1[0] * (1 - t) + c2[0] * t)
    g = int(c1[1] * (1 - t) + c2[1] * t)
    b = int(c1[2] * (1 - t) + c2[2] * t)
    draw.line((0, y, SIZE, y), fill=(r, g, b, 255))

# Subtle radial accent glow
accent = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
accent_draw = ImageDraw.Draw(accent)
accent_draw.ellipse((80, 60, 760, 740), fill=(200, 145, 255, 85))
accent = accent.filter(ImageFilter.GaussianBlur(80))
img = Image.alpha_composite(img, accent)

# Rounded-square icon container (safe area)
container = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
container_draw = ImageDraw.Draw(container)
margin = 70
radius = 220
container_draw.rounded_rectangle(
    (margin, margin, SIZE - margin, SIZE - margin),
    radius=radius,
    fill=(255, 255, 255, 14),
)
container = container.filter(ImageFilter.GaussianBlur(1.5))
img = Image.alpha_composite(img, container)

# Scale body shadow
shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
shadow_draw.rounded_rectangle((235, 260, 789, 840), radius=130, fill=(0, 0, 0, 120))
shadow = shadow.filter(ImageFilter.GaussianBlur(32))
img = Image.alpha_composite(img, shadow)

# Scale body
scale_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
scale_draw = ImageDraw.Draw(scale_layer)
scale_draw.rounded_rectangle((220, 245, 804, 825), radius=135, fill=(245, 239, 255, 255))

# Soft inner highlight
highlight = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
highlight_draw = ImageDraw.Draw(highlight)
highlight_draw.rounded_rectangle((245, 270, 779, 500), radius=110, fill=(255, 255, 255, 85))
highlight = highlight.filter(ImageFilter.GaussianBlur(20))
scale_layer = Image.alpha_composite(scale_layer, highlight)

# Digital display with neon glow
display_glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
display_glow_draw = ImageDraw.Draw(display_glow)
display_glow_draw.rounded_rectangle((330, 345, 694, 490), radius=34, fill=(150, 90, 255, 160))
display_glow = display_glow.filter(ImageFilter.GaussianBlur(18))
scale_layer = Image.alpha_composite(scale_layer, display_glow)

scale_draw = ImageDraw.Draw(scale_layer)
scale_draw.rounded_rectangle((340, 355, 684, 480), radius=28, fill=(61, 24, 110, 255))

# Corner feet details
for bx, by in [(285, 730), (670, 730)]:
    scale_draw.rounded_rectangle((bx, by, bx + 70, by + 48), radius=20, fill=(216, 206, 245, 255))

# BMI text
font = None
font_candidates = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
]
for path in font_candidates:
    try:
        font = ImageFont.truetype(path, 92)
        break
    except OSError:
        continue
if font is None:
    font = ImageFont.load_default()

text = "BMI"
bbox = scale_draw.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
text_x = (SIZE - text_w) // 2
text_y = 356 + ((125 - text_h) // 2) - 2

# Text glow
text_glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
text_glow_draw = ImageDraw.Draw(text_glow)
text_glow_draw.text((text_x, text_y), text, font=font, fill=(183, 147, 255, 210))
text_glow = text_glow.filter(ImageFilter.GaussianBlur(6))
scale_layer = Image.alpha_composite(scale_layer, text_glow)

scale_draw = ImageDraw.Draw(scale_layer)
scale_draw.text((text_x, text_y), text, font=font, fill=(243, 235, 255, 255))

img = Image.alpha_composite(img, scale_layer)

# Final polish with vignette
vignette = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
vg = ImageDraw.Draw(vignette)
vg.rounded_rectangle((36, 36, SIZE - 36, SIZE - 36), radius=250, outline=(255, 255, 255, 30), width=4)
img = Image.alpha_composite(img, vignette)

img.save("assets/icon.png", "PNG")
print("Generated assets/icon.png")
