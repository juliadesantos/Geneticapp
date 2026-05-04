"""
Punto de entrada para ejecutar las pruebas de geneticapp.

Ejecutar con:
    python -m pruebas

O desde chastack:
    chastack probar
"""

import unittest
import sys
import os
import traceback

# Agregar el directorio fuente al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pruebas.config_pruebas import (
    crearBaseDeDatosPruebas,
    destruirBaseDeDatosPruebas,
    poblarTablasPruebas,
    CI
)

def descubrirPruebas():
    """Descubre y carga todas las pruebas en el directorio pruebas/"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Buscar todas las pruebas en el directorio actual
    directorio_pruebas = os.path.dirname(__file__)
    tests = loader.discover(
        start_dir=directorio_pruebas,
        pattern='test_*.py',
        top_level_dir=os.path.join(directorio_pruebas, '..')
    )
    suite.addTests(tests)

    return suite

def ejecutarPruebas(verbosidad: int = 2) -> bool:
    """
    Ejecuta todas las pruebas del proyecto.

    Args:
        verbosidad: Nivel de detalle en la salida (0-2)

    Returns:
        True si todas las pruebas pasaron, False si hubo fallos
    """
    suite = descubrirPruebas()
    runner = unittest.TextTestRunner(verbosity=verbosidad)
    resultado = runner.run(suite)
    return resultado.wasSuccessful()

def main():
    """Función principal que configura, ejecuta y limpia las pruebas."""
    exito = False

    print("=" * 60)
    print("  PRUEBAS DE GENETICAPP")
    print("=" * 60)
    print()

    if CI:
        print("[CI] Ejecutando en entorno de integración continua")

    try:
        # 1. Crear base de datos de pruebas
        print("[1/4] Creando base de datos de pruebas...")
        crearBaseDeDatosPruebas()
        print("      Base de datos creada.")

        # 2. Poblar tablas con datos de prueba
        print("[2/4] Poblando tablas con datos de prueba...")
        poblarTablasPruebas()
        print("      Tablas pobladas.")

        # 3. Ejecutar pruebas
        print("[3/4] Ejecutando pruebas...")
        print("-" * 60)
        exito = ejecutarPruebas()
        print("-" * 60)

    except Exception as e:
        print(f"\n[ERROR] Error durante la ejecución de pruebas:")
        print(f"        {e}")
        print(traceback.format_exc())
        exito = False

    finally:
        # 4. Limpiar base de datos de pruebas
        print("[4/4] Limpiando base de datos de pruebas...")
        try:
            destruirBaseDeDatosPruebas()
            print("      Base de datos eliminada.")
        except Exception as e:
            print(f"      [ADVERTENCIA] No se pudo eliminar la base de datos: {e}")

    print()
    print("=" * 60)
    if exito:
        print("  RESULTADO: TODAS LAS PRUEBAS PASARON")
    else:
        print("  RESULTADO: ALGUNAS PRUEBAS FALLARON")
    print("=" * 60)

    sys.exit(0 if exito else 1)

if __name__ == "__main__":
    main()
