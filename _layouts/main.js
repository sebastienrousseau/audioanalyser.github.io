'use strict';

// 1. Theme Engine
(function() {
  var storedTheme = localStorage.getItem('theme-mode') || 'system';

  function applyTheme(mode) {
    var effectiveTheme = mode;
    if (mode === 'system') {
      var isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      effectiveTheme = isDark ? 'dark' : 'light';
    }
    document.documentElement.setAttribute('data-theme-mode', mode);
    document.documentElement.setAttribute('data-theme', effectiveTheme);
    localStorage.setItem('theme-mode', mode);

    var buttons = document.querySelectorAll('.theme-btn');
    buttons.forEach(function(btn) {
      if (btn.getAttribute('data-theme-mode') === mode) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  // Apply immediately
  applyTheme(storedTheme);

  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function() {
      if ((localStorage.getItem('theme-mode') || 'system') === 'system') {
        applyTheme('system');
      }
    });
  }

  function initApp() {
    applyTheme(localStorage.getItem('theme-mode') || 'system');

    // Attach theme toggle buttons
    var themeButtons = document.querySelectorAll('.theme-btn');
    themeButtons.forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        var mode = btn.getAttribute('data-theme-mode');
        if (mode) applyTheme(mode);
      });
    });

    // Mobile Navbar toggle
    var navToggle = document.getElementById('navbarToggle');
    var navMenu = document.getElementById('navbarMenu');
    if (navToggle && navMenu) {
      navToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        var isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
        navToggle.setAttribute('aria-expanded', !isExpanded);
        navMenu.classList.toggle('show');
      });
    }

    // FAQ Expand / Collapse All Engine
    var toggleBtn = document.getElementById('toggleAllBtn');
    var toggleText = document.getElementById('toggleAllText');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        var allDetails = document.querySelectorAll('.apple-faq-list-exact details, .apple-faq-accordion details, details.apple-faq-item');
        if (!allDetails.length) return;
        var allOpen = Array.from(allDetails).every(function(d) { return d.open; });
        var nextState = !allOpen;
        allDetails.forEach(function(d) { d.open = nextState; });
        if (toggleText) toggleText.textContent = nextState ? 'Collapse all' : 'Expand all';
        toggleBtn.setAttribute('aria-expanded', String(nextState));
        var icon = toggleBtn.querySelector('svg');
        if (icon) {
          icon.style.transform = nextState ? 'rotate(180deg)' : 'rotate(0deg)';
          icon.style.transition = 'transform 0.25s ease';
        }
      });

      document.querySelectorAll('.apple-faq-list-exact details, .apple-faq-accordion details, details.apple-faq-item').forEach(function(detail) {
        detail.addEventListener('toggle', function() {
          var allDetails = document.querySelectorAll('.apple-faq-list-exact details, .apple-faq-accordion details, details.apple-faq-item');
          var allOpen = Array.from(allDetails).every(function(d) { return d.open; });
          if (toggleText) toggleText.textContent = allOpen ? 'Collapse all' : 'Expand all';
          toggleBtn.setAttribute('aria-expanded', String(allOpen));
          var icon = toggleBtn.querySelector('svg');
          if (icon) {
            icon.style.transform = allOpen ? 'rotate(180deg)' : 'rotate(0deg)';
          }
        });
      });
    }

    // Search Engine Modal
    var searchIndex = null;
    var isFetching = false;
    var modal = document.getElementById('searchModal');
    var input = document.getElementById('searchInput');
    var results = document.getElementById('searchResults');
    var closeBtn = document.getElementById('searchClose');

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    async function loadSearch() {
      if (searchIndex || isFetching) return;
      isFetching = true;
      try {
        var res = await fetch('/search-index.json');
        if (res.ok) {
          var data = await res.json();
          searchIndex = Array.isArray(data) ? data : (data.entries || []);
        } else {
          searchIndex = [];
        }
      } catch (e) {
        searchIndex = [];
      } finally {
        isFetching = false;
      }
    }

    function openSearch() {
      if (!modal) return;
      modal.classList.add('active');
      loadSearch();
      setTimeout(function() {
        if (input) {
          input.focus();
          if (input.value.trim()) {
            input.dispatchEvent(new Event('input'));
          }
        }
      }, 50);
    }

    function closeSearch() {
      if (!modal) return;
      modal.classList.remove('active');
      if (input) input.value = '';
      if (results) results.innerHTML = '<div class="search-empty">Type to search...</div>';
    }

    var triggers = document.querySelectorAll('#searchTrigger, #searchTriggerMobile, .search-trigger');
    triggers.forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        openSearch();
      });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeSearch);
    if (modal) {
      var backdrop = modal.querySelector('.search-backdrop');
      if (backdrop) backdrop.addEventListener('click', closeSearch);
    }

    window.addEventListener('keydown', function(e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        openSearch();
      } else if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
        closeSearch();
      }
    });

    if (input) {
      input.addEventListener('input', function() {
        var query = input.value.trim().toLowerCase();
        if (!query) {
          results.innerHTML = '<div class="search-empty">Type to search...</div>';
          return;
        }
        if (!searchIndex) {
          results.innerHTML = '<div class="search-empty">Loading search index...</div>';
          loadSearch().then(function() {
            input.dispatchEvent(new Event('input'));
          });
          return;
        }
        if (searchIndex.length === 0) {
          results.innerHTML = '<div class="search-empty">No results found for "' + escapeHtml(query) + '"</div>';
          return;
        }
        var tokens = query.split(/\s+/).filter(Boolean);
        var matches = searchIndex.filter(function(item) {
          var t = (item.title || '').toLowerCase();
          var d = (item.description || '').toLowerCase();
          var c = (item.content || '').toLowerCase();
          var u = (item.url || '').toLowerCase();
          var target = t + ' ' + d + ' ' + c + ' ' + u;
          return tokens.every(function(tok) { return target.includes(tok); });
        }).slice(0, 10);

        if (matches.length === 0) {
          results.innerHTML = '<div class="search-empty">No results found for "' + escapeHtml(query) + '"</div>';
          return;
        }
        results.innerHTML = matches.map(function(item) {
          return '<a class="search-item" href="' + item.url + '">' +
            '<div class="search-item-title">' + escapeHtml(item.title) + '</div>' +
            '<div class="search-item-desc">' + escapeHtml((item.description || item.content || '').replace(/<[^>]+>/g, '').slice(0, 140)) + '...</div>' +
          '</a>';
        }).join('');
      });
    }

            // 5. Photo Lightbox Modal Engine
    var lightboxModal = document.getElementById('photoLightboxModal');
    if (!lightboxModal) {
      lightboxModal = document.createElement('div');
      lightboxModal.id = 'photoLightboxModal';
      lightboxModal.className = 'photo-lightbox-modal';
      lightboxModal.setAttribute('role', 'dialog');
      lightboxModal.setAttribute('aria-modal', 'true');
      lightboxModal.setAttribute('aria-label', 'Photo Preview');
      lightboxModal.innerHTML = '<div class="photo-lightbox-backdrop"></div>' +
        '<div class="photo-lightbox-content">' +
        '  <div class="photo-lightbox-media-wrap">' +
        '    <button type="button" class="photo-lightbox-close" aria-label="Close photo preview">✕</button>' +
        '    <img src="" alt="" class="photo-lightbox-img" id="lightboxImg" />' +
        '  </div>' +
        '  <div class="photo-lightbox-caption" id="lightboxCaption"></div>' +
        '</div>';
      document.body.appendChild(lightboxModal);
    }

    var lightboxImg = document.getElementById('lightboxImg');
    var lightboxCaption = document.getElementById('lightboxCaption');
    var lightboxClose = lightboxModal.querySelector('.photo-lightbox-close');
    var lightboxBackdrop = lightboxModal.querySelector('.photo-lightbox-backdrop');

    function openLightbox(src, alt) {
      if (!lightboxImg) return;
      lightboxImg.src = src;
      lightboxImg.alt = alt || 'Photo Preview';
      if (lightboxCaption) lightboxCaption.textContent = alt || '';
      lightboxModal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      if (!lightboxModal) return;
      lightboxModal.classList.remove('active');
      if (lightboxImg) lightboxImg.src = '';
      document.body.style.overflow = '';
    }

    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    if (lightboxBackdrop) lightboxBackdrop.addEventListener('click', closeLightbox);

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && lightboxModal && lightboxModal.classList.contains('active')) {
        closeLightbox();
      }
    });

    document.addEventListener('click', function(e) {
      var photoTarget = e.target.closest('.photo-card, .photo-img-wrapper, .gallery-card, .gallery-img-wrapper, figure');
      if (photoTarget) {
        var img = photoTarget.querySelector('img');
        if (img && img.src) {
          e.preventDefault();
          openLightbox(img.src, img.alt);
        }
      }
    });
    }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
})();
