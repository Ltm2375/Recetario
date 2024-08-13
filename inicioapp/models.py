from django.db import models
from django.db.models import *
from django.contrib.auth.models import User
# Create your models here.

class Receta(models.Model):
    nombre = models.CharField(max_length=50,null=False)
    paisProcedencia = models.CharField(max_length=50, null=False)
    nroPersona = models.IntegerField(default=0,null=False)
    cantidadBuscadas= models.IntegerField(default=0,null=True)
    def __str__(self) -> str:
        return self.nombre

class Ingrediente(models.Model):
    nombre= models.CharField(max_length=50, null=False)
    tipo = models.CharField(max_length=20,null=False)
    paisProcedencia = models.CharField(max_length=20, null=True)
    unidadMedida = models.CharField(max_length=20, null=False)
    precioPromedio = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0.00)#max_digits: Este argumento es obligatorio y define el número máximo de dígitos que el número puede tener en total. 
    #decimal_places: Este argumento es obligatorio y define el número de dígitos que puede haber después del punto decimal.
    def __str__(self) -> str:
        return self.nombre


class RecetaDetalle(models.Model):
    idReceta = models.ForeignKey(Receta, on_delete=models.CASCADE)#se pone el cascade para que cuando se elimine una receta se eliminarán sus detalles
    idIngrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0,null=False)
    precioEsperado = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, null=False)

    def __str__(self) -> str:
        return self.idReceta.nombre + ' ' + self.idIngrediente.nombre
    

class Mensaje(models.Model):
    idUsuario = models.ForeignKey(User,on_delete=models.CASCADE)
    razon = models.CharField(max_length=100, blank=False , null=False)
    descripcion = models.CharField(max_length=200, null=True)
    fechaEnviado = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.idUsuario} - {self.razon}"

class Departamento(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='provincias')

    def __str__(self):
        return self.nombre

class Distrito(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='distritos')

    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apePaterno = models.CharField(max_length=100)
    apeMaterno = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    email = models.EmailField()
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
