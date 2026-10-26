---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Contributing to Audio Analyser | Audio Analyser"
description: "How to report a bug, suggest a feature or send a change to Audio Analyser: setting up, running the tests and linters, and opening a pull request."
keywords: "contribute to audio analyser, audioanalyser development, pytest"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "Contributing"
headline: "Contributing to Audio Analyser"
lead: "Bug reports, documentation fixes and code are all welcome."
---
## How do I report a bug or ask for a feature?

[Open an issue](https://github.com/sebastienrousseau/audioanalyser.github.io/issues) with the steps to reproduce, what you
expected and what happened, and your Python version and operating system.
Report security problems by email instead, as the
[security page](/audioanalyser.github.io/security/#how-do-i-report-a-vulnerability) explains.

## How do I set up the repository?

```bash
git clone https://github.com/sebastienrousseau/audioanalyser.github.io.git
cd audioanalyser.github.io
pip install -r requirements.txt pytest pytest-cov flake8 pylint bandit
```

## How do I check a change?

```bash
pytest                                # tests, 95% coverage floor
flake8
pylint audioanalyser/
bandit -c .bandit.yml -r audioanalyser/
```

The tests replace PyAudio with a stub when PortAudio is not installed, and
deselect the integration tests that need a live Ollama server; run those
with `pytest -m integration`.

## How do I send a change?

Create a branch, make the change with its tests, run the checks above and
open a pull request against `main`.

## What about this website?

The site's source is in `_posts/` and `_layouts/` of the same repository;
`make build` builds and checks it.
