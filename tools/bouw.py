#!/usr/bin/env python3
"""Bouwt de losse pagina's van leemsmid.nl uit de lijst WORKS in index.html.

Maakt: werk/<slug>/index.html, leemstuc/index.html, sitemap.xml en de tekstversie
van het portfolio in index.html (voor zoekmachines). Draai na elke wijziging in WORKS:
    python3 tools/bouw.py
Heeft node nodig om de lijst WORKS te lezen.
"""
import json, os, re, subprocess, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://leemsmid.nl"
TODAY = datetime.date.today().isoformat()
esc = lambda t: html.escape(str(t), quote=True)

INDEX = os.path.join(ROOT, "index.html")
src = open(INDEX, encoding="utf-8").read()
a = src.index("var WORKS=") + len("var WORKS=")
b = src.index("];", a) + 1
WORKS = json.loads(subprocess.check_output(["node", "-e", "process.stdout.write(JSON.stringify(eval(require('fs').readFileSync(0,'utf8'))))"], input=src[a:b].encode()))

ONDERWERP = {
    "graniet": "Antraciet leemstuc in een keuken in Assen",
    "kleur": "Glanspleister met lapis lazuli, goud, amethist en jade in Zutphen",
    "roest": "Roestkleurige leemstuc met ijzeroxide in Amersfoort",
    "ruw": "Leemstuc zonder pigment in Brummen",
}

def pad(n): return "%02d" % n
def plek(w): return w["plaats"] + (", " + w["ruimte"].lower() if w.get("ruimte") else "")
def pigm(w): return ", ".join(w["pigment"]) if w["pigment"] else "Zonder pigment"

CSS = """
@font-face{font-family:"Bodoni Moda";font-weight:400;font-display:swap;src:url(/fonts/bodoni-moda-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Bodoni Moda";font-style:italic;font-weight:400;font-display:swap;src:url(/fonts/bodoni-moda-latin-400-italic.woff2) format("woff2")}
@font-face{font-family:"Spline Sans Mono";font-weight:300;font-display:swap;src:url(/fonts/spline-sans-mono-latin-300-normal.woff2) format("woff2")}
@font-face{font-family:"Spline Sans Mono";font-weight:400;font-display:swap;src:url(/fonts/spline-sans-mono-latin-400-normal.woff2) format("woff2")}
:root{color-scheme:dark;--ground:#0C0B0A;--ink:#E6E0D6;--ink-soft:#A39B90;--ink-faint:#5E5850;--rule:#26221E;--earth:#B8865A;
--serif:"Bodoni Moda","Didot","Bodoni 72",Georgia,serif;--mono:"Spline Sans Mono",ui-monospace,Menlo,Consolas,monospace;--gutter:clamp(16px,4vw,56px)}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--serif);font-size:18px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}
img,video{max-width:100%;display:block}
.label{font-family:var(--mono);font-weight:300;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft)}
.bar{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:calc(18px + env(safe-area-inset-top,0px)) var(--gutter) 18px}
.mark{font-size:15px;letter-spacing:.34em;text-transform:uppercase;text-decoration:none;padding:.55em .36em .5em .7em;border:1.5px solid transparent;border-image:linear-gradient(135deg,#E9CF8E 0%,#A97C3A 35%,#F1DCA2 55%,#9A7134 80%,#D9B76E 100%) 1}
.bar nav{display:flex;gap:clamp(12px,3vw,36px)}
.bar nav a{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft);text-decoration:none}
.bar nav a:hover,.bar nav a[aria-current]{color:var(--ink)}
main{padding:8svh var(--gutter) 12svh;max-width:1180px}
h1{margin:10px 0 0;font-weight:400;font-style:italic;font-size:clamp(44px,7vw,96px);line-height:1;text-wrap:balance}
h2{margin:0 0 14px;font-weight:400;font-size:clamp(26px,3vw,36px);line-height:1.15;text-wrap:balance}
.lede{margin:28px 0 0;max-width:40ch;font-size:clamp(21px,2.1vw,27px);line-height:1.45;text-wrap:pretty}
.prose p{max-width:62ch;margin:0 0 1em;color:var(--ink-soft)}
.prose section{border-top:1px solid var(--rule);padding:34px 0 18px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:12px 48px}
.prose ol{margin:0;padding:0;list-style:none;counter-reset:s;max-width:62ch}
.prose li{counter-increment:s;display:grid;grid-template-columns:42px 1fr;color:var(--ink-soft);margin-bottom:1em}
.prose li::before{content:counter(s,decimal-leading-zero);font-family:var(--mono);font-size:12px;color:var(--earth);padding-top:5px}
.facts{margin:36px 0 0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px 24px;border-top:1px solid var(--rule);padding-top:20px;max-width:900px}
.facts div{display:flex;flex-direction:column;gap:6px;min-width:0}
.facts dt{font-family:var(--mono);font-weight:300;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-faint)}
.facts dd{margin:0;font-size:16px}
.photos{margin-top:8svh;display:grid;gap:clamp(16px,3vw,40px);justify-items:center}
.photos img,.photos video{max-height:86svh;width:auto;height:auto}
.ask{margin-top:10svh;border-top:1px solid var(--rule);padding-top:26px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px 56px}
.ask p{margin:0;max-width:44ch;color:var(--ink-soft)}
.line{display:flex;justify-content:space-between;gap:16px;align-items:baseline;border-bottom:1px solid var(--rule);padding:10px 0}
.line span:last-child{font-size:20px;user-select:all;overflow-wrap:anywhere;text-align:right}
.others{margin-top:8svh;border-top:1px solid var(--rule);padding-top:22px;display:flex;flex-wrap:wrap;gap:12px 36px;align-items:baseline}
.others a{font-style:italic;font-size:22px;text-decoration:none}
.others a:hover{color:#fff}
.back{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-soft);text-decoration:none}
footer{display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;padding:28px var(--gutter) calc(28px + env(safe-area-inset-bottom,0px));border-top:1px solid var(--rule)}
footer a,footer span{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-faint);text-decoration:none}
footer div{display:flex;gap:24px;flex-wrap:wrap}
@media (max-width:820px){.facts{grid-template-columns:repeat(2,minmax(0,1fr))}.ask,.prose section{grid-template-columns:minmax(0,1fr)}}
@media (max-width:520px){.bar{flex-wrap:wrap;row-gap:14px}.bar nav{width:100%;justify-content:space-between}}
@media (max-width:620px){body{font-size:17px}.mark{letter-spacing:.22em;font-size:14px;padding:.5em .3em .45em .52em}.bar nav{gap:12px}.bar nav a{letter-spacing:.08em;font-size:10.5px}.photos img,.photos video{max-height:none;width:100%}}
"""

def page(path, title, desc, body, ld, img=SITE + "/img/og-ls.jpg", current=None):
    url = SITE + path
    nav = [("/#portfolio", "Portfolio"), ("/#maker", "Tom"), ("/leemstuc/", "Leemstuc"), ("/#aanvraag", "Aanvraag")]
    navh = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if t == current else "", t) for h, t in nav)
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Tom Smit">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0C0B0A">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Leemsmid">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{img}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="nl_NL">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<link rel="preload" href="/fonts/bodoni-moda-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
</head>
<body>
<header class="bar"><a class="mark" href="/">Leemsmid</a><nav aria-label="Hoofdnavigatie">{navh}</nav></header>
<main>
{body}
</main>
<footer><span>Leemsmid, Zutphen</span><div><a href="https://www.instagram.com/leemsmid" rel="noopener">Instagram</a><a href="/leemstuc/">Over leemstuc</a><a href="/#architecten">Voor architecten</a></div></footer>
</body>
</html>
"""

CONTACT = """<div class="line"><span class="label">E-mail</span><span>info@leemsmid.nl</span></div>
    <div class="line"><span class="label">Telefoon</span><span>06 5194 7969</span></div>"""

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}

sitemap = [("/", [SITE + "/" + s["src"] for w in WORKS for s in w["shots"]] + [SITE + "/img/tom-smit-leemsmid-pigment-mengen.jpg"])]

# ---------- werkpagina's ----------
for w in WORKS:
    slug = w["slug"]; path = f"/werk/{slug}/"
    title = f"{w['title']}: {ONDERWERP[slug]} | Leemsmid"
    desc = w.get("verhaal", "")
    facts = [("Plek", plek(w)), ("Jaar", w["jaar"]), ("Pigment", pigm(w)), ("Klei", w["klei"] + (", " + w["herkomst"] if w.get("herkomst") else ""))]
    fh = "".join(f"<div><dt>{a}</dt><dd>{esc(b)}</dd></div>" for a, b in facts)
    ph = []
    for s in w["shots"]:
        if s.get("video"):
            ph.append(f'<video src="/{s["video"]}" poster="/{s["src"]}" muted loop playsinline autoplay preload="metadata" width="{s["w"]}" height="{s["h"]}" aria-label="{esc(s["alt"])}"></video>')
        else:
            ph.append(f'<img src="/{s["src"]}" alt="{esc(s["alt"])}" width="{s["w"]}" height="{s["h"]}" loading="lazy">')
    ph[0] = ph[0].replace(' loading="lazy"', ' fetchpriority="high"')
    others = " ".join(f'<a href="/werk/{o["slug"]}/">{esc(o["title"])}</a>' for o in WORKS if o is not w)
    body = f"""<a class="back" href="/#portfolio">Portfolio 2026</a>
  <div class="label" style="margin-top:28px">Nr. {pad(w['nr'])}</div>
  <h1>{esc(w['title'])}</h1>
  <p class="lede">{esc(w.get('verhaal',''))}</p>
  <dl class="facts">{fh}</dl>
  <div class="photos">
    {chr(10).join(ph)}
  </div>
  <section class="ask">
    <div><div class="label" style="margin-bottom:14px">Aanvraag</div><p>Ook zo'n wand, voor een andere ruimte? Stuur een foto van de wand, waar hij staat en welke periode de voorkeur heeft. Ik neem dan contact op.</p></div>
    <div>{CONTACT}</div>
  </section>
  <nav class="others" aria-label="Andere werken"><span class="label">Meer werk</span> {others}</nav>"""
    imgs = [SITE + "/" + s["src"] for s in w["shots"]]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CreativeWork", "name": w["title"], "headline": ONDERWERP[slug], "description": desc, "url": SITE + path,
         "image": imgs, "dateCreated": str(w["jaar"]), "material": ["leem", w["klei"]] + w["pigment"],
         "locationCreated": {"@type": "Place", "name": w["plaats"]},
         "creator": {"@type": "Person", "name": "Tom Smit", "url": SITE + "/"},
         "publisher": {"@id": SITE + "/#leemsmid"}},
        crumbs([("Leemsmid", "/"), ("Portfolio 2026", "/#portfolio"), (w["title"], path)])]}
    os.makedirs(os.path.join(ROOT, "werk", slug), exist_ok=True)
    open(os.path.join(ROOT, "werk", slug, "index.html"), "w", encoding="utf-8").write(
        page(path, title, desc, body, ld, img=imgs[0]))
    sitemap.append((path, imgs))

# ---------- pagina over leemstuc ----------
LEEM = open(os.path.join(ROOT, "tools", "leemstuc.html"), encoding="utf-8").read()
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "WebPage", "name": "Leemstuc en glanspleister", "url": SITE + "/leemstuc/",
     "about": ["leemstuc", "glanspleister", "leempleister", "binnenklimaat"], "author": {"@type": "Person", "name": "Tom Smit"},
     "publisher": {"@id": SITE + "/#leemsmid"}},
    crumbs([("Leemsmid", "/"), ("Leemstuc", "/leemstuc/")])]}
os.makedirs(os.path.join(ROOT, "leemstuc"), exist_ok=True)
open(os.path.join(ROOT, "leemstuc", "index.html"), "w", encoding="utf-8").write(page(
    "/leemstuc/", "Leemstuc en glanspleister: wat het is en wat het met een kamer doet | Leemsmid",
    "Leemstuc is een pleister van klei, zand, marmer en pigment. Wat het doet met vocht en warmte in huis, waar het kan, hoe je het onderhoudt en hoe een opdracht verloopt.",
    LEEM, ld, img=SITE + "/img/glanspleister-kleur-detail-goud-lapis-lazuli.jpg", current="Leemstuc"))
sitemap.append(("/leemstuc/", [SITE + "/img/glanspleister-kleur-detail-goud-lapis-lazuli.jpg"]))

# ---------- sitemap ----------
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for path, imgs in sitemap:
    xml.append(f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{TODAY}</lastmod>")
    for i in dict.fromkeys(imgs): xml.append(f"    <image:image><image:loc>{i}</image:loc></image:image>")
    xml.append("  </url>")
xml.append("</urlset>\n")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml))

# ---------- tekstversie portfolio in index.html ----------
cards = []
for w in WORKS:
    s0 = w["shots"][0]
    cards.append(f'<article class="work"><a class="plate" href="/werk/{w["slug"]}/" data-nr="{w["nr"]}"><img src="{s0["src"]}" alt="{esc(s0["alt"])}" width="{s0["w"]}" height="{s0["h"]}" loading="lazy"></a>'
                 f'<a class="cap" href="/werk/{w["slug"]}/" data-nr="{w["nr"]}"><span class="no">Nr. {pad(w["nr"])}</span><span class="t">{esc(w["title"])}</span>'
                 f'<span class="m">{esc(plek(w))} &middot; {esc(pigm(w))} &middot; {esc(w["klei"])}, {esc(w["herkomst"])} &middot; {w["jaar"]}</span></a></article>')
new = re.sub(r'(<div class="hang" id="hang">\n      ).*?(\n    </div>)', lambda m: m.group(1) + "\n      ".join(cards) + m.group(2), src, count=1, flags=re.S)
open(INDEX, "w", encoding="utf-8").write(new)
print("klaar:", [w["slug"] for w in WORKS])
