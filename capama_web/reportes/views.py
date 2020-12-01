from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Empleados, Materiales, ReportesEmpleado, ReportesUsuario, Usuarios
from django.views.decorators.cache import cache_control
# Create your views here.

#para desactivar la cache y evitar que el navegador guarde la pantalla anterior y la recarge como nueva
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reportesUsuarios(request):
    #para validar si hay una sesión activa
    if 'member_id' in request.session:
        reportesU = ReportesUsuario.objects.order_by('prioridad')
        # print(reportesU.)
        # cantidadReportesUsuario = reportesU.count()

        return render(request, 'reportesUsuarios.html', {'reportesU':reportesU})

    return HttpResponseRedirect('/login/')
    
#para desactivar la cache y evitar que el navegador guarde la pantalla anterior y la recarge como nueva
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    #lista para almacenar posibles errores
    errores = [] #lista para almacenar los errores que se mostraran 
     #si el usuario intenta ir al login, se valida si la sesión está activa, si es así, se le manda a la página principal  
    if 'member_id' in request.session:  
        return HttpResponseRedirect('/reportesUsuarios/')
        #validaciones de que haya datos en el formulario
    if request.method == 'POST':
        if not request.POST.get('usuario',''):
            errores.append('Introduce tu nombre de usuario')
        if not request.POST.get('password',''):
            errores.append('Introduce tu contraseña')
        if not errores:
            try:
                #obtenemos los datos del usuario desde la BD
                validar = Empleados.objects.get(email = request.POST['usuario'])
            except Empleados.DoesNotExist:
                errores.append('¡El de empleado no existe!')
            else:
                if validar.contrasena == request.POST['password']:
                    request.session['member_id'] = validar.id
                    #request.session es un diccionario de datos, en el cual llenamos con información del usuario
                    return HttpResponseRedirect('/reportesUsuarios/')
                errores.append('La contraseña no es correcta')

    return render(request,'login.html',{'errores':errores})

def logout(request):
    try:
         del request.session['member_id']
    except KeyError:
             pass
    return HttpResponseRedirect('/login/')