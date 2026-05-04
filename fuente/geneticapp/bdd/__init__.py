import chastack_bdd as chbdd
def devolverBDD() -> chbdd.BaseDeDatos_MySQL:
    from geneticapp.servidor.config import (
        CONFIG_BDD
    )
    return chbdd.BaseDeDatos_MySQL(CONFIG_BDD)

def registrarBddGlobal(bdd : chbdd.BaseDeDatos_MySQL, g):
    g.bdd = bdd
    return g.bdd
