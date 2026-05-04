import flask as fl
from flask import (
    g, 
    current_app as APLICACION, 
    session as COOKIE_SESION, 
    request as SOLICITUD
)
import chastack_utiles_flask.ruteo as ruteo
from geneticapp.servidor import SERVIDOR

@SERVIDOR.route("/", methods=['GET'])
def inicio():
    return fl.render_template("inicio.html.j2")
