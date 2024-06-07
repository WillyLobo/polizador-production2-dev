[+] Add permission checks to the navbar.html menu.

[ ] Create model Incorporacion.
    - Model will allow to insert comisionados into a previously approved executive order.
    [+] Fields: comisionado, actuacion_electronica, resolucion
    
[+] Build create/update templates.
    [+] InstrumentosLegalesDecretos.
    [+] InstrumentosLegalesResoluciones.
    [+] Vehiculos
    [+] Montos viaticos diarios.
    [+] Incorporacion

[+] Create concatenated fields for display.
    [+] Vehículos= vehiculo_str(TextField)
    [+] Comisionados= comisionado_nombreyapellido(TextField)
    [ ] Solicitud= get_comisionados(TextField)

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
    [ ] ListaInstrumentosLegalesDecretosView
    [ ] ListaInstrumentosLegalesResolucionesView

[ ] Create reportes views for solicitudes.
    [ ] Filter by solicitud.solicitud_solicitante.

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

[+] Agregar campos aseguradora y número de póliza al modelo Vehiculo.

[ ] Review code to get comisionado_estrato(models.ComisionadoSolicitud.viaticos_computado), taking consideration that cabinet personel does not receive compensation.

[+] Fix form_invalid() in UpdateSolicitud view.
[+] Fix allowances for vocal in organigrama model.
[+] Fix form_invalid() in CrearSolitidud view.

[+] Check order of comisionados in template.docx.
[+] Add non working day check on Articulo 1º of solicitud_template.docx.
[+] Add solicitud_decreto_viaticos check on solicitud_template.docx
[+] Add reference to executive order 211/2020 for allowances outside of working days.
[+] Remove scrollMonth & scrollInput from Datepicker.
[ ] Add a way to update template.docx(ej: upload and overwrite the original file).
[ ] Add logic to template.docx for allowance payments outside the province.
[ ] Create docx template for Incorporados.
[ ] Check comisionadosolicitud_chofer for values in registered drivers.

[ ] Add a right-side frame to form templates to provide help-text.
[ ] Add embedded pdf view to list detail templates.

[ ] Generate cron shell script to backup database.
[ ] Add a more advanced logging capability.


###############################################
# Legend:                                     #
#     [ ] = Pending                           #
#     [+] = Completed                         #
#     [!] = Forcibly not needed/implemented.  #
#---------------------------------------------#
