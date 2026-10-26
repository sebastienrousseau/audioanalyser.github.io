---
name: "audioanalyser"
short_name: "audioanalyser"
title: "Accessibility statement | Audio Analyser"
description: "How the Audio Analyser website is built to be accessible, how it is checked on every build, and how to report a barrier."
keywords: "audio analyser accessibility, accessibility statement"
author: "Sebastien Rousseau"
date: "2026-10-26"
news_publication_date: "2026-10-26"
layout: "page"
language: "en-GB"
schema: "page"
changefreq: "monthly"
eyebrow: "Accessibility"
headline: "Accessibility statement"
lead: "This site aims to be usable by everyone, with any input device and any assistive technology."
---
## How is the site built for accessibility?

- The site uses the Prism theme with colours taken from the Audio Analyser
  logo. Every text colour pair is checked at a contrast ratio of at least
  7:1, and borders and focus rings at 3:1, in light and dark mode; the build
  fails if one falls short.
- Navigation works without JavaScript; the menus are disclosure buttons with
  their expanded state announced, and Escape closes them.
- Every page has a skip link, one level-one heading and a language attribute.
- Light, dark and system themes are available from the header.

## How is it checked?

Every build runs the contrast check and the site generator's audit, which
includes its WCAG checks, and fails if the generator's quality gate reports
an issue.

## How do I report a barrier?

Use the [contact form](/audioanalyser.github.io/contact/) or
[open an issue](https://github.com/sebastienrousseau/audioanalyser.github.io/issues) describing the page and the problem, and it
will be fixed.
