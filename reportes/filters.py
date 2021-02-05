import django_filters
from django import forms
from django_filters import DateFilter, CharFilter

from .models import *

#para mostrar el calendar en vez de un field simple
class DateInput(forms.DateInput):
    input_type = 'fecha'

class ReportesUsuarioFilter(django_filters.FilterSet):

    ZONA = (
        ('','---------'),        
        ('Nuevos desarrollos','Nuevos desarrollos'),
        ('Urbana', 'Urbana'),
        ('Conurbada', 'Conurbada')
        )

    TIPOSERVICIO = (       
        ('','---------'),
        ('Agua potable','Agua potable'),
        ('Pipas', 'Pipas'),
        ('Alcantarillado', 'Alcantarillado')
    )
    TIPOANOMALIA = (
         ('','---------'),
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
    PRIORIDAD = (
        ('','---------'),
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Grave', 'Grave')
    )
    #los dos campos siguiente se utilizan para poder filtrar por ragos de fecha
    start_date = DateFilter(field_name="fecha", lookup_expr='gte', widget=forms.TextInput(attrs={'id':'datepicker'}))
    end_date = DateFilter(field_name="fecha", lookup_expr='lte',label='Fecha menor que', widget=forms.TextInput(attrs={'id':'datepicker2'}))
    
    # se agrega el charfilter para que filtre sin escribir todo el campo, resultados relacionados
    folio_seguimiento = CharFilter(field_name='folio_seguimiento', lookup_expr='icontains', label='Folio seguimiento',widget=forms.TextInput(attrs={'class':'form-control'}))
    descripcion =  CharFilter(field_name='descripcion', lookup_expr='icontains', label='Descripción',widget=forms.TextInput(attrs={'class':'form-control'}))
    colonia =  CharFilter(field_name='colonia', lookup_expr='icontains', label='Colonia',widget=forms.TextInput(attrs={'class':'form-control'}))
    calle =  CharFilter(field_name='calle', lookup_expr='icontains', label='Calle',widget=forms.TextInput(attrs={'class':'form-control'}))
    cp =  CharFilter(field_name='cp', lookup_expr='icontains', label='C.P.',widget=forms.TextInput(attrs={'class':'form-control'}))
    num_interior =  CharFilter(field_name='num_interior', lookup_expr='icontains', label='Número interior',widget=forms.TextInput(attrs={'class':'form-control'}))
    num_exterior =  CharFilter(field_name='num_exterior', lookup_expr='icontains', label='Número exterior',widget=forms.TextInput(attrs={'class':'form-control'}))
    zona =  CharFilter(field_name='zona', lookup_expr='icontains', label='Zona',widget=forms.Select(attrs={'class':'form-control'},choices=ZONA))
    tipo_servicio =  CharFilter(field_name='tipo_servicio', lookup_expr='icontains', label='Tipo de servicio',widget=forms.Select(attrs={'class':'form-control'},choices=TIPOSERVICIO,))
    tipo_anomalia =  CharFilter(field_name='tipo_anomalia', lookup_expr='icontains', label='Tipo de anomalía',widget=forms.Select(attrs={'class':'form-control'},choices=TIPOANOMALIA,))
    prioridad =  CharFilter(field_name='prioridad', lookup_expr='icontains', label='prioridad',widget=forms.Select(attrs={'class':'form-control'},choices=PRIORIDAD,))


    class Meta:
        model = ReportesUsuario
        fields = '__all__'
        exclude = ['fecha', 'geolocalizacion', 'foto']

class DateInput2(forms.DateInput):
    input_type = 'fecha_inicio'
    input_type = 'fecha_fin'

class ReportesEmpleadoFilter(django_filters.FilterSet):
    
    ZONA = (
        ('','---------'),        
        ('Nuevos desarrollos','Nuevos desarrollos'),
        ('Urbana', 'Urbana'),
        ('Conurbada', 'Conurbada')
        )

    TIPOSERVICIO = (       
        ('','---------'),
        ('Agua potable','Agua potable'),
        ('Pipas', 'Pipas'),
        ('Alcantarillado', 'Alcantarillado')
    )
    TIPOANOMALIA = (
         ('','---------'),
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
    PRIORIDAD = (
        ('','---------'),
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Grave', 'Grave')
    )

    start_date = CharFilter(field_name='fecha_inicio',lookup_expr='gte',label='Fecha inicio',  widget=forms.TextInput(attrs={'id':'datepicker'}))
    end_date = CharFilter(field_name='fecha_inicio',lookup_expr='lte', label='Fecha inicio menor que',  widget=forms.TextInput(attrs={'id':'datepicker2'}))

    start_date2 = CharFilter(field_name='fecha_fin',lookup_expr='gte',  widget=forms.TextInput(attrs={'id':'datepicker'}))
    end_date2 =  CharFilter(field_name='fecha_fin',lookup_expr='lte', label='Fecha fin menor que', widget=forms.TextInput(attrs={'id':'datepicker'}))
    
    # se agrega el charfilter para que filtre sin escribir todo el campo, resultados relacionados

    class Meta:
        model = ReportesEmpleado
        fields = '__all__'
        exclude = ['fecha_inicio', 'fecha_fin','foto']


class MostrarUsuarioFilter(django_filters.FilterSet):
    

    # se agrega el charfilter para que filtre sin escribir todo el campo, resultados relacionados
    nombre = CharFilter(field_name='nombre', lookup_expr='icontains', label='Nombre',widget=forms.TextInput(attrs={'class':'form-control'}))
    apellidos = CharFilter(field_name='apellidos', lookup_expr='icontains', label='Apellidos',widget=forms.TextInput(attrs={'class':'form-control'}))
    email= CharFilter(field_name='email', lookup_expr='icontains', label='Email',widget=forms.TextInput(attrs={'class':'form-control'}))
    contrasena = CharFilter(field_name='contrasena', lookup_expr='icontains', label='Contraseña',widget=forms.TextInput(attrs={'class':'form-control'}))
    num_contrato = CharFilter(field_name='num_contrato', lookup_expr='icontains', label='Número de contrato',widget=forms.TextInput(attrs={'class':'form-control'}))
    colonia = CharFilter(field_name='colonia', lookup_expr='icontains', label='Colonia',widget=forms.TextInput(attrs={'class':'form-control'}))
    calle = CharFilter(field_name='calle', lookup_expr='icontains', label='Calle',widget=forms.TextInput(attrs={'class':'form-control'}))
    cp = CharFilter(field_name='cp', lookup_expr='icontains', label='C.P.',widget=forms.TextInput(attrs={'class':'form-control'}))
    telefono = CharFilter(field_name='telefono', lookup_expr='icontains', label='Teléfono',widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model = Usuarios
        fields = '__all__'
      


class MostrarEmpleadoFilter(django_filters.FilterSet):
    

    # se agrega el charfilter para que filtre sin escribir todo el campo, resultados relacionados
    nombre = CharFilter(field_name='nombre', lookup_expr='icontains', label='Nombre',widget=forms.TextInput(attrs={'class':'form-control'}))
    apellidos = CharFilter(field_name='apellidos', lookup_expr='icontains', label='Apellidos',widget=forms.TextInput(attrs={'class':'form-control'}))
    email= CharFilter(field_name='email', lookup_expr='icontains', label='Email',widget=forms.TextInput(attrs={'class':'form-control'}))
    contrasena = CharFilter(field_name='contrasena', lookup_expr='icontains', label='Contraseña',widget=forms.TextInput(attrs={'class':'form-control'}))
    telefono = CharFilter(field_name='telefono', lookup_expr='icontains', label='Teléfono',widget=forms.TextInput(attrs={'class':'form-control'}))
    cargo = CharFilter(field_name='cargo', lookup_expr='icontains', label='Cargo',widget=forms.TextInput(attrs={'class':'form-control'}))
    num_empleado = CharFilter(field_name='num_empleado', lookup_expr='icontains', label='Número de empleado',widget=forms.TextInput(attrs={'class':'form-control'}))
    colonia = CharFilter(field_name='colonia', lookup_expr='icontains', label='Colonia',widget=forms.TextInput(attrs={'class':'form-control'}))
    calle = CharFilter(field_name='calle', lookup_expr='icontains', label='Calle',widget=forms.TextInput(attrs={'class':'form-control'}))
    cp = CharFilter(field_name='cp', lookup_expr='icontains', label='C.P.',widget=forms.TextInput(attrs={'class':'form-control'}))
    zona = CharFilter(field_name='zona', lookup_expr='icontains', label='Zona',widget=forms.TextInput(attrs={'class':'form-control'}))
    disponibilidad = CharFilter(field_name='disponibilidad', lookup_expr='icontains', label='Disponibilidad',widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Empleados
        fields = '__all__'
        


