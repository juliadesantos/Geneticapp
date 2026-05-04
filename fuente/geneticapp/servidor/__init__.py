import flask as fl
from flask import (
    g, 
    current_app as APLICACION, 
    session as COOKIE_SESION, 
    request as SOLICITUD
)

import datetime as dt
import os 

import geneticapp.bdd as BDD
from geneticapp.bdd.globales import GLOBALES

raiz = os.path.abspath(os.path.dirname(__file__))

SERVIDOR = fl.Flask(
    __name__.split('.')[0],
    static_url_path='',
    static_folder=os.path.join(raiz, "estatico"),
    template_folder=os.path.join(raiz, "plantillas")
)

SERVIDOR.config.from_pyfile(os.path.join(raiz, "config.py"))
SERVIDOR.permanent_session_lifetime = dt.timedelta(days=31)
from geneticapp.servidor.planos.enfermedades import enfermedades_bp
SERVIDOR.register_blueprint(
    enfermedades_bp,
    url_prefix = "/enfermedades",
)
from geneticapp.servidor.planos.medicamentos import medicamentos_bp
SERVIDOR.register_blueprint(
    medicamentos_bp,
    url_prefix = "/medicamentos",
)
from geneticapp.servidor.planos.geneticapp import geneticapp_bp
SERVIDOR.register_blueprint(
    geneticapp_bp,
    url_prefix = "/geneticapp",
)


if SERVIDOR.config.get('AMBIENTE_GENETICAPP') == 'DESARROLLO':
    from geneticapp.servidor.planos.desarrollo import desarrollo_bp
    SERVIDOR.register_blueprint(
        desarrollo_bp,
        url_prefix = "/desarrollo",
    )

@SERVIDOR.before_request
def montarBDD():
    from geneticapp.bdd import registrarBddGlobal, devolverBDD
    BDD.registrarBddGlobal(BDD.devolverBDD(), g)


@SERVIDOR.context_processor
def inyectarContexto():
    return dict(
        GLOBALES = GLOBALES,
        CONFIG = SERVIDOR.config,
    )

import geneticapp.servidor.vistas
import geneticapp.servidor.planos.enfermedades.vistas
import geneticapp.servidor.planos.medicamentos.vistas
import geneticapp.servidor.planos.geneticapp.vistas

if SERVIDOR.config.get('AMBIENTE_GENETICAPP') == 'DESARROLLO':
    import geneticapp.servidor.planos.desarrollo.vistas

