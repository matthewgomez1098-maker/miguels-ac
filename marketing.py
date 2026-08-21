#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miguel's A/C — print and social artwork.

    python3 marketing.py

Generates into print/:
    door-hanger.html    4.25 x 11 in, front + back, bleed + aligned die-cut
    business-card.html  3.5 x 2 in, front + back, bleed + safe area
    flyer.html          8.5 x 11 in letter leave-behind
    instagram.html      1080x1350 posts and 1080x1920 stories

Contact details come from data.py, so the phone number on a door hanger cannot
drift from the phone number on the website — which is exactly how the first set
of artwork ended up with three different numbers on it.

Export: open the file, Cmd-P, Save as PDF, margins None, scale 100%, and tick
"Background graphics". Text stays vector, so there is no DPI to worry about.
For Instagram, screenshot each canvas or use the download button on the page.
"""
import os
import sys

sys.dont_write_bytecode = True
from data import BUSINESS as B  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "print")

PHONE = B["phone"]
TEL = "tel:+" + B["phone_href"].lstrip("+")
EMAIL = B["email"]
SITE = "matthewgomez1098-maker.github.io/miguels-ac"

# The license number is still a placeholder. California requires the real number
# on contractor advertising, so it renders as an obvious blank rather than a
# convincing fake — nobody can send these to a printer without noticing.
LICENCE_IS_REAL = "0000000" not in B["license"]
LICENCE = B["license"] if LICENCE_IS_REAL else "CSLB Lic. # ____________"

SERVICES_SHORT = [
    ("snow", "AC repair", "Same-day, most calls"),
    ("unit", "New systems", "Sized right, permitted"),
    ("wrench", "Maintenance", "Two tune-ups a year"),
    ("flame", "Heating", "Furnaces and heat pumps"),
    ("duct", "Ductwork", "Testing, sealing, replacement"),
    ("leaf", "Air quality", "Filtration and ventilation"),
]

PROMISES = [
    "Same-day service on most calls",
    "No overtime or weekend charges",
    "Flat-rate quote before work starts",
    "1-year parts and labor warranty",
]

ICONS = {
    "snow": '<path d="M12 2v20M12 2l-3 3M12 2l3 3M12 22l-3-3M12 22l3-3M2.7 7l17.3 10M2.7 17L20 7"/>',
    "unit": '<rect x="3" y="5" width="18" height="8" rx="1.5"/><path d="M7 17v2M12 17v3M17 17v2M6 9h12"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0 5.3 5.3l-8.5 8.5a2.8 2.8 0 0 1-4-4l8.5-8.5a4 4 0 0 0-1.3-1.3z"/><path d="M14.7 6.3 18 3l3 3-3.3 3.3"/>',
    "flame": '<path d="M12 2s5 5.5 5 10a5 5 0 0 1-10 0c0-1.5.6-2.9 1.4-4C9 10 12 8 12 2z"/>',
    "duct": '<path d="M3 7h11v10H3zM14 9h4l3 3-3 3h-4"/><path d="M6 7v10M9 7v10"/>',
    "leaf": '<path d="M4 20c0-9 6-14 16-14 0 10-5 15-14 15H4v-1z"/><path d="M9 15c2-3 5-5 8-6"/>',
    "phone": '<path d="M6 3h4l2 5-2.5 1.5a12 12 0 0 0 5 5L16 12l5 2v4a2 2 0 0 1-2.2 2A17 17 0 0 1 4 5.2 2 2 0 0 1 6 3z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 6l10 7L22 6"/>',
    "web": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/>',
    "pin": '<path d="M12 21s7-5.7 7-11a7 7 0 1 0-14 0c0 5.3 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/>',
    "check": '<path d="m4 12 5 5L20 6"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.5C7.4 20.4 4 17 4 12V6l8-3z"/><path d="m9 12 2 2 4-4"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
}


QR_URL = "https://" + SITE + "/"


def qr_svg(fg="#0A2240", bg="none"):
    """Inline SVG QR for QR_URL. Vector, so it prints crisp at any size.
    Falls back to nothing if the qrcode module is missing - a missing QR is
    better than a broken one that scans to the wrong place."""
    try:
        import qrcode
    except ImportError:
        return ""
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,
                      box_size=1, border=0)
    q.add_data(QR_URL)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    rects = "".join(
        '<rect x="%d" y="%d" width="1" height="1"/>' % (x, y)
        for y, row in enumerate(m) for x, v in enumerate(row) if v
    )
    return ('<svg class="qr" viewBox="0 0 %d %d" shape-rendering="crispEdges" '
            'role="img" aria-label="Scan for miguelsac site">'
            '<rect width="%d" height="%d" fill="%s"/>'
            '<g fill="%s">%s</g></svg>' % (n, n, n, n, bg, fg, rects))


def ic(name, cls=""):
    return ('<svg class="ic %s" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">%s</svg>'
            % (cls, ICONS[name]))


# ---------------------------------------------------------------------------
# Shared CSS
# ---------------------------------------------------------------------------
BASE_CSS = """
@font-face{font-family:'Archivo';font-style:normal;font-weight:600 800;font-display:block;
  src:url('../assets/fonts/archivo-var.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:400 700;font-display:block;
  src:url('../assets/fonts/inter-var.woff2') format('woff2')}

:root{
  --navy:#071C38; --navy2:#0D2E58; --brand:#2478C0; --accent:#54A8E4;
  --ink:#0A2240; --body:#4A5F78; --line:#DFE7F0; --paper:#fff;
  --display:'Archivo',system-ui,sans-serif; --text:'Inter',system-ui,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#8792a3;font-family:var(--text);color:var(--body);
  -webkit-font-smoothing:antialiased;padding:24px}
ul{list-style:none}
h1,h2,h3{font-family:var(--display);color:var(--ink);line-height:1.02;
  letter-spacing:-.03em;font-weight:800}
.ic{width:1em;height:1em;flex:none;display:block}

/* Every artboard: exact physical size, bleed included. */
.sheet{position:relative;overflow:hidden;background:var(--paper);
  margin:0 auto 24px;box-shadow:0 10px 40px rgba(0,0,0,.35)}

.noprint{max-width:760px;margin:0 auto 24px;background:#fff;border-radius:8px;
  padding:16px 20px;font-size:14px;line-height:1.6;color:#0A2240}
.noprint h2{font-size:17px;margin-bottom:6px}
.noprint code{background:#eef2f7;padding:1px 5px;border-radius:3px;font-size:12px}
.noprint button{margin-top:10px;background:#2478C0;color:#fff;border:0;border-radius:5px;
  padding:9px 16px;font:600 14px var(--display);cursor:pointer}
.noprint button:hover{background:#1B5E99}
.warn{background:#FFF8E5;border:1px solid #E6C77A;color:#6B4E12;border-radius:6px;
  padding:10px 14px;margin-top:12px;font-size:13px}

/* Trim/safe guides are screen-only aids. */
.guide{position:absolute;inset:var(--bleed);border:1px dashed rgba(255,0,80,.55);
  pointer-events:none;z-index:99}
.guide::after{content:'trim';position:absolute;top:-14px;left:0;font:600 8px var(--text);
  color:rgba(255,0,80,.75)}
body.clean .guide{display:none}

@media print{
  body{background:none;padding:0}
  .noprint{display:none}
  .sheet{box-shadow:none;margin:0;break-after:page}
  .sheet:last-child{break-after:auto}
  .guide{display:none}
}
"""


def shell(title, css, body, page_css, note=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &mdash; Miguel's A/C</title>
<style>{BASE_CSS}{css}
@media print{{@page{{{page_css}}}}}
</style>
</head>
<body>
<div class="noprint">
  <h2>{title}</h2>
  {note}
  <button onclick="document.body.classList.toggle('clean')">Toggle trim guides</button>
  <button onclick="window.print()">Print / Save as PDF</button>
</div>
{body}
</body>
</html>
"""


PRINT_NOTE = ("Print with <b>margins: None</b>, <b>scale 100%</b>, and "
              "<b>Background graphics ON</b>. Text exports as vector, so there is no "
              "resolution limit. The dashed line is the trim edge &mdash; keep anything "
              "that must survive the cut inside it.")


def licence_warning():
    if LICENCE_IS_REAL:
        return ""
    return ('<div class="warn"><b>Do not send to a printer yet.</b> The contractor '
            'license renders as a blank line because <code>data.py</code> still has the '
            'placeholder. California requires the real number on contractor advertising '
            '(B&amp;P Code &sect;7030.5). Fill in <code>BUSINESS["license"]</code> and '
            're-run <code>python3 marketing.py</code>.</div>')


def contact_block(cls=""):
    return f"""<ul class="contact {cls}">
  <li>{ic('phone')}<b>{PHONE}</b></li>
  <li>{ic('mail')}<span>{EMAIL}</span></li>
  <li>{ic('web')}<span>{SITE}</span></li>
</ul>"""


# ---------------------------------------------------------------------------
# Door hanger — 4.25 x 11 in
# ---------------------------------------------------------------------------
def door_hanger():
    css = """
.sheet--dh{width:4.5in;height:11.25in;--bleed:.125in}
/* The die-cut must sit identically on both sides or the print will not line up,
   so it is one rule applied to both faces. */
.diecut{position:absolute;left:50%;transform:translateX(-50%);z-index:40;pointer-events:none}
.diehole{top:.55in;width:1.25in;height:1.25in;border-radius:50%;
  border:1.5px dashed rgba(255,0,80,.6)}
.dieslot{top:.125in;width:.42in;height:.55in;border-left:1.5px dashed rgba(255,0,80,.6);
  border-right:1.5px dashed rgba(255,0,80,.6)}
body.clean .diecut{display:none}

.dh{position:absolute;inset:0;display:flex;flex-direction:column;
  padding:2.15in .42in .5in}
.dh--front{background:linear-gradient(170deg,#0D2E58 0%,#071C38 62%)}
.dh__cap{position:absolute;top:0;left:0;right:0;height:2.05in;background:var(--navy)}
.dh__logo{width:1.55in;height:auto;margin:0 auto .22in;display:block}
.dh__name{font-family:var(--display);font-size:31pt;color:#fff;text-align:center;
  line-height:.94;letter-spacing:-.035em}
.dh__tag{text-align:center;color:var(--accent);font:700 8.5pt/1 var(--display);
  letter-spacing:.16em;text-transform:uppercase;margin-top:.1in}
.dh__rule{height:2px;background:rgba(84,168,228,.4);margin:.26in 0}
.dh__lead{color:#fff;font-family:var(--display);font-size:23pt;line-height:1.06;letter-spacing:-.03em;
  text-align:center;letter-spacing:-.02em}
.dh__sub{color:#AFC4D8;font-size:10pt;line-height:1.5;text-align:center;margin-top:.14in}
.dh__cta{background:var(--accent);border-radius:.09in;
  padding:.19in .12in;text-align:center;color:var(--navy)}
.dh__cta small{display:block;font:700 8pt/1 var(--display);letter-spacing:.15em;
  text-transform:uppercase;opacity:.72}
.dh__cta b{display:block;font:800 26pt/1 var(--display);letter-spacing:-.03em;margin-top:.05in}
.dh__mid{margin:auto 0;padding:.1in 0}
.dh__promise{margin-bottom:.22in;display:grid;gap:.095in}
.dh__promise li{display:flex;gap:.08in;align-items:flex-start;color:#CBDCEA;font-size:8.7pt;line-height:1.3}
.dh__promise .ic{font-size:10pt;color:var(--accent);margin-top:.5pt}
.dh__lic{text-align:center;color:#7E97AE;font-size:7pt;letter-spacing:.05em}

.dh--back{background:#fff}
.dh--back .dh__cap{background:var(--navy)}
.dh__backhead{font-family:var(--display);font-size:20pt;color:#fff;text-align:center;
  letter-spacing:-.03em}
.dh__backsub{text-align:center;color:var(--accent);font:700 7.5pt/1 var(--display);
  letter-spacing:.16em;text-transform:uppercase;margin-top:.08in}
.svc{display:grid;gap:.105in;margin-bottom:.24in}
.svc li{display:flex;gap:.13in;align-items:center;padding-bottom:.095in;
  border-bottom:1px solid var(--line)}
.svc li:last-child{border-bottom:0}
.svc .ic{font-size:15pt;color:var(--brand)}
.svc b{display:block;font:700 10.5pt/1.15 var(--display);color:var(--ink)}
.svc span{display:block;font-size:7.8pt;color:var(--body);margin-top:1pt}
.areas{background:#F3F7FC;border:1px solid var(--line);border-radius:.07in;
  padding:.14in .15in;margin-bottom:.2in}
.areas b{display:block;font:700 7.5pt/1 var(--display);letter-spacing:.13em;
  text-transform:uppercase;color:var(--brand);margin-bottom:.06in}
.areas p{font-size:8pt;line-height:1.45;color:var(--body)}
.qrbox{margin-top:auto;display:flex;gap:.16in;align-items:center;
  border:1px solid var(--line);border-radius:.07in;padding:.15in;margin-bottom:.2in}
.qr{width:.92in;height:.92in;flex:none}
.qrbox b{display:block;font:700 10pt/1.1 var(--display);color:var(--ink)}
.qrbox p{font-size:7.6pt;line-height:1.35;color:var(--body);margin-top:2pt}
.qrbox span{display:block;font-size:6.6pt;color:var(--brand);margin-top:3pt;word-break:break-all}
.contact{display:grid;gap:.1in}
.contact li{display:flex;gap:.11in;align-items:center;font-size:9.5pt;color:var(--ink)}
.contact .ic{font-size:12pt;color:var(--brand)}
.contact b{font:800 14pt/1 var(--display);letter-spacing:-.02em}
.contact span{word-break:break-all;font-size:8.4pt}
"""
    promises = "".join("<li>%s<span>%s</span></li>" % (ic("check"), p) for p in PROMISES)
    svc = "".join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (ic(k), n, d)
                  for k, n, d in SERVICES_SHORT)
    die = ('<div class="diecut diehole"></div><div class="diecut dieslot"></div>')

    body = f"""
<section class="sheet sheet--dh">
  <div class="guide"></div>{die}
  <div class="dh dh--front">
    <div class="dh__cap"></div>
    <img class="dh__logo" src="../assets/img/logo-print.png" alt="Miguel's A/C">
    <div class="dh__name">MIGUEL'S A/C</div>
    <div class="dh__tag">Trusted Locally</div>
    <div class="dh__rule"></div>
    <div class="dh__mid">
      <p class="dh__lead">Your neighbors<br>already have<br>our number.</p>
      <p class="dh__sub">Same-day AC repair across the Inland Empire and Los Angeles County. We answer the phone.</p>
    </div>
    <ul class="dh__promise">{promises}</ul>
    <div class="dh__cta"><small>Call or text</small><b>{PHONE}</b></div>
    <p class="dh__lic" style="margin-top:.14in">{LICENCE}</p>
  </div>
</section>

<section class="sheet sheet--dh">
  <div class="guide"></div>{die}
  <div class="dh dh--back">
    <div class="dh__cap" style="height:1.9in;display:flex;flex-direction:column;justify-content:center">
      <div class="dh__backhead">What we do</div>
      <div class="dh__backsub">Homes &middot; ADUs &middot; Small commercial</div>
    </div>
    <ul class="svc">{svc}</ul>
    <div class="areas">
      <b>Where we work</b>
      <p>Rancho Cucamonga &middot; Ontario &middot; Fontana &middot; Riverside &middot; San Bernardino &middot; Corona &middot; Redlands &middot; Moreno Valley &middot; Pomona &middot; Pasadena &middot; West Covina &middot; and across LA County</p>
    </div>
    <div class="qrbox">
      {qr_svg()}
      <div>
        <b>See the whole thing</b>
        <p>Scan for services, service areas and booking.</p>
        <span>{SITE}</span>
      </div>
    </div>
    {contact_block()}
    <p class="dh__lic" style="margin-top:.16in;color:var(--body)">{LICENCE}</p>
  </div>
</section>
"""
    note = ("Two artboards: front, then back. Trim <b>4.25 &times; 11 in</b> with "
            "0.125 in bleed. The dashed circle and slot are the standard door-hanger "
            "die &mdash; identical on both faces so a double-sided cut lines up. "
            + PRINT_NOTE + licence_warning())
    return shell("Door hanger", css, body, "size:4.5in 11.25in;margin:0", note)


# ---------------------------------------------------------------------------
# Business card — 3.5 x 2 in
# ---------------------------------------------------------------------------
def business_card():
    css = """
.sheet--bc{width:3.75in;height:2.25in;--bleed:.125in}
.bc{position:absolute;inset:0;padding:.3in .32in;display:flex}
.bc--front{background:linear-gradient(150deg,#0D2E58,#071C38);color:#fff;
  align-items:center;gap:.22in}
.bc__logo{width:1.02in;height:auto;flex:none}
.bc__name{font-family:var(--display);font-size:19pt;color:#fff;line-height:.95;
  letter-spacing:-.035em}
.bc__tag{color:var(--accent);font:700 6.4pt/1 var(--display);letter-spacing:.15em;
  text-transform:uppercase;margin-top:.055in}
.bc__svc{color:#AFC4D8;font-size:7.1pt;margin-top:.1in;line-height:1.4}
.bc__phone{margin-top:.11in;font:800 13pt/1 var(--display);color:var(--accent);
  letter-spacing:-.02em}

.bc--back{background:#fff;flex-direction:column;justify-content:center}
.bc--back .contact{display:grid;gap:.085in}
.bc--back .contact li{display:flex;gap:.1in;align-items:center;color:var(--ink);font-size:8pt}
.bc--back .contact .ic{font-size:10.5pt;color:var(--brand)}
.bc--back .contact b{font:800 12.5pt/1 var(--display);letter-spacing:-.02em}
.bc__head{font-family:var(--display);font-size:12.5pt;color:var(--ink);margin-bottom:.04in}
.bc__sub{font-size:7.4pt;color:var(--body);margin-bottom:.16in;line-height:1.4}
.bc__foot{margin-top:.16in;padding-top:.1in;border-top:1px solid var(--line);
  font-size:6.4pt;color:var(--body);display:flex;justify-content:space-between;gap:.1in}
"""
    body = f"""
<section class="sheet sheet--bc">
  <div class="guide"></div>
  <div class="bc bc--front">
    <img class="bc__logo" src="../assets/img/logo-print.png" alt="Miguel's A/C">
    <div>
      <div class="bc__name">MIGUEL'S<br>A/C</div>
      <div class="bc__tag">Trusted Locally</div>
      <div class="bc__svc">Repair &middot; Install &middot; Maintenance</div>
      <div class="bc__phone">{PHONE}</div>
    </div>
  </div>
</section>

<section class="sheet sheet--bc">
  <div class="guide"></div>
  <div class="bc bc--back">
    <div class="bc__head">Miguel Guardado</div>
    <p class="bc__sub">Same-day AC repair &mdash; Inland Empire &amp; Los Angeles County</p>
    {contact_block()}
    <div class="bc__foot"><span>{LICENCE}</span><span>No overtime charges</span></div>
  </div>
</section>
"""
    note = ("Front, then back. Trim <b>3.5 &times; 2 in</b> with 0.125 in bleed. "
            "Keep text at least 0.125 in inside the dashed line. " + PRINT_NOTE
            + licence_warning())
    return shell("Business card", css, body, "size:3.75in 2.25in;margin:0", note)


# ---------------------------------------------------------------------------
# Flyer — 8.5 x 11 in
# ---------------------------------------------------------------------------
def flyer():
    css = """
.sheet--fl{width:8.75in;height:11.25in;--bleed:.125in}
.fl{position:absolute;inset:0;display:flex;flex-direction:column}
.fl__hero{flex:none;background:linear-gradient(160deg,#0D2E58,#071C38);color:#fff;
  padding:.6in .7in .5in;position:relative;overflow:hidden}
.fl__hero::after{content:'';position:absolute;width:6in;height:6in;right:-2in;top:-2.6in;
  border-radius:50%;background:radial-gradient(circle,rgba(84,168,228,.24),transparent 68%)}
.fl__top{display:flex;align-items:center;gap:.24in;position:relative}
.fl__logo{width:1.35in;height:auto;flex:none}
.fl__name{font-family:var(--display);font-size:29pt;color:#fff;line-height:.94;letter-spacing:-.035em}
.fl__tag{color:var(--accent);font:700 8pt/1 var(--display);letter-spacing:.16em;
  text-transform:uppercase;margin-top:.07in}
.fl__h1{font-size:34pt;color:#fff;margin-top:.3in;line-height:.98;position:relative;max-width:6.4in}
.fl__lead{color:#B9CDDF;font-size:11pt;line-height:1.5;margin-top:.14in;max-width:5.5in;position:relative}
.fl__body{padding:.45in .7in .38in;flex:1;min-height:0;display:flex;flex-direction:column}
.fl__grid{display:grid;grid-template-columns:1fr 1fr;gap:.23in .4in;margin-bottom:.32in}
.fl__grid li{display:flex;gap:.16in;align-items:flex-start}
.fl__grid .ic{font-size:19pt;color:var(--brand);margin-top:1pt}
.fl__grid b{display:block;font:700 12pt/1.15 var(--display);color:var(--ink)}
.fl__grid span{display:block;font-size:9pt;color:var(--body);margin-top:2pt;line-height:1.4}
.fl__why{background:#F3F7FC;border:1px solid var(--line);border-radius:.09in;
  padding:.22in .28in;margin-bottom:.28in}
.fl__why h3{font-size:13pt;margin-bottom:.14in}
.fl__why ul{display:grid;grid-template-columns:1fr 1fr;gap:.1in .3in}
.fl__why li{display:flex;gap:.1in;align-items:center;font-size:9.5pt;color:var(--ink)}
.fl__why .ic{font-size:12pt;color:var(--brand)}
.fl__cta{margin-top:auto;background:var(--navy);border-radius:.09in;padding:.28in .32in;
  display:flex;align-items:center;justify-content:space-between;gap:.3in;color:#fff}
.fl__cta small{display:block;font:700 8pt/1 var(--display);letter-spacing:.16em;
  text-transform:uppercase;color:var(--accent)}
.fl__cta b{display:block;font:800 30pt/1 var(--display);letter-spacing:-.03em;margin-top:.06in}
.fl__cta p{font-size:8.6pt;color:#AFC4D8;margin-top:.08in}
.fl__cta .side{text-align:right;font-size:8.4pt;color:#AFC4D8;line-height:1.6;flex:none;white-space:nowrap}
.fl__foot{padding:.16in .7in .2in;font-size:7.6pt;color:var(--body);
  display:flex;justify-content:space-between;gap:.2in;border-top:1px solid var(--line)}
"""
    grid = "".join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (ic(k), n, d)
                   for k, n, d in SERVICES_SHORT)
    why = "".join("<li>%s<span>%s</span></li>" % (ic("check"), p) for p in PROMISES)
    body = f"""
<section class="sheet sheet--fl">
  <div class="guide"></div>
  <div class="fl">
    <header class="fl__hero">
      <div class="fl__top">
        <img class="fl__logo" src="../assets/img/logo-print.png" alt="Miguel's A/C">
        <div>
          <div class="fl__name">MIGUEL'S A/C</div>
          <div class="fl__tag">Trusted Locally &middot; Inland Empire &amp; LA</div>
        </div>
      </div>
      <h1 class="fl__h1">Your house is hot.<br>We fix that today.</h1>
      <p class="fl__lead">Same-day air conditioning repair across the Inland Empire and
      Los Angeles County. A person answers the phone, a stocked truck shows up, and you
      get the price before any work starts.</p>
    </header>

    <div class="fl__body">
      <ul class="fl__grid">{grid}</ul>

      <div class="fl__why">
        <h3>Why neighbors call us back</h3>
        <ul>{why}</ul>
      </div>

      <div class="fl__cta">
        <div>
          <small>Call or text</small>
          <b>{PHONE}</b>
          <p>{B['hours_weekday']} &middot; {B['hours_emergency']}</p>
        </div>
        <div class="side">{EMAIL}<br>{SITE}</div>
      </div>
    </div>

    <footer class="fl__foot">
      <span>{LICENCE}</span>
      <span>Inland Empire &amp; Los Angeles County &middot; No travel surcharge</span>
    </footer>
  </div>
</section>
"""
    note = ("One Letter page, trim <b>8.5 &times; 11 in</b> with 0.125 in bleed. "
            "Prints fine on a home printer too &mdash; just choose <b>Fit to page</b> "
            "instead of 100% if your printer cannot do full bleed. " + PRINT_NOTE
            + licence_warning())
    return shell("Flyer (8.5 x 11)", css, body, "size:8.75in 11.25in;margin:0", note)


# ---------------------------------------------------------------------------
# Instagram — 1080x1350 posts, 1080x1920 stories
# ---------------------------------------------------------------------------
def instagram():
    css = """
body{background:#111826}
.sheet{--bleed:0}
.sheet--post{width:1080px;height:1350px}
.sheet--story{width:1080px;height:1920px}
.ig{position:absolute;inset:0;display:flex;flex-direction:column;
  background:linear-gradient(163deg,#0D2E58,#071C38);color:#fff;overflow:hidden}
.ig::after{content:'';position:absolute;width:900px;height:900px;right:-280px;top:-330px;
  border-radius:50%;background:radial-gradient(circle,rgba(84,168,228,.26),transparent 68%)}
.ig__in{position:relative;padding:78px 84px;display:flex;flex-direction:column;height:100%}
.sheet--story .ig__in{padding:190px 84px 150px}
.ig__logo{width:178px;height:auto}
.ig__eyebrow{color:var(--accent);font:700 24px/1 var(--display);letter-spacing:.2em;
  text-transform:uppercase;margin-top:44px}
.ig__h1{font-family:var(--display);font-size:92px;line-height:.96;color:#fff;
  letter-spacing:-.035em;margin-top:22px}
.sheet--story .ig__h1{font-size:118px}
.ig__p{color:#B9CDDF;font-size:29px;line-height:1.42;margin-top:26px;max-width:820px}
.ig__list{margin-top:38px;display:grid;gap:19px}
.ig__list li{display:flex;gap:20px;align-items:center;font-size:31px;color:#DCE8F3}
.ig__list .ic{font-size:38px;color:var(--accent)}
.ig__cta{margin-top:auto;background:var(--accent);color:var(--navy);border-radius:20px;
  padding:34px 42px;display:flex;align-items:center;justify-content:space-between;gap:28px}
.ig__cta small{display:block;font:700 22px/1 var(--display);letter-spacing:.18em;
  text-transform:uppercase;opacity:.72}
.ig__cta b{display:block;font:800 66px/1 var(--display);letter-spacing:-.03em;margin-top:10px}
.ig__cta .ic{font-size:64px}
.ig__foot{margin-top:28px;color:#7E97AE;font-size:22px;display:flex;justify-content:space-between;gap:20px}
.cap{max-width:1080px;margin:0 auto 30px;background:#fff;border-radius:10px;padding:18px 22px;
  font-size:13.5px;line-height:1.65;color:#0A2240}
.cap b{font-family:var(--display)}
.cap textarea{width:100%;margin-top:8px;border:1px solid #DFE7F0;border-radius:6px;
  padding:10px;font:13px/1.6 var(--text);resize:vertical;min-height:112px}
"""
    svc = "".join("<li>%s<span>%s</span></li>" % (ic(k), n) for k, n, _ in SERVICES_SHORT[:4])
    promises = "".join("<li>%s<span>%s</span></li>" % (ic("check"), p) for p in PROMISES[:3])

    def panel(kind, eyebrow, h1, p, items):
        return f"""
<section class="sheet sheet--{kind}">
  <div class="ig"><div class="ig__in">
    <img class="ig__logo" src="../assets/img/logo-print.png" alt="Miguel's A/C">
    <div class="ig__eyebrow">{eyebrow}</div>
    <h1 class="ig__h1">{h1}</h1>
    <p class="ig__p">{p}</p>
    <ul class="ig__list">{items}</ul>
    <div class="ig__cta">
      <div><small>Call or text</small><b>{PHONE}</b></div>
      {ic('phone')}
    </div>
    <div class="ig__foot"><span>Inland Empire &amp; LA County</span><span>{LICENCE}</span></div>
  </div></div>
</section>"""

    caption = (
        "Hot house? We do same-day AC repair across the Inland Empire and LA County.\n\n"
        "A person answers the phone, a stocked truck shows up, and you get a flat-rate "
        "price before any work starts. No overtime charges, no weekend surcharge, no "
        "surprise invoice.\n\n"
        "Repair · New systems · Maintenance · Heating · Ductwork · Air quality\n\n"
        "Call or text " + PHONE + "\n\n"
        "#hvac #airconditioning #inlandempire #ranchocucamonga #ontarioca #fontana "
        "#riversideca #sanbernardino #losangeles #acrepair #hvaclife #smallbusiness"
    )

    body = f"""
<div class="cap">
  <b>Caption &mdash; copy this with the post</b>
  <textarea readonly>{caption}</textarea>
</div>
""" + panel("post", "Same-day service",
            "Your house<br>is hot.<br>We fix that<br>today.",
            "Same-day AC repair across the Inland Empire and Los Angeles County.",
            promises) + panel(
    "post", "What we do",
    "Repair,<br>install,<br>maintain.",
    "Homes, ADUs and small commercial. One crew, flat-rate pricing, no overtime charges.",
    svc) + panel(
    "story", "Same-day service",
    "Broken A/C?<br>Call us<br>today.",
    "Inland Empire &amp; Los Angeles County. A person answers the phone.",
    promises)

    note = ("Three canvases: two <b>1080 &times; 1350</b> feed posts and one "
            "<b>1080 &times; 1920</b> story. These are screen artwork, not print &mdash; "
            "screenshot each canvas at 100% zoom, or right-click &rarr; "
            "<i>Capture node screenshot</i> in DevTools for an exact-pixel export. "
            "The caption above is ready to paste." + licence_warning())
    return shell("Instagram set", css, body, "size:1080px 1350px;margin:0", note)


def main():
    os.makedirs(OUT, exist_ok=True)
    pieces = {
        "door-hanger.html": door_hanger(),
        "business-card.html": business_card(),
        "flyer.html": flyer(),
        "instagram.html": instagram(),
    }
    for name, html in pieces.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(html)
        print("  print/%-22s %6.1f KB" % (name, len(html.encode()) / 1024))
    print("\nphone %s   email %s" % (PHONE, EMAIL))
    if not LICENCE_IS_REAL:
        print("\n!! Licence is still a placeholder — it renders as a blank line.")
        print("   Fill BUSINESS['license'] in data.py before sending to a printer.")


if __name__ == "__main__":
    main()
