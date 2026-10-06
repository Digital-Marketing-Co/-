# Tailwind motion catalog

Pick at least three coordinated items from this list for any primary nav, hero, or mega menu. Honor `prefers-reduced-motion: reduce` by snapping to the end state with no continuous animation.

## Required pairing

1. One enter animation
2. One idle or sheen animation
3. One pointer/focus animation
4. A reduced-motion media block that disables 1–3

## Enter

- `animate-in fade-in zoom-in-95 slide-in-from-top-2 duration-300`
- Panel `origin-top` with `scale-y` and `opacity`
- Stagger children with increasing `delay-75`, `delay-100`, `delay-150` (cap at 8 visible items, then static)
- 3D open — `perspective-[1200px]` parent, child `rotateX(-8deg)` to `rotateX(0)`

## Idle

- Slow gradient shift on the page field (`animate-[gradient-shift_18s_ease_infinite]`)
- Hairline sheen across glass (`animate-[sheen_6s_ease-in-out_infinite]`)
- Soft float on holographic tiles (`animate-[float_7s_ease-in-out_infinite]`) — amplitude <= 6 px
- Conic border spin paused until hover if it distracts

## Pointer and focus

- Tile `hover:-translate-y-1 hover:scale-[1.02] hover:shadow-[0_20px_50px_-20px_rgba(0,0,0,0.45)]`
- Iridescent border intensification on hover and `:focus-visible`
- Magnetic underline or light-bar that follows the active item
- Icon `group-hover:rotate-6 group-hover:scale-110`

## Exit

- Reverse of enter, duration 150–200 ms
- Do not leave `pointer-events` hot on a closing panel

## Custom keyframes to ship in CSS

```css
@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes sheen {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
@keyframes hologram-edge {
  0%, 100% { filter: hue-rotate(0deg); }
  50% { filter: hue-rotate(25deg); }
}
```

## Performance

- Animate `transform` and `opacity` only.
- Do not animate `blur`, `top`, `height`, or `box-shadow` color on every frame for large trees.
- Pause idle animations when the document is hidden (`document.hidden`).

## Accessibility

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
