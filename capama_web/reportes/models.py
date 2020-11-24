from django.db import models

# Create your models here.
class Usuarios(models.Model):
    nombre = models.CharField(max_length = 45)
    apellidos = models.CharField(max_length = 45)
    email = models.EmailField()
    contrasena = models.CharField(max_length = 45)
    num_contrato = models.CharField(max_length = 45)
    telefono = models.CharField(max_length = 10)

class Empleados(models.Model):
    # son los diferentes cargos y las opciones que saldrán en el panel de administración
    CARGOS = (
        ('Administrador', 'Administrador'),
        ('Sobrestante', 'Sobrestante'),
    )

    nombre = models.CharField(max_length = 45)
    apellidos = models.CharField(max_length = 45)
    email = models.EmailField()
    contrasena = models.CharField(max_length = 45)
    telefono = models.CharField(max_length = 10)
    cargo = models.CharField(max_length=20, choices = CARGOS, default= CARGOS)
    num_empleado = models.CharField(max_length = 45)

class ReportesUsuario (models.Model):
    PRIORIDAD = (
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Grave', 'Grave')
    )

    ESTADOS = (
        ('Reportado','Reportado'),
        ('En reparación', 'En reparación'),
        ('Reparado', 'Reparado')
    )
    tipo = models.CharField(max_length = 45)
    foto = models.CharField(max_length = 50)
    prioridad = models.CharField(max_length = 20, choices=PRIORIDAD, default= PRIORIDAD)
    geoLocalizacion = models.CharField(max_length = 100)
    colonia = models.CharField(max_length = 50)
    calle = models.CharField(max_length = 50)
    cp = models.IntegerField(blank = True)
    num_interior = models.IntegerField(blank = True)
    num_exterior = models.IntegerField(blank = True)
    descripcion = models.CharField(max_length = 200)
    fecha = models.DateTimeField(auto_now_add = True)
    estado = models.CharField(max_length = 20, choices = ESTADOS, default=ESTADOS)
    id_usuario = models.ForeignKey(Usuarios, on_delete= models.CASCADE)


class ReportesEmpleado (models.Model):
    PRIORIDAD = (
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Grave', 'Grave')
    )

    ESTADOS = (
        ('Reportado','Reportado'),
        ('En reparación', 'En reparación'),
        ('Reparado', 'Reparado')
    )
    # la fecha de inicio se cambiará el auto_now_add
    fecha_inicio = models.DateTimeField(auto_now_add = True)
    fecha_fin = models.DateTimeField(auto_now_add = True)
    tipo = models.CharField(max_length = 45)
    foto = models.CharField(max_length = 50)
    prioridad = models.CharField(max_length = 20, choices=PRIORIDAD, default= PRIORIDAD)
    descripcion = models.CharField(max_length = 200)
    # -----------esos datos ya vienen implícitos en el reporte del usuario---------

    # geoLocalizacion = models.CharField(max_length = 100)
    # colonia = models.CharField(max_length = 50)
    # calle = models.CharField(max_length = 50)
    # cp = models.IntegerField(blank = True)
    # num_interior = models.IntegerField(blank = True)
    # num_exterior = models.IntegerField(blank = True)
    # fecha = models.DateTimeField(auto_now_add = True)
    estado = models.CharField(max_length = 20, choices = ESTADOS, default=ESTADOS)
    id_empleado = models.ForeignKey(Empleados, on_delete = models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete = models.DO_NOTHING)

class Materiales (models.Model):
    material = models.CharField(max_length = 50)
    cantidad = models.IntegerField()
    id_reporte_empleado = models.ForeignKey(ReportesEmpleado, on_delete=models.CASCADE)


