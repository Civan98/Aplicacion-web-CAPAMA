from django.contrib import admin
from .models import Usuarios, Empleados, ReportesUsuario, ReportesEmpleado, Materiales
# Register your models here.


admin.site.register(Usuarios)
admin.site.register(Empleados)
admin.site.register(ReportesUsuario)
admin.site.register(ReportesEmpleado)
admin.site.register(Materiales)