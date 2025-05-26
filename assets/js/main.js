// Menu functionality
class MenuManager {
  constructor() {
    this.menuToggle = document.getElementById('menu-toggle');
    this.sidebar = document.getElementById('sidebar');
    this.menuOverlay = document.createElement('div');
    this.menuOverlay.id = 'menu-overlay';
    this.menuOverlay.className = 'menu-overlay';
    document.body.appendChild(this.menuOverlay);
    this.init();
  }

  init() {
    if (!this.menuToggle || !this.sidebar) {
      console.warn('Menu elements not found');
      return;
    }
    this.setupMenuToggle();
    this.setupOverlayClick();
    this.setupMenuItemsClick();
    this.setupEscapeKey();
    this.setupResizeHandler();
    this.setupTouchEvents();
  }

  toggleMenu(force = null) {
    const isActive = force !== null ? force : !this.sidebar.classList.contains('active');
    
    // Add/remove classes
    this.sidebar.classList.toggle('active', isActive);
    this.menuOverlay.classList.toggle('active', isActive);
    document.body.classList.toggle('menu-open', isActive);
    
    // Toggle icon
    const icon = this.menuToggle.querySelector('i');
    if (icon) {
      icon.className = isActive ? 'fas fa-times' : 'fas fa-bars';
    }

    // Prevent body scroll when menu is open
    if (isActive) {
      document.body.style.top = `-${window.scrollY}px`;
      document.body.style.position = 'fixed';
      document.body.style.width = '100%';
    } else {
      const scrollY = document.body.style.top;
      document.body.style.position = '';
      document.body.style.top = '';
      document.body.style.width = '';
      window.scrollTo(0, parseInt(scrollY || '0') * -1);
    }
  }

  setupMenuToggle() {
    this.menuToggle.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.toggleMenu();
    }, { passive: false });

    // Add touch event handling
    this.menuToggle.addEventListener('touchstart', (e) => {
      e.preventDefault();
      this.toggleMenu();
    }, { passive: false });
  }

  setupOverlayClick() {
    this.menuOverlay.addEventListener('click', (e) => {
      e.preventDefault();
      this.toggleMenu(false);
    });

    this.menuOverlay.addEventListener('touchstart', (e) => {
      e.preventDefault();
      this.toggleMenu(false);
    }, { passive: false });
  }

  setupMenuItemsClick() {
    const menuItems = document.querySelectorAll('.sidebar-menu a, .sidebar-categories li');
    menuItems.forEach(item => {
      item.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          this.toggleMenu(false);
        }
      });
    });
  }

  setupEscapeKey() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.sidebar.classList.contains('active')) {
        this.toggleMenu(false);
      }
    });
  }

  setupResizeHandler() {
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        if (window.innerWidth > 768) {
          this.toggleMenu(false);
        }
      }, 100);
    });
  }

  setupTouchEvents() {
    let touchStartX = 0;
    let touchEndX = 0;
    
    document.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });

    document.addEventListener('touchmove', (e) => {
      if (this.sidebar.classList.contains('active')) {
        e.preventDefault();
      }
    }, { passive: false });

    document.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].clientX;
      const swipeDistance = touchEndX - touchStartX;
      
      // Left swipe
      if (swipeDistance < -50 && this.sidebar.classList.contains('active')) {
        this.toggleMenu(false);
      }
      // Right swipe near left edge
      else if (swipeDistance > 50 && touchStartX < 30 && !this.sidebar.classList.contains('active')) {
        this.toggleMenu(true);
      }
    }, { passive: true });
  }
}

// Game functionality
class GameManager {
  constructor() {
    this.init();
  }

  init() {
    this.setupPlayButtons();
    this.setupFramePlayButton();
  }

  setupPlayButtons() {
    const gameItems = document.querySelectorAll('.game-item');
    gameItems.forEach(item => {
      const playButton = item.querySelector('.play-button');
      if (playButton) {
        playButton.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          
          // Get the href from parent anchor tag
          const gameUrl = item.getAttribute('href');
          if (gameUrl) {
            window.location.href = gameUrl;
          }
        });
      }
    });
  }

  setupFramePlayButton() {
    const playButton = document.getElementById('playGameButton');
    const gameFrame = document.getElementById('game-frame');
    const thumbnail = document.querySelector('.game-thumbnail');
    
    if (playButton && gameFrame && thumbnail) {
      playButton.addEventListener('click', () => {
        // Hide thumbnail and show iframe
        thumbnail.style.display = 'none';
        gameFrame.style.display = 'block';
        
        // Focus on the game frame
        gameFrame.focus();
      });
    }
  }
}

// Ad performance optimization
class AdManager {
  constructor() {
    this.connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    this.init();
  }

  init() {
    this.checkConnection();
    this.optimizeAdLoading();
  }

  checkConnection() {
    if (this.connection && this.isSlowConnection()) {
      this.reduceAds();
    }
  }

  isSlowConnection() {
    return this.connection.effectiveType === '2g' || this.connection.effectiveType === 'slow-2g';
  }

  reduceAds() {
    const adContainers = document.querySelectorAll('.ad-container');
    adContainers.forEach((container, index) => {
      if (index > 0) container.style.display = 'none';
    });
  }

  optimizeAdLoading() {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(() => {
        const adScripts = document.querySelectorAll('.ad-container script');
        adScripts.forEach(script => {
          const parent = script.parentNode;
          const newScript = document.createElement('script');
          newScript.textContent = script.textContent;
          parent.removeChild(script);
          setTimeout(() => parent.appendChild(newScript), 100);
        });
      }, 1000);
    });
  }
}

// Search functionality
class SearchManager {
  constructor() {
    this.searchInput = document.getElementById('game-search');
    this.gameItems = document.querySelectorAll('.game-item');
    this.init();
  }

  init() {
    if (this.searchInput) {
      this.setupSearch();
    }
  }

  setupSearch() {
    this.searchInput.addEventListener('input', () => {
      const searchTerm = this.searchInput.value.toLowerCase().trim();
      this.filterGames(searchTerm);
    });
  }

  filterGames(searchTerm) {
    this.gameItems.forEach(item => {
      const gameName = item.querySelector('span').textContent.toLowerCase();
      item.style.display = gameName.includes(searchTerm) || searchTerm === '' ? '' : 'none';
    });
  }
}

// Initialize managers
document.addEventListener('DOMContentLoaded', () => {
  new MenuManager();
  new GameManager();
  new AdManager();
  new SearchManager();
}); 