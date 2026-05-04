# 🧬 GeneticApp

App web de consulta sobre **enfermedades genéticas y sus medicamentos**, construida con Flask + MySQL usando el framework **Ch'askapp**.

---

## ¿Para qué sirve?

Permite registrar y consultar enfermedades genéticas (gen afectado, tipo de herencia, síntomas) y los medicamentos asociados a cada una. Incluye CRUD completo para ambas entidades.

---

## Stack

- **Python 3.13** — Lenguaje principal
- **Flask** — Framework web
- **MySQL** — Base de datos
- **Ch'askapp** — Herramientas de desarrollo (stack PYFAMUX)
- **HTMX** — Navegación sin recarga de página

---

## Requisitos previos

- [Ch'askapp](https://github.com/hernanatn/chastack) instalado
- MySQL Server activo
- Python 3.13+

---

## Instalación

### 1 — Clonar el repositorio

```bash
git clone https://github.com/juliadesantos/Geneticapp.git
cd Geneticapp
```

### 2 — Crear la base de datos

Abrí MySQL (Workbench o Command Line) y ejecutá estos archivos **en orden**:

```sql
source fuente/geneticapp/bdd/bdd.sql
source fuente/geneticapp/bdd/globales.sql
source fuente/geneticapp/bdd/enfermedades.sql
source fuente/geneticapp/bdd/medicamentos.sql
```

> ⚠️ **Puerto MySQL distinto al 3306**
>
> Si tu MySQL no corre en el puerto estándar 3306, editá `fuente/geneticapp/servidor/config.py`
> y cambiá el número de puerto en el parche `PARAMETROS_CONEXION`:
>
> ```python
> type(CONFIG_BDD).PARAMETROS_CONEXION = property(lambda self: {
>     ...
>     "port": 3306,  # ← cambiá este número por tu puerto
>     ...
> })
> ```

### 3 — Correr la app

```bash
chaskapp correr
```

La app estará disponible en: **http://127.0.0.1:6969**

---

## Uso

| URL | Descripción |
|-----|-------------|
| `/` | Página principal |
| `/enfermedades/` | Listado de enfermedades |
| `/enfermedades/nueva` | Crear nueva enfermedad |
| `/enfermedades/<id>` | Ver detalle |
| `/enfermedades/<id>/editar` | Editar |
| `/medicamentos/` | Listado de medicamentos |
| `/medicamentos/nuevo` | Crear nuevo medicamento |
| `/medicamentos/<id>` | Ver detalle |
| `/medicamentos/<id>/editar` | Editar |

---

## Estructura del proyecto

```
geneticapp/
├── fuente/
│   └── geneticapp/
│       ├── bdd/                  # Modelos y esquemas SQL
│       │   ├── enfermedades.py   # Modelo Enfermedad
│       │   ├── enfermedades.sql  # Tabla Enfermedad
│       │   ├── medicamentos.py   # Modelo Medicamento
│       │   ├── medicamentos.sql  # Tabla Medicamento
│       │   └── .sintetico/       # Datos de prueba
│       ├── servidor/
│       │   ├── config.py         # Configuración y conexión BDD
│       │   ├── plantillas/       # Templates HTML (Jinja2)
│       │   └── planos/
│       │       ├── enfermedades/ # Blueprint enfermedades (CRUD)
│       │       └── medicamentos/ # Blueprint medicamentos (CRUD)
│       └── pruebas/              # Tests
└── README.md
```

---

## Otros comandos

```bash
chaskapp probar      # Ejecutar pruebas
chaskapp minificar   # Minificar CSS y JS
```

---

*Proyecto creado con [Ch'askapp](https://github.com/hernanatn/chastack)*
