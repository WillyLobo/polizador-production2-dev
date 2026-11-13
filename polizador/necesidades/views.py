from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.db.models import Case, Count, Exists, IntegerField, OuterRef, Q, Value, When
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from necesidades.forms import GestionForm, NecesidadForm
from necesidades.models import Apoyo, Necesidad

PERM_GESTIONAR = "necesidades.gestionar_necesidad"
ORDENES = {
    "urgencia": ["cerrada", "urgencia", "-n_apoyos", "-creado"],
    "apoyos": ["cerrada", "-n_apoyos", "urgencia", "-creado"],
    "recientes": ["cerrada", "-creado"],
}


def _puede_editar(user, necesidad):
    return necesidad.autor_username == user.get_username() or user.has_perm(PERM_GESTIONAR)


def _volver(request, pk=None):
    """Vuelve a la lista conservando los filtros que tenía el usuario."""
    filtros = QueryDict(request.POST.get("filtros", ""))
    limpios = QueryDict(mutable=True)
    for clave in ("modulo", "estado", "orden"):
        if filtros.get(clave):
            limpios[clave] = filtros[clave]
    url = reverse("necesidades:lista")
    if limpios:
        url += "?" + limpios.urlencode()
    if pk:
        url += f"#n{pk}"
    return redirect(url)


def _render_lista(request, form, editando=None):
    user = request.user
    username = user.get_username()
    gestor = user.has_perm(PERM_GESTIONAR)

    todas = Necesidad.objects.annotate(
        n_apoyos=Count("apoyos"),
        yo_apoyo=Exists(Apoyo.objects.filter(necesidad=OuterRef("pk"), username=username)),
        cerrada=Case(When(estado__in=Necesidad.ESTADOS_CERRADOS, then=Value(1)),
                     default=Value(0), output_field=IntegerField()),
    )
    totales = Necesidad.objects.aggregate(
        total=Count("pk"),
        bloquean=Count("pk", filter=Q(urgencia=Necesidad.Urgencia.BLOQUEA)
                       & ~Q(estado__in=Necesidad.ESTADOS_CERRADOS)),
        hablar=Count("pk", filter=Q(estado=Necesidad.Estado.HABLAR)),
        resueltas=Count("pk", filter=Q(estado=Necesidad.Estado.RESUELTA)),
    )

    modulo = request.GET.get("modulo", "")
    estado = request.GET.get("estado", "")
    orden = request.GET.get("orden", "urgencia")
    if orden not in ORDENES:
        orden = "urgencia"
    lista = todas
    if modulo in Necesidad.Modulo.values:
        lista = lista.filter(modulo=modulo)
    if estado in Necesidad.Estado.values:
        lista = lista.filter(estado=estado)
    lista = list(lista.order_by(*ORDENES[orden]))
    for n in lista:
        n.es_mia = n.autor_username == username
        n.puede_editar = n.es_mia or gestor
        if gestor:
            n.gestion_form = GestionForm(instance=n, prefix=f"g{n.pk}")

    return render(request, "necesidades/lista.html", {
        "form": form,
        "editando": editando,
        "necesidades": lista,
        "totales": totales,
        "gestor": gestor,
        "modulos": Necesidad.Modulo.choices,
        "estados": Necesidad.Estado.choices,
        "filtro": {"modulo": modulo, "estado": estado, "orden": orden},
        "filtros_qs": request.GET.urlencode(),
    })


@login_required
def lista(request):
    # La oficina se precarga con la última que usó el usuario.
    ultima = (Necesidad.objects.filter(autor_username=request.user.get_username())
              .exclude(oficina="").order_by("-creado").values_list("oficina", flat=True).first())
    return _render_lista(request, NecesidadForm(initial={"oficina": ultima or ""}))


@login_required
@require_POST
def crear(request):
    form = NecesidadForm(request.POST)
    if not form.is_valid():
        return _render_lista(request, form)
    necesidad = form.save(commit=False)
    necesidad.autor_username = request.user.get_username()
    necesidad.autor_nombre = request.user.get_full_name() or request.user.get_username()
    necesidad.save()
    messages.success(request, "Tu pedido quedó cargado. Gracias.")
    return _volver(request, necesidad.pk)


@login_required
def editar(request, pk):
    necesidad = get_object_or_404(Necesidad, pk=pk)
    if not _puede_editar(request.user, necesidad):
        raise PermissionDenied
    if request.method == "POST":
        form = NecesidadForm(request.POST, instance=necesidad)
        if form.is_valid():
            necesidad = form.save(commit=False)
            necesidad.editado = timezone.now()
            necesidad.save()
            messages.success(request, "Cambios guardados.")
            return _volver(request, necesidad.pk)
    else:
        form = NecesidadForm(instance=necesidad)
    return _render_lista(request, form, editando=necesidad)


@login_required
@require_POST
def borrar(request, pk):
    necesidad = get_object_or_404(Necesidad, pk=pk)
    if not _puede_editar(request.user, necesidad):
        raise PermissionDenied
    necesidad.delete()
    messages.success(request, "Pedido borrado.")
    return _volver(request)


@login_required
@require_POST
def apoyar(request, pk):
    necesidad = get_object_or_404(Necesidad, pk=pk)
    username = request.user.get_username()
    if necesidad.autor_username == username:
        return _volver(request, pk)
    borrados, _ = Apoyo.objects.filter(necesidad=necesidad, username=username).delete()
    if not borrados:
        try:
            Apoyo.objects.create(necesidad=necesidad, username=username)
        except IntegrityError:
            pass  # doble clic: ya quedó registrado
    return _volver(request, pk)


@login_required
@require_POST
def gestionar(request, pk):
    if not request.user.has_perm(PERM_GESTIONAR):
        raise PermissionDenied
    necesidad = get_object_or_404(Necesidad, pk=pk)
    form = GestionForm(request.POST, instance=necesidad, prefix=f"g{pk}")
    if form.is_valid():
        necesidad = form.save(commit=False)
        necesidad.respondido_por = request.user.get_username()
        necesidad.save()
        messages.success(request, f"Revisión guardada: «{necesidad.titulo}».")
    else:
        messages.error(request, "No se pudo guardar la revisión: el estado no es válido.")
    return _volver(request, pk)


@login_required
def resumen(request):
    """Texto plano con los pedidos abiertos, agrupados por parte del sistema, para la reunión."""
    abiertas = (Necesidad.objects.exclude(estado__in=Necesidad.ESTADOS_CERRADOS)
                .annotate(n_apoyos=Count("apoyos")).order_by("urgencia", "-n_apoyos", "creado"))
    lineas = [f"Necesidades y pedidos - abiertos al {timezone.localdate():%d/%m/%Y}", ""]
    for valor, etiqueta in Necesidad.Modulo.choices:
        grupo = [n for n in abiertas if n.modulo == valor]
        if not grupo:
            continue
        lineas.append(etiqueta.upper())
        for n in grupo:
            extra = f" (+{n.n_apoyos})" if n.n_apoyos else ""
            if n.estado != Necesidad.Estado.NUEVA:
                extra += f" · {n.get_estado_display()}"
            quien = n.autor_nombre + (f", {n.oficina}" if n.oficina else "")
            lineas.append(f"- [{n.get_urgencia_display()}] {n.titulo} — {quien}{extra}")
            if n.ejemplo:
                lineas.append(f"    Ej.: {n.ejemplo}")
        lineas.append("")
    if len(lineas) == 2:
        lineas.append("No hay pedidos abiertos.")
    return HttpResponse("\n".join(lineas), content_type="text/plain; charset=utf-8")
