from django.db import models

# Create your models here.
class Usuarios(models.Model):
    nombre = models.CharField(max_length = 45)
    apellidos = models.CharField(max_length = 45)
    email = models.EmailField()
    contrasena = models.CharField(max_length = 45)
    num_contrato = models.CharField(max_length = 45)
    telefono = models.CharField(max_length = 10)
    
    # para mostrar en el sitio de administración la llave foránea, pero de forma más detallada
    # también para que al mostrar la tabla, se muestren los registros de forma detallada
    # el id marca error porque no está definido aquí en el modelo, pero este se asignó de forma automática

    def __str__(self):
        return ("%d.- %s %s" % ( self.id, self.nombre, self.apellidos))
    
    
    class Meta:
        verbose_name_plural= 'Usuarios'

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


    def __str__(self):
        return ("%d.- %s %s" % ( self.id, self.nombre, self.apellidos))

    class Meta:
        verbose_name_plural= 'Empleados'

class ReportesUsuario (models.Model):
    PRIORIDAD = (
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Grave', 'Grave')
    )

    ESTADOS = (
        ('Nuevo','Nuevo'),
        ('En proceso', 'En proceso'),
        ('Monitoreado', 'Monitoreado'),
        ('Atendido', 'Atendido')
    )

    ZONA = (        
        ('Nuevos desarrollos','Nuevos desarrollos'),
        ('Urbana', 'Urbana'),
        ('Conurbada', 'Conurbada')
    )
    TIPOANOMALIA = (
        ('Falta de agua','Falta de agua'),
        ('Falta de presion', 'Falta de presion'),
        ('Fuga en la red Hidraulica', 'Fuga en la red Hidraulica'),
        ('Fuga en la toma','Fuga en la toma'),
        ('Inspeccion', 'Inspeccion'),
        ('Material listo', 'Material listo'),
        ('Toma obstruida','Toma obstruida'),
        ('Toma desconectada', 'Toma desconectada'),
        ('Desazolve', 'Desazolve')
    )

    TIPOSERVICIO =(       
        ('Agua potable','Agua potable'),
        ('Pipas', 'Pipas'),
        ('Alcantarillado', 'Alcantarillado')
    )

    zona = models.CharField(max_length = 50, choices=ZONA, default= ZONA )
    tipo_anomalia = models.CharField(max_length = 50, choices=TIPOANOMALIA, default= TIPOANOMALIA)
    tipo_servicio = models.CharField(max_length = 50, choices=TIPOSERVICIO, default= TIPOSERVICIO)
    folio_seguimiento = models.CharField(max_length = 50, blank = True)
    foto = models.CharField(max_length = 50)
    prioridad = models.CharField(max_length = 20, choices=PRIORIDAD, default= PRIORIDAD)
    geoLocalizacion = models.CharField(max_length = 100, verbose_name='Geolocalización')
    colonia = models.CharField(max_length = 50)
    calle = models.CharField(max_length = 50)
    cp = models.IntegerField(blank = True, verbose_name='código postal')
    num_interior = models.IntegerField(blank = True)
    num_exterior = models.IntegerField(blank = True)
    descripcion = models.CharField(max_length = 200)
    fecha = models.DateTimeField(auto_now_add = True)
    estado = models.CharField(max_length = 20, choices = ESTADOS, default=ESTADOS)
    id_usuario = models.ForeignKey(Usuarios, on_delete= models.CASCADE)

    # mostrar el folio de seguimiento
    def __str__(self):
        return self.folio_seguimiento
    

    class Meta:
        verbose_name_plural= 'Reportes del usuario'


class ReportesEmpleado (models.Model):
    PRIORIDAD = (
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Grave', 'Grave')
    )
    ESTADOS = (
        ('Nuevo','Nuevo'),
        ('En proceso', 'En proceso'),
        ('Monitoreado', 'Monitoreado'),
        ('Atendido', 'Atendido')
    )
    ZONA = (        
        ('Nuevos desarrollos','Nuevos desarrollos'),
        ('Urbana', 'Urbana'),
        ('Conurbada', 'Conurbada')
    )
    TIPOANOMALIA = (
        ('Falta de agua','Falta de agua'),
        ('Falta de presion', 'Falta de presion'),
        ('Fuga en la red Hidraulica', 'Fuga en la red Hidraulica'),
        ('Fuga en la toma','Fuga en la toma'),
        ('Inspeccion', 'Inspeccion'),
        ('Material listo', 'Material listo'),
        ('Toma obstruida','Toma obstruida'),
        ('Toma desconectada', 'Toma desconectada'),
        ('Desazolve', 'Desazolve')
    )

    TIPOSERVICIO =(       
        ('Agua potable','Agua potable'),
        ('Pipas', 'Pipas'),
        ('Alcantarillado', 'Alcantarillado')
    )
    # la fecha de inicio se cambiará el auto_now_add
    fecha_inicio = models.DateTimeField(auto_now_add = True)
    fecha_fin = models.DateTimeField(auto_now_add = True)
    zona = models.CharField(max_length = 40, choices=ZONA, default= ZONA)
    tipo_anomalia = models.CharField(max_length = 50, choices=TIPOANOMALIA, default= TIPOANOMALIA)
    tipo_servicio = models.CharField(max_length = 50, choices=TIPOSERVICIO, default= TIPOSERVICIO)
    folio_seguimiento = models.CharField(max_length = 50, blank = True)
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
    
    # mostrar el folio de seguimiento
    def __str__(self):
        return self.folio_seguimiento
    
    class Meta:
        verbose_name_plural= 'Reportes del empleado'

class Materiales (models.Model):
    material = models.CharField(max_length = 50)
    cantidad = models.IntegerField()
    id_reporte_empleado = models.ForeignKey(ReportesEmpleado, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural= 'Materiales'
    

