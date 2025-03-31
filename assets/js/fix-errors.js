// Fix AudioContext error
function initAudio() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    if (audioContext.state === 'suspended') {
        audioContext.resume();
    }
}

// Add event listeners for user interaction
document.addEventListener('click', initAudio, { once: true });
document.addEventListener('touchstart', initAudio, { once: true });

// Fix GPT loading issues
window.googletag = window.googletag || { cmd: [] };
let gptLoaded = false;

function loadGPT() {
    if (!gptLoaded) {
        const script = document.createElement('script');
        script.src = 'https://securepubads.g.doubleclick.net/tag/js/gpt.js';
        script.async = true;
        document.head.appendChild(script);
        gptLoaded = true;
    }
}

// Load GPT only when needed
document.addEventListener('DOMContentLoaded', function() {
    // Load GPT after a short delay to avoid multiple loads
    setTimeout(loadGPT, 1000);
});

// Fix PokiSDK initialization
if (typeof PokiSDK !== 'undefined') {
    PokiSDK.init().then(
        function() {
            console.log('PokiSDK initialized successfully');
        }
    ).catch(
        function(error) {
            console.error('PokiSDK initialization failed:', error);
        }
    );
}

// Fix GameAnalytics initialization
if (typeof GameAnalytics !== 'undefined') {
    GameAnalytics.configureBuild('1.0.0');
    GameAnalytics.initialize('YOUR_GAME_KEY', 'YOUR_SECRET_KEY');
}

// Remove unused preload links
document.addEventListener('DOMContentLoaded', function() {
    const preloadLinks = document.querySelectorAll('link[rel="preload"]');
    preloadLinks.forEach(link => {
        if (!link.hasAttribute('as')) {
            link.remove();
        }
    });
}); 