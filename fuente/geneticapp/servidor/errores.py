from geneticapp.servidor import SERVIDOR
from chastack_bdd.errores import * 

import flask as fl
from flask.templating import TemplateNotFound
from werkzeug.exceptions import HTTPException, BadRequest, NotFound
import traceback


class ErrorDialogo(Exception): ...

@SERVIDOR.errorhandler(TemplateNotFound)
def manejarPlantillaNoExiste(e):
    servidor.logger.error(f'--- {solicitud.full_path} => {solicitud.endpoint}() --- \n {type(e)} {e} \n {traceback.format_exc()}')
    
@SERVIDOR.errorhandler(FileNotFoundError)
def manejarArchivoNoEncontrado(e):
    servidor.logger.debug(f'--- {solicitud.full_path} => {solicitud.endpoint}() --- \n {type(e)} {e} \n {traceback.format_exc()}')
    
@SERVIDOR.errorhandler(404)
def manejar404(e): 
    servidor.logger.debug(f'--- {solicitud.full_path} => {solicitud.endpoint}() --- \n {type(e)} {e}')
    return fl.render_template(
        f"errores/404.html.j2",
        USUARIO = g.esteUsuario
    )
    return crearRespuesta(msj,404)



@SERVIDOR.errorhandler(ErrorBDD)
def manejarErrorBDD(e):
    import traceback
    servidor.logger.error(f"{e} \n {traceback.format_exc()}")
    respuesta = crearRespuesta("",429)
    respuesta.headers['Retry-After'] = 1
    return respuesta

@SERVIDOR.errorhandler(500)
@SERVIDOR.errorhandler(AssertionError)
@SERVIDOR.errorhandler(Exception)
@SERVIDOR.errorhandler(ErrorMalaSolicitud)
@SERVIDOR.errorhandler(SinResultado)
@SERVIDOR.errorhandler(ErrorDialogo)
def manejar500(e):
    servidor.logger.error(f'[500] --- {solicitud.full_path} => {solicitud.endpoint}() --- \n {type(e)} {e} \n {traceback.format_exc()}')
    fl.flash(f'No pudimos procesar tu solicitud. {e}')
    respuesta = crearRespuesta(
        fl.render_template(
            "errores/500.html.j2",
            ERROR = f'No pudimos procesar tu solicitud. {e}'
        )
    )
    return respuesta
    