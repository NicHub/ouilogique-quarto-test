#!/usr/bin/env bash
set -euo pipefail

OUT=../images
mkdir -p $OUT

logo_urls=(
#   "https://upload.wikimedia.org/wikipedia/commons/2/22/Slackware_logo_from_the_official_Slackware_site.svg"
#   "https://upload.wikimedia.org/wikipedia/commons/4/4a/Debian-OpenLogo.svg"
#   "https://upload.wikimedia.org/wikipedia/en/e/ee/Red_Hat_Enterprise_Linux_logo-en.svg"
#   "https://en.wikipedia.org/wiki/Special:FilePath/Gentoo%20Linux%20logo%20matte.svg"
#   "https://upload.wikimedia.org/wikipedia/commons/5/56/Arch_Linux_logo_with_light_text.svg"
#   "https://upload.wikimedia.org/wikipedia/commons/7/72/OpenSUSE_Leap_green_logo.svg"
#   "https://en.wikipedia.org/wiki/Special:FilePath/Alpine%20Linux.svg"
#   "https://en.wikipedia.org/wiki/Special:FilePath/Fedora%20logo%20%282021%29.svg"
#   "https://en.wikipedia.org/wiki/Special:FilePath/Garuda-purple.svg"
  "https://en.wikipedia.org/wiki/Special:FilePath/Solus.svg"
  "https://en.wikipedia.org/wiki/Special:FilePath/System-rescue-cd-logo-new.svg"
  "https://upload.wikimedia.org/wikipedia/commons/0/00/Ubuntu-logo-no-wordmark-2022.svg"
  "https://upload.wikimedia.org/wikipedia/commons/0/02/Void_Linux_logo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/0/09/Backtrack_logo.png"
  "https://upload.wikimedia.org/wikipedia/commons/1/14/Zorin_Logomark.svg"
  "https://upload.wikimedia.org/wikipedia/commons/2/29/MX_LINUX_Logo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/3/34/Grmllogo.png"
  "https://upload.wikimedia.org/wikipedia/commons/3/3c/Kubuntu_2024_Logo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/4/45/The_Linux_Mint_Logo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/4/4b/ArtixLogo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/4/4b/Banner_logo_Puppy.png"
  "https://upload.wikimedia.org/wikipedia/commons/4/4b/EndeavourOS_Logo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/4/4b/Kali_Linux_2.0_wordmark.svg"
  "https://upload.wikimedia.org/wikipedia/commons/5/5a/SteamOS_wordmark.svg"
  "https://upload.wikimedia.org/wikipedia/commons/7/79/Linux_Lite_Simple_Fast_Free_logo.png"
  "https://upload.wikimedia.org/wikipedia/commons/8/83/Elementary_OS_logo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/9/99/Tails-logo-flat-inverted.svg"
  "https://upload.wikimedia.org/wikipedia/commons/c/c4/NixOS_logo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/c/c5/Pop_OS-Logo-nobg.svg"
  "https://upload.wikimedia.org/wikipedia/commons/d/d1/Raspberry_Pi_OS_Logo.png"
  "https://upload.wikimedia.org/wikipedia/commons/e/ea/Logo_manjaro_rounded_2022.svg"
  "https://upload.wikimedia.org/wikipedia/commons/e/ea/Nobara_logotype.png"
  "https://upload.wikimedia.org/wikipedia/commons/e/ec/Calculatelinux-logo.png"
  "https://upload.wikimedia.org/wikipedia/commons/f/f4/Devuan-logo.svg"
  "https://upload.wikimedia.org/wikipedia/commons/f/f5/Deepin_logo.svg"
  "https://upload.wikimedia.org/wikipedia/en/e/e3/Clear_Linux_logo.svg"
)

for url in "${logo_urls[@]}"; do
  wget -P $OUT "$url"
  sleep 60
done
