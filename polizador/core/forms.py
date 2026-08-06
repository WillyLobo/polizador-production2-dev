from django import forms


class BaseCommandRunForm(forms.Form):
    """Base para los forms declarados en core.management_commands_registry: valida los
    parámetros de un management command desde la web y los traduce al argv real que
    recibe el subprocess. Cada comando habilitado define su propia subclase — nada se
    arma dinámicamente a partir de argparse."""

    def to_argv(self):
        raise NotImplementedError


class CheckResolucionesForm(BaseCommandRunForm):
    """El comando `resolucion_audit` no toma argumentos."""

    def to_argv(self):
        return []


class BcraUviForm(BaseCommandRunForm):
    full_sync = forms.BooleanField(
        required=False,
        label="Sincronización completa",
        help_text=(
            "Descarga toda la serie histórica desde el primer valor informado por el BCRA, "
            "ignorando lo que ya hay en la base (los duplicados se omiten). Sin marcar, solo "
            "trae los valores nuevos desde el último registrado."
        ),
    )

    def to_argv(self):
        argv = []
        if self.cleaned_data["full_sync"]:
            argv.append("--full-sync")
        return argv


class DryRunCheckApplyForm(BaseCommandRunForm):
    """Base para comandos que ofrecen tres modos mutuamente excluyentes: chequeo rápido
    de solo lectura, simulación detallada sin guardar, o aplicar los cambios de verdad.
    El modo más seguro (chequeo) queda preseleccionado."""

    MODE_CHECK = "check"
    MODE_DRY_RUN = "dry_run"
    MODE_APPLY = "apply"
    MODE_CHOICES = [
        (MODE_CHECK, "Solo verificar (no modifica nada)"),
        (MODE_DRY_RUN, "Simular (muestra el detalle de los cambios, sin guardarlos)"),
        (MODE_APPLY, "Aplicar (guarda los cambios)"),
    ]

    mode = forms.ChoiceField(choices=MODE_CHOICES, initial=MODE_CHECK, widget=forms.RadioSelect)

    def to_argv(self):
        mode = self.cleaned_data["mode"]
        if mode == self.MODE_CHECK:
            return ["--check"]
        if mode == self.MODE_DRY_RUN:
            return ["--dry-run"]
        return []


class FixObraResolucionNumbersForm(DryRunCheckApplyForm):
    """No exponemos --output (ruta de archivo libre): se deja que el comando use su
    default (relativo al cwd del subprocess), para no aceptar una ruta arbitraria del
    lado del servidor."""


class NumerosCertificadosAuditForm(DryRunCheckApplyForm):
    pass


class CopiarBucketDevForm(BaseCommandRunForm):
    """No exponemos --source/--destination (nombres de bucket libres): el comando ya
    trae como default el único sentido autorizado, producción -> dev. Dejar que se
    tipeen nombres de bucket arbitrarios podría copiar o pisar datos en el bucket
    equivocado con credenciales que sí tienen permiso de escritura."""

    STORAGE_CLASS_CHOICES = [(c, c) for c in ("STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE")]

    dry_run = forms.BooleanField(
        required=False,
        initial=True,
        label="Simular (dry-run)",
        help_text="Tildado: no copia nada, solo informa cuántos objetos copiaría. Destildalo para copiar de verdad.",
    )
    overwrite = forms.BooleanField(
        required=False,
        label="Sobreescribir existentes",
        help_text="Vuelve a copiar objetos que ya están en destino con el mismo tamaño (por default se saltean).",
    )
    storage_class = forms.ChoiceField(
        choices=STORAGE_CLASS_CHOICES,
        initial="COLDLINE",
        label="Storage class en destino",
    )

    def to_argv(self):
        argv = []
        if self.cleaned_data["dry_run"]:
            argv.append("--dry-run")
        if self.cleaned_data["overwrite"]:
            argv.append("--overwrite")
        argv += ["--storage-class", self.cleaned_data["storage_class"]]
        return argv


class ResaveComisionadoForm(BaseCommandRunForm):
    """El comando `resave_comisionado` no toma argumentos."""

    def to_argv(self):
        return []


class EmpaquetarResolucionesMensualForm(BaseCommandRunForm):
    FORMATO_CHOICES = [
        ("ambos", "ZIP y PDF"),
        ("zip", "Solo ZIP"),
        ("pdf", "Solo PDF"),
    ]

    ano = forms.IntegerField(
        required=False, min_value=2000, max_value=2100, label="Año",
        help_text="Vacío junto con Mes: usa el mes anterior al actual.",
    )
    mes = forms.IntegerField(required=False, min_value=1, max_value=12, label="Mes (1-12)")
    tamano_maximo_mb = forms.IntegerField(
        required=False, min_value=1, initial=13, label="Tamaño máximo por parte (MB)"
    )
    formato = forms.ChoiceField(choices=FORMATO_CHOICES, initial="ambos", label="Formato a generar")

    def clean(self):
        cleaned_data = super().clean()
        ano = cleaned_data.get("ano")
        mes = cleaned_data.get("mes")
        if (ano is None) != (mes is None):
            raise forms.ValidationError("Año y Mes se completan juntos (o se dejan los dos vacíos).")
        return cleaned_data

    def to_argv(self):
        argv = []
        ano = self.cleaned_data.get("ano")
        mes = self.cleaned_data.get("mes")
        if ano is not None:
            argv += ["--ano", str(ano)]
        if mes is not None:
            argv += ["--mes", str(mes)]
        tamano_maximo_mb = self.cleaned_data.get("tamano_maximo_mb")
        if tamano_maximo_mb:
            argv += ["--tamano-maximo-mb", str(tamano_maximo_mb)]
        argv += ["--formato", self.cleaned_data["formato"]]
        return argv


class SyncResolucionesSgtForm(BaseCommandRunForm):
    """No exponemos --headed: abre una ventana de navegador visible para depurar
    selectores a mano, algo que no tiene sentido (ni funciona) corriendo como
    subprocess sin display en el servidor."""

    dry_run = forms.BooleanField(
        required=False,
        initial=True,
        label="Simular (dry-run)",
        help_text=(
            "Tildado: solo informa qué resoluciones faltan (consulta el SGT, no descarga "
            "ni guarda nada). Destildalo para importar de verdad."
        ),
    )
    limit = forms.IntegerField(
        required=False,
        min_value=1,
        label="Límite de resoluciones a descargar",
        help_text="Vacío: sin límite. Útil para probar con pocas antes de correr sin límite.",
    )

    def to_argv(self):
        argv = []
        if self.cleaned_data["dry_run"]:
            argv.append("--dry-run")
        limit = self.cleaned_data.get("limit")
        if limit:
            argv += ["--limit", str(limit)]
        return argv
