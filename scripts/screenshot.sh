#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0 OR MIT
# Render static/images/screenshot.png (1500x1000) from the built site with
# headless Chrome. The image is the site's Open Graph/Twitter preview and the
# demo image in README.md. Run `make build` first.
set -euo pipefail

chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
command -v "$chrome" >/dev/null 2>&1 || [ -x "$chrome" ] || { echo "set CHROME to a Chrome or Chromium binary" >&2; exit 1; }
[ -f docs/index.html ] || { echo "docs/ is missing; run make build first" >&2; exit 1; }

# A site whose base_url has a path (a GitHub Pages project site) links its
# assets under that path, so serve docs/ there.
prefix=$(python3 -c 'import tomllib,urllib.parse;print(urllib.parse.urlsplit(tomllib.load(open("ssg.toml","rb"))["base_url"]).path.rstrip("/"))')
root=$(mktemp -d)
if [ -n "$prefix" ]; then
  mkdir -p "$root$(dirname "$prefix")"
  ln -s "$PWD/docs" "$root$prefix"
else
  rmdir "$root"
  root="$PWD/docs"
fi

port=8766
python3 -m http.server "$port" --bind 127.0.0.1 --directory "$root" >/dev/null 2>&1 &
server=$!
trap 'kill "$server"; [ -n "$prefix" ] && rm -rf "$root"' EXIT
for _ in $(seq 1 50); do curl -fs "http://127.0.0.1:$port$prefix/" >/dev/null && break; sleep 0.1; done

mkdir -p static/images
# Light scheme pinned, so the image does not depend on the machine's appearance.
"$chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1500,1000 \
  --blink-settings=preferredColorScheme=1 --force-device-scale-factor=1 --screenshot="$PWD/static/images/screenshot.png" \
  "http://127.0.0.1:$port$prefix/" >/dev/null 2>&1
echo "wrote static/images/screenshot.png"
