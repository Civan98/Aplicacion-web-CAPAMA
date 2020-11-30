from django.urls import path
from . import views

urlpatterns = [
    path('reportesUsuarios/',views.reportesUsuarios, name='reportes'),
    path('logout/',views.logout, name ='logout')
]
