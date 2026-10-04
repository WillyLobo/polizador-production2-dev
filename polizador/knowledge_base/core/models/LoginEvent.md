---
symbol: LoginEvent
kind: class
module: core/models.py
lines: 143-167
signature_hash: sha1:b358a3c7a3a520940776ce298b45f2431d9a8c55
authored: true
---
# LoginEvent

**Módulo:** `core/models.py` (líneas 143-167) · hereda de `models.Model`

## Propósito

Un inicio de sesión registrado (usuario + timestamp + IP), usado para graficar actividad de usuarios en `DashboardView` (`login_summary`/`recent_logins`, en `core/dashboard_data.py`, fuera del alcance de este manifest).

`backend` guarda la ruta completa del backend que autenticó (la que Django deja en
`user.backend`), vacía en las filas anteriores a que existiera el campo. `por_ldap` es
`backend.endswith("LDAPBackend")`. Para eso se agregó: `manage.py retirar_password_local`
sólo le quita la contraseña local a un usuario después de haberlo visto entrar por LDAP al
menos una vez, y ese "haberlo visto" se comprueba con estas filas.

## Firma

```python
class LoginEvent(models.Model):
```

## Uso real

`registrar_login` (`core/signals.py`, mismo módulo más abajo) crea una instancia en cada `user_logged_in`.

## Ver también

- [registrar_login](../signals/registrar_login.md)
- [DashboardView](../views/DashboardView.md)

- [CustomUser](../../personalizador/models/CustomUser.md) — `ad_username`/`solo_ldap`.
