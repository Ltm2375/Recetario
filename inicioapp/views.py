from django.shortcuts import render
from .models import *
from django.db.models import Count
# Create your views here.

def index(request):
    return render(request, 'index.html')

def recetasComunes(request):
    return render(request,'recetasComunes.html')

def transparencia(request):
    return render(request,'transparencia.html')

def login(request):
    return render(request,'login.html')


def asistenciaTecnica(request):
    return render(request,'asistenciaTecnica.html')

def historialRecetas(request):
    return render(request,'historialRecetas.html')

def indexRegistrar(request):
    return render(request,'registrarUsuario.html')



def indexBuscarReceta(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'buscarReceta.html', {'ingredientes': ingredientes})

def buscar_receta(request):
    
    if request.method == 'POST':
        
        ingredientes_ids = request.POST.getlist('ingredientes_ids')
        if len(ingredientes_ids) < 3:
            return render(request, 'buscarReceta.html', {'error': 'Se deben seleccionar al menos 3 ingredientes.'})
        
        # Encuentra las recetas que contienen al menos 3 de los ingredientes seleccionados
        recetas = Receta.objects.filter(
            recetadetalle__idIngrediente__in=ingredientes_ids
        ).annotate(
            num_ingredientes=Count('recetadetalle')
        ).filter(
            num_ingredientes__gte=3
        ).distinct()

        return render(request, 'mostrarRecetas.html', {'recetas': recetas})

    return render(request, 'inicio.html')
