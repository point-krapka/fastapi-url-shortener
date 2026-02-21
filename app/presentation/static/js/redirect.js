(function () {
    function detectOS(userAgent) {
        if (/windows/i.test(userAgent)) return "Windows";
        if (/android/i.test(userAgent)) return "Android";
        if (/iphone|ipad|ipod/i.test(userAgent)) return "iOS";
        if (/macintosh|mac os x/i.test(userAgent)) return "macOS";
        if (/linux/i.test(userAgent)) return "Linux";
        return "Unknown";
    }

    function detectBrowser(userAgent) {
        if (/edg/i.test(userAgent)) return "Edge";
        if (/opr|opera/i.test(userAgent)) return "Opera";
        if (/chrome|crios/i.test(userAgent)) return "Chrome";
        if (/firefox|fxios/i.test(userAgent)) return "Firefox";
        if (/safari/i.test(userAgent) && !/chrome|crios|edg/i.test(userAgent)) return "Safari";
        return "Unknown";
    }

    function detectDevice(userAgent) {
        if (/tablet|ipad/i.test(userAgent)) return "Tablet";
        if (/mobi|iphone|android/i.test(userAgent)) return "Mobile";
        return "Desktop";
    }

    function postTrack(endpoint, payload) {
        var body = JSON.stringify(payload);

        if (navigator.sendBeacon) {
            var blob = new Blob([body], { type: "application/json" });
            navigator.sendBeacon(endpoint, blob);
            return;
        }

        fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: body,
            keepalive: true,
            credentials: "same-origin",
        }).catch(function () {});
    }

    var root = document.documentElement;
    var targetUrl = root.dataset.targetUrl || "/";
    var shortUrl = root.dataset.shortUrl || "";
    var endpoint = root.dataset.trackEndpoint || "/api/track";

    var userAgent = navigator.userAgent || "";
    var payload = {
        curl_url: shortUrl,
        os: detectOS(userAgent),
        browser: detectBrowser(userAgent),
        device: detectDevice(userAgent),
        language: navigator.language || null,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || null,
        size_window: window.innerWidth + "x" + window.innerHeight,
    };

    if (shortUrl) {
        postTrack(endpoint, payload);
    }

    setTimeout(function () {
        window.location.replace(targetUrl);
    }, 60);
})();
