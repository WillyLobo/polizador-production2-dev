"""
Armado del texto (VISTO/CONSIDERANDO/Artículos) de las resoluciones de
viáticos: solicitud (Chaco), solicitud exterior e incorporación.

Estas funciones no generan .docx ni conocen nada de OOXML/python-docx —
solo devuelven strings y listas. La construcción del documento en sí vive
en `docx_builder.py`. Se centralizan acá porque hasta ahora estaban
duplicadas casi literalmente en cada una de las tres vistas `*_docx`.
"""


def separate_items(items):
	concatenated_items = ", ".join(items)
	last_comma_index = concatenated_items.rfind(",")
	if last_comma_index != -1:
		concatenated_items = concatenated_items[:last_comma_index] + " y" + concatenated_items[last_comma_index + 1:]
	return concatenated_items


def generate_localidad_list(localidades):
	if len(localidades) > 1:
		text_localidad = "las localidades de"
	else:
		text_localidad = "la localidad de"
	lista_localidades = separate_items([str(localidad.localidad_nombre) for localidad in localidades])
	return f"{text_localidad} {lista_localidades}"


def generate_fechas_list(fechas):
	if len(fechas) > 1:
		text_fechas = "los días"
	else:
		text_fechas = "el día"
	lista_fechas = separate_items([str(fecha) for fecha in fechas])
	return f"{text_fechas} {lista_fechas}"


def generate_agente_list_articulo(agentes, cantidad_de_dias):
	"""
	Devuelve, por cada agente comisionado, la fila que se vuelca en el
	Artículo 2°: [comisionado_id, nombre_cuil, monto, subparrafo].

	`cantidad_de_dias` es un int (días de la comisión), tomado por el
	llamador de `actuacion.solicitud_cantidad_de_dias.days` (Solicitud) o
	`incorporacion_solicitud.solicitud_cantidad_de_dias.days` (Incorporacion).
	"""
	dias_texto = f"{cantidad_de_dias} {'dias' if cantidad_de_dias > 1 else 'dia'}"

	filas = []
	for agente in agentes:
		nombre_cuil = f"{agente.persona.abreviatura} {agente.persona.agente_nombreyapellido} – CUIL Nº{agente.persona.cuil}"
		combustible = "{:,.2f}".format(agente.comisionadosolicitud_combustible).replace(",", "@").replace(".", ",").replace("@", ".")
		pasaje = "{:,.2f}".format(agente.comisionadosolicitud_pasaje).replace(",", "@").replace(".", ",").replace("@", ".")
		gastos = "{:,.2f}".format(agente.comisionadosolicitud_gastos).replace(",", "@").replace(".", ",").replace("@", ".")
		valor_viatico_dia = "{:,.2f}".format(agente.valor_viatico_dia()).replace(",", "@").replace(".", ",").replace("@", ".")
		valor_viatico_total = "{:,.2f}".format(agente.viaticos_total()).replace(",", "@").replace(".", ",").replace("@", ".")

		subparrafo = f"(Viáticos: {dias_texto} a razón de ${valor_viatico_dia} diarios"
		if pasaje != "0,00":
			subparrafo += f" + Pasaje: ${pasaje}"
		if gastos != "0,00":
			subparrafo += f" + Gastos: ${gastos}"
		if combustible != "0,00":
			subparrafo += f" + Combustible: ${combustible}"
		subparrafo += ")."

		filas.append({
			"comisionado_id": agente.pk,
			"nombre_cuil": nombre_cuil,
			"monto": valor_viatico_total,
			"subparrafo": subparrafo,
		})
	return filas


# Bloques fijos que se repiten sin cambios en las tres resoluciones (no
# editables desde la web: son boilerplate legal, no texto que dependa de
# los datos de cada actuación).
CONSIDERANDOS_FIJOS_FINALES = [
	"Que conforme a lo establecido en Memorándum Nº050/2014 de la Contaduría General de la Provincia, “si los agentes no efectuasen la rendición y/o reintegro del excedente del presente anticipo dentro del plazo reglamentario, autorizan expresamente a retener de sus haberes los importes recibidos y/o reintegrados”;",
	"Que el suscripto está facultado a autorizar comisiones y viáticos;",
	"Por ello;",
]

ARTICULO_TRES = "El gasto emergente de lo dispuesto en la presente Resolución, deberá imputarse a la partida específica del Instituto, según la naturaleza de este."
ARTICULO_CUATRO = "Si el subresponsable no efectuare las rendiciones y/o reintegro del excedente del presente anticipo dentro del plazo reglamentario, autoriza expresamente a retener de sus haberes los importes recibidos y/o reintegrados”. Según Memorándum Nº050/2014 de Contaduría General."
ARTICULO_CINCO = "Regístrese, comuníquese y archívese."
