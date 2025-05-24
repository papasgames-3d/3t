// App State Management
const AppState = {
  games: [],
  categories: [],
  currentCategory: null,
  searchTerm: '',
  isLoading: false,
  error: null
};

// UI Components
class UI {
  static elements = {
    menuToggle: document.getElementById('menuToggle'),
    searchInput: document.getElementById('searchInput'),
    featuredGames: document.getElementById('featuredGames'),
    newGames: document.getElementById('newGames'),
    heroGames: document.querySelector('.hero-games')
  };

  static init() {
    this.setupEventListeners();
    this.setupIntersectionObserver();
  }

  static setupEventListeners() {
    // Menu Toggle
    if (this.elements.menuToggle) {
      this.elements.menuToggle.addEventListener('click', () => {
        document.body.classList.toggle('menu-open');
      });
    }

    // Search Input
    if (this.elements.searchInput) {
      this.elements.searchInput.addEventListener('input', this.debounce((e) => {
        AppState.searchTerm = e.target.value.toLowerCase();
        GameManager.filterGames();
      }, 300));
    }

    // Close menu on click outside
    document.addEventListener('click', (e) => {
      if (document.body.classList.contains('menu-open') && 
          !e.target.closest('.main-nav') && 
          !e.target.closest('.menu-toggle')) {
        document.body.classList.remove('menu-open');
      }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  }

  static setupIntersectionObserver() {
    const options = {
      root: null,
      rootMargin: '20px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, options);

    // Observe game cards and category cards
    document.querySelectorAll('.game-card, .category-card').forEach(el => {
      observer.observe(el);
    });
  }

  static debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  static showLoading() {
    AppState.isLoading = true;
    // Add loading UI logic
  }

  static hideLoading() {
    AppState.isLoading = false;
    // Remove loading UI logic
  }

  static showError(message) {
    AppState.error = message;
    // Show error UI logic
  }
}

// Game Management
class GameManager {
  static async init() {
    try {
      UI.showLoading();
      await this.loadGames();
      this.renderGames();
      UI.hideLoading();
    } catch (error) {
      UI.showError('Failed to load games');
      console.error('Error initializing games:', error);
    }
  }

  static async loadGames() {
    // Simulate API call - Replace with actual API call
    AppState.games = [
      {
        id: 1,
        title: 'Zombie Tag',
        category: 'action',
        image: 'assets/img/games/zombie-tag.jpg',
        description: 'Survive in a world of zombies',
        featured: true,
        new: true
      },
      // Add more games...
    ];
  }

  static renderGames() {
    if (UI.elements.featuredGames) {
      const featured = AppState.games.filter(game => game.featured);
      UI.elements.featuredGames.innerHTML = this.createGameCards(featured);
    }

    if (UI.elements.newGames) {
      const newGames = AppState.games.filter(game => game.new);
      UI.elements.newGames.innerHTML = this.createGameCards(newGames);
    }

    if (UI.elements.heroGames) {
      const heroGames = AppState.games.filter(game => game.featured).slice(0, 3);
      UI.elements.heroGames.innerHTML = this.createHeroGameCards(heroGames);
    }
  }

  static createGameCards(games) {
    return games.map(game => `
      <div class="game-card">
        <img src="${game.image}" alt="${game.title}">
        <div class="game-card-content">
          <h3>${game.title}</h3>
          <p>${game.description}</p>
        </div>
      </div>
    `).join('');
  }

  static createHeroGameCards(games) {
    return games.map(game => `
      <div class="hero-game-card">
        <img src="${game.image}" alt="${game.title}">
        <h3>${game.title}</h3>
      </div>
    `).join('');
  }

  static filterGames() {
    const filtered = AppState.games.filter(game => {
      const matchesSearch = game.title.toLowerCase().includes(AppState.searchTerm);
      const matchesCategory = !AppState.currentCategory || game.category === AppState.currentCategory;
      return matchesSearch && matchesCategory;
    });

    this.renderGames(filtered);
  }
}

// Analytics
class Analytics {
  static init() {
    this.setupPageViewTracking();
    this.setupEventTracking();
  }

  static setupPageViewTracking() {
    // Track page views
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-54L5E2NJ3K');
  }

  static setupEventTracking() {
    // Track game clicks
    document.addEventListener('click', (e) => {
      const gameCard = e.target.closest('.game-card');
      if (gameCard) {
        const gameTitle = gameCard.querySelector('h3').textContent;
        gtag('event', 'game_click', {
          'game_title': gameTitle
        });
      }
    });

    // Track search
    if (UI.elements.searchInput) {
      UI.elements.searchInput.addEventListener('change', (e) => {
        gtag('event', 'game_search', {
          'search_term': e.target.value
        });
      });
    }
  }
}

// Performance Optimization
class Performance {
  static init() {
    this.setupLazyLoading();
    this.optimizeAssets();
  }

  static setupLazyLoading() {
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    });

    images.forEach(img => imageObserver.observe(img));
  }

  static optimizeAssets() {
    // Defer non-critical resources
    const deferredScripts = document.querySelectorAll('script[data-defer]');
    deferredScripts.forEach(script => {
      script.setAttribute('defer', '');
    });
  }
}

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
  UI.init();
  GameManager.init();
  Analytics.init();
  Performance.init();
}); 

// Intelligent ad display management
function manageAdExperience() {
let pageDepth = 0;
let userEngaged = false;
const adContainers = document.querySelectorAll('.ad-container:not(.ad-horizontal):not(.ad-sticky-bottom)');

// Track scroll depth
window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const docHeight = Math.max(
    document.body.scrollHeight, 
    document.body.offsetHeight, 
    document.documentElement.clientHeight, 
    document.documentElement.scrollHeight, 
    document.documentElement.offsetHeight
    );
    const windowHeight = window.innerHeight;
    const scrollPercent = scrollTop / (docHeight - windowHeight);
    pageDepth = Math.max(pageDepth, scrollPercent);
    
    // If user scrolled more than 50% of the page, consider them engaged
    if (pageDepth > 0.5) {
    userEngaged = true;
    }
    
    // Show more ads for engaged users
    if (userEngaged) {
    adContainers.forEach(container => {
        container.style.display = '';
    });
    } else {
    // Limit ads for non-engaged users (show only first few)
    adContainers.forEach((container, index) => {
        if (index > 2) {
        container.style.display = 'none';
        }
    });
    }
});

// Track game interaction as highest engagement
document.getElementById('game-frame').addEventListener('click', function() {
    userEngaged = true;
    // User played the game, they're definitely engaged - show all ads
    adContainers.forEach(container => {
    container.style.display = '';
    });
});
}

// Initialize ad experience management
document.addEventListener('DOMContentLoaded', function() {
manageAdExperience();
});

// Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
const menuToggle = document.getElementById('menu-toggle');
const sidebar = document.getElementById('sidebar');
const menuOverlay = document.getElementById('menuOverlay') || document.getElementById('menu-overlay');

// Toggle menu function
function toggleMenu() {
    sidebar.classList.toggle('active');
    if (menuOverlay) {
    menuOverlay.classList.toggle('active');
    }
    
    // Toggle between hamburger and close icon
    const icon = menuToggle.querySelector('i');
    if (icon.classList.contains('fa-bars')) {
    icon.classList.remove('fa-bars');
    icon.classList.add('fa-times');
    } else {
    icon.classList.remove('fa-times');
    icon.classList.add('fa-bars');
    }
}

// Add click event to menu toggle button
if (menuToggle) {
    menuToggle.addEventListener('click', function(e) {
    e.preventDefault();
    toggleMenu();
    });
}

// Close menu when clicking overlay
if (menuOverlay) {
    menuOverlay.addEventListener('click', toggleMenu);
}

// Close menu when clicking a menu item on mobile
const menuItems = document.querySelectorAll('.sidebar-menu a, .sidebar-categories li');
menuItems.forEach(item => {
    item.addEventListener('click', function() {
    if (window.innerWidth <= 768 && sidebar.classList.contains('active')) {
        toggleMenu();
    }
    });
});

// Close menu when ESC key is pressed
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && sidebar.classList.contains('active')) {
    toggleMenu();
    }
});

// Share button functionality
const shareBtn = document.getElementById('share-btn');
const shareMenu = document.getElementById('share-menu');

if (shareBtn) {
    shareBtn.addEventListener('click', function() {
    shareMenu.classList.toggle('active');
    });
}

// Copy link functionality
const copyLinkBtn = document.getElementById('copy-link-btn');

if (copyLinkBtn) {
    copyLinkBtn.addEventListener('click', function() {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
        alert('Link copied to clipboard!');
        shareMenu.classList.remove('active');
    });
    });
}

// Social share buttons
const facebookBtn = document.getElementById('facebook-btn');
const twitterBtn = document.getElementById('twitter-btn');
const pinterestBtn = document.getElementById('pinterest-btn');

if (facebookBtn) {
    facebookBtn.addEventListener('click', function() {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}`, '_blank');
    });
}

if (twitterBtn) {
    twitterBtn.addEventListener('click', function() {
    window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(window.location.href)}&text=${encodeURIComponent(document.title)}`, '_blank');
    });
}

if (pinterestBtn) {
    pinterestBtn.addEventListener('click', function() {
    window.open(`https://pinterest.com/pin/create/button/?url=${encodeURIComponent(window.location.href)}&description=${encodeURIComponent(document.title)}`, '_blank');
    });
}

// Fullscreen button functionality
const fullscreenBtn = document.getElementById('fullscreen-btn');
const gameFrame = document.getElementById('game-frame');

if (fullscreenBtn && gameFrame) {
    fullscreenBtn.addEventListener('click', function() {
    if (gameFrame.requestFullscreen) {
        gameFrame.requestFullscreen();
    } else if (gameFrame.mozRequestFullScreen) {
        gameFrame.mozRequestFullScreen();
    } else if (gameFrame.webkitRequestFullscreen) {
        gameFrame.webkitRequestFullscreen();
    } else if (gameFrame.msRequestFullscreen) {
        gameFrame.msRequestFullscreen();
    }
    });
}
});

// Performance optimization for ads
function optimizeAdPerformance() {
// Detect if user has slow connection
const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
let isSlowConnection = false;

if (connection) {
    isSlowConnection = connection.effectiveType === '2g' || connection.effectiveType === 'slow-2g';
}

// Reduce ads on slow connections
if (isSlowConnection) {
    const adContainers = document.querySelectorAll('.ad-container');
    // Keep only the first ad and remove others
    adContainers.forEach((container, index) => {
    if (index > 0) {
        container.style.display = 'none';
    }
    });
}

// Prioritize main content loading
document.addEventListener('DOMContentLoaded', function() {
    // Delay ad loading to ensure page content loads first
    setTimeout(() => {
    const adScripts = document.querySelectorAll('.ad-container script');
    adScripts.forEach(script => {
        const parent = script.parentNode;
        const newScript = document.createElement('script');
        newScript.textContent = script.textContent;
        parent.removeChild(script);
        setTimeout(() => {
        parent.appendChild(newScript);
        }, 100);
    });
    }, 1000);
});
}

// Initialize performance optimizations
optimizeAdPerformance();
