import flask as fl
from flask import (
    g, 
    current_app as APLICACION, 
    session as COOKIE_SESION, 
    request as SOLICITUD
)
import chastack_utiles_flask.ruteo as ruteo

import geneticapp.bdd as BDD

from geneticapp.servidor.planos.geneticapp import geneticapp_bp

@geneticapp_bp.route("/", methods=['GET'])
def inicio():
    return fl.render_template("geneticapp/inicio.html.j2")
