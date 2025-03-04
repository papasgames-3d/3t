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
  
  // Đặt crossorigin="anonymous" cho tất cả các script từ domain khác
  if (url.includes('//') && !url.includes(window.location.hostname)) {
    link.setAttribute('crossorigin', 'anonymous');
  }
  return link;
};

// Tránh các lỗi GPT bằng cách xác định các slot đã tồn tại
const preventGPTErrors = () => {
  // Kiểm tra nếu đã tồn tại googletag
  if (typeof window.googletag !== 'undefined') {
    const originalDefineSlot = window.googletag.defineSlot;
    
    // Ghi đè hàm defineSlot để kiểm tra trùng lặp
    window.googletag.defineSlot = function(...args) {
      try {
        const divId = args[1];
        // Kiểm tra xem div đã được định nghĩa slot chưa
        if (document.getElementById(divId) && document.getElementById(divId).getAttribute('data-slot-defined') === 'true') {
          console.log(`Slot for ${divId} already defined, skipping.`);
          return {
            addService: function() { return this; },
            defineSizeMapping: function() { return this; },
            setTargeting: function() { return this; }
          };
        }
        
        // Đánh dấu div đã được định nghĩa
        const div = document.getElementById(divId);
        if (div) {
          div.setAttribute('data-slot-defined', 'true');
        }
        
        // Gọi hàm gốc
        return originalDefineSlot.apply(window.googletag, args);
      } catch (e) {
        console.error('Error in defineSlot:', e);
        // Trả về đối tượng giả để tránh lỗi null
        return {
          addService: function() { return this; },
          defineSizeMapping: function() { return this; },
          setTargeting: function() { return this; }
        };
      }
    };
  }
};

// Tải script wgplayer với cách tốt hơn
const loadWgPlayerScript = () => {
  try {
    // Nếu script đã được tải, không làm gì cả
    if (document.querySelector('script[src*="universal.wgplayer.com"]')) {
      console.log('WGPlayer script already loaded');
      return;
    }

    // Tạo script để xử lý lỗi CORS
    const corsHelperScript = document.createElement('script');
    corsHelperScript.textContent = `
      // Khi nhận được lỗi CORS, thiết lập lại cách tải
      window.addEventListener('error', function(e) {
        if (e.message && e.message.includes('CORS')) {
          console.warn('CORS error detected, retrying with different approach...');
          
          // Thử phương pháp JSONP nếu có thể
          const scriptURL = e.target ? e.target.src : '';
          if (scriptURL && scriptURL.includes('universal.wgplayer.com')) {
            const script = document.createElement('script');
            script.async = true;
            script.src = scriptURL + '&callback=wgPlayerCallback';
            document.head.appendChild(script);
          }
        }
      }, true);
      
      // Callback cho JSONP
      window.wgPlayerCallback = function(data) {
        console.log('WGPlayer loaded via JSONP fallback');
      };
    `;
    document.head.appendChild(corsHelperScript);

    // Setup GPT error handling
    preventGPTErrors();

    // Tạo preload link cho script chính
    const mainScriptUrl = `https://universal.wgplayer.com/tag/?lh=${window.location.hostname}&wp=${window.location.pathname}&ws=${window.location.search}`;
    const preloadLink = createPreloadLink(mainScriptUrl);
    document.head.appendChild(preloadLink);

    // Sau đó tải script thực tế
    setTimeout(() => {
      const script = document.createElement('script');
      script.async = true;
      script.src = mainScriptUrl;
      script.fetchPriority = 'high';
      script.setAttribute('crossorigin', 'anonymous');
      script.onerror = function(e) {
        console.warn('Error loading WGPlayer script, trying alternative method...');
      };
      document.head.appendChild(script);
      console.log('WGPlayer script loading started');
    }, 100);
  } catch (error) {
    console.error('Error loading WGPlayer script:', error);
  }
};

// Tự động tải script khi trang đã tải xong
document.addEventListener('DOMContentLoaded', () => {
  try {
    loadWgPlayerScript();
  } catch (error) {
    console.error('Error in DOMContentLoaded handler:', error);
  }
});

// Export các function cho sử dụng từ bên ngoài
window.adLoader = {
  loadWgPlayerScript,
  isWgPlayerLoaded,
  preventGPTErrors
}; 