from django.urls import path
from . import views

urlpatterns = [
    path('reportesUsuarios/',views.reportesUsuarios, name='reportes'),
    path('logout/',views.logout, name ='logout'),
    path('login/',views.login, name ='login'),
    path('reportesUsuarios/',views.reportesUsuarios, name='reportesUsuarios'),
    path('registrarUsuario/',views.registrarUsuario, name='registrarUsuario'),
    path('registrarEmpleado/',views.registrarEmpleado, name='registrarEmpleado'),
    path('mostrarUsuarios/',views.mostrarUsuarios, name='mostrarUsuarios'),
    path('modificarUsuarios/<int:idUsuario>',views.modificarUsuarios, name='modificarUsuarios'),
    path('mostrarEmpleados/',views.mostrarEmpleados, name='mostrarEmpleados'),
    path('modificarEmpleados/<int:idEmpleado>',views.modificarEmpleados, name='modificarEmpleados'),
    path('detallesReporteUsuario/<int:idReporte>',views.detallesReporteUsuario, name='detallesReporteUsuario'),
    # path('reportesUsuario/', views.reportesUsuario, name='modificarEmpleados'),
]
