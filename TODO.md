# Models
[+] Create model Incorporacion.
    - Model will allow to insert comisionados into a previously approved executive order.
    [+] Fields: comisionado, actuacion_electronica, resolucion
[+] Split Solicitud.solicitud_actuacion into year and number fields.

[+] Build create/update templates.
    [+] InstrumentosLegalesDecretos.
    [+] InstrumentosLegalesResoluciones.
    [+] Vehiculos
    [+] Montos viaticos diarios.
    [+] Incorporacion

[+] Create concatenated fields for display.
    [+] Vehículos= vehiculo_str(TextField)
    [+] Comisionados= comisionado_nombreyapellido(TextField)
    [!] Solicitud= get_comisionados(TextField)

[ ] Comisionado Model:
    [!] Move calculations for valor_viatico_dia from Comisionadosolicitud to Comisionado model.

[ ] ComisionadoSolicitud Model:
    [+] Moved comisionadosolicitud_viatico_diario to field via model save method.
    [+] Moved comisionadosolicitud_viatico_computado to field via model save method.
    [+] Moved comisionadosolicitud_viatico_total to field via model save method.
    [+] Moved comisionadosolicitud_cantidad_de_dias to field via model save method.

[+] Build Create/Update/Delete/List views.
    [+] InstrumentosLegalesDecretos.
    [+] InstrumentosLegalesResoluciones.
    [+] Vehiculos
    [+] Montos viaticos diarios.
    [+] Incorporacion

[+] Add navbar links.
    [+] InstrumentosLegalesDecretos.
    [+] InstrumentosLegalesResoluciones.
    [+] Vehiculos
    [+] Montos viaticos diarios
    [+] Incorporacion

[ ] Create detail templates.
    [+] ListaSolicitudesView
    [ ] ListaIncorporacionesView
    [ ] ListaComisionadosView
    [ ] ListaVehiculosView
    [+] ListaInstrumentosLegalesDecretosView
    [+] ListaInstrumentosLegalesResolucionesView

[ ] Create report views.
    [?] Filter by solicitud.solicitud_solicitante.
    [ ] Filter by agent.
    [+] Report days that agentes are not present based on allowances days.
        [+] Report should have name, days absent, day that the report was made, executive order number that approved the allowance.

[+] Move Provincia model to carga_app.
    # Number of provinces remain static, no need to implement.
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
[ ] Add field localidad_distancia to Localidad model(carga app).
[ ] Add route distance to Localidades(from Capital city, Resistencia).
[ ] Add save method to set Comisionados into Solicitud database field.
[ ] Add ajax to validate instrumentolegalresoluciones in forms.
[ ] Add button option for Solicitud to be withou allowances.

[+] Add vehiculo_poliza & vehiculo_poliza_aseguradora fields to Vehiculo model.
[ ] Add field instrumentolegalresoluciones_actuacion to InstrumentosLegalesResoluciones model, generated from instrumentolegalresoluciones_descripcion split.

[?] Review code to get comisionado_estrato(models.ComisionadoSolicitud.viaticos_computado), taking consideration that cabinet personel does not receive compensation.

[+] Fix form_invalid() in UpdateSolicitud view.
[+] Fix allowances for vocal in organigrama model.
[+] Fix form_invalid() in CrearSolitidud view.

# Docx Templates
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
[ ] Add a way to update template.docx(ej: upload and overwrite the original file).

# Web Templates
[+] Add permission checks to the navbar.html menu.
[+] Remove scrollMonth & scrollInput from Datepicker.
[ ] Add a right-side frame in form templates to provide help-text.
[+] Add embedded pdf view to list detail templates.
[+] Add an intermediate page to redirect to solicitud or solicitud-exterior view.
[+] Add an intermediate page to redirect to intrumentolegaldecretos or montoviaticodiario view.

[+] Generate cron shell script to backup database.
[ ] Add more advanced logging capability.

# Experimental features to add/check:
[ ] Use IA to summarize executive orders.

# Fix Bugs:
[+] Fix wrong parameter in nginx.conf regarding client_max_body_size.
[+] Fix plural omission in template_exterior: "quienes se trasladaran" should check if plural.


# ------------------------------------------- #
#           Systemonchi APP                #
# ------------------------------------------- #

# Models:
[ ] Create database models based on RRHH requests.

# ------------------------------------------- #
# Legend:                                     #
#     [ ] = Pending                           #
#     [+] = Completed                         #
#     [!] = Forcibly not needed/implemented.  #
#     [?] = Implementation needs review.      #
# ------------------------------------------- #
