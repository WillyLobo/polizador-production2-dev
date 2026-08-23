# Polizador

Sistema de gestión interna para el **Instituto Provincial de Desarrollo Urbano y Vivienda (IPDUV)**.

## Descripción

Polizador es una aplicación web desarrollada en Django que gestiona varios trámites internos del instituto:

- **Viáticos** (`secretariador`): solicitudes de comisión de servicio, anticipos de viáticos, instrumentos legales (decretos y resoluciones) con generación de documentos Word, vehículos propios y de terceros, incorporaciones a solicitudes ya aprobadas.
- **Obras públicas** (`carga`): contratos de obra, certificados mensuales de avance, planes de trabajo, fojas de medición, representantes técnicos y pólizas de seguro.
- **RRHH** (`personalizador`): usuarios (`CustomUser`), agentes y estructura organizativa (gerencias, direcciones, departamentos, oficinas, categorías).
- **API** (`api`): API interna en `django-ninja` (montada en `/v1/api/`) que expone datos de las apps anteriores, usada sobre todo para widgets `select2` y búsquedas cruzadas entre apps.

## Características Principales

- Gestión completa de solicitudes de comisión de servicio y comisionados.
- Cálculo automático de montos a anticipar en viáticos.
- Generación de resoluciones y otros documentos en formato Word (`docxtpl`).
- OCR de instrumentos legales vía Google Cloud Vision / Document AI (comandos de gestión, no en tiempo de request).
- Almacenamiento dual de archivos: Google Cloud Storage + disco local.
- Auditoría de cambios sobre los modelos principales (`django-simple-history`).
- Autenticación vía `django-allauth`.
- Reportes y estadísticas.

## Requisitos del Sistema

- Python 3.x
- PostgreSQL con la extensión **PostGIS** (el proyecto usa `django.contrib.gis`; ver `scripts/setup_postgis.sh`)
- Redis (cache por defecto y cache de `select2`)
- Nginx + Gunicorn (para producción)
- Dependencias listadas en `requirements.txt` (generado a partir de `requirements.in` con `pip-compile`)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Crear y activar entorno virtual:
```bash
python -m venv env
source env/bin/activate  # En Linux/Mac
```

3. Instalar dependencias:
```bash
cd polizador
pip install -r requirements.txt
```
Para agregar o actualizar dependencias, editar `requirements.in` y regenerar `requirements.txt` con `pip-compile` (no editar `requirements.txt` a mano).

4. Configurar variables de entorno: crear un archivo `.env` dentro de `polizador/` con, como mínimo:
```
DEBUG=
SECRET_KEY=
ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=
DBHOST=
DBUSER=
DBNAME=
DBPASSWORD=
CACHE_URL=
REDIS_URL=
SENTRY_DSN=
MAILGUN_API_KEY=
MAILGUN_SENDER_DOMAIN=
```

5. Configurar la base de datos (requiere PostGIS ya instalado en el motor Postgres):
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Tests

```bash
python manage.py test                      # todas las apps
python manage.py test carga                # una app
python manage.py test api.tests.test_api   # un módulo
```

## Estructura del Proyecto

Todo el código vive bajo `polizador/` (el paquete del proyecto Django es `polizador/polizador/`):

- `carga/`: obras públicas.
- `secretariador/`: viáticos, comisiones de servicio e instrumentos legales.
- `personalizador/`: RRHH.
- `api/`: API interna en `django-ninja`.
- `core/`: utilidades y funcionalidad compartida entre apps.
- `templates/`: plantillas HTML compartidas.
- `static_files/`: archivos estáticos (CSS, JS, imágenes).
- `scripts/`: scripts de mantenimiento (p. ej. `setup_postgis.sh`).

## Características Técnicas

- Framework: Django (con `django.contrib.gis` / GeoDjango)
- Base de datos: PostgreSQL + PostGIS
- Cache: Redis
- Frontend: HTML, CSS, JavaScript (jQuery, DataTables, select2)
- Generación de documentos: `docxtpl` / `python-docx`
- OCR: Google Cloud Vision y Document AI
- Almacenamiento: Google Cloud Storage + local
- Email: Mailgun (vía `django-anymail`)
- Errores: Sentry (solo con `DEBUG=False`)
- Servidor web: Nginx + Gunicorn (producción)

## Mantenimiento

El proyecto incluye:
- Auto-numeración de campos secuenciales vía signals (p. ej. número de foja de medición).
- Sistema de logging.
- Validadores personalizados (`secretariador/functions.py`).
- Manejo de permisos y roles (`PermissionRequiredMixin`, grupos).
- Auditoría de cambios (`django-simple-history`).

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

GNU GENERAL PUBLIC LICENSE Version 3

## Contacto

