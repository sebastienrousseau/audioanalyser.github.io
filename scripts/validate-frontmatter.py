#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR MIT
# Semantic Version: v0.0.1
# Frontmatter Schema & Structural Linter
import os, sys

target_dirs = ["content", "_posts", "docs"]
found_files = []
ignored_names = {"README.md", "OPERATIONS.md", "i18n-followup.md", "SECURITY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE.md", "CHANGELOG.md"}

for td in target_dirs:
    if os.path.isdir(td):
        for root, dirs, files in os.walk(td):
            # Skip hidden directories like .vitepress
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if f.endswith(".md") and f not in ignored_names:
                    found_files.append(os.path.join(root, f))

if not found_files:
    print("No Markdown content pages found to validate.")
    sys.exit(0)

errors = []
for fpath in found_files:
    try:
        with open(fpath, "r", errors="ignore") as fp:
            content = fp.read()
            if not content.startswith("---"):
                errors.append(f"{fpath}: Missing frontmatter opening delimiter (---)")
                continue
            parts = content.split("---", 2)
            if len(parts) < 3:
                errors.append(f"{fpath}: Missing frontmatter closing delimiter (---)")
                continue
            fm = parts[1]
            if "title:" not in fm and "title =" not in fm:
                errors.append(f"{fpath}: Missing mandatory `title:` frontmatter field")
    except Exception as e:
        errors.append(f"{fpath}: Read error: {e}")

if errors:
    print(f"Frontmatter Validation: {len(errors)} error(s) found:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print(f"Frontmatter Validation: {len(found_files)} markdown page(s) verified successfully.")
    sys.exit(0)
