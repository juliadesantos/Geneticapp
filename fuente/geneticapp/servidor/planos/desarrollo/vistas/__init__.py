import flask as fl
from flask import (
    g,
    current_app as APLICACION,
    session as COOKIE_SESION,
    request as SOLICITUD
)
import chastack_utiles_flask.ruteo as ruteo

import geneticapp.bdd as BDD

from geneticapp.servidor.planos.desarrollo import desarrollo_bp


def obtener_arbol_rutas():
    """
    Genera un arbol de rutas dinamico a partir de la aplicacion Flask.
    Retorna una estructura que puede ser renderizada en el template.
    """
    rutas = []
    app = APLICACION._get_current_object()

    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue

        metodos = [m for m in rule.methods if m not in ('HEAD', 'OPTIONS')]

        # Determinar el tipo de ruta (plano o principal)
        endpoint_parts = rule.endpoint.split('.')
        if len(endpoint_parts) > 1:
            plano = endpoint_parts[0].replace('_', ' ').title()
        else:
            plano = 'Principal'

        rutas.append({
            'ruta': str(rule.rule),
            'metodos': ', '.join(sorted(metodos)),
            'endpoint': rule.endpoint,
            'plano': plano,
            'argumentos': list(rule.arguments) if rule.arguments else []
        })

    # Ordenar por ruta
    rutas.sort(key=lambda x: x['ruta'])

    return rutas


def obtener_planos_info():
    """
    Obtiene informacion sobre los blueprints registrados.
    """
    app = APLICACION._get_current_object()
    planos = []

    for nombre, blueprint in app.blueprints.items():
        if nombre == 'desarrollo':
            continue  # No mostrar el plano desarrollo en la lista

        rutas_plano = [
            rule for rule in app.url_map.iter_rules()
            if rule.endpoint.startswith(nombre + '.') or
               rule.endpoint.startswith(nombre.replace('.', '_') + '.')
        ]

        planos.append({
            'nombre': nombre.replace('_', ' ').title(),
            'nombre_minus': nombre.replace(' ', '_').lower(),
            'url_prefix': blueprint.url_prefix or '/',
            'num_rutas': len(rutas_plano),
            'static_folder': blueprint.static_folder is not None,
            'template_folder': blueprint.template_folder is not None,
        })

    return planos


@desarrollo_bp.route("/", methods=['GET'])
def inicio():
    rutas = obtener_arbol_rutas()
    planos = obtener_planos_info()
    return fl.render_template(
        "desarrollo/inicio.html.j2",
        rutas=rutas,
        planos_info=planos
    )


@desarrollo_bp.route("/chastack", methods=['GET'])
def chastack():
    """Pagina de documentacion de Ch'astack"""
    return fl.render_template("desarrollo/chastack.html.j2")


@desarrollo_bp.route("/rutas", methods=['GET'])
def rutas():
    """API JSON de rutas para uso dinamico"""
    rutas = obtener_arbol_rutas()
    return fl.jsonify(rutas)
