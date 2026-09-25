$(function () {
    var $contrato = $("#id_poliza_contrato");
    var $financiamiento = $("#id_poliza_financiamiento");
    var $concepto = $("#id_poliza_concepto");
    var $anticipoPct = $("#id_poliza_anticipo_pct");
    var $anticipoWrap = $("#poliza-anticipo-pct-wrap");
    var $texto = $("#garantia-sugerida-texto");

    function toggleAnticipo() {
        $anticipoWrap.toggle($concepto.val() === "A");
    }

    function actualizar() {
        var contratoId = $contrato.val();
        var financiamiento = $financiamiento.val();
        var concepto = $concepto.val();
        if (!contratoId || !financiamiento || !concepto) {
            $texto.text("Complete Obra, Contrato, Financiamiento y Concepto.");
            return;
        }
        var params = {financiamiento: financiamiento, concepto: concepto};
        if (concepto === "A") {
            params.anticipo_pct = $anticipoPct.val() || "0";
        }
        $.get("/v1/api/contrato/" + contratoId + "/monto-garantia/", params)
            .done(function (data) {
                if (Number(data.monto_contrato_pesos) === 0 && Number(data.monto_contrato_uvi) === 0) {
                    $texto.text("El Contrato no tiene montos cargados para ese Financiamiento.");
                    return;
                }
                $texto.html(
                    "Monto de Contrato: $" + data.monto_contrato_pesos + " / " + data.monto_contrato_uvi + " UVI" +
                    "<br>Monto sugerido a cubrir: $" + data.monto_a_cubrir_pesos + " / " + data.monto_a_cubrir_uvi + " UVI"
                );
            })
            .fail(function () {
                $texto.text("No se pudo calcular el monto sugerido.");
            });
    }

    $(document).on("change", "#id_poliza_contrato, #id_poliza_financiamiento, #id_poliza_concepto, #id_poliza_anticipo_pct", function () {
        toggleAnticipo();
        actualizar();
    });

    $(document).on("change", "#id_poliza_obra", function () {
        $texto.text("Complete Obra, Contrato, Financiamiento y Concepto.");
    });

    toggleAnticipo();
    if ($contrato.val()) {
        actualizar();
    }
});
