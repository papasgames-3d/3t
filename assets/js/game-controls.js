// Game controls functionality
document.addEventListener('DOMContentLoaded', function() {
    const gameContainer = document.querySelector('.game-frame-container');
    const gameFrame = document.getElementById('game-frame');
    const playButton = document.getElementById('playGameButton');
    const thumbnail = document.querySelector('.game-thumbnail');
    const shareButton = document.getElementById('share-btn');
    const shareMenu = document.getElementById('share-menu');
    const fullscreenButton = document.getElementById('fullscreen-btn');
    const loadingOverlay = document.querySelector('.loading-overlay');

    if (!gameContainer || !playButton || !gameFrame || !thumbnail) {
        return;
    }

    // Play button click handler
    playButton.addEventListener('click', function() {
        thumbnail.style.display = 'none';
        if (loadingOverlay) loadingOverlay.style.display = 'flex';

        const gameUrl = gameFrame.getAttribute('data-src');
        gameFrame.src = gameUrl;

        gameFrame.onload = function() {
            if (loadingOverlay) loadingOverlay.style.display = 'none';
            gameFrame.style.display = 'block';
        };
    });

    // Share button functionality
    if (shareButton && shareMenu) {
    shareButton.addEventListener('click', function(e) {
        e.stopPropagation();
        shareMenu.classList.toggle('active');
    });

    // Close share menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!shareMenu.contains(e.target) && !shareButton.contains(e.target)) {
            shareMenu.classList.remove('active');
        }
    });
    }

    // Share buttons functionality
    const copyLinkBtn = document.getElementById('copy-link-btn');
    const facebookBtn = document.getElementById('facebook-btn');
    const twitterBtn = document.getElementById('twitter-btn');
    const pinterestBtn = document.getElementById('pinterest-btn');
    if (copyLinkBtn) copyLinkBtn.addEventListener('click', function() {
        navigator.clipboard.writeText(window.location.href);
        alert('Link copied to clipboard!');
    });
    if (facebookBtn) facebookBtn.addEventListener('click', function() {
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}`, '_blank');
    });
    if (twitterBtn) twitterBtn.addEventListener('click', function() {
        window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(window.location.href)}`, '_blank');
    });
    if (pinterestBtn) pinterestBtn.addEventListener('click', function() {
        window.open(`https://pinterest.com/pin/create/button/?url=${encodeURIComponent(window.location.href)}`, '_blank');
    });

    // Fullscreen functionality
    if (!fullscreenButton) return;
    fullscreenButton.addEventListener('click', function() {
        if (!document.fullscreenElement) {
            if (gameContainer.requestFullscreen) {
                gameContainer.requestFullscreen();
            } else if (gameContainer.webkitRequestFullscreen) {
                gameContainer.webkitRequestFullscreen();
            } else if (gameContainer.msRequestFullscreen) {
                gameContainer.msRequestFullscreen();
            }
            fullscreenButton.innerHTML = '<i class="fas fa-compress"></i>';
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
            fullscreenButton.innerHTML = '<i class="fas fa-expand"></i>';
        }
    });

    // Update fullscreen button icon when exiting fullscreen via Esc key
    document.addEventListener('fullscreenchange', function() {
        if (!document.fullscreenElement) {
            fullscreenButton.innerHTML = '<i class="fas fa-expand"></i>';
        }
    });
}); 