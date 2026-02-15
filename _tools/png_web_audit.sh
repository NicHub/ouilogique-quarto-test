#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'USAGE'
Usage: png-web-audit.sh <image.png>

Génère un mini rapport d'audit web pour un fichier PNG:
- taille disque
- dimensions
- modèle/couleurspace/profondeur/alpha
- nombre de couleurs uniques
- estimation RAM (RGB8/RGBA8)
- profil ICC
- chunks PNG
- infos additionnelles (résolution, interlace, compression)
USAGE
}

human_size() {
    awk -v b="$1" '
        function H(x) {
            s = "B KB MB GB TB"
            split(s, u)
            i = 1
            while (x >= 1024 && i < 5) {
                x /= 1024
                i++
            }
            return sprintf("%.2f %s", x, u[i])
        }
        BEGIN { print H(b) }
    '
}

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "Erreur: commande requise introuvable: $1" >&2
        exit 1
    }
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
    usage
    exit 0
fi

if [[ $# -ne 1 ]]; then
    usage >&2
    exit 1
fi

file="$1"

if [[ ! -f "$file" ]]; then
    echo "Erreur: fichier introuvable: $file" >&2
    exit 1
fi

if [[ "${file##*.}" != "png" && "${file##*.}" != "PNG" ]]; then
    echo "Avertissement: extension non .png (on continue quand même)." >&2
fi

require_cmd magick
require_cmd exiftool

read -r width height depth type colorspace alpha unique_colors <<< "$(
    magick identify -format '%w %h %z %[type] %[colorspace] %A %k' "$file"
)"

disk_bytes=$(stat -f%z "$file")
rgb_bytes=$((width * height * 3))
rgba_bytes=$((width * height * 4))

icc_profile=$(exiftool -s3 -icc_profile:ProfileDescription "$file" 2>/dev/null || true)
if [[ -z "$icc_profile" ]]; then
    icc_profile="none"
fi

extra_meta=$(exiftool -s3 -XResolution -YResolution -PNG:Interlace -PNG:Compression "$file" 2>/dev/null | paste -sd' | ' -)
if [[ -z "$extra_meta" ]]; then
    extra_meta="none"
fi

png_chunks="(pngcheck absent ou sortie vide)"
if command -v pngcheck >/dev/null 2>&1; then
    chunks=$(pngcheck -v "$file" 2>/dev/null | awk '/ chunk / { print $2 }' | sort -u | paste -sd',' -)
    if [[ -n "$chunks" ]]; then
        png_chunks="$chunks"
    fi
fi

cat <<REPORT

# PNG WEB AUDIT

file: "$file"
disk_size:
  bytes: $disk_bytes
  human: "$(human_size "$disk_bytes")"
dimensions:
  width: $width
  height: $height
color_model:
  type: "$type"
  colorspace: "$colorspace"
  depth_bits: $depth
  alpha: "$alpha"
unique_colors: $unique_colors
ram_estimate:
  rgb8:
    bytes: $rgb_bytes
    human: "$(human_size "$rgb_bytes")"
  rgba8:
    bytes: $rgba_bytes
    human: "$(human_size "$rgba_bytes")"
icc_profile: "$icc_profile"
png_chunks: "$png_chunks"
extra_metadata: "$extra_meta"

REPORT
