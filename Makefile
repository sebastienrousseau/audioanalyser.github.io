# Basic Makefile for AudioAnalyser Application
# Copyright (C) 2023-2026 Sebastien Rousseau.
# SPDX-License-Identifier: Apache-2.0 OR MIT

.PHONY: install run clean contrast validate

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
