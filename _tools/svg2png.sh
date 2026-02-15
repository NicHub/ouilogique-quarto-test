#!/usr/bin/env bash

###
#
# Export SVG to PDF and PNG
#
# @author         Nicolas Jeanmonod
# @copyright (c)  2026 ouilogique.com All rights reserved.
#
#
# Inkscape 1.0.1
# Install from Ubuntu Software GUI installer
# Install path is /snap/bin/inkscape
# !! Doesn't work with Inkscape v 0.92.3. !!
# brew install --cask inkscape # macOS
#
# PNGQUANT
# https://pngquant.org/
# sudo apt-get update
# sudo apt-get install pngquant
# brew install pngquant # macOS
#
##

# Strict mode.
set -Eeuo pipefail

# Aliases to binaries.
shopt -s expand_aliases
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    alias inkscape='/snap/bin/inkscape'
elif [[ "$OSTYPE" == "darwin"* ]]; then
    alias inkscape='/Applications/Inkscape.app/Contents/MacOS/Inkscape'
else
    echo "OSTYPE $OSTYPE not supported"
    exit
fi

# Test if the binaries for transform are present.
test_if_binary_exists () {
    if ! type $COMMAND &> /dev/null
    then
        echo "$COMMAND could not be found"
        exit
    fi
}
COMMANDS=(
    inkscape
    pngquant
    gm
)
for COMMAND in "${COMMANDS[@]}"; do
    test_if_binary_exists
done

convert () {
    # Convert SVG to PNG.
    # inkscape --export-area-page --export-width $WIDTH --export-height $HEIGHT $FILENAME_IN -o $FILENAME_OUT
    inkscape --export-area-page $FILENAME_IN -o $FILENAME_OUT

    # Optimize PNG.
    pngquant --speed 1 --strip --verbose --force 10 $FILENAME_OUT --output $FILENAME_OUT

    # Check PNG info.
    source png_web_audit.sh $FILENAME_OUT
}

# SVG file to convert (without extension).
FILENAMES=(
    ../posts/2020-12-25-installer-pi-hole-sur-un-raspberry/images/Vortex_with_Wordmark-thumb
)

for FILENAME in "${FILENAMES[@]}"; do
    FILENAME_IN=$FILENAME.svg
    FILENAME_OUT=$FILENAME.png
    convert
    if command -v imgcat >/dev/null 2>&1; then
        imgcat -H 10 $FILENAME_OUT
    fi
done
