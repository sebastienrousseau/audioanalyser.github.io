---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Security: where your audio goes, and reporting vulnerabilities | Audio Analyser"
description: "What Audio Analyser sends to Azure and to language-model providers, how it handles keys, what CI checks, and how to report a vulnerability."
keywords: "audio analyser security, azure speech privacy, report vulnerability"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "Security"
headline: "Where your audio goes"
lead: "Audio Analyser runs on your machine. These are the only places it sends data."
nav_security: "true"
---
## What leaves the machine?

| Command | Sends | To |
| :--- | :--- | :--- |
| `-stt` | Audio | Azure AI Speech |
| `-ta` | Transcripts | Azure AI Language |
| `-t` | Transcripts | Azure AI Translator |
| `-tts` | Text | Azure AI Speech |
| `-sum` | Transcripts | Your `LLM_PROVIDER`; nothing with a local Ollama server |
| `-rec`, `-s` | Nothing | Local only |

Results stay in local folders and a local SQLite database.

## Where are the keys?

In environment variables, normally a `.env` file in the working directory.
Keep it out of version control; the repository's `.gitignore` excludes
`.env`.

## Is the dashboard safe to expose?

No. `-s` starts a development web server with no authentication, meant for
use on your own machine. Do not expose port 8080 to a network you do not
trust.

## What does CI check?

Every push and pull request to `main` and `feat/` branches runs the test
suite with a 95% coverage floor, flake8, pylint and bandit. Dependabot watches the Python dependencies and
the GitHub Actions, and CodeQL scans the code.

## How do I report a vulnerability?

Email **sebastian.rousseau@gmail.com**, the address in the repository's
[security policy](https://github.com/sebastienrousseau/audioanalyser.github.io/security/policy). Do not open a public issue.
Machine-readable contact details are in
[security.txt](/audioanalyser.github.io/.well-known/security.txt).
