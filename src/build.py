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
     "acta.systems wertet Prüfberichte, Zeichnungen und technische Unterlagen mit KI aus. Festpreis-Pakete vom Check bis zum Betrieb, gehostet in der EU, jede Antwort mit Quelle.", ""),
    ("leistungen", "Leistungen und Preise – acta.systems",
     "Sieben Pakete mit festem Umfang, fester Lieferzeit und Festpreis: Dokumenten-Check, Sicherheitscheck, Pipeline- und Wissensassistent-Pilot, Betrieb.", "leistungen"),
    ("beispiele", "Beispiele – acta.systems",
     "Drei Beispiele aus der Praxis: Prüfberichte auswerten, Schriftfelder aus technischen Zeichnungen lesen, Fristen aus Dokumenten erkennen und erinnern.", "beispiele"),
    ("beispiel-pruefberichte", "Beispiel: Prüfberichte automatisch auswerten – acta.systems",
     "Wie aus gescannten Prüfberichten ein Datensatz mit Quellenangabe für das ERP wird, und was dabei nicht automatisch passiert.", "beispiele"),
    ("beispiel-zeichnungen", "Beispiel: Daten aus technischen Zeichnungen – acta.systems",
     "Schriftfeld, Werkstoff, Revision und Toleranzangaben aus technischen Zeichnungen lesen und Revisionsstände vergleichen.", "beispiele"),
    ("beispiel-fristen", "Beispiel: Fristen erkennen und erinnern – acta.systems",
     "Prüf-, Kalibrier- und Kündigungsfristen aus Bescheinigungen und Verträgen lesen und rechtzeitig daran erinnern.", "beispiele"),
    ("vorgehen", "Vorgehen – acta.systems",
     "Vom Erstgespräch über Check und Pilot bis zum Betrieb: Ablauf, Abnahme, Datenschutz und Sicherheit.", "vorgehen"),
    ("ueber-uns", "Über uns – acta.systems",
     "Wer hinter acta.systems steht und wie wir arbeiten.", "ueber-uns"),
    ("faq", "Häufige Fragen – acta.systems",
     "Antworten zu Daten, Ablauf, Preisen, Abnahme und Technik.", "faq"),
    ("kontakt", "Kontakt – acta.systems",
     "Erstgespräch vereinbaren oder eine Frage stellen.", "kontakt"),
    ("impressum", "Impressum – acta.systems", "Impressum und Offenlegung.", ""),
    ("datenschutz", "Datenschutz – acta.systems", "Datenschutzinformation für diese Website.", ""),
]

NAV = [("leistungen", "Leistungen"), ("beispiele", "Beispiele"), ("vorgehen", "Vorgehen"),
       ("ueber-uns", "Über uns"), ("faq", "FAQ"), ("kontakt", "Kontakt")]


def nav_html(active):
    links = "".join(
        f'<a href="{k}.html"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for k, t in NAV)
    return links


def brand_words(html):
    head, body = html.split("<body>", 1)
    def wrap(seg):
        return re.sub(r"acta\.systems\b", '<span class="bw">acta.<span class="bw-s">systems</span></span>', seg)
    body = re.sub(r">([^<]+)<", lambda m: ">" + wrap(m.group(1)) + "<", body)
    return head + "<body>" + body


def build():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    logo = (SRC / "logo.svg").read_text(encoding="utf-8")
    for name, title, desc, active in PAGES:
        body = (SRC / "pages" / f"{name}.html").read_text(encoding="utf-8")
        body = re.sub(r"\{\{PART:([\w-]+)\}\}", lambda m: (SRC / "partials" / f"{m.group(1)}.svg").read_text(encoding="utf-8"), body)
        url = BASE + ("/" if name == "index" else f"/{name}.html")
        html = (layout.replace("{{TITLE}}", title).replace("{{DESC}}", desc).replace("{{URL}}", url)
                .replace("{{NAV}}", nav_html(active)).replace("{{BODY}}", body))
        html = brand_words(html)
        html = html.replace("{{LOGO}}", logo).replace("{{SHOP}}", SHOP)
        assert "{{" not in html, f"offener Platzhalter in {name}"
        (ROOT / f"{name}.html").write_text(html, encoding="utf-8")
        print(f"{name}.html  {len(html)//1024} KB")


if __name__ == "__main__":
    build()
