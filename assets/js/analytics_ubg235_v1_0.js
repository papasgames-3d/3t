function loadGoogleAnalytics() {
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-54L5E2NJ3K');
}

function loadDnsPrefetch() {
    var link = document.createElement('link');
    link.href = "https://universal.wgplayer.com";
    link.rel = "dns-prefetch";
    document.head.appendChild(link);
}

window.addEventListener("load", function() {
    if (navigator.webdriver) {
      console.log('Bot Browser');
    } else {
      console.log('Human Browser');
      loadGoogleAnalytics();
      loadDnsPrefetch();
    }
});
