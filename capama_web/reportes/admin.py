from django.contrib import admin
from .models import Usuarios, Empleados, ReportesUsuario, ReportesEmpleado, Materiales
# Register your models here.

# mostrar los datos de los registros

class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellidos','email','contrasena', 'num_contrato', 'telefono')
    # para la barra de búsqueda, se puede usar el núm_contrato, telégono, email
    search_fields = ('num_contrato','telefono','email')

admin.site.register(Usuarios, UsuariosAdmin)

class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellidos','email','contrasena', 'telefono','cargo', 'num_empleado')
    list_filter = ( 'cargo', 'email')
    search_fields = ('num_empleado','telefono','email')

admin.site.register(Empleados, EmpleadosAdmin)

class ReportesUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','zona', 'folio_seguimiento','prioridad','fecha', 'cp', 'colonia', 'estado', 'id_usuario')
    list_filter = ('prioridad', 'fecha', 'estado', 'id_usuario', 'zona', 'tipo_anomalia','tipo_servicio')
    search_fields = ('folio_seguimiento','colonia')
admin.site.register(ReportesUsuario, ReportesUsuarioAdmin)

class ReportesEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id','zona','prioridad','fecha_inicio', 'estado', 'id_empleado')
    list_filter = ('prioridad', 'estado', 'id_empleado', 'zona','tipo_anomalia','tipo_servicio')
    search_fields = ('id_empleado__num_empleado', 'zona')

admin.site.register(ReportesEmpleado, ReportesEmpleadoAdmin)

class MaterialesAdmin(admin.ModelAdmin):
    list_display = ('id_reporte_empleado','material', 'cantidad')
    list_filter = ('id_reporte_empleado','material')
    search_fields = ('id_reporte_empleado__folio_seguimiento','material')

admin.site.register(Materiales, MaterialesAdmin)