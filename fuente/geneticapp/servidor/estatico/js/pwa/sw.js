const CACHE_NAME = 'geneticapp-v1.0.0';
const SIN_CONEXION = '/sinConexion';

// Archivos esenciales para el funcionamiento sin conexión
const ARCHIVOS_ESENCIALES = [
  '/',
  '/sinConexion',
  '/js/global.js',
  '/js/modulos/utiles.js',
  // Agrega aquí los CSS críticos
  '/css/base.css',
  '/css/identidad/colores.css',
  '/css/identidad/tipografía/fuentes.css',
  // CDN críticos
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://unpkg.com/htmx.org@2.0.4'
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
  console.log('[SW]: Instalando...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW]: Cacheando archivos esenciales');
        return cache.addAll(ARCHIVOS_ESENCIALES);
      })
      .then(() => {
        console.log('[SW]: Instalación completada');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[SW]: Error durante la instalación:', error);
      })
  );
});

// Activación del Service Worker
self.addEventListener('activate', (event) => {
  console.log('[SW]: Activando...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW]: Eliminando cache antigua:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('[SW]: Activación completada');
      return self.clients.claim();
    })
  );
});

// Intercepción de peticiones
self.addEventListener('fetch', (event) => {
  // Solo manejar peticiones GET
  if (event.request.method !== 'GET') {
    return;
  }

  // Estrategia: Network First, luego Cache, luego Offline
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Si la respuesta es exitosa, cachearla
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseClone);
            });
        }
        return response;
      })
      .catch(() => {
        // Si la red falla, buscar en cache
        return caches.match(event.request)
          .then((cachedResponse) => {
            if (cachedResponse) {
              return cachedResponse;
            }
            
            // Si no está en cache y es una navegación, mostrar página sin conexión
            if (event.request.mode === 'navigate') {
              return caches.match(SIN_CONEXION);
            }
            
            // Para otros recursos, retornar un error
            return new Response('Recurso no disponible sin conexión', {
              status: 503,
              statusText: 'Service Unavailable'
            });
          });
      })
  );
});

// Manejo de mensajes del cliente
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Sincronización en segundo plano (opcional)
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Aquí puedes agregar lógica para sincronizar datos cuando se recupere la conexión
      console.log('[SW]: Sincronización en segundo plano')
    );
  }
});

// Notificaciones push (opcional)
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json();
    
    event.waitUntil(
      self.registration.showNotification(data.title, {
        body: data.body,
        icon: '/static/publico/img/pwa/icon-192x192.png',
        badge: '/static/publico/img/pwa/icon-72x72.png',
        tag: 'geneticapp-notification',
        requireInteraction: true
      })
    );
  }
});