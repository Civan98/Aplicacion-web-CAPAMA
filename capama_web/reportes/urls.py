from django.urls import path
from . import views

urlpatterns = [
    path('reportesUsuarios/',views.reportesUsuarios, name='reportes'),
    path('registrarUsuario/',views.registrarUsuario, name='registrarUsuario'),
    path('registrarEmpleado/',views.registrarEmpleado, name='registrarEmpleado'),
    path('mostrarUsuarios/',views.mostrarUsuarios, name='mostrarUsuarios'),
    path('modificarUsuarios/<int:idUsuario>',views.modificarUsuarios, name='modificarUsuarios'),
    path('mostrarEmpleados/',views.mostrarEmpleados, name='mostrarEmpleados'),
    path('modificarEmpleados/<int:idEmpleado>',views.modificarEmpleados, name='modificarEmpleados'),
]
