#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# generate-qrcode.sh — Génère un QR code aux couleurs Data Lille
# Usage : ./generate-qrcode.sh <URL> [fichier_sortie.png]
# ------------------------------------------------------------------

API="https://api.qrcode-monkey.com"
LOGO_PATH="$(dirname "$0")/logo-qrcode.png"

if [[ $# -lt 1 ]]; then
  echo "Usage : $0 <URL> [fichier_sortie.png]"
  exit 1
fi

URL="$1"
OUTPUT="${2:-qrcode.png}"

# --- Étape 1 : Upload du logo -------------------------------------------
echo "⬆ Upload du logo..."
UPLOAD_RESPONSE=$(curl -s -X POST "${API}/qr/uploadImage" \
  -F "file=@${LOGO_PATH}")

LOGO_FILE=$(echo "$UPLOAD_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['file'])" 2>/dev/null)

if [[ -z "$LOGO_FILE" ]]; then
  echo "Erreur lors de l'upload du logo : ${UPLOAD_RESPONSE}"
  exit 1
fi
echo "  Logo uploadé : ${LOGO_FILE}"

# --- Étape 2 : Génération du QR code ------------------------------------
echo "⬇ Génération du QR code pour : ${URL}"

JSON_PAYLOAD=$(cat <<ENDJSON
{
  "data": "${URL}",
  "config": {
    "body": "circle",
    "eye": "frame1",
    "eyeBall": "ball14",
    "erf1": ["fh"],
    "erf2": [],
    "erf3": ["fh", "fv"],
    "brf1": ["fh"],
    "brf2": [],
    "brf3": ["fh", "fv"],
    "bodyColor": "#E9006E",
    "bgColor": "#FFFFFF",
    "eye1Color": "#E9006E",
    "eye2Color": "#E9006E",
    "eye3Color": "#261F1B",
    "eyeBall1Color": "#E9006E",
    "eyeBall2Color": "#E9006E",
    "eyeBall3Color": "#261F1B",
    "gradientColor1": "#E9006E",
    "gradientColor2": "#261F1B",
    "gradientType": "linear",
    "gradientOnEyes": false,
    "logo": "${LOGO_FILE}",
    "logoMode": "clean"
  },
  "size": 1000,
  "download": false,
  "file": "png"
}
ENDJSON
)

HTTP_CODE=$(curl -s -o "${OUTPUT}" -w "%{http_code}" -X POST "${API}/qr/custom" \
  -H "Content-Type: application/json" \
  -d "${JSON_PAYLOAD}")

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "Erreur API (HTTP ${HTTP_CODE})"
  cat "${OUTPUT}"
  rm -f "${OUTPUT}"
  exit 1
fi

FILE_SIZE=$(wc -c < "${OUTPUT}" | tr -d ' ')
echo "QR code généré : ${OUTPUT} (${FILE_SIZE} octets)"
