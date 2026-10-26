#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Give every built page its own Open Graph image.

For each page in the output it renders a 1200x630 card (the page title
and description on the Audio Analyser palette, with the logo) through headless
Chrome into og/<slug>.png, then points the page's og:image and
twitter:image at that file. Run after post-build.py. The build fails if
Chrome is missing or any page is left without its image, so CI enforces
it. Set CHROME to choose the binary.
"""

from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import tomllib

CONFIG = tomllib.loads(Path("ssg.toml").read_text(encoding="utf-8"))
BASE = CONFIG["base_url"].rstrip("/")
OUT = Path(CONFIG["output_dir"])
LOGO = Path("static/logo.svg").read_text(encoding="utf-8")
WIDTH, HEIGHT = 1200, 630
SKIP = {"404", "offline", "thanks"}
CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
)
TITLE = re.compile(r'<meta property="og:title" content="([^"]*)"')
DESCRIPTION = re.compile(r'<meta name="description" content="([^"]*)"')
OG_IMAGE = re.compile(r'(<meta property="og:image" content=")[^"]*(")')
OG_WIDTH = re.compile(r'(<meta property="og:image:width" content=")[^"]*(")')
OG_HEIGHT = re.compile(r'(<meta property="og:image:height" content=")[^"]*(")')
TWITTER_IMAGE = re.compile(r'(<meta name="twitter:image" content=")[^"]*(")')

CARD = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{w}px;height:{h}px;background:#111111;color:#fafafa;
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}}
.card{{box-sizing:border-box;height:100%;padding:72px 80px;display:flex;flex-direction:column;
border-top:12px solid #8cc6ff}}
.brand{{display:flex;align-items:center;gap:20px;font-size:34px;font-weight:600;color:#8cc6ff}}
.brand svg{{width:72px;height:72px}}
h1{{font-size:68px;line-height:1.1;margin:56px 0 24px;font-weight:700;letter-spacing:-0.02em}}
p{{font-size:30px;line-height:1.4;margin:0;color:#d4d4d8;max-width:1000px}}
.url{{margin-top:auto;font-size:26px;color:#a1a1aa}}
</style></head><body><div class="card">
<div class="brand">{logo}<span>Audio Analyser</span></div>
<h1>{title}</h1><p>{description}</p><div class="url">{host}</div>
</div></body></html>"""


def find_chrome() -> str:
    for candidate in (os.environ.get("CHROME"), *CHROME_CANDIDATES):
        if candidate and (shutil.which(candidate) or Path(candidate).is_file()):
            return candidate
    sys.exit("og_images: no Chrome or Chromium found; set CHROME")


def slug_for(page: Path) -> str:
    rel = page.parent.relative_to(OUT).as_posix()
    return "home" if rel == "." else rel.replace("/", "-")


def pages() -> list[Path]:
    found = sorted(OUT.rglob("index.html"))
    return [p for p in found if slug_for(p) not in SKIP]


def card_html(page_html: str) -> str:
    title = TITLE.search(page_html)
    description = DESCRIPTION.search(page_html)
    if not title or not description:
        raise ValueError("page has no og:title or description")
    host = BASE.split("://", 1)[-1]
    return CARD.format(
        w=WIDTH,
        h=HEIGHT,
        logo=LOGO,
        title=title.group(1),
        description=description.group(1),
        host=html.escape(host),
    )


def render(chrome: str, card: str, target: Path, workdir: Path) -> None:
    source = workdir / f"{target.stem}.html"
    source.write_text(card, encoding="utf-8")
    # Its own profile, so a running Chrome on the same machine is never shared.
    command = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={workdir / 'profile'}",
        f"--window-size={WIDTH},{HEIGHT}",
        "--force-device-scale-factor=1",
        f"--screenshot={target.resolve()}",
        source.as_uri(),
    ]
    subprocess.run(command, check=True, capture_output=True, timeout=60)
    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError(f"Chrome wrote no image for {target.name}")


def point_meta(page_html: str, url: str) -> str:
    for pattern, value in (
        (OG_IMAGE, url),
        (TWITTER_IMAGE, url),
        (OG_WIDTH, str(WIDTH)),
        (OG_HEIGHT, str(HEIGHT)),
    ):
        page_html, count = pattern.subn(rf"\g<1>{value}\g<2>", page_html)
        if count != 1:
            raise ValueError(
                f"expected one {pattern.pattern[:30]}... tag, found {count}"
            )
    return page_html


def main() -> int:
    chrome = find_chrome()
    target_dir = OUT / "og"
    target_dir.mkdir(exist_ok=True)
    done = 0
    with tempfile.TemporaryDirectory() as tmp:
        for page in pages():
            slug = slug_for(page)
            page_html = page.read_text(encoding="utf-8")
            render(chrome, card_html(page_html), target_dir / f"{slug}.png", Path(tmp))
            page.write_text(
                point_meta(page_html, f"{BASE}/og/{slug}.png"), encoding="utf-8"
            )
            done += 1
    print(f"og_images: {done} pages, one 1200x630 image each in {target_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
