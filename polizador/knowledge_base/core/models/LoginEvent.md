---
symbol: LoginEvent
kind: class
module: core/models.py
lines: 143-154
signature_hash: sha1:444552195965df57706e1a82f589fe71a09eeadd
authored: true
---
# LoginEvent

**Módulo:** `core/models.py` (líneas 143-154) · hereda de `models.Model`

## Propósito

Un inicio de sesión registrado (usuario + timestamp + IP), usado para graficar actividad de usuarios en `DashboardView` (`login_summary`/`recent_logins`, en `core/dashboard_data.py`, fuera del alcance de este manifest).

## Firma

```python
class LoginEvent(models.Model):
```

## Uso real

`registrar_login` (`core/signals.py`, mismo módulo más abajo) crea una instancia en cada `user_logged_in`.

## Ver también

- [registrar_login](../signals/registrar_login.md)
- [DashboardView](../views/DashboardView.md)