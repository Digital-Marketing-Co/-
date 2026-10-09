---
name: coffee
description: Compile a landscape coffee-table PDF of full-bleed generated stills after the user types /coffee plus a subject and an optional page count. Use when the user types /coffee, asks for a coffee table book, a full-bleed picture book, or a large-format image album with no page margins. Page one is a unifying cover still with an elegant readable title. Every page is one unique full-bleed generate that fills the trim on top, right, left, and bottom. A rerun appends another full iteration of stills to the same book.
metadata:
  type: workflow
  version: "4.1"
  flag: /coffee
  owner: Web Development Corporation
  visual_stack: visual-system
---

# /coffee

Compile one landscape coffee-table PDF. Every printed page is a single generated still drawn at x = 0, y = 0, width = page, height = page, with a 1.5 pt overscan so no viewer hairline shows paper. No text inset. No side gutter. No letterbox. No top or bottom paper band. No alpha ramp on any edge. No visible footer.

Skill path is `/root/.grok/server-skills/coffee`.

Documents this skill emits follow `/root/.grok/server-skills/visual-system/SKILL.md` for palette and depth only. Coffee pages override the publication bar where that bar would corrupt bleed: do not stamp a footer, do not add an alpha ramp, do not inset the still. Copyright stays in document info. The cover company line is the only printed company text.

Generate prompts append the beauty lock in `references/prompts.md`. Every still is a fresh generate. No stock download. No reused path, hash, or prompt.

Read on demand

- `references/geometry.md` — locked page, four-edge bleed, no mask punch-out
- `references/cover-title.md` — cover still plus composited title, skill-local faces
- `references/prompts.md` — scene split and beauty lock
- `references/uniqueness.md` — fail-closed path, byte, and prompt audit
- `references/html-link.md` — Digital Marketing Company HTML snippet and PDF click target
- `references/iteration.md` — 24 new pages per run, append on rerun

If the user only asked to create or edit this skill and supplied no subject, stop after the skill files exist. Do not invent a book.

## When this skill runs

- User typed `/coffee` followed by a subject, with or without a page count.
- User asked for a coffee table book, a full-bleed picture book, or a large-format image album with no margins.
- User asked to fill every page edge with a generated still.
- User reran `/coffee` on a subject that already has a book. Append. Do not replace.

If there is no subject and no existing book, ask what they want to see. Do not invent a theme.

## Parse the command

```bash
python3 /root/.grok/server-skills/coffee/scripts/parse_coffee_request.py \
  "/coffee SUBJECT" \
  --existing /workspace/artifacts/<slug>/coffee.json
```

The helper prints `subject`, `page_count`, `pages_this_iteration`, `append`, `mode`, and `slug`.

Iteration ceiling is 24 new full-bleed pages. That is the maximum this run can return. Do not plan fewer unless the user named a smaller count.

- No integer: add 24 pages.
- Named count of 2 through 24: add that many.
- Named count above 24: add 24 this run and say what remains.
- Existing `coffee.json` for the same slug: `append` is true. Add another ceiling of pages. Keep every earlier still.

A number is a page count only when it is the last token or it sits next to the word page. Interior numbers stay in the subject.

`page_count` is the book total after this run. Page 1 is the cover. Later pages are leaves.

## Workflow

### 1. Plan scenes

Write or extend `coffee.json` before any generate.

- `title` — short book title, 3 to 8 words, derived from the subject. Not a sentence.
- `subtitle` — optional one line, at most 12 words.
- `subject` — raw user subject.
- `mode` — landscape, square, or portrait.
- `page_count` — integer after this run.
- `pages` — one object per still that will print.

Page 1, first run only

- `role` = `cover`
- `scene` = the single still that belongs to the whole subject at once.
- `prompt` = cover prompt from `references/prompts.md`

Leaves

- `role` = `leaf`
- One distinct scene per new page. Change vantage, hour, weather, named object, or scale.
- On a rerun, do not repeat a scene or prompt already in `coffee.json`.
- Each prompt names concrete visible objects from the subject. Futuristic light is a treatment of those objects, not a subject swap.

Append with:

```bash
python3 /root/.grok/server-skills/coffee/scripts/extend_book.py \
  /workspace/artifacts/<slug>/coffee.json \
  --add /tmp/coffee-add.json
```

`coffee-add.json` is a list of `{scene, prompt}`. The helper refuses a prompt already on the book.

### 2. Generate stills

One generate call per new page. Orientation is landscape unless the user asked for square or portrait. Generate the whole iteration in parallel waves. Do not stop after a handful. If a call fails, retry that page once, then continue. Bind only pages that received a still.

Save raw files as `stills/raw-NN.png`. Fit each one:

```bash
python3 /root/.grok/server-skills/coffee/scripts/fit_still.py \
  stills/raw-NN.png stills/fit-NN.png --mode landscape
```

Fit cover-crops to 3600 x 2700. It does not pad. Exit 1 means a light paper bar survived; generate that page again.

Record `fitted` on the page object. Do not print the raw path.

### 3. Cover type

First run only. Faces and the command are in `references/cover-title.md`. The title must stay easy to read on a lower-third veil. Interior leaves stay pure stills. Do not composite running text on leaves. Do not stamp a footer band.

### 4. Build the PDF

```bash
python3 /root/.grok/server-skills/coffee/scripts/build_coffee_pdf.py \
  /workspace/artifacts/<slug>/coffee.json \
  --out /workspace/artifacts/<Title_Slug>_Coffee.pdf
```

The builder cover-crops again, flattens alpha onto the image, and draws each still past the trim with `mask` left unset. Do not pass `mask="auto"`. That flag was punching highlights into white holes.

A link annotation over the cover title block opens `https://digitalmarketingco.org`. Visible anchor text and title attribute stay Digital Marketing Company. Plain domain text is DigitalMarketingCo.org.

Write `coffee-link.html` in the slug folder. The builder does this.

Living copyright goes in document info only. Owner is Web Development Corporation. Do not draw a footer rule on the stills.

### 5. Uniqueness audit

```bash
python3 /root/.grok/server-skills/coffee/scripts/audit_unique_images.py \
  /workspace/artifacts/<slug>/coffee.json
```

Exit code 1 blocks delivery. Replace each colliding still and audit again.

### 6. Visual QA

```bash
pdftoppm -png -r 40 /workspace/artifacts/<Title_Slug>_Coffee.pdf /tmp/coffee-page
```

Inspect every page. Rebuild when any of these appear:

- white or cream bars on any edge
- letterbox, pillarbox, or side gutter
- bright holes where highlights were punched out
- repeated stills
- unreadable cover title
- baked caption type inside a generate
- U+FFFC, tofu, empty boxes, or raw TeX
- checkerboard baked into RGB

Write `stills/qa.md` with the hash table and the pass or fail line.

### 7. Deliver

Deliver the PDF plus `coffee-link.html`. Render the PDF for the user. On a rerun, deliver the rebuilt book with the new pages included, and say how many pages were added.

## Geometry lock

Default page is landscape 12 in wide by 9 in tall. 300 dpi source is 3600 x 2700 px. PDF points are 864 x 648.

Optional overrides only when the user names them in the same turn:

- `square` — 11 x 11 in, source 3300 x 3300
- `portrait` — 9 x 12 in, source 2700 x 3600

Never mix sizes inside one book.

## What used to corrupt the file

- PDF image draw used `mask="auto"`, so near-white pixels became holes.
- Draw stretched or letterboxed instead of cover-cropping to the trim.
- Cover faces pointed at a font tree that is not installed, so the title fell back to a bitmap face.
- Page budget stopped at 12 or 40, and a rerun replaced the book instead of adding pages.
- Uniqueness and HTML notes pointed at `/home/workdir`, so the audit never ran on this host.
- Publication-bar footer and alpha-ramp rules were being applied to stills, which paints paper over the bleed.

## Publication bar, coffee override

Fail closed on a missing still, a shared hash, a shared prompt, a paper bar, or an unreadable cover title. Do not apply these publication-bar items to coffee pages: alpha ramp on the top and bottom, one copyright notice drawn in the footer, heading keep-with-next. Those insert paper and type into the bleed. Copyright stays in document info. The house link is the cover annotation plus `coffee-link.html`.

## Delivery sweep

Run this once, last, after every other section.

1. Resolve the negative skill at `/root/.grok/server-skills/negative`.
2. Extract visible text from chat, the PDF info, captions, and filenames.
3. Run `python3 /root/.grok/server-skills/negative/scripts/sweep_negative.py` on that text.
4. Exit 1 blocks delivery. Rewrite every hit so the sentence still reads as English. Re-scan until CLEAN.
5. Verbatim user source and the blocklist file itself are the only carve-outs.
