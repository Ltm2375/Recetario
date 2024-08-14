from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'index.html')

def recetasComunes(request):
    return render(request,'recetasComunes.html')

def transparencia(request):
    return render(request,'transparencia.html')

def indexlogin(request):
    return render(request,'login.html')

def asistenciaTecnica(request):
    razones = ['Receta no encontrada','Ingrediente no encontrado','Problema con búsqueda','Problema con historial de recetas','Otro tipo de razón']
    return render(request,'asistenciaTecnica.html',{'razones': razones})

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

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            print("Datos del formulario:", form.cleaned_data)
            user = form.save()
            PerfilUsuario.objects.create(
                user=user,
                nombres=form.cleaned_data['nombres'],
                apePaterno=form.cleaned_data['apePaterno'],
                apeMaterno=form.cleaned_data['apeMaterno'],
                fechaNacimiento=form.cleaned_data['fechaNacimiento'],
                email=form.cleaned_data['email'],
                departamento=form.cleaned_data['departamento'],
                provincia=form.cleaned_data['provincia'],
                distrito=form.cleaned_data['distrito']
            )
            login(request, user)
            return redirect('indexlogin')
        else:
            #opciones para depurar
            print("Errores del formulario:", form.errors)
            print("Datos enviados:", request.POST)
            print("Departamentos disponibles:", Departamento.objects.all())
            print("Provincias disponibles:", Provincia.objects.all())
            print("Distritos disponibles:", Distrito.objects.all())
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registrarUsuario.html', {'form': form})

def loginUsuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')  # Redirige a la página de inicio o donde desees
        else:
            messages.error(request, 'Usuario o contraseña incorrectos. Inténtalo de nuevo.')
    return render(request, 'login.html')

def logoutUsuario(request):
    logout(request)
    return redirect('inicio')


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
        if ingredientes_ids:
            ids_str = ingredientes_ids[0]  # Obtiene la primera cadena de la lista
            ids_list = ids_str.split(',')  # Divide la cadena en una lista de IDs

        if len(ids_list) < 3:
            return redirect('indexBuscarReceta')
        
        ingredientes_ids_list = [int(id_str) for id_str in ids_str.split(',')]
        # Encuentra las recetas que contienen al menos 3 de los ingredientes seleccionados
        recetas = Receta.objects.filter(
            recetadetalle__idIngrediente__in=ingredientes_ids_list
        ).annotate(
            num_ingredientes=Count('recetadetalle')
        ).filter(
            num_ingredientes__gte=3
        ).distinct()
        
        # Registrar el historial de recetas
        if request.user.is_authenticated:
            for receta in recetas:
                # Verificar si ya existe un historial para esta receta y usuario
                if not HistorialRecetas.objects.filter(user=request.user, receta_id=receta).exists():
                    HistorialRecetas.objects.create(
                        user=request.user,
                        receta_id=receta,
                    )

        return render(request, 'mostrarRecetas.html', {'recetas': recetas})

    return render(request, 'inicio.html')

def historial_recetas(request):
    
    # Consulta las recetas buscadas por el usuario logueado
    historial = HistorialRecetas.objects.filter(user=request.user).values('receta_id','fechaBuscada').annotate(
        cantidad_busquedas=Count('receta_id')
    ).order_by('-cantidad_busquedas')  # Ordenar por cantidad de búsquedas descendente

    # Obtén los IDs de recetas
    receta_ids = [entry['receta_id'] for entry in historial]
    
    # Obtén las recetas completas
    recetas = Receta.objects.filter(id__in=receta_ids)

    # Mapea recetas a sus conteos
    receta_dict = {receta.id: receta for receta in recetas}

    # Agrega información de receta y cantidad de búsquedas
    historial_con_recetas = [
        {
            'receta': receta_dict[entry['receta_id']],
            'fechaBuscada': entry['fechaBuscada']
        }
        for entry in historial
    ]

    return render(request, 'historialRecetas.html', {'historial_recetas': historial_con_recetas})

@login_required
def asistenciaTecnica(request):
    razones = [
        'Receta no encontrada',
        'Ingrediente no encontrado',
        'Problema con búsqueda',
        'Problema con historial de recetas',
        'Otro tipo de razón'
    ]
    
    if request.method == 'POST':
        razon_texto = request.POST.get('razon_texto')  # Obtener el texto del select
        motivo = request.POST.get('motivo', '').strip()
        checkbox_checked = 'checkbox' in request.POST

        if checkbox_checked:
            razon = motivo if motivo else 'Otra razón'
        else:
            razon = razon_texto if razon_texto else 'Otra razón'

        descripcion = request.POST.get('descripcion', '').strip()

        if razon:  # Asegurarse de que el campo 'razon' no esté vacío
            mensaje = Mensaje(
                idUsuario=request.user,
                razon=razon,
                descripcion=descripcion
            )
            mensaje.save()
            return redirect('asistencia')  # Reemplaza con la URL a la que redirigir después de guardar
        else:
            return render(request, 'asistenciaTecnica.html', {'razones': razones, 'error': 'Debes seleccionar una razón o ingresar un motivo.'})

    return render(request, 'asistenciaTecnica.html', {'razones': razones})
