# QA checklist

Run `scripts/qa_pepe.py` on the artifact folder. Fix every fail. Re-run until PASS.

| Id | Check | Fix |
| --- | --- | --- |
| Q1 | `node --check` on `pepe-promptform.js` | Repair syntax |
| Q2 | File defines `customElements.define` and `PepePromptform` | Add the public API |
| Q3 | Shadow root attach | Add `attachShadow({ mode: "open" })` |
| Q4 | `prefers-reduced-motion` in CSS | Add the media block and disable loops |
| Q5 | `:focus-visible` rule present | Add a visible focus ring |
| Q6 | Button or control has an accessible name | Add `aria-label` or text |
| Q7 | `pepe-ready` and `pepe-action` dispatched | Wire the events |
| Q8 | `mount` and `unmount` on `window.PepePromptform` | Export both |
| Q9 | No `document.body.style` write | Remove the leak |
| Q10 | JS under 40 KB and CSS under 24 KB | Cut unused rules |
| Q11 | Host `index.html` contains the custom element | Add the install demo |
| Q12 | Visible UI strings avoid the negative blocklist | Rewrite the string |

Do not delete a check. Do not mark PASS by hand.
