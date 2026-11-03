#!/usr/bin/env python3
"""Baut die statischen Seiten von actasystems.eu.

Inhalte:  src/pages/<name>.html  (nur der Inhalt von <main>)
Rahmen:   src/layout.html        (Kopf, Navigation, Fuß)
Stil:     assets/site.css

Aufruf:   python3 src/build.py      → schreibt <name>.html ins Repo-Wurzelverzeichnis

Platzhalter in Seiten: {{SHOP}} (Webshop-Adresse), {{LOGO}} (Logo als SVG),
{{PART:name}} (fügt src/partials/name.svg ein).
"acta.systems" im sichtbaren Text wird automatisch zweifarbig gesetzt.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SHOP = "https://shop.actasystems.eu"
BASE = "https://actasystems.eu"

# Datei, Seitentitel, Beschreibung, aktiver Menüpunkt
PAGES = [
    ("index", "acta.systems – KI für technische Dokumente in Industrie-KMU",
     "acta.systems vermietet KI-Arbeitskräfte für technische Dokumente: Prüfberichte, Zeichnungen, Fristen und Handbücher. Feste Monatsrate, Einrichtung und Betrieb in der EU inklusive, jeder Wert mit Quelle.", ""),
    ("leistungen", "Angebot und Preise – acta.systems",
     "Dokumenten-Check als Einstieg, dazu Dokumentenkraft und Wissenskraft zur festen Monatsrate mit Einrichtung, Betrieb und 3 Monaten Probezeit.", "leistungen"),
    ("beispiele", "Beispiele – acta.systems",
     "Drei Beispiele aus der Praxis: Prüfberichte auswerten, Schriftfelder aus technischen Zeichnungen lesen, Fristen aus Dokumenten erkennen und erinnern.", "beispiele"),
    ("beispiel-pruefberichte", "Beispiel: Prüfberichte automatisch auswerten – acta.systems",
     "Wie aus gescannten Prüfberichten ein Datensatz mit Quellenangabe für das ERP wird, und was dabei nicht automatisch passiert.", "beispiele"),
    ("beispiel-zeichnungen", "Beispiel: Daten aus technischen Zeichnungen – acta.systems",
     "Schriftfeld, Werkstoff, Revision und Toleranzangaben aus technischen Zeichnungen lesen und Revisionsstände vergleichen.", "beispiele"),
    ("beispiel-fristen", "Beispiel: Fristen erkennen und erinnern – acta.systems",
     "Prüf-, Kalibrier- und Kündigungsfristen aus Bescheinigungen und Verträgen lesen und rechtzeitig daran erinnern.", "beispiele"),
    ("vorgehen", "Vorgehen – acta.systems",
     "Vom Erstgespräch über Check, Einrichtung und Probezeit bis zum Betrieb: Ablauf, Abnahme, Datenschutz und Sicherheit.", "vorgehen"),
    ("ueber-uns", "Über uns – acta.systems",
     "Woher acta.systems kommt und wie wir arbeiten.", "ueber-uns"),
    ("faq", "Häufige Fragen – acta.systems",
     "Antworten zu Daten, Ablauf, Preisen, Abnahme und Technik.", "faq"),
    ("kontakt", "Kontakt – acta.systems",
     "Erstgespräch vereinbaren oder eine Frage stellen.", "kontakt"),
    ("impressum", "Impressum – acta.systems", "Impressum und Offenlegung.", ""),
    ("datenschutz", "Datenschutz – acta.systems", "Datenschutzinformation für diese Website.", ""),
]

NAV = [("leistungen", "Leistungen"), ("beispiele", "Beispiele"), ("vorgehen", "Vorgehen"),
       ("ueber-uns", "Über uns"), ("faq", "FAQ"), ("kontakt", "Kontakt")]

# ---------- Englisch (Ausgabe unter /en/) ----------
# Quell-Schlüssel (deutsch) → englischer Dateiname. Links in src/pages-en/ verwenden die deutschen
# Schlüssel wie in src/pages/; build.py schreibt sie für /en/ auf die englischen Namen um.
EN_NAMES = {"index": "index", "leistungen": "services", "beispiele": "examples",
            "beispiel-pruefberichte": "example-inspection-reports", "beispiel-zeichnungen": "example-drawings",
            "beispiel-fristen": "example-deadlines", "vorgehen": "process", "ueber-uns": "about",
            "faq": "faq", "kontakt": "contact", "impressum": "imprint", "datenschutz": "privacy"}
EN_META = {
    "index": ("acta.systems – AI for technical documents in industrial SMEs",
              "acta.systems rents out AI workers for technical documents: inspection reports, drawings, deadlines and manuals. One fixed monthly rate, setup and EU operation included, every value with its source."),
    "leistungen": ("Offer and prices – acta.systems",
                   "Document check as the entry point, then Document Worker and Knowledge Worker at a fixed monthly rate with setup, operation and a 3-month trial period."),
    "beispiele": ("Examples – acta.systems",
                  "Three examples: reading inspection reports, title blocks of technical drawings, and deadlines in certificates and contracts."),
    "beispiel-pruefberichte": ("Example: extracting inspection reports – acta.systems",
                               "How scanned inspection reports become a record with source references for your ERP, and what is not automated."),
    "beispiel-zeichnungen": ("Example: data from technical drawings – acta.systems",
                             "Reading title block, material, revision and tolerances from technical drawings and comparing revisions."),
    "beispiel-fristen": ("Example: finding deadlines and sending reminders – acta.systems",
                         "Reading inspection, calibration and notice periods from certificates and contracts and reminding the right person in time."),
    "vorgehen": ("Process – acta.systems", "From the first call through check, setup and trial period to operation: steps, acceptance, data protection and security."),
    "ueber-uns": ("About – acta.systems", "Where acta.systems comes from and how we work."),
    "faq": ("FAQ – acta.systems", "Answers on data, process, prices, acceptance and technology."),
    "kontakt": ("Contact – acta.systems", "Book an intro call or ask a question."),
    "impressum": ("Imprint – acta.systems", "Legal notice and disclosure."),
    "datenschutz": ("Privacy – acta.systems", "Privacy information for this website."),
}
NAV_EN = [("leistungen", "Services"), ("beispiele", "Examples"), ("vorgehen", "Process"),
          ("ueber-uns", "About"), ("faq", "FAQ"), ("kontakt", "Contact")]


def nav_html(active, nav=None, names=None):
    nav = nav or NAV
    names = names or {k: k for k, _ in NAV + [("index", "")]}
    return "".join(
        f'<a href="{names.get(k, k)}.html"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for k, t in nav)


def brand_words(html):
    head, body = html.split("<body>", 1)
    def wrap(seg):
        return re.sub(r"acta\.systems\b", '<span class="bw">acta.<span class="bw-s">systems</span></span>', seg)
    body = re.sub(r">([^<]+)<", lambda m: ">" + wrap(m.group(1)) + "<", body)
    return head + "<body>" + body


def page_url(lang, name):
    if lang == "de":
        return BASE + ("/" if name == "index" else f"/{name}.html")
    en = EN_NAMES[name]
    return BASE + ("/en/" if en == "index" else f"/en/{en}.html")


def render(lang, name, title, desc, active):
    en = lang == "en"
    layout = (SRC / ("layout-en.html" if en else "layout.html")).read_text(encoding="utf-8")
    logo = (SRC / "logo.svg").read_text(encoding="utf-8")
    body = (SRC / ("pages-en" if en else "pages") / f"{name}.html").read_text(encoding="utf-8")
    def part(m):
        f = SRC / "partials-en" / f"{m.group(1)}.svg"
        if not (en and f.exists()):
            f = SRC / "partials" / f"{m.group(1)}.svg"
        return f.read_text(encoding="utf-8")
    body = re.sub(r"\{\{PART:([\w-]+)\}\}", part, body)
    html = (layout.replace("{{TITLE}}", title).replace("{{DESC}}", desc).replace("{{URL}}", page_url(lang, name))
            .replace("{{URL_DE}}", page_url("de", name)).replace("{{URL_EN}}", page_url("en", name))
            .replace("{{NAV}}", nav_html(active, NAV_EN if en else NAV, EN_NAMES if en else None))
            .replace("{{BODY}}", body))
    # Sprachumschalter: relativer Link zur Gegenseite
    if en:
        alt = "../" + ("index.html" if name == "index" else f"{name}.html")
    else:
        alt = "en/" + EN_NAMES[name] + ".html"
    html = html.replace("{{LANGLINK}}", alt)
    html = brand_words(html)
    html = html.replace("{{LOGO}}", logo).replace("{{SHOP}}", SHOP)
    if en:
        # interne Links auf englische Dateinamen, Assets eine Ebene höher
        html = re.sub(r'href="([\w-]+)\.html(#[\w-]*)?"',
                      lambda m: f'href="{EN_NAMES.get(m.group(1), m.group(1))}.html{m.group(2) or ""}"', html)
        html = html.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
        html = html.replace('href="../../', 'href="../')
    assert "{{" not in html, f"offener Platzhalter in {lang}/{name}"
    out = ROOT / ("en" if en else "") / f"{EN_NAMES[name] if en else name}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"{lang}/{out.name}  {len(html)//1024} KB")


def build():
    for name, title, desc, active in PAGES:
        render("de", name, title, desc, active)
    if (SRC / "pages-en").exists():
        for name, _, _, active in PAGES:
            if (SRC / "pages-en" / f"{name}.html").exists():
                t, d = EN_META[name]
                render("en", name, t, d, active)


if __name__ == "__main__":
    build()
