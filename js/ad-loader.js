/**
 * Ad Loader - Handles advertising script loading
 * Fixes preload issues with wgplayer.com scripts
 */

// Kiểm tra nếu script wgplayer đã được tải
const isWgPlayerLoaded = () => {
  // Kiểm tra biến toàn cục wgPlayer
  if (typeof window.wgPlayer !== 'undefined') {
    return true;
  }
  
  // Kiểm tra nếu script đã được nhúng trong trang
  if (document.querySelector('script[src*="universal.wgplayer.com"]')) {
    return true;
  }
  
  // Kiểm tra nếu script đang trong quá trình tải
  if (document.querySelector('link[rel="preload"][href*="universal.wgplayer.com"]')) {
    return true;
  }
  
  return false;
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
    // Nếu đã ghi đè defineSlot rồi thì không làm lại
    if (window.googletag._defineSlotOverriden) {
      return;
    }
    
    const originalDefineSlot = window.googletag.defineSlot;
    window.googletag._defineSlotOverriden = true;
    
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
    // Kiểm tra kỹ hơn nếu script đã được tải
    if (isWgPlayerLoaded()) {
      console.log('WGPlayer script already loaded or loading, skipping duplicate load');
      return;
    }

    // Đánh dấu là đang tải để tránh tải trùng lặp
    window._wgPlayerLoading = true;

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
      // Kiểm tra lại trước khi tải
      if (isWgPlayerLoaded()) {
        console.log('WGPlayer script detected before loading, aborting duplicate load');
        return;
      }
      
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

// Chỉ tải script khi trang đã tải xong và script chưa tồn tại
document.addEventListener('DOMContentLoaded', () => {
  // Đảm bảo GPT errors ngăn chặn luôn được áp dụng
  try {
    preventGPTErrors();
  } catch (error) {
    console.error('Error preventing GPT errors:', error);
  }
  
  // Chỉ tải WGPlayer nếu chưa tồn tại
  try {
    if (!isWgPlayerLoaded()) {
      loadWgPlayerScript();
    } else {
      console.log('WGPlayer already exists in page, skipping loader');
    }
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