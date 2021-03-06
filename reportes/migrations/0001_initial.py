# Generated by Django 3.0.2 on 2020-12-09 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=45, verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('contrasena', models.CharField(max_length=45, verbose_name='Contraseña')),
                ('telefono', models.CharField(max_length=10, verbose_name='Teléfono')),
                ('cargo', models.CharField(choices=[('Administrador', 'Administrador'), ('Sobrestante', 'Sobrestante')], default=(('Administrador', 'Administrador'), ('Sobrestante', 'Sobrestante')), max_length=20, verbose_name='Cargo')),
                ('num_empleado', models.CharField(max_length=45, verbose_name='Número de empleado')),
                ('colonia', models.CharField(max_length=45, verbose_name='Colonia')),
                ('calle', models.CharField(max_length=45, verbose_name='Calle')),
                ('cp', models.IntegerField(blank=True, default=0, verbose_name='Código Postal')),
                ('zona', models.CharField(choices=[('Nuevos desarrollos', 'Nuevos desarrollos'), ('Urbana', 'Urbana'), ('Conurbada', 'Conurbada')], default=(('Nuevos desarrollos', 'Nuevos desarrollos'), ('Urbana', 'Urbana'), ('Conurbada', 'Conurbada')), max_length=50)),
                ('disponibilidad', models.TextField(choices=[('Disponible', 'Disponible'), ('En fuga', 'En fuga')], default='Disponible', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Empleados',
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, verbose_name='Nombre')),
                ('apellidos', models.CharField(max_length=45, verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('contrasena', models.CharField(max_length=45, verbose_name='Contraseña')),
                ('num_contrato', models.CharField(max_length=45, verbose_name='Número de contrato')),
                ('telefono', models.CharField(max_length=10, verbose_name='Teléfono')),
                ('colonia', models.CharField(max_length=45, verbose_name='Colonia')),
                ('calle', models.CharField(max_length=45, verbose_name='Calle')),
                ('cp', models.IntegerField(blank=True, default=0, verbose_name='Código Postal')),
            ],
            options={
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='ReportesUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona', models.CharField(choices=[('Nuevos desarrollos', 'Nuevos desarrollos'), ('Urbana', 'Urbana'), ('Conurbada', 'Conurbada')], default=(('Nuevos desarrollos', 'Nuevos desarrollos'), ('Urbana', 'Urbana'), ('Conurbada', 'Conurbada')), max_length=50)),
                ('tipo_anomalia', models.CharField(choices=[('Falta de agua', 'Falta de agua'), ('Falta de presion', 'Falta de presion'), ('Fuga en la red Hidraulica', 'Fuga en la red Hidraulica'), ('Fuga en la toma', 'Fuga en la toma'), ('Inspeccion', 'Inspeccion'), ('Material listo', 'Material listo'), ('Toma obstruida', 'Toma obstruida'), ('Toma desconectada', 'Toma desconectada'), ('Desazolve', 'Desazolve')], default=(('Falta de agua', 'Falta de agua'), ('Falta de presion', 'Falta de presion'), ('Fuga en la red Hidraulica', 'Fuga en la red Hidraulica'), ('Fuga en la toma', 'Fuga en la toma'), ('Inspeccion', 'Inspeccion'), ('Material listo', 'Material listo'), ('Toma obstruida', 'Toma obstruida'), ('Toma desconectada', 'Toma desconectada'), ('Desazolve', 'Desazolve')), max_length=50)),
                ('tipo_servicio', models.CharField(choices=[('Agua potable', 'Agua potable'), ('Pipas', 'Pipas'), ('Alcantarillado', 'Alcantarillado')], default=(('Agua potable', 'Agua potable'), ('Pipas', 'Pipas'), ('Alcantarillado', 'Alcantarillado')), max_length=50)),
                ('folio_seguimiento', models.CharField(max_length=50, unique=True)),
                ('foto', models.CharField(max_length=50)),
                ('prioridad', models.CharField(choices=[('Leve', 'Leve'), ('Moderada', 'Moderada'), ('Grave', 'Grave')], default=(('Leve', 'Leve'), ('Moderada', 'Moderada'), ('Grave', 'Grave')), max_length=20)),
                ('geolocalizacion', models.CharField(max_length=100, verbose_name='Geolocalización')),
                ('colonia', models.CharField(max_length=50)),
                ('calle', models.CharField(max_length=50)),
                ('cp', models.IntegerField(blank=True, verbose_name='código postal')),
                ('num_interior', models.IntegerField(blank=True, default=0)),
                ('num_exterior', models.IntegerField(blank=True, default=0)),
                ('descripcion', models.CharField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('Nuevo', 'Nuevo'), ('En proceso', 'En proceso'), ('Monitoreado', 'Monitoreado'), ('Atendido', 'Atendido')], default=(('Nuevo', 'Nuevo'), ('En proceso', 'En proceso'), ('Monitoreado', 'Monitoreado'), ('Atendido', 'Atendido')), max_length=20)),
                ('id_empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='reportes.Empleados', verbose_name='Empleado')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reportes.Usuarios', verbose_name='Usuario')),
            ],
            options={
                'verbose_name_plural': 'Reportes del usuario',
            },
        ),
        migrations.CreateModel(
            name='ReportesEmpleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(auto_now_add=True)),
                ('fecha_fin', models.DateTimeField(auto_now_add=True)),
                ('zona', models.CharField(choices=[('Nuevos desarrollos', 'Nuevos desarrollos'), ('Urbana', 'Urbana'), ('Conurbada', 'Conurbada')], default=(('Nuevos desarrollos', 'Nuevos desarrollos'), ('Urbana', 'Urbana'), ('Conurbada', 'Conurbada')), max_length=40)),
                ('tipo_anomalia', models.CharField(choices=[('Falta de agua', 'Falta de agua'), ('Falta de presion', 'Falta de presion'), ('Fuga en la red Hidraulica', 'Fuga en la red Hidraulica'), ('Fuga en la toma', 'Fuga en la toma'), ('Inspeccion', 'Inspeccion'), ('Material listo', 'Material listo'), ('Toma obstruida', 'Toma obstruida'), ('Toma desconectada', 'Toma desconectada'), ('Desazolve', 'Desazolve')], default=(('Falta de agua', 'Falta de agua'), ('Falta de presion', 'Falta de presion'), ('Fuga en la red Hidraulica', 'Fuga en la red Hidraulica'), ('Fuga en la toma', 'Fuga en la toma'), ('Inspeccion', 'Inspeccion'), ('Material listo', 'Material listo'), ('Toma obstruida', 'Toma obstruida'), ('Toma desconectada', 'Toma desconectada'), ('Desazolve', 'Desazolve')), max_length=50)),
                ('tipo_servicio', models.CharField(choices=[('Agua potable', 'Agua potable'), ('Pipas', 'Pipas'), ('Alcantarillado', 'Alcantarillado')], default=(('Agua potable', 'Agua potable'), ('Pipas', 'Pipas'), ('Alcantarillado', 'Alcantarillado')), max_length=50)),
                ('foto', models.CharField(max_length=50)),
                ('prioridad', models.CharField(choices=[('Leve', 'Leve'), ('Moderada', 'Moderada'), ('Grave', 'Grave')], default=(('Leve', 'Leve'), ('Moderada', 'Moderada'), ('Grave', 'Grave')), max_length=20)),
                ('descripcion', models.CharField(max_length=200)),
                ('estado', models.CharField(choices=[('Nuevo', 'Nuevo'), ('En proceso', 'En proceso'), ('Monitoreado', 'Monitoreado'), ('Atendido', 'Atendido')], default=(('Nuevo', 'Nuevo'), ('En proceso', 'En proceso'), ('Monitoreado', 'Monitoreado'), ('Atendido', 'Atendido')), max_length=20)),
                ('id_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reportes.Empleados', verbose_name='Empleado')),
                ('id_repoteUsuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='reportes.ReportesUsuario', verbose_name='Folio seguimiento')),
            ],
            options={
                'verbose_name_plural': 'Reportes del empleado',
            },
        ),
        migrations.CreateModel(
            name='Materiales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
                ('id_reporte_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reportes.ReportesEmpleado')),
            ],
            options={
                'verbose_name_plural': 'Materiales',
            },
        ),
    ]
