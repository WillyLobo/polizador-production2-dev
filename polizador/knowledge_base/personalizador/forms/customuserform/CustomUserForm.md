---
symbol: CustomUserForm
kind: class
module: personalizador/forms/customuserform.py
lines: 5-24
signature_hash: sha1:352f283dc46610c557077600a48090dfe25883d6
authored: true
---

# CustomUserForm

**Módulo:** `personalizador/forms/customuserform.py` (líneas 5-24) · hereda de `SignupForm, forms.ModelForm`

## Propósito

Form de signup de `django-allauth`, no un `ModelForm` de administración: hereda de
`SignupForm` (de allauth) **y** `forms.ModelForm` a la vez, para agregar `first_name`/
`last_name` al flujo estándar de registro de cuenta del sitio. `save(request)` delega en
`SignupForm.save()` (que crea el `CustomUser` con allauth) y solo agrega la asignación de
nombre/apellido antes de devolver el usuario creado.

## Firma

```python
class CustomUserForm(SignupForm, forms.ModelForm):
```

## Uso real

Configurado como `ACCOUNT_FORMS['signup']` (o equivalente) en `settings.py`, usado por las vistas de signup de `allauth.account`.

## Ver también

- [CustomUser](../../models/CustomUser.md)
