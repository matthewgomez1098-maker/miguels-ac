#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bundle the whole site into one self-contained HTML file.

    python3 bundle.py [output.html]

Produces a single file with every page inlined and a hash router, so the
43-page site can be shared as one private link with no hosting. Everything is
embedded — fonts, stylesheet, logo — because the artifact host blocks requests
to any external origin.

This is a share/preview artifact, not the deployable site. Run build.py for that.
"""
import base64
import html as htmllib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
from data import BUSINESS, CITIES  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "miguels-ac-preview.html")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def data_uri(path, mime):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode())


def grab(html, tag, attrs=""):
    """Return the first <tag ...>...</tag> block, inclusive."""
    m = re.search(r"<%s%s[^>]*>" % (tag, attrs), html)
    if not m:
        raise SystemExit("could not find <%s%s> " % (tag, attrs))
    start = m.start()
    depth, i = 0, m.start()
    open_re = re.compile(r"<%s[\s>]" % tag)
    close = "</%s>" % tag
    while i < len(html):
        if open_re.match(html, i):
            depth += 1
        elif html.startswith(close, i):
            depth -= 1
            if depth == 0:
                return html[start:i + len(close)]
        i += 1
    raise SystemExit("unbalanced <%s>" % tag)


def ascii_html(s):
    """Non-ASCII -> numeric entities. innerHTML decodes these, so routed content
    is safe no matter what charset the host document declares."""
    return "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in s)


def ascii_css(s):
    """Non-ASCII -> CSS unicode escapes; CSS strings cannot use HTML entities.
    The trailing space terminates the escape so the next char is not eaten."""
    return "".join(c if ord(c) < 128 else "\\%04X " % ord(c) for c in s)


def ascii_js(s):
    return json.dumps(s)          # ensure_ascii gives us \uXXXX


SAMPLE = '<span class="sample">Sample &mdash; not real</span>'


def mark_samples(html):
    """Label the invented testimonials and stats in-place. The banner at the top
    can be dismissed; these cannot, so nothing fabricated reads as genuine."""
    return (html
            .replace('<p class="eyebrow">Reviews</p>',
                     '<p class="eyebrow">Reviews ' + SAMPLE + '</p>')
            .replace('<p class="eyebrow">By the numbers</p>',
                     '<p class="eyebrow">By the numbers ' + SAMPLE + '</p>'))


def rewrite_links(html):
    """/riverside.html -> #/riverside ; /index.html -> #/index"""
    html = re.sub(r'href="/([a-z0-9\-]+)\.html"', r'href="#/\1"', html)
    html = html.replace('href="/index.html"', 'href="#/index"')
    return html


def main():
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html")
                   and f != os.path.basename(OUT))
    if not pages:
        raise SystemExit("no pages — run build.py first")

    index = read("index.html")

    # --- shared chrome, taken once from index.html -------------------------
    topbar = grab(index, "div", r' class="topbar"')
    header = grab(index, "header")
    callbar = grab(index, "div", r' class="callbar"')
    footer = grab(index, "footer")

    # --- inline assets ------------------------------------------------------
    css = ascii_css(read("assets", "css", "style.css"))
    fonts = ascii_css(read("assets", "fonts", "fonts.css"))
    for name in ("archivo-var", "inter-var"):
        fonts = fonts.replace(
            "url('/assets/fonts/%s.woff2')" % name,
            "url('%s')" % data_uri("assets/fonts/%s.woff2" % name, "font/woff2"),
        )

    logo = data_uri("assets/img/logo-mark.webp", "image/webp")
    # <picture> with a same-origin srcset can't resolve here — collapse to one img.
    def swap_logo(block):
        return re.sub(
            r'<picture class="logo__mark">.*?</picture>',
            '<img class="logo__mark-img" src="%s" alt="" width="192" height="192">' % logo,
            block, flags=re.S)

    header, footer = swap_logo(header), swap_logo(footer)
    topbar, header, callbar, footer = [
        ascii_html(rewrite_links(x)) for x in (topbar, header, callbar, footer)]

    # --- every page's <main> ------------------------------------------------
    routes, titles = [], []
    for f in pages:
        html = read(f)
        slug = f[:-5]
        raw = re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", html, re.S).group(1))
        title = htmllib.unescape(raw)          # document.title takes plain text
        body = mark_samples(rewrite_links(grab(html, "main")))
        body = ascii_html(body)
        routes.append('  %s: %s,' % (js_key(slug), js_str(body)))
        titles.append('  %s: %s,' % (js_key(slug), ascii_js(title)))

    js_app = ascii_html(read("assets", "js", "main.js"))
    # main.js binds once on load; the router needs to re-bind after each render.
    js_app = js_app.replace("(function () {\n  \"use strict\";", "window.__miguelsInit = function () {\n  \"use strict\";")
    js_app = re.sub(r"\}\)\(\);\s*$", "};\n", js_app)

    placeholders = [
        "Contractor licence number", "Shop address", "Founding year (2009)",
        "Customer reviews and the 4.9★ / 912 rating", "Booking forms (they confirm but do not send)",
    ]
    chips = ascii_html("".join("<li>%s</li>" % p for p in placeholders))

    out = TEMPLATE % {
        "fonts": fonts,
        "css": css,
        "topbar": topbar,
        "header": header,
        "callbar": callbar,
        "footer": footer,
        "routes": "\n".join(routes),
        "titles": "\n".join(titles),
        "app_js": js_app,
        "chips": chips,
        "phone": BUSINESS["phone"],
        "count": len(pages),
        "cities": len(CITIES),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(out)
    print("bundled %d pages -> %s (%.1f KB)" % (len(pages), OUT, os.path.getsize(OUT) / 1024))


def js_str(s):
    return ("`" + s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${") + "`")


def js_key(s):
    return '"%s"' % s


TEMPLATE = """<title>Miguel's A/C</title>
<style>
%(fonts)s
%(css)s

/* ---- Preview chrome. Not part of the site; kept visually separate so nobody
        mistakes the placeholder notice for site content. ---- */
.preview {
  background: #FFF8E5; border-bottom: 1px solid #E6C77A; color: #6B4E12;
  font-family: var(--font-body); font-size: .8125rem; line-height: 1.5;
}
.preview__inner {
  max-width: var(--container); margin-inline: auto; padding: .75rem var(--gutter);
  display: flex; flex-wrap: wrap; gap: .5rem 1.25rem; align-items: baseline;
}
.preview strong { font-family: var(--font-display); font-weight: 700; color: #4E3A0C; }
.preview ul { display: flex; flex-wrap: wrap; gap: .35rem .5rem; list-style: none; margin: 0; padding: 0; }
.preview li {
  background: rgba(120,90,20,.10); border: 1px solid rgba(120,90,20,.22);
  border-radius: 999px; padding: .1rem .55rem; font-size: .75rem;
}
.preview__close {
  margin-left: auto; background: none; border: 1px solid rgba(120,90,20,.35);
  border-radius: 4px; color: inherit; cursor: pointer; font-size: .75rem;
  padding: .2rem .6rem; font-weight: 600;
}
.preview__close:hover { background: rgba(120,90,20,.12); }
.sample {
  display: inline-block; margin-left: .5rem; vertical-align: middle;
  background: #FFF8E5; border: 1px solid #E6C77A; color: #6B4E12;
  border-radius: 999px; padding: .1rem .5rem;
  font-family: var(--font-body); font-size: .625rem; font-weight: 600;
  letter-spacing: .04em; text-transform: none;
}
.logo__mark-img { display: block; width: 54px; height: auto; flex: none; }
.footer .logo__mark-img { width: 62px; }
@media (max-width: 700px) { .preview ul { display: none; } }
</style>

<div class="preview" id="preview">
  <div class="preview__inner">
    <strong>Private preview</strong>
    <span>%(count)d pages, %(cities)d cities. Phone and email are live &mdash; still placeholder:</span>
    <ul>%(chips)s</ul>
    <button class="preview__close" type="button" onclick="document.getElementById('preview').remove()">Hide</button>
  </div>
</div>

%(topbar)s
%(header)s
%(callbar)s
<div id="view"></div>
%(footer)s

<script>
const ROUTES = {
%(routes)s
};
const TITLES = {
%(titles)s
};

%(app_js)s

function render(slug) {
  if (!ROUTES[slug]) slug = "index";
  document.getElementById("view").innerHTML = ROUTES[slug];
  document.title = TITLES[slug] || "Miguel's A/C";

  // Reflect the active page in the nav, the way the generated pages do.
  document.querySelectorAll('.nav a[aria-current]').forEach(function (a) {
    a.removeAttribute("aria-current");
  });
  document.querySelectorAll('.nav a[href="#/' + slug + '"]').forEach(function (a) {
    a.setAttribute("aria-current", "page");
  });

  // Close any open menu left over from the click that got us here.
  var nav = document.getElementById("primary-nav");
  if (nav) nav.setAttribute("data-open", "false");
  var burger = document.querySelector(".burger");
  if (burger) burger.setAttribute("aria-expanded", "false");
  document.querySelectorAll('.nav__group').forEach(function (g) {
    g.setAttribute("data-open", "false");
  });

  window.__miguelsInit();
  window.scrollTo({ top: 0, behavior: "instant" });
  setTimeout(revealFailsafe, 700);
}

/* Scroll-reveal starts elements at opacity 0 and relies on IntersectionObserver
   callbacks to bring them back. Some embedding contexts - a hidden tab, an
   iframe that starts offscreen - never deliver those callbacks, which would
   leave the page blank. Probe whether the observer works at all; if it does
   not, show everything rather than risk an empty preview. */
var ioWorks = false;
if ("IntersectionObserver" in window) {
  new IntersectionObserver(function (entries, obs) {
    if (entries.some(function (e) { return e.isIntersecting; })) {
      ioWorks = true;
      obs.disconnect();
    }
  }).observe(document.querySelector(".header"));
} 

function revealFailsafe() {
  if (ioWorks) return;
  // A context that withholds observer callbacks usually freezes transitions too,
  // so drop the animation and snap to the final state. Visible beats pretty.
  document.querySelectorAll("[data-reveal]:not(.is-visible)").forEach(function (el) {
    el.style.transition = "none";
    el.classList.add("is-visible");
  });
}
window.addEventListener("scroll", function () {
  if (!ioWorks) revealFailsafe();
}, { passive: true });

function currentSlug() {
  var h = location.hash.replace(/^#\\/?/, "");
  return h || "index";
}

window.addEventListener("hashchange", function () { render(currentSlug()); });
render(currentSlug());
</script>
"""

if __name__ == "__main__":
    main()
