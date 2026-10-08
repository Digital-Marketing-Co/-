"""LOCKED TYPE AND PAGE GEOMETRY for /print.

Same owner and type stack as /folio. Page frame is full-bleed so images
can touch trim; text uses TEXT_INSET_IN.
"""

from pathlib import Path

FONT_DIR = Path(__file__).resolve().parent / "fonts"

DISPLAY = "EBGaramond"
DISPLAY_BOLD = "EBGaramond-Bold"
DISPLAY_ITALIC = "EBGaramond-Italic"
DISPLAY_BOLDITALIC = "EBGaramond-BoldItalic"

BODY = "Literata"
BODY_BOLD = "Literata-Bold"
BODY_ITALIC = "Literata-Italic"
BODY_BOLDITALIC = "Literata-BoldItalic"

CHROME = "LibreFranklin"
CHROME_BOLD = "LibreFranklin-Bold"
CHROME_ITALIC = "LibreFranklin-Italic"
CHROME_BOLDITALIC = "LibreFranklin-BoldItalic"

TITLE_PT = 26
SUBTITLE_PT = 13
H1_PT = 16
H2_PT = 13.5
H3_PT = 12
BODY_PT = 11.5
CAPTION_PT = 9.5
KICKER_PT = 8.5
FOOTER_PT = 8
COPYRIGHT_PT = 8

TITLE_LEADING = 32
SUBTITLE_LEADING = 18
H1_LEADING = 21
H2_LEADING = 18
H3_LEADING = 16
BODY_LEADING = 17
CAPTION_LEADING = 13
FOOTER_LEADING = 11

PAGE_WIDTH_IN = 8.5
PAGE_HEIGHT_IN = 11.0
TEXT_INSET_IN = 0.85
MARGIN_TOP_IN = 0.70
MARGIN_BOTTOM_IN = 0.70
BANNER_HEIGHT_IN = 3.15
FIGURE_MAX_HEIGHT_IN = 4.6
HEADING_KEEP_IN = 1.40
PRINT_DPI = 300

INK = "#1A1916"
MUTED = "#4A4742"
RULE = "#2C2A26"
RULE_SOFT = "#B7B1A6"
CREAM = "#FBF7F0"
LINK = "#1F3A5F"

OWNER_LEGAL = "Web Development Corporation, a Delaware Corporation"
OWNER_SHORT = "Web Development Corporation"
OWNER_FOUNDED = 2012

HOUSE_ANCHOR = "Digital Marketing Co."
HOUSE_HREF = "https://digitalmarketingco.org"
HOUSE_DOMAIN = "DigitalMarketingCo.org"
HOUSE_PUBLICATION_PATH = "/print"

COPYRIGHT_FIELD = "WCACopyrightYear"
