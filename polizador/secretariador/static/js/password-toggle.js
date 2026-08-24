document.addEventListener("click", function (event) {
    var button = event.target.closest(".password-toggle");
    if (!button) {
        return;
    }

    var input = document.getElementById(button.dataset.target);
    var icon = button.querySelector("i");
    if (!input || !icon) {
        return;
    }

    var showing = input.type === "text";
    input.type = showing ? "password" : "text";
    icon.classList.toggle("bi-eye", showing);
    icon.classList.toggle("bi-eye-slash", !showing);
    button.setAttribute("aria-label", showing ? "Mostrar contraseña" : "Ocultar contraseña");
});
