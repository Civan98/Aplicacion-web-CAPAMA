from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .models import Empleados, Materiales, ReportesEmpleado, ReportesUsuario, Usuarios
from django.views.decorators.cache import cache_control
from django.template import Template, Context
from reportes.forms import FormLogin
# Create your views here.

#para desactivar la cache y evitar que el navegador guarde la pantalla anterior y la recarge como nueva
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reportesUsuarios(request):
    #para validar si hay una sesión activa
    if 'member_id' in request.session:
        #datos del empleado en session
        empleado = Empleados.objects.get(id = request.session['member_id'])
        nomEmpleado = empleado.nombre+' '+empleado.apellidos
        cargo = empleado.cargo

        reportesU = ReportesUsuario.objects.order_by('prioridad')
        # print(reportesU.)
        # cantidadReportesUsuario = reportesU.count()

        return render(request, 'reportesUsuarios.html', {'reportesU':reportesU, 'nomEmpleado': nomEmpleado, 'cargo':cargo})

    return HttpResponseRedirect('/login/')
    
#para desactivar la cache y evitar que el navegador guarde la pantalla anterior y la recarge como nueva
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    #lista para almacenar posibles errores
    errores = []
     #se valida si la sesión está activa 
    if 'member_id' in request.session:  
        return HttpResponseRedirect('/reportesUsuarios/')
    else:
        if request.method == 'POST':
            miformulario = FormLogin(request.POST)

            if miformulario.is_valid():#validaciones de que sea correcto
                infoForm = miformulario.cleaned_data
                    
                try:
                    validar = Empleados.objects.get(email = infoForm['email'])#obtenemos los datos del usuario desde la BD
                    if  validar.contrasena == infoForm['password']:
                            request.session['member_id'] = validar.id
                            #request.session es un diccionario de datos, en el cual llenamos con información del usuario
                            return HttpResponseRedirect('/reportesUsuarios/')
                    else:
                        errores.append('¡Contraseña Incorrecta!')
                except Empleados.DoesNotExist:
                    errores.append('¡El Correo Electronico no existe!')

            Context ={'errores':errores, 'form': miformulario}
 
        else: 
            miformulario=FormLogin()
            Context ={'errores':errores, 'form': miformulario}

    return render(request,'login.html',Context)

def logout(request):
    try:
         del request.session['member_id']
    except KeyError:
             pass
    return HttpResponseRedirect('/login/')