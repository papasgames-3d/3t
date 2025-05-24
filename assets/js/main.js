// Menu functionality
class MenuManager {
  constructor() {
    this.menuToggle = document.getElementById('menu-toggle');
    this.sidebar = document.getElementById('sidebar');
    this.menuOverlay = document.getElementById('menuOverlay') || document.getElementById('menu-overlay');
    this.init();
  }

  init() {
    this.setupMenuToggle();
    this.setupOverlayClick();
    this.setupMenuItemsClick();
    this.setupEscapeKey();
  }

  toggleMenu() {
    this.sidebar.classList.toggle('active');
    if (this.menuOverlay) {
      this.menuOverlay.classList.toggle('active');
    }
    this.toggleIcon();
  }

  toggleIcon() {
    const icon = this.menuToggle.querySelector('i');
    icon.classList.toggle('fa-bars');
    icon.classList.toggle('fa-times');
  }

  setupMenuToggle() {
    if (this.menuToggle) {
      this.menuToggle.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleMenu();
      });
    }
  }

  setupOverlayClick() {
    if (this.menuOverlay) {
      this.menuOverlay.addEventListener('click', () => this.toggleMenu());
    }
  }

  setupMenuItemsClick() {
    const menuItems = document.querySelectorAll('.sidebar-menu a, .sidebar-categories li');
    menuItems.forEach(item => {
      item.addEventListener('click', () => {
        if (window.innerWidth <= 768 && this.sidebar.classList.contains('active')) {
          this.toggleMenu();
        }
      });
    });
  }

  setupEscapeKey() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.sidebar.classList.contains('active')) {
        this.toggleMenu();
      }
    });
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

// Initialize all managers when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new MenuManager();
  new AdManager();
  new SearchManager();
}); 