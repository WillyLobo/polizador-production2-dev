"""
Vinculacion de la cuenta de polizador con la cuenta de red (Active Directory).

El usuario entra como siempre (su usuario y contrasena de polizador) y despues
escribe sus credenciales de red. Si el bind contra el AD funciona, queda probado
que las dos identidades son de la misma persona: la sesion dice quien es en
polizador y el bind dice quien es en el AD. Se guarda el sAMAccountName que
devolvio el AD -- no lo que el usuario tipeo.

Por que este rodeo y no simplemente dejar que entren por LDAP: django-auth-ldap
autentica contra el AD y despues busca el CustomUser correspondiente; si no lo
encuentra, AUTH_LDAP_NO_NEW_USERS corta. El vinculo tiene que existir ANTES de
que el login por LDAP pueda funcionar, asi que no se puede descubrir a partir de
un login por LDAP. De ahi que la pregunta se haga dentro de una sesion ya
autenticada.

Nadie queda afuera: quien no tiene cuenta de red puede decirlo (ad_sin_cuenta_red)
y queda marcado para que lo revise un administrador, en vez de chocar con un muro
en cada login.
"""
import logging
import unicodedata

from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import FormView, TemplateView, View

from core import ldap_ad

logger = logging.getLogger(__name__)


def _normalizar(texto):
    descompuesto = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in descompuesto if not unicodedata.combining(c)).lower()


class VincularADForm(forms.Form):
    ad_username = forms.CharField(
        label="Usuario de red",
        max_length=150,
        help_text="El mismo con el que iniciás sesión en tu computadora del IPDUV.",
    )
    ad_password = forms.CharField(label="Contraseña de red", widget=forms.PasswordInput)

    def clean(self):
        datos = super().clean()
        usuario, clave = datos.get("ad_username"), datos.get("ad_password")
        if not usuario or not clave:
            return datos
        try:
            entrada = ldap_ad.verificar_credenciales(usuario, clave)
        except ldap_ad.ADNoConfigurado:
            raise forms.ValidationError(
                "La conexión con el directorio del IPDUV no está configurada. Avisá a sistemas."
            )
        except ldap_ad.ADNoDisponible:
            logger.exception("AD no disponible al vincular la cuenta de %s", usuario)
            raise forms.ValidationError(
                "No se pudo contactar al servidor del IPDUV. Probá de nuevo en unos minutos."
            )
        if entrada is None:
            # A proposito no se distingue "no existe" de "contrasena incorrecta".
            raise forms.ValidationError("Usuario o contraseña de red incorrectos.")
        datos["entrada_ad"] = entrada
        return datos


class VincularADView(LoginRequiredMixin, FormView):
    template_name = "vincular_ad/index.html"
    form_class = VincularADForm
    success_url = "/home/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.ad_username:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        # Para los ~16 usuarios cuyo username ya coincide con el de red, esto
        # deja el formulario a un solo campo.
        return {"ad_username": self.request.user.username}

    def form_valid(self, form):
        entrada = form.cleaned_data["entrada_ad"]
        sam = entrada["sAMAccountName"]
        User = get_user_model()

        ya_usado = User.objects.filter(ad_username=sam).exclude(pk=self.request.user.pk).first()
        if ya_usado:
            logger.warning(
                "Intento de vincular %s (AD) a %s, ya vinculada a %s",
                sam, self.request.user.username, ya_usado.username,
            )
            form.add_error(None, "Esa cuenta de red ya está vinculada a otro usuario. Avisá a sistemas.")
            return self.form_invalid(form)

        usuario = self.request.user
        usuario.ad_username = sam
        usuario.ad_vinculado_en = timezone.now()
        usuario.ad_sin_cuenta_red = False
        usuario.save(update_fields=["ad_username", "ad_vinculado_en", "ad_sin_cuenta_red"])

        # No bloquea: el nombre en polizador y el del AD casi nunca coinciden
        # palabra por palabra. Solo se deja registrado para que un administrador
        # pueda revisar los casos raros (una cuenta compartida, por ejemplo).
        nombre_django = _normalizar(f"{usuario.first_name} {usuario.last_name}")
        nombre_ad = _normalizar(entrada.get("displayName", ""))
        comparten = set(nombre_django.split()) & set(nombre_ad.split())
        logger.info(
            "Cuenta vinculada: polizador=%s -> AD=%s (%s)%s",
            usuario.username, sam, entrada.get("displayName", ""),
            "" if comparten else "  [OJO: los nombres no comparten ninguna palabra]",
        )

        messages.success(
            self.request,
            f"Listo. Tu cuenta quedó vinculada a «{sam}». "
            "A partir de ahora vas a poder entrar con tus credenciales del IPDUV.",
        )
        return super().form_valid(form)


class SinCuentaRedView(LoginRequiredMixin, View):
    """El usuario declara no tener cuenta de red. Queda marcado para revision."""

    def post(self, request, *args, **kwargs):
        request.user.ad_sin_cuenta_red = True
        request.user.save(update_fields=["ad_sin_cuenta_red"])
        logger.info("%s declara no tener cuenta de red", request.user.username)
        messages.info(
            request,
            "Anotado. Vas a seguir entrando con tu usuario y contraseña de polizador; "
            "sistemas va a revisar tu caso.",
        )
        return redirect("/home/")


class PasswordSetBloqueadoView(LoginRequiredMixin, TemplateView):
    """Reemplaza /accounts/password/set/ para quien ya entra solo por LDAP.

    allauth manda a esa pagina a cualquiera sin contrasena utilizable que abra
    "cambiar contraseña" (PasswordChangeView redirige a account_set_password), y
    ahi SetPasswordForm no pide la contrasena anterior -- con razon, porque la
    pensaron para cuentas de login social, que nunca tuvieron una. El efecto
    para nosotros es que un usuario al que se le retiro la contrasena local se
    pone otra en dos clics, y vuelve a existir una via de entrada que no pasa por
    el AD. Eso anula el sentido de haberla retirado: desactivar a alguien en el
    AD dejaria de quitarle el acceso.

    A quien todavia conserva contrasena local no se lo toca: la vista de allauth
    sigue atendiendolo igual que siempre.
    """

    template_name = "vincular_ad/password_ldap.html"

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.solo_ldap):
            from allauth.account.views import password_set

            return password_set(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Un POST a esta URL es alguien que mando el formulario de allauth (una
        # pestaña vieja, o el navegador reenviando). Se le muestra la misma
        # explicacion en vez del 405 que daria TemplateView por si solo.
        return self.get(request, *args, **kwargs)
