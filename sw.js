const CACHE_NAME = 'ems-guidelines-v1';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './styles.css',
    './app.js',
    './manifest.json',
    './pages/airway.html',
    './pages/algorithms.html',
    './pages/allergic.html',
    './pages/burns.html',
    './pages/calculator.html',
    './pages/cardiac.html',
    './pages/consent.html',
    './pages/diabetes.html',
    './pages/extremity.html',
    './pages/hemorrhagic.html',
    './pages/med-list.html',
    './pages/medications.html',
    './pages/pain.html',
    './pages/patient-determination.html',
    './pages/pediatric.html',
    './pages/quick-cards.html',
    './pages/respiratory.html',
    './pages/seizure.html',
    './pages/stroke.html',
    './pages/supportive-care.html',
    './pages/trauma-general.html'
];

// Install Event - Cache Assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(ASSETS_TO_CACHE);
            })
    );
});

// Activate Event - Clean old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Fetch Event - Serve from cache, then network
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Return cached version if found
                if (response) {
                    return response;
                }
                // Otherwise fetch from network
                return fetch(event.request).then(
                    response => {
                        // Check if valid response
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // Clone response to cache it
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME)
                            .then(cache => {
                                cache.put(event.request, responseToCache);
                            });

                        return response;
                    }
                );
            })
    );
});
