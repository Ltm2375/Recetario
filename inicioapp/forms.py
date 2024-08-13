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
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(), empty_label="Seleccione una provincia")
    distrito = forms.ModelChoiceField(queryset=Distrito.objects.all(), empty_label="Seleccione un distrito")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('departamento'):
            self.fields['provincia'].queryset = Provincia.objects.filter(departamento_id=self.initial['departamento'])
        if self.initial.get('provincia'):
            self.fields['distrito'].queryset = Distrito.objects.filter(provincia_id=self.initial['provincia'])
    
    def clean(self):
        cleaned_data = super().clean()
        departamento_id = cleaned_data.get('departamento')
        provincia_id = cleaned_data.get('provincia')
        distrito_id = cleaned_data.get('distrito')
        if departamento_id and isinstance(departamento_id, str):
            departamento_id = int(departamento_id)
            if not Departamento.objects.filter(id=departamento_id).exists():
                self.add_error('departamento', 'Seleccione un departamento válido.')

        if provincia_id and isinstance(provincia_id, str):
            provincia_id = int(provincia_id)
            if not Provincia.objects.filter(id=provincia_id).exists():
                self.add_error('provincia', 'Seleccione una provincia válida.')

        if distrito_id and isinstance(distrito_id, str):
            distrito_id = int(distrito_id)
            if not Distrito.objects.filter(id=distrito_id).exists():
                self.add_error('distrito', 'Seleccione un distrito válido.')

        return cleaned_data

