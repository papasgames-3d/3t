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
    // Search Input
    if (this.elements.searchInput) {
      this.elements.searchInput.addEventListener('input', this.debounce((e) => {
        AppState.searchTerm = e.target.value.toLowerCase();
        GameManager.filterGames();
      }, 300));
    }

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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  UI.init();
  GameManager.init();
});
