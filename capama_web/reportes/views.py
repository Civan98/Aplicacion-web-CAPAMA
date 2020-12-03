from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Empleados, Materiales, ReportesEmpleado, ReportesUsuario, Usuarios
from django.views.decorators.cache import cache_control
from django.template import Template, Context
from reportes.forms import FormLogin
from django.core.paginator import Paginator
# importar el formulario del registro del usuario del archivo forms
from .forms import UsuarioForm, EmpleadoForm, DetallesReporteUsuarioForm
import re
# Create your views here.

    
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



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reportesUsuarios(request):
    #para validar si hay una sesión activa
    if 'member_id' in request.session:
        #datos del empleado en session
        empleado = Empleados.objects.get(id = request.session['member_id'])
        nomEmpleado = empleado.nombre+' '+empleado.apellidos
        cargo = empleado.cargo

        reportesU = ReportesUsuario.objects.order_by('prioridad')
        paginator = Paginator(reportesU, 2)#el 2 es número de instancias que se muestran en la paginación
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # print(reportesU.)
        # cantidadReportesUsuario = reportesU.count()

        return render(request, 'reportes/reportesUsuarios.html', {'reportesU':page_obj, 'nomEmpleado': nomEmpleado, 'cargo':cargo})
    return HttpResponseRedirect('/login/')

def registrarUsuario(request):
    if 'member_id' in request.session:
        # datosObtenidos = UsuarioForm()

        # # si hay una petición de insertar datos:
        if request.method == 'POST':
            datosObtenidos = UsuarioForm(request.POST or None)
            pattern = '[0-9]{3,3}\-[0-9]{3,3}\-[0-9]{4,4}\-[0-9]'
            num_contratoObtenido = request.POST['num_contrato']
            conincidencia = re.findall(pattern,num_contratoObtenido)
            if (conincidencia == []):
                error ='Inserte correctamente su número de contrato (incluya guiones)'
                print(error)
                # datosObtenidos = UsuarioForm()
                context= {
                    'formularioUsuario':datosObtenidos, 
                    'error':error
                }
                return render(request, 'registrarUsuario.html', context)
            else:
                if Usuarios.objects.filter(num_contrato = num_contratoObtenido).exists():
                    error ='Error: su número de contrato ya ha sido registrado'
                    print(error)
                    # datosObtenidos = UsuarioForm()
                    context= {
                    'formularioUsuario':datosObtenidos,
                    'error':error
                    }
                    return render(request, 'registrarUsuario.html', context)

            if datosObtenidos.is_valid():        
                print(datosObtenidos)
                datosObtenidos.save()
                datosObtenidos = UsuarioForm()
        else:
            datosObtenidos = UsuarioForm()
            
        context = {'formularioUsuario': datosObtenidos}
        return render(request, 'registrarUsuario.html', context)
    return HttpResponseRedirect('/login/')

def registrarEmpleado(request):
    if 'member_id' in request.session:
        if request.method =='POST':
            datosObtenidos = EmpleadoForm(request.POST)
            num_empleadoForm = request.POST['num_empleado']
            if Empleados.objects.filter(num_empleado = num_empleadoForm).exists():
                error ='Error: su número de usuario ya ha sido registrado'
                context= {
                    'formularioUsuario':datosObtenidos,
                    'error':error
                    }
                return render(request, 'registrarUsuario.html', context)


            if datosObtenidos.is_valid():
                print(datosObtenidos)        
                datosObtenidos.save()
                datosObtenidos = EmpleadoForm()
        
        else:
            datosObtenidos = EmpleadoForm()
        context ={'formularioEmpleado':datosObtenidos}
        return render(request,'registrarEmpleado.html', context)
    return HttpResponseRedirect('/login/')

def mostrarUsuarios(request):
    if 'member_id' in request.session:
        infoUsuarios = Usuarios.objects.all()
        paginator = Paginator(infoUsuarios, 2)#el 2 es número de instancias que se muestran en la paginación
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(infoUsuarios)    
        return render(request, 'mostrarUsuarios.html', {'usuarios':page_obj})
    return HttpResponseRedirect('/login/')

def modificarUsuarios(request, idUsuario):
    if 'member_id' in request.session:
        datosUsuario = Usuarios.objects.get(id = idUsuario)

        datosExtraidos = {
            'nombre': datosUsuario.nombre,
            'apellidos': datosUsuario.apellidos,
            'telefono': datosUsuario.telefono,
            'email': datosUsuario.email,
            'num_contrato': datosUsuario.num_contrato,
            'colonia': datosUsuario.colonia,
            'calle': datosUsuario.calle,
            'cp': datosUsuario.cp,
            'contrasena': datosUsuario.contrasena,
            'temp_contrasena':datosUsuario.contrasena,
        }

        formModificarUsuario = UsuarioForm(initial=datosExtraidos)
        if request.method == 'POST':
            # print(request.POST['num_contrato'])
            pattern = '[0-9]{3,3}\-[0-9]{3,3}\-[0-9]{4,4}\-[0-9]'
            num_contratoObtenido = request.POST['num_contrato']
            conincidencia = re.findall(pattern, num_contratoObtenido)
            if (conincidencia == []):
                error ='Inserte correctamente su número de contrato (incluya guiones)'
                print(error)
                context= {
                    'datosNuevos':formModificarUsuario,
                    'error':error
                }
                return render(request, 'modificarUsuario.html', context)
            # si los numeros de contrato son diferentes
            if(datosUsuario.num_contrato != num_contratoObtenido):
                # comprobar si existe el nuevo número de contrato
                # print(Usuarios.objects.filter(num_contrato = num_contratoObtenido).count())
                if(Usuarios.objects.filter(num_contrato = num_contratoObtenido).count() == 1):
                    error ='Error: su número de contrato: '+ num_contratoObtenido +' ya ha sido registrado.' 
                    print(formModificarUsuario)
                    context= {
                        'datosNuevos':formModificarUsuario,
                        'error':error
                    }
                    return render(request, 'modificarUsuario.html', context)

        # if request.method == 'POST':
            formModificarUsuario = UsuarioForm(request.POST)


            if formModificarUsuario.is_valid():
                datosUsuario.nombre = request.POST['nombre']
                datosUsuario.apellidos = request.POST['apellidos']
                datosUsuario.telefono = request.POST['telefono']
                datosUsuario.email = request.POST['email']
                datosUsuario.num_contrato = request.POST['num_contrato']
                datosUsuario.colonia = request.POST['colonia']
                datosUsuario.calle = request.POST['calle']
                datosUsuario.cp = request.POST['cp']
                datosUsuario.contrasena = request.POST['contrasena']
                datosUsuario.save()
                formModificarUsuario = UsuarioForm(request.POST)
                redirect('modificarUsuarios/'+str(idUsuario))
        else:
            formModificarUsuario = UsuarioForm(initial=datosExtraidos)

        context= {
            'datosNuevos':formModificarUsuario,
            # 'error':error
        }
        return render(request, 'modificarUsuario.html', context)
    return HttpResponseRedirect('/login/')

def mostrarEmpleados(request):
    if 'member_id' in request.session:
        infoEmpleados = Empleados.objects.all()
        paginator = Paginator(infoEmpleados, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        #print(infoEmpleados)
        return render(request,'mostrarEmpleados.html',{'empleados':page_obj} )
    return HttpResponseRedirect('/login/')

def modificarEmpleados(request, idEmpleado):
    if 'member_id' in request.session:
        datosEmpleado = Empleados.objects.get(id = idEmpleado)

        datosExtraidos = {
            'nombre': datosEmpleado.nombre,
            'apellidos': datosEmpleado.apellidos,
            'telefono': datosEmpleado.telefono,
            'email': datosEmpleado.email,
            'num_empleado': datosEmpleado.num_empleado,
            'colonia': datosEmpleado.colonia,
            'calle': datosEmpleado.calle,
            'cp': datosEmpleado.cp,
            'contrasena': datosEmpleado.contrasena,
            'temp_contrasena':datosEmpleado.contrasena,
            'disponibilidad':datosEmpleado.disponibilidad,
            'zona':datosEmpleado.zona
        }
        formModificarEmpleado = EmpleadoForm(initial=datosExtraidos)
        if request.method == 'POST':          
            # obtener el número de empleado del formulario
            num_empleadoForm = request.POST['num_empleado']
            if(datosEmpleado.num_empleado != num_empleadoForm):
                if(Empleados.objects.filter(num_empleado = num_empleadoForm).count() == 1):
                    error ='Error: su número de empleado: '+ num_empleadoForm +' ya ha sido registrado.' 
                    print(formModificarEmpleado)
                    context= {
                        'datosNuevos':formModificarEmpleado,
                        'error':error
                    }                           
                return render(request, 'modificarEmpleado.html', context)

            formModificarEmpleado = EmpleadoForm(request.POST)  
            if formModificarEmpleado.is_valid():
                datosEmpleado.nombre = request.POST['nombre']
                datosEmpleado.apellidos = request.POST['apellidos']
                datosEmpleado.telefono = request.POST['telefono']
                datosEmpleado.email = request.POST['email']
                datosEmpleado.num_empleado = request.POST['num_empleado']
                datosEmpleado.colonia = request.POST['colonia']
                datosEmpleado.calle = request.POST['calle']
                datosEmpleado.cp = request.POST['cp']
                datosEmpleado.contrasena = request.POST['contrasena']
                datosEmpleado.save()
                formModificarEmpleado = EmpleadoForm(request.POST)
                # formModificarEmpleado = EmpleadoForm(initial=datosExtraidos)
                redirect('modificarUsuarios/'+str(idEmpleado))

        else:
            formModificarEmpleado = EmpleadoForm(initial=datosExtraidos)
        context= {'datosNuevos':formModificarEmpleado}
        return render(request,'modificarEmpleado.html',context)
    return HttpResponseRedirect('/login/')

def detallesReporteUsuario(request, idReporte):
    if 'member_id' in request.session:
        # obtener los datos del reporte para después popular el formulario
        datosReporte = ReportesUsuario.objects.get(id = idReporte)
        # popular el combo de empleado a asignar con sólo sobrestantes y dependiendo de la zona de la fuga
        sobrestante = Empleados.objects.filter(cargo = 'Sobrestante', zona = datosReporte.zona)

        # extraer los empleados disponibles y los que etán en fuga, y asignarlos a una lista
        listaEmpleadosDisponibles = []
        listaEmpleadosEnFuga = []
        for datosE in sobrestante:
            if(datosE.disponibilidad == 'Disponible'):
                listaEmpleadosDisponibles.append(datosE.nombre +' ' +datosE.apellidos +'| Num empleado: '+datosE.num_empleado)
            else:
                listaEmpleadosEnFuga.append(datosE.nombre +' ' +datosE.apellidos +'| Num empleado: '+datosE.num_empleado)
        # inicializar el id del empleado en crudo
        idEmpleadoRaw=[]
        idEmpleadoRaw.append('-1')

    # datos para inicializar el formulario, se obtienen del reporte que se visualiza
        datos = {
            'zona':datosReporte.zona,
            'tipo_anomalia':datosReporte.tipo_anomalia,
            'folio_seguimiento':datosReporte.folio_seguimiento,
            'foto':datosReporte.foto,
            'prioridad':datosReporte.prioridad,
            'geoLocalizacion':datosReporte.geoLocalizacion,
            'colonia':datosReporte.colonia,
            'calle':datosReporte.calle,
            'cp':datosReporte.cp, 
            'num_interior':datosReporte.num_interior, 
            'num_exterior':datosReporte.num_exterior, 
            'descripcion':datosReporte.descripcion,
            'fecha':datosReporte.fecha,
            'id_usuario':datosReporte.id_usuario,        
            'estado': datosReporte.estado
        }
        #inicializar el formulario con los datos del reporte seleccionado
        reporteU = DetallesReporteUsuarioForm(initial=datos) 

    # -------------------NOTA---------------------
    # posible error con bajas probabilidades de que suceda
    # si asignamos un empleado a la fuga, este se guarda correctamente
    #pero si modificamos de forma directa en la bd de nuevo el estado a Nuevo y el empleado a " " (sin asignar)
    # luego volvemos a la página, y recargamos, con los cambios en la bd antes dicho, este no respetará, y se guardará el empleado que está seleccionado
    # esto se soluciona si dirigimos al usuario (después de asignar al reporte al empleado ) a alguna página que diga: "se ha asignado correctamente el empleado"

        # if datosReporte.id_empleado is None:
        #     print('sin empleado asignado')
        # else:
        #     print('con empleado asignado')

        if request.method =='POST':
            # sólo los reportes nuevos se pueden editar
            if datosReporte.estado == 'Nuevo':   
                # print('datos '+datosReporte.id_empleado)         
                if(request.POST['seleccionarSobrestante']!="" and datosReporte.id_empleado is None):
                    # modificar la disponibilidad del empleado a 'En fuga', para ello debemos obtener su instancia
                    idEmpleadoAsignado = request.POST['seleccionarSobrestante']
                    empleadoAsignado = Empleados.objects.get(id = idEmpleadoAsignado)
                    empleadoAsignado.disponibilidad = 'En fuga'
                    empleadoAsignado.save()
                    # Modificamos el reporte para asignar al sobrestante seleccionado y su estado
                    # print(empleadoAsignado)
                    datosReporte.estado = 'En proceso' 
                    datosReporte.id_empleado = empleadoAsignado
                    datosReporte.save()
                    # obtener el id del empleado en crudo para que el combobox se quede con el empleado que está asignado
                    idEmpleadoCombo = str(datosReporte.id_empleado)
                    idEmpleadoRaw = idEmpleadoCombo.split('.')
                    # rellenar nuevamente el formulario con los datos
                    datos['estado'] = datosReporte.estado
                    #inicializar el formulario con los datos del reporte seleccionado
                    reporteU = DetallesReporteUsuarioForm(initial=datos) 
                    redirect('detallesReporteUsuario/'+str(idReporte))
                    print('datos in'+datos['estado'])

                else:
                    print('no entra if')
                    # para evitar cuando se le mueve directo a la bd se vuelve a comprobar los sobrestantes y el combo aparezca como no asignado
                    sobrestante = Empleados.objects.filter(cargo = 'Sobrestante', zona = datosReporte.zona)
            
            else:
                # rellenar el combo con el empleado asignado si noes nuevo el reporte
                idEmpleadoCombo = str(datosReporte.id_empleado)
                idEmpleadoRaw = idEmpleadoCombo.split('.')            
                # mostrar alguna advertencia de si el reporte ya se le asignó un sobrestante
                
        print('prueba '+ idEmpleadoRaw[0])
        context = {
            'datosReporte': reporteU,   
            'sobrestante':sobrestante,
            'estado': datosReporte.estado,
            'idEmpleadoReporte': int(idEmpleadoRaw[0]),
            'empleadosDisponibles': listaEmpleadosDisponibles,
            'empleadosEnFuga': listaEmpleadosEnFuga
        }

        return render(request, 'reportes/detallesReporteUsuario.html', context)
    return HttpResponseRedirect('/login/')




    # manipular el id de los empleados (debido que el método __str__ interfiere con su retorno), obteniendo sólo el id
    # comprobar si hay datos en la bd del id_empleado asignado al reporte
    # existeID = False
    # if(datosReporte.id_empleado is None):
    #     print('no hay dato')
    # else:
    #     existeID = True
    #     idEmpleado = str(datosReporte.id_empleado)
    #     idEmpleadoRaw = idEmpleado.split('.')




    # popular el formulario con datos iniciales obtenidos
    # ----------------------------------------v1
    # reporteU = DetallesReporteUsuarioForm(initial=datos)

    # # cuando se le asigne un sobreestante, se cambiará el estado del reporte a 'en proceso
    # # cuando el sobreestante reciba, le de aceptar al reporte, se cambiará el estado a 'Monitoreado'
    # # cuando el sobreestante termine de reparar la fuga se cambiará el estado a 'Atendido'
    # if request.method == 'POST':        
    #     # evitar que si ya se atendió un reporte, se pueda seguir modificando y por ende cambie de estado
    #     if(datosReporte.estado == 'Nuevo'):       
    #         # print('prueba ' + request.POST['seleccionarSobrestante'])               
    #         if request.POST['seleccionarSobrestante'] == '':
    #             # print(request.POST['seleccionarSobrestante'])
    #             # idEmpleadoRaw[0] = "-1"
    #             context={
    #                 'datosReporte':reporteU,
    #                 'sobrestante': sobrestante,
    #                 'estado': datosReporte.estado,                    
    #                 'empleadosDisponibles': listaEmpleadosDisponibles,
    #                 'empleadosEnFuga': listaEmpleadosEnFuga
    #             }
    #             return render(request, 'reportes/detallesReporteUsuario.html', context)
    #         else:
    #             if not existeID:
    #                 # actualizar la disponibilidad del empleado, creando primero su instancia y después sobreescribir sus datos
    #                 # extraer el id de forma cruda, porque no logro obtener sólo el id, el método __str__ de models interfiere
    #                 idEmpleadoAsignado = request.POST['seleccionarSobrestante']
    #                 instanciaEmpleado = Empleados.objects.get(id=idEmpleadoAsignado)
    #                 instanciaEmpleado.disponibilidad = 'En fuga'
    #                 instanciaEmpleado.save()
    #                 datosReporte.estado = 'En proceso'
    #                 idEmpleado = int(request.POST['seleccionarSobrestante'])
    #                 # para retornar el idEmpleado se necesita una instancia (varios objetos)
    #                 instancia = Empleados.objects.get(id=idEmpleado)    
    #                 datosReporte.id_empleado = instancia
    #                 datosReporte.save()  
    #                 context={
    #                     'datosReporte':reporteU,
    #                     'sobrestante': sobrestante,
    #                     'estado': datosReporte.estado,
    #                     'idEmpleadoReporte': idEmpleadoAsignado,
    #                     'empleadosDisponibles': listaEmpleadosDisponibles,
    #                     'empleadosEnFuga': listaEmpleadosEnFuga
    #                 }
    #             else:
    #                 context={
    #                 'datosReporte':reporteU,
    #                 'sobrestante': sobrestante,
    #                 'estado': datosReporte.estado,                    
    #                 'empleadosDisponibles': listaEmpleadosDisponibles,
    #                 'empleadosEnFuga': listaEmpleadosEnFuga
    #                 }

    # else:
    #     context={
    #         'datosReporte':reporteU,
    #         'sobrestante': sobrestante,
    #         'estado': datosReporte.estado,                    
    #         'empleadosDisponibles': listaEmpleadosDisponibles,
    #         'empleadosEnFuga': listaEmpleadosEnFuga
    #     }
        

    # return render(request, 'reportes/detallesReporteUsuario.html', context)
# ----------------------------------v1 fin
# def reportesEmpleado(request):
#     reportesU = ReportesUsuario.objects.all()
#     return render(request, 'reportesUsuarios.html', {'reportesUsuario':reportesU})