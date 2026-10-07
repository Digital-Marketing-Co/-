# Heading keep-with-next

A section, subsection, or subsubsection heading that is not followed by paragraph text on the same page is an orphan heading. Move that heading to the next page before delivery.

## Rule

- A heading counts as followed by paragraph text only when at least the first two lines of a body paragraph sit on the same page, under that heading.
- A heading followed only by another heading, a rule, a spacer, a banner, a caption, or a page footer is not followed by paragraph text.
- Move the orphan heading, and any immediately following headings that also lack a paragraph, onto the next page as one chain. The first heading in the chain must open that page with its paragraph.
- Do not leave a heading as the last text block on a page.
- Running headers, footers, page numbers, the title-leaf display title, and TOC entry lines are not section headings for this rule.

## Builder contract

ReportLab and equivalent flow builders:

1. Set `keepWithNext = True` on every heading flowable.
2. The next flowable after a heading must be the first body paragraph, not a spacer or rule. If a banner is required, place it after the first paragraph or keep the heading-plus-paragraph pair together and put the banner above the heading on the new page.
3. Before placing a heading, measure remaining frame height. If it is less than heading height plus two body lines (about 2.4 times body leading), insert a page break before the heading.
4. A heading whose section has no paragraph yet is unfinished. Do not ship it at the bottom of a page while the paragraph is still empty.

DOCX: heading styles use keep-with-next, and the following paragraph is not page-break-before. PPTX: do not end a slide on a heading with no body. HTML/print: `break-after: avoid` and `page-break-after: avoid` on `h1`–`h3`, with the next `p` kept.

## Scan

```bash
python3 /root/.grok/server-skills/latex/scripts/scan_orphan_headings.py \
  --pdf /home/workdir/artifacts/<file>.pdf
```

Exit code 1 blocks delivery. Rebuild with the page break in front of the orphan heading, then scan again.
