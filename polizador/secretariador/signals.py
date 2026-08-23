from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.dispatch import receiver

from .models import ComisionadoSolicitud, Incorporacion, Solicitud

# Campos de Solicitud que alimentan `_calcular_texto_solicitud`/`_calcular_texto_exterior`.
# `solicitud_localidades` (m2m) y los agentes (ComisionadoSolicitud) se manejan aparte.
CAMPOS_TEXTO_SOLICITUD = [
	"solicitud_actuacion_jurisdiccion",
	"solicitud_actuacion_numero",
	"solicitud_actuacion_ano",
	"solicitud_provincia_id",
	"solicitud_ciudad",
	"solicitud_decreto_viaticos_id",
	"solicitud_fecha_desde",
	"solicitud_fecha_hasta",
	"solicitud_tareas",
	"solicitud_vehiculo_id",
	"solicitud_aereo",
	"solicitud_dia_inhabil",
]

# Campos de Solicitud que además alimentan `_calcular_texto_incorporacion` (vía
# `actuacion.incorporacion_solicitud.<campo>`) para la Incorporacion asociada,
# si existe. No coincide con CAMPOS_TEXTO_SOLICITUD: por ej. `solicitud_resolucion`
# no se usa en el texto de la propia Solicitud, pero sí en el de su Incorporacion.
CAMPOS_INCORPORACION_DESDE_SOLICITUD = [
	"solicitud_resolucion_id",
	"solicitud_decreto_viaticos_id",
	"solicitud_fecha_desde",
	"solicitud_fecha_hasta",
	"solicitud_tareas",
	"solicitud_dia_inhabil",
]

# Campos propios de Incorporacion que alimentan `_calcular_texto_incorporacion`
# (a través de `actuacion.incorporacion_actuacion`, el GeneratedField armado con estos tres).
CAMPOS_TEXTO_INCORPORACION = [
	"incorporacion_actuacion_jurisdiccion",
	"incorporacion_actuacion_numero",
	"incorporacion_actuacion_ano",
]


def _valor_comparable(instance, campo):
	"""Normaliza el valor en memoria de `campo` al tipo que devuelve la
	consulta a la base. Sin esto, comparar contra un valor recién asignado
	pero todavía no "pasado por" el campo (p. ej. una fecha asignada como
	string) contra el `date` que trae la fila existente dispararía una
	invalidación espuria."""
	valor = getattr(instance, campo)
	if campo.endswith("_id"):
		return valor
	return instance._meta.get_field(campo).to_python(valor)


def _invalidar_texto(model, pk, campo_texto):
	if not pk:
		return
	obj = model.objects.filter(pk=pk).exclude(**{campo_texto: None}).first()
	if obj:
		setattr(obj, campo_texto, None)
		obj.save(update_fields=[campo_texto])


def _invalidar_texto_solicitud(solicitud_id):
	_invalidar_texto(Solicitud, solicitud_id, "solicitud_texto_actuacion")


def _invalidar_texto_incorporacion(incorporacion_id):
	_invalidar_texto(Incorporacion, incorporacion_id, "incorporacion_texto_actuacion")


def _invalidar_incorporacion_de_solicitud(solicitud_id):
	"""Invalida el texto de la Incorporacion asociada a esta Solicitud, si existe
	(relación 1 a 1 en la práctica: `unique_incorporacion_1` sobre `incorporacion_solicitud`)."""
	if not solicitud_id:
		return
	incorporacion_id = Incorporacion.objects.filter(incorporacion_solicitud_id=solicitud_id).values_list("pk", flat=True).first()
	_invalidar_texto_incorporacion(incorporacion_id)


@receiver(pre_save, sender=Solicitud)
def invalidar_texto_actuacion_por_cambio_de_datos(sender, instance, **kwargs):
	"""`solicitud_texto_actuacion` (y, en cascada, `incorporacion_texto_actuacion`
	de la Incorporacion asociada) son snapshots editados a mano del texto de la
	resolución. Si después cambian los datos de la Solicitud que ese texto
	describe, el snapshot queda desactualizado y `editar_texto_solicitud`/
	`editar_texto_incorporacion` seguirían mostrándolo tal cual, sin reflejar
	el cambio (ver `revisar_texto_actuacion` en textoactuacionviews.py). Los
	invalidamos acá para forzar el recálculo la próxima vez que se abra el
	formulario de texto o se genere el .docx."""
	if not instance.pk:
		return
	campos = set(CAMPOS_TEXTO_SOLICITUD) | set(CAMPOS_INCORPORACION_DESDE_SOLICITUD)
	anterior = Solicitud.objects.filter(pk=instance.pk).values(*campos).first()
	if anterior is None:
		return

	def cambio(lista):
		return any(anterior[campo] != _valor_comparable(instance, campo) for campo in lista)

	if instance.solicitud_texto_actuacion and cambio(CAMPOS_TEXTO_SOLICITUD):
		instance.solicitud_texto_actuacion = None
	if cambio(CAMPOS_INCORPORACION_DESDE_SOLICITUD):
		_invalidar_incorporacion_de_solicitud(instance.pk)


@receiver(pre_save, sender=Incorporacion)
def invalidar_texto_incorporacion_por_cambio_de_datos(sender, instance, **kwargs):
	if not instance.pk or not instance.incorporacion_texto_actuacion:
		return
	anterior = Incorporacion.objects.filter(pk=instance.pk).values(*CAMPOS_TEXTO_INCORPORACION).first()
	if anterior is None:
		return
	if any(anterior[campo] != _valor_comparable(instance, campo) for campo in CAMPOS_TEXTO_INCORPORACION):
		instance.incorporacion_texto_actuacion = None


@receiver(m2m_changed, sender=Solicitud.solicitud_localidades.through)
def invalidar_texto_actuacion_por_localidades(sender, instance, action, **kwargs):
	if action in ("post_add", "post_remove", "post_clear"):
		_invalidar_texto_solicitud(instance.pk)
		_invalidar_incorporacion_de_solicitud(instance.pk)


@receiver(post_save, sender=ComisionadoSolicitud)
@receiver(post_delete, sender=ComisionadoSolicitud)
def invalidar_texto_actuacion_por_comisionados(sender, instance, **kwargs):
	# Agente de la Solicitud original (`agentes_solicitud`): afecta el texto de
	# la Solicitud y también el de su Incorporacion, si tiene una.
	_invalidar_texto_solicitud(instance.comisionadosolicitud_foreign_id)
	_invalidar_incorporacion_de_solicitud(instance.comisionadosolicitud_foreign_id)
	# Agente agregado directamente en la Incorporacion (`agentes_incorporacion`).
	_invalidar_texto_incorporacion(instance.comisionadosolicitud_incorporacion_foreign_id)
