import flask as fl
from flask import (
    g,
    current_app as APLICACION,
    session as COOKIE_SESION,
    request as SOLICITUD
)
import chastack_utiles_flask.ruteo as ruteo

import geneticapp.bdd as BDD
from geneticapp.bdd.medicamentos import Medicamento
from geneticapp.bdd.enfermedades import Enfermedad

from geneticapp.servidor.planos.medicamentos import medicamentos_bp


@medicamentos_bp.route("/", methods=['GET'])
def inicio():
    medicamentos = Medicamento.devolverRegistros(g.bdd)
    return fl.render_template("medicamentos/inicio.html.j2", medicamentos=medicamentos)


@medicamentos_bp.route("/<int:id>", methods=['GET'])
def detalle(id):
    medicamento = Medicamento(g.bdd, id)
    enfermedad = Enfermedad(g.bdd, medicamento.enfermedad_id)
    return fl.render_template("medicamentos/detalle.html.j2", medicamento=medicamento, enfermedad=enfermedad)


@medicamentos_bp.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    if SOLICITUD.method == 'POST':
        datos = {
            'nombre': SOLICITUD.form.get('nombre'),
            'principio_activo': SOLICITUD.form.get('principio_activo'),
            'dosis': SOLICITUD.form.get('dosis'),
            'enfermedad_id': SOLICITUD.form.get('enfermedad_id'),
        }
        medicamento = Medicamento(g.bdd, datos)
        medicamento.guardar()
        fl.flash('Medicamento creado correctamente.', 'EXITO')
        return fl.redirect(fl.url_for('.inicio'))
    enfermedades = Enfermedad.devolverRegistros(g.bdd)
    return fl.render_template("medicamentos/crear.html.j2", enfermedades=enfermedades)


@medicamentos_bp.route("/<int:id>/editar", methods=['GET', 'POST'])
def editar(id):
    medicamento = Medicamento(g.bdd, id)
    if SOLICITUD.method == 'POST':
        medicamento.nombre = SOLICITUD.form.get('nombre')
        medicamento.principio_activo = SOLICITUD.form.get('principio_activo')
        medicamento.dosis = SOLICITUD.form.get('dosis')
        medicamento.enfermedad_id = SOLICITUD.form.get('enfermedad_id')
        medicamento.guardar()
        fl.flash('Medicamento actualizado correctamente.', 'EXITO')
        return fl.redirect(fl.url_for('.detalle', id=id))
    enfermedades = Enfermedad.devolverRegistros(g.bdd)
    return fl.render_template("medicamentos/editar.html.j2", medicamento=medicamento, enfermedades=enfermedades)


@medicamentos_bp.route("/<int:id>/eliminar", methods=['POST'])
def eliminar(id):
    medicamento = Medicamento(g.bdd, id)
    medicamento.eliminar()
    fl.flash('Medicamento eliminado.', 'EXITO')
    return fl.redirect(fl.url_for('.inicio'))
