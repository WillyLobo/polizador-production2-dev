"""
Adaptador de allauth para polizador.

Cierra el alta de cuentas por la web. Polizador es una app interna del IPDUV:
las cuentas las crea un administrador desde el panel de Django
(/admin/personalizador/customuser/add/), que es el unico lugar donde ademas se
le asignan los grupos -- sin grupos una cuenta nueva no puede ver nada util, asi
que el alta self-service nunca completaba el trabajo por si sola.

Hasta ahora /accounts/signup/ estaba abierto con los valores por default de
allauth (cuenta ACTIVA, sin verificacion de mail), asi que cualquiera que
llegara al sitio podia crearse un usuario y pasar los login_required. Quedan
como evidencia dos cuentas cuyo username es una direccion personal de correo.

Cerrarlo NO toca a los usuarios existentes: siguen entrando con su usuario y
contrasena como siempre. Lo unico que deja de existir es el alta por la web.
"""
from allauth.account.adapter import DefaultAccountAdapter


class PolizadorAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False

    def send_password_reset_mail(self, user, email, context):
        """A quien ya entra solo por LDAP no se le manda un link para ponerse una
        contrasena local: se le explica que su contrasena es la de red.

        Sin esto, allauth le manda el link igual -- filter_users_by_email() no
        mira has_usable_password() -- y seguirlo le devuelve una contrasena local
        funcionando. Eso anula el sentido de habersela retirado: la idea es que
        desactivar a alguien en el AD le quite el acceso, y una contrasena local
        nueva sobrevive a esa baja.

        Se manda igual un correo (otro), para no cambiar lo que ve quien pide el
        reset: allauth responde siempre lo mismo pida lo que pida, justamente
        para no revelar que cuentas existen. Si acá no se mandara nada, quien
        tiene cuenta de red veria "te mandamos un mail" y no le llegaria nunca.

        El hook existe para esto; su propio docstring en allauth sugiere
        engancharse acá y mirar has_usable_password.
        """
        if getattr(user, "solo_ldap", False):
            return self.send_mail("account/email/password_reset_ldap", email, context)
        return super().send_password_reset_mail(user, email, context)
