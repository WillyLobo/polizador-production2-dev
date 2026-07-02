# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Polizador is a Django web app for the Instituto Provincial de Desarrollo Urbano y Vivienda (IPDUV). It manages:
- **carga**: public works (obras) — contracts, monthly certificados (progress certificates), planes de trabajo, fojas de medición (measurement sheets), technical representatives, insurance policies. Note: README calls this app "Obsoleto" but it has been under active development in recent commits — treat that label with skepticism and check git history rather than assuming the app is dead.
- **secretariador**: per-diem/travel-allowance management (viáticos) — solicitudes de comisión de servicio, instrumentos legales (decretos/resoluciones), vehículos, generation of .docx resolutions.
- **personalizador**: HR (RRHH) — `CustomUser` (`AUTH_USER_MODEL`), `Agente`, org structure (Gerencia, Dirección, Departamento, Oficina, Categoria, etc.).
- **api**: a `django-ninja` API (mounted at `/v1/api/`) exposing selected data (mostly for select2 widgets and cross-app lookups) on top of the three apps above.

All source lives under `polizador/` (the repo root is one level above the Django project). The actual Django project package is `polizador/polizador/`.

## Common commands

Run everything from `polizador/` (where `manage.py` lives), with the virtualenv in `env/` activated:

```bash
cd polizador
source ../env/bin/activate   # or wherever the venv is activated from
python manage.py runserver
python manage.py migrate
python manage.py makemigrations <app>
```

Tests use Django's built-in test runner (`django.test.TestCase`); `pytest-django` is a listed dependency but there is no `pytest.ini`/`pyproject.toml` configuring it, so prefer:

```bash
python manage.py test                      # all apps
python manage.py test carga                # one app
python manage.py test api.tests.test_api   # one module
python manage.py test api.tests.test_api.AuthTest.test_users_requires_auth  # one test
```

There is no configured linter/formatter (no flake8/ruff/black config) — match the surrounding code style (this codebase mixes tabs and spaces per-file; follow whatever the file you're editing already uses).

Config comes from a `.env` file in `polizador/` (read via `django-environ`), not from environment variables set elsewhere. Required keys: `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DBHOST`, `DBUSER`, `DBNAME`, `DBPASSWORD`, `CACHE_URL`, `REDIS_URL`, `SENTRY_DSN`, `MAILGUN_API_KEY`, `MAILGUN_SENDER_DOMAIN`.

## Architecture notes

**Views/forms are split per-model, not per-app.** `carga` and `secretariador` don't use a single `views.py`/`forms.py`; each has a `views/` and `forms/` package with one module per model (e.g. `carga/views/obraviews.py`, `carga/forms/obraforms.py`). `carga/urls.py` does `from carga.views.<x>views import *` for each module. Note `secretariador/` has both a stale `views.py` (just leftover imports, dead) and the real `views/` package — the package wins on import; don't edit `views.py`.

**Standard CRUD view pattern** (see `carga/views/obraviews.py`): class-based views decorated with `@method_decorator(login_required, name="dispatch")`, mixed with `PermissionRequiredMixin` and an explicit `permission_required = "<app>.<action>_<model>"` string, using Django's generic `CreateView`/`UpdateView`/`DeleteView`/`DetailView`. Deletion views show related objects to be cascade-deleted via `carga/views/generics.py::get_deleted_objects`.

**List views use `django-ajax-datatable`.** Table listing pages subclass `AjaxDatatableView` (e.g. `ListaObrasView` in `obraviews.py`) rather than plain `ListView`.

**Autocomplete widgets use `django-select2`.** Widget classes subclass `s2forms.ModelSelect2Widget` (see `carga/views/ajaxviews.py`), are wrapped in `LoginRequiredMixin`, and results are cached via the dedicated `"select2"` cache backend (`SELECT2_CACHE_BACKEND`, backed by `REDIS_URL`). Some widgets are dependency-aware (`dependent_fields`) — they scope results based on a sibling form field's currently selected value (see `PlanDependentWidgetMixin`).

**The `api` app is django-ninja, not DRF.** Routes are registered by importing view modules for their side effects in `api/router.py` (`api/views/{carga,secretariador,personalizador,select2}_views.py`). Auth/permission checks are plain decorators in `api/permissions.py` (`require_auth`, `require_staff`, `get_optional_perms(*perms)`, `get_group_perms(*groups)`) raising `ninja.errors.AuthenticationError`/`AuthorizationError`, not DRF permission classes.

**Document generation** uses `docxtpl` (Jinja2-in-docx) against static templates in `secretariador/media/*.docx` (`solicitud_template.docx`, `solicitud_exterior.docx`, `solicitud_incorporacion.docx`) — see `secretariador/views/solicitudviews.py`, `solicitud_exteriorviews.py`, `incorporacionviews.py`.

**File storage is dual local+cloud.** `polizador/storages.py::GCloudAndLocalStorage` extends `django-storages`' `GoogleCloudStorage` to write every upload to both GCS (bucket `polizador-production-pdf`) and local `MEDIA_ROOT`. GCS credentials load from `polizador-production.json` in `BASE_DIR` if present; storage falls back gracefully (`GS_CREDENTIALS = None`) when that file is absent, e.g. locally.

**Auto-numbering via signals**, not model `save()` overrides, for sequential fields that must stay gapless across a chain of related records (e.g. `foja_numero` on `FojaDeMedicion`, etapa numbers on `PlanDeTrabajosEtapa`) — see `carga/signals.py`, wired up in `carga/apps.py`.

**`simple_history`** is installed and used for audit trails (`HistoryRequestMiddleware` is in `MIDDLEWARE`); check a model's `history` manager before adding a bespoke audit-log field.

**Custom validators** for domain rules live in `secretariador/functions.py` (`CuitValidator`, `FileValidator`) and are reused across forms.

**OCR/external integrations** are implemented as management commands, not request-time views: `secretariador/management/commands/OCR*.py` (Google Cloud Vision/Document AI OCR for instrumentos legales), `carga/management/commands/bcra_uvi.py` + `carga/bcra_api.py` (BCRA public API client for UVI values used in some monetary calculations).

**Context processors** (`polizador/context_processors.py`) inject `groups` (the current user's group names, for permission checks in templates) and a set of `*imglink` HTML snippets (icons for edit/delete/detail/pdf actions) into every template context — prefer these over hardcoding icon markup.

**Templates** are resolved from three `DIRS` (`templates/`, `carga/templates/`, `secretariador/templates/`) plus each app's own `APP_DIRS` templates; `personalizador` has no dedicated templates dir. Custom form-widget templates go in `templates/django/forms/widgets/`.

**Debug vs. production branches in `settings.py`** are significant: `DEBUG_TOOLBAR`, console email backend, and `sentry_sdk` init are all conditioned on `DEBUG`. Sentry is *not* initialized when `DEBUG=True`.
