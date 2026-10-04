---
symbol: CustomUser
kind: class
module: personalizador/models.py
lines: 25-73
signature_hash: sha1:35cfd56a1ab4d6b356d1a83d5256e25f24a91d40
authored: true
---

# CustomUser

**Módulo:** `personalizador/models.py` (líneas 25-73) · hereda de `AbstractUser`

## Propósito

`AUTH_USER_MODEL` del proyecto (`AbstractUser` de Django + `first_name`/`last_name`
redeclarados con label en español, más `usuario_dni` opcional). Es el modelo de
autenticación (login/permisos), separado de [Agente](Agente.md) (el registro de RRHH) —
`Agente.agente_usuario` es el `OneToOneField` que los vincula cuando un empleado tiene
cuenta en el sitio, pero un `CustomUser` puede existir sin `Agente` (ej. una cuenta de
proveedor externo) y viceversa (un `Agente` cargado en RRHH sin acceso al sitio).

**Vínculo con el Active Directory.** El `username` de polizador casi nunca coincide con la
cuenta de red: hay apodos y hasta correos personales (ver `manage.py auditar_usuarios_ad`).
Por eso el mapeo no se adivina: cada usuario vincula su propia cuenta desde
`core/views_vincular_ad.py` escribiendo sus credenciales de red, y el bind contra el AD
prueba que las dos identidades son suyas.
- `ad_username` es el `sAMAccountName` que devolvió el AD, no lo que tipeó el usuario. Es
  `unique` con `null=True` (no `""`): Postgres admite muchos NULL bajo una restricción única
  pero un solo `""`.
- `ad_vinculado_en` es la fecha del vínculo.
- `ad_sin_cuenta_red` es la salida para quien no tiene cuenta de red. Lo marca para que lo
  revise un administrador (filtro en el admin) y `VincularADMiddleware` deja de mandarlo a
  la página de vinculación.

`solo_ldap` es verdadero cuando el usuario tiene `ad_username` **y** ya no tiene contraseña
local utilizable, el estado en que lo deja `manage.py retirar_password_local`. Tener
`ad_username` no alcanza: durante la transición mucha gente está vinculada y conserva su
contraseña. `core/adapters.py` y la vista de cambio de contraseña lo usan para impedir que
alguien vuelva a habilitar la contraseña local. Si eso pasara, desactivar a la persona en
el AD dejaría de quitarle el acceso.

El historial (`usuario_history`) es un `M2MHistoricalRecords` que también audita `groups` y
`user_permissions`.

## Firma

```python
class CustomUser(AbstractUser):
```

## Uso real

`settings.AUTH_USER_MODEL`; `CustomUserForm` (`personalizador/forms/customuserform.py`) lo usa para el signup de `django-allauth`.

## Ver también

- [Agente](Agente.md)

- [LoginEvent](../../core/models/LoginEvent.md) — `backend` registra con qué backend entró cada login.
