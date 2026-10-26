---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Recommendation providers: OpenAI, Anthropic, Gemini, Ollama and CLIs | Audio Analyser"
description: "The six language-model providers Audio Analyser can use for summaries and recommendations, their default models, how each authenticates and where your transcripts go."
keywords: "audio analyser llm providers, openai, anthropic claude, google gemini, ollama local llm, claude code cli"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "Providers"
headline: "Choose who reads your transcripts"
lead: "Set LLM_PROVIDER to one of six backends. The rest of Audio Analyser works the same whichever you pick."
nav_providers: "true"
---
## The six providers

| `LLM_PROVIDER` | Default model | Authentication | Extra install |
| :--- | :--- | :--- | :--- |
| `openai` (default) | `gpt-4.1-mini` | `GPT3_API_KEY` | None |
| `anthropic` | `claude-opus-5` | `ANTHROPIC_API_KEY`, or a stored `ant auth login` session | `pip install anthropic` |
| `gemini` | `gemini-2.5-flash` | `GEMINI_API_KEY`, or Vertex AI with `GOOGLE_CLOUD_PROJECT` | `pip install google-genai` |
| `ollama` | `llama3.1` | None | A running Ollama server with the model pulled |
| `claude-cli` | The CLI's own | A signed-in Claude Code CLI | The CLI |
| `agy-cli` | The CLI's own | A signed-in Agy CLI | The CLI |

`LLM_MODEL` overrides the default for any provider. For `openai`, the older
`OPENAI_MODEL` setting still works when `LLM_MODEL` is unset.

## Which one keeps my data local?

`ollama`. It talks to the server at `OLLAMA_HOST`, `http://localhost:11434`
by default, so with a local server transcripts never leave the machine.
Every other provider sends transcripts to its service.

## What if the SDK is missing?

The provider SDKs are imported only when used, so installing one never
requires the others. Choosing a provider whose SDK is not installed stops
with an error that names the package to install, and an unknown
`LLM_PROVIDER` lists the valid names.
