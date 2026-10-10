"""LOCKED STATIC TYPE SCALE for /deep.

These numbers are the contract. Do not recompute, scale, or "improve" them
at runtime. They are exactly double the house monograph scale that
phd-ivy-monograph would have used (11/13/22/9.5/8 -> 22/26/44/19/16).

Face: bundled Gelasio (SIL OFL), metrics-compatible with Georgia, registered
in the PDF under the family name Georgia so every style sheet says Georgia.
"""

# Typeface family name used in ReportLab styles (do not rename).
FONT_FAMILY = "Georgia"
FONT_REGULAR = "Georgia"
FONT_BOLD = "Georgia-Bold"
FONT_ITALIC = "Georgia-Italic"
FONT_BOLDITALIC = "Georgia-BoldItalic"

# Point sizes — locked static integers.
TITLE_PT = 44
SUBTITLE_PT = 26
H1_PT = 26
H2_PT = 24
BODY_PT = 22
ABSTRACT_PT = 22
NOTE_PT = 19
BIBLIO_PT = 22
CAPTION_PT = 19
KICKER_PT = 18
FOOTER_PT = 16
PAGENUM_PT = 16

# Leadings (pt) — locked at 1.36–1.45 × size so 22 pt body still sets.
TITLE_LEADING = 52
SUBTITLE_LEADING = 34
H1_LEADING = 34
H2_LEADING = 32
BODY_LEADING = 32
ABSTRACT_LEADING = 32
NOTE_LEADING = 26
BIBLIO_LEADING = 32
CAPTION_LEADING = 26
FOOTER_LEADING = 20

# Page geometry — letter, locked.
PAGE_WIDTH_IN = 8.5
PAGE_HEIGHT_IN = 11.0
MARGIN_LEFT_IN = 0.85
MARGIN_RIGHT_IN = 0.85
MARGIN_TOP_IN = 0.70
MARGIN_BOTTOM_IN = 0.70

# Banner geometry consumed by /banner — locked.
BANNER_BLEED_WIDTH_IN = 8.5          # full page width, left and right bleed
BANNER_CONTENT_HEIGHT_IN = 2.35      # visible band
BANNER_FADE_IN = 1.0                 # top inch and bottom inch alpha fade
BANNER_TOTAL_HEIGHT_IN = 4.35        # 1.0 + 2.35 + 1.0

# Placeholder tracking URL pattern. Replace later with the SEO title URL
# of the matching synthesis node. {section_id} is required.
BANNER_HREF_TEMPLATE = (
    "https://DigitalMarketingCo.org/r/?src=deep-banner&section={section_id}"
)
