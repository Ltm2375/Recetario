# Generated by Django 5.0.7 on 2024-07-21 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('tipo', models.CharField(max_length=20)),
                ('paisProcedencia', models.CharField(max_length=20, null=True)),
                ('unidadMedida', models.CharField(max_length=20)),
                ('precioPromedio', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('paisProcedencia', models.CharField(max_length=50)),
                ('nroPersona', models.IntegerField(default=0)),
                ('cantidadBuscadas', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apePaterno', models.CharField(max_length=50)),
                ('apeMaterno', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('fechaNacimiento', models.DateField()),
                ('departamento', models.DateField(max_length=30)),
                ('provincia', models.DateField(max_length=30)),
                ('distrito', models.DateField(max_length=30)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecetaDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('precioEsperado', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('idIngrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioapp.ingrediente')),
                ('idReceta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioapp.receta')),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200, null=True)),
                ('fechaEnviado', models.DateTimeField(auto_now_add=True)),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inicioapp.usuario')),
            ],
        ),
    ]
