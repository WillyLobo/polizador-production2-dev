from django.urls import path

from necesidades import views

app_name = "necesidades"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("nueva/", views.crear, name="crear"),
    path("<int:pk>/editar/", views.editar, name="editar"),
    path("<int:pk>/borrar/", views.borrar, name="borrar"),
    path("<int:pk>/apoyar/", views.apoyar, name="apoyar"),
    path("<int:pk>/gestionar/", views.gestionar, name="gestionar"),
    path("resumen.txt", views.resumen, name="resumen"),
]
