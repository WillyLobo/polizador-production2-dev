[+] Add permission checks to the navbar.html menu.

[+] Build create/update templates.
    [+] InstrumentosLegalesDecretos.
    [+] InstrumentosLegalesResoluciones.
    [+] Vehiculos
    [+] Montos viaticos diarios.

[+] Create concatenated fields for display.
    [+] Vehículos= vehiculo_str(TextField)
    [+] Comisionados= comisionado_nombreyapellido(TextField)

[+] Build Create/Update/Delete/List views.
    [+] InstrumentosLegalesDecretos.
    [+] InstrumentosLegalesResoluciones.
    [+] Vehiculos
    [+] Montos viaticos diarios.

[+] Add navbar links.
    [+] InstrumentosLegalesDecretos.
    [+] InstrumentosLegalesResoluciones.
    [+] Vehiculos
    [+] Montos viaticos diarios

[ ] Create detail templates.
    [ ] ListaComisionadosView
    [+] ListaSolicitudesView
    [ ] ListaVehiculosView
    [ ] ListaInstrumentosLegalesDecretosView
    [ ] ListaInstrumentosLegalesResolucionesView

[+] Move Provincia model to carga_app.
    # Number of provinces remain static, no need to implement.
    [!] Create Views.
    [!] Create Templates.

[+] Test form date validators.
[+] Create CuitValidator validator.
[+] Create FileValidator validator, to check for file types and size on upload.

[+] Agregar campos aseguradora y número de póliza al modelo Vehiculo.

[ ] Review code to get comisionado_estrato(models.ComisionadoSolicitud.viaticos_computado), taking consideration that cabinet personel does not receive compensation.

[+] Fix form_invalid() in UpdateSolicitud view.
[ ] Fix form_invalid() in CrearSolitidud view.

[ ] Add a way to update template.docx(ej: upload and overwrite the original file).
[ ] Add logic to template.docx for allowance payments outside the province.

[ ] Generate cron shell script to backup database.


###############################################
# Legend:                                     #
#     [ ] = Pending                           #
#     [+] = Completed                         #
#     [!] = Forcibly not needed/implemented.  #
#---------------------------------------------#
