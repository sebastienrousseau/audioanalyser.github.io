---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Command and configuration reference | Audio Analyser"
description: "Reference for Audio Analyser: every command-line flag, the environment variables each module reads, and the folders it writes to."
keywords: "audioanalyser commands, audio analyser cli, audioanalyser environment variables"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "Reference"
headline: "Commands and configuration"
lead: "Checked against audioanalyser/__main__.py and the modules on the main branch."
nav_docs: "true"
---
## Commands

Run each as `python -m audioanalyser <flag>`; one task per run.

| Flag | What it does | Example |
| :--- | :--- | :--- |
| `-rec [settings.json]` | Record from the microphone | `-rec` |
| `-stt <file>` | Transcribe an audio file with Azure AI Speech | `-stt meeting.wav` |
| `-ta` | Analyse every transcript in `TRANSCRIPTS_FOLDER` | `-ta` |
| `-sum` | Summarise transcripts and write recommendations | `-sum` |
| `-t <codes...>` | Translate transcripts into these languages | `-t fr de` |
| `-tts <text> <name>` | Speak the text and save it as `<name>` | `-tts "hello" greeting` |
| `-s` | Start the dashboard on port 8080 | `-s` |
| `-h` | Print the usage | `-h` |

## Configuration

Settings are environment variables, read from a `.env` file in the working
directory. `env.example` documents most of them.

### Folders

| Variable | Used by |
| :--- | :--- |
| `INPUT_FOLDER` | Recording (output), transcription (input) |
| `TRANSCRIPTS_FOLDER` | Transcription (output), analysis, recommendations, translation (input) |
| `REPORTS_FOLDER` | Analysis (output) |
| `RECOMMENDATIONS_FOLDER` | Recommendations (output) |
| `TRANSLATIONS_FOLDER` | Translation (output) |
| `RECORDS_FOLDER` | Text to speech (output) |

### Azure

| Variable | Service |
| :--- | :--- |
| `AZURE_AUDIO_TEXT_KEY`, `REGION`, `AUDIO_EXTENSION` | Azure AI Speech |
| `AZURE_LANGUAGE_ENDPOINT`, `AZURE_LANGUAGE_KEY` | Azure AI Language |
| `AZURE_TRANSLATOR_KEY`, `AZURE_TRANSLATOR_ENDPOINT`, `TRANSLATIONS_LANGUAGES` | Azure AI Translator |
| `TRANSCRIPTS_DB_TABLE_NAME`, `ANALYSIS_DB_TABLE_NAME` | SQLite table names |

### Recommendations

| Variable | Meaning |
| :--- | :--- |
| `LLM_PROVIDER` | `openai` (default), `anthropic`, `gemini`, `ollama`, `claude-cli`, `agy-cli` |
| `LLM_MODEL` | Model for the chosen provider; overrides its default |
| `GPT3_API_KEY`, `OPENAI_MODEL` | OpenAI key, and the older model setting |
| `ANTHROPIC_API_KEY` | Anthropic key |
| `GEMINI_API_KEY`, `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` | Gemini, by key or through Vertex AI |
| `OLLAMA_HOST` | Ollama server, `http://localhost:11434` by default |

### Recording

`CHANNELS`, `CHUNK`, `FORMAT`, `RATE` and `RECORD_SECONDS` set the recording
defaults; a settings file passed to `-rec` overrides them.
