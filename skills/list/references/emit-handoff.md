# Emit and stacked-flag handoff

## Default product

A letter-size inventory PDF named `/home/workdir/artifacts/<YYYY>-<slug>-list.pdf` plus the working folder `/home/workdir/artifacts/list-<slug>/`.

The PDF is a catalog, not a narrative report. Body order is locked in `SKILL.md` step 5.

## Stack order

1. `/list` research and `list.json`
2. `/banner` — every section and every subsection
3. `/images` — mid-section figures only when the 500-word rule earns them; max sharp size; full bleed only when the bitmap already meets the page-width floor
4. Builder (`list` catalog, or `/folio` / `/deep` when those flags are present)
5. `/copyright` living footer

Do not stamp the footer before figures exist. Do not generate figures before `list.json` has real section and subsection titles.

## What this skill is not

- `/corpus` harvests works of one creator
- `/atlas` inventories places as map figures
- `/deep` and `/folio` write argument-driven reports
- `/iterate` enlarges an existing argument

`/list` may hand `items.jsonl` and `sources.jsonl` to those skills when the user stacked them. It does not silently become them.

## Banner contract for list catalogs

Every body section and every taxonomy subsection receives its own generate. The master inventory section is one banner. Each class subsection is another banner. Notes and Bibliography stay bare.

## Image contract for list catalogs

Generate at or above the page-width pixel floor (2550 px wide at letter, prefer 3300 px). Print at 100 percent page width only when that floor is already met. If a candidate raster is narrower, regenerate at the floor. Do not LANCZOS-upscale a small preview across the page. Do not squash aspect to force a height.

## House link

Do not print a house-marks prose sentence. `/copyright` stamps two centered three-dimensional buttons on every page: Digital Marketing Co. (https://DigitalMarketingCo.org) and Web Development Corporation (https://WebDevelopment.tv). Title text equals the visible name. Links open in a new window.
