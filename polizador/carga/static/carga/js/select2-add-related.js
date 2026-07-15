$(function () {
    var $modalEl = $("#addRelatedModal");
    var $modalBody = $modalEl.find(".modal-body");
    var modal = new bootstrap.Modal($modalEl.get(0));
    var currentCreateUrl = null;
    var currentSelectId = null;

    function bindFormAction() {
        $modalBody.find("#popupCreateForm").attr("action", currentCreateUrl);
    }

    $(document).on("click", ".select2-add-related", function () {
        currentSelectId = $(this).data("select-id");
        currentCreateUrl = $(this).data("create-url");
        var url = currentCreateUrl + (currentCreateUrl.indexOf("?") > -1 ? "&" : "?") + "_popup=1";

        $.get(url).done(function (html) {
            $modalBody.html(html);
            bindFormAction();
            modal.show();
        }).fail(function () {
            alert("No se pudo cargar el formulario.");
        });
    });

    $(document).on("submit", "#popupCreateForm", function (e) {
        e.preventDefault();
        var $form = $(this);

        $.ajax({
            url: currentCreateUrl,
            method: "POST",
            data: $form.serialize(),
            dataType: "json",
        }).done(function (data) {
            var $select = $("#" + currentSelectId);
            var option = new Option(data.text, data.id, true, true);
            $select.append(option).trigger("change");
            modal.hide();
        }).fail(function (xhr) {
            if (xhr.status === 400) {
                $modalBody.html(xhr.responseText);
                bindFormAction();
            } else {
                alert("No se pudo guardar.");
            }
        });
    });
});
