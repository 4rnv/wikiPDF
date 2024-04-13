if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('static/js/sw.js').then(registration => {
            console.log('ServiceWorker registration successful');
        }, err => {
            console.log('ServiceWorker registration failed: ', err);
        }).catch(err => {
            console.log(err);
        });
    });
  } else {
    console.log('Service workers are not supported (Firefox Private Browsing).');
  }