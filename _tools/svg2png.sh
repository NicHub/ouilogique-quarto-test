#!/usr/bin/env bash

###
#
##

shopt -s expand_aliases
alias inkscape='/Applications/Inkscape.app/Contents/MacOS/Inkscape'

FILENAMES=(
    # ../posts/2020-12-25-installer-pi-hole-sur-un-raspberry/images/Vortex_with_Wordmark-thumb
    # ../posts/2023-03-09-installer-raspberry-pi-os-sur-raspberry-pi-sans-clavier-ni-souris-ni-ecran/images/Raspberry_Pi_Logo-thumb
    # ../posts/2018-02-15-introduction-html/images/HTML5_Logo-thumb
    # ../posts/2018-02-16-introduction-css/images/CSS3_logo_and_wordmark-thumb
    ../posts/2018-02-17-introduction-javascript/images/Javascript-shield-thumb
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

    open -Wa ImageOptim.app "$FILENAME_OUT"

    source png_web_audit.sh $FILENAME_OUT

done
