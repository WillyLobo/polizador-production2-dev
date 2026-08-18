---
symbol: CustomUser
kind: class
module: personalizador/models.py
lines: 24-34
signature_hash: sha1:37dca6c9fadb757c57234b0a6243a72b3314bdf7
authored: true
---

# CustomUser

**Módulo:** `personalizador/models.py` (líneas 24-34) · hereda de `AbstractUser`

## Propósito

`AUTH_USER_MODEL` del proyecto (`AbstractUser` de Django + `first_name`/`last_name`
redeclarados con label en español, más `usuario_dni` opcional). Es el modelo de
autenticación (login/permisos), separado de [Agente](Agente.md) (el registro de RRHH) —
`Agente.agente_usuario` es el `OneToOneField` que los vincula cuando un empleado tiene
cuenta en el sitio, pero un `CustomUser` puede existir sin `Agente` (ej. una cuenta de
proveedor externo) y viceversa (un `Agente` cargado en RRHH sin acceso al sitio).

## Firma

```python
class CustomUser(AbstractUser):
```

## Uso real

`settings.AUTH_USER_MODEL`; `CustomUserForm` (`personalizador/forms/customuserform.py`) lo usa para el signup de `django-allauth`.

## Ver también

- [Agente](Agente.md)
