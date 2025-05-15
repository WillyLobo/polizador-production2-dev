.. :changelog:

History
=======
v0.1.3-7
------
* Added DecretoWidget for use in SolicitudForm and SolicitudExteriorForm.
* Updated MontoViaticoDiario model to include ordering options.
* Adjusted sum function in JavaScript to handle Spanish number formatting(attempt number 4 million to get it right).

v0.1.3-6
------
* Added method in InstrumentoLegalesDecretos and InstrumentoLegalesResoluciones to fill the instrument number to 5 digits.
* Fixed sumacolumna.js to use es-LA locale for parsing numbers.
* Added fields "comisionado_personal_transitorio" and "comisionado_personal_de_gabinete" in Comisionado model.
* Added required field styling to style.css.
* Refactored multiple forms in secretariador.app to use form mixins reducing code duplication.
* Finally fixed inline formsets in secretariador.app to work with select2 widgets.
* Changed default cache timeout for select2 to 1 day.

v0.1.3-5
------
* Added new template for creating and updating InstrumentosLegalesResoluciones.

v0.1.3-4
------
* Fixed error when creating a new Solicitud that pointed to the wrong MontoViaticoDiario instance.

v0.1.3-3
------
* Added initial value to solicitud_decreto_viaticos field in SolicitudForm and SolicitudExteriorForm.

v0.1.3-2
------
* Added configuratio for Sentry(https://sentry.io/) error tracking.

v0.1.3-1
------
* Added filter to instrumentoslegalesresoluciones OCR field in datatables.
* Fixed ComisionadoSolicitud cloned select2 widgets.
* Fixed reportesviews to include incorporaciones in the query.
* Fixed missing bootstrap5 theme in reportesviews.

v0.1.3
------
* Added annual calendar report by agent.

v0.1.2
* Fixed buttons in old templates.
* Changed render_row_details in ListaListaInstrumentosLegalesDecretosView and ListaListaInstrumentosLegalesResolucionesView to improve loading times.
* Changed style in navbar for ease of navigation.
* Added script to collect UVI values from BCRA api.

v0.1.1
------
* Fixed buttons that had wrong style in update-incorporacion.html.
* Added delete button so comisionados could be removed from form in update-incorporacion.html

v0.1.0
------
* First tracked changelog.