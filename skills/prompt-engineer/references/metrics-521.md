# 521 auditor metrics

Lock these checks to every HTML route `/PromptEngineer` writes.
They implement the twelve dimensions of https://digitalmarketingco.org/free-website-auditor.
Do not claim a live 100 score unless an external run exists. Self-score honestly.

Dimensions — SEO, Performance, Mobile, Security, Accessibility, AI Readiness, AIO, GEO, AEO, Local SEO, Schema.org, WCAG.

Total checks — 521.

## SEO (48)

1. Unique title tag 50-60 characters
2. Title includes primary intent phrase
3. Title is not duplicated across routes
4. Meta description 150-160 characters
5. Meta description unique per route
6. Meta description contains a verb and an outcome
7. Single H1 matching page intent
8. H1 is not the same string as every other H1
9. Heading outline is sequential H1-H2-H3
10. No skipped heading levels
11. Canonical link present and absolute
12. Canonical is self-referential unless a true duplicate exists
13. Robots meta allows indexing when the page is public
14. X-Robots-Tag does not contradict robots meta
15. Clean slug with hyphens not underscores
16. Slug length under 75 characters
17. No session IDs in public URLs
18. HTTPS URL only in internal links
19. Internal links use descriptive anchors
20. No click-here only anchors
21. Primary keyword appears in first 100 words
22. Primary keyword appears in one H2
23. Image filenames are descriptive slugs
24. Every content image has alt text
25. Decorative images use empty alt
26. Pagination uses rel next prev when paged
27. XML sitemap entry exists for the route
28. Sitemap lastmod is ISO date
29. Robots.txt allows the route
30. Favicon link present
31. Apple touch icon present
32. Theme-color meta present
33. Language attribute on html
34. Hreflang only when locales exist and reciprocal
35. No keyword stuffing in title
36. No doorway-page parameter sets
37. 404 does not return 200
38. Redirects are single-hop 301
39. Trailing-slash policy is consistent
40. WWW policy is consistent
41. Breadcrumb visible when depth > 1
42. BreadcrumbList JSON-LD matches visible crumbs
43. Outbound links that leave the site are intentional
44. Sponsored or UGC links use rel where required
45. Print and screen content are the same intent
46. No hidden text for ranking
47. Primary CTA is crawlable as a link or button
48. Page is reachable from nav or footer within two clicks
## Performance (42)

49. LCP target under 2.5s on 4G mid-tier
50. INP target under 200ms
51. CLS target under 0.1
52. TTFB target under 800ms
53. Speed Index considered in hero choice
54. Hero image has width and height attributes
55. Hero image is modern format WebP or AVIF with fallback
56. Hero fetchpriority high when it is LCP
57. Below-fold images lazy-load
58. Lazy-load is not applied to LCP image
59. Background video not required for first paint
60. CSS critical path is small or inlined with care
61. No render-blocking unused CSS payload over budget
62. Fonts use font-display swap or optional
63. Font files subset to used glyphs when possible
64. Preconnect for required origins only
65. Preload only for true critical assets
66. No more than one webfamily without reason
67. JavaScript deferred or typed module
68. No unused analytics tags on first paint
69. Third-party scripts after interactive content
70. Animation uses transform and opacity only
71. No layout-thrashing hover on large trees
72. Images compressed without visible banding
73. SVG icons preferred for UI chrome
74. Cache headers planned for static assets
75. HTML is not a 2MB document
76. JSON data for menus is cacheable
77. No document.write
78. No synchronous XHR on first load
79. Mega menu is not a 200-node paint on load if closed
80. Closed menu content can be deferred
81. Reduced-motion path avoids continuous GPU work
82. RequestAnimationFrame not polling when hidden
83. 404 page is static-fast
84. Footer accordion JS is small
85. No infinite animation when tab is backgrounded
86. Responsive images use srcset when multiple densities exist
87. Avoid layout shift from webfont swap on H1
88. Avoid layout shift from mega menu open
89. Avoid layout shift from accordion expand on first paint
90. Total blocking time considered when adding motion libraries
## Mobile (36)

91. Viewport meta width device-width initial-scale 1
92. No user-scalable no unless a map exception is documented
93. Tap targets at least 44x44 px
94. Spacing between adjacent targets at least 8 px
95. No horizontal scroll at 320 px
96. No horizontal scroll at 375 px
97. No horizontal scroll at 390 px
98. Readable type at 16 px minimum for inputs
99. Menu usable with one thumb on 390 px
100. Off-canvas menu covers and can be dismissed
101. Sticky header does not eat half the viewport
102. Forms do not zoom unexpectedly on iOS
103. Input types match data (email tel url)
104. Autocapitalize and autocomplete set where useful
105. Click-to-call uses tel links when a number is shown
106. Maps links open a native map when an address is shown
107. Images do not overflow the content well
108. Tables scroll inside a region if present
109. Mega menu becomes accordion under 768 px
110. Footer accordion is the mobile footer pattern
111. Focus is visible on iOS Safari
112. Hover-only actions have a tap equivalent
113. Safe-area insets respected on notched phones
114. Landscape phone still usable
115. 768 px tablet layout is a real mid layout
116. Touch callout and selection do not break buttons
117. Disabled pinch only if a custom zoom control exists
118. App icons and tiles are not letterboxed
119. Theme color matches the header field
120. No Flash or plugin content
121. Fixed position elements do not collide with the home indicator
122. Virtual keyboard does not hide the submit control without scroll
123. Content reflows not shrink-to-fit text
124. Contrast holds in outdoor brightness (avoid hairline gray type)
125. Gestures are not the only way to open Apps
126. Pointer coarse media query used for hit targets when needed
## Security (50)

127. All asset URLs are HTTPS
128. No mixed content
129. No inline API keys or tokens in JS
130. No secrets in HTML comments
131. No secrets in data-* attributes
132. External scripts use integrity when pinned
133. External scripts use crossorigin when needed
134. Target blank links include relnoopener noreferrer
135. Forms POST over HTTPS
136. Search fields do not reflect unsanitized HTML
137. InnerHTML not fed raw query strings
138. JSON parse of local data is trusted local only
139. CSP planned — default-src self plus documented extras
140. CSP does not rely on unsafe-eval unless documented
141. Referrer-Policy is set
142. X-Content-Type-Options nosniff planned
143. Frame ancestors deny or same origin unless embed is required
144. Permissions-Policy disables unused powerful APIs
145. No open redirect on next= parameters
146. 404 does not echo raw path as HTML
147. User-generated names are escaped
148. SVG uploads not accepted without sanitize
149. CORS not set to star for credentialed routes
150. Cookies that exist are Secure and SameSite
151. Session cookies HttpOnly
152. No autocomplete on on secret fields if any
153. Admin routes not linked in public nav
154. Source maps not published on production if they leak internals
155. Directory listing disabled on static hosts
156. Well-known security.txt optional but not contradictory
157. Dependency URLs are known CDNs
158. Tailwind CDN noted as a build-time risk and replaced in production when possible
159. No eval
160. No new Function on user strings
161. PostMessage origins checked if used
162. WebSocket endpoints wss only if used
163. File download links have correct Content-Disposition when applicable
164. Rate-limit contact forms if present
165. Honeypot or time-trap on public forms
166. CSRF token on state-changing forms
167. Auth surfaces not exposed by the menu if they must stay private
168. Error text does not leak stack traces
169. Server version headers not advertised in copy
170. Subresource integrity documented in README when CDN is used
171. Third-party pixels listed in a privacy note
172. No password in query string ever
173. No token in hash unless the protocol requires it
174. Clickjacking considered for embeddable widgets
175. Supply-chain scripts inventoried
176. OWASP path — no obvious IDOR in demo IDs
## Accessibility (48)

177. Skip link is first focusable control
178. Landmarks header main footer nav present
179. Only one banner landmark
180. Nav labels distinguish primary and footer
181. Main contains the H1
182. Buttons are button elements
183. Links are a elements with href
184. Menu button has aria-expanded
185. Menu button has aria-controls
186. Open menu uses aria-modal when it is a dialog
187. Escape closes the mega menu
188. Focus returns to the Apps button on close
189. Focus is trapped only while the mobile sheet is open
190. Arrow keys move among top-level items where a menubar pattern is used
191. If not a menubar, Tab order is documented and complete
192. aria-current page on the active route
193. Icons that convey meaning have accessible names
194. Purely decorative icons are hidden from AT
195. Form fields have labels
196. Error messages are associated with fields
197. Required fields announced
198. Color is not the only error signal
199. Focus visible 3:1 against adjacent colors
200. Text contrast 4.5:1 for body
201. Large text contrast 3:1
202. UI component contrast 3:1
203. Hit target 44 px
204. No keyboard trap outside the intentional dialog trap
205. Tabindex not greater than 0
206. Positive tabindex avoided
207. Heading text is unique enough to scan
208. Lists are ul or ol not div soup
209. Accordion headers are buttons
210. Accordion aria-expanded reflects state
211. Reduced motion honored
212. Autoplay motion stops under reduced motion
213. Language of passages marked if mixed
214. Page language is English unless specified
215. Charts if any have text equivalents
216. Captions for any video
217. Transcript or description for any audio
218. Live regions used sparingly for menu state if needed
219. Status messages are not toast-only
220. Name role value works on custom controls
221. Do not rely on title tooltips for essential info
222. Touch and keyboard can reach every app link
223. 404 heading is announced as the page title too
224. Footer accordion is operable with VoiceOver rotor
## AI Readiness (40)

225. Machine-readable title distinct from brand-only strings
226. First paragraph answers what the page is
227. Entity of the organization is named in text
228. SameAs candidates exist for the brand
229. JSON-LD Organization or WebSite present on chrome pages
230. JSON-LD WebPage present on each route
231. Author or publisher named when content is editorial
232. Dates in ISO when dates exist
233. FAQ material uses question and answer prose not only headings
234. No contradictory claims between title and H1
235. Primary entity mentioned before decorative copy
236. App names are consistent strings across nav apps footer 404
237. Abbreviations expanded once
238. Units and numbers written plainly
239. Tables have headers if quantitative
240. Code samples not required on marketing chrome
241. Crawlable text not only canvas
242. Important links are in HTML not only JS click handlers
243. Hash routes not used as the only public URL
244. Canonical helps engines pick the app URL
245. llms.txt considered for the site root
246. robots allows GPTBot and Google-Extended unless policy forbids
247. Policy forbids recorded in robots if bots are blocked
248. OG tags give engines a clean card
249. Image alt is literal so multimodal models can ground
250. No text baked into OG that contradicts the title
251. Contact path is a real URL
252. About path is a real URL when claimed
253. Brand name Digital Marketing Company appears as that string
254. Domain string DigitalMarketingCo.org used when the domain is written
255. Auditor URL cited only when the page is about the auditor
256. No fake statistics in copy
257. No unsourced 100 scores claimed
258. Structured data validates as JSON
259. Structured data types match visible content
260. No JSON-LD for reviews that do not exist
261. No JSON-LD for prices that do not exist
262. Breadcrumb entities match visible labels
263. Speakable not claimed unless a true speakable block exists
264. Content is extractable without executing a 3D scene
## AIO (42)

265. Page answers one primary question in the first screen
266. Definitions are explicit sentences
267. Entities are introduced with a type (app, service, page)
268. E-E-A-T — organization named as operator
269. E-E-A-T — contact path available
270. E-E-A-T — no anonymous medical or legal claims
271. Chunkable sections with H2 that can stand alone
272. Lists used for inventories not for prose paragraphs
273. App blurbs are one-sentence facts
274. No synonym stuffing that confuses the entity
275. Consistent casing for product names
276. Internal links use the same anchor for the same target
277. Avoid pronoun-only first sentences
278. Avoid we-statement walls with no noun
279. Dates of update in visible text when the page is a living tool
280. Versioning not required for static chrome
281. Citations when a third-party metric is named
282. Auditor named with its real URL when referenced
283. No hidden prompt instructions in HTML comments
284. No model-facing jailbreak strings
285. Alt text is not keyword lists
286. Captions if used add data not duplicate the heading
287. Summary block for long app catalogs
288. Machine sitemap of apps in JSON
289. Human sitemap of apps in HTML
290. Duplicate content between menu and /apps is exact not paraphrased names
291. Paraphrase allowed only in blurbs
292. Safety copy present if the app domain requires it
293. Age gate only if the remainder requires it
294. Localization hooks documented if Spanish pages exist
295. Do not invent Spanish copy unless asked
296. Token budget — first 300 words contain the job of the page
297. No decorative lorem
298. No placeholder TBD in shipped HTML
299. Error pages explain the miss then offer apps
300. Success states named if forms exist
301. Empty states named if grids can be empty
302. Authoritative last line is the house link not a slogan pile
303. AIO copy does not fight GEO claims
304. AIO copy does not fight AEO snippet wording
305. Entity IDs stable in data/apps.json
306. Slugs stable across nav footer 404
## GEO (40)

307. Page can be cited as a standalone source for its topic
308. Brand + topic co-occur in the title or H1
309. Factual sentence engines can quote without trimming junk
310. No wall of adjectives before the first fact
311. Apps inventory is complete so engines do not invent extras
312. Order of apps is published so citations can match
313. Disambiguation — Digital Marketing Company vs generic agency nouns
314. Location of the firm only if local pages claim it
315. Do not geo-spam cities the page is not about
316. Generative engines see the same HTML as users
317. Important facts not only inside images
318. Important facts not only inside canvas
319. Schema supports the same facts as prose
320. No contradicting OG description
321. No contradicting Twitter description
322. Canonical prevents split citations
323. 404 does not become a cited product page
324. Menu labels match page titles closely
325. Short definition of each app under 25 words
326. No unverifiable superlative as the only description
327. When a superlative is used a measurable claim sits next to it
328. SGE-style overview would find a clear entity card
329. Perplexity-style citation would have a clean paragraph
330. Grok-style answer would not need to guess the app list
331. Gemini-style answer would see organization markup
332. Bing Chat-style answer would see site name meta
333. Avoid interstitials that hide the inventory
334. Avoid pagination for a short app list
335. Use a single inventory page plus chrome mirrors
336. Cite the auditor as a tool URL not as this page's identity unless it is the auditor
337. Do not claim a 521 score without running checks
338. Do not claim partnership marks that are not on the page
339. Authoritative outbound link to digitalmarketingco.org
340. Visible anchor equals title attribute on that link
341. Plain domain casing DigitalMarketingCo.org
342. Topic cluster — apps nav footer 404 all point at the same slugs
343. No orphan app route
344. No phantom app in the menu missing a page
345. Change frequency of the inventory documented in README
346. GEO paragraph is human-readable not a keyword barge
## AEO (40)

347. One featured-snippet candidate paragraph near the top on content pages
348. Direct answer then context
349. Question-style H2 only when a real question is answered
350. People-Also-Ask items only when written as Q and A
351. Voice-ready short answers under 30 words where a definition exists
352. Numbers written as numerals when they are metrics
353. Units named beside numbers
354. How-to steps are numbered lists if a how-to exists
355. Not a how-to page unless the remainder is a how-to
356. FAQPage schema only when visible FAQs exist
357. Each FAQ answer is self-contained
358. No FAQ that only says click here
359. Speakable content is short if marked
360. Do not mark the whole article speakable
361. Table of apps can answer which apps exist
362. First cell or first item is the official name
363. Synonyms of an app appear after the official name
364. Local business questions deferred to Local SEO pages
365. Price questions not answered if no price exists
366. Hours questions not answered if no hours exist
367. Contact questions link to a real contact route
368. 404 answers did this URL move with the app list
369. Menu does not hide the only statement of what an app is
370. Answer text is in the DOM as text nodes
371. No essential answer only in aria-label
372. Snippet-friendly 40-60 word blurb on /apps cards
373. Consistent punctuation in blurbs
374. No emoji-only answers
375. No bait title that the paragraph does not support
376. Meta description can stand as a spoken answer
377. Title can stand as a spoken title
378. Avoid rhyme-only slogans as the only description
379. Name the operator in one AEO sentence
380. Name the inventory in one AEO sentence
381. Name the next action in one AEO sentence
382. Do not stack three CTAs before one fact
383. Use strong not span for a single key phrase at most once
384. Time-to-answer for a voice user under ten seconds of reading
385. Accented characters used correctly if names need them
386. No ALL CAPS paragraphs
## Local SEO (36)

387. NAP only on pages that are actually local
388. NAP strings consistent when present
389. LocalBusiness schema only when a real location is claimed
390. Address matches the visible address
391. Telephone matches the visible telephone
392. Opening hours match visible hours when claimed
393. Geo coordinates only when verified
394. Google Maps link uses the same name string
395. City names not stuffed into app titles
396. Service-area copy only on service-area pages
397. Do not attach a city to a calculator app unless it is local
398. Organization schema can exist without LocalBusiness
399. SameAs social profiles only if real
400. Review schema only if reviews are visible and real
401. Aggregate rating not invented
402. Locale of the page matches the audience
403. Imperial or metric units consistent with the audience
404. Embedded map has a title and a text address fallback
405. Click-to-call visible on local pages
406. Directions CTA visible on local pages
407. Local landing pages not thin copies of /apps
408. Footer city list not a dump unless it is a real directory
409. hCard or equivalent microdata not required if JSON-LD is complete
410. Postal code formatted correctly when present
411. Country named when the address is international
412. Multi-location pages do not mix NAP blocks
413. Geotagged images not required
414. Local modifiers in title only when the page is local
415. GBP name not contradicted
416. Do not invent a GBP URL
417. Emergency or after-hours notes only if true
418. Parking or transit notes only if true
419. Accessibility of the physical site described only if true
420. Local page still passes the global 521 chrome checks
421. Apps that are tools stay tools not fake local services
422. 404 does not claim a storefront
## Schema.org (47)

423. JSON-LD is valid JSON
424. JSON-LD is in a script type application/ld+json
425. WebSite type on the home or chrome shell
426. WebSite name matches visible brand
427. WebSite url matches the site origin
428. SearchAction only if a working search exists
429. Organization type with name Digital Marketing Company when that is the operator
430. Organization url https://digitalmarketingco.org
431. Organization logo object with url width height when a logo file exists
432. WebPage type on each route
433. WebPage url equals canonical
434. WebPage name equals title intent
435. WebPage isPartOf points at WebSite
436. BreadcrumbList on depth greater than one
437. ItemList for the apps inventory on /apps
438. ItemList order matches data/apps.json
439. ListItem position is 1-indexed and contiguous
440. ListItem name matches visible title
441. ListItem url matches href
442. SoftwareApplication type only for real apps that behave as software
443. ApplicationCategory set when SoftwareApplication is used
444. Offer type only when a real offer exists
445. FAQPage only with visible FAQs
446. QAPage only for true Q and A pages
447. Article only for articles
448. NewsArticle not used for tools
449. ImageObject for OG image with url width height
450. primaryImageOfPage when a still exists
451. inLanguage set to en-US unless specified
452. datePublished only when known
453. dateModified only when known
454. publisher Organization reference consistent
455. No speakable without a real speakable block
456. No review without visible reviews
457. No aggregateRating without visible ratings
458. No videoObject without a video
459. No event without an event
460. No jobPosting without a job
461. About page uses AboutPage if it is an about page
462. Contact page uses ContactPage if it is a contact page
463. CollectionPage allowed for /apps
464. ItemPage allowed for a single app
465. 404 uses no Product schema
466. Mega menu is not marked as a fake SiteNavigationElement dump that lists hidden URLs
467. SiteNavigationElement if used matches visible nav
468. SameAs array only real profiles
469. No duplicate identical JSON-LD blocks that conflict
## WCAG (52)

470. WCAG 2.2 Level AA target for chrome
471. 1.1.1 Non-text content — alts present
472. 1.2.1 Audio-only and video-only — alternatives if media exists
473. 1.2.2 Captions if live-action video exists
474. 1.2.3 Audio description or media alternative if needed
475. 1.3.1 Info and relationships — headings lists labels
476. 1.3.2 Meaningful sequence — DOM order matches reading order
477. 1.3.3 Sensory characteristics — instructions not color-only or shape-only
478. 1.3.4 Orientation — page works portrait and landscape
479. 1.3.5 Identify input purpose — autocomplete on common fields
480. 1.4.1 Use of color — not the only indicator
481. 1.4.2 Audio control — no autoplaying audio
482. 1.4.3 Contrast minimum — body 4.5:1
483. 1.4.4 Resize text — 200 percent zoom without loss
484. 1.4.5 Images of text — UI type is live text
485. 1.4.10 Reflow — 320 px without two-axis scroll
486. 1.4.11 Non-text contrast — icons and focus 3:1
487. 1.4.12 Text spacing — no clipping when spacing CSS is applied
488. 1.4.13 Content on hover or focus — mega menu hoverable and dismissable
489. 2.1.1 Keyboard — all actions reachable
490. 2.1.2 No keyboard trap except intentional dialog
491. 2.1.4 Character key shortcuts — none that block typing
492. 2.2.1 Timing adjustable — no surprise timeouts on the menu
493. 2.2.2 Pause stop hide — idle animations can stop
494. 2.3.1 Three flashes — no flashing panels
495. 2.4.1 Bypass blocks — skip link
496. 2.4.2 Page titled — unique titles
497. 2.4.3 Focus order — logical
498. 2.4.4 Link purpose in context
499. 2.4.5 Multiple ways — nav plus footer plus 404 list
500. 2.4.6 Headings and labels describe topic
501. 2.4.7 Focus visible
502. 2.4.11 Focus not obscured — sticky header does not bury focus
503. 2.5.1 Pointer gestures — tap works without a path gesture
504. 2.5.2 Pointer cancellation — click on up
505. 2.5.3 Label in name — visible label is in the accessible name
506. 2.5.4 Motion actuation — shake not required
507. 2.5.7 Dragging movements — drag not the only menu method
508. 2.5.8 Target size minimum — 24 px absolute floor, 44 px house floor
509. 3.1.1 Language of page
510. 3.1.2 Language of parts if mixed
511. 3.2.1 On focus — focus does not open a new URL
512. 3.2.2 On input — typing does not submit by surprise
513. 3.2.3 Consistent navigation — Apps order identical everywhere
514. 3.2.4 Consistent identification — same icon means the same app
515. 3.2.6 Consistent help — contact in the same region when present
516. 3.3.1 Error identification if forms exist
517. 3.3.2 Labels or instructions if forms exist
518. 3.3.3 Error suggestion if forms exist
519. 4.1.1 Parsing — no duplicate ids
520. 4.1.2 Name role value
521. 4.1.3 Status messages — menu open state available to AT
