---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Changelog: recent Audio Analyser changes | Audio Analyser"
description: "Recent changes to Audio Analyser from its Git history: Anthropic, Gemini and Ollama providers, quality gates, coverage reporting and dependency fixes."
keywords: "audio analyser changelog, audioanalyser release notes"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "Changelog"
headline: "Recent changes"
lead: "From the repository's merged pull requests. The full history is on GitHub."
---
## Since v0.0.7

- **Dependency advisories fixed:** aiohttp 3.14.4, certifi 2026.10.23,
  multidict 6.9.1, setuptools 84.2.1 and urllib3 2.8.0, with floors in
  `pyproject.toml` so affected versions cannot resolve.
- **Least-privilege CI token:** the Python workflow reads by default and
  only the release job writes.
- **This website** rebuilt with Static Site Generator 0.0.69, deployed by
  GitHub Actions.

## Earlier in 2026

- **More recommendation providers** (#42): Anthropic, Gemini and Ollama
  alongside OpenAI, chosen with `LLM_PROVIDER`.
- **Quality gates enforced** (#43): pylint and bandit join the test suite
  and flake8 in CI, with a coverage floor.
- **Coverage reporting** (#44, #45) to Codecov.
- **Release changelog** (#46): the release job writes a real changelog.

The [commit history](https://github.com/sebastienrousseau/audioanalyser.github.io/commits/main) and the
[releases](https://github.com/sebastienrousseau/audioanalyser.github.io/releases) have every change.
