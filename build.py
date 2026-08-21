#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miguel's A/C static site generator.

    python3 build.py

Reads content from data.py and writes plain .html files next to this script.
No dependencies — standard library only.
"""

import html
import os
import re
import sys

sys.dont_write_bytecode = True
from data import (  # noqa: E402
    BUSINESS, SERVICES, CITIES, CITY_NAMES, STATS, REVIEWS,
    PLANS, HOME_FAQ, PROCESS, REGIONS, DISPATCH,
)

ROOT = os.path.dirname(os.path.abspath(__file__))

# Preview mode: adds noindex, a placeholder banner, and "Sample - not real"
# labels on the invented reviews and stats. Set False for the real launch.
PREVIEW = True

B = BUSINESS
PHONE = B["phone"]
TEL = "tel:+" + B["phone_href"].lstrip("+")

# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------
ICONS = {
    "snowflake": '<path d="M12 2v20M12 2l-3 3M12 2l3 3M12 22l-3-3M12 22l3-3M2.7 7l17.3 10M2.7 7l.7 4.1M2.7 7l4.1-.7M20 17l-4.1.7M20 17l-.7-4.1M2.7 17L20 7M2.7 17l4.1.7M2.7 17l.7-4.1M20 7l-4.1-.7M20 7l-.7 4.1"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0 5.3 5.3l-8.5 8.5a2.8 2.8 0 0 1-4-4l8.5-8.5a4 4 0 0 0-1.3-1.3z"/><path d="M14.7 6.3 18 3l3 3-3.3 3.3"/>',
    "flame": '<path d="M12 2s5 5.5 5 10a5 5 0 0 1-10 0c0-1.5.6-2.9 1.4-4C9 10 12 8 12 2z"/><path d="M12 22a5 5 0 0 0 5-5"/>',
    "wind": '<path d="M3 8h11a3 3 0 1 0-3-3M3 16h13a3 3 0 1 1-3 3M3 12h17"/>',
    "duct": '<path d="M3 7h11v10H3zM14 9h4l3 3-3 3h-4"/><path d="M6 7v10M9 7v10"/>',
    "leaf": '<path d="M4 20c0-9 6-14 16-14 0 10-5 15-14 15H4v-1z"/><path d="M9 15c2-3 5-5 8-6"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/><path d="m9 12 2 2 4-4"/>',
    "check": '<path d="m4 12 5 5L20 6"/>',
    "phone": '<path d="M6 3h4l2 5-2.5 1.5a12 12 0 0 0 5 5L16 12l5 2v4a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2 2 2 0 0 1 6 3z"/>',
    "calendar": '<path d="M4 6h16v15H4zM4 10h16M8 3v4M16 3v4"/>',
    "chevron": '<path d="m5 8 5 5 5-5"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "star": '<path d="m12 3 2.7 5.6 6.3.9-4.5 4.3 1 6.2-5.5-3-5.5 3 1-6.2L3 9.5l6.3-.9z" fill="currentColor" stroke="none"/>',
    "pin": '<path d="M12 21s7-5.7 7-11a7 7 0 1 0-14 0c0 5.3 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "badge": '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 7 5-2.5 5 2.5-1.5-7"/>',
    "dollar": '<path d="M12 3v18M16 7.5C16 6 14.2 5 12 5S8 6 8 7.5 9.8 10 12 10.5s4 1.3 4 3-1.8 2.5-4 2.5-4-1-4-2.5"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "home": '<path d="M4 11 12 4l8 7v9H4z"/><path d="M9 20v-6h6v6"/>',
}


def icon(name, cls=""):
    body = ICONS.get(name, ICONS["check"])
    c = ' class="%s"' % cls if cls else ""
    return (
        '<svg%s viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true">%s</svg>' % (c, body)
    )


def e(text):
    return html.escape(str(text), quote=True)


# ---------------------------------------------------------------------------
# Navigation model
# ---------------------------------------------------------------------------
SERVICE_LINKS = [(s["nav"], "/%s.html" % s["slug"]) for s in SERVICES]
AREA_LINKS = [(c["name"], "/%s.html" % c["slug"]) for c in CITIES]


def by_region():
    """[(region, [city, ...]), ...] in REGIONS order."""
    return [(r, [c for c in CITIES if c["region"] == r]) for r in REGIONS]


def head(title, desc, path, schema=""):
    canonical = B["domain"] + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canonical)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:site_name" content="{e(B['name'])}">
<meta property="og:image" content="{e(B['domain'])}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#071C38">
{'<meta name="robots" content="noindex, nofollow">' if PREVIEW else ''}
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/css/style.css">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/favicon-180.png">
{schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""


def logo(footer=False):
    """Badge mark + wordmark. The badge art carries its own name, but at header
    size that lettering is unreadable, so the text lockup stays alongside it."""
    # Header logo is above the fold on every page — never lazy-load it.
    loading = 'loading="lazy"' if footer else 'fetchpriority="high"'
    return f"""<a class="logo" href="/index.html" aria-label="{e(B['name'])} home">
  <picture class="logo__mark">
    <source type="image/webp" srcset="/assets/img/logo-mark.webp">
    <img src="/assets/img/logo-mark.png" alt="" width="192" height="192" decoding="async" {loading}>
  </picture>
  <span class="logo__text">{e(B['name'])}<span>{e(B['tagline'])}</span></span>
</a>"""


def dropdown(label, links, wide=False):
    items = "\n".join(
        '        <a href="%s">%s</a>' % (href, e(name)) for name, href in links
    )
    cls = " nav__menu--wide" if wide else ""
    return f"""      <div class="nav__group" data-open="false">
        <button class="nav__toggle" type="button" aria-expanded="false">{e(label)} {icon('chevron')}</button>
        <div class="nav__menu{cls}">
{items}
        </div>
      </div>"""


def area_dropdown():
    """29 cities is too many for a flat list — group the menu by region."""
    cols = []
    for region, cities in by_region():
        links = "\n".join(
            '            <a href="/%s.html">%s</a>' % (c["slug"], e(c["name"]))
            for c in cities
        )
        cols.append(
            '          <div class="nav__col">\n'
            '            <p class="nav__colhead">%s</p>\n%s\n          </div>'
            % (e(region), links)
        )
    return f"""      <div class="nav__group nav__group--mega" data-open="false">
        <button class="nav__toggle" type="button" aria-expanded="false">Service areas {icon('chevron')}</button>
        <div class="nav__menu nav__menu--mega">
{chr(10).join(cols)}
          <a class="nav__allareas" href="/service-areas.html">All service areas &rarr;</a>
        </div>
      </div>"""


def header(active=""):
    def cur(key):
        return ' aria-current="page"' if active == key else ""

    return f"""<div class="topbar">
  <div class="container topbar__inner">
    <span>{icon('clock')} <strong>{e(B['hours_weekday'])}</strong> · {e(B['hours_emergency'])}</span>
    <div class="topbar__right">
      <span>{e(B['license'])}</span>
      <a href="mailto:{e(B['email'])}">{e(B['email'])}</a>
    </div>
  </div>
</div>

<header class="header">
  <div class="container header__inner">
    {logo()}
    <nav class="nav" id="primary-nav" data-open="false" aria-label="Main">
{dropdown('Services', SERVICE_LINKS)}
{area_dropdown()}
      <a href="/financing.html"{cur('financing')}>Financing</a>
      <a href="/reviews.html"{cur('reviews')}>Reviews</a>
      <a href="/about.html"{cur('about')}>About</a>
      <a href="/contact.html"{cur('contact')}>Contact</a>
      <div class="nav__mobile-cta">
        <a class="btn btn--primary btn--block" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
        <a class="btn btn--ghost btn--block" href="/contact.html">Book online</a>
      </div>
    </nav>
    <div class="header__cta">
      <a class="header__phone" href="{TEL}">{icon('phone')} {e(PHONE)}</a>
      <a class="btn btn--primary" href="/contact.html">Book online</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<div class="callbar">
  <a class="is-primary" href="{TEL}">{icon('phone')} Call now</a>
  <a href="/contact.html">{icon('calendar')} Book online</a>
</div>
"""


def crumbs(trail):
    """trail: list of (label, href or None)."""
    parts = []
    for label, href in trail:
        if href:
            parts.append('<li><a href="%s">%s</a></li>' % (href, e(label)))
        else:
            parts.append('<li aria-current="page">%s</li>' % e(label))
    return (
        '<nav class="crumbs" aria-label="Breadcrumb"><div class="container">'
        "<ol>%s</ol></div></nav>" % "".join(parts)
    )


def footer():
    svc = "\n".join(
        '      <li><a href="%s">%s</a></li>' % (h, e(n)) for n, h in SERVICE_LINKS
    )
    # One line per region keeps the footer readable at 29 cities.
    areas = "\n".join(
        '      <li><a href="/%s.html">%s</a></li>' % (cities[0]["slug"], e(region))
        for region, cities in by_region() if cities
    )
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div class="footer__about">
        {logo(footer=True)}
        <p>Licensed HVAC contractors serving the Inland Empire and Los Angeles County since {e(B['founded'])}. Honest quotes, flat-rate pricing, and no overtime charges — ever.</p>
        <div class="footer__contact">
          <a href="{TEL}">{icon('phone')} {e(PHONE)}</a>
          <a href="mailto:{e(B['email'])}">{e(B['email'])}</a>
          <span>{e(B['address_line'])}</span>
          <span>{e(B['hours_weekday'])}</span>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
{svc}
        </ul>
      </div>
      <div>
        <h4>Service areas</h4>
        <ul>
{areas}
      <li><a href="/service-areas.html">All areas →</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/about.html">About us</a></li>
          <li><a href="/reviews.html">Reviews</a></li>
          <li><a href="/financing.html">Financing</a></li>
          <li><a href="/maintenance-plans.html">Maintenance plans</a></li>
          <li><a href="/contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 {e(B['legal_name'])}. All rights reserved. {e(B['license'])}</span>
      <ul>
        <li><a href="/contact.html">Privacy policy</a></li>
        <li><a href="/contact.html">Terms of service</a></li>
        <li><a href="/contact.html">Accessibility</a></li>
      </ul>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Reusable sections
# ---------------------------------------------------------------------------
def lead_form(heading, sub, form_id="book", compact=False):
    opts = "\n".join(
        '        <option>%s</option>' % e(s["name"]) for s in SERVICES
    )
    cities = "\n".join('        <option>%s</option>' % e(n) for n in CITY_NAMES)
    return f"""<form class="lead-form" data-lead-form id="{form_id}" novalidate>
  <div class="field-row">
    <div class="field">
      <label for="{form_id}-name">Name</label>
      <input id="{form_id}-name" name="name" type="text" autocomplete="name" placeholder="Your name" required>
    </div>
    <div class="field">
      <label for="{form_id}-phone">Phone</label>
      <input id="{form_id}-phone" name="phone" type="tel" autocomplete="tel" placeholder="(909) 000-0000" required>
    </div>
  </div>
  <div class="field">
    <label for="{form_id}-city">City</label>
    <select id="{form_id}-city" name="city">
      <option value="">Select your city</option>
{cities}
      <option>Other / nearby</option>
    </select>
  </div>
  <div class="field">
    <label for="{form_id}-service">What do you need?</label>
    <select id="{form_id}-service" name="service">
      <option value="">Select a service</option>
      <option>Emergency — no cool air</option>
{opts}
      <option>Not sure — need an opinion</option>
    </select>
  </div>
  {'' if compact else '''<div class="field">
    <label for="%s-notes">Anything we should know?</label>
    <textarea id="%s-notes" name="notes" placeholder="Making a noise, blowing warm, tripped the breaker..."></textarea>
  </div>''' % (form_id, form_id)}
  <button class="btn btn--primary btn--block btn--lg" type="submit">Request service</button>
  <p class="form-note">Or call {e(PHONE)} for the fastest response. We never share your information.</p>
  <p class="form-status" tabindex="-1" role="status">Got it — we will call you back shortly to confirm your window. For anything urgent, call {e(PHONE)} now.</p>
</form>"""


def trust_strip():
    items = [
        ("bolt", "Same-day service"),
        ("dollar", "No overtime charges"),
        ("badge", "Licensed &amp; insured"),
        ("shield", "1-year repair warranty"),
        ("check", "Flat-rate quotes upfront"),
    ]
    inner = "\n".join(
        '      <div class="trust__item">%s %s</div>' % (icon(k), v) for k, v in items
    )
    return f"""<section class="trust">
  <div class="container trust__inner">
{inner}
  </div>
</section>"""


def stats_section(heading="Fifteen summers of Inland Empire heat"):
    cells = "\n".join(
        '      <div class="stat"><b>%s</b><span>%s</span></div>' % (e(n), e(l))
        for n, l in STATS
    )
    return f"""<section class="section section--navy">
  <div class="container">
    <div class="section-head center" data-reveal>
      <p class="eyebrow">By the numbers</p>
      <h2 class="h2">{e(heading)}</h2>
      <p class="lead">We have been running these routes long enough to know which tract has undersized returns and which brand's control boards fail at year eight.</p>
    </div>
    <div class="stats" data-reveal>
{cells}
    </div>
  </div>
</section>"""


def reviews_section(limit=3, city=None):
    picked = REVIEWS[:limit]
    stars = '<div class="stars">%s</div>' % (icon("star") * 5)
    cards = []
    for name, role, text in picked:
        initials = "".join(p[0] for p in name.split()[:2]).upper()
        cards.append(f"""      <figure class="quote" data-reveal>
        {stars}
        <blockquote>“{e(text)}”</blockquote>
        <figcaption>
          <span class="avatar" aria-hidden="true">{e(initials)}</span>
          <span><cite>{e(name)}</cite><small>{e(role)}</small></span>
        </figcaption>
      </figure>""")
    head_txt = "What neighbors in %s say" % e(city) if city else "What our customers say"
    return f"""<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal>
      <p class="eyebrow">Reviews</p>
      <h2 class="h2">{head_txt}</h2>
      <p class="lead">4.9 stars across more than 900 reviews on Google, Yelp and Nextdoor.</p>
    </div>
    <div class="grid grid--3">
{chr(10).join(cards)}
    </div>
    <div class="btn-row center"><a class="link-arrow" href="/reviews.html">Read more reviews</a></div>
  </div>
</section>"""


def faq_section(items, heading="Questions people ask before they call"):
    lis = []
    for i, (q, a) in enumerate(items):
        lis.append(f"""        <div class="faq__item" data-open="{'true' if i == 0 else 'false'}">
          <button class="faq__q" type="button" aria-expanded="{'true' if i == 0 else 'false'}">
            <span>{e(q)}</span>{icon('plus')}
          </button>
          <div class="faq__a"><p>{e(a)}</p></div>
        </div>""")
    return f"""<section class="section">
  <div class="container faq">
    <div data-reveal>
      <p class="eyebrow">FAQ</p>
      <h2 class="h2">{e(heading)}</h2>
      <p class="lead" style="margin-top:1.25rem">Still not sure? Call us. We would rather answer a question for free than have you guess.</p>
      <div class="btn-row">
        <a class="btn btn--dark" href="{TEL}">{icon('phone')} {e(PHONE)}</a>
      </div>
    </div>
    <div class="faq__list" data-reveal>
{chr(10).join(lis)}
    </div>
  </div>
</section>"""


def cta_band(heading="Your house is hot. Let's fix that today.",
             text="Call now for emergency service, or book online in under a minute. Same-day windows on most calls placed before 2pm."):
    return f"""<section class="cta-band">
  <div class="container cta-band__inner">
    <div data-reveal>
      <h2>{e(heading)}</h2>
      <p>{e(text)}</p>
    </div>
    <div class="btn-row" data-reveal>
      <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
      <a class="btn btn--ghost-light btn--lg" href="/contact.html">Book online</a>
    </div>
  </div>
</section>"""


def plans_section():
    cards = []
    for p in PLANS:
        feats = "\n".join(
            "          <li>%s<span>%s</span></li>" % (icon("check"), e(f))
            for f in p["features"]
        )
        badge = '<span class="plan__badge">Most popular</span>' if p["featured"] else ""
        cls = " plan--featured" if p["featured"] else ""
        btn = "btn--primary" if p["featured"] else "btn--ghost"
        cards.append(f"""      <div class="plan{cls}" data-reveal>
        {badge}
        <p class="card__tag">{e(p['sub'])}</p>
        <h3>{e(p['name'])}</h3>
        <p class="plan__price">{e(p['price'])}<small>{e(p['price_note'])}</small></p>
        <ul class="checklist">
{feats}
        </ul>
        <a class="btn {btn} btn--block" href="{p['href']}">{e(p['cta'])}</a>
      </div>""")
    return f"""<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal>
      <p class="eyebrow">Pricing</p>
      <h2 class="h2">Three ways to work with us</h2>
      <p class="lead">Every one of them starts with a number you approve before we begin.</p>
    </div>
    <div class="plans">
{chr(10).join(cards)}
    </div>
  </div>
</section>"""


def services_grid(exclude=None, heading="What we fix", eyebrow="Services",
                  sub="Full HVAC service for homes and small commercial properties across the Inland Empire and Los Angeles County."):
    cards = []
    for s in SERVICES:
        if s["slug"] == exclude:
            continue
        cards.append(f"""      <a class="card card--link" href="/{s['slug']}.html" data-reveal>
        <span class="card__icon">{icon(s['icon'])}</span>
        <p class="card__tag">{e(s['tag'])}</p>
        <h3>{e(s['name'])}</h3>
        <p>{e(s['short'])}</p>
        <span class="link-arrow">Learn more</span>
      </a>""")
    return f"""<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal>
      <p class="eyebrow">{e(eyebrow)}</p>
      <h2 class="h2">{e(heading)}</h2>
      <p class="lead">{e(sub)}</p>
    </div>
    <div class="grid grid--3">
{chr(10).join(cards)}
    </div>
  </div>
</section>"""


def area_chips(heading="Where we work"):
    groups = []
    for region, cities in by_region():
        chips = "\n".join(
            '        <a href="/%s.html">%s %s</a>' % (c["slug"], icon("pin"), e(c["name"]))
            for c in cities
        )
        groups.append(
            '      <div class="chipgroup" data-reveal>\n'
            '        <p class="chipgroup__head">%s</p>\n'
            '        <div class="chips">\n%s\n        </div>\n      </div>'
            % (e(region), chips)
        )
    return f"""<section class="section section--navy">
  <div class="container">
    <div class="section-head" data-reveal style="max-width:46rem">
      <p class="eyebrow">Service areas</p>
      <h2 class="h2">{e(heading)}</h2>
      <p class="lead">The Inland Empire and Los Angeles County — {len(CITIES)} cities across {len(REGIONS)} regions. Same flat-rate pricing everywhere; we never add a travel surcharge for the far end of a route.</p>
    </div>
    <div class="chipgroups">
{chr(10).join(groups)}
    </div>
  </div>
</section>"""


def process_section():
    steps = "\n".join(
        '      <div class="step" data-reveal><h3>%s</h3><p>%s</p></div>' % (e(t), e(d))
        for t, d in PROCESS
    )
    return f"""<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal>
      <p class="eyebrow">How it works</p>
      <h2 class="h2">No mystery, no runaround</h2>
      <p class="lead">Four steps, and you know the price before step four.</p>
    </div>
    <div class="steps">
{steps}
    </div>
  </div>
</section>"""


def figure(icon_name, caption, cls=""):
    return f"""<figure class="figure {cls}" data-reveal>
  {icon(icon_name)}
  <figcaption>{e(caption)}</figcaption>
</figure>"""


# ---------------------------------------------------------------------------
# Schema.org
# ---------------------------------------------------------------------------
def local_business_schema():
    areas = ", ".join('"%s, CA"' % c["name"] for c in CITIES)
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HVACBusiness",
  "name": "{B['legal_name']}",
  "image": "{B['domain']}/assets/img/og.jpg",
  "url": "{B['domain']}",
  "telephone": "+{B['phone_href'].lstrip('+')}",
  "email": "{B['email']}",
  "founder": {{"@type": "Person", "name": "{B['owner']}"}},
  "priceRange": "$$",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{B['street']}",
    "addressLocality": "{B['city']}",
    "addressRegion": "{B['state']}",
    "postalCode": "{B['zip']}",
    "addressCountry": "US"
  }},
  "areaServed": [{areas}],
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "912"
  }},
  "openingHoursSpecification": [{{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    "opens": "07:00",
    "closes": "20:00"
  }}]
}}
</script>"""


def faq_schema(items):
    qs = ",\n".join(
        '    {"@type": "Question", "name": %s, "acceptedAnswer": {"@type": "Answer", "text": %s}}'
        % (jstr(q), jstr(a))
        for q, a in items
    )
    return (
        '<script type="application/ld+json">\n'
        '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[\n'
        + qs
        + "\n]}\n</script>"
    )


def jstr(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


# ---------------------------------------------------------------------------
# Page writers
# ---------------------------------------------------------------------------
PAGES = []


SAMPLE_TAG = '<span class="sample">Sample &mdash; not real</span>'

PREVIEW_BAR = """<div class="preview" id="preview">
  <div class="preview__inner">
    <strong>Preview</strong>
    <span>Phone and email are live. Still placeholder:</span>
    <ul><li>Contractor licence number</li><li>Shop address</li><li>Founding year</li>
    <li>Reviews and the 4.9-star rating</li><li>Booking forms (they confirm but do not send)</li></ul>
    <button class="preview__close" type="button" onclick="document.getElementById('preview').remove()">Hide</button>
  </div>
</div>
"""


def to_relative(html):
    """Root-absolute -> relative. Every page sits at the same level, so this
    works identically at a domain root, in a /repo/ subpath, or over file://."""
    return re.sub(r'(href|src|srcset)="/(?!/)', r'\1="', html)


def apply_preview(html):
    html = html.replace('<p class="eyebrow">Reviews</p>',
                        '<p class="eyebrow">Reviews ' + SAMPLE_TAG + '</p>')
    html = html.replace('<p class="eyebrow">By the numbers</p>',
                        '<p class="eyebrow">By the numbers ' + SAMPLE_TAG + '</p>')
    html = html.replace('<a class="skip-link" href="#main">Skip to content</a>',
                        '<a class="skip-link" href="#main">Skip to content</a>\n' + PREVIEW_BAR)
    return html


def write(path, content):
    content = to_relative(content)
    if PREVIEW:
        content = apply_preview(content)
    out = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(content)
    PAGES.append(path)


def page_home():
    path = "/index.html"
    hero_services = "\n".join(
        '        <a href="/%s.html">%s %s</a>' % (s["slug"], icon("check"), e(s["name"]))
        for s in SERVICES[:5]
    )
    body = f"""{header('home')}
<main id="main">

<section class="hero">
  <div class="container hero__inner">
    <div>
      <span class="hero__flag"><span class="dot"></span> Same-day service available</span>
      <h1>Same-day AC repair across the Inland Empire &amp; LA</h1>
      <p class="lead">Your house is hot. We fix that fast. Serving the Inland Empire and all of Los Angeles County — no overtime charges, flat-rate quotes, and a real arrival window.</p>
      <div class="btn-row">
        <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
        <a class="btn btn--ghost-light btn--lg" href="/contact.html">Book online</a>
      </div>
      <div class="hero__proof">
        <div><b>4.9★</b>912 reviews</div>
        <div><b>{len(CITIES)}</b>Cities served</div>
        <div><b>$0</b>Overtime surcharge</div>
      </div>
    </div>
    <div class="hero__card" data-reveal>
      <h2>Book a visit</h2>
      <p>Tell us what the system is doing. We will call you right back with a window.</p>
      {lead_form('Book a visit', '', 'hero', compact=True)}
    </div>
  </div>
</section>

{trust_strip()}

<section class="section">
  <div class="container split">
    <div data-reveal>
      <p class="eyebrow">Fast</p>
      <h2 class="h2">Cool air back in your house today</h2>
      <p class="lead" style="margin-top:1.25rem">When the temperature hits 105, you need a crew that answers the phone. We show up the same day with a fully stocked truck and get your system running again — usually on the first visit, because the parts that fail out here are the parts we carry.</p>
      <ul class="checklist">
        <li>{icon('check')}<span><strong>Emergency service.</strong> A broken AC is an emergency in the Inland Empire. We take calls late and arrive ready to work.</span></li>
        <li>{icon('check')}<span><strong>Stocked trucks.</strong> Capacitors, contactors, motors, thermostats and refrigerant on board — not on order.</span></li>
        <li>{icon('check')}<span><strong>Honest diagnosis.</strong> If a $200 part fixes it, we will not try to sell you a $9,000 system.</span></li>
      </ul>
      <div class="btn-row">
        <a class="btn btn--dark" href="{TEL}">Call now</a>
        <a class="link-arrow" href="/air-conditioning-repair.html" style="align-self:center">See how repairs work</a>
      </div>
    </div>
    {figure('bolt', 'Same-day emergency dispatch')}
  </div>
</section>

{services_grid()}

<section class="section section--alt">
  <div class="container split split--reverse">
    <div data-reveal>
      <p class="eyebrow">Straight answers</p>
      <h2 class="h2">We would rather fix it than sell you a new one</h2>
      <p class="lead" style="margin-top:1.25rem">Plenty of companies out here run a replacement-first playbook: show up, find a "cracked heat exchanger," quote a system. We do the opposite. We test the ducts, test the charge, test the capacitor, and tell you the smallest thing that will actually solve the problem.</p>
      <ul class="checklist">
        <li>{icon('check')}<span>Flat-rate quote in writing before any work starts</span></li>
        <li>{icon('check')}<span>Repair and replace numbers side by side, so you can decide</span></li>
        <li>{icon('check')}<span>Permits and HERS testing handled on every install</span></li>
        <li>{icon('check')}<span>1-year parts and labor warranty on repairs</span></li>
      </ul>
      <div class="btn-row"><a class="btn btn--ghost" href="/about.html">More about how we work</a></div>
    </div>
    {figure('shield', 'Licensed, bonded and insured')}
  </div>
</section>

{process_section()}

{reviews_section()}

{stats_section()}

{plans_section()}

{area_chips()}

{faq_section(HOME_FAQ)}

{cta_band()}

</main>
{footer()}"""
    schema = local_business_schema() + "\n" + faq_schema(HOME_FAQ)
    write(path, head(
        "Miguel's A/C | Same-Day AC Repair | Inland Empire & Los Angeles",
        "Same-day air conditioning repair, installation and maintenance across the Inland Empire and Los Angeles County. No overtime charges, flat-rate quotes. Call %s." % PHONE,
        path, schema) + body)


def page_services():
    path = "/services.html"
    body = f"""{header('services')}
<main id="main">
<section class="pagehero">
  <div class="container pagehero__inner">
    <p class="eyebrow">Services</p>
    <h1 class="h1">Everything that keeps a house cool</h1>
    <p class="lead">Repair, replacement, ductwork, air quality and maintenance — for single-family homes, ADUs, and small commercial properties across the Inland Empire and Los Angeles County.</p>
    <div class="btn-row">
      <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
      <a class="btn btn--ghost-light btn--lg" href="/contact.html">Book online</a>
    </div>
  </div>
</section>
{crumbs([("Home", "/index.html"), ("Services", None)])}
{trust_strip()}
{services_grid(heading="Pick what you need", eyebrow="All services", sub="Not sure which one applies? Call us and describe what the system is doing — we will tell you for free.")}
{process_section()}
{plans_section()}
{reviews_section()}
{area_chips()}
{cta_band()}
</main>
{footer()}"""
    write(path, head(
        "HVAC Services | AC Repair, Installation & Maintenance | Miguel's A/C",
        "AC repair, system replacement, heat pumps, mini-splits, duct work, air quality and maintenance plans across the Inland Empire and all of Los Angeles County.",
        path, local_business_schema()) + body)


def page_service(s):
    path = "/%s.html" % s["slug"]
    bullets = "\n".join(
        "      <li>%s<span>%s</span></li>" % (icon("check"), e(b)) for b in s["bullets"]
    )
    others = [x for x in SERVICES if x["slug"] != s["slug"]][:3]
    related = "\n".join(f"""      <a class="card card--link" href="/{o['slug']}.html" data-reveal>
        <span class="card__icon">{icon(o['icon'])}</span>
        <h3>{e(o['name'])}</h3>
        <p>{e(o['short'])}</p>
        <span class="link-arrow">Learn more</span>
      </a>""" for o in others)
    city_chips = "\n".join(
        '      <a href="%s">%s %s</a>' % (h, icon("pin"), e(n)) for n, h in AREA_LINKS
    )
    body = f"""{header()}
<main id="main">
<section class="pagehero">
  <div class="container pagehero__inner">
    <p class="eyebrow">{e(s['tag'])}</p>
    <h1 class="h1">{e(s['hero_h1'])}</h1>
    <p class="lead">{e(s['hero_p'])}</p>
    <div class="btn-row">
      <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
      <a class="btn btn--ghost-light btn--lg" href="/contact.html">Book online</a>
    </div>
  </div>
</section>
{crumbs([("Home", "/index.html"), ("Services", "/services.html"), (s["name"], None)])}
{trust_strip()}

<section class="section">
  <div class="container split">
    <div data-reveal>
      <p class="eyebrow">What's included</p>
      <h2 class="h2">{e(s['body_h2'])}</h2>
      <p class="lead" style="margin-top:1.25rem">{e(s['body_p'])}</p>
      <ul class="checklist">
{bullets}
      </ul>
      <div class="btn-row">
        <a class="btn btn--dark" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
        <a class="btn btn--ghost" href="/contact.html">Request a quote</a>
      </div>
    </div>
    <div>
      {figure(s['icon'], s['name'])}
      <div class="card" style="margin-top:1.5rem" data-reveal>
        <h3>Book {e(s['name'].lower())}</h3>
        <p style="margin-bottom:1.25rem">Same-day windows on most calls placed before 2pm.</p>
        {lead_form('Book', '', 'svc', compact=True)}
      </div>
    </div>
  </div>
</section>

{process_section()}

{faq_section(s['faq'], heading="%s: common questions" % s['name'])}

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal>
      <p class="eyebrow">Related</p>
      <h2 class="h2">Often booked together</h2>
    </div>
    <div class="grid grid--3">
{related}
    </div>
  </div>
</section>

<section class="section section--navy">
  <div class="container">
    <div class="section-head" data-reveal style="max-width:44rem">
      <p class="eyebrow">Coverage</p>
      <h2 class="h2">{e(s['name'])} in your city</h2>
      <p class="lead">We run this service everywhere we work, at the same rate.</p>
    </div>
    <div class="chips" data-reveal>
{city_chips}
    </div>
  </div>
</section>

{cta_band()}
</main>
{footer()}"""
    meta = s["meta"].format(phone=PHONE) if "{phone}" in s["meta"] else s["meta"]
    schema = local_business_schema() + "\n" + faq_schema(s["faq"])
    write(path, head(s["title"], meta, path, schema) + body)


def page_service_areas():
    path = "/service-areas.html"
    blocks = []
    for region, cities in by_region():
        cards = "\n".join(f"""        <a class="card card--link" href="/{c['slug']}.html" data-reveal>
          <span class="card__icon">{icon('pin')}</span>
          <p class="card__tag">{e(c['county'])}</p>
          <h3>{e(c['name'])}</h3>
          <p>{e(c['meta_extra'])}</p>
          <span class="link-arrow">HVAC in {e(c['name'])}</span>
        </a>""" for c in cities)
        blocks.append(f"""    <div class="region" data-reveal>
      <div class="region__head">
        <h2 class="h3">{e(region)}</h2>
        <p>{e(DISPATCH[cities[0]['dispatch']])}</p>
      </div>
      <div class="grid grid--3">
{cards}
      </div>
    </div>""")

    body = f"""{header()}
<main id="main">
<section class="pagehero">
  <div class="container pagehero__inner">
    <p class="eyebrow">Service areas</p>
    <h1 class="h1">{len(CITIES)} cities across the Inland Empire and Los Angeles</h1>
    <p class="lead">From Redlands and Riverside out to Santa Monica and the South Bay — Riverside County, San Bernardino County and all of Los Angeles County. Same flat-rate pricing everywhere, with no travel surcharge for the far end of a route.</p>
    <div class="btn-row">
      <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
      <a class="btn btn--ghost-light btn--lg" href="/contact.html">Book online</a>
    </div>
  </div>
</section>
{crumbs([("Home", "/index.html"), ("Service areas", None)])}
{trust_strip()}

<section class="section">
  <div class="container">
    <div class="section-head center" data-reveal>
      <p class="eyebrow">Coverage</p>
      <h2 class="h2">Find your city</h2>
      <p class="lead">Scheduling differs by how far out you are, and we say so honestly below rather than promising every address a same-day window. Don't see your city? Call — if you're near one of these, we probably already drive past you.</p>
    </div>
    <div class="regions">
{chr(10).join(blocks)}
    </div>
  </div>
</section>

{services_grid(heading="Every service, in every city", eyebrow="Services", sub="We do not limit what a route can handle. The same crews run repairs, installs and duct work across the whole service area.")}
{reviews_section()}
{stats_section()}
{cta_band()}
</main>
{footer()}"""
    write(path, head(
        "HVAC Service Areas | Inland Empire & Los Angeles | Miguel's A/C",
        "Miguel's A/C serves %d cities across the Inland Empire and Los Angeles County — Riverside, San Bernardino, Pasadena, Long Beach, Santa Monica, the San Fernando Valley and more." % len(CITIES),
        path, local_business_schema()) + body)


def page_city(c):
    path = "/%s.html" % c["slug"]
    # Prefer neighbours in the same region — they are the genuinely useful links.
    same = [x for x in CITIES if x["region"] == c["region"] and x["slug"] != c["slug"]]
    other = [x for x in CITIES if x["region"] != c["region"]]
    nearby = (same + other)[:7]
    nearby_chips = "\n".join(
        '      <a href="/%s.html">%s %s</a>' % (n["slug"], icon("pin"), e(n["name"]))
        for n in nearby
    )
    svc_cards = "\n".join(f"""      <a class="card card--link" href="/{s['slug']}.html" data-reveal>
        <span class="card__icon">{icon(s['icon'])}</span>
        <p class="card__tag">{e(s['tag'])}</p>
        <h3>{e(s['name'])} in {e(c['name'])}</h3>
        <p>{e(s['short'])}</p>
        <span class="link-arrow">Learn more</span>
      </a>""" for s in SERVICES)
    hoods = "\n".join(
        "      <li>%s<span>%s</span></li>" % (icon("pin"), e(a)) for a in c["areas"]
    )
    city_faq = [
        ("Do you charge extra to come out to %s?" % c["name"],
         "No. We do not add travel surcharges anywhere in our service area. A call in %s is billed at the same rate as a call two blocks from our shop." % c["name"]),
        ("How fast can you get to %s?" % c["name"],
         "%s We would rather quote you a window we can actually hold than promise same-day everywhere and miss it." % DISPATCH[c["dispatch"]]),
        ("Are you licensed to work in %s?" % c["county"],
         "Yes. We are licensed, bonded and insured statewide, and we pull permits with the local building department on every equipment changeout."),
        ("Which brands do you service in %s?" % c["name"],
         "All the major ones — Carrier, Trane, Lennox, Goodman, Rheem, American Standard, Bryant, York, Daikin and Mitsubishi."),
    ]
    body = f"""{header()}
<main id="main">
<section class="pagehero">
  <div class="container pagehero__inner">
    <p class="eyebrow">{e(c['region'])} &middot; {e(c['county'])}</p>
    <h1 class="h1">HVAC and AC repair in {e(c['name'])}</h1>
    <p class="lead">{e(c['blurb'])}</p>
    <p class="pagehero__dispatch">{icon('clock')} {e(DISPATCH[c['dispatch']])}</p>
    <div class="btn-row">
      <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
      <a class="btn btn--ghost-light btn--lg" href="/contact.html">Book online</a>
    </div>
  </div>
</section>
{crumbs([("Home", "/index.html"), ("Service areas", "/service-areas.html"), (c["name"], None)])}
{trust_strip()}

<section class="section">
  <div class="container split">
    <div data-reveal>
      <p class="eyebrow">Local knowledge</p>
      <h2 class="h2">We know the houses in {e(c['name'])}</h2>
      <p class="lead" style="margin-top:1.25rem">{e(c['note'])}</p>
      <p style="margin-top:1rem">That is the difference between a company that services {e(c['name'])} and one that just happens to drive through it. We know which tracts have undersized returns, which era of equipment fails first, and what a fair repair actually costs here.</p>
      <div class="btn-row">
        <a class="btn btn--dark" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
        <a class="btn btn--ghost" href="/contact.html">Book a visit</a>
      </div>
    </div>
    <div class="card" data-reveal>
      <h3>Neighborhoods we cover in {e(c['name'])}</h3>
      <ul class="checklist">
{hoods}
      </ul>
      <p class="form-note" style="margin-top:1.5rem">Nearby and not listed? Call us — the route probably already passes you.</p>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container">
    <div class="section-head center" data-reveal>
      <p class="eyebrow">Services</p>
      <h2 class="h2">What we do in {e(c['name'])}</h2>
      <p class="lead">The full service list, at the same rates we charge everywhere else.</p>
    </div>
    <div class="grid grid--3">
{svc_cards}
    </div>
  </div>
</section>

{process_section()}
{reviews_section(city=c['name'])}
{faq_section(city_faq, heading="%s: common questions" % c['name'])}

<section class="section section--navy">
  <div class="container">
    <div class="section-head" data-reveal style="max-width:44rem">
      <p class="eyebrow">Nearby</p>
      <h2 class="h2">We also serve</h2>
    </div>
    <div class="chips" data-reveal>
{nearby_chips}
      <a href="/service-areas.html">All service areas</a>
    </div>
  </div>
</section>

{cta_band(heading="Hot house in %s? Let's get it sorted." % c['name'], text=DISPATCH[c["dispatch"]] + " Call now for emergency service, or book online in under a minute.")}
</main>
{footer()}"""
    # Only claim same-day where we actually run same-day. A title that promises
    # it on a scheduled-route city contradicts the dispatch note on the page.
    if c["dispatch"] == "same-day":
        title = "Same-Day AC Repair in %s, CA | Miguel's A/C" % c["name"]
        lede = "Same-day air conditioning repair, installation and maintenance"
    else:
        title = "AC Repair & HVAC Service in %s, CA | Miguel's A/C" % c["name"]
        lede = "Air conditioning repair, installation and maintenance"
    desc = "%s in %s, %s. Serving %s No overtime charges. Call %s." % (
        lede, c["name"], c["county"], c["meta_extra"], PHONE)
    schema = local_business_schema() + "\n" + faq_schema(city_faq)
    write(path, head(title, desc, path, schema) + body)


def page_about():
    path = "/about.html"
    body = f"""{header('about')}
<main id="main">
<section class="pagehero">
  <div class="container pagehero__inner">
    <p class="eyebrow">Our story</p>
    <h1 class="h1">Started in a truck. Still answers the phone.</h1>
    <p class="lead">Owner-operated by {e(B['owner'])}. Miguel's A/C has been running Inland Empire routes since {e(B['founded'])}, growing by fixing things correctly the first time and telling people the truth about what their system needed — which turns out to be a decent business model.</p>
  </div>
</section>
{crumbs([("Home", "/index.html"), ("About", None)])}
{trust_strip()}

<section class="section">
  <div class="container split">
    <div data-reveal>
      <p class="eyebrow">Why we do it this way</p>
      <h2 class="h2">The replacement-first playbook is not our playbook</h2>
      <p class="lead" style="margin-top:1.25rem">There is a version of this industry that runs on commissioned salespeople in service uniforms. They arrive at a no-cool call, find something alarming, and leave with a signed contract for a new system. Sometimes the system genuinely needed replacing. Often it needed a $200 capacitor.</p>
      <p style="margin-top:1rem">We built the opposite. Our techs are paid to diagnose, not to close. When a repair is the right call, we repair it. When replacement genuinely is the better economics, we show you both numbers and let you sit with them. A customer who trusts our diagnosis calls us for the next fifteen years — that math works better than one oversold system.</p>
      <ul class="checklist">
        <li>{icon('check')}<span>Technicians are not paid commission on equipment sales</span></li>
        <li>{icon('check')}<span>Flat-rate pricing published before work starts</span></li>
        <li>{icon('check')}<span>Permits and HERS testing on every install, without being asked</span></li>
        <li>{icon('check')}<span>No overtime, weekend or holiday surcharges</span></li>
      </ul>
    </div>
    {figure('home', 'Serving the IE since ' + B['founded'])}
  </div>
</section>

{stats_section(heading="What fifteen years looks like")}

<section class="section">
  <div class="container split split--reverse">
    <div data-reveal>
      <p class="eyebrow">Credentials</p>
      <h2 class="h2">Licensed, bonded, insured — and happy to prove it</h2>
      <p class="lead" style="margin-top:1.25rem">Our California contractor's license number appears on every estimate we write and at the bottom of every page on this site. Before you let any HVAC contractor open a panel in your house, ask for theirs and look it up on the CSLB website. It takes thirty seconds and it filters out a surprising number of people.</p>
      <ul class="checklist">
        <li>{icon('badge')}<span>{e(B['license'])} — California C-20 HVAC contractor</span></li>
        <li>{icon('shield')}<span>General liability and workers' compensation coverage</span></li>
        <li>{icon('check')}<span>EPA Section 608 certified for refrigerant handling</span></li>
        <li>{icon('check')}<span>Factory-trained on all major residential equipment lines</span></li>
      </ul>
      <div class="btn-row"><a class="btn btn--ghost" href="/contact.html">Get in touch</a></div>
    </div>
    {figure('badge', 'California C-20 licensed')}
  </div>
</section>

{process_section()}
{reviews_section(limit=6)}
{area_chips(heading="The routes we run")}
{cta_band()}
</main>
{footer()}"""
    write(path, head(
        "About Miguel's A/C | Inland Empire HVAC Since %s" % B["founded"],
        "Licensed California HVAC contractors serving the Inland Empire and Los Angeles County since %s. Techs paid to diagnose, not to sell. Flat-rate pricing, no overtime charges." % B["founded"],
        path, local_business_schema()) + body)


def page_reviews():
    path = "/reviews.html"
    stars = '<div class="stars">%s</div>' % (icon("star") * 5)
    cards = []
    for name, role, text in REVIEWS:
        initials = "".join(p[0] for p in name.split()[:2]).upper()
        cards.append(f"""      <figure class="quote" data-reveal>
        {stars}
        <blockquote>“{e(text)}”</blockquote>
        <figcaption>
          <span class="avatar" aria-hidden="true">{e(initials)}</span>
          <span><cite>{e(name)}</cite><small>{e(role)}</small></span>
        </figcaption>
      </figure>""")
    body = f"""{header('reviews')}
<main id="main">
<section class="pagehero">
  <div class="container pagehero__inner">
    <p class="eyebrow">Reviews</p>
    <h1 class="h1">4.9 stars across 912 reviews</h1>
    <p class="lead">Google, Yelp and Nextdoor. The pattern in almost all of them is the same: we showed up when we said we would, and we did not try to sell a system that wasn't needed.</p>
    <div class="btn-row">
      <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
      <a class="btn btn--ghost-light btn--lg" href="/contact.html">Book online</a>
    </div>
  </div>
</section>
{crumbs([("Home", "/index.html"), ("Reviews", None)])}
{trust_strip()}

<section class="section">
  <div class="container">
    <div class="grid grid--3">
{chr(10).join(cards)}
    </div>
    <p class="todo">TODO before launch: swap these for real, verbatim reviews pulled from your Google Business Profile, and link the section to your live review page. Do not publish testimonials you cannot attribute to a real customer.</p>
  </div>
</section>

{stats_section(heading="The numbers behind the stars")}
{plans_section()}
{area_chips()}
{cta_band()}
</main>
{footer()}"""
    write(path, head(
        "Customer Reviews | Miguel's A/C | Inland Empire HVAC",
        "Read what Inland Empire and LA homeowners say about Miguel's A/C — 4.9 stars across 912 reviews for same-day repair and honest diagnosis.",
        path, local_business_schema()) + body)


def page_financing():
    path = "/financing.html"
    faq = [
        ("Does applying affect my credit?",
         "The initial pre-qualification is a soft pull that does not affect your score. Only if you move forward with a full application does a hard inquiry happen, and we tell you before that point."),
        ("How fast is approval?",
         "Usually minutes. In most cases we can pre-qualify you on the same visit where we quote the system, so you see the monthly number before we leave."),
        ("Is there a prepayment penalty?",
         "No. You can pay the balance off early at any time without a fee."),
        ("What can I finance?",
         "System replacements, heat pump installs, full duct replacements and larger air quality projects. Small repairs are generally not worth financing and we will say so."),
        ("Do rebates reduce what I finance?",
         "Rebates typically arrive after the install, so you finance the full amount and keep the rebate when it lands. We will walk you through which programs you qualify for."),
    ]
    body = f"""{header('financing')}
<main id="main">
<section class="pagehero">
  <div class="container pagehero__inner">
    <p class="eyebrow">Financing</p>
    <h1 class="h1">A new system, spread across monthly payments</h1>
    <p class="lead">A compressor rarely fails at a convenient moment. Financing lets you fix it now and pay for it over time — with approved credit, no prepayment penalty, and a soft-pull pre-qualification that does not touch your score.</p>
    <div class="btn-row">
      <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
      <a class="btn btn--ghost-light btn--lg" href="/contact.html">Request a quote</a>
    </div>
  </div>
</section>
{crumbs([("Home", "/index.html"), ("Financing", None)])}
{trust_strip()}

<section class="section">
  <div class="container split">
    <div data-reveal>
      <p class="eyebrow">How it works</p>
      <h2 class="h2">See the monthly number before you decide</h2>
      <p class="lead" style="margin-top:1.25rem">When we quote a replacement, we show you the cash price and the monthly payment side by side. No contractor should ever quote you a monthly payment without showing the total — that is how people end up paying far more than the system was worth.</p>
      <ul class="checklist">
        <li>{icon('check')}<span>Soft-pull pre-qualification — no impact on your credit score</span></li>
        <li>{icon('check')}<span>Approval usually in minutes, often during the quote visit</span></li>
        <li>{icon('check')}<span>No prepayment penalty if you pay it off early</span></li>
        <li>{icon('check')}<span>Cash price always shown next to the monthly payment</span></li>
        <li>{icon('check')}<span>Rebates and tax credits are yours to keep on top of it</span></li>
      </ul>
      <p class="todo">TODO before launch: connect this page to your actual lender's application flow (GreenSky, Synchrony, Wells Fargo, etc.) and publish the real APR ranges and terms. Consumer financing disclosures are legally required.</p>
    </div>
    <div class="card" data-reveal>
      <h3>Request a financed quote</h3>
      <p style="margin-bottom:1.25rem">Tell us about the system and we will bring both numbers.</p>
      {lead_form('Financing', '', 'fin', compact=True)}
    </div>
  </div>
</section>

{plans_section()}

<section class="section section--navy">
  <div class="container split">
    <div data-reveal>
      <p class="eyebrow">Stack the savings</p>
      <h2 class="h2">Rebates and tax credits you should not leave on the table</h2>
      <p class="lead">California has some of the most aggressive electrification incentives in the country, and they stack with federal tax credits. On a heat pump install, incentives frequently cover a meaningful share of the project.</p>
      <ul class="checklist">
        <li>{icon('check')}<span>Federal energy-efficient home improvement tax credits</span></li>
        <li>{icon('check')}<span>California electrification and heat pump rebate programs</span></li>
        <li>{icon('check')}<span>Local utility efficiency rebates (SCE, SoCalGas and municipal utilities)</span></li>
        <li>{icon('check')}<span>We file the paperwork with you instead of handing you a form</span></li>
      </ul>
      <div class="btn-row"><a class="btn btn--primary" href="/heat-pumps.html">See heat pump options</a></div>
    </div>
    {figure('dollar', 'Rebates + credits + financing')}
  </div>
</section>

{faq_section(faq, heading="Financing questions")}
{cta_band(heading="Get both numbers before you commit.", text="We will quote the cash price and the monthly payment on the same estimate, so you can compare honestly.")}
</main>
{footer()}"""
    write(path, head(
        "HVAC Financing | Monthly Payments on a New System | Miguel's A/C",
        "Finance a new AC or heat pump with monthly payments, soft-pull pre-qualification and no prepayment penalty. Serving the Inland Empire and LA.",
        path, local_business_schema() + "\n" + faq_schema(faq)) + body)


def page_contact():
    path = "/contact.html"
    body = f"""{header('contact')}
<main id="main">
<section class="pagehero">
  <div class="container pagehero__inner">
    <p class="eyebrow">Contact</p>
    <h1 class="h1">Tell us what your system is doing</h1>
    <p class="lead">Fastest way to reach us is the phone — a person picks up during business hours. If it is late or you would rather type it out, the form goes to the same dispatcher.</p>
  </div>
</section>
{crumbs([("Home", "/index.html"), ("Contact", None)])}
{trust_strip()}

<section class="section">
  <div class="container split">
    <div data-reveal>
      <p class="eyebrow">Reach us</p>
      <h2 class="h2">Call, text or book online</h2>
      <ul class="checklist" style="margin-top:1.75rem">
        <li>{icon('phone')}<span><strong>Phone</strong><br><a class="link-arrow" href="{TEL}">{e(PHONE)}</a><br><small>Ask for {e(B['owner'].split()[0])}</small></span></li>
        <li>{icon('calendar')}<span><strong>Email</strong><br><a class="link-arrow" href="mailto:{e(B['email'])}">{e(B['email'])}</a></span></li>
        <li>{icon('pin')}<span><strong>Shop</strong><br>{e(B['address_line'])}</span></li>
        <li>{icon('clock')}<span><strong>Hours</strong><br>{e(B['hours_weekday'])}<br>{e(B['hours_emergency'])}</span></li>
        <li>{icon('badge')}<span><strong>License</strong><br>{e(B['license'])}</span></li>
      </ul>
      <p class="todo">TODO before launch: replace the placeholder phone, email, address and license number in <code>data.py</code>, then embed a Google Map of your shop location here.</p>
      <div class="btn-row">
        <a class="btn btn--primary btn--lg" href="{TEL}">{icon('phone')} Call {e(PHONE)}</a>
      </div>
    </div>
    <div class="card" data-reveal>
      <h3>Request service</h3>
      <p style="margin-bottom:1.25rem">Same-day windows on most requests submitted before 2pm.</p>
      {lead_form('Request service', '', 'contact')}
      <p class="todo">TODO: this form currently confirms inline and does not send anywhere. Point it at your CRM, ServiceTitan, Housecall Pro, or a form service like Formspree before launch.</p>
    </div>
  </div>
</section>

{area_chips(heading="Cities we dispatch to")}
{faq_section(HOME_FAQ)}
{cta_band()}
</main>
{footer()}"""
    write(path, head(
        "Contact Miguel's A/C | Book Same-Day HVAC Service",
        "Call %s or book online for same-day AC repair across the Inland Empire and eastern Los Angeles County." % PHONE,
        path, local_business_schema()) + body)


def write_extras():
    urls = "\n".join(
        "  <url><loc>%s%s</loc><changefreq>monthly</changefreq><priority>%s</priority></url>"
        % (B["domain"], p, "1.0" if p == "/index.html" else "0.8")
        for p in sorted(PAGES)
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + "\n</urlset>\n"
        )
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % B["domain"])


def main():
    page_home()
    page_services()
    for s in SERVICES:
        page_service(s)
    page_service_areas()
    for c in CITIES:
        page_city(c)
    page_about()
    page_reviews()
    page_financing()
    page_contact()
    write_extras()
    print("Built %d pages:" % len(PAGES))
    for p in sorted(PAGES):
        print("  ", p)


if __name__ == "__main__":
    main()
