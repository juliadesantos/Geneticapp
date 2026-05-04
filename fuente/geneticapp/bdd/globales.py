from chastack_bdd import Tabla
from geneticapp.bdd import devolverBDD

class Globales(metaclass=Tabla):
    ...

GLOBALES = Globales(devolverBDD(),1)