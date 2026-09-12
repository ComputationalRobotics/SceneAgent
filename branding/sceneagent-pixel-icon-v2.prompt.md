# SceneAgent icon — 32×32 edition

Generated using the built-in imagegen tool. Simplified for a native 32×32 icon, then exported using ImageMagick nearest-neighbor sampling with no dithering, a fixed NASA-red/ink/transparent palette, and binary alpha.

- `sceneagent-pixel-icon-v2-32.png`: canonical 32×32 PNG. Use this for the small icon.
- `sceneagent-pixel-icon-v2-preview.png`: exact 16× nearest-neighbor enlargement of the canonical pixels, transparent, 512×512.
- `sceneagent-pixel-icon-v2-on-paper.png`: exact 8× enlargement shown on the design system's cream paper color, with 24px surrounding padding; presentation preview only.
- `sceneagent-pixel-icon-v2-source.png`: unmodified imagegen source, 1254×1254.

Palette of the final 32×32 PNG: NASA red `#E03C31`, ink `#111111`, fully transparent. Alpha is binary. Inspected at native size and enlarged. Intended for white or light neutral backgrounds. For larger display sizes, use integer multiples of 32 and CSS `image-rendering: pixelated`.

Source: `/Users/lrh/.codex/generated_images/01a08846-e8a5-7740-b68b-213611717b12/exec-5a8f81ba-4349-43ef-87c3-ddc11acc8825.png`.

## Final generation prompt

```text
Use case: logo-brand.
Create a new, extremely simple SceneAgent pixel-art icon designed for a 32x32-pixel favicon. One compact red pixel globe above one compact black pixel anvil. Use an actual 32x32 logical grid, displayed enlarged. Every logical pixel is a large square; all steps must be grid-aligned. The whole mark fills a 28x28 square with 2 pixels of padding.
Globe: round red disk 20 logical pixels in diameter, two very large simple transparent cutouts suggesting the Americas and Africa, no coastline detail. Anvil: 28 pixels wide, 8 pixels tall, 2-pixel-thick flat top, asymmetric stepped horn, stout waist, broad foot. Slight separation of 1 logical pixel between globe and anvil.
1975 NASA graphics manual character: NASA red #E03C31 and ink black #111111, restrained geometric industrial graphic, perfectly flat solid colors.
Genuinely transparent background with alpha. All unpainted areas must be transparent, including cutouts. Do NOT illustrate a checkerboard, paper, fabric, folds or any backdrop.
Only the icon, no text or wordmark, no detached squares, no ornaments, no mockup, no texture, no gradient, no thin outlines. Large solid pixel clusters and wide clean cutouts that read at native 32x32 size. Square image.
```

