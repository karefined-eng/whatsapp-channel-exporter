# Store assets

This directory contains the shared graphics prepared for the Chrome Web Store and Microsoft Edge Add-ons listings. Store screenshots use the real extension UI captures in `website/public/actual-ui-*.png`; the surrounding typography and framing are generated locally, and no private WhatsApp data is included.

| File | Dimensions | Purpose |
|---|---:|---|
| `edge-icon-300.png` | 300×300 | Microsoft Edge Add-ons listing icon |
| `promo-tile-440x280.png` | 440×280 | Chrome/Edge promotional tile |
| `marquee-tile-1400x560.png` | 1400×560 | Chrome/Edge marquee tile |
| `screenshot-1-1280x800.png` | 1280×800 | Store screenshot: channel/date/export controls |
| `screenshot-2-1280x800.png` | 1280×800 | Store screenshot: export progress and reporting |

Regenerate the full pack from the repository root with:

```sh
python scripts/generate-marketing-assets.py
```

The generator writes the store assets, the website OG PNG/JPEG files, and the website marquee image in one pass. Review the rendered files for authenticity and privacy before submitting a store listing.
