import os

import flask as fl
from flask import (
    g, 
    current_app as APLICACION, 
    session as COOKIE_SESION, 
    request as SOLICITUD
)
import chastack_utiles_flask.ruteo as ruteo

import geneticapp.bdd as BDD
from geneticapp.bdd.globales import GLOBALES

base_dir = os.path.abspath(os.path.dirname(__file__))
plantillas_dir = os.path.join(base_dir, "plantillas")

geneticapp_bp : fl.Blueprint = fl.Blueprint(
    __name__.replace('.', '_'),
    __name__.split('.')[-1],
    static_url_path='',
    static_folder=os.path.join(base_dir, "estatico"),
    template_folder=plantillas_dir,
    url_prefix="/geneticapp",
)


@geneticapp_bp.context_processor
def inyectarContexto():
    return dict(
        GLOBALES = GLOBALES
    )


import geneticapp.servidor.planos.geneticapp.vistas