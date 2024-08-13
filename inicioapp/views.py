from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Count
from django.http import JsonResponse
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
    form = RegistroUsuarioForm()
    departamentos = Departamento.objects.all()
    context = {
        'form': form,
        'departamentos': departamentos,
    }
    return render(request, 'registrarUsuario.html', context)

def provincias_por_departamento(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = Provincia.objects.filter(departamento_id=departamento_id).values('id', 'nombre')
    return JsonResponse(list(provincias), safe=False)

def distritos_por_provincia(request):
    provincia_id = request.GET.get('provincia_id')
    distritos = Distrito.objects.filter(provincia_id=provincia_id).values('id', 'nombre')
    return JsonResponse(list(distritos), safe=False)

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
