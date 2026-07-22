# Chery Antigua — lead-capture website

A simple, fast, static site for **Chery Antigua** whose job is to (1) capture
leads and (2) present standard information about the Chery Tiggo line-up.

Design matched to the **official Chery regional template** (cherysxm.com / cheryinternational.com):

- Light `#f4f4f4` backgrounds with a subtle diagonal pattern
- **Deep Chery navy** `#0B457F` structure · **champagne-bronze** `#A4896C` CTAs
- Dark near-black performance bands with big italic stat numerals
- Big italic uppercase model wordmarks over full-bleed imagery
- Type: **Poppins** — the typeface Chery's sites use

## Editing

All content lives in `build.py` (`SITE`, `OFFER`, `MODELS`, `TECH`). After editing:

```bash
python3 build.py
```

This regenerates `index.html`, `contact.html`, `models/*.html` and `brochures/*.html`.
CSS/JS in `/assets` are hand-edited. Images live in `/images`.

## Preview locally

```bash
python3 -m http.server 5179
```

Then open http://localhost:5179.

## Brochure PDFs

With the local server running:

```bash
./make-brochures.sh 5179
```

Renders `brochures/pdf/<slug>.pdf` via headless Chrome.

## Leads

Quote modal, test-drive wizard and message form all flow through `deliverLead()` in
`assets/site.js`, which POSTs to the VMP `ingestWebLead` Supabase Edge Function with
`brand: "Chery"` and keeps a `localStorage` (`chery_leads`) backup.

The VMP `ingestWebLead` handler is brand-aware: the `chery.ag` origin is allowlisted
and its leads notify `sales@chery.ag` (deployed).

WhatsApp/Call: +1 (268) 464-3345.

## Images

Model photos are official Chery assets from the marketing Dropbox
(`Manufacturers/Chery/Images`, the factory `Model Data` presentations, and
`_Product Images and Videos/CHERY/Vehicle Images` for the 360 sets and
Tiggo 9 gallery). Logos from `.../Chery/Logo`. 360 spin frames live in
`images/360/<model>/<colour>/01..NN.jpg`.

## Deploying

Pure static files — host anywhere (Netlify/Vercel/Cloudflare Pages, GitHub Pages,
or upload the folder to the `chery.ag` web root).
