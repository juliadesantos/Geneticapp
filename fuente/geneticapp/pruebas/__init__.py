"""
Módulo de pruebas para geneticapp.

Este módulo contiene las pruebas unitarias y de integración
completamente desacopladas de la base de datos de desarrollo.

Ejecutar con:
    python -m pruebas

O desde chastack:
    chastack probar
"""

from pruebas.config_pruebas import (
    CONFIG_BDD_PRUEBAS,
    crearBaseDeDatosPruebas,
    destruirBaseDeDatosPruebas,
    poblarTablasPruebas
)

__all__ = [
    'CONFIG_BDD_PRUEBAS',
    'crearBaseDeDatosPruebas',
    'destruirBaseDeDatosPruebas',
    'poblarTablasPruebas'
]
