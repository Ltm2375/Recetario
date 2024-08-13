from django.contrib.auth.hashers import make_password
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegistroUsuarioForm(UserCreationForm):
    nombres = forms.CharField(max_length=100)
    apePaterno = forms.CharField(max_length=100)
    apeMaterno = forms.CharField(max_length=100)
    fechaNacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(required=True)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), empty_label="Seleccione un departamento")
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.none(), empty_label="Seleccione una provincia")
    distrito = forms.ModelChoiceField(queryset=Distrito.objects.none(), empty_label="Seleccione un distrito")


    class Meta:
        model = User
        fields = ['username', 'email', 'password']