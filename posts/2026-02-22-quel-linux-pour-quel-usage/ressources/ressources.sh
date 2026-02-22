#  Quel Linux pour quel usage ?
URL=https://www.youtube.com/watch?v=rlNtyhGLA_Y

# List transcripts format
# formats: vtt, srt, ttml, srv3, srv2, srv1, json3
yt-dlp --list-subs "${URL}"

yt-dlp --write-auto-sub --skip-download --sub-lang fr-orig --sub-format   vtt "${URL}"
yt-dlp --write-auto-sub --skip-download --sub-lang fr-orig --sub-format   srt "${URL}"
yt-dlp --write-auto-sub --skip-download --sub-lang fr-orig --sub-format  ttml "${URL}" # Best
yt-dlp --write-auto-sub --skip-download --sub-lang fr-orig --sub-format  srv3 "${URL}"
yt-dlp --write-auto-sub --skip-download --sub-lang fr-orig --sub-format  srv2 "${URL}"
yt-dlp --write-auto-sub --skip-download --sub-lang fr-orig --sub-format  srv1 "${URL}"
yt-dlp --write-auto-sub --skip-download --sub-lang fr-orig --sub-format json3 "${URL}"

yt-dlp -f "bestvideo+bestaudio/best" "${URL}"
