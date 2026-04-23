from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


PAGE_W = 1654
PAGE_H = 2339
MARGIN = 120

BG = "#fbf6ef"
PANEL = "#fffdf8"
INK = "#1f2430"
MUTED = "#5c6676"
ACCENT = "#cb6d2e"
ACCENT_SOFT = "#f2dcc9"
DARK = "#182033"
LINE = "#dfd2c1"

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "DOBLI_Passion-Plan-Resubmission.pdf"

FONT_DIR = Path(r"C:\Windows\Fonts")


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size=size)


FONT_SANS = load_font("segoeui.ttf", 30)
FONT_SANS_SMALL = load_font("segoeui.ttf", 21)
FONT_SANS_LABEL = load_font("arialbd.ttf", 19)
FONT_SANS_BOLD = load_font("arialbd.ttf", 29)
FONT_SERIF_TITLE = load_font("georgiab.ttf", 78)
FONT_SERIF_H2 = load_font("georgiab.ttf", 40)
FONT_SERIF_H3 = load_font("georgiab.ttf", 30)


MISSION = (
    "I am becoming an Ignatian leader who uses technology with competence, "
    "conscience, and compassion. I want to grow into a disciplined and faithful "
    "man who keeps learning, leads with humility, and creates systems that solve "
    "real problems for people. Guided by integrity, perseverance, service, and "
    "cura personalis, I hope to build work that is excellent, ethical, and deeply "
    "human. In the years ahead, I want my success to be measured not only by what "
    "I achieve, but by the kind of person I become and the lives I help improve "
    "through my work."
)

PRAYER = (
    "Lord, guide the person I am becoming. Form in me a heart that listens before "
    "it speaks, serves before it seeks recognition, and chooses what is right even "
    "when it is difficult. Bless my studies, future work, relationships, and "
    "decisions so that they may reflect Your wisdom and love. When I succeed, keep "
    "me humble. When I fail, keep me faithful. When I am uncertain, remind me that "
    "Your grace goes before me. Give me courage, discipline, compassion, and hope "
    "so that my life may honor You and become a source of help, peace, and "
    "encouragement to others."
)

ROADMAP_INTRO = (
    "Over the next 10-20 years, I see my vocation at the intersection of "
    "technology, leadership, and service. I want to become a professional who "
    "builds useful digital solutions, grows into trustworthy leadership, and "
    "remains grounded in faith, integrity, and responsibility."
)

ROADMAP = [
    (
        "Years 1-3",
        "Finish my degree well, deepen my skills in software development and "
        "problem-solving, and begin meaningful work in the tech field. I want to "
        "build strong habits of discipline, prayer, and lifelong learning while "
        "starting to support my family and future goals.",
    ),
    (
        "Years 4-10",
        "Grow into a dependable developer and emerging leader who can design "
        "systems that answer real needs. I hope to gain financial stability, take "
        "on bigger responsibilities, and mentor others while learning how "
        "technology and business can work together for lasting impact.",
    ),
    (
        "Years 10-20",
        "Lead or help build a mission-driven team, business, or initiative that "
        "creates practical and human-centered solutions. I want to live a stable, "
        "meaningful life, remain active in service to the community, and build a "
        "future marked by generosity, purpose, and integrity.",
    ),
]

VALUES = ["Faith", "Integrity", "Discipline", "Excellence", "Service", "Compassion"]

CLOSING = (
    "My goal is to build a life that is stable, useful, and God-centered. I want "
    "the systems I create, the work I lead, and the relationships I keep to "
    "reflect cura personalis, responsibility, and love in action. In this way, my "
    "career will not only be a path to success, but also a vocation through which "
    "I can serve others well."
)


def make_page() -> Image.Image:
    page = Image.new("RGBA", (PAGE_W, PAGE_H), BG)
    overlay = Image.new("RGBA", (PAGE_W, PAGE_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((PAGE_W - 500, -180, PAGE_W + 140, 320), fill=(203, 109, 46, 28))
    draw.ellipse((-160, PAGE_H - 380, 380, PAGE_H + 120), fill=(24, 32, 51, 18))
    return Image.alpha_composite(page, overlay)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> float:
    return draw.textlength(text, font=font)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if text_width(draw, trial, font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def line_height(font: ImageFont.FreeTypeFont, extra: int = 12) -> int:
    bbox = font.getbbox("Ag")
    return (bbox[3] - bbox[1]) + extra


def measure_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
    paragraph_gap: int = 18,
    extra: int = 12,
) -> int:
    total = 0
    paragraphs = text.split("\n")
    for idx, para in enumerate(paragraphs):
        lines = wrap_text(draw, para, font, max_width) if para else [""]
        total += len(lines) * line_height(font, extra)
        if idx < len(paragraphs) - 1:
            total += paragraph_gap
    return total


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    x: int,
    y: int,
    max_width: int,
    fill,
    paragraph_gap: int = 18,
    extra: int = 12,
) -> int:
    paragraphs = text.split("\n")
    for idx, para in enumerate(paragraphs):
        lines = wrap_text(draw, para, font, max_width) if para else [""]
        for line in lines:
            draw.text((x, y), line, font=font, fill=fill)
            y += line_height(font, extra)
        if idx < len(paragraphs) - 1:
            y += paragraph_gap
    return y


def rounded_panel(draw, box, fill, outline=None, width=1, radius=28):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_tag(draw, x, y, text):
    pill_h = 42
    pill_w = int(text_width(draw, text, FONT_SANS_LABEL) + 34)
    rounded_panel(draw, (x, y, x + pill_w, y + pill_h), ACCENT_SOFT, radius=20)
    draw.text((x + 17, y + 9), text, font=FONT_SANS_LABEL, fill="#8c4312")
    return y + pill_h


def draw_card(draw, x, y, w, tag, title, body):
    inner_w = w - 72
    body_h = measure_wrapped(draw, body, FONT_SANS, inner_w, extra=14)
    h = 54 + 30 + 26 + 20 + body_h + 36
    rounded_panel(draw, (x, y, x + w, y + h), PANEL, outline=ImageColor.getrgb(LINE), width=2, radius=28)
    tag_bottom = draw_tag(draw, x + 32, y + 28, tag)
    title_y = tag_bottom + 18
    draw.text((x + 32, title_y), title, font=FONT_SERIF_H2, fill=DARK)
    body_y = title_y + 58
    draw_wrapped(draw, body, FONT_SANS, x + 32, body_y, inner_w, INK, extra=14)
    return y + h


def draw_footer(draw, left, right):
    y = PAGE_H - 92
    draw.line((MARGIN, y, PAGE_W - MARGIN, y), fill=ImageColor.getrgb(LINE), width=2)
    draw.text((MARGIN, y + 22), left.upper(), font=FONT_SANS_SMALL, fill=MUTED)
    right_w = int(text_width(draw, right.upper(), FONT_SANS_SMALL))
    draw.text((PAGE_W - MARGIN - right_w, y + 22), right.upper(), font=FONT_SANS_SMALL, fill=MUTED)


def draw_page_one():
    page = make_page()
    draw = ImageDraw.Draw(page)

    draw.rounded_rectangle((MARGIN, 150, MARGIN + 88, 164), radius=7, fill=ACCENT)
    draw.text((MARGIN, 192), "MODULE 03 / BECOMING AN IGNATIAN LEADER FOR LIFE", font=FONT_SANS_LABEL, fill=ACCENT)
    draw.text((MARGIN, 242), "Passion Plan", font=FONT_SERIF_TITLE, fill=DARK)

    intro = (
        "A clearer expression of who I am becoming, the life I hope to build, "
        "and the kind of leader I want to be through faith, discipline, "
        "service, and purposeful work."
    )
    draw_wrapped(draw, intro, FONT_SANS, MARGIN, 360, 910, MUTED, extra=12)

    meta_x = PAGE_W - MARGIN - 390
    meta_y = 180
    rounded_panel(draw, (meta_x, meta_y, meta_x + 390, meta_y + 272), (255, 255, 255, 222), outline=(223, 210, 193), width=2, radius=24)
    labels = [
        ("STUDENT", "Ferdinand John F. Dobli"),
        ("PROGRAM", "BS Information Technology / IT 4-A"),
        ("COURSE CONTEXT", "Seniors' Integration Program"),
    ]
    cy = meta_y + 30
    for label, value in labels:
        draw.text((meta_x + 28, cy), label, font=FONT_SANS_LABEL, fill=MUTED)
        cy += 30
        draw_wrapped(draw, value, FONT_SANS_SMALL, meta_x + 28, cy, 330, INK, extra=8)
        cy += 54

    y = 520
    y = draw_card(draw, MARGIN, y, PAGE_W - (MARGIN * 2), "1 / Personal Mission Statement", "Who I Am Becoming", MISSION)
    y += 26
    y = draw_card(draw, MARGIN, y, PAGE_W - (MARGIN * 2), "2 / Prayer for My Future Self", "Prayer for the Years Ahead", PRAYER)
    y += 30

    lead_h = 184
    rounded_panel(draw, (MARGIN, y, PAGE_W - MARGIN, y + lead_h), "#182033", radius=28)
    lead = (
        "I want my future to be rooted in both excellence and service: to keep striving "
        "for more, not for prestige alone, but for the greater good I can offer through "
        "the work I do and the life I live."
    )
    draw_wrapped(draw, lead, FONT_SANS, MARGIN + 36, y + 36, PAGE_W - (MARGIN * 2) - 72, "#fff7ef", extra=14)

    draw_footer(draw, "Passion Plan Resubmission", "Ferdinand John F. Dobli")
    return page.convert("RGB")


def draw_page_two():
    page = make_page()
    draw = ImageDraw.Draw(page)

    draw.rounded_rectangle((MARGIN, 150, MARGIN + 88, 164), radius=7, fill=ACCENT)
    draw.text((MARGIN, 192), "3 / 10-20 YEAR PASSION PLAN", font=FONT_SANS_LABEL, fill=ACCENT)
    draw.text((MARGIN, 242), "Long-Term Roadmap", font=FONT_SERIF_TITLE, fill=DARK)
    draw_wrapped(draw, ROADMAP_INTRO, FONT_SANS, MARGIN, 360, PAGE_W - (MARGIN * 2), MUTED, extra=12)

    gutter = 22
    card_w = (PAGE_W - (MARGIN * 2) - (gutter * 2)) // 3
    top = 520
    for idx, (title, body) in enumerate(ROADMAP):
        x = MARGIN + idx * (card_w + gutter)
        rounded_panel(draw, (x, top, x + card_w, top + 660), PANEL, outline=(223, 210, 193), width=2, radius=28)
        draw.rounded_rectangle((x, top, x + card_w, top + 18), radius=28, fill=ACCENT)
        draw.text((x + 28, top + 42), title, font=FONT_SERIF_H3, fill=DARK)
        draw_wrapped(draw, body, FONT_SANS_SMALL, x + 28, top + 102, card_w - 56, INK, extra=11)

    values_y = 1250
    rounded_panel(draw, (MARGIN, values_y, PAGE_W - MARGIN, values_y + 330), PANEL, outline=(223, 210, 193), width=2, radius=28)
    tag_bottom = draw_tag(draw, MARGIN + 32, values_y + 28, "Core Values")
    draw.text((MARGIN + 32, tag_bottom + 18), "Values I Will Uphold", font=FONT_SERIF_H2, fill=DARK)

    pill_x = MARGIN + 32
    pill_y = values_y + 160
    pill_w = 390
    pill_h = 72
    pill_gap = 20
    for idx, value in enumerate(VALUES):
        row = idx // 3
        col = idx % 3
        x = pill_x + col * (pill_w + pill_gap)
        y = pill_y + row * (pill_h + pill_gap)
        rounded_panel(draw, (x, y, x + pill_w, y + pill_h), "#fffaf3", outline=(223, 210, 193), width=2, radius=24)
        tw = int(text_width(draw, value.upper(), FONT_SANS_LABEL))
        draw.text((x + (pill_w - tw) / 2, y + 22), value.upper(), font=FONT_SANS_LABEL, fill="#33405a")

    closing_y = 1642
    rounded_panel(draw, (MARGIN, closing_y, PAGE_W - MARGIN, closing_y + 360), DARK, radius=28)
    draw_wrapped(draw, CLOSING, FONT_SANS, MARGIN + 36, closing_y + 42, PAGE_W - (MARGIN * 2) - 72, "#fff7ef", extra=14)

    draw_footer(draw, "Module 03 / Ignatian Leadership", "BSIT 4-A")
    return page.convert("RGB")


def main():
    pages = [draw_page_one(), draw_page_two()]
    pages[0].save(OUTPUT, "PDF", resolution=200.0, save_all=True, append_images=pages[1:])
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
