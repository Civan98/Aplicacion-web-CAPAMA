from django.db import models

# Create your models here.
class Usuarios(models.Model):
    nombre = models.CharField(max_length = 45, verbose_name='Nombre')
    apellidos = models.CharField(max_length = 45, verbose_name= 'Apellidos')
    email = models.EmailField(verbose_name='Email', unique=True ) 
    contrasena = models.CharField(max_length = 45, verbose_name='Contraseña')
    num_contrato = models.CharField(max_length = 45, unique=True, verbose_name= 'Número de contrato')
    telefono = models.CharField(max_length = 10, verbose_name= 'Teléfono')
    colonia = models.CharField(max_length=45, verbose_name='Colonia')
    calle = models.CharField(max_length=45, verbose_name='Calle')
    cp = models.IntegerField(verbose_name='Código Postal', blank= True, default=00000)
    
    # para mostrar en el sitio de administración la llave foránea, pero de forma más detallada
    # también para que al mostrar la tabla, se muestren los registros de forma detallada
    # el id marca error porque no está definido aquí en el modelo, pero este se asignó de forma automática

    def __str__(self):
        return ("%s  %s %s" % (self.num_contrato, self.nombre, self.apellidos))
    
    
    class Meta:
        verbose_name_plural= 'Usuarios'

class Empleados(models.Model):
    # son los diferentes cargos y las opciones que saldrán en el panel de administración
    CARGOS = (
        ('Administrador', 'Administrador'),
        ('Sobrestante', 'Sobrestante'),
        ('Pipas', 'Pipas'),
        ('Alcantarillado', 'Alcantarillado')        
    )
    ZONA = (        
        ('Nuevos desarrollos','Nuevos desarrollos'),
        ('Urbana', 'Urbana'),
        ('Conurbada', 'Conurbada')
    )
    DISPONIBLE =(
        ('Disponible','Disponible'),
        ('En fuga','En fuga'),
        ('Fuera de servicio','Fuera de servicio')
    )
    nombre = models.CharField(max_length = 45, verbose_name='Nombre')
    apellidos = models.CharField(max_length = 45, verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Email', unique=True)
    contrasena = models.CharField(max_length = 45, verbose_name='Contraseña')
    telefono = models.CharField(max_length = 10, verbose_name='Teléfono')
    cargo = models.CharField(max_length=20, choices = CARGOS, default= CARGOS, verbose_name='Cargo')
    num_empleado = models.CharField(max_length = 45, unique=True, verbose_name='Número de empleado')
    colonia = models.CharField(max_length=45, verbose_name='Colonia')
    calle = models.CharField(max_length=45, verbose_name='Calle')
    cp = models.IntegerField(verbose_name='Código Postal', blank= True, default=00000)
    zona = models.CharField(max_length = 50, choices=ZONA, default= ZONA )
    disponibilidad = models.TextField(max_length=50, choices=DISPONIBLE, default='Disponible')


    def __str__(self):
        return ("%s   %s %s" % ( self.num_empleado, self.nombre, self.apellidos))

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
    folio_seguimiento = models.CharField(max_length = 50, unique=True)
    foto = models.CharField(max_length = 200)
    prioridad = models.CharField(max_length = 20, choices=PRIORIDAD, default= PRIORIDAD)
    geolocalizacion = models.CharField(max_length = 200, verbose_name='Geolocalización')
    colonia = models.CharField(max_length = 50)
    calle = models.CharField(max_length = 50)
    cp = models.IntegerField(blank = True, verbose_name='código postal')
    num_interior = models.IntegerField(blank = True, default=0)
    num_exterior = models.IntegerField(blank = True, default= 0)
    descripcion = models.CharField(max_length = 200)
    fecha = models.DateTimeField(auto_now_add = True)
    estado = models.CharField(max_length = 20, choices = ESTADOS, default=ESTADOS)
    id_usuario = models.ForeignKey(Usuarios, on_delete = models.CASCADE, verbose_name='Usuario')
    id_empleado = models.ForeignKey(Empleados, on_delete = models.DO_NOTHING, blank= True, null=True, verbose_name='Empleado')

    # mostrar el folio de seguimiento
    def __str__(self):
        return ("%d.- %s" % ( self.id, self.folio_seguimiento))
    

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
    # folio_seguimiento = models.CharField(max_length = 50, unique=True)
    foto = models.CharField(max_length = 200)
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
    id_empleado = models.ForeignKey(Empleados, on_delete = models.CASCADE, verbose_name='Empleado')
    id_repoteUsuario = models.ForeignKey(ReportesUsuario, on_delete = models.DO_NOTHING, verbose_name='Folio seguimiento')
    # id_usuario = models.ForeignKey(Usuarios, on_delete = models.DO_NOTHING)
    
    # mostrar el folio de seguimiento
    def __str__(self):
        return str(self.id_repoteUsuario)
    
    class Meta:
        verbose_name_plural= 'Reportes del empleado'

class Materiales (models.Model):
    material = models.CharField(max_length = 50)
    cantidad = models.IntegerField()
    id_reporte_empleado = models.ForeignKey(ReportesEmpleado, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural= 'Materiales'
    

