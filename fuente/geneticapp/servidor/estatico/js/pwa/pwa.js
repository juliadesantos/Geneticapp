       // Registro del SW
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('/js/pwa/sw.js')
                    .then(function(registro) {
                        console.log('SW registrado exitosamente:', registro.scope);
                        
                        // Verificar actualizaciones
                        registro.addEventListener('updatefound', function() {
                            const installingWorker = registro.installing;
                            installingWorker.addEventListener('statechange', function() {
                                if (installingWorker.state === 'installed') {
                                    if (navigator.serviceWorker.controller) {
                                        // Hay una nueva versión disponible
                                        mostrarActualizaciónDisponible();
                                    }
                                }
                            });
                        });
                    })
                    .catch(function(error) {
                        console.error('Error al registrar SW:', error);
                    });
            });
        }

        // PWA Install Banner
        let deferredPrompt;
        const installBanner = document.getElementById('banner-pwa');
        const installBtn = document.getElementById('boton-instalar-pwa');
        const dismissBtn = document.getElementById('boton-omitir-pwa');

        // Escuchar evento beforeinstallprompt
        window.addEventListener('beforeinstallprompt', function(e) {
            e.preventDefault();
            deferredPrompt = e;
            
            // Mostrar banner si no se ha instalado ni rechazado
            if (!localStorage.getItem('pwa-dismissed') && !window.matchMedia('(display-mode: standalone)').matches) {
                setTimeout(() => {
                    installBanner.classList.add('mostrar');
                }, 3000);
            }
        });

        // Manejar instalación
        installBtn.addEventListener('click', function() {
            installBanner.classList.remove('mostrar');
            
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt.userChoice.then(function(choiceResult) {
                    if (choiceResult.outcome === 'accepted') {
                        console.log('PWA instalada por el usuario');
                    } else {
                        console.log('Usuario rechazó la instalación');
                    }
                    deferredPrompt = null;
                });
            }
        });

        // Manejar rechazo
        dismissBtn.addEventListener('click', function() {
            installBanner.classList.remove('mostrar');
            localStorage.setItem('pwa-dismissed', 'true');
        });

        // Detectar cuando se instala la PWA
        window.addEventListener('appinstalled', function() {
            console.log('PWA instalada exitosamente');
            installBanner.classList.remove('mostrar');
        });

        // Indicador de conexión
        const connectionIndicator = document.getElementById('indicador-conexion');
        const connectionText = document.getElementById('connection-text');

        function actualizarEstadoConección() {
            const isOnline = navigator.onLine;
            
            if (isOnline) {
                connectionIndicator.className = 'indicador-conexion online';
                connectionText.textContent = 'Conectado';
            } else {
                connectionIndicator.className = 'indicador-conexion offline';
                connectionText.textContent = 'Sin conexión';
            }
            
            // Mostrar indicador temporalmente
            connectionIndicator.classList.add('mostrar');
            setTimeout(() => {
                connectionIndicator.classList.remove('mostrar');
            }, 3000);
        }

        // Escuchar cambios de conexión
        window.addEventListener('online', actualizarEstadoConección);
        window.addEventListener('offline', actualizarEstadoConección);

        // Función para mostrar notificación de actualización
        function mostrarActualizaciónDisponible() {
            if (confirm('¡Hay una nueva versión de MetaClub disponible! ¿Deseas actualizar?')) {
                window.location.reload();
            }
        }