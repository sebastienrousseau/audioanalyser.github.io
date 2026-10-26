# Makefile for Audio Analyser: the Python application and its website.
# Copyright (C) 2023-2026 Sebastien Rousseau.
# SPDX-License-Identifier: Apache-2.0 OR MIT

.PHONY: all help install run build serve screenshot clean

all: build

help:
	@echo "make install    - install the application's Python dependencies"
	@echo "make run        - run the application (python -m audioanalyser)"
	@echo "make build      - build the website into docs/ and run every check"
	@echo "make serve      - build, then serve the site on http://127.0.0.1:8000/audioanalyser.github.io/"
	@echo "make screenshot - render static/images/screenshot.png from the build"
	@echo "make clean      - remove Python and website build output"

install:
	pip install -r requirements.txt

run:
	python -m audioanalyser

# contrast.py gates the colour tokens (WCAG AAA text, 3:1 UI); ssg's own
# quality gate runs inside post-build.py; `ssg audit` then checks
# the final files (WCAG, JSON-LD, CSP/SRI, links, metadata, feeds...).
build:
	rm -rf docs
	python3 scripts/contrast.py
	ssg build -f ssg.toml -q
	python3 scripts/anchor_headings.py docs
	python3 scripts/post-build.py
	python3 scripts/og_images.py
	scripts/audit.sh

# The site lives under /audioanalyser.github.io/ on sebastienrousseau.com,
# so it is served under the same path locally.
serve: build
	rm -rf .serve && mkdir -p .serve && ln -s "$(CURDIR)/docs" .serve/audioanalyser.github.io
	python3 -m http.server 8000 --bind 127.0.0.1 --directory .serve

screenshot: build
	scripts/screenshot.sh

clean:
	rm -rf __pycache__ build/ dist/ *.egg-info docs public .cache .serve
