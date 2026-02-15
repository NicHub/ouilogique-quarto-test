#!/usr/bin/env bash

###
#
##

shopt -s expand_aliases
alias inkscape='/Applications/Inkscape.app/Contents/MacOS/Inkscape'

FILENAMES=(
    ../posts/2020-12-25-installer-pi-hole-sur-un-raspberry/images/Vortex_with_Wordmark-thumb
)

for filename in "${FILENAMES[@]}"; do
    echo "PROCESSING ${filename}"

    FILENAME_IN=$filename.svg
    FILENAME_OUT=$filename.png

    # inkscape                      \
    #     --export-area-page        \
    #     --export-width 512        \
    #     --export-height 512       \
    #     "$FILENAME_IN"            \
    #     -o "$FILENAME_OUT"

    inkscape                      \
        --export-area-page        \
        "$FILENAME_IN"            \
        -o "$FILENAME_OUT"

    source png_web_audit.sh $FILENAME_OUT

    pngquant                      \
        --strip                   \
        --speed 1                 \
        --verbose                 \
        --force                   \
        --skip-if-larger          \
        --quality 0-2             \
        10                        \
        --output "$FILENAME_OUT" \
        "$FILENAME_OUT"

    source png_web_audit.sh $FILENAME_OUT

    open -a ImageOptim.app "$FILENAME_OUT"

    source png_web_audit.sh $FILENAME_OUT

done
