# Polizador

Sistema de gestión para la administración de anticipos de viáticos.

## Descripción

Polizador es una aplicación web desarrollada en Django que permite gestionar distintos trámites internos para el Instituto Provincial de Desarrollo Urbano y Vivienda:
- Solicitudes de comisiones de servicio.
- Gestión de anticipos de viáticos.
- Instrumentos legales (decretos y resoluciones).
- Vehículos propiedad del instituto y de terceros en uso en comisiones de servicio.
- Incorporaciones a solicitudes ya aprobadas con instrumento legal.
- Reportes y estadísticas.

## Características Principales

- Gestión completa de solicitudes y comisionados
- Cálculo automático de montos a anticipar en viáticos.
- Generación de resoluciones en formato Word.
- Interfaz web intuitiva.
- Reportes personalizados.
- OCR para procesamiento de documentos.
- Respaldo automático de base de datos.

## Requisitos del Sistema

- Python 3.x
- PostgreSQL
- Nginx (para producción)
- Dependencias listadas en `requirements.txt`

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
pip install -r requirements.txt
```

4. Configurar la base de datos:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Estructura del Proyecto

- `polizador/`: Directorio principal del proyecto
  - `carga/`: Aplicación para el seguimiento de obras (Obsoleto)
  - `secretariador/`: Gestión de documentos y comisiones de servicio.
  - `personalizador/`: App para la gestión de recursos humanos.
  - `templates/`: Plantillas HTML
  - `static_files/`: Archivos estáticos (CSS, JS, imágenes)

## Características Técnicas

- Framework: Django
- Base de datos: PostgreSQL
- Frontend: HTML, CSS, JavaScript
- Generación de documentos: python-docx
- OCR: Tesseract
- Servidor web: Nginx (producción)

## Mantenimiento

El proyecto incluye:
- Scripts de respaldo automático
- Sistema de logging
- Validadores personalizados
- Manejo de permisos y roles

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

GNU GENERAL PUBLIC LICENSE Version 3

## Contacto

