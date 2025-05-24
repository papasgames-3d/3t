// Google Analytics
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-54L5E2NJ3K');

// WGPlayer Universal Tag
!function(e,t){
  a=e.createElement("script"),
  m=e.getElementsByTagName("script")[0],
  a.async=1,
  a.src=t,
  a.fetchPriority='high',
  m.parentNode.insertBefore(a,m)
}(document,"https://universal.wgplayer.com/tag/?lh="+window.location.hostname+"&wp="+window.location.pathname+"&ws="+window.location.search);

// Google AdSense
(adsbygoogle = window.adsbygoogle || []).push({});

// Google Analytics Event Tracking
function trackEvent(category, action, label = null, value = null) {
  if (typeof gtag !== 'undefined') {
    const eventParams = {
      event_category: category,
      event_action: action
    };
    
    if (label) eventParams.event_label = label;
    if (value) eventParams.value = value;
    
    gtag('event', action, eventParams);
  }
}

// Track page views
function trackPageView(path, title) {
  if (typeof gtag !== 'undefined') {
    gtag('config', 'G-54L5E2NJ3K', {
      page_path: path,
      page_title: title
    });
  }
}

// Track game interactions
function trackGameInteraction(gameId, action) {
  trackEvent('Game', action, gameId);
}

// Track ad impressions
function trackAdImpression(adUnit) {
  trackEvent('Advertisement', 'Impression', adUnit);
}

// Track ad clicks
function trackAdClick(adUnit) {
  trackEvent('Advertisement', 'Click', adUnit);
}

// Track social shares
function trackSocialShare(platform, gameId) {
  trackEvent('Social', 'Share', platform, gameId);
}

// Initialize tracking on page load
document.addEventListener('DOMContentLoaded', function() {
  // Track initial page view
  trackPageView(window.location.pathname, document.title);
  
  // Track game frame interactions
  const gameFrame = document.getElementById('game-frame');
  if (gameFrame) {
    const gameId = gameFrame.getAttribute('data-game-id') || 'monkey-mart';
    trackGameInteraction(gameId, 'Load');
    
    // Track fullscreen
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    if (fullscreenBtn) {
      fullscreenBtn.addEventListener('click', () => {
        trackGameInteraction(gameId, 'Fullscreen');
      });
    }
    
    // Track sharing
    const shareBtn = document.getElementById('share-btn');
    if (shareBtn) {
      shareBtn.addEventListener('click', () => {
        trackGameInteraction(gameId, 'Share Menu Open');
      });
    }
  }
  
  // Track ad containers
  const adContainers = document.querySelectorAll('.ad-container');
  adContainers.forEach((container, index) => {
    const adUnit = container.id || `ad-unit-${index}`;
    
    // Use Intersection Observer to track ad impressions
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          trackAdImpression(adUnit);
          observer.unobserve(entry.target);
        }
      });
    });
    
    observer.observe(container);
  });
}); 