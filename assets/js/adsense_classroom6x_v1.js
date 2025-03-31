window.addEventListener("load", (event) => {
    function inFrame () {
        try {
            return window.self !== window.top;
        } catch (e) {
            return true;
        }
    }

    function botBrowser() {
        try {
            return navigator.webdriver
        } catch (e) {
            return true;
        }
    }

    function loadUserScripts() {
        // Load wgplayer script
        !function(e,t){
            a=e.createElement("script");
            m=e.getElementsByTagName("script")[0];
            a.async=1;
            a.src=t;
            a.fetchPriority='high';
            m.parentNode.insertBefore(a,m)
        }(document,"https://universal.wgplayer.com/tag/?lh="+window.location.hostname+"&wp="+window.location.pathname+"&ws="+window.location.search);
    }

    if (botBrowser()) {
        console.log('Bot Browser');
    } else {
        console.log('Human Browser');
        if (window.location.href.indexOf("/classroom6x.gitlab.io")> -1) {
            if (inFrame()) {
                console.log("Scripts Skip! Frame!");
            } else if (window.location.href.indexOf(".html")== -1) {
                console.log("Scripts Skip! Home Page!");
            } else if (window.location.href.indexOf("-unblockedz.html")> -1) {
                console.log("Scripts Skip! DMCA!");            
            } else {
                console.log("Scripts Served!");
                loadUserScripts();
            }
        } else {
            console.log("Scripts Skip! Not Games235!");
        }
    }
});
