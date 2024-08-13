from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="inicio"),
    path('recetasComunes/',views.recetasComunes, name="recetasComunes"),
    path('transparencia/',views.transparencia, name="transparencia"),
    path('login/',views.login, name="login"),
    path('indexBuscarReceta/',views.indexBuscarReceta, name="indexBuscarReceta"),
    path('asistencia/',views.asistenciaTecnica, name= "asistencia"),
    path('historialReceta/',views.historialRecetas, name="historialRecetas"),
    path('index/',views.indexRegistrar, name="indexRegistrar"),
    path('buscarReceta/',views.buscar_receta,name="buscarReceta"),
    path('registrar/',views.indexRegistrar,name="indexRegistrar")
]