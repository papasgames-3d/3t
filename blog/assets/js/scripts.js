document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            const mainNav = document.querySelector('.main-nav');
            if (mainNav) {
                mainNav.classList.toggle('active');
                mobileMenuToggle.classList.toggle('active');
            }
        });
    }

    // Back to top button
    const backToTopButton = document.createElement('a');
    backToTopButton.href = '#';
    backToTopButton.classList.add('back-to-top');
    backToTopButton.innerHTML = '<i class="arrow-up">↑</i>';
    document.body.appendChild(backToTopButton);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });

    backToTopButton.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // External links
    const links = document.querySelectorAll('a');
    links.forEach(link => {
        const href = link.getAttribute('href');
        if (href && href.startsWith('http') && !href.includes(window.location.hostname)) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
}); 