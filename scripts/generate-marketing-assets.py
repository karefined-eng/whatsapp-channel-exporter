"""Generate the shared Chrome, Edge, and website marketing image pack.

The extension UI images are real captures from website/public. This script only
adds branded framing, typography, and layout around those captures so store
screenshots remain faithful to the product.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "store-assets"
PUBLIC = ROOT / "website" / "public"
WEB = ROOT / "website"
ICON_SRC = ROOT / "src" / "assets" / "icons"

BG = (5, 12, 14)
PANEL = (13, 23, 25)
PANEL_2 = (17, 30, 31)
TEXT = (245, 248, 247)
MUTED = (162, 181, 181)
GREEN = (25, 205, 123)
GREEN_SOFT = (122, 244, 184)
LINE = (38, 83, 75)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=255)
    return mask


def radial_background(size: tuple[int, int], green_spots: list[tuple[float, float, float]]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, BG)
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            r, g, b = BG
            for sx, sy, radius in green_spots:
                distance = math.sqrt(((x - sx * width) ** 2) + ((y - sy * height) ** 2))
                strength = max(0.0, 1.0 - distance / radius)
                strength *= strength
                r += int(1 * strength)
                g += int(46 * strength)
                b += int(25 * strength)
            # Very subtle vertical lift keeps the dark cards readable.
            lift = int(6 * (1 - y / max(1, height)))
            pixels[x, y] = (min(255, r + lift), min(255, g + lift), min(255, b + lift))
    return image


def grid(draw: ImageDraw.ImageDraw, size: tuple[int, int], step: int = 56) -> None:
    width, height = size
    for x in range(0, width, step):
        draw.line((x, 0, x, height), fill=(21, 39, 39), width=1)
    for y in range(0, height, step):
        draw.line((0, y, width, y), fill=(21, 39, 39), width=1)


def glow_line(image: Image.Image, points: list[tuple[int, int]], width: int = 2) -> None:
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.line(points, fill=(*GREEN, 90), width=width * 10, joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(width * 5))
    image.alpha_composite(glow)
    draw = ImageDraw.Draw(image)
    draw.line(points, fill=(*GREEN, 185), width=width, joint="curve")


def draw_icon(size: int) -> Image.Image:
    """Rasterize the geometry from website/public/favicon.svg.

    The Chrome variant keeps a transparent margin around the favicon artwork;
    the source favicon itself remains the canonical vector design.
    """
    scale = 4
    canvas = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    margin = round(size * 0.125) * scale
    artwork = size * scale - 2 * margin

    def point(value: float) -> int:
        return round(margin + (value / 64) * artwork)

    # Premium dark container: <rect x="2" y="2" width="60" height="60" rx="16">.
    draw.rounded_rectangle(
        (point(2), point(2), point(62), point(62)),
        radius=point(16) - margin,
        fill=(28, 28, 28, 255),
        outline=(51, 51, 51, 255),
        width=max(2, round(1.5 * artwork / 64)),
    )

    def gradient_line(target: Image.Image, start: tuple[int, int], end: tuple[int, int], width: int) -> None:
        line = ImageDraw.Draw(target)
        steps = max(1, abs(end[0] - start[0]))
        for index in range(steps):
            ratio = index / max(1, steps - 1)
            color = (
                round(37 + (18 - 37) * ratio),
                round(211 + (140 - 211) * ratio),
                round(102 + (126 - 102) * ratio),
                255,
            )
            x1 = start[0] + round((end[0] - start[0]) * index / steps)
            x2 = start[0] + round((end[0] - start[0]) * (index + 1) / steps)
            y1 = start[1] + round((end[1] - start[1]) * index / steps)
            y2 = start[1] + round((end[1] - start[1]) * (index + 1) / steps)
            line.line((x1, y1, x2, y2), fill=color, width=width)

    accent_start, accent_end = (point(12), point(2)), (point(52), point(2))
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).line((accent_start, accent_end), fill=(*GREEN, 165), width=max(2, round(4 * artwork / 64)))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(2, round(2.5 * artwork / 64)))))
    gradient_line(canvas, accent_start, accent_end, max(2, round(3 * artwork / 64)))

    # Export arrow and archive tray: the exact paths from the favicon's group.
    arrow = [
        (point(32), point(20)),
        (point(32), point(38)),
    ]
    arrow_left = [(point(24), point(30)), (point(32), point(38)), (point(40), point(30))]
    tray = [(point(20), point(44)), (point(44), point(44))]
    symbol_glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    symbol_draw = ImageDraw.Draw(symbol_glow)
    stroke = max(2, round(4 * artwork / 64))
    symbol_draw.line(arrow, fill=(*GREEN, 180), width=stroke * 2, joint="curve")
    symbol_draw.line(arrow_left, fill=(*GREEN, 180), width=stroke * 2, joint="curve")
    symbol_draw.line(tray, fill=(*GREEN, 180), width=stroke * 2)
    canvas.alpha_composite(symbol_glow.filter(ImageFilter.GaussianBlur(max(2, round(2.5 * artwork / 64)))))
    gradient_line(canvas, arrow[0], arrow[1], stroke)
    gradient_line(canvas, arrow_left[0], arrow_left[1], stroke)
    gradient_line(canvas, tray[0], tray[1], stroke)
    # SVG filters can bleed beyond their source shape. Clip that glow to the
    # favicon artwork area so Chrome retains the required transparent margin.
    clipped = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    clipped.alpha_composite(canvas.crop((margin, margin, size * scale - margin, size * scale - margin)), (margin, margin))
    return clipped.resize((size, size), Image.Resampling.LANCZOS)


def save_icon_assets() -> None:
    ICON_SRC.mkdir(parents=True, exist_ok=True)
    icon128 = draw_icon(128)
    icon128.save(ICON_SRC / "icon128.png")
    icon128.resize((48, 48), Image.Resampling.LANCZOS).save(ICON_SRC / "icon48.png")
    icon128.resize((16, 16), Image.Resampling.LANCZOS).save(ICON_SRC / "icon16.png")
    draw_icon(300).save(STORE / "edge-icon-300.png")


def add_card(base: Image.Image, image: Image.Image, box: tuple[int, int, int, int], radius: int = 18) -> None:
    x, y, width, height = box
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((x + 8, y + 12, x + width + 8, y + height + 12), radius, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    base.alpha_composite(shadow)
    card = image.convert("RGBA").resize((width, height), Image.Resampling.LANCZOS)
    card.putalpha(rounded_mask((width, height), radius))
    base.alpha_composite(card, (x, y))
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((x, y, x + width, y + height), radius, outline=(*GREEN, 120), width=2)


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, size: int = 18) -> None:
    draw.text(xy, text.upper(), font=font(size, bold=True), fill=GREEN_SOFT, stroke_width=0)


def make_promo_tile() -> None:
    size = (440, 280)
    image = radial_background(size, [(0.05, 0.15, 290), (1.0, 0.8, 320)]).convert("RGBA")
    draw = ImageDraw.Draw(image)
    grid(draw, size, 40)
    icon = draw_icon(76)
    image.alpha_composite(icon, (28, 25))
    label(draw, (122, 31), "Local archive", 13)
    draw.text((28, 122), "WA Channel", font=font(28, bold=True), fill=TEXT)
    draw.text((28, 155), "Exporter", font=font(28, bold=True), fill=TEXT)
    draw.text((29, 201), "Read-only ZIP exports", font=font(16), fill=MUTED)
    ui = Image.open(PUBLIC / "actual-ui-1.png").convert("RGB")
    add_card(image, ui, (328, 22, 91, 236), radius=12)
    glow_line(image, [(26, 244), (192, 244), (280, 229), (326, 229)], 2)
    image.convert("RGB").save(STORE / "promo-tile-440x280.png", quality=95)


def make_marquee() -> None:
    size = (1400, 560)
    image = radial_background(size, [(0.08, 0.26, 450), (0.95, 0.65, 520)]).convert("RGBA")
    draw = ImageDraw.Draw(image)
    grid(draw, size, 70)
    draw.rounded_rectangle((28, 28, 1371, 531), radius=24, outline=(*LINE, 220), width=2)
    label(draw, (78, 76), "WA CHANNEL EXPORTER", 18)
    draw.text((78, 132), "Archive the channel", font=font(58, bold=True), fill=TEXT)
    draw.text((78, 198), "you can see.", font=font(58, bold=True), fill=TEXT)
    draw.text((82, 290), "Local, read-only exports for WhatsApp Channel posts", font=font(22), fill=MUTED)
    draw.text((82, 324), "and available media in a portable archive.", font=font(22), fill=MUTED)
    chips = [("LOCAL-FIRST", 82), ("READ-ONLY", 230), ("ZIP ARCHIVE", 366)]
    for text, x in chips:
        draw.rounded_rectangle((x, 410, x + 130, 450), radius=20, fill=(18, 30, 31, 230), outline=(*LINE, 220), width=1)
        draw.text((x + 17, 422), text, font=font(13, bold=True), fill=GREEN_SOFT)
    ui1 = Image.open(PUBLIC / "actual-ui-1.png").convert("RGB")
    ui2 = Image.open(PUBLIC / "actual-ui-2.png").convert("RGB")
    add_card(image, ui1, (860, 64, 232, 420), radius=16)
    add_card(image, ui2, (1110, 108, 198, 360), radius=16)
    glow_line(image, [(778, 300), (842, 300), (890, 270)], 2)
    image.convert("RGB").save(STORE / "marquee-tile-1400x560.png", quality=95)
    # Keep the website's promo art aligned with the store marquee dimensions.
    image.convert("RGB").save(PUBLIC / "promo-marquee.png", quality=95)


def make_store_screenshot(title: str, subtitle: str, ui_path: Path, output: Path, callouts: list[str]) -> None:
    size = (1280, 800)
    image = radial_background(size, [(0.1, 0.15, 520), (0.85, 0.9, 500)]).convert("RGBA")
    draw = ImageDraw.Draw(image)
    grid(draw, size, 64)
    label(draw, (44, 38), "WA CHANNEL EXPORTER", 14)
    draw.text((44, 82), title, font=font(38, bold=True), fill=TEXT)
    draw.text((44, 136), subtitle, font=font(20), fill=MUTED)
    draw.rounded_rectangle((44, 184, 608, 666), radius=22, fill=(8, 17, 18, 190), outline=(*LINE, 180), width=2)
    draw.text((84, 236), "Built for a clean", font=font(30, bold=True), fill=TEXT)
    draw.text((84, 276), "local archive workflow.", font=font(30, bold=True), fill=GREEN_SOFT)
    y = 360
    for text in callouts:
        draw.ellipse((86, y + 4, 100, y + 18), fill=GREEN)
        draw.text((122, y), text, font=font(20), fill=TEXT)
        y += 74
    draw.text((84, 612), "No post content is uploaded by the extension.", font=font(16), fill=MUTED)
    ui = Image.open(ui_path).convert("RGB")
    add_card(image, ui, (760, 88, 390, 622), radius=20)
    draw = ImageDraw.Draw(image)
    draw.text((44, 742), "Real extension UI · captured for store listing", font=font(15), fill=(113, 151, 145))
    image.convert("RGB").save(output, quality=95)


def make_og(kind: str) -> None:
    size = (1200, 630)
    image = radial_background(size, [(0.02, 0.16, 430), (0.96, 0.75, 450)]).convert("RGBA")
    draw = ImageDraw.Draw(image)
    grid(draw, size, 60)
    icon = draw_icon(76)
    image.alpha_composite(icon, (70, 72))
    label(draw, (166, 86), "WA CHANNEL EXPORTER", 14)
    if kind == "pdf":
        headline = "Export clean PDF records."
        subhead = "Turn a channel archive into a portable, readable document."
        ui = Image.open(PUBLIC / "actual-ui-2.png").convert("RGB")
        tag = "PDF-READY ARCHIVE"
    else:
        headline = "Archive the channel you can see."
        subhead = "Export WhatsApp Channel posts and available media into a local ZIP."
        ui = Image.open(PUBLIC / "actual-ui-1.png").convert("RGB")
        tag = "LOCAL-FIRST · READ-ONLY"
    draw.text((70, 176), headline, font=font(43, bold=True), fill=TEXT)
    draw.text((72, 246), subhead, font=font(20), fill=MUTED)
    draw.rounded_rectangle((72, 350, 490, 404), radius=26, fill=(14, 32, 29, 230), outline=(*LINE, 220), width=2)
    draw.text((98, 367), tag, font=font(15, bold=True), fill=GREEN_SOFT)
    draw.text((72, 514), "100% local archive workflow", font=font(17), fill=(127, 174, 163))
    add_card(image, ui, (748, 42, 310, 548), radius=18)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1068, 130, 1148, 420), radius=18, fill=(12, 26, 26, 220), outline=(*GREEN, 150), width=2)
    draw.text((1086, 160), "ZIP", font=font(20, bold=True), fill=GREEN_SOFT)
    draw.text((1082, 242), "PDF", font=font(20, bold=True), fill=TEXT)
    draw.text((1082, 324), "CSV", font=font(20, bold=True), fill=TEXT)
    glow_line(image, [(520, 370), (650, 370), (740, 310)], 2)
    png_path = WEB / ("og-pdf.png" if kind == "pdf" else "og-main.png")
    jpg_path = WEB / ("og-pdf.jpg" if kind == "pdf" else "og-main.jpg")
    public_path = PUBLIC / png_path.name
    image.convert("RGB").save(png_path, quality=95)
    image.convert("RGB").save(jpg_path, quality=92, optimize=True)
    image.convert("RGB").save(public_path, quality=95)


def main() -> None:
    STORE.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    save_icon_assets()
    make_promo_tile()
    make_marquee()
    make_store_screenshot(
        "Choose what to export",
        "Set a date range and select posts, media, or PDF output.",
        PUBLIC / "actual-ui-1.png",
        STORE / "screenshot-1-1280x800.png",
        ["Date range stays in your control", "Posts, media, or PDF output", "The extension is read-only"],
    )
    make_store_screenshot(
        "Review the export before download",
        "See counts, boundaries, and partial-content reporting before saving.",
        PUBLIC / "actual-ui-2.png",
        STORE / "screenshot-2-1280x800.png",
        ["Review included posts and media", "See unavailable items clearly", "Copy a redacted diagnostic"],
    )
    make_og("main")
    make_og("pdf")
    print("Generated shared Chrome, Edge, and website marketing assets.")


if __name__ == "__main__":
    main()
