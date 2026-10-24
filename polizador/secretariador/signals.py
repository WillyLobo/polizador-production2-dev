from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.db.models import Q
from django.dispatch import receiver

from .models import ComisionadoSolicitud, Incorporacion, Solicitud, sincronizar_comisionados

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

# Campos de Solicitud de los que dependen los campos derivados de sus
# ComisionadoSolicitud (y de los de su Incorporacion): las fechas, los días; la
# provincia y el decreto, la tarifa diaria. Ver sincronizar_comisionados().
CAMPOS_DIAS_SOLICITUD = [
	"solicitud_fecha_desde",
	"solicitud_fecha_hasta",
]
CAMPOS_TARIFA_SOLICITUD = [
	"solicitud_provincia_id",
	"solicitud_decreto_viaticos_id",
]

MOTIVO_SINCRONIZAR_SOLICITUD = "Solicitud editada: recálculo de días/viáticos"
MOTIVO_SINCRONIZAR_INCORPORACION = "Incorporación asociada a otra Solicitud: recálculo de días/viáticos"


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


def _campos_que_se_guardan(model, campos, update_fields):
	"""Con save(update_fields=...), un campo distinto en memoria pero fuera de
	update_fields no llega a la base: no cuenta como cambio."""
	if update_fields is None:
		return campos
	return [campo for campo in campos if model._meta.get_field(campo).name in update_fields]


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


@receiver(pre_save, sender=Solicitud)
def detectar_cambios_para_comisionados(sender, instance, update_fields=None, **kwargs):
	"""Los días y viáticos de un ComisionadoSolicitud son copias calculadas a partir
	de su Solicitud, y los formsets de edición solo guardan las filas que el usuario
	tocó: corregir solo las fechas de la Solicitud dejaba a sus comisionados con los
	días viejos. Acá se anota qué cambió, para que `sincronizar_comisionados_de_solicitud`
	los recalcule una vez guardada la Solicitud (y su GeneratedField de días)."""
	instance._sincronizar_comisionados = None
	if not instance.pk:
		return
	campos_dias = _campos_que_se_guardan(Solicitud, CAMPOS_DIAS_SOLICITUD, update_fields)
	campos_tarifa = _campos_que_se_guardan(Solicitud, CAMPOS_TARIFA_SOLICITUD, update_fields)
	if not campos_dias and not campos_tarifa:
		return
	anterior = Solicitud.objects.filter(pk=instance.pk).values(*campos_dias, *campos_tarifa).first()
	if anterior is None:
		return

	def cambio(lista):
		return any(anterior[campo] != _valor_comparable(instance, campo) for campo in lista)

	if cambio(campos_tarifa):
		instance._sincronizar_comisionados = {"recalcular_diario": True}
	elif cambio(campos_dias):
		instance._sincronizar_comisionados = {"recalcular_diario": False}


@receiver(post_save, sender=Solicitud)
def sincronizar_comisionados_de_solicitud(sender, instance, created, **kwargs):
	"""Recalcula los comisionados de la Solicitud y los agregados por una
	Incorporacion a ella. El viático diario solo se recalcula si cambió la
	provincia o el decreto; si solo cambiaron las fechas queda congelado
	(ver ComisionadoSolicitud.recalcular_campos_derivados)."""
	pendiente = getattr(instance, "_sincronizar_comisionados", None)
	instance._sincronizar_comisionados = None
	if created or pendiente is None:
		return
	comisionados = ComisionadoSolicitud.objects.filter(
		Q(comisionadosolicitud_foreign=instance)
		| Q(comisionadosolicitud_incorporacion_foreign__incorporacion_solicitud=instance)
	)
	sincronizar_comisionados(comisionados, pendiente["recalcular_diario"], MOTIVO_SINCRONIZAR_SOLICITUD)


@receiver(pre_save, sender=Incorporacion)
def detectar_cambio_de_solicitud_de_incorporacion(sender, instance, update_fields=None, **kwargs):
	"""Si la Incorporacion pasa a apuntar a otra Solicitud, sus comisionados
	cambian de viaje (fechas, provincia, decreto): se recalculan del todo."""
	instance._sincronizar_comisionados = False
	if not instance.pk or not _campos_que_se_guardan(Incorporacion, ["incorporacion_solicitud_id"], update_fields):
		return
	anterior = Incorporacion.objects.filter(pk=instance.pk).values_list("incorporacion_solicitud_id", flat=True).first()
	instance._sincronizar_comisionados = anterior is not None and anterior != instance.incorporacion_solicitud_id


@receiver(post_save, sender=Incorporacion)
def sincronizar_comisionados_de_incorporacion(sender, instance, created, **kwargs):
	pendiente = getattr(instance, "_sincronizar_comisionados", False)
	instance._sincronizar_comisionados = False
	if created or not pendiente:
		return
	comisionados = ComisionadoSolicitud.objects.filter(comisionadosolicitud_incorporacion_foreign=instance)
	sincronizar_comisionados(comisionados, True, MOTIVO_SINCRONIZAR_INCORPORACION)
