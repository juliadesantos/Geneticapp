import flask as fl
from flask import (
    g,
    current_app as APLICACION,
    session as COOKIE_SESION,
    request as SOLICITUD
)
import chastack_utiles_flask.ruteo as ruteo

import geneticapp.bdd as BDD
from geneticapp.bdd.enfermedades import Enfermedad

from geneticapp.servidor.planos.enfermedades import enfermedades_bp


@enfermedades_bp.route("/", methods=['GET'])
def inicio():
    enfermedades = Enfermedad.devolverRegistros(g.bdd)
    return fl.render_template("enfermedades/inicio.html.j2", enfermedades=enfermedades)


@enfermedades_bp.route("/<int:id>", methods=['GET'])
def detalle(id):
    enfermedad = Enfermedad(g.bdd, id)
    return fl.render_template("enfermedades/detalle.html.j2", enfermedad=enfermedad)


@enfermedades_bp.route("/nueva", methods=['GET', 'POST'])
def nueva():
    if SOLICITUD.method == 'POST':
        datos = {
            'nombre': SOLICITUD.form.get('nombre'),
            'gen_afectado': SOLICITUD.form.get('gen_afectado'),
            'tipo_herencia': SOLICITUD.form.get('tipo_herencia'),
            'sintomas': SOLICITUD.form.get('sintomas'),
        }
        enfermedad = Enfermedad(g.bdd, datos)
        enfermedad.guardar()
        fl.flash('Enfermedad creada correctamente.', 'EXITO')
        return fl.redirect(fl.url_for('.inicio'))
    return fl.render_template("enfermedades/crear.html.j2")


@enfermedades_bp.route("/<int:id>/editar", methods=['GET', 'POST'])
def editar(id):
    enfermedad = Enfermedad(g.bdd, id)
    if SOLICITUD.method == 'POST':
        enfermedad.nombre = SOLICITUD.form.get('nombre')
        enfermedad.gen_afectado = SOLICITUD.form.get('gen_afectado')
        enfermedad.tipo_herencia = SOLICITUD.form.get('tipo_herencia')
        enfermedad.sintomas = SOLICITUD.form.get('sintomas')
        enfermedad.guardar()
        fl.flash('Enfermedad actualizada correctamente.', 'EXITO')
        return fl.redirect(fl.url_for('.detalle', id=id))
    return fl.render_template("enfermedades/editar.html.j2", enfermedad=enfermedad)


@enfermedades_bp.route("/<int:id>/eliminar", methods=['POST'])
def eliminar(id):
    enfermedad = Enfermedad(g.bdd, id)
    enfermedad.eliminar()
    fl.flash('Enfermedad eliminada.', 'EXITO')
    return fl.redirect(fl.url_for('.inicio'))
