# Basic Makefile for AudioAnalyser Application
# Copyright (C) 2023-2026 Sebastien Rousseau.
# SPDX-License-Identifier: Apache-2.0 OR MIT

.PHONY: install run clean contrast validate build

build:
	@ssg build -f ssg.toml
	@mkdir -p docs/icons docs/assets/images
	@cp -R icons/. docs/icons/ 2>/dev/null || true
	@cp -R icons/. docs/assets/images/ 2>/dev/null || true
	@cp audio-analyser-architecture.png docs/ 2>/dev/null || true
	@cp audio-analyser-architecture.png docs/assets/images/ 2>/dev/null || true
	@cp public/404.html docs/404.html 2>/dev/null || true

install:
	pip install -r requirements.txt

run:
	python -m audioanalyser

clean:
	rm -rf __pycache__ build/ dist/ *.egg-info

contrast:
	@/usr/bin/python3 scripts/audit-contrast.py

validate:
	@/usr/bin/python3 scripts/validate-frontmatter.py
