

/**
 * Representa el estado global de la aplicación.
 *
 * @typedef {Object} Estado
 * @property {boolean} __inicializada                 - Indica si el estado ya fue inicializado.
 * @property {'tema-claro' | 'tema-oscuro'} tema    - Tema activo ('tema-claro' | 'tema-oscuro').
 * @property {function(): void} cambiarTema         - Alterna el tema entre claro y oscuro.
 * @property {function(): boolean} esMovil          - Determina si el dispositivo es móvil.
 * @property {function(): void} iniciar             - Inicializa el estado global y aplica tema por defecto.
 * @property {function(): void} destruir            - Limpia el estado global.
 * @property {function(): void} reiniciar           - Reinicia el estado global.
*/


/**
 * Módulo de Estado Global (IIFE)
 */
(function (window, document) {
    'use strict';


    function formatearVelocidad(bps) {
        const mbps = bps / (1024 * 1024) * 10;
        if (mbps >= 1000) {
            return `${Math.round(bps / 1024)} GB/s`;
        }
        if (mbps < 0.1) {
            return `${Math.round(bps / 1024)} KB/s`;
        }
        return `${mbps.toFixed(1)} MB/s`;
    }

    function formatearTiempo(segundos) {
        if (segundos < 60) {
            return `${Math.round(segundos)}s`;
        } else if (segundos < 3600) {
            return `${Math.round(segundos / 60)}m ${Math.round(segundos % 60)}s`;
        } else {
            const horas = Math.floor(segundos / 3600);
            const minutos = Math.floor((segundos % 3600) / 60);
            return `${horas}h ${minutos}m`;
        }
    }

    /**
     * Procesa un parcial HTML que contiene OOB swaps con htmx
     * @param {string} cadena_html 
     */
    function procesarOOB(cadena_html) {
        const contenedor = document.createElement('div');
        contenedor.innerHTML = cadena_html;

        Array.from(contenedor.children).forEach(el => {
            if (typeof htmx !== 'undefined') {
                htmx.process(el);

                const swapOOB = el.getAttribute('hx-swap-oob');
                if (swapOOB) {
                    const [swapStyle, targetSelector] = swapOOB.split(':');
                    htmx.swap(
                        targetSelector,
                        el.outerHTML,
                        { swapStyle: swapStyle }
                    );
                }
            } else {
                console.warn('htmx no está definido, no se puede procesar OOB.');
            }
        });
    }

    // ==========================================
    // OBJETO DE ESTADO PRINCIPAL
    // ==========================================

    let __inicializada = false;
    /**
     * Representa el estado global de la aplicación.
     * @type {Estado} Estado
     */
    const ESTADO = {
        tema: 'tema-claro',

        // Exponemos las utilidades para que sean accesibles vía ESTADO.utilidades.formatearTiempo(...)
        utilidades: {
            formatearVelocidad,
            formatearTiempo,
            procesarOOB
        },

        cambiarTema() {
            const raiz = document.documentElement;
            this.tema = raiz.classList.contains('tema-oscuro') ? 'tema-claro' : 'tema-oscuro';

            raiz.classList.remove('tema-oscuro', 'tema-claro');
            raiz.classList.add(this.tema);
            localStorage.setItem('tema', this.tema);
            
            const eventoPersonalizado = new CustomEvent("cambiar-tema", {
                detail: { tema: this.tema }
            });
            window.dispatchEvent(eventoPersonalizado);
        },

        aplicarCascada() {
            const raiz = document.documentElement;
            const estilo = getComputedStyle(raiz).getPropertyValue("--animacion-media");
            // Manejo de error si la variable CSS no existe
            const duracion = estilo ? parseInt(estilo.trim()) : 0; 

            document.querySelectorAll(".cascada").forEach(contenedor => {
                const corrimiento = parseInt(contenedor.dataset.corrimiento) || 0;
                const hijos = contenedor.children;
                const total = hijos.length;

                Array.from(hijos).forEach((e, i) => {
                    let indice = i;
                    if (contenedor.classList.contains('invertida')) indice = 0 - i;
                    const atraso = corrimiento + (total - 1 - indice) * duracion;
                    e.style.animationDelay = `${atraso}ms`;
                });
            });
        },

        advertencia(mensaje) {
            this.renderizarNotificacion(mensaje, 'advertencia');
            console.warn(`\t%cADVERTENCIA:%c ${mensaje}`,
                'font-family: "neo-sans",sans-serif;padding:5px;font-size:18px ;color:white;background-color:#f8794f;font-weight:bold;',
                'font-family: "neo-sans",sans-serif;padding:5px;font-size:18px;color:#f8794f;'
            );
        },
        error(mensaje) {
            this.renderizarNotificacion(mensaje, 'error');
            console.error(`\t%cERROR:%c ${mensaje}`,
                'font-family: "neo-sans",sans-serif;padding:5px;font-size:18px ;color:white;background-color:#A33333;font-weight:bold;',
                'font-family: "neo-sans",sans-serif;padding:5px;font-size:18px;color:#A33333;'
            );
        },
        info(mensaje) {
            this.renderizarNotificacion(mensaje, 'info');
            console.info(`\t%cINFO: ${mensaje}`, 'font-family: "neo-sans",sans-serif;padding:5px;font-size:18px ;color:#0c96ad;');
        },
        exito(mensaje) {
            this.renderizarNotificacion(mensaje, 'exito');
            console.info(`\t%cÉXITO:%c ${mensaje}`,
                'font-family: "neo-sans",sans-serif;padding:5px;font-size:18px ;color:white;background-color:#027956;font-weight:bold;',
                'font-family: "neo-sans",sans-serif;padding:5px;font-size:18px;color:#027956;'
            );
        },

        esMovil() {
            const tamRaiz = parseFloat(getComputedStyle(document.documentElement).fontSize);
            const anchoMax = 40 * tamRaiz;
            return (
                /Mobi|Android|iPhone|iPad|iPod|Windows Phone|webOS|BlackBerry|Opera Mini|IEMobile|Mobile/i.test(navigator.userAgent) ||
                ('ontouchstart' in window && navigator.maxTouchPoints > 0) ||
                window.matchMedia(`(max-width: ${anchoMax}px)`).matches
            );
        },

        iniciar() {
            if (__inicializada) return;
            
            // Exponer la instancia actual en window.estado
            window.estado = this; 
            
            const raiz = document.documentElement;
            raiz.classList.add('tema-claro');
            
            if (localStorage.tema !== undefined) {
                if (localStorage.tema === 'tema-oscuro') {
                    this.cambiarTema();
                }
            } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                this.cambiarTema();
            }
            __inicializada = true;
        },

        renderizarNotificacion(mensaje, tipo) {
            const div = document.createElement("div");
            div.className = `tarjeta notificacion fila ${tipo} aparece`;
            div.innerHTML = `
            ${mensaje}
            <a href="#">
                <span class="material-symbols-outlined">close_small</span>
            </a>
            `;

            requestAnimationFrame(() => {
                div.addEventListener("animationend", function handler() {
                    div.classList.remove("aparece");
                    div.removeEventListener("animationend", handler);

                    if (tipo !== "error" && tipo !== "exito") {
                        setTimeout(() => {
                            div.classList.add("desaparece");
                            div.addEventListener("animationend", function h2() {
                                div.classList.remove("desaparece");
                                div.classList.add("oculto");
                                div.removeEventListener("animationend", h2);
                                // Nota: colapsarNotificaciones debe estar definido globalmente 
                                // o pasarse como dependencia.
                                if (typeof colapsarNotificaciones === 'function') {
                                    colapsarNotificaciones();
                                }
                            });
                        }, 1000);
                    }
                });
            });

            const a = div.querySelector("a");
            a.addEventListener("click", (ev) => {
                ev.preventDefault();
                div.classList.remove("aparece");
                div.classList.add("desaparece");
                div.addEventListener("animationend", function h3() {
                    div.classList.remove("desaparece");
                    div.classList.add("oculto");
                    div.removeEventListener("animationend", h3);
                    if (typeof colapsarNotificaciones === 'function') {
                        colapsarNotificaciones();
                    }
                });
            });

            const expande = document.querySelector("#notificaciones > .expande");
            if (expande) {
                expande.appendChild(div);
            }

            return div;
        },

        destruir() {
            // Limpieza consistente de la variable global
            window.estado = undefined; 
            __inicializada = false;
        },

        reiniciar() {
            this.destruir();
            this.iniciar();
        }
    };

    window.ESTADO = ESTADO;

})(window, document);