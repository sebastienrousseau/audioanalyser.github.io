---
name: "Audio Analyser"
short_name: "AA"
title: "Documentation & Quick Start | Python SDK & CLI"
description: "Complete developer guide for Audio Analyser: PyPI package installation, Python SDK examples, CLI commands, and Docker microservice deployment."
keywords: "Audio Analyser Documentation, Python Audio SDK, PyPI Audio Analyser, CLI Audio Processing, Fast Fourier Transform Code, Docker Audio Microservice"
author: "Sébastien Rousseau"
date: "2026-08-31"
language: "en-GB"
layout: "documentation"
permalink: "https://audioanalyser.github.io/documentation/index.html"
---

<section class="section">
  <div class="container stack">
    <div class="stack text-center">
      <p class="eyebrow">DEVELOPER DOCUMENTATION</p>
      <h1>Getting Started with Audio Analyser</h1>
      <p class="lead mx-auto" style="max-width:48rem;">Install the CLI tool, integrate the Python library, or deploy the containerized microservice in minutes.</p>
    </div>

    <div class="card stack" style="margin-top:var(--gap); padding:var(--gap);">
      <div style="display:flex; align-items:center; gap:12px;">
        <img src="/icons/store.png" alt="" aria-hidden="true" width="36" height="36" />
        <h2>1. Installation via PyPI</h2>
      </div>
      <p>Install the official package using standard Python package managers:</p>
      <div style="background:var(--surface-soft); padding:1rem 1.25rem; border-radius:12px; border:1px solid var(--line-soft); font-family:monospace; font-size:0.95rem;">
        pip install audioanalyser
      </div>

      <div style="display:flex; align-items:center; gap:12px; margin-top:var(--gap);">
        <img src="/icons/analyze.png" alt="" aria-hidden="true" width="36" height="36" />
        <h2>2. Python SDK Usage Example</h2>
      </div>
      <p>Analyze an audio file, compute Fast Fourier Transforms, extract speech transcripts, and evaluate conversation sentiment:</p>
      <pre style="background:var(--surface-soft); padding:1rem 1.25rem; border-radius:12px; border:1px solid var(--line-soft); font-family:monospace; font-size:0.92rem; overflow-x:auto;">
<code>from audioanalyser import AudioAnalyser

# Initialize the analyser with language configuration
analyser = AudioAnalyser(language="en-US")

# Process audio file and extract acoustic telemetry
result = analyser.process("sample_call.wav")

# Output insights
print(f"Transcript: {result.transcript}")
print(f"Sentiment Score: {result.sentiment_score}")
print(f"Spectral Centroid (Hz): {result.spectral_centroid}")
print(f"Key Phrases: {result.key_phrases}")</code></pre>

      <div style="display:flex; align-items:center; gap:12px; margin-top:var(--gap);">
        <img src="/icons/server.png" alt="" aria-hidden="true" width="36" height="36" />
        <h2>3. CLI Command Line Interface</h2>
      </div>
      <p>Run instant audio analysis and generate structured JSON reports directly from your terminal:</p>
      <div style="background:var(--surface-soft); padding:1rem 1.25rem; border-radius:12px; border:1px solid var(--line-soft); font-family:monospace; font-size:0.95rem;">
        audioanalyser process --input recordings/call-01.wav --output report.json
      </div>
    </div>
  </div>
</section>