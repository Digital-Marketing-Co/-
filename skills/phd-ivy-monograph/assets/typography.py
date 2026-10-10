"""LOCKED TYPE SCALE for the unified WCA compact Ivy report.

Do not recompute, scale, or "improve" these numbers at runtime.

Stack (unchanged families; compact sizes)
- Display (title, part heads): EB Garamond
- Body, abstract, notes, bibliography: Literata 18pt optical, set at 10 pt
- Chrome (kicker, running header, footer, copyright field): Libre Franklin

v1 Folio set body at 11.5/17. v2 compact is a university-press /
think-tank working-paper measure: 10/14.2 on a 6.55-inch column,
about 68–74 characters. Display drops from 26 to 20 so the title
leaf does not shout over the argument.

All three families are SIL OFL 1.1 and bundled under assets/fonts/.
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

# Point sizes — locked compact scale (v2).
TITLE_PT = 20
SUBTITLE_PT = 11
H1_PT = 13
H2_PT = 11
BODY_PT = 10
ABSTRACT_PT = 9.5
NOTE_PT = 8
BIBLIO_PT = 9
CAPTION_PT = 8
KICKER_PT = 7.5
FOOTER_PT = 7
PAGENUM_PT = 7
COPYRIGHT_PT = 7
PAGE_FOOTNOTE_PT = 7.5
META_PT = 9

# Leadings (pt).
TITLE_LEADING = 24
SUBTITLE_LEADING = 15
H1_LEADING = 16.5
H2_LEADING = 14
BODY_LEADING = 14.2
ABSTRACT_LEADING = 13.5
NOTE_LEADING = 11
BIBLIO_LEADING = 12.5
CAPTION_LEADING = 11
FOOTER_LEADING = 9.5
PAGE_FOOTNOTE_LEADING = 10

# Page geometry — letter.
PAGE_WIDTH_IN = 8.5
PAGE_HEIGHT_IN = 11.0
MARGIN_LEFT_IN = 0.95
MARGIN_RIGHT_IN = 0.90
MARGIN_TOP_IN = 0.70
MARGIN_BOTTOM_IN = 0.62
FOOTNOTE_BAND_IN = 1.12
COPYRIGHT_BAND_IN = 0.58

# Colors — warm academic cream on near-black ink. Body contrast exceeds WCAG AAA.
INK = "#1A1916"
MUTED = "#4A4742"
RULE = "#2C2A26"
RULE_SOFT = "#B7B1A6"
CREAM = "#FBF7F0"
LINK = "#1F3A5F"

OWNER_LEGAL = "Web Development Corporation, a Delaware Corporation"
OWNER_SHORT = "Web Development Corporation"
FOOTER_OWNER = "Web Development Corporation"
OWNER_FOUNDED = 2012

HOUSE_ANCHOR = "Digital Marketing Company"
HOUSE_HREF = "https://DigitalMarketingCo.org"
HOUSE_DOMAIN = "DigitalMarketingCo.org"
HOUSE_PUBLICATION_PATH = "/white-papers"

COPYRIGHT_FIELD = "WCACopyrightYear"
STYLE_TOKEN = "WCA Compact Ivy"
STYLE_VERSION = "2.0"
