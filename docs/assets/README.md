# CIC shared site assets

The homepage generated directly under `docs/` uses `assets/site.css` and
`assets/cic-logo.png`. Generated problem pages under `docs/problems/` use
`../assets/site.css` and `../assets/cic-logo.png`. The CSS uses system fonts and
a black, white, and gray palette; it has no runtime dependencies or JavaScript.

## Logo provenance

`cic-logo.png` is the official CIC mark recovered from the former challenge
portal, not a recreation. The repository originally added the logo at
`docs/assets/images/cic-logo.jpeg` in commit
`a60814ce735299120701276054c2d04dd0b6cfd4`. That asset has Git blob ID
`290d4d2b868770843a0778bcafefdf72345d6a05`; the former portal used it in its
Coding Interview Club brand link.

Recovery used:

```sh
git show a60814ce735299120701276054c2d04dd0b6cfd4:docs/assets/images/cic-logo.jpeg > /tmp/cic-logo.jpeg
sips -s format png /tmp/cic-logo.jpeg --out docs/assets/cic-logo.png
```

The conversion preserves the 447 × 447 artwork, with no cropping, recoloring,
or resizing. Decoding both source and restored images to BMP with `sips` and
comparing them with `cmp` produced identical files. Source JPEG SHA-256:
`1e799503d7361ae534b60e7874bae6c585355c76e70837b75d534c0e02489da3`.
Restored PNG SHA-256:
`50e86b6229a3950e8ce4dfd86675f5d76778bd8339f2a87bc1e861979e51befa`.

Use an empty `alt` when the logo sits beside visible “Coding Interview Club”
text inside the same link. If the image is the link’s only content, give the
link an accessible name such as `aria-label="Coding Interview Club home"`.
Keep its proportions and leave it on a white surface.

## Component contract

`style-guide.html` demonstrates the classes and semantic markup. It is a
component preview, excluded from indexing, and contains no real assignment.

| Class | Usage |
|---|---|
| `container` | Centered content, maximum 72rem, with mobile gutters |
| `site-header`, `site-brand`, `site-nav` | Wrapping header and navigation; use `aria-current="page"` on the current link |
| `skip-link` | First link, pointing to a unique main ID; use `tabindex="-1"` on the main target |
| `page-header`, `eyebrow`, `meta`, `muted` | Page hierarchy and secondary text |
| `breadcrumbs` | A labeled `nav` containing an ordered list |
| `content-layout`, `prose` | Reading layout, with optional direct child `aside` |
| `problem-grid`, `problem-card`, `tag` | Responsive list of exercises or categories; use real headings and links |
| `actions`, `button`, `button-secondary` | Native links or buttons, with primary and secondary appearance |
| `table-scroll` | Focusable overflow region around a semantic table; add `role="region"`, a meaningful `aria-label`, and `tabindex="0"` |
| `notice` | Neutral information with visible text and border |
| `details-content` | Content wrapper inside native `details`, following `summary` |
| `site-footer` | Secondary footer content |

Add `tabindex="0"` and a descriptive `aria-label` to code blocks that may
scroll horizontally. Use semantic headings, table header scopes, and native
controls. CSS supplies a shared 3px focus ring with contrasting edges; avoid
removing it in page-specific styles. The reduced-motion rule disables animation
and smooth scrolling, and forced-colors mode uses the system highlight color.

## Verification

Serve the preview with `python3 -m http.server 8766 --bind 127.0.0.1 --directory docs`
and open `http://127.0.0.1:8766/assets/style-guide.html`.

Checks performed in Chromium on 2026-10-22:

- Visually inspected 1280 × 900 and 320 × 900. Document width matched viewport
  width at both sizes; mobile navigation wrapped and cards stacked.
- At 320px with the root font size set to 200%, document width remained 320px.
- Tab exposed the skip link with a 3px outline; Enter moved to the main target.
  Enter on the focused native summary opened the disclosure with a 3px outline.
- Overflowing code stayed inside its focusable scroll area. The logo loaded at
  its original intrinsic width of 447px. The preview loaded zero scripts.
- Forced-colors emulation retained a 3px system-colored focus outline.
- Calculated contrast ratios: ink/paper 17.93:1, muted/paper 7.81:1,
  muted/surface 7.17:1, strong border/paper 4.74:1, hovered primary button
  text/background 10.37:1. Text links are underlined and tags include labels.

These are shared-component checks. Screen-reader testing, additional browser
engines, and acceptance of the final generated site are separate verification
work. The local preview server returned one expected `/favicon.ico` 404; no
script errors were observed.
