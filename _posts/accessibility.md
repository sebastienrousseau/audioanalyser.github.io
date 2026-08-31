---
name: "Audio Analyser"
short_name: "AA"
title: "Accessibility Statement | WCAG 2.2 AA / AAA Standards"
description: "Comprehensive accessibility statement for Audio Analyser: WCAG 2.2 AA / AAA conformance, keyboard navigability, 7:1 contrast, and screen reader verification."
keywords: "Accessibility Statement, WCAG 2.2 AA, WCAG AAA, Digital Inclusion, Screen Reader Verification, Section 508, EN 301 549, High Contrast, Keyboard Accessible"
author: "Sébastien Rousseau"
date: "2026-08-31"
language: "en-GB"
layout: "accessibility"
permalink: "https://audioanalyser.github.io/accessibility/index.html"
---

<section class="section">
  <div class="container stack">
    <div class="stack">
      <p class="eyebrow">DIGITAL INCLUSION &amp; STANDARDS</p>
      <h1>Accessibility Statement</h1>
      <p class="lead">Our commitment to universal digital inclusion, WCAG 2.2 Level AA and AAA conformance, and keyboard accessibility for developers and researchers worldwide.</p>
    </div>

    <!-- Executive Summary Card -->
    <div class="card" style="background:var(--surface-soft); padding:var(--gap); margin-top:var(--gap); border-left:4px solid var(--accent);">
      <p class="lead" style="margin:0; font-weight:500;">Audio Analyser is dedicated to ensuring digital accessibility for people of all abilities. We continually improve the user experience for everyone and apply relevant accessibility standards across all documentation, API references, and interactive signal processing tools.</p>
    </div>

    <div class="stack" style="gap:var(--gap); margin-top:var(--gap);">
      <!-- 1. Standards & Conformance -->
      <article class="card stack" style="padding:var(--gap);">
        <h2>1. Conformance Standards &amp; Principles</h2>
        <div class="prose">
          <p>The Web Content Accessibility Guidelines (WCAG) defines requirements for designers and developers to improve accessibility for people with disabilities. It defines three levels of conformance: Level A, Level AA, and Level AAA.</p>
          <p>Audio Analyser is <strong>fully conformant with WCAG 2.2 Level AA</strong> and satisfies key <strong>Level AAA</strong> success criteria across all published pages, documentation, and tools. We also comply with the European Standard <strong>EN 301 549</strong> and the United States <strong>Section 508</strong> of the Rehabilitation Act.</p>
        </div>
      </article>

      <!-- 2. Four WCAG Principles -->
      <article class="card stack" style="padding:var(--gap);">
        <h2>2. Accessibility Measures by Principle</h2>
        <div class="grid grid-2" style="gap:1.5rem; margin-top:0.5rem;">
          <div class="card" style="background:var(--surface-soft); padding:1.25rem;">
            <h3 style="margin-top:0; color:var(--accent);">A. Perceivable</h3>
            <ul style="margin-bottom:0; font-size:0.92rem;">
              <li><strong>High Contrast:</strong> Text and interactive UI elements maintain a minimum contrast ratio of 7:1 against backgrounds in both light and dark themes.</li>
              <li><strong>Alternative Text:</strong> All diagrams, waveform schematics, and architecture graphics provide detailed alternative text descriptions.</li>
              <li><strong>Responsive Reflow:</strong> Content reflows seamlessly up to 400% zoom without horizontal scrolling or loss of information.</li>
            </ul>
          </div>

          <div class="card" style="background:var(--surface-soft); padding:1.25rem;">
            <h3 style="margin-top:0; color:var(--accent);">B. Operable</h3>
            <ul style="margin-bottom:0; font-size:0.92rem;">
              <li><strong>Keyboard Navigation:</strong> All navigation menus, search triggers, code copy actions, and theme toggles are 100% operable via keyboard.</li>
              <li><strong>Focus Management:</strong> Clear, high-visibility focus indicators with zero keyboard traps across modal dialogs.</li>
              <li><strong>Bypass Blocks:</strong> A visible "Skip to main content" link is available as the first focusable element on every page.</li>
            </ul>
          </div>

          <div class="card" style="background:var(--surface-soft); padding:1.25rem;">
            <h3 style="margin-top:0; color:var(--accent);">C. Understandable</h3>
            <ul style="margin-bottom:0; font-size:0.92rem;">
              <li><strong>Predictable Layout:</strong> Symmetrical navigation, consistent page hierarchy, and standard landmark placement across all pages.</li>
              <li><strong>Clear Language:</strong> Technical audio concepts and API specifications are clearly structured with semantic HTML5 elements.</li>
              <li><strong>Error Prevention:</strong> Support and feedback forms provide clear field labels, explicit requirements, and error messages.</li>
            </ul>
          </div>

          <div class="card" style="background:var(--surface-soft); padding:1.25rem;">
            <h3 style="margin-top:0; color:var(--accent);">D. Robust</h3>
            <ul style="margin-bottom:0; font-size:0.92rem;">
              <li><strong>Assistive Tech Compatibility:</strong> Tested with screen readers including Apple VoiceOver, NVDA, and JAWS.</li>
              <li><strong>Semantic Markup:</strong> Valid HTML5 elements with appropriate WAI-ARIA roles, states, and properties.</li>
              <li><strong>Progressive Enhancement:</strong> Core documentation and navigation remain fully accessible even if JavaScript is disabled.</li>
            </ul>
          </div>
        </div>
      </article>

      <!-- 3. Assessment & Continuous Testing -->
      <article class="card stack" style="padding:var(--gap);">
        <h2>3. Assessment &amp; Testing Methodology</h2>
        <div class="prose">
          <p>Audio Analyser assesses accessibility through a multi-layered evaluation procedure:</p>
          <ul>
            <li><strong>Automated CI Testing:</strong> Automated audits using Google Lighthouse and axe-core integrated into the continuous deployment pipeline with a target of 100/100 accessibility.</li>
            <li><strong>Manual Keyboard Audits:</strong> Comprehensive manual testing navigating exclusively via Tab, Shift+Tab, Enter, Space, and Arrow keys.</li>
            <li><strong>Assistive Device Testing:</strong> Real-world screen reader testing on macOS VoiceOver (Safari/Chrome) and Windows NVDA (Firefox/Edge).</li>
            <li><strong>Color Contrast Analysis:</strong> Automated and manual verification of all CSS color tokens across Light and Dark modes.</li>
          </ul>
        </div>
      </article>

      <!-- 4. Feedback & Contact -->
      <article class="card stack" style="padding:var(--gap);">
        <h2>4. Feedback &amp; Contact Information</h2>
        <div class="prose">
          <p>We welcome your feedback on the accessibility of Audio Analyser. If you encounter accessibility barriers or require documentation in an alternative format, please contact us:</p>
          <ul>
            <li><strong>Developer Inquiries:</strong> Use our <a href="/contact/index.html">Contact Form</a>.</li>
            <li><strong>GitHub Issue Tracker:</strong> Submit an issue on <a href="https://github.com/sebastienrousseau/audioanalyser.github.io/issues" target="_blank" rel="noopener">GitHub Issues</a> with the tag <code>accessibility</code>.</li>
            <li><strong>Response Target:</strong> We aim to acknowledge accessibility feedback within 2 business days and implement resolutions promptly.</li>
          </ul>
          <p style="font-size:0.88rem; color:var(--ink-muted); margin-top:1.5rem;">This statement was created on 31 August 2024 and last reviewed on 31 August 2026.</p>
        </div>
      </article>
    </div>
  </div>
</section>