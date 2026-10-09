// Audio Analyser Main JavaScript Engine
"use strict";

(function() {
  // 1. Theme Engine
  function applyTheme(mode) {
    if (mode === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    localStorage.setItem("theme-mode", mode);
    var toggle = document.getElementById("themeToggle");
    if (toggle) {
      toggle.setAttribute("aria-pressed", mode === "dark" ? "true" : "false");
    }
  }

  var savedTheme = localStorage.getItem("theme-mode");
  if (!savedTheme) {
    savedTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  applyTheme(savedTheme);

  document.addEventListener("DOMContentLoaded", function() {
    var themeToggle = document.getElementById("themeToggle");
    if (themeToggle) {
      themeToggle.addEventListener("click", function() {
        var isDark = document.documentElement.getAttribute("data-theme") === "dark";
        applyTheme(isDark ? "light" : "dark");
      });
    }

    // 2. Mobile Nav Toggle
    var navToggle = document.getElementById("navToggle");
    var navMenu = document.getElementById("navMenu");
    if (navToggle && navMenu) {
      navToggle.addEventListener("click", function() {
        var isOpen = navToggle.getAttribute("aria-expanded") === "true";
        var nextState = !isOpen;
        navToggle.setAttribute("aria-expanded", String(nextState));
        navMenu.setAttribute("data-open", String(nextState));
        navMenu.classList.toggle("open", nextState);
        navMenu.classList.toggle("active", nextState);
      });

      var navLinks = navMenu.querySelectorAll(".nav-link");
      navLinks.forEach(function(link) {
        link.addEventListener("click", function() {
          navToggle.setAttribute("aria-expanded", "false");
          navMenu.setAttribute("data-open", "false");
          navMenu.classList.remove("open", "active");
        });
      });
    }

    // 3. Intelligent Search Engine
    var searchIndex = [
    {
        "title": "Audio Analyser Overview",
        "desc": "Real-time acoustic analysis, Fast Fourier Transform (FFT), sub-5ms DSP latency, WebAudio streaming, and speech intelligence.",
        "keywords": "audio analyser home overview fast fourier transform fft dsp digital signal processing webaudio speech to text stt acoustic intelligence latency pcm",
        "url": "/"
    },
    {
        "title": "Real-Time Spectral FFT & Frequency Analysis",
        "desc": "Sub-5ms Fast Fourier Transform (FFT), Mel-frequency filterbanks (MFCCs), spectral centroid, zero-crossing rate, and spectrograms.",
        "keywords": "fast fourier transform fft spectral analysis spectrogram frequency domain mfcc mel frequency cepstral coefficients pitch detection audio dsp",
        "url": "/features/index.html#spectral-fft"
    },
    {
        "title": "Automated Speech-to-Text & Diarization",
        "desc": "Speech recognition (STT), multi-speaker diarization, punctuation normalization, and time-aligned transcription across 60+ languages.",
        "keywords": "speech to text stt speech recognition diarization transcription speaker separation translation languages audio transcribe",
        "url": "/features/index.html#speech-to-text"
    },
    {
        "title": "Conversational Sentiment & Tone Detection",
        "desc": "Acoustic prosody metrics, pitch variation, linguistic tone scoring, key entity extraction, and automated summary reports.",
        "keywords": "sentiment analysis tone detection acoustic prosody emotions intent summary reports speech intelligence recommendations",
        "url": "/features/index.html#sentiment-tone"
    },
    {
        "title": "DSP Architecture & System Ecosystem",
        "desc": "Technical pipeline spanning audio ingestion, Rust DSP transformation, and Python AI inference engines.",
        "keywords": "system architecture pipeline rust python dsp audio processing webaudio engine diagram wasm webassembly microservices",
        "url": "/about/index.html"
    },
    {
        "title": "Documentation, SDK & Quick Start",
        "desc": "Installation via `pip install audioanalyser`, Python SDK usage examples, CLI terminal processing, and Docker containers.",
        "keywords": "documentation quickstart python sdk pypi pip cli command line docker api reference tutorial installation",
        "url": "/documentation/index.html"
    },
    {
        "title": "Developer Support & Community",
        "desc": "Open-source GitHub repository, issue tracker, developer support form, and enterprise deployment inquiries.",
        "keywords": "contact support developer help issue tracker bug report github repository enterprise community form",
        "url": "/contact/index.html"
    },
    {
        "title": "Made with Static Site Generator (SSG)",
        "desc": "Static Site Generator performance architecture, 100/100 Lighthouse metrics, sub-50ms TTFB, and zero tracking bloat.",
        "keywords": "made with ssg static site generator performance lighthouse speed fast security privacy rust ssg",
        "url": "/made-with-ssg/index.html"
    },
    {
        "title": "Accessibility Statement",
        "desc": "Commitment to digital inclusion, WCAG 2.2 Level AA and AAA compliance, high contrast, and screen reader support.",
        "keywords": "accessibility statement wcag 2.2 aa aaa screen reader keyboard contrast digital inclusion a11y",
        "url": "/accessibility/index.html"
    },
    {
        "title": "Privacy Policy",
        "desc": "Privacy-by-design standards, zero tracking cookies, and strict UK GDPR / EU GDPR data handling compliance.",
        "keywords": "privacy policy gdpr cookies zero tracking data protection security privacy",
        "url": "/privacy/index.html"
    },
    {
        "title": "Terms of Use",
        "desc": "Terms governing access, software use, and open-source dual Apache-2.0 and MIT licensing.",
        "keywords": "terms of use legal apache-2.0 mit license software conditions open source",
        "url": "/terms/index.html"
    }
];

    var searchModal = document.getElementById("searchModal");
    var searchTrigger = document.getElementById("searchTrigger");
    var searchClose = document.getElementById("searchClose");
    var searchInput = document.getElementById("searchInput");
    var searchResults = document.getElementById("searchResults");

    // Fetch latest search-index.json if available
    fetch("/search-index.json")
      .then(function(res) { return res.json(); })
      .then(function(data) { if (Array.isArray(data) && data.length) searchIndex = data; })
      .catch(function() {});

    function openSearch() {
      if (searchModal) {
        searchModal.style.display = "flex";
        searchModal.classList.add("active");
        if (searchInput) {
          searchInput.value = "";
          searchInput.focus();
          renderResults("");
        }
      }
    }

    function closeSearch() {
      if (searchModal) {
        searchModal.style.display = "none";
        searchModal.classList.remove("active");
      }
    }

    if (searchTrigger) searchTrigger.addEventListener("click", openSearch);
    if (searchClose) searchClose.addEventListener("click", closeSearch);
    if (searchModal) {
      var backdrop = searchModal.querySelector(".search-backdrop");
      if (backdrop) backdrop.addEventListener("click", closeSearch);
    }

    document.addEventListener("keydown", function(e) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        openSearch();
      }
      if (e.key === "Escape" && searchModal && searchModal.classList.contains("active")) {
        closeSearch();
      }
    });

    function escapeHtml(str) {
      return (str || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function renderResults(q) {
      if (!searchResults) return;
      var query = q.trim().toLowerCase();
      if (!query) {
        searchResults.innerHTML = '<div class="search-empty">Type to search Audio Analyser features, DSP, documentation...</div>';
        return;
      }

      var words = query.split(/\s+/).filter(function(w) { return w.length > 0; });

      var matches = searchIndex.filter(function(item) {
        var haystack = ((item.title || "") + " " + (item.desc || "") + " " + (item.keywords || "")).toLowerCase();
        // Return true if query as full phrase is present, or if all query words are present
        if (haystack.indexOf(query) !== -1) return true;
        return words.every(function(word) {
          return haystack.indexOf(word) !== -1;
        });
      });

      if (matches.length === 0) {
        searchResults.innerHTML = '<div class="search-empty">No results found for "<strong>' + escapeHtml(query) + '</strong>"</div>';
        return;
      }

      var html = "";
      matches.forEach(function(item) {
        html += '<a href="' + item.url + '" class="search-item">' +
          '<div class="search-item-title">' + escapeHtml(item.title) + '</div>' +
          '<div class="search-item-desc">' + escapeHtml(item.desc) + '</div>' +
          '</a>';
      });
      searchResults.innerHTML = html;
    }

    if (searchInput) {
      searchInput.addEventListener("input", function() {
        renderResults(searchInput.value);
      });
    }

    // 4. Photo Lightbox Modal Engine (On-Demand)
    var photoLightboxModal = null;
    function openLightbox(src, alt) {
      if (!photoLightboxModal) {
        photoLightboxModal = document.createElement("div");
        photoLightboxModal.id = "photoLightboxModal";
        photoLightboxModal.className = "photo-lightbox-modal";
        photoLightboxModal.setAttribute("role", "dialog");
        photoLightboxModal.setAttribute("aria-modal", "true");
        photoLightboxModal.innerHTML = '<div class="photo-lightbox-backdrop"></div>' +
          '<div class="photo-lightbox-content">' +
          '<button type="button" class="photo-lightbox-close" aria-label="Close image">✕</button>' +
          '<div class="photo-lightbox-media-wrap">' +
          '<img class="photo-lightbox-img" src="" alt="">' +
          '</div>' +
          '</div>';
        document.body.appendChild(photoLightboxModal);
        photoLightboxModal.querySelector(".photo-lightbox-close").addEventListener("click", closeLightbox);
        photoLightboxModal.querySelector(".photo-lightbox-backdrop").addEventListener("click", closeLightbox);
      }
      var img = photoLightboxModal.querySelector(".photo-lightbox-img");
      img.src = src;
      img.alt = alt || "Full size view";
      photoLightboxModal.style.display = "flex";
      photoLightboxModal.classList.add("active");
    }

    function closeLightbox() {
      if (photoLightboxModal) {
        photoLightboxModal.style.display = "none";
        photoLightboxModal.classList.remove("active");
      }
    }
  });

  // 5. Service Worker Lifecycle
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js", { scope: "./" }).then(function(reg) {
      reg.update();
    }).catch(function() {});
  }
})();
