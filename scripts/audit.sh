#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0 OR MIT
# Run `ssg audit` on docs/ the way GitHub Pages serves it.
#
# The site is a project site: base_url carries a path
# (/audioanalyser.github.io), and every internal link starts with it.
# ssg 0.0.69's links gate resolves a root-relative link against the
# output directory itself, so on docs/ it reports every internal link as
# missing. That gate runs on a copy of docs/ placed under the base path,
# which is how the files are served. Every other gate reads files at the
# site root (llms.txt, agents.txt, _headers...) and runs on docs/ as it
# is. Both runs fail the build on any error.
set -euo pipefail

prefix=$(python3 -c 'import tomllib,urllib.parse;print(urllib.parse.urlsplit(tomllib.load(open("ssg.toml","rb"))["base_url"]).path.rstrip("/"))')
if [ -z "$prefix" ]; then
  exec ssg audit -o docs -f ssg.toml --skip-network
fi

stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
mkdir -p "$stage$(dirname "$prefix")"
cp -R docs "$stage$prefix"

for gate in wcag jsonld hreflang lang_consistency csp_sri pqc_tls html5 \
  metadata markdownlint performance ai_discovery feeds images search_index; do
  ssg audit -o docs -f ssg.toml --skip-network --gate "$gate" 2>&1 | grep -v -e '^\[INFO' -e 'not selected'
done
ssg audit -o "$stage" -f ssg.toml --skip-network --gate links 2>&1 | grep -v -e '^\[INFO' -e 'not selected'
echo "audit: all 15 gates passed"
