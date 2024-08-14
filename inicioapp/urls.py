from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="inicio"),
    path('recetasComunes/',views.recetasComunes, name="recetasComunes"),
    path('transparencia/',views.transparencia, name="transparencia"),
    path('indexlogin/',views.indexlogin, name="indexlogin"),
    path('indexBuscarReceta/',views.indexBuscarReceta, name="indexBuscarReceta"),
    path('asistencia/',views.asistenciaTecnica, name= "asistencia"),
    path('indexRegistrar/',views.indexRegistrar, name="indexRegistrar"),
    path('buscarReceta/',views.buscar_receta,name="buscarReceta"),
    path('registrar/',views.indexRegistrar,name="indexRegistrar"),
    path('provincias/',views.provincias_por_departamento,name="provincias_por_departamento"),
    path('distritos/',views.distritos_por_provincia,name="distritos_por_provincia"),
    path('registrarUsuario/',views.registrar_usuario,name="registraUsuario"),
    path('loginUsuario/',views.loginUsuario,name="loginUsuario"),
    path('cerrarSesion/',views.logoutUsuario,name="logoutUsuario"),
    path('historialBusquedas/',views.historial_recetas,name="historial_recetas")
]