// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('Service Worker: Registered', reg))
            .catch(err => console.error('Service Worker: Error', err));
    });
}

// UI Initialization
document.addEventListener('DOMContentLoaded', () => {
    console.log("Application initialized.");
});