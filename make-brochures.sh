#!/usr/bin/env bash
# Regenerate the model brochure PDFs from the HTML in brochures/.
# Run `python3 build.py` first, and have the site served locally (port 8000).
#   python3 -m http.server 8000 &
#   ./make-brochures.sh
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT="${1:-8000}"
mkdir -p brochures/pdf
for m in tiggo-4 tiggo-4-hev tiggo-7-pro tiggo-8 tiggo-9; do
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="brochures/pdf/$m.pdf" \
    "http://localhost:$PORT/brochures/$m.html"
  echo "wrote brochures/pdf/$m.pdf"
done
