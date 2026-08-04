from django import forms


class BaseCommandRunForm(forms.Form):
    """Base para los forms declarados en core.management_commands_registry: valida los
    parámetros de un management command desde la web y los traduce al argv real que
    recibe el subprocess. Cada comando habilitado define su propia subclase — nada se
    arma dinámicamente a partir de argparse."""

    def to_argv(self):
        raise NotImplementedError


class CheckResolucionesForm(BaseCommandRunForm):
    """El comando `checks` no toma argumentos."""

    def to_argv(self):
        return []
