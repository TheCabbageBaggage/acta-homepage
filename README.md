# acta-homepage — actasystems.eu

Statische Firmenseite von acta.systems: KI für technische Dokumente in Industrie-KMU.
Kein JavaScript, keine Cookies, keine externen Abrufe. Gemeinsames acta-CI mit acta.lab
(Petrol `#285d66`, Tinte `#071012`, Papier `#f7f6f2`, Inter und JetBrains Mono selbst gehostet).
„systems“ hat immer eine andere Farbe als „acta“: auf hellem Grund Petrol, auf dunklem `#8fb4ba`.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `src/pages/*.html` | Inhalt jeder Seite (nur `<main>`). **Texte hier ändern.** |
| `src/pages-en/*.html` | englische Fassung, gleiche Dateinamen; Ausgabe unter `en/` mit englischen Dateinamen |
| `src/layout-en.html`, `src/partials-en/` | englischer Rahmen und englische Grafiken |
| `src/layout.html` | Kopf, Navigation und Fuß für alle Seiten |
| `src/partials/*.svg` | Grafiken der Beispiele, eingebunden mit `{{PART:name}}` |
| `src/build.py` | baut die Seiten; enthält die Seitenliste mit Titel und Beschreibung |
| `assets/site.css` | Gestaltung |
| `assets/brand/`, `assets/fonts/` | Logo, Favicon, OG-Bild, Schriften (OFL) |
| `*.html` im Wurzelverzeichnis, `en/*.html` | **generiert**, nicht direkt bearbeiten |

```bash
python3 src/build.py          # nach jeder Änderung an src/
```

Seiten: Start, Leistungen, Beispiele (Prüfberichte, Zeichnungen, Fristen), Vorgehen,
Über uns, FAQ, Kontakt, Impressum, Datenschutz. Impressum und Datenschutz sind Entwürfe
mit markierten Platzhaltern und müssen vor der Veröffentlichung ergänzt werden.

## Englische Fassung

Seiten unter `/en/` (services, examples, process, about, faq, contact, imprint, privacy …).
Jede Seite hat einen Sprachumschalter DE/EN und `hreflang`-Verweise. Links in `src/pages-en/`
behalten die deutschen Dateinamen, `build.py` schreibt sie auf die englischen um (`EN_NAMES`).
Titel und Beschreibungen der englischen Seiten stehen in `EN_META`.

## Webshop

Bestell-Links zeigen auf `https://shop.actasystems.eu` (Konstante `SHOP` in `src/build.py`).
Verwendete Routen laut Shop-Projektplan: `/pakete`, `/pakete/<slug>`, `/agb`, `/avv`, `/datenschutz`.

## Deploy

```bash
docker compose up -d --build
```
