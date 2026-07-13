'use strict';

// Contraparte de ajax_datatable/js/utils.js para listados servidos por endpoints
// django-ninja (ver /v1/api/datatables/...). A diferencia de AjaxDatatableViewUtils,
// las columnas se definen de forma estática en cada template (no se piden al backend
// vía action=initialize) y el request/response usa un contrato simple por querystring
// en vez del formato con corchetes de DataTables.
window.NinjaDatatableUtils = (function() {

    function _load_row_details(rowData, detailUrl) {
        var div = $('<div/>').addClass('row-details-wrapper loading').text('Cargando...');
        var url = detailUrl.replace('{id}', encodeURIComponent(rowData.id));
        $.ajax({
            url: url,
            dataType: 'json',
            success: function(json) {
                div.html(json.html).removeClass('loading');
            }
        });
        return div;
    }

    // Click en cualquier celda de la fila expande/colapsa una fila hija con el detalle
    // (equivalente a "full_row_select" + _load_row_details() en ajax_datatable/js/utils.js).
    function _bind_row_expand(table, detailUrl) {
        table.on('click', 'td', function(event) {
            var tr = $(this).closest('tr');
            if (tr.hasClass('details') && !$(event.target).hasClass('btn-close')) {
                return;
            }
            var row = table.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
                return;
            }
            table.rows().every(function() { this.child.hide(); });
            table.$('tr').removeClass('shown');
            row.child(_load_row_details(row.data(), detailUrl), 'details').show();
            tr.addClass('shown');
        });
    }

    // Soporta orden multi-columna (shift+click en DataTables): cada entrada se
    // manda como "-clave" (desc) o "clave" (asc), separadas por coma.
    function _order_by_param(dtOrder, columns) {
        if (!dtOrder || !dtOrder.length) {
            return '';
        }
        return dtOrder.map(function(o) {
            var col = columns[o.column];
            var key = (col && (col.name || col.data)) || 'id';
            return (o.dir === 'desc' ? '-' : '') + key;
        }).join(',');
    }

    function _apply_filter_value(table, columnFilters, key, value) {
        if (value) {
            columnFilters[key] = value;
        } else {
            delete columnFilters[key];
        }
        table.draw();
    }

    // Select con opciones fijas (col.filterChoices: [[valor, etiqueta], ...]) o
    // cargadas una vez desde el backend (col.filterChoicesUrl: {choices: [...]}),
    // equivalente a "choices"/"autofilter" en ajax_datatable/js/utils.js.
    function _build_select_filter(table, columnFilters, key) {
        var select = $('<select class="form-select form-select-sm"><option value=""></option></select>');
        select.on('change', function() {
            _apply_filter_value(table, columnFilters, key, $(this).val());
        });
        return select;
    }

    function _fill_select_choices(select, choices) {
        choices.forEach(function(choice) {
            $('<option></option>').attr('value', choice[0]).text(choice[1]).appendTo(select);
        });
    }

    // Input nativo type="date" (mismo criterio que DateHTMLWidget en custom_forms.py:
    // sin librerías de terceros, el picker lo pone el navegador). El valor llega al
    // backend ya en formato ISO yyyy-mm-dd, listo para comparar contra un DateField.
    function _build_date_filter(table, columnFilters, key) {
        var input = $('<input type="date" class="form-control form-control-sm">');
        input.on('change', function() {
            _apply_filter_value(table, columnFilters, key, $(this).val());
        });
        return input;
    }

    // Agrega una fila de filtros por columna debajo del encabezado (texto libre,
    // <select> para filterType:'select', input de fecha para filterType:'date') y
    // redibuja la tabla al cambiar un valor, equivalente a "show_column_filters" en
    // ajax_datatable/js/utils.js pero con columnas estáticas.
    function _bind_column_filters(table, element, columns, columnFilters) {
        var filterRow = $('<tr class="ninja-datatable-filter-row"></tr>');

        columns.forEach(function(col) {
            var cell = $('<th></th>');
            if (col.filterable !== false && col.searchable !== false && col.data) {
                var key = col.name || col.data;
                var field;
                if (col.filterType === 'select') {
                    field = _build_select_filter(table, columnFilters, key);
                    if (col.filterChoices) {
                        _fill_select_choices(field, col.filterChoices);
                    } else if (col.filterChoicesUrl) {
                        $.getJSON(col.filterChoicesUrl, function(data) {
                            _fill_select_choices(field, data.choices || []);
                        });
                    }
                } else if (col.filterType === 'date') {
                    field = _build_date_filter(table, columnFilters, key);
                } else {
                    field = $('<input type="text" class="form-control form-control-sm" placeholder="...">');
                    field.on('keyup change', function() {
                        _apply_filter_value(table, columnFilters, key, $(this).val());
                    });
                }
                cell.append(field);
            }
            filterRow.append(cell);
        });

        element.find('thead').append(filterRow);
    }

    function initialize_table(element, url, columns, options) {
        options = options || {};
        var columnFilters = {};

        var dtOptions = $.extend({
            processing: true,
            serverSide: true,
            autoWidth: false,
            language: window.DATATABLES_ES,
            layout: {
                topStart: 'search',
                topEnd: 'pageLength',
                bottomStart: 'info',
                bottomEnd: 'paging'
            },
            columns: columns,
            order: options.order || [[0, 'desc']],
            lengthMenu: options.lengthMenu || [[10, 25, 50, 100], [10, 25, 50, 100]],
            ajax: {
                url: url,
                type: 'GET',
                data: function(d) {
                    var extra = options.extraData ? options.extraData() : {};
                    return $.extend({
                        draw: d.draw,
                        start: d.start,
                        length: d.length,
                        search: d.search.value,
                        order_by: _order_by_param(d.order, columns),
                        filters: JSON.stringify(columnFilters)
                    }, extra);
                }
            }
        }, options.dataTableOptions || {});

        var table = element.DataTable(dtOptions);

        if (options.columnFilters !== false) {
            _bind_column_filters(table, element, columns, columnFilters);
        }

        if (options.detailUrl) {
            _bind_row_expand(table, options.detailUrl);
        }

        return table;
    }

    return {
        initialize_table: initialize_table
    };

})();
