# Miguel's A/C — website

Static site for an Inland Empire / Los Angeles HVAC company. 43 pages, no build
dependencies, no framework. Built from the Relume wireframe export.

## Run it locally

```bash
python3 miguels-ac/serve.py
```

Then open http://localhost:8077. Use a server rather than opening the `.html`
files directly — links are root-absolute (`/index.html`, `/assets/...`) so they
resolve the same way locally as in production.

## Regenerate the pages

Every page shares one header, footer, CTA band and form. Those live in
`build.py`; all copy lives in `data.py`. Edit either, then:

```bash
python3 miguels-ac/build.py
```

That rewrites all 43 `.html` files plus `sitemap.xml` and `robots.txt`.

Do not hand-edit the generated `.html` files — the next build overwrites them.

## Sharing a preview

To hand someone the whole site as one private link — no hosting, no domain:

```bash
python3 bundle.py
```

That writes `miguels-ac-preview.html`: every page inlined behind a hash router,
with the stylesheet, both fonts and the logo embedded as data URIs. One file,
~1.2 MB, works offline, opens anywhere. Publish it as a private artifact or just
email the file.

The bundle is a preview, not the deployable site. It differs deliberately:

- A dismissible banner lists what is still placeholder.
- The invented testimonials and the 4.9-star stats carry a **"Sample — not real"**
  label that cannot be dismissed, so nothing fabricated can be mistaken for
  genuine.
- Output is pure ASCII with non-ASCII as entities and CSS escapes, because the
  host owns `<head>` and we cannot declare a charset.
- Scroll-reveal has a failsafe: it probes whether `IntersectionObserver`
  actually fires and, if not, snaps everything visible. An embedded iframe that
  starts offscreen never delivers those callbacks, and a blank page in front of
  a client is not a tradeoff worth making for a fade-in.

Re-run `build.py` before `bundle.py` — the bundler reads the generated pages.

## Files

| File | What it is |
| --- | --- |
| `data.py` | All content: business details, 7 services, 29 cities, reviews, plans, FAQs |
| `build.py` | Templates + page assembly. Run it to regenerate |
| `serve.py` | Local preview server |
| `bundle.py` | Bundles all 43 pages into one shareable file |
| `assets/css/style.css` | The entire stylesheet (hand-written, ~700 lines) |
| `assets/js/main.js` | Nav, mobile drawer, FAQ accordion, scroll reveal, form handling |
| `assets/img/` | Generated logo assets — do not edit directly |
| `assets/fonts/` | Self-hosted subsetted webfonts — generated, do not edit |
| `brand/` | Original logo art + the scripts that derive web assets and fonts. **Not for deployment** |
| `*.html` | Generated — do not edit directly |

## Performance

The site loads no third-party resources at all — no font CDN, no analytics, no
external anything. Every byte comes from your own origin.

A warm page-to-page navigation transfers **~9 KB**: the gzipped HTML, and a
304 for each of the six subresources. Cold load is about 80 KB.

Three things get it there, and it's worth knowing why so a future change
doesn't undo them:

1. **Fonts are self-hosted and subsetted.** A `<link>` to fonts.googleapis.com
   is render-blocking and costs two extra DNS + TLS handshakes before a single
   word paints — on *every* page load. `brand/fetch-fonts.py` pulls the variable
   font for each family and subsets it to the characters the site can render:
   two files, 61 KB total, versus 291 KB of static weights from Google. Both are
   preloaded so they start downloading before the CSS is parsed.

   ```bash
   python3 brand/fetch-fonts.py     # needs: pip install --user fonttools brotli
   ```

   Re-run it if you add a font weight or start using characters outside Latin-1
   (the `UNICODES` range in that script is the boundary).

2. **`serve.py` sends `Cache-Control: no-cache`** — which means "cache it, but
   revalidate", *not* "don't cache". Each navigation costs a conditional request
   answered with an empty 304 rather than a re-download, and your edits still
   appear on the next reload. Do not change this to `no-store`; that forces a
   full re-download of the stylesheet, fonts and logo on every single click.

3. **`serve.py` is threaded, speaks HTTP/1.1, and gzips text.** Keep-alive means
   one connection for the page and its assets. Gzip takes the HTML from 48 KB to
   9 KB and the stylesheet from 29 KB to 7 KB.

**In production**, your host handles items 2 and 3 — Vercel, Netlify and GitHub
Pages all gzip/brotli automatically. Configure caching as: `no-cache` for
`.html`, and `max-age=31536000, immutable` for everything under `/assets/`.
That's safe for fonts and images as-is; if you edit `style.css` or `main.js`
after going live, add a query string (`style.css?v=2`) so browsers pick it up.

## Logo

The original art is a 3584×4800 PNG on a white background — 16 MB, far too heavy
to ship. `brand/make-logo-assets.py` derives everything the site loads:

```bash
python3 brand/make-logo-assets.py
```

It trims the white margin, knocks the background out to transparency (only where
white connects to the border, so the white in the wordmark and the mascot's teeth
survive), and writes into `assets/img/`:

| Asset | Used for |
| --- | --- |
| `logo-mark.webp` / `.png` | 192px square badge — header and footer |
| `logo-mark@2x.webp` / `.png` | 512px, for any larger placement |
| `favicon-32.png`, `favicon-180.png` | Browser tab and iOS home screen |
| `logo-full.webp` / `.png` | 900px full lockup including the bottom point |
| `og.jpg` | 1200×630 social card — navy field, logo, headline |

The header serves WebP (18 KB) with a PNG fallback via `<picture>`, at 192px
natural for a 54px display — 3.6× density, sharp on any screen.

Only `brand/` holds the original. Exclude that folder when you deploy.

## Pages

- **Home** — `index.html`
- **Services** — `services.html` + 7 service pages
  (`air-conditioning-repair`, `ac-installation-replacement`, `heat-pumps`,
  `ductless-mini-splits`, `duct-repair-replacement`, `indoor-air-quality`,
  `maintenance-plans`)
- **Service areas** — `service-areas.html` + 29 city pages across 6 regions:
  Inland Empire (8), San Gabriel Valley (8), Central & Southeast LA (5),
  South Bay & Harbor (2), Westside (2), San Fernando Valley & North (4)
- **Company** — `about.html`, `reviews.html`, `financing.html`, `contact.html`

Each city page has unique copy, its own neighborhood list, its own FAQ block and
its own `HVACBusiness` + `FAQPage` structured data. That is deliberate — near-
duplicate city pages get filtered out of local search results.

### Dispatch tiers

Coverage runs from Redlands to Santa Monica — 90 minutes end to end — so the
pages do not all make the same promise. Each city carries a `dispatch` key in
`data.py` that drives its scheduling line, its page title and its FAQ answer:

| Tier | Regions | What the page says |
| --- | --- | --- |
| `same-day` | Inland Empire, San Gabriel Valley | "Same-day windows on most calls placed before 2pm." |
| `scheduled` | Central & Southeast LA, San Fernando Valley | "Same-day when a truck is already out that way, next-day otherwise." |
| `route` | South Bay & Harbor, Westside, Santa Clarita | "We run scheduled routes out here. Call before noon for next-day." |

Titles follow the tier too — only `same-day` cities are titled "Same-Day AC
Repair". A page that promises same-day to Santa Monica and then misses it costs
more in reviews than the booking was worth. Change a city's tier in `data.py`
and the copy, title and FAQ all follow.

## Before launch — required

Everything below is a placeholder. Most of it is one edit in `data.py`.

1. **Contact details** — `BUSINESS` at the top of `data.py`. Change once there,
   rebuild, and it updates everywhere.
   - ~~`phone`~~ — **done**: (909) 228-7653, owner Miguel Guardado
   - ~~`email`~~ — **done**: miguelguardadohvac@gmail.com
   - `street` / `zip` — currently a made-up Rancho Cucamonga address
   - `license` — currently `CSLB Lic. #0000000`. **Use the real C-20 number.**
     Publishing a fake contractor license number is a legal problem, not a
     cosmetic one.
   - `founded` — `2009` is invented, and the About page now says
     "Owner-operated by Miguel Guardado ... since 2009". A made-up year next to
     a real person's name is worse than a generic one. Fix or cut it.
   - `hours_weekday` — invented; confirm the real hours
   - `domain` — drives canonical URLs and the sitemap
2. **The forms do not submit anywhere.** They confirm inline and clear. Point
   them at your CRM (ServiceTitan, Housecall Pro) or a form service (Formspree,
   Netlify Forms) before you drive any traffic here.
3. **Reviews are written placeholders.** Replace them in `data.py` with real,
   verbatim reviews from your Google Business Profile. Do not publish
   testimonials you cannot attribute to a real customer — the FTC treats
   fabricated reviews as deceptive advertising.
4. **Stats are placeholders** — "6,400+ systems", "912 reviews", "4.9★", "15+
   years". These also appear in the `aggregateRating` structured data, where a
   made-up number is a Google policy violation. Use real figures or delete the
   `aggregateRating` block in `build.py`.
5. **Financing terms.** `financing.html` describes soft-pull pre-qualification
   and no prepayment penalty generically. Wire it to your actual lender and
   publish their real APR ranges — consumer credit advertising disclosures are
   legally required.
6. **Photos.** Every image slot is a styled `.figure` placeholder. Swap each one
   for a real `<img>` — job site photos, the crew, trucks, before/afters. This is
   the single biggest visual upgrade available, and homeowners looking for a
   contractor respond to real faces.

## Nice to have

- Google Map embed on `contact.html` (there is a marked spot for it)
- Google Business Profile link on `reviews.html`
- Analytics / call tracking
- A vector (SVG) version of the logo, if the designer has one — it would replace
  the raster badge and shrink the header asset to a couple of KB

## Design notes

The palette is sampled from the logo art, not picked by eye:

| Token | Value | Where it comes from | Used for |
| --- | --- | --- | --- |
| `--navy` | `#071C38` | logo's deep blue, darkened | Dark sections, hero, footer |
| `--brand` | `#2478C0` | the logo's dominant blue | Buttons and accents on light |
| `--accent` | `#54A8E4` | the logo's cyan highlight | Accents and CTAs on dark |
| `--accent-soft` | `#E9F3FB` | tint of the above | Icon chips, form confirmations |
| `--star` | `#F5A623` | — | Review stars only |

Two rules govern which blue appears where. On light surfaces, `--brand` (4.6:1
against white). On navy, `--brand` drops to 3.7:1 and goes muddy, so dark
sections switch to `--accent` with dark text — 6.5:1, and it keeps the emergency
CTA the loudest thing on screen. Every pairing in the stylesheet was measured
against its actual rendered background and clears WCAG AA.

Review stars stay warm amber. It's the one place a brand color would hurt —
blue stars read as *unfilled*. Change `--star` if you disagree.

Archivo for display, Inter for body, both from Google Fonts. Every CTA is a
phone call first, a form second — HVAC emergencies convert by phone, and the
sticky bottom call bar on mobile is the highest-value element on the site.

The stylesheet is plain CSS with custom properties, no preprocessor. Breakpoints
are `560px`, `760px`, `900px`, `1040px` (nav collapses) and `780px` (call bar
appears).
