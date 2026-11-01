# acta-homepage — actasystems.eu

Statische Firmenseite von acta.systems: KI für technische Dokumente in Industrie-KMU.
Gemeinsames acta-CI mit acta.lab (Petrol `#285d66`, Tinte `#071012`, Papier `#f7f6f2`,
Inter und JetBrains Mono, selbst gehostet). „systems“ hat immer eine andere Farbe als
„acta“: auf hellem Grund Petrol, auf dunklem `#8fb4ba` (Klasse `.on-dark`).

| Pfad | Inhalt |
|---|---|
| `index.html` | die Seite, CSS inline, kein JavaScript |
| `assets/brand/` | Logo (hell, dunkel), Icon, Favicon, OG-Bild |
| `assets/fonts/` | Inter, JetBrains Mono (OFL) |
| `Dockerfile`, `docker-compose.yml` | Auslieferung auf Port 8080 |

## Webshop

Alle Paket-, Kontakt- und Rechtslinks zeigen auf den Webshop
(`https://shop.actasystems.eu`, Routen laut `projectplan_actalab_shop.md`:
`/pakete`, `/pakete/<slug>`, `/kontakt`, `/impressum`, `/datenschutz`, `/agb`, `/avv`).
Andere Shop-Adresse:

```bash
sed -i 's#https://shop.actasystems.eu#https://NEUE-ADRESSE#g' index.html
```

## Deploy

```bash
docker compose up -d --build
```

Preise und Paketumfänge entsprechen dem Angebotsportfolio (Stand November 2026).
Bei Preisänderungen `index.html` und den Shop-Katalog gemeinsam anpassen.
