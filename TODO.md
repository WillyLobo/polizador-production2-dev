[+] Agregar los campos nombre y apellido al formulario de registro de cuenta
[+] Eliminar easy Audit
[+] Crear script para recopilar datos del valor UVI con fuente del BCRA
[+] Revisar los campos de modelos que requieren operaciones aritmeticas y aplicar campos generados
    a nivel base de datos.
[?] Crear grupos de permisos para los usuarios:
    [+] Direccion General
    [+] Gerencia Operativa
    [+] Grupos para edición y grupos para vistas(tipo invitado solo para ver reportes)?
[+] Repasar los permisos en los Views
[+] Ordenar el cuadro busqueda de datatables
[?] Ajustar los templates de reportes de la app carga para ajustarse al resto del sitio
[?] Corregir los Select en las páginas de creación de reportes
[+] Redireccionar usuarios con permisos fuera de la vista sin permisos
[+] Modificar modelo Agente para vincularlo a los agentes de la app secretariador
[+] VerReporteCertificadoPorMes deberia dar opción de ver los certificados por fecha de carga o fecha de certificado
[+] Reparar los templates para ajustar viewport size
[+] Rehacer la integracion para contratos y resoluciones digitales de obras
[+] Crear API view que devuelva los meses/años disponibles en los certificados para su utilizacion en select2
[?] Hacer un favicon mas decente
[+] Añadir campo Representante Tecnico a las obras.
[ ] Implementar campo georeferencia(con PostGIS) para las obras.
[+] Actualizar a la ultima version de dataTables. 
    [+] Convertir "dom:" a "layout:".
    [+] Agregar boton para exportar a pdf/excel.
[ ] Eliminar codigo muerto JS.
[+] Corregir el filtrado previo de resoluciones, o agregar el filtro por tipo en datatable.
[ ] Normalizar los numeros de resoluciones para que usen el mismo separador("-").
[ ] Crear helper que convierta los numeros de resoluciones nuevos al formato de numero de resoluciones digitales(S.G.T.)
[+] Crear helper para agregar objetos FK directamente desde los formularios.
[+] Agregar opcion de remover firmas de gerente/representante tecnico en la foja de medicion.
[ ] Agregar helptext dinamico a los campos CUIL/CUIT de los formularios que sugieran el numero de CUIL/CUIT.

# Certificados
[+] Una foja deberia engendrar 1 certificado por cada financiamiento.
[+] El certificado solo deberia utilizar el plan de trabajos vigente.
[+] Se debe poder crear certificado de anticipo que no llevan foja y el valor se debe descontar proporcionalmente de los certificados posteriores hasta cumplir la totalidad del anticipo.
[+] Se deben poder crear certificados que se aprueban con resolucion o contrato pero que no llevan foja de medicion por ser hechos consumados.

# Fojas y Planes de Trabajo
[!] Agregar listado de fojas y planes de trabajo con DataTables
[?] Crear Home para la inspección donde muestren las obras que no han sido medidas aún
[+] Crear funciones que generen acumulado total en las fojas de medicion
[+] Crear vista que devuelva las obras donde el usuario es inspector
[+] Verificar que una obra pueda tener varios planes de trabajo... pero solo uno activo
[+] Imagenes multiples para fojas de medicion
[+] Campo archivo para planes de trabajo dititalizados

# Models
[+] Create model Incorporacion.

[+] Build create/update templates.

[+] Create concatenated fields for display.

[+] Comisionado Model:

[+] ComisionadoSolicitud Model:

[+] Build Create/Update/Delete/List views.

[+] Add navbar links.

[+] Create detail templates.
    [+] ListaIncorporacionesView
    [+] ListaComisionadosView
    [+] ListaVehiculosView

[+] Create report views.
    [+] Filter by agent.

[!] Add field localidad_distancia to Localidad model(carga app).
[!] Add route distance to Localidades(from Capital city, Resistencia).
[!] Add save method to set Comisionados into Solicitud database field.
[!] Add ajax to validate if instrumentolegalresoluciones is not duplicated before filling it in the form.
[!] Add field instrumentolegalresoluciones_actuacion to InstrumentosLegalesResoluciones model, generated from instrumentolegalresoluciones_descripcion split.

# Docx Templates
[ ] Add a way to update template.docx(ej: upload and overwrite the original file).

# Web Templates
[!] Add a right-side frame in form templates to provide help-text.

[+] Add more advanced logging capability.

# Experimental features to add/check:

# Fix Bugs:
[1] Add field incorporacion_solicitud_jurisdiccion that is currently hardcoded.
[1] Fix unique constraint in solicitud and solicitud incorporacion (it should check for actuacion_jurisdiccion, actuacion_numero, actuacion_ano in the constraint).

# DONE:
[+] FIXED: Model will allow to insert comisionados into a previously approved executive order.
[+] Fields: comisionado, actuacion_electronica, resolucion
[+] Split Solicitud.solicitud_actuacion into year and number fields.
[+] InstrumentosLegalesDecretos.
[+] InstrumentosLegalesResoluciones.
[+] Vehiculos
[+] Montos viaticos diarios.
[+] Incorporacion
[+] Vehículos= vehiculo_str(TextField)
[+] Comisionados= comisionado_nombreyapellido(TextField)
[!] Solicitud= get_comisionados(TextField)
[!] Move calculations for valor_viatico_dia from Comisionadosolicitud to Comisionado model.
[+] Moved comisionadosolicitud_viatico_diario to field via model save method.
[+] Moved comisionadosolicitud_viatico_computado to field via model save method.
[+] Moved comisionadosolicitud_viatico_total to field via model save method.
[+] Moved comisionadosolicitud_cantidad_de_dias to field via model save method.
[+] InstrumentosLegalesDecretos.
[+] InstrumentosLegalesResoluciones.
[+] Vehiculos
[+] Montos viaticos diarios.
[+] Incorporacion
[+] InstrumentosLegalesDecretos.
[+] InstrumentosLegalesResoluciones.
[+] Vehiculos
[+] Montos viaticos diarios
[+] Incorporacion
[+] ListaSolicitudesView
[+] ListaInstrumentosLegalesDecretosView
[+] ListaInstrumentosLegalesResolucionesView
[+] Report days that agentes are not present based on allowances days.
    [+] Report should have name, days absent, day that the report was made, executive order number that approved the allowance.
[?] Filter by solicitud.solicitud_solicitante.
[!] Create Views.
[!] Create Templates.
[+] Test form date validators.
[+] Create CuitValidator validator.
[+] Create FileValidator validator, to check for file types and size on upload.
[+] Add model constraints.
[+] Add default values in model.save method to avoid blank form fields in Solicitudes.
[+] solicitud.actuacion_electronica should be capitalized on model.clean method.
[+] Add field fecha de firma to instrumentoslegales models.
[+] Add functionality to deprecate Solicitudes.
[+] Add button option for Solicitud to be without allowances.
[+] Add constraint to solicitud so comisionados cannot be duplicated.
[+] Fix get_absolute_url() in reportesviews CrearReporteViaticosPorAgenteIndividual that is calling the wrong url.
[+] Add vehiculo_poliza & vehiculo_poliza_aseguradora fields to Vehiculo model.
[?] Review code to get comisionado_estrato(models.ComisionadoSolicitud.viaticos_computado), taking consideration that cabinet personel does not receive compensation.
[+] Fix form_invalid() in UpdateSolicitud view.
[+] Fix allowances for vocal in organigrama model.
[+] Fix form_invalid() in CrearSolitidud view.
[+] Check order of comisionados in template.docx.
[+] Add non working day check on Articulo 1º of solicitud_template.docx.
[+] Add solicitud_decreto_viaticos check on solicitud_template.docx
[+] Add reference to executive order 211/2020 for allowances outside of working days.
[+] Add logic to template.docx for allowance payments outside the province.
    [+] Created new template solicitud_exterior.docx
[+] Create docx template for Incorporados.
[!] Check comisionadosolicitud_chofer for values in registered drivers.
[+] Change Actuacion field to set number and year independently.
[+] Fix solicitud_cantidad_de_dias to integer(days).
[+] Remove solicitud.solicitud_viaticos_total.
[+] Fix "Combustible" in template.
[+] Add permission checks to the navbar.html menu.
[+] Remove scrollMonth & scrollInput from Datepicker.
[+] Add embedded pdf view to list detail templates.
[+] Add an intermediate page to redirect to solicitud or solicitud-exterior view.
[+] Add an intermediate page to redirect to intrumentolegaldecretos or montoviaticodiario view.
[+] Generate cron shell script to backup database.
[+] OCR for InstrumentosLegalesResoluciones.
[?] Use IA to summarize executive orders.
[+] Fix wrong parameter in nginx.conf regarding client_max_body_size.
[+] Fix plural omission in template_exterior: "quienes se trasladaran" should check if plural.
[+] Move Provincia model to carga_app.


# ------------------------------------------- #
#           Systemonchi APP                #
# ------------------------------------------- #

# Models:
[+] Create database models based on RRHH requests.

# ------------------------------------------- #
# Legend:                                     #
#     [ ] = Pending                           #
#     [+] = Completed                         #
#     [!] = Forcibly not needed/implemented.  #
#     [?] = Implementation needs review.      #
# ------------------------------------------- #
