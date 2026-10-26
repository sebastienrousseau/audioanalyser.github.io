---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Audio Analyser: speech-to-text and text analysis with Azure AI"
description: "Audio Analyser is an open-source Python command-line tool that records audio, transcribes it with Azure AI Speech, analyses the text with Azure AI Language and writes recommendations with a choice of language model."
keywords: "Audio Analyser, audioanalyser, speech to text, Azure AI Speech, text analytics, sentiment analysis, transcription, Python, Ollama, OpenAI, Anthropic"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "index"
language: "en-GB"
schema: "page"
changefreq: "weekly"
eyebrow: "Open-source Python tool"
headline: "Turn recordings into transcripts, analysis and recommendations"
lead: "Audio Analyser records or reads your audio, transcribes it with Azure AI Speech, analyses the text with Azure AI Language, and asks the language model of your choice for a summary and recommendations."
---
## What is Audio Analyser?

Audio Analyser is a free, open-source Python application by
[Sebastien Rousseau](https://sebastienrousseau.com/). From the command line
or a local web dashboard it records audio, transcribes audio files with
Azure AI Speech, runs sentiment analysis, entity recognition, key-phrase
extraction and language detection with Azure AI Language, translates
transcripts with Azure AI Translator, reads text aloud, and writes
summaries and recommendations with OpenAI, Anthropic, Google Gemini, a
local Ollama model, or a signed-in Claude Code or Agy CLI.

## What do I need?

Python 3.10 or newer, an Azure subscription with Speech and Language
resources, and a key for the recommendation provider you choose (none for
Ollama or the CLI providers). The [getting started guide](/audioanalyser.github.io/getting-started/)
walks through the setup.

## Where does my data go?

Audio goes to Azure AI Speech to be transcribed, and transcripts go to
Azure AI Language and to your recommendation provider. Results are written
to local folders and a local SQLite database. The
[security page](/audioanalyser.github.io/security/) lists every outbound call.

## Is it on PyPI?

The `audioanalyser` package on PyPI is version 0.0.6, from February 2024. It
predates the provider choice and the current dashboard, so install from a
clone of the repository instead, as the [guide](/audioanalyser.github.io/getting-started/)
shows.
