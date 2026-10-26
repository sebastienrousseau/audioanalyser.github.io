---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Getting started with Audio Analyser: install, configure and run | Audio Analyser"
description: "Clone Audio Analyser, install its pinned requirements, configure Azure keys and folders in a .env file, and transcribe, analyse and summarise a first recording."
keywords: "audio analyser install, audioanalyser setup, azure speech key, .env configuration"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "Getting started"
headline: "Your first transcript with Audio Analyser"
lead: "From a fresh clone to a transcript, an analysis and a set of recommendations."
nav_docs: "true"
---
## What do I need?

- **Python 3.10 or newer.** CI tests on Python 3.10.
- **PortAudio**, for PyAudio: `portaudio19-dev` on Debian and Ubuntu, as
  CI installs it. PyAudio publishes wheels for Windows only, so elsewhere
  pip builds it against PortAudio.
- **Azure resources:** a Speech resource for transcription and text to
  speech, a Language resource for analysis, and a Translator resource if
  you translate.
- **A recommendation provider:** an API key for OpenAI, Anthropic or
  Gemini, or a local Ollama server.

## How do I install it?

```bash
git clone https://github.com/sebastienrousseau/audioanalyser.github.io.git
cd audioanalyser.github.io
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` pins every dependency with hashes. For the Anthropic or
Gemini providers, also install their SDK: `pip install anthropic` or
`pip install google-genai`.

## How do I configure it?

Copy the example environment file and fill it in:

```bash
cp env.example .env
```

The main settings:

| Variable | What it is |
| :--- | :--- |
| `INPUT_FOLDER` | Where recordings are written and audio is read |
| `TRANSCRIPTS_FOLDER` | Where transcripts are written |
| `REPORTS_FOLDER` | Where text analysis results go |
| `RECOMMENDATIONS_FOLDER` | Where summaries and recommendations go |
| `AZURE_AUDIO_TEXT_KEY`, `REGION` | Azure AI Speech key and region |
| `AZURE_LANGUAGE_ENDPOINT`, `AZURE_LANGUAGE_KEY` | Azure AI Language |
| `LLM_PROVIDER`, `LLM_MODEL` | Recommendation provider and model |

The [reference](/audioanalyser.github.io/documentation/#configuration) lists the rest.

## How do I run a first analysis?

```bash
python -m audioanalyser -rec            # record ten seconds
python -m audioanalyser -stt meeting.wav
python -m audioanalyser -ta
python -m audioanalyser -sum
```

Or start the dashboard and do the same from the browser:

```bash
python -m audioanalyser -s
```

then open `http://127.0.0.1:8080/`.
