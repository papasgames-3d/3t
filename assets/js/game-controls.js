document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const gameFrame = document.getElementById('game-frame');
    const gameThumb = document.querySelector('.game-thumbnail');
    const playButton = document.getElementById('playGameButton');
    const shareBtn = document.getElementById('share-btn');
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const shareMenu = document.getElementById('share-menu');
    const copyLinkBtn = document.getElementById('copy-link-btn');
    const facebookBtn = document.getElementById('facebook-btn');
    const twitterBtn = document.getElementById('twitter-btn');
    const pinterestBtn = document.getElementById('pinterest-btn');

    // Play button functionality
    if (playButton) {
        playButton.addEventListener('click', function() {
            if (gameThumb && gameFrame) {
                gameThumb.style.display = 'none';
                gameFrame.style.display = 'block';
            }
        });
    }

    // Share menu toggle
    if (shareBtn) {
        shareBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            shareMenu.classList.toggle('active');
        });
    }

    // Close share menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!shareMenu.contains(e.target) && !shareBtn.contains(e.target)) {
            shareMenu.classList.remove('active');
        }
    });

    // Fullscreen functionality
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', function() {
            if (gameFrame) {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                } else {
                    gameFrame.requestFullscreen().catch(err => {
                        console.log('Error attempting to enable fullscreen:', err);
                    });
                }
            }
        });
    }

    // Share buttons functionality
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', function() {
            navigator.clipboard.writeText(window.location.href)
                .then(() => {
                    alert('Link copied to clipboard!');
                    shareMenu.classList.remove('active');
                })
                .catch(err => {
                    console.log('Error copying link:', err);
                });
        });
    }

    if (facebookBtn) {
        facebookBtn.addEventListener('click', function() {
            const url = encodeURIComponent(window.location.href);
            window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
        });
    }

    if (twitterBtn) {
        twitterBtn.addEventListener('click', function() {
            const url = encodeURIComponent(window.location.href);
            const text = encodeURIComponent(document.title);
            window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank');
        });
    }

    if (pinterestBtn) {
        pinterestBtn.addEventListener('click', function() {
            const url = encodeURIComponent(window.location.href);
            const media = encodeURIComponent(document.querySelector('.game-thumbnail img')?.src || '');
            const description = encodeURIComponent(document.title);
            window.open(`https://pinterest.com/pin/create/button/?url=${url}&media=${media}&description=${description}`, '_blank');
        });
    }
}); 