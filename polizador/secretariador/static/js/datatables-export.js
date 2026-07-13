'use strict';

// Botones de exportación (Excel/PDF) para las tablas de reportes client-side
// (paging:false, todos los datos ya están en el DOM). Uso:
//
//   new DataTable('#tablaReporte', {
//       layout: { topStart: 'buttons' },
//       buttons: DatatablesExportButtons.build('Reporte de Certificados por Mes'),
//       ...
//   });
//
// Excluye del export las columnas marcadas con d-print-none (acciones/links),
// igual que ya se ocultan al imprimir.
window.DatatablesExportButtons = (function() {

    function build(title, options) {
        options = options || {};
        var exportOptions = $.extend({ columns: ':not(.d-print-none)' }, options.exportOptions || {});

        return [
            {
                extend: 'excelHtml5',
                text: '<i class="bi bi-file-earmark-excel"></i> Excel',
                className: 'btn-outline-success btn-sm',
                title: title,
                exportOptions: exportOptions
            },
            {
                extend: 'pdfHtml5',
                text: '<i class="bi bi-file-earmark-pdf"></i> PDF',
                className: 'btn-outline-danger btn-sm',
                title: title,
                orientation: 'landscape',
                pageSize: 'A4',
                exportOptions: exportOptions,
                // pdfMake dimensiona las columnas según su contenido y no respeta
                // el ancho de la hoja: se fuerza a que se repartan el ancho
                // disponible en partes iguales y se ajusta la letra para que
                // entren sin desbordar.
                customize: function(doc) {
                    doc.defaultStyle.fontSize = 7;
                    doc.styles.tableHeader.fontSize = 8;
                    doc.pageMargins = [20, 30, 20, 30];
                    var el = doc.content[1];
                    var numCols = el.table.body[0].length;
                    // pdfmake suma el padding horizontal (4pt por lado por default)
                    // POR FUERA del ancho declarado de cada columna, así que si no se
                    // descuenta la tabla termina siendo más ancha que la hoja y las
                    // últimas columnas quedan recortadas. Se reduce el padding y se
                    // descuenta ese overhead del ancho disponible.
                    var cellPadding = 2;
                    el.layout = {
                        paddingLeft: function() { return cellPadding; },
                        paddingRight: function() { return cellPadding; },
                        paddingTop: function() { return 2; },
                        paddingBottom: function() { return 2; }
                    };
                    var pageWidthPt = 841.89; // A4 landscape
                    var availableWidth = pageWidthPt - doc.pageMargins[0] - doc.pageMargins[2] - numCols * cellPadding * 2;
                    el.table.widths = Array(numCols).fill(availableWidth / numCols);
                }
            }
        ];
    }

    return { build: build };

})();
