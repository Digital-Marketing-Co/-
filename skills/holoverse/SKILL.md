---
name: holoverse
display_name: HOLOVERSE
description: HOLOVERSE — immersive year-3629 holographic universe app concept (QAIR v2). Six bilingual EN/ES realms, layered parallax with gyroscope fallback, true three.js voxel mode, zero-inference-credit runtime. Use to build, extend, audit, or integrate HOLOVERSE.
version: "1.0"
author: Digital Marketing Co
type: app-concept
tags: [holoverse, three.js, immersive, holographic, Year 3629]
---
# HOLOVERSE — Six-Realm Holographic Universe

## Purpose
HOLOVERSE is an immersive, optimistic **Year 3629** holographic-universe web experience. Visitors explore six layered cosmic and terrestrial realms with depth parallax (pointer, touch, scroll, and permission-gated gyroscope), holographic-glass UI, and an optional true-3D voxel mode rendered with three.js. The core runtime is deterministic and makes **zero paid LLM/Abacus inference calls**. This skill packages the QAIR v2 master prompt plus the verified standalone build so agents can rebuild, extend, audit, or integrate HOLOVERSE without re-deriving its design.

## Six Realms
| # | Realm (EN) | Reino (ES) |
|---|---|---|
| 1 | Nebular Forge | Fragua de Nebulosa |
| 2 | Ember Plateau | Meseta Ember |
| 3 | Abyssal Core | Núcleo Abisal |
| 4 | Photon Canopy | Dosel de Fotones |
| 5 | Temporal Rift | Grieta Temporal |
| 6 | Crystalline Shore | Orilla Cristalina |

Every realm ships bilingual EN/ES titles and copy and is rendered as an 8-layer parallax composition (stars, nebula, sky, horizon, midground, foreground, particles, lighting). A seeded voxel field gives the true-3D mode.

## Technical stack
- **Vite**: dev server and production bundler (multi-page: `index.html`, `guide.html`)
- **TypeScript**: strict typing; `tsc` build gate
- **three.js**: voxel field and procedural scenes, separate from the 2D parallax
- **vitest**: automated tests
- Source modules in the reference build: `src/app.ts`, `src/realms.ts`, `src/i18n.ts`, `src/parallax.ts`, `src/main.ts`, `src/voxel.ts`, `src/voxel-field.ts`, `src/guide.ts`, `src/tokens.css`

## Verified deliverables
Observed in the build session. These are not guarantees for future changes:
- The standalone HOLOVERSE app (Vite + TypeScript + three.js) was **built** with a clean `tsc` build.
- **7/7 vitest tests pass.**
- `index.html` and `guide.html` both returned HTTP 200 from the local server.
- Re-run `npx tsc --noEmit && npx vitest run && npm run build` after any change. Never claim passes you did not observe.

## Integration note
This skill and the standalone build do **not** change the live site. To add HOLOVERSE as `/apps/holoverse` on **digitalmarketingco.org**, do the work in the **managed app conversation** that owns that Next.js codebase. Follow master prompt §5 (Architecture), §15 (Phased Implementation), and §16 (Deployment / Rollback), and keep the `HOLOVERSE_ENABLED` feature flag.

## References
- [references/master-prompt.md](references/master-prompt.md): verbatim QAIR v2 master prompt (source of truth)
- [references/quality-profile.md](references/quality-profile.md): execution and evidence profile
- [evals/quality-cases.json](evals/quality-cases.json): representative evaluation cases

---

## Master Prompt (full content)

# /QAIR -new HOLOVERSE — Abacus.ai Master Web-Application Prompt (QAIR v2.0.0)

> **Provenance and caveats.** This prompt was generated with the QAIR skill (v2.0.0) from the GitHub repo `Digital-Marketing-Co/-`, branch `main`, commit `7f54d9a`. The HOLOVERSE brief was given as a ChatGPT share link, but that link needs a login and could not be read. **No content from that brief is used here.** The HOLOVERSE concept below is an **assumption**: an immersive, optimistic year-3629 "holographic universe" web experience in which visitors explore layered cosmic and terrestrial realms, with a holographic-glass UI. Replace §0 with the real brief if it differs. No research, tests, deployments, or affiliations are claimed.

---

## 0. Assumed Brief (REPLACE IF THE CHATGPT BRIEF DIFFERS)
| # | Assumption | Status |
|---|---|---|
| A1 | HOLOVERSE is a browser-based immersive universe made of "realms" (cosmic and terrestrial scenes) that users explore through depth parallax, optional gyroscope input, and a true 3D voxel mode. | Assumption |
| A2 | Audience: the general public plus Digital Marketing Co. visitors. Purpose: brand showcase, education, and engagement. | Assumption |
| A3 | Ships as a new route inside digitalmarketingco.org (`/apps/holoverse`) **or** as a standalone app. The target is undecided. | Open question |
| A4 | Core runtime must use no paid LLM/Abacus inference (`-credits zero`). | From QAIR rules plus the user's standing credit-minimization rule |
| A5 | Bilingual EN/ES with an integral guide page, following the project's app-installation rule. | From project decisions |

---

## 1. Mission
Build **HOLOVERSE**: a fast, accessible, breathtaking year-3629 holographic universe where every realm has luminous, layered imagery and responds to pointer, touch, scroll, and (with permission) device orientation. An optional true-voxel mode renders real 3D volumes on the GPU. All core functions are deterministic and need no inference credits. The visual quality must be "museum-grade" without sacrificing Core Web Vitals, WCAG 2.2 AA, or low-end devices.

## 2. Verified Facts and Uncertainties
**Verified (observed in this session):**
- The repo `Digital-Marketing-Co/-` is reachable and synced read-only at `main@7f54d9a`.
- The QAIR skill file is `skills/QAIR/SKILL.md`, v2.0.0.
- A holographic image style lock exists at `skills/book/references/holographic-style.md`: 3300×1856 RGBA, 16:9, gold/violet rim light, and the clause "no caption text, no watermark, no logo".
- The main web app is Next.js, hosted at digitalmarketingco.org and digitalmarketing.abacusai.app (per project records).

**Uncertain / not inspected:**
- The original HOLOVERSE brief, which sits behind the login wall.
- Whether a HOLOVERSE route already exists in the managed web app. That codebase was not inspected in this run.
- Hosting, storage, and bandwidth costs at scale.
- Any device support percentages. None are claimed.

## 3. Competitive Feature-Gap Matrix (category-level, hedged)
Market coverage is **not** exhaustive, and no figures are claimed. Verify each item with live research before acting on it.

| Category / example | Typical strengths | Typical gaps HOLOVERSE can target | Priority |
|---|---|---|---|
| Physical hologram-room venues (e.g. "Holoverse" by Euclideon, Gold Coast; **verify current status**) | True room-scale immersion | Not on the web, needs a venue visit, paid tickets | Differentiator: web access anywhere |
| three.js / WebGL showcase sites (open source, MIT) | Rich 3D, free libraries | Often inaccessible, heavy, no reduced-motion option | Parity plus an accessibility differentiator |
| WebXR experiences | Headset immersion | Narrow device support, fragile permissions | Frontier: optional WebXR entry, Phase 5 |
| Parallax wallpaper / live-wallpaper apps | Gyro depth on phones | Native only, little narrative or education | Parity: gyro parallax with fallback |
| Voxel engines (e.g. MagicaVoxel-style tools, open-source WebGL voxel renderers) | True volumetric scenes | Creator tools, not curated experiences | Differentiator: curated voxel realms |
| Space-education sites (agency galleries, planetarium web apps) | Authoritative content | Static presentation | Differentiator: immersive and educational, with cited facts |

## 4. Prioritized Exhaustive Backlog
**P0 — Must-have**
1. Realm gallery (≥6 realms: 3 cosmic, 3 terrestrial), each with a hero parallax scene, title, short description, and EN/ES copy.
2. Layered parallax engine with 8 layers: stars, nebula, sky, horizon, midground, foreground, particles, lighting. Pointer, touch, and scroll input.
3. Gyroscope mode behind an explicit "Enable motion" button (iOS `DeviceOrientationEvent.requestPermission`). Graceful fallback when denied or unsupported.
4. Reduced-motion compliance: `prefers-reduced-motion` shows a static composed frame, and an in-app motion toggle is always visible.
5. Crossfade transitions between realms (alpha compositing, gradient masks, opacity interpolation).
6. Responsive WebP Q85 assets (+ optional AVIF), lazy loading, and blur placeholders.
7. Holographic-glass UI kit with ≥4.5:1 text contrast on every surface.
8. Integral EN/ES guide page: usage, examples, limitations, TOC, truthful dates, shared OG/Twitter images derived from the same banner artwork.
9. SEO: per-realm metadata, JSON-LD (`WebApplication`, `ImageObject`, `BreadcrumbList`), sitemap entries, and SEO-friendly slugs and filenames.

**P1 — Competitive parity**
10. Guided "Voyage" mode (auto-tour with pause, keyboard skip, and a captions track).
11. Share card per realm (deep link, OG image).
12. Favorites stored in localStorage; no account required.
13. Admin realm manager: CRUD realms, upload layers to S3, reorder, publish/unpublish, preview.
14. Privacy-respecting analytics (aggregate realm views, no PII).

**P2 — Differentiators**
15. True voxel mode: GPU raymarched or instanced-cube voxel volumes (e.g. 128³) per realm, generated deterministically from seeded noise. Clearly separate from the 2D parallax.
16. Deterministic procedural star fields and nebulae (seeded noise shaders). Zero assets, zero credits.
17. Day/night and "epoch" sliders that change lighting uniforms.
18. Ambient soundscape (opt-in, muted by default, volume control).

**P3 — Frontier**
19. WebXR immersive-vr / immersive-ar entry where supported.
20. Multi-realm portal graph (navigable star map).
21. Offline PWA caching of visited realms.

## 5. Architecture
- **Preferred:** a new route group `/apps/holoverse` inside the existing Next.js App Router project (preserve the stack and shared navbar/footer; content sits below the navbar; full-bleed media layer with a constrained content layer). Alternative: a standalone Next.js app.
- Strict TypeScript, React Server Components for realm metadata, and Client Components only for the canvas engine.
- Rendering: CSS transforms + `requestAnimationFrame` for 2D parallax; three.js (MIT) for voxel mode and procedural shaders, dynamically imported and code-split.
- Data: Prisma/PostgreSQL for realms and layers. Uploads go to S3 (never the public bundle). Static generation with ISR for realm pages.
- Caching: immutable hashed asset URLs, `Cache-Control: public, max-age=31536000, immutable` for images, ISR revalidate on admin publish.
- No runtime LLM calls anywhere in the request path.

## 6. Schema / Migrations (Prisma sketch)
```prisma
model HoloRealm {
  id           String   @id @default(cuid())
  slug         String   @unique            // seo-friendly, e.g. "aurora-ocean-terrestrial-realm"
  kind         RealmKind                    // COSMIC | TERRESTRIAL
  titleEn      String
  titleEs      String
  summaryEn    String
  summaryEs    String
  voxelSeed    Int?                         // deterministic voxel generation
  sortOrder    Int      @default(0)
  published    Boolean  @default(false)
  layers       HoloLayer[]
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt
}
model HoloLayer {
  id        String   @id @default(cuid())
  realmId   String
  realm     HoloRealm @relation(fields: [realmId], references: [id], onDelete: Cascade)
  role      LayerRole   // STARS|NEBULA|SKY|HORIZON|MIDGROUND|FOREGROUND|PARTICLES|LIGHTING
  s3Key     String
  width     Int
  height    Int
  depth     Float       // parallax factor 0..1
  altEn     String
  altEs     String
  @@index([realmId, role])
}
enum RealmKind { COSMIC TERRESTRIAL }
enum LayerRole { STARS NEBULA SKY HORIZON MIDGROUND FOREGROUND PARTICLES LIGHTING }
```
Migration is additive only (new tables). Rollback: drop the two tables and enums. No existing tables are touched.

## 7. User Journeys
1. **Visitor (phone):** lands on `/apps/holoverse`, sees a static hero instantly (LCP image), taps a realm, and the parallax responds to touch. Taps "Enable motion", grants permission, and the gyro takes over. If denied, a toast explains the fallback.
2. **Visitor (reduced motion):** gets static composed frames, crossfades replaced by instant swaps, and full content parity.
3. **Keyboard/screen reader:** tabs through the realm cards; arrow keys pan the parallax; each realm has a text description and layer alt text; voxel canvas has `aria-hidden` plus a text equivalent.
4. **Admin:** creates a realm, uploads 8 layers to S3, sets depths, previews, publishes, and ISR revalidates.
5. **Sharer:** copies a realm link; the OG card shows the realm banner derived from the same artwork.

## 8. UI Tokens and 3629 Visual Direction
- Reuse the site's electric-blue brand tokens. Add holographic tokens: `--holo-glass-bg: rgba(10,18,40,0.55)`, `--holo-glass-border: rgba(140,200,255,0.35)`, `--holo-rim-gold: #E8C46A`, `--holo-rim-violet: #8B6CFF`, `--holo-glow: 0 0 24px rgba(120,180,255,0.35)`, `backdrop-filter: blur(16px) saturate(140%)`.
- Typography: the existing site fonts. Display headings tracked slightly wide; body ≥16px.
- Mood: optimistic, luminous, serene. Gold and violet rim light, volumetric god-rays, crystalline architecture coexisting with lush terrestrial nature.
- Hard rules: no overlapping or illegible text over imagery (verify at 390px width); a scrim behind text whenever contrast is below 4.5:1.

## 9. AI Asset Generation and WebP Q85 Pipeline
- **Canvas:** 3300×1856 RGBA, 16:9 (the repo's holographic plate lock). LANCZOS resample if the output size differs; never letterbox.
- **Style clause (from the repo, append to every prompt):** `futuristic cinematic still of the named objects, absolutely beautiful, stunning editorial stock-photo quality, photoreal volumetric lighting, physically based materials, gold and violet rim light, shallow depth of field, razor-sharp focus on the named objects, same lighting family, no caption text, no watermark, no logo, no allegory`
- Generate layers separately on transparent or keyable backgrounds (foreground and midground get alpha; sky and stars are opaque).
- Export: WebP quality 85 at widths 640/1280/1920/3300, plus optional AVIF. Use SEO-friendly names, e.g. `holoverse-aurora-ocean-terrestrial-realm-foreground-1920.webp`.
- Any change to a banner regenerates every derived image (OG, Twitter, thumbnail, listing, hero) from the same artwork.
- Asset generation is a one-time **build-time** cost, separate from runtime (which is zero-credit).

## 10. Parallax and Voxel Engine
- **2D parallax:** 8 layers, each `translate3d(x·depth, y·depth, 0)`, with spring smoothing (critically damped). Input sources are ranked gyro > pointer > touch > scroll. Clamp displacement to ±3% of the viewport. Pause when the tab is hidden or off-screen (`IntersectionObserver`).
- **Crossfade:** two stacked realm compositions; interpolate opacity over 600 ms with a radial gradient mask. Instant swap under reduced motion.
- **Gyroscope:** request permission only on a user gesture. Detect support. Normalize `beta`/`gamma`, calibrate to the initial orientation, and add a dead zone. Fall back silently.
- **Voxel mode (truth rule):** a 2D RGBA WebP is **not** a voxel volume. Voxel mode uses real 3D data: a seeded 3D noise volume rendered with GPU raymarching in a fragment shader, or instanced cubes. Budget: ≤128³ on mobile, adaptive resolution scaling, 30fps floor, auto-disabled when WebGL2 is unavailable.
- **Budgets:** JS for the parallax route ≤80 KB gz before voxel; the voxel chunk is lazy-loaded; ≤8 decoded layers in memory per realm.

## 11. Zero-Inference-Credit Runtime Plan
- No Abacus or paid LLM calls in any user-facing or admin request path.
- Procedural visuals come from deterministic shaders with seeded PRNGs.
- Expenses that remain non-zero and are reported separately: build-time agent work, one-time image generation, hosting, S3 storage, and bandwidth.

## 12. Privacy / Security
- No PII collected. Favorites stay in localStorage. Analytics are aggregate only.
- Device orientation is used locally only and never transmitted.
- Admin routes require existing auth plus RBAC (admin role). S3 uploads use presigned URLs with MIME and size validation (image/webp, image/avif, image/png ≤15 MB).
- Security headers: CSP (allow only self, S3/CDN, and `blob:` for workers), `Permissions-Policy` limited to the needed sensors, plus HSTS, `X-Content-Type-Options`, and `Referrer-Policy`.
- OWASP checks: input validation, IDOR on realm and layer IDs, rate limiting on admin mutations.

## 13. WCAG 2.2 AA / Accessibility
Text contrast ≥4.5:1 (UI ≥3:1); visible focus rings; full keyboard operation; motion toggle (2.3.3, 2.2.2 pause control for auto-tour); no flashing >3/s; target size ≥24×24; alt text for every layer; `lang` switching for ES; captions for Voyage narration; reflow at 320px.

## 14. QA Matrix and Commands
| Area | Test | Method | Pass criterion |
|---|---|---|---|
| Build | Type check and build | `npx tsc --noEmit && npm run build` | Exit 0 |
| Lint | ESLint | `npm run lint` | 0 errors |
| Routes | `/apps/holoverse`, each `/apps/holoverse/[slug]`, guide EN/ES | Playwright HTTP plus render | 200, no console errors |
| Parallax | Pointer/touch/scroll displacement | Playwright synthetic events | Layer transforms change and stay within clamp |
| Gyro | Permission granted/denied/unsupported | Playwright with mocked `DeviceOrientationEvent` | Correct mode and fallback message |
| Reduced motion | `prefers-reduced-motion: reduce` | Playwright `emulateMedia` | No animation; content parity |
| Voxel | WebGL2 present/absent | Playwright, plus headless flag to disable GPU | Renders, or shows the text fallback |
| A11y | axe-core on all routes, EN phone/ES desktop | `@axe-core/playwright` | 0 serious/critical |
| Contrast | Text over imagery at 390/768/1440 | Screenshot plus computed-style check | ≥4.5:1, no overlap/clipping |
| Perf | LCP, CLS, INP | Lighthouse CI (mobile) | LCP ≤2.5s, CLS ≤0.1, INP ≤200ms |
| SEO | Metadata, JSON-LD validity, sitemap | Schema validator script | Valid, unique titles |
| Admin | CRUD, upload, RBAC denial for non-admin | API tests | 2xx for admin, 403 otherwise |
| Security | Headers, IDOR, upload MIME spoofing | curl plus API tests | Headers present; rejections correct |
| Visual regression | Each realm at 3 widths | Playwright snapshots | Within the diff threshold |
| Images | All assets load, WebP served | Crawl for 404s, check content-type | 0 broken |

Report actual pass/fail/blocked counts. Never invent passes.

## 15. Phased Implementation
1. **Phase 1:** schema, migration, admin realm manager, S3 upload, 2 seed realms.
2. **Phase 2:** 2D parallax engine, gyro and fallbacks, reduced motion, crossfades.
3. **Phase 3:** asset pipeline; 6 realms with WebP Q85 variants and derived OG images; EN/ES guide page.
4. **Phase 4:** voxel mode and procedural shaders; Voyage mode; sharing; favorites.
5. **Phase 5 (optional):** WebXR, star-map portal graph, PWA offline.

Run the QA matrix after each phase, cheapest deterministic checks first.

## 16. Deployment / Rollback
- Checkpoint before each phase. Deploy to the main hosts only after type check, build, and the QA gates pass (this follows the project's auto-merge/deploy default).
- Rollback: revert to the prior checkpoint. The migration is additive (drop the tables if needed). The feature flag `HOLOVERSE_ENABLED` hides the route instantly.

## 17. Acceptance Criteria
- ≥6 published realms render on phone and desktop in EN and ES, with no console errors.
- Parallax responds to pointer, touch, and scroll; gyro works after permission and falls back cleanly.
- Reduced-motion users get full content with no animation.
- Voxel mode renders true 3D volumes where WebGL2 is supported, with a text fallback otherwise.
- axe reports 0 serious/critical; contrast ≥4.5:1; no overlapping text at 390px.
- Lighthouse mobile meets LCP ≤2.5s, CLS ≤0.1, INP ≤200ms on the realm index.
- Zero runtime inference calls (verified by a network log review).
- The guide page is published EN/ES with truthful dates and derived images.

## 18. Evidence Report (to be filled by the executing agent)
| Item | Result |
|---|---|
| Commands executed | — |
| Routes tested | — |
| Pass / Fail / Blocked | — |
| Screenshots | — |
| Changed files | — |
| Unresolved issues | — |
| Deployment URL (observed) | — |
| Rollback checkpoint | — |

---

## Copy-Ready Abacus.ai Execution Directive
> Inspect the existing Digital Marketing Co. Next.js app and its shared layout and design tokens first; preserve all working features. Implement HOLOVERSE per §4–§17 in the phases of §15, as an additive `/apps/holoverse` route group behind the `HOLOVERSE_ENABLED` flag. Store uploads in S3 and keep content below the navbar. Use no paid LLM/Abacus inference at runtime. Generate imagery at build time only, with the §9 canvas and style clause, WebP Q85 responsive variants, SEO-friendly filenames, and derived OG/Twitter images. Treat 2D WebP and true voxel volumes as distinct. Request gyroscope permission only on a user gesture, with fallbacks. Meet WCAG 2.2 AA and the Core Web Vitals budgets. Run the §14 QA matrix deterministically and report only observed results in §18. Never invent APIs, credentials, test passes, or deployment success. Checkpoint, then deploy to the main hosts once all gates pass.
