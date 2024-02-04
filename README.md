<!-- markdownlint-disable MD033 MD041 -->

<img
  align="right"
  alt="Logo of Audio Analyser"
  height="261"
  src="https://kura.pro/audioanalyser/images/logos/audioanalyser.webp"
  width="261"
  />

<!-- markdownlint-enable MD033 MD041 -->

# audioanalyser.co - Official Website 🌏

Welcome to the repository for
[audioanalyser.co](https://audioanalyser.co), the digital presence of Audio Analyser.

Audio Analyser offers state-of-the-art audio transcription, integrated speech-to-text, text analysis, and multilingual translations, efficiently providing critical insights from audio data to enhance both customer experience (CX) and employee experience (EX).

## Quick Start Guide

Setting up and running the website locally is easy and quick with the
[Shokunin Static Site Generator (SSG)][00].

### Prerequisites

Ensure you have the **Rust toolchain** installed. If not, follow the guide on
the [Rust website][01] to set it up.

### Installation & Usage

1. Install Shokunin SSG:

```shell
cargo install ssg
```

2. Clone the repository

```shell
git clone https://github.com/sebastienrousseau/audioanalyser.github.io.git
```

3. Generate the static site for audioanalyser.co

```shell
ssg -n=docs -c=_posts -t=_layouts -o=output -s=public
```


[00]: https://shokunin.one "Shokunin Static Site Generator"
[01]: https://www.rust-lang.org/learn/get-started "Rust"
