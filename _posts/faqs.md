---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Frequently asked questions about Audio Analyser | Audio Analyser"
description: "Answers about Audio Analyser: what it does, what it needs, PyPI, local-only use, providers, the dashboard, supported Python and the licence."
keywords: "audio analyser faq, audioanalyser pypi, audio analyser offline, audio analyser ollama"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "FAQ"
headline: "Frequently asked questions"
lead: "Short answers first; each links to the page with the detail where there is one."
nav_faqs: "true"
---
## What is Audio Analyser?

A Python application that records, transcribes and analyses audio with Azure
AI, and writes recommendations with a language model. See the
[features](/audioanalyser.github.io/features/).

## Do I need Azure?

Yes, for transcription, analysis, translation and text to speech. Only the
recommendations step can run without a cloud service, using Ollama.

## Can I install it from PyPI?

PyPI has version 0.0.6 from February 2024, without the provider choice.
Install from a clone; see [getting started](/audioanalyser.github.io/getting-started/).

## Can transcripts stay on my machine?

The recommendations can, with `LLM_PROVIDER=ollama`. Transcription itself
always goes through Azure AI Speech. See the
[security page](/audioanalyser.github.io/security/#what-leaves-the-machine).

## Which language model does it use?

OpenAI's `gpt-4.1-mini` by default; Anthropic, Gemini, Ollama and two CLI
providers are also supported. See [providers](/audioanalyser.github.io/providers/).

## Is there a graphical interface?

Yes: `python -m audioanalyser -s` starts a local dashboard on port 8080. See
[the dashboard](/audioanalyser.github.io/features/#the-dashboard).

## Which Python versions are supported?

Python 3.10 or newer; CI runs on 3.10.

## What licence is it under?

The repository carries the Apache License 2.0 and the MIT licence. See the
[terms](/audioanalyser.github.io/terms/).
