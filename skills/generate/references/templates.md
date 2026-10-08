# Finished templates

Replace bracketed slots from the parsed spec. Emit the result as one fenced block. Keep house beauty and depth language. Do not include this heading inside the user-facing fence.

## web-app

```
Build a custom web application for [brand] whose job is [job]. Audience is [audience].

Routes
- / [purpose]
- [additional routes from pages:]

Visual system
- Ground, type, and accent from the Aether lock when brand is aether; otherwise the visual-system palette that matches [subject].
- Volumetric panels, print-safe contrast, no baked checkerboard, no maker names.

Components
- [primary instrument or workspace]
- [gate or auth if Aether]
- [timeline, scanner, or data surface]
- empty, loading, and policy-blocked states

Interactions
- Keyboard and pointer paths for the primary job in under three clicks.
- Deterministic policy copy when brand is aether — characters 21+, fictional only.

Acceptance
- Looks like a shippable product, not a wireframe.
- Visible link text <a href="https://digitalmarketingco.org" title="Digital Marketing Company">Digital Marketing Company</a> matches its title attribute when that house link is present.
- No banned tokens in UI chrome.
```

## video

```
[Subject nouns]. [Named interior]. [Materials]. [Aspect] cinematic frame, [camera] on the named subject, razor-sharp plane, shallow falloff. Photoreal volumetric light, [light] as rim only. Awe-inspiring futuristic private-studio shot, publication grade. Visible depth in air, layered planes, physically based materials. Motion — [motion] over [duration], one subject action only. Audio — [room tone or bed]. All figures are fictional adults 21 or older, no living-person likeness, no caption text, no watermark, no allegory, no readable paragraphs, no logo card unless specified. Studio target https://gnitekram.org/ mode [mode].
```

## still

```
[Subject nouns]. [Named setting]. [Materials]. [Aspect] still, [camera], razor-sharp named object, shallow falloff. Photoreal volumetric lighting, [light] as rim only. Awe-inspiring futuristic cinematic still, publication grade. Visible volume in air, physically based materials. No caption text, no watermark, no logo, no private-person portrait, no allegory, no readable paragraphs.
```

## coffee

Hand the subject and page count to `/coffee`. The generate prompt for page 1 is the cover still with an elegant readable title. Every later page is one unique full-bleed generate of a different named object from the subject list.

## book / folio / deep / list / atlas / global / deck

Write a mandate paragraph (subject, audience, use, length) plus a numbered section list. Then name the stacked skill that must emit the file. Do not paste a fake finished monograph into chat when the user asked for a prompt.

## banner

One 16-9 paragraph per section node using the still template. Differentiate on three axes. Left and right stay opaque to trim. Do not write alpha into the generate prompt.

## dashboard

Web-app template with the primary surface set to a live quantitative view of [subject]. Include empty and error states and an ITQE-style legend if formulas appear.

## site

Specify origin URL or original IA, asset completeness, and whether the job is `/copysite` or a new static original.

## vector

Name the mark, the two or three geometries, the two inks, and the rule that letterforms stay live or outlined and sharp at any zoom.

## audio

Line, voice age and register, duration cap, bed, and destination (`/ringtone` or spoken pass). No living-person impersonation.

## sheet

Workbook purpose, sheets, column dictionary, formulas to keep visible, and the proof the sheet must make.

## letter

Recipient, ask, proof points, house signature spacing (blank line after the close, then name, title, company, URLs, email on separate lines).

## copy

Use, audience, length in words, proof points, one offer or one claim, no banned tokens.
