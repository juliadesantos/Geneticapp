# geneticapp

Proyecto creado con Ch'astack.

## Stack

Este proyecto utiliza el stack **PYFAMUX** (Python + Flask + MySQL + Ch'astack):

- **Python 3.13** - Lenguaje principal
- **Flask** - Framework web
- **MySQL** - Base de datos
- **Ch'astack** - Herramientas de desarrollo

## Requisitos

- [Ch'astack](https://github.com/hernanatn/chastack) instalado
- MySQL Server (Ch'astack lo instala automáticamente)
- Python 3.13+ (gestionado por Ch'astack)

## Instalación

1. Clone el repositorio:
```bash
git clone <url-del-repositorio>
cd geneticapp
```

2. Inicialice el entorno con Ch'astack:
```bash
chastack inicializar
```

3. La base de datos se crea automáticamente. Si necesita resetearla:
```bash
chastack resetear-bdd
```

## Desarrollo

### Ejecutar servidor de desarrollo

```bash
chastack correr
```

El servidor estará disponible en:
- Local: http://localhost:6969
- LAN: http://0.0.0.0:6969

### Ejecutar pruebas

```bash
chastack probar
```

### Minificar estáticos

```bash
chastack minificar
```

## Estructura del proyecto

```
geneticapp/
├── .secretos/              # Secretos del proyecto (ignorado por git)
│   ├── pimienta            # Token de seguridad
│   └── llave               # Llave secreta
├── docs/                   # Documentación
├── fuente/
│   └── geneticapp/
│       ├── bdd/            # Scripts y modelos de base de datos
│       ├── cerebro/        # Lógica de negocio
│       ├── pruebas/        # Pruebas unitarias e integración
│       ├── servidor/       # Aplicación Flask
│       │   ├── estatico/   # Archivos estáticos (CSS, JS)
│       │   ├── plantillas/ # Plantillas Jinja2
│       │   └── planos/     # Blueprints de Flask
│       └── utiles/         # Utilidades compartidas
└── README.md
```

## Planos (Blueprints)


Este proyecto incluye los siguientes planos:

- **Enfermedades**: `/enfermedades/`
- **Medicamentos**: `/medicamentos/`
- **geneticapp**: `/geneticapp/`



## Configuración de entornos

### Desarrollo
- Base de datos: `geneticapp_desarrollo`
- Puerto: 6969
- Debug: Activado





## Variables de entorno

El proyecto utiliza las siguientes variables de entorno:

| Variable | Descripción |
|----------|-------------|
| `AMBIENTE_GENETICAPP` | Ambiente actual (DESARROLLO, ESCENIFICACION, PRODUCCION) |
| `PIMIENTA` | Token de seguridad para hashing |
| `LLAVE_SECRETA` | Llave secreta para sesiones Flask |


## Licencia

[Especificar licencia]

---

*Proyecto creado con [Ch'astack](https://github.com/hernanatn/chastack)*
