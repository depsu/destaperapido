#!/usr/bin/env bash
# Lee total y rating de google-reviews.json y actualiza
# el reviewCount en el schema JSON-LD de todas las páginas HTML.
# Uso: bash scripts/sync-reviews.sh

set -euo pipefail

JSON="public/data/google-reviews.json"

if [ ! -f "$JSON" ]; then
  echo "Error: no existe $JSON"
  exit 1
fi

TOTAL=$(python3 -c "import json; print(json.load(open('$JSON'))['total'])")
RATING=$(python3 -c "import json; print(json.load(open('$JSON'))['rating'])")

echo "Sincronizando: rating=$RATING, reviewCount=$TOTAL"

COUNT=0
while IFS= read -r -d '' file; do
  if grep -q '"reviewCount"' "$file"; then
    sed -i '' -E "s/\"reviewCount\": *\"[0-9]+\"/\"reviewCount\": \"$TOTAL\"/" "$file"
    sed -i '' -E "s/\"ratingValue\": *\"[0-9.]+\"/\"ratingValue\": \"$RATING\"/" "$file"
    COUNT=$((COUNT + 1))
  fi
done < <(find public -name '*.html' -print0)

# Actualizar también textos hardcodeados tipo "Google · 16 reseñas reales"
while IFS= read -r -d '' file; do
  sed -i '' -E "s/Google · [0-9]+ reseñas reales/Google · $TOTAL reseñas reales/" "$file"
done < <(find public -name '*.html' -print0)

echo "Actualizado reviewCount a $TOTAL en $COUNT archivos."
