import os
import json
import chastack_bdd as chbdd

# Ch'astack
LLAVE_SECRETA = os.environ.get('LLAVE_SECRETA_')
PIMIENTA = os.environ.get('PIMIENTA')
GMAIL_CUENTA_DE_SERVICIO = json.loads(os.environ.get('GMAIL_CUENTA_DE_SERVICIO','{}'))
GMAIL_REMITENTE = os.environ.get('GMAIL_REMITENTE')

# Flask
SECRET_KEY = os.environ.get('LLAVE_SECRETA')
SESSION_COOKIE_SAMESITE='None'
SESSION_COOKIE_SECURE = True

AMBIENTE_GENETICAPP = os.environ.get('AMBIENTE_GENETICAPP')
if not AMBIENTE_GENETICAPP or AMBIENTE_GENETICAPP == 'DESARROLLO':
    URL_BASE='http://127.0.0.1:6969'
    CSS = 'css'
    CONFIG_BDD : chbdd.ConfigMySQL = chbdd.ConfigMySQL(
        "localhost",
        "servidor_local_geneticapp",
        "S3rv1d0r@.geneticapp!",
        "geneticapp_desarrollo",
    )
    type(CONFIG_BDD).PARAMETROS_CONEXION = property(lambda self: {
        "host": "localhost",
        "user": "servidor_local_geneticapp",
        "password": "S3rv1d0r@.geneticapp!",
        "database": "geneticapp_desarrollo",
        "port": 3307,
        "use_pure": False,
    })
    EXPLAIN_TEMPLATE_LOADING = True
elif AMBIENTE_GENETICAPP in ('PROTOTIPO','DEMO','ESCENIFICACION'):
    URL_BASE=''
    CSS = 'min-css'
    CDN_DOMAIN = ''
    CDN_HTTPS = True
    CONFIG_BDD : chbdd.ConfigMySQL = chbdd.ConfigMySQL(
        "localhost", 
        "servidor_local_geneticapp", 
        "S3rv1d0r@.geneticapp!", 
        "geneticapp_escenificacion",
    ) # HACER: Cambiar a config escenificación
    EXPLAIN_TEMPLATE_LOADING = True
elif AMBIENTE_GENETICAPP == 'PRODUCCION':
    URL_BASE=''
    CSS = 'min-css'
    CDN_DOMAIN = ''
    CDN_HTTPS = True
    CONFIG_BDD : chbdd.ConfigMySQL = chbdd.ConfigMySQL(
        "localhost", 
        "servidor_local_geneticapp", 
        "S3rv1d0r@.geneticapp!", 
        "geneticapp_produccion",
    ) # HACER: Cambiar a config producción
#CACHE_OPTIONS='777'

