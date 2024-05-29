// Usage:
//
// sumaColumnaPesos(tablename, column to sum, cellId to write the data)
// sumaColumnaUvi(tablename, column to sum, cellId to write the data)
function parseLocaleNumber(stringNumber, locale) {
  var thousandSeparator = Intl.NumberFormat(locale).format(11111).replace(/\p{Number}/gu, '');
  var decimalSeparator = Intl.NumberFormat(locale).format(1.1).replace(/\p{Number}/gu, '');

  return parseFloat(stringNumber
    .replace(new RegExp('\\' + thousandSeparator, 'g'), '')
    .replace(new RegExp('\\' + decimalSeparator), '.')
  );
};
function sumaColumnaPesos(tabla, columna, celdaId) {
  var table = document.getElementById(tabla),
    sumVal = 0;
  for (var i = 1; i < table.rows.length - 1; i++) {
    sumVal = sumVal + parseLocaleNumber(table.rows[i].cells[columna].innerHTML);
  };

  return document.getElementById(celdaId).innerHTML = "$" + sumVal.toLocaleString();
};
function sumaColumnaUvi(tabla, columna, celdaId) {
  var table = document.getElementById(tabla),
    sumVal = 0;
  for (var i = 1; i < table.rows.length - 1; i++) {
    sumVal = sumVal + parseLocaleNumber(table.rows[i].cells[columna].innerHTML);
  };

  return document.getElementById(celdaId).innerHTML = sumVal.toLocaleString();
};