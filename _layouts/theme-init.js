/*!
 * Runs before first paint (loaded synchronously in <head>) so the stored
 * theme is applied without a flash of the wrong palette.
 *
 * Only an explicit user choice is stamped onto <html>. When no choice has
 * been stored the attribute is deliberately left off, so the stylesheet's
 * `prefers-color-scheme` block decides and the page follows the OS.
 */
(function () {
  var root = document.documentElement;
  root.classList.remove('no-js');
  try {
    var saved = localStorage.getItem('theme');
    if (saved === 'dark' || saved === 'light') {
      root.setAttribute('data-theme', saved);
    }
  } catch (e) {
    /* Private browsing or blocked storage: fall back to the OS preference. */
  }
})();
