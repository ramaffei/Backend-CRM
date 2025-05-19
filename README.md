# BACKEND Para proyecto de APP web CRM

Este proyecto es un backend para un sistema CRM (Customer Relationship Management) desarrollado con Flask en Python.

## Estructura del Proyecto

- `entrypoint.py`: Punto de entrada principal de la aplicación.
- `app/`: Contiene la lógica principal de la aplicación, módulos, utilidades y manejo de errores.
- `config/`: Archivos de configuración para diferentes entornos (desarrollo, producción, testing, etc).
- `migrations/`: Archivos de migración de base de datos gestionados por Alembic.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd Backend-CRM
   ```
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno según el archivo de configuración deseado en la carpeta `config/`.

## Migraciones de Base de Datos

Para aplicar migraciones:
```bash
flask db upgrade
```

Para crear una nueva migración:
```bash
flask db migrate -m "Descripción de la migración"
```

## Ejecución

Puedes iniciar la aplicación ejecutando:
```bash
python entrypoint.py
```
O usando un servidor WSGI como Gunicorn o uWSGI con el archivo `flaskapp.wsgi`.

## Estructura de Módulos

- `caja`, `clientes`, `empleados`, `login`, `turnos`, `ventas`: Cada uno contiene recursos y esquemas para la API REST.

## Contribución

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad o corrección de bug.
3. Realiza tus cambios y haz commit.
4. Envía un Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT.

## ✨ Autor

Rodrigo Maffei.

[Github](https://www.github.com/ramaffei)

[Linkedin](https://www.linkedin.com/in/ramaffei)