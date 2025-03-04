/**
 * Ad Loader - Handles advertising script loading
 * Fixes preload issues with wgplayer.com scripts
 */

// Kiểm tra nếu script wgplayer đã được tải
const isWgPlayerLoaded = () => {
  return typeof window.wgPlayer !== 'undefined';
};

// Tạo preload link với thuộc tính as phù hợp
const createPreloadLink = (url, as = 'script') => {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.href = url;
  link.as = as;
  link.crossOrigin = 'anonymous';
  return link;
};

// Tải script wgplayer với cách tốt hơn
const loadWgPlayerScript = () => {
  // Nếu script đã được tải, không làm gì cả
  if (document.querySelector('script[src*="universal.wgplayer.com"]')) {
    return;
  }

  // Tạo preload link cho script chính
  const mainScriptUrl = `https://universal.wgplayer.com/tag/?lh=${window.location.hostname}&wp=${window.location.pathname}&ws=${window.location.search}`;
  const preloadLink = createPreloadLink(mainScriptUrl);
  document.head.appendChild(preloadLink);

  // Tạo preload link cho file config với as="script"
  const configUrl = "https://afg.wgplayer.com/monkeymart.one/wgAds.mobile.conf.js";
  const configPreloadLink = createPreloadLink(configUrl);
  document.head.appendChild(configPreloadLink);

  // Sau đó tải script thực tế
  setTimeout(() => {
    const script = document.createElement('script');
    script.async = true;
    script.src = mainScriptUrl;
    script.fetchPriority = 'high';
    document.head.appendChild(script);
  }, 100);
};

// Tự động tải script khi trang đã tải xong
document.addEventListener('DOMContentLoaded', () => {
  loadWgPlayerScript();
});

// Export các function cho sử dụng từ bên ngoài
window.adLoader = {
  loadWgPlayerScript,
  isWgPlayerLoaded
}; 