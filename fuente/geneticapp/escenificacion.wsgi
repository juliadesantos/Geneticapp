import sys
import os


raiz = os.path.abspath(os.path.dirname(__file__))
servidor = os.path.join(raiz,'servidor')
cerebro = os.path.join(raiz,'cerebro')
bdd = os.path.join(raiz,'bdd')

sys.path.insert(0, raiz)
sys.path.insert(0, servidor)
sys.path.insert(0, cerebro)
sys.path.insert(0, bdd)

def leerSecreto(nombre_archivo):
    ruta = os.path.join(raiz, '..', '..', '.secretos', nombre_archivo)
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read().strip()

os.environ['AMBIENTE_GENETICAPP'] = 'ESCENIFICACION'
os.environ['PIMIENTA'] = leerSecreto('pimienta')
os.environ['LLAVE_SECRETA'] = leerSecreto('llave')

from fidelizapp import servidor as application