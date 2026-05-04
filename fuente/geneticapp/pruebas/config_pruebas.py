"""
Configuración de base de datos para pruebas de geneticapp.

Este módulo proporciona una base de datos completamente separada
de la de desarrollo/producción para ejecutar pruebas de forma segura.
"""

import os
import traceback
import subprocess
from pathlib import Path
import mysql.connector
from mysql.connector import Error
from chastack_bdd import ConfigMySQL, BaseDeDatos_MySQL

# Detectar si estamos en CI (GitHub Actions, etc.)
CI = os.environ.get("CI", "false").lower() == "true"

# Configuración de conexión
MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1") if CI else "localhost"
MYSQL_ROOT_PASSWORD = os.environ.get("MYSQL_ROOT_PASSWORD", "Ro0t.@My5ql!")

# Nombre de la base de datos de pruebas (único para este proyecto)
NOMBRE_BDD_PRUEBAS = "geneticapp_pruebas"
USUARIO_PRUEBAS = "geneticapp_test"
PASSWORD_PRUEBAS = "pRU3b4s!geneticapp!1234"

# Configuración de BDD para pruebas
CONFIG_BDD_PRUEBAS = ConfigMySQL(
    MYSQL_HOST,
    USUARIO_PRUEBAS,
    PASSWORD_PRUEBAS,
    NOMBRE_BDD_PRUEBAS,
)

# Rutas a los scripts SQL
RUTA_PRUEBAS = Path(__file__).parent
RUTA_BDD = RUTA_PRUEBAS.parent / "bdd"
SCRIPT_MONTAR = RUTA_PRUEBAS / "montar_pruebas.sql"
SCRIPT_DESMONTAR = RUTA_PRUEBAS / "desmontar_pruebas.sql"


def obtenerConexionRoot():
    """Obtiene una conexión como root para administrar la BDD de pruebas."""
    if not MYSQL_ROOT_PASSWORD:
        raise ValueError(
            "No se encontró MYSQL_ROOT_PASSWORD en las variables de entorno. "
            "Defina esta variable para poder crear/destruir la base de datos de pruebas."
        )

    return mysql.connector.connect(
        host=MYSQL_HOST,
        user="root",
        password=MYSQL_ROOT_PASSWORD
    )


def ejecutarScriptSQL(ruta_script: Path, base_datos: str = None):
    """
    Ejecuta un script SQL usando mysql cli.

    Args:
        ruta_script: Ruta al archivo .sql a ejecutar
        base_datos: Base de datos a usar (opcional)
    """
    if not ruta_script.exists():
        raise FileNotFoundError(f"Script SQL no encontrado: {ruta_script}")

    cmd = ["mysql", "-u", "root", f"-p{MYSQL_ROOT_PASSWORD}", "-h", MYSQL_HOST]
    if base_datos:
        cmd.append(base_datos)

    with open(ruta_script, "r", encoding="utf-8") as f:
        contenido = f.read()

    result = subprocess.run(
        cmd,
        input=contenido,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Error ejecutando {ruta_script}: {result.stderr}")


def crearBaseDeDatosPruebas():
    """
    Crea la base de datos y usuario de pruebas ejecutando el script SQL amalgamado.

    Requiere que MYSQL_ROOT_PASSWORD esté definida en el entorno.
    """
    # 1. Ejecutar script principal de montado
    ejecutarScriptSQL(SCRIPT_MONTAR)

    # 2. Ejecutar scripts adicionales de bdd (excepto bdd.sql y globales.sql que ya están en montar_pruebas.sql)
    if RUTA_BDD.exists():
        for archivo_sql in sorted(RUTA_BDD.glob("*.sql")):
            if archivo_sql.name in ["bdd.sql", "globales.sql", "montar_pruebas.sql", "desmontar_pruebas.sql"]:
                continue
            try:
                ejecutarScriptSQL(archivo_sql, NOMBRE_BDD_PRUEBAS)
            except Exception as e:
                print(f"Advertencia: Error ejecutando {archivo_sql.name}: {e}")

    # 3. Ejecutar scripts de datos sintéticos
    ruta_sintetico = RUTA_BDD / ".sintetico"
    if ruta_sintetico.exists():
        for archivo_sql in sorted(ruta_sintetico.glob("*.sql")):
            try:
                ejecutarScriptSQL(archivo_sql, NOMBRE_BDD_PRUEBAS)
            except Exception as e:
                print(f"Advertencia: Error ejecutando datos sintéticos {archivo_sql.name}: {e}")


def destruirBaseDeDatosPruebas():
    """
    Elimina la base de datos y usuario de pruebas ejecutando el script SQL.

    Requiere que MYSQL_ROOT_PASSWORD esté definida en el entorno.
    """
    ejecutarScriptSQL(SCRIPT_DESMONTAR)


def poblarTablasPruebas():
    """
    Crea las tablas y datos iniciales para pruebas.

    Esta función ejecuta los scripts de bdd/.sintetico/ para poblar
    con datos de prueba. Los programadores deben agregar archivos .sql
    en ese directorio con los datos sintéticos necesarios.
    """
    ruta_sintetico = RUTA_BDD / ".sintetico"

    if not ruta_sintetico.exists():
        print(f"Nota: No existe directorio {ruta_sintetico}, creándolo...")
        ruta_sintetico.mkdir(parents=True, exist_ok=True)
        # Crear archivo ejemplo
        ejemplo = ruta_sintetico / "_ejemplo.sql"
        ejemplo.write_text("""-- Ejemplo de archivo de datos sintéticos
-- Renombre este archivo quitando el _ inicial y agregue sus datos de prueba
-- Los archivos en este directorio se ejecutan al montar la BDD de pruebas

-- INSERT INTO MiTabla (campo1, campo2) VALUES ('valor1', 'valor2');
""", encoding="utf-8")
        return

    for archivo_sql in sorted(ruta_sintetico.glob("*.sql")):
        # Saltar archivos que empiezan con _
        if archivo_sql.name.startswith("_"):
            continue
        try:
            ejecutarScriptSQL(archivo_sql, NOMBRE_BDD_PRUEBAS)
        except Exception as e:
            print(f"Error poblando con {archivo_sql.name}: {e}")


def devolverBDDPruebas() -> BaseDeDatos_MySQL:
    """
    Devuelve una instancia de BaseDeDatos_MySQL configurada para pruebas.

    Returns:
        Instancia de BaseDeDatos_MySQL conectada a la BDD de pruebas
    """
    return BaseDeDatos_MySQL(CONFIG_BDD_PRUEBAS)
