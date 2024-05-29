// Usage:
//
// sumaColumnaPesos(tablename, column to sum, cellId to write the data)
// sumaColumnaUvi(tablename, column to sum, cellId to write the data)
function parseLocaleNumber(stringNumber, locale) {
  stringNumber = stringNumber.replace(/\&nbsp;/g, '');
  var thousandSeparator = Intl.NumberFormat(locale).format(11111).replace(/\p{Number}/gu, '');
  var decimalSeparator = Intl.NumberFormat(locale).format(1.1).replace(/\p{Number}/gu, '');

  return parseFloat(stringNumber
    .replace(new RegExp('\\' + thousandSeparator, 'g'), '')
    .replace(new RegExp('\\' + decimalSeparator), '.')
  );
};
function sumaColumna(tabla, columna, celdaId) {
  var table = document.getElementById(tabla),
    sumVal = 0;
  for (var i = 1; i < table.rows.length - 1; i++) {
    if (isNaN(parseLocaleNumber(table.rows[i].cells[columna].innerHTML))) {
    }
    else {
      sumVal = sumVal + parseLocaleNumber(table.rows[i].cells[columna].innerHTML);
    }
  };

  return document.getElementById(celdaId).innerHTML = sumVal.toLocaleString();
};

function sumaColumnaPesos(tabla, columna, celdaId) {
  var table = document.getElementById(tabla),
    sumVal = 0;
  for (var i = 1; i < table.rows.length - 1; i++) {
    if (isNaN(parseLocaleNumber(table.rows[i].cells[columna].innerHTML))) {
    }
    else {
      sumVal = sumVal + parseLocaleNumber(table.rows[i].cells[columna].innerHTML);
    }
  };

  return document.getElementById(celdaId).innerHTML = "$" + sumVal.toLocaleString();
};

function sumaColumnaUvi(tabla, columna, celdaId) {
  var table = document.getElementById(tabla),
    sumVal = 0;
  for (var i = 1; i < table.rows.length - 1; i++) {
    if (isNaN(parseLocaleNumber(table.rows[i].cells[columna].innerHTML))) {
    }
    else {
      sumVal = sumVal + parseLocaleNumber(table.rows[i].cells[columna].innerHTML);
    }
  };

  return document.getElementById(celdaId).innerHTML = sumVal.toLocaleString();
};

function cloneMore(selector, type) {
  var newElement = $(selector).clone(true);
  var total = $('#id_' + type + '-TOTAL_FORMS').val();
  var csrf = $(selector).find("[name='csrfmiddlewaretoken']").val();

  newElement.find(':input').each(function () {
    var name = $(this).attr('name').replace('-' + (total - 1) + '-', '-' + total + '-');
    var id = 'id_' + name;
    var elementValue = $(this).attr('value')
    $(this).attr({ 'name': name, 'id': id }).val(elementValue).removeAttr('checked');
  });

  newElement.find('label').each(function () {
    var newFor = $(this).attr('for').replace('-' + (total - 1) + '-', '-' + total + '-');
    $(this).attr('for', newFor);
  });
  newElement.find("[name='csrfmiddlewaretoken']").each(function () {
    $(this).attr('value', csrf)
  });
  total++;
  $('#id_' + type + '-TOTAL_FORMS').val(total);
  $(selector).after(newElement);
}

// Crappy Graph Function.
// Uso:
// makeGraph(table, rubro, financiamiento, fecha, pesos, acumulado)
// table: id del canvas donde se dibuja el grafico.
// rubro: rubro de la obra a ejecutar, ej. "Vivienda".
// financiamiento: origen del financiamiento, ej "Nación".
// fecha: array con los meses de la ordenada.
// pesos: array con los montos en pesos.
// acumulado: array con los porcentajes acumulados.
function makeGraph(table, rubro, financiamiento, fecha, pesos, acumulado) {
  new Chart(table, {
    type: 'line',
    data: {
      labels: fecha,
      datasets: [{
        label: 'Monto Mensual en Pesos',
        yAxisID: 'A',
        data: pesos,
        fill: true,
        borderColor: "#0066ff",
        tension: 0.4
      }, {
        label: 'Avance Porcentual Acumulado',
        yAxisID: 'B',
        data: acumulado,
        fill: true,
        borderColor: "#00cc66",
        tension: 0.4
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Certificados: " + rubro + " | Financiamiento: " + financiamiento
        }
      },
      scales: {
        A: {
          type: 'linear',
          position: 'left',
        },
        B: {
          type: 'linear',
          position: 'right',
          ticks: {
            max: 100,
            min: 0
          }
        }
      }
    }
  });
}