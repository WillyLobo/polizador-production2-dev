.. :changelog:

History
=======
v0.1.4
------
* Refactored forms, templates and views in Apps 'carga' and 'secretariador' for better organization and readability.

v0.1.3-15
Se eliminaron las aplicaciones 'widget_tweaks' y 'extra_views' de INSTALLED_APPS en settings.py. Se añadieron comentarios y un modelo en desarrollo 'Asuntos' en models.py, así como un nuevo método 'save' en el modelo 'Vehiculo' para limpiar espacios en el campo 'vehiculo_patente'. Se implementó una nueva clase 'DivErrorList' en el formulario 'ComisionadoSolicitudForm' para personalizar la visualización de errores. Se realizaron ajustes en las plantillas para mejorar la presentación de formularios y se actualizaron las vistas para manejar correctamente los errores de los formsets.
v0.1.3-14
------
* Removed widget_tweaks and extra_views from INSTALLED_APPS in settings.py.
* Added 'save' method in the 'Vehiculo' model to clean spaces in the 'vehiculo_patente' field.
* Added comments and a development model 'Asuntos' in models.py as well as fields in InstrumentosLegalesResoluciones model (WIP no db changes or migrations yet). 
* Implemented a new 'DivErrorList' class in the 'ComisionadoSolicitudForm' form to customize error display.
* Made adjustments to templates to improve form presentation and updated views to handle formset errors correctly.

v0.1.3-13
------
* Added administrative tools to navigate through the instrumentoslegalesresoluciones model.
* Added administrative tools to navigate through the instrumentoslegalesmemorandum model.
* Added administrative tools to navigate through the instrumentoslegalesdecretos model.

v0.1.3-12
------
* Added Calendario Semanal link to navbar.

v0.1.3-11
------
* Added ordering by name in Aseguradora and Empresa models.
* Created new widget for Aseguradora in ajaxviews.py.
* Added field "vehiculo_poliza_aseguradora" in Vehiculo model.
* Added field "vehiculo_titular_empresa" in Vehiculo model.
* Added field "vehiculo_titular_agente" in Vehiculo model.
* Added field "vehiculo_n_motor" in Vehiculo model.
* Added field "vehiculo_n_chasis" in Vehiculo model.
* Updated VehiculoForm and SolicitudForm to include new fields related to the vehicle.
* Generated migrations to reflect these changes in the database.

v0.1.3-10
------
* Added rowCallback event to Lista-solicitudes.html to highlight anulled rows.

v0.1.3-9
------
* Added field "comisionado_personal_transitorio" in Comisionado model.
* Added field "comisionado_personal_de_gabinete" in Comisionado model.
* Added tag to show "(C)" in __str__ method in Comisionado model.
* Modifified ordering in MontoViaticoDiario model.


v0.1.3-8
------
* Added ComisionadoWidget to IncorporacionForm.
* Added floating menu to solicitud, solicitudexterior, incorporacion, incorporacionexterior, incorporaciondecretoviaticos, incorporaciondecretoviaticosexterior templates.
* Adjusted scroll behavior in JavaScript.

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