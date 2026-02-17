#!/usr/bin/env bash

###
# Install rg on Linux
# sudo apt install ripgrep -y
#
# Install rg on macOS
# brew install ripgrep
#
# usage:
# cd <dir to scan>
# bash <path to this script>/detect_gremlins.sh
##

set -euo pipefail

# COUNT ALL GREMLINS
results=$(rg                  \
    --with-filename           \
    --line-number             \
    --column                  \
    --only-matching           \
    "[\x{E000}-\x{F8FF}]"     \
    .)
echo "$results"
echo "Gremlins count: $(echo "$results" | wc -l)"

echo -e "\n===\n"

# COUNT FILES CONTAINING GREMLINS
results=$(rg                  \
    -l                  \
    --only-matching           \
    "[\x{E000}-\x{F8FF}]"     \
    .)
echo "$results"
echo "file count: $(echo "$results" | wc -l)"


###
# OTHER PUAs (Private Use Area (Zone d'usage privé))
#
# # Toutes les plages problématiques connues
# PATTERNS=(
#     # Private Use Areas (les trois)
#     "[\x{E000}-\x{F8FF}]"
#     "[\x{F0000}-\x{FFFFF}]"
#     "[\x{100000}-\x{10FFFF}]"
#
#     # Contrôles C0 (hors \t \n \r)
#     "[\x{00}-\x{08}\x{0B}\x{0C}\x{0E}-\x{1F}]"
#
#     # DEL + contrôles C1
#     "[\x{7F}-\x{9F}]"
#
#     # Zero-width et direction marks
#     "[\x{200B}-\x{200F}\x{202A}-\x{202E}\x{2060}-\x{2064}\x{206A}-\x{206F}]"
#
#     # Séparateurs de lignes/paragraphes
#     "[\x{2028}\x{2029}]"
#
#     # BOM en milieu de fichier + noncharacters fin BMP
#     "[\x{FEFF}\x{FFF0}-\x{FFFF}]"
#
#     # Noncharacters Unicode officiels
#     "[\x{FDD0}-\x{FDEF}]"
#
#     # Surrogates (invalides en UTF-8)
#     "[\x{D800}-\x{DFFF}]"
#
#     # Replacement character (UTF-8 corrompu)
#     "\x{FFFD}"
# )
##