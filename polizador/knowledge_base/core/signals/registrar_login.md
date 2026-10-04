---
symbol: registrar_login
kind: function
module: core/signals.py
lines: 15-28
signature_hash: sha1:e3fa737410aa76835fc37cf5c53555629948dc18
authored: true
---

# registrar_login

**Módulo:** `core/signals.py` (líneas 15-28)

## Propósito

Receiver de la señal estándar de Django `user_logged_in`: crea un `LoginEvent` en cada inicio de sesión exitoso, para poder graficar actividad de usuarios en el dashboard — el único uso de señales propio de `core` (todas las de `carga`/`secretariador` son sobre modelos de negocio; esta es sobre autenticación).

También guarda en `LoginEvent.backend` con qué backend entró el usuario (`getattr(user, "backend", "")`). `authenticate()` deja esa ruta en `user.backend` antes de emitir la señal, así que acá ya está disponible. Esa fila es la prueba de que la persona ya puede entrar por LDAP, condición para que `retirar_password_local` le quite después la contraseña local.

## Firma

```python
def registrar_login(sender, request, user, **kwargs):
```

## Uso real

Se dispara solo, en cada login exitoso (cualquier vista de `allauth` o `django.contrib.auth`) — no se llama directamente.

## Flujo de datos

```mermaid
sequenceDiagram
    participant U as Usuario (login)
    participant D as django.contrib.auth / allauth
    participant S as registrar_login
    participant L as LoginEvent

    U->>D: credenciales válidas
    D-->>S: user_logged_in
    S->>S: _client_ip(request)
    S->>L: LoginEvent.objects.create(user, ip_address, backend)
```

## Ver también

- [LoginEvent](../models/LoginEvent.md)
- [_client_ip](_client_ip.md)
