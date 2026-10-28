#!/bin/bash
# Gera DOCX + PDF (2 passadas p/ sumário). Uso: bash build.sh
set -e
cd "$(dirname "$0")"
export NODE_PATH=$HOME/tcc-npm/node_modules
OUT=$HOME/tcc-build-out; mkdir -p "$OUT"
python3 prepare.py
echo '{}' > pages.json
N="Projeto de Pesquisa - Paulo Ricardo"
for i in 1 2 3; do
  node build_docx.js pages.json "$OUT/$N.docx"
  (cd "$OUT" && /snap/bin/libreoffice --headless --convert-to pdf "$N.docx" >/dev/null 2>&1)
  cp "$OUT/$N.pdf" proj.pdf
  cp pages.json pages.prev
  python3 pages.py proj.pdf >/dev/null
  cmp -s pages.json pages.prev && break
done
node build_docx.js pages.json "$OUT/$N.docx"
(cd "$OUT" && /snap/bin/libreoffice --headless --convert-to pdf "$N.docx" >/dev/null 2>&1)
ls -la "$OUT"
