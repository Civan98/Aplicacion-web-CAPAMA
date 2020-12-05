import django_filters
from django import forms
from django_filters import DateFilter, CharFilter

from .models import *

#para mostrar el calendar en vez de un field simple
class DateInput(forms.DateInput):
    input_type = 'fecha'

class ReportesUsuarioFilter(django_filters.FilterSet):
    #los dos campos siguiente se utilizan para poder filtrar por ragos de fecha
    start_date = DateFilter(field_name="fecha", lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name="fecha", lookup_expr='lte',label='Fecha menor que', widget=DateInput(attrs={'type': 'date'}))
    
    # se agrega el charfilter para que filtre sin escribir todo el campo, resultados relacionados
    folio_seguimiento = CharFilter(field_name='folio_seguimiento', lookup_expr='icontains', label='Folio seguimiento')
    tipo_anomalia = CharFilter(field_name='tipo_anomalia', lookup_expr='icontains', label='Tipo anomalía')
    descripcion =  CharFilter(field_name='descripcion', lookup_expr='icontains', label='Descripción')
    colonia =  CharFilter(field_name='colonia', lookup_expr='icontains', label='Colonia')
    calle =  CharFilter(field_name='calle', lookup_expr='icontains', label='Calle')
    cp =  CharFilter(field_name='cp', lookup_expr='icontains', label='C.P.')
    num_interior =  CharFilter(field_name='num_interior', lookup_expr='icontains', label='Número interior')
    num_exterior =  CharFilter(field_name='num_exterior', lookup_expr='icontains', label='Número exterior')


    class Meta:
        model = ReportesUsuario
        fields = '__all__'
        exclude = ['fecha', 'geolocalizacion', 'foto']

class DateInput2(forms.DateInput):
    input_type = 'fecha_inicio'
    input_type = 'fecha_fin'

class ReportesEmpleadoFilter(django_filters.FilterSet):
    
    
    start_date = DateFilter(field_name='fecha_inicio',lookup_expr='gte',  widget=DateInput2(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='fecha_inicio',lookup_expr='lte', label='Fecha inicio menor que',  widget=DateInput2(attrs={'type': 'date'}))
    
    start_date2 = DateFilter(field_name='fecha_fin',lookup_expr='gte',  widget=DateInput2(attrs={'type': 'date'}))
    end_date2 =  DateFilter(field_name='fecha_fin',lookup_expr='lte', label='Fecha fin menor que', widget=DateInput2(attrs={'type': 'date'}))
    
    
    # se agrega el charfilter para que filtre sin escribir todo el campo, resultados relacionados
    descripcion =  CharFilter(field_name='descripcion', lookup_expr='icontains', label='Descripción')

    class Meta:
        model = ReportesEmpleado
        fields = '__all__'
        exclude = ['fecha_inicio', 'fecha_fin','foto']


