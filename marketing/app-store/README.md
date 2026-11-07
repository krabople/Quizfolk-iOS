# App Store screenshot artwork

Ten captioned images per device size, composed around unretouched native simulator captures. The editable layouts use Quizfolk's existing icon, Nunito font and colour palette.

## Capturing

Run the manual **App Store screenshots** GitHub Actions workflow. It uses the existing app UI with fictional local data, without contacting the production service. `--store-screenshots` and its fixture hooks are compiled out of Release builds. The capture suite is skipped during normal CI.

The workflow captures medium iPhone, large iPhone and 13-inch iPad. The app still targets device family 1. The iPad capture therefore preserves the real compatibility-mode presentation, including its system margins; it does not represent native iPad support.

Keep the exported attachment manifest and provenance alongside the originals. Map the selected originals into these filenames under each of `iphone-medium`, `iphone-large` and `ipad`:

| Original attachment | Renderer filename |
| --- | --- |
| STORE-01-duel | Gameplay.png |
| STORE-02-topics | Topics.png |
| STORE-03-challenges | Friends.png |
| STORE-04-topic-progress | Levels.png |
| STORE-05-topic-league | League.png |
| STORE-06-tournament | Tournament.png |
| STORE-07-friends | Party.png |
| STORE-08-badges | Badges.png |
| STORE-09-rival-profile | Profile.png |
| STORE-10-result | Result.png |

## Rendering

Use Node.js with `playwright` and `sharp`, and a local Chromium browser. These packages are already available in the Codex desktop runtime. `STORE_BROWSER_CHANNEL` defaults to `chrome` and can be set to `msedge`.

```text
node marketing/app-store/render.cjs CAPTURE_ROOT OUTPUT_ROOT
```

The renderer checks native capture dimensions, text overflow, final dimensions and absence of alpha. It exports RGB/sRGB PNGs, editable HTML layouts, original captures, numbered captions, a browsable index, contact sheets and a verification manifest containing source hashes. It does not repaint or rearrange any part of an app screen.

## Device sizes

- iPhone medium: 1206 × 2622, portrait.
- iPhone large: 1320 × 2868, portrait.
- iPad 13-inch: 2064 × 2752, portrait.

Apple's [screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/) were checked on 7 November 2026. The page currently lists medium Dynamic Island iPhone screenshots as required; the large set is also provided. iPad screenshots are required for apps supporting iPadOS. The current iPhone-only build may not expose an iPad upload slot.

Apple permits up to ten screenshots per size. Its [product-page guidance](https://developer.apple.com/app-store/product-page/) recommends real app UI with the main experience in the first images. [Guideline 2.3](https://developer.apple.com/app-store/review/guidelines/#accurate-metadata) permits explanatory overlays and calls for fictional account details. Captions describe existing functionality, with no implication of real-time multiplayer or cash prizes.

Creating this set does not submit the app for review or upload assets to App Store Connect.
