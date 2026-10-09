
(function() {
  // 1. Theme Switcher Engine (Light / Dark / System)
  const storedTheme = localStorage.getItem('theme-mode') || 'system';
  function applyTheme(mode) {
    if (mode === 'system') {
      const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.documentElement.setAttribute('data-theme-mode', isDark ? 'dark' : 'light');
    } else {
      document.documentElement.setAttribute('data-theme-mode', mode);
    }
    localStorage.setItem('theme-mode', mode);
    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-theme-mode') === mode);
    });
  }
  
  applyTheme(storedTheme);
  
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if ((localStorage.getItem('theme-mode') || 'system') === 'system') {
      applyTheme('system');
    }
  });

  document.addEventListener('DOMContentLoaded', () => {
    applyTheme(localStorage.getItem('theme-mode') || 'system');
    document.querySelectorAll('.theme-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.getAttribute('data-theme-mode');
        applyTheme(mode);
      });
    });

    // 2. Search Modal & Engine
    let searchIndex = null;
    const modal = document.getElementById('searchModal');
    const input = document.getElementById('searchInput');
    const results = document.getElementById('searchResults');
    const trigger = document.getElementById('searchTrigger');
    const closeBtn = document.getElementById('searchClose');

    async function loadSearch() {
      if (!searchIndex) {
        try {
          const res = await fetch('/search-index.json');
          if (res.ok) searchIndex = await res.json();
        } catch (e) {
          searchIndex = [];
        }
      }
    }

    function openSearch() {
      if (!modal) return;
      modal.style.display = 'flex';
      loadSearch();
      setTimeout(() => input && input.focus(), 50);
    }

    function closeSearch() {
      if (!modal) return;
      modal.style.display = 'none';
      if (input) input.value = '';
      if (results) results.innerHTML = '<div class="search-empty">Type to search...</div>';
    }

    if (trigger) trigger.addEventListener('click', openSearch);
    if (closeBtn) closeBtn.addEventListener('click', closeSearch);
    if (modal) {
      modal.querySelector('.search-backdrop').addEventListener('click', closeSearch);
    }

    window.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        openSearch();
      } else if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
        closeSearch();
      }
    });

    if (input) {
      input.addEventListener('input', () => {
        const query = input.value.trim().toLowerCase();
        if (!query || !searchIndex || searchIndex.length === 0) {
          results.innerHTML = '<div class="search-empty">Type to search...</div>';
          return;
        }
        const matches = searchIndex.filter(item => 
          (item.title && item.title.toLowerCase().includes(query)) ||
          (item.description && item.description.toLowerCase().includes(query)) ||
          (item.content && item.content.toLowerCase().includes(query))
        ).slice(0, 8);

        if (matches.length === 0) {
          results.innerHTML = '<div class="search-empty">No results found for "' + query + '"</div>';
          return;
        }

        results.innerHTML = matches.map(item => `
          <a class="search-item" href="${item.url}">
            <div class="search-item-title">${item.title}</div>
            <div class="search-item-desc">${item.description || item.content || ''}</div>
          </a>
        `).join('');
      });
    }
  });
})();
