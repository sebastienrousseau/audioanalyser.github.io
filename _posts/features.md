---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Features: recording, transcription, analysis and recommendations | Audio Analyser"
description: "What Audio Analyser does: microphone recording, Azure AI Speech transcription, Azure AI Language text analysis, recommendations from six language-model providers, translation, text to speech and a local dashboard."
keywords: "audio analyser features, azure speech to text, azure text analytics, sentiment analysis, llm recommendations, text to speech, translation"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "Features"
headline: "What Audio Analyser does, and where it stops"
lead: "Each section says what the command does, which service it uses and where it writes its results."
nav_features: "true"
---
## Recording

**`-rec` records from the default microphone** into `INPUT_FOLDER`. By
default it records ten seconds of mono, 16-bit audio at 44.1 kHz. Pass a
JSON file to change the channels (one or two), the sample rate (8,000 to
48,000 Hz), the sample format and the duration:

```bash
python -m audioanalyser -rec settings.json
```

Recording uses PyAudio, which needs the PortAudio library on the machine.

## Speech to text

**`-stt` transcribes an audio file with Azure AI Speech.** It handles long
recordings through continuous recognition, and saves each transcript as
text and JSON in `TRANSCRIPTS_FOLDER`, with a row in a SQLite database.

```bash
python -m audioanalyser -stt meeting.wav
```

## Text analysis

**`-ta` analyses every `.txt` transcript in `TRANSCRIPTS_FOLDER`** with Azure
AI Language: sentiment, named entities, key phrases and the language of the
text. Results go to `REPORTS_FOLDER` as text and JSON, with a summary in
SQLite.

## Recommendations

**`-sum` sends each transcript to a language model** and writes a summary
with recommendations to `RECOMMENDATIONS_FOLDER`. The provider is chosen
with `LLM_PROVIDER`: `openai` (the default), `anthropic`, `gemini`,
`ollama`, `claude-cli` or `agy-cli`. The
[providers page](/audioanalyser.github.io/providers/) covers each one.

## Translation and text to speech

**`-t` translates transcripts with Azure AI Translator** into the languages
you list, for example `-t fr de`, writing them to `TRANSLATIONS_FOLDER`.
**`-tts` reads text aloud with Azure AI Speech** and saves the audio file:

```bash
python -m audioanalyser -tts "hello" greeting
```

## The dashboard

**`-s` starts a local web server on port 8080** with a dashboard for
recording, transcribing, analysing, generating recommendations and reading
the results, and the same actions as HTTP endpoints. It serves the
`dashboard/` folder of the repository, so run it from a clone.

## Where it stops

- It needs Azure: transcription, analysis, translation and text to speech
  have no offline alternative in the code.
- The command line handles one task per run; there is no single command
  for the whole pipeline.
- Folders and keys come from environment variables, usually a `.env` file;
  there is no configuration file of its own.
