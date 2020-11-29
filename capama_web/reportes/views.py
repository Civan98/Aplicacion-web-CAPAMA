from django.shortcuts import render, HttpResponse
from .models import Empleados, Materiales, ReportesEmpleado, ReportesUsuario, Usuarios
# Create your views here.

def reportesUsuarios(request):
    reportesU = ReportesUsuario.objects.order_by('prioridad')
    # print(reportesU.)
    # cantidadReportesUsuario = reportesU.count()

    return render(request, 'reportesUsuarios.html', {'reportesU':reportesU})