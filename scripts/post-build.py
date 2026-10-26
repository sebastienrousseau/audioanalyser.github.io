#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR MIT
"""Finish the site that `ssg build` wrote, using the values in ssg.toml.

- Points og:url and the hreflang alternate at each page's own canonical
  URL (the layout's shared head cannot know it; ssg sets the canonical).
- Replaces the dev-server origin ssg leaves in some links with base_url.
- Writes one sitemap.xml for the whole site, dated by the last commit,
  so a rebuild of the same commit produces the same file.
- Writes llms.txt (and CNAME when the site is served at the root of its
  own domain), and copies robots.txt, .well-known/, static/ (site files
  such as a logo) and 404.html into the output.
- Works when base_url has a path, as on a GitHub Pages project site:
  every root-relative link then starts with that path.
- Fails the build unless ssg's own 10-pillar quality gate passed 10/10.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from urllib.parse import urlsplit

CONFIG = tomllib.loads(Path("ssg.toml").read_text(encoding="utf-8"))
BASE = CONFIG["base_url"].rstrip("/")
OUT = Path(CONFIG["output_dir"])
# "" for a site at the root of its domain, "/name" for one under a path.
PREFIX = urlsplit(BASE).path.rstrip("/")
SKIP_IN_SITEMAP = {"404", "offline", "thanks"}
CANONICAL = re.compile(r'<link rel="canonical" href="([^"]+)"\s*/?>')


def last_commit_date() -> str:
    date = os.environ.get("SITE_DATE")
    if date:
        return date
    out = subprocess.run(["git", "log", "-1", "--format=%cs"], capture_output=True, text=True, check=False)
    return out.stdout.strip() or "1970-01-01"


def source_date(page: Path) -> str:
    """Last commit date of the Markdown file a built page comes from."""
    rel = page.parent.relative_to(OUT)
    src = Path(CONFIG["content_dir"]) / (f"{rel}.md" if str(rel) != "." else "index.md")
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(src)],
                         capture_output=True, text=True, check=False)
    return out.stdout.strip() or last_commit_date()


def fix_page(page: Path) -> str | None:
    text = page.read_text(encoding="utf-8")
    for dev in ("http://127.0.0.1:8000", "http://localhost:8000"):
        text = text.replace(dev, BASE)
    if PREFIX:
        # ssg 0.0.69 links the syntax-highlighting stylesheet at the domain
        # root (/highlight.<hash>.css) even when base_url has a path, which
        # 404s on a project site. Put any such link under the base path.
        text = re.sub(r'\b(href|src)="/(?!' + re.escape(PREFIX.lstrip("/")) + r'/)([^"/][^"]*)"',
                      lambda m: f'{m.group(1)}="{PREFIX}/{m.group(2)}"' if (OUT / m.group(2)).is_file() else m.group(0),
                      text)
    m = CANONICAL.search(text)
    url = m.group(1) if m else None
    if url:
        text = re.sub(r'(<meta property="og:url" content=")[^"]*(")', rf"\g<1>{url}\g<2>", text)
        text = re.sub(r'(<link rel="alternate" href=")[^"]*(" hreflang=)', rf"\g<1>{url}\g<2>", text)
    # dateModified: the last commit to the page's source, next to the
    # datePublished the layout prints, so freshness is machine-readable.
    text = re.sub(r'("datePublished": "[^"]*")', rf'\1,\n            "dateModified": "{source_date(page)}"', text, count=1)
    page.write_text(text, encoding="utf-8")
    return url


def title_of(page: Path) -> str:
    m = re.search(r"<title>(.*?)</title>", page.read_text(encoding="utf-8"), flags=re.DOTALL)
    return m.group(1).strip() if m else page.parent.name


def site_relative(path: str) -> str:
    """A root-relative URL path as a path inside the output directory."""
    if PREFIX and (path == PREFIX or path.startswith(PREFIX + "/")):
        path = path[len(PREFIX):]
    return path.lstrip("/")


def check_sri() -> list[str]:
    """Each local <script>/<link> with integrity= must match its file."""
    import base64
    import hashlib
    bad = []
    tag = re.compile(r'<(?:script|link)\b[^>]*\bintegrity="([^"]+)"[^>]*>')
    for page in sorted(OUT.rglob("*.html")):
        for m in tag.finditer(page.read_text(encoding="utf-8")):
            ref = re.search(r'\b(?:src|href)="(/[^"]+)"', m.group(0))
            if not ref:
                continue
            algo, _, want = m.group(1).partition("-")
            asset = OUT / site_relative(ref.group(1))
            got = base64.b64encode(hashlib.new(algo, asset.read_bytes()).digest()).decode() if asset.is_file() else "missing"
            if got != want:
                bad.append(f"{page.relative_to(OUT)}: {ref.group(1)} ({got if got == 'missing' else 'hash differs'})")
    return bad


def check_fragments() -> list[str]:
    """Every link to /page/#id on this site must land on an existing id."""
    ids = {}
    for page in OUT.rglob("index.html"):
        url = PREFIX + "/" + str(page.parent.relative_to(OUT)).replace(".", "") + "/"
        ids[url.replace("//", "/")] = set(re.findall(r'\bid="([^"]+)"', page.read_text(encoding="utf-8")))
    bad = []
    for page in sorted(OUT.rglob("*.html")):
        for path, frag in re.findall(r'href="(/[^"#?]*)#([^"]+)"', page.read_text(encoding="utf-8")):
            target = path if path.endswith("/") else path + "/"
            if frag not in ids.get(target, set()):
                bad.append(f"{page.relative_to(OUT)}: {path}#{frag}")
    return sorted(set(bad))


def main() -> None:
    date = last_commit_date()
    entries = []
    for page in sorted(OUT.rglob("*.html")):
        url = fix_page(page)
        top = page.relative_to(OUT).parts[0]
        if url and top not in SKIP_IN_SITEMAP:
            entries.append((url, title_of(page)))
    urls = "".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{date}</lastmod>\n  </url>\n" for u, _ in entries
    )
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n',
        encoding="utf-8",
    )
    shutil.copy2("robots.txt", OUT / "robots.txt")
    shutil.copytree(".well-known", OUT / ".well-known", dirs_exist_ok=True)
    if Path("static").is_dir():
        shutil.copytree("static", OUT, dirs_exist_ok=True)
    # GitHub Pages serves /404.html for a missing page; every link in it
    # is root-relative, so a copy of the built 404 page works there.
    if (OUT / "404" / "index.html").is_file():
        shutil.copy2(OUT / "404" / "index.html", OUT / "404.html")
    # A project site under a path is served from its owner's domain, which
    # its own repository configures; a CNAME here would claim that domain.
    if not PREFIX:
        domain = BASE.split("://", 1)[1]
        (OUT / "CNAME").write_text(domain + "\n", encoding="utf-8")
    else:
        (OUT / "CNAME").unlink(missing_ok=True)
    pages = "".join(f"- [{t}]({u})\n" for u, t in entries)
    (OUT / "llms.txt").write_text(
        f"# {CONFIG['site_name']}\n\n> {CONFIG['site_description']}\n\n## Pages\n\n{pages}", encoding="utf-8"
    )
    print(f"post-build: {len(entries)} pages in sitemap.xml, dated {date}")
    frags = check_fragments()
    if frags:
        print("broken #fragment links:\n  " + "\n  ".join(frags), file=sys.stderr)
        sys.exit(1)
    sri = check_sri()
    if sri:
        print("SRI check failed:\n  " + "\n  ".join(sri), file=sys.stderr)
        sys.exit(1)
    report = json.loads((OUT / "quality-gate-report.json").read_text(encoding="utf-8"))
    # Every pillar must pass. ssg 0.0.69's SRI pillar misreads an
    # apostrophe in an HTML comment in <head> as an opening quote, so
    # base.html keeps its head comments free of them.
    issues = [f"{name}: {issue}" for name, p in report["pillars"].items() for issue in p["issues"]]
    if issues or report["passed_pillars"] != report["total_pillars"]:
        print("quality gate failed:\n  " + "\n  ".join(issues), file=sys.stderr)
        sys.exit(1)
    print(f"quality gate: {report['passed_pillars']}/{report['total_pillars']} pillars, 0 issues")


if __name__ == "__main__":
    main()
