# Embed contract

The widget installs inside another web application. It is not a full site.

## Host install

```html
<div id="host-slot"></div>
<script type="module" src="/pepe-promptform.js"></script>
<script type="module">
  const node = document.createElement("pepe-promptform");
  node.setAttribute("label", "Pulse deck");
  document.getElementById("host-slot").appendChild(node);
</script>
```

Or:

```js
window.PepePromptform.mount("#host-slot", { label: "Pulse deck" });
window.PepePromptform.unmount("#host-slot");
```

## Required surface

- Custom element `pepe-promptform` (override with `mount:` key only if the remainder names a different tag).
- Attributes: `label`, `accent` (hex), `density` (`compact` | `regular`).
- Events: `pepe-ready`, `pepe-action` (detail.action).
- Methods on the element: `setReading(text)`, `setBusy(boolean)`, `destroy()`.
- `window.PepePromptform.mount(selector, options)` returns the element.
- `window.PepePromptform.unmount(selector)` removes it.

## Isolation

- Attach an open Shadow DOM.
- All selectors live under `:host` or inside the shadow tree.
- Do not set styles on `document.body` except a one-time reduced-motion read.
- Do not require Tailwind, a bundler, or a CDN for the installed widget.
- The demo `index.html` may use a plain host layout to prove install. The widget files must still work if copied into a foreign app.

## File budget

- `pepe-promptform.js` under 40 KB uncompressed.
- `pepe-promptform.css` under 24 KB uncompressed.
- First paint uses no image network request.
