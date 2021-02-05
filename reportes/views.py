from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Empleados, Materiales, ReportesEmpleado, ReportesUsuario, Usuarios
from django.views.decorators.cache import cache_control
from django.template import Template, Context
from reportes.forms import FormLogin
from django.core.paginator import Paginator
from .filters import ReportesUsuarioFilter, ReportesEmpleadoFilter, MostrarUsuarioFilter,MostrarEmpleadoFilter
# importar el formulario del registro del usuario del archivo forms
from .forms import UsuarioForm, EmpleadoForm, DetallesReporteUsuarioForm
from capama_web.settings import base
from django.core.mail import send_mail
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
                        if validar.cargo == 'Pipas' or validar.cargo == 'Sobrestante' or validar.cargo == 'Alcantarillado':
                            errores.append('Lo sentimos, No tienes acceso!')
                        else:
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def buscarFolioEmpleado(request):
    if 'member_id' in request.session:
        if request.method == 'POST':
            folio = request.POST['folio']#obtener el folio escrito es el form

            reportesE = ReportesEmpleado.objects.all()#se obtienen todos los reportes de empleado

            for reportes in reportesE:#se realiza la busqueda
                #print(reportes.id_repoteusuario.folio_seguimiento)
                if reportes.id_repoteusuario.folio_seguimiento == folio:#si el folio a buscar es igual a algun folio de los reportes hechos  
                    return render(request, 'reportes/buscarFolioEmpleado.html', {'folio':folio,'reportesE':reportes})# retornamos esos datos
                else:
                    error='No hay reportes de empleados con ese folio'
                
            return render(request, 'reportes/buscarFolioEmpleado.html',{'folio':folio, 'error':error})

        else:
            return render(request, 'reportes/buscarFolioEmpleado.html')
    return HttpResponseRedirect('/login/')

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

        #para poder filtrar
        myFilter = ReportesUsuarioFilter(request.GET, queryset=reportesU)
        reportesU = myFilter.qs
        #para poder paginar
        paginator = Paginator(reportesU, 20)#el 20 es número de instancias que se muestran en la paginación
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number) #page_obj es el objeto de tabla que retorna ya filtrado y paginado

        # print(reportesU.)
        # cantidadReportesUsuario = reportesU.count()

        return render(request, 'reportes/reportesUsuarios.html', {'reportesU':page_obj, 'nomEmpleado': nomEmpleado, 'cargo':cargo, 'myFilter':myFilter })
    return HttpResponseRedirect('/login/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reportesEmpleados(request):
    #para validar si hay una sesión activa
    if 'member_id' in request.session:
        #datos del empleado en session
        empleado = Empleados.objects.get(id = request.session['member_id'])
        nomEmpleado = empleado.nombre+' '+empleado.apellidos
        cargo = empleado.cargo
        
        reportesE = ReportesEmpleado.objects.order_by('prioridad')
        # folios = reportesE.id_repoteusuario.folio_seguimiento
        #para poder filtrar
        myFilter = ReportesEmpleadoFilter(request.GET, queryset=reportesE)
        reportesE  = myFilter.qs
        #para poder paginar
        paginator = Paginator(reportesE, 20)#el 20 es número de instancias que se muestran en la paginación
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # print(reportesU.)
        # cantidadReportesUsuario = reportesU.count()

        return render(request, 'reportes/reportesEmpleados.html', {'reportesE':page_obj, 'nomEmpleado': nomEmpleado, 'cargo':cargo, 'myFilter':myFilter})
    return HttpResponseRedirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registrarUsuario(request):
    if 'member_id' in request.session:
        # datosObtenidos = UsuarioForm()

        # # si hay una petición de insertar datos:
        if request.method == 'POST':
            datosObtenidos = UsuarioForm(request.POST or None)
            pattern = '[0-9]{3,3}\-[0-9]{3,3}\-[0-9]{4,4}\-[0-9]'
            num_contratoObtenido = request.POST['num_contrato']
            emailObtenido = request.POST['email']
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
                if Usuarios.objects.filter(email = emailObtenido).exists():
                    error ='Error: su email ya ha sido registrado'
                    print(error)
                    # datosObtenidos = UsuarioForm()
                    context= {
                    'formularioUsuario':datosObtenidos,
                    'error':error
                    }
                    return render(request, 'registrarUsuario.html', context)

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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registrarEmpleado(request):
    
    if 'member_id' in request.session:
        if request.method =='POST':
            
            datosObtenidos = EmpleadoForm(request.POST)
            num_empleadoForm = request.POST['num_empleado']
            emailObtenido = request.POST['email']
            if Empleados.objects.filter(email = emailObtenido).exists():                
                error ='Error: su email ya ha sido registrado'
                context= {
                    'formularioEmpleado':datosObtenidos,
                    'error':error
                    }
                return render(request, 'registrarEmpleado.html', context)

            if Empleados.objects.filter(num_empleado = num_empleadoForm).exists():
                
                error ='Error: su número de usuario ya ha sido registrado'
                context= {
                    'formularioEmpleado':datosObtenidos,
                    'error':error
                    }
                return render(request, 'registrarEmpleado.html', context)


            if datosObtenidos.is_valid():
                print('prueba en valid')
                print(datosObtenidos)        
                datosObtenidos.save()
                datosObtenidos = EmpleadoForm()
        
        else:
            datosObtenidos = EmpleadoForm()
        context ={'formularioEmpleado':datosObtenidos}
        return render(request,'registrarEmpleado.html', context)
    return HttpResponseRedirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mostrarUsuarios(request):
    if 'member_id' in request.session:
        infoUsuarios = Usuarios.objects.all()

        #para poder filtrar
        myFilter = MostrarUsuarioFilter(request.GET, queryset=infoUsuarios)
        infoUsuarios  = myFilter.qs
        #para poder paginar
        paginator = Paginator(infoUsuarios, 20)#el 2 es número de instancias que se muestran en la paginación
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        print(infoUsuarios)    
        return render(request, 'mostrarUsuarios.html', {'usuarios':page_obj,'myFilter':myFilter})
    return HttpResponseRedirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
            emailObtenido = request.POST['email']
            if (conincidencia == []):
                error ='Inserte correctamente su número de contrato (incluya guiones)'
                print(error)
                context= {
                    'datosNuevos':formModificarUsuario,
                    'error':error
                }
                return render(request, 'modificarUsuario.html', context)
            if(datosUsuario.email != emailObtenido):
                if(Usuarios.objects.filter(email = emailObtenido).count() == 1):
                    error ='Error: su email: '+emailObtenido+' ya ha sido registrado.' 
                    print(formModificarUsuario)
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mostrarEmpleados(request):
    if 'member_id' in request.session:
        infoEmpleados = Empleados.objects.all()

         #para poder filtrar
        myFilter = MostrarEmpleadoFilter(request.GET, queryset=infoEmpleados)
        infoEmpleados  = myFilter.qs
        #para paginar
        paginator = Paginator(infoEmpleados, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        #print(infoEmpleados)
        return render(request,'mostrarEmpleados.html',{'empleados':page_obj,'myFilter':myFilter} )
    return HttpResponseRedirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
            'zona':datosEmpleado.zona,
            'cargo': datosEmpleado.cargo
        }
        formModificarEmpleado = EmpleadoForm(initial=datosExtraidos)
        if request.method == 'POST':          
            # obtener el número de empleado del formulario
            num_empleadoForm = request.POST['num_empleado']
            emailObtenido = request.POST['email']            
            if(datosEmpleado.num_empleado != num_empleadoForm):
                if(Empleados.objects.filter(num_empleado = num_empleadoForm).count() == 1):
                    error ='Error: su número de empleado: '+ num_empleadoForm +' ya ha sido registrado.' 
                    print(formModificarEmpleado)
                    context= {
                        'datosNuevos':formModificarEmpleado,
                        'error':error
                    }                           
                    return render(request, 'modificarEmpleado.html', context)
            if(datosEmpleado.email != emailObtenido):
                if(Empleados.objects.filter(email = emailObtenido).count() == 1):
                    error ='Error: su email ya ha sido registrado.' 
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
                datosEmpleado.disponibilidad = request.POST['disponibilidad']                
                datosEmpleado.save()
                formModificarEmpleado = EmpleadoForm(request.POST)
                # formModificarEmpleado = EmpleadoForm(initial=datosExtraidos)
                redirect('modificarUsuarios/'+str(idEmpleado))

        else:
            formModificarEmpleado = EmpleadoForm(initial=datosExtraidos)
        context= {'datosNuevos':formModificarEmpleado}
        return render(request,'modificarEmpleado.html',context)
    return HttpResponseRedirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def detallesReporteEmpleado(request, idReporteUsuario, idReporte):
    if 'member_id' in request.session:
        datosReporte = ReportesUsuario.objects.get(id = idReporteUsuario)
        datosMateriales = Materiales.objects.filter(id_reporte_empleado_id = idReporte)#id de la tabla de materiales
         
         #coordenadas
        coordenadas = datosReporte.geolocalizacion.split(sep=',')
        longitud = coordenadas[0]
        latitud = coordenadas[1]

        #para la foto, consultamos la foto del reporte del empleaddo
        reportesE = ReportesEmpleado.objects.get(id = idReporte)
        foto = reportesE.foto


        return render(request, 'reportes/detallesReporteEmpleado.html', {'datosReporteU': datosReporte, 'datosMateriales':datosMateriales, 'latitud':latitud, 'longitud':longitud, 'foto': foto})
    return HttpResponseRedirect('/login/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def detallesReporteUsuario(request, idReporte):
    if 'member_id' in request.session:
        
        # obtener los datos del reporte para después popular el formulario
        datosReporte = ReportesUsuario.objects.get(id = idReporte)
        print('id  usuario ' + datosReporte.id_usuario.email)
        # obtener el id del empleado antiguo, para cambiarlo a disponible si a este lo asignaron a una fuga
        if(datosReporte.id_empleado is not None):
            empleadoAnterior = datosReporte.id_empleado.id
            datosEmpleadoAnterior = datosReporte.id_empleado        
            estadoEmp = datosReporte.id_empleado.disponibilidad
            advertencia ="no"
            if(estadoEmp == 'Fuera de servicio'):
                advertencia = "Empleado fuera de servicio, asigne otro empleado"
        else:
            empleadoAnterior = ""
            datosEmpleadoAnterior = ""        
            estadoEmp = ""
            advertencia ="no"
        # print(datosReporte.id_empleado.id)
        cargoEmpleado = ""
        # determinar el tipo de reporte para poder mostrar los empleados asociados a ese problema
        if(datosReporte.tipo_servicio == 'Agua potable'):
            cargoEmpleado = 'Sobrestante'
        elif(datosReporte.tipo_servicio == 'Pipas'):
            cargoEmpleado = 'Pipas'
        else:
            cargoEmpleado = 'Alcantarillado'

        # popular el combo de empleado a asignar con sólo sobrestantes y dependiendo de la zona de la fuga
        sobrestante = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona)

        listaEmpleadosDisponibles = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona, disponibilidad ='Disponible')
        listaEmpleadosEnFuga = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona, disponibilidad ='En fuga')
        listaEmpleadosFuera = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona, disponibilidad ='Fuera de servicio')

        # for datosE in sobrestante:
            
        #     if(datosE.disponibilidad == 'Disponible'):
        #         listaEmpleadosDisponibles.append('Num empleado: '+datosE.num_empleado+'  '+datosE.nombre +' ' +datosE.apellidos )
        #     elif(datosE.disponibilidad == 'En fuga'):
        #         listaEmpleadosEnFuga.append('Num empleado: '+datosE.num_empleado +'  '+datosE.nombre +' ' +datosE.apellidos)    
        #     else:
        #         listaEmpleadosFuera.append('Num empleado: '+datosE.num_empleado +'  '+datosE.nombre +' ' +datosE.apellidos)  



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
            'geoLocalizacion':datosReporte.geolocalizacion,
            'colonia':datosReporte.colonia,
            'calle':datosReporte.calle,
            'cp':datosReporte.cp, 
            'num_interior':datosReporte.num_interior, 
            'num_exterior':datosReporte.num_exterior, 
            'descripcion':datosReporte.descripcion,
            'fecha':datosReporte.fecha,
            'id_usuario':datosReporte.id_usuario,        
            'estado': datosReporte.estado,
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
            
            # si no hay empleados, que no haga alguna acción
            if (len(listaEmpleadosEnFuga) ==0 and len(listaEmpleadosDisponibles)==0):
                
                return redirect('/reportesUsuarios')
            # sólo los reportes nuevos se pueden editar o en proceso. *puede que también los monitoreados.*
            if (datosReporte.estado == 'Nuevo' or datosReporte.estado == 'En proceso'):               
                #para que no se pueda modificar si ya hay asignado un sobrestante
                # para que se modifique o cambie de sobrestante por si el anterior no logró resolver
                # el get y false evita el multivaluekey error, es para saber si no han seleccionado nada
                if(request.POST.get('seleccionarSobrestante',False)):
                    enviarMail = True
                    # poner disponible al usuario antigio si este no está fuera de servicio
                    if(estadoEmp != 'Fuera de servicio' and datosReporte.id_empleado is not None):
                        empleadoReporteAnterior = Empleados.objects.get(id = empleadoAnterior)
                        empleadoReporteAnterior.disponibilidad = 'Disponible'
                        empleadoReporteAnterior.save()
                        # si ya había un empleado, no mandar correo, pues ya se le debió haber mandado uno
                        enviarMail = False

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
                    # obtener el id del empleado en crudo para que el combobox se quede con el empleado que está asignado, siguiendo la relación                                 
                    idEmpleadoRaw = datosReporte.id_empleado.id                                        
                    # rellenar nuevamente el formulario con los datos
                    datos['estado'] = datosReporte.estado
                    #inicializar el formulario con los datos del reporte seleccionado
                    reporteU = DetallesReporteUsuarioForm(initial=datos) 
                    # redirect('detallesReporteUsuario/'+str(idReporte))
                    #  rellenar los empleados disponibles
                    sobrestante = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona)
                    # extraer los empleados disponibles y los que etán en fuga, y asignarlos a una lista
                             
                    listaEmpleadosDisponibles = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona, disponibilidad ='Disponible')
                    listaEmpleadosEnFuga = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona, disponibilidad ='En fuga')
                    listaEmpleadosFuera = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona, disponibilidad ='Fuera de servicio') 
                    datosEmpleadoAnterior = datosReporte.id_empleado        
                    empleadoAnterior = datosReporte.id_empleado.id
                    advertencia ="no"

                    

                    # enviar correo para notificar al usuario el estado de su reporte ha cambiado a "En proceso"
                    subject = 'Estado de deporte con folio de seguimiento: '+ datosReporte.folio_seguimiento
                    message = 'Se le ha asignado un empleado a su reporte. Estado: En proceso.'
                    email_from = base.EMAIL_HOST_USER
                    # obtener el email del usuario
                    recipient_list = [datosReporte.id_usuario.email]
                    send_mail(subject, message, email_from, recipient_list)

                    # enviar correo para notificar al empleado que se le asignó un reporte
                    subject = 'Nuevo reporte asignado: '+ datosReporte.folio_seguimiento
                    message = 'Se le ha asignado un nuevo reporte, acceda a la app para más detalles.'
                    email_from = base.EMAIL_HOST_USER
                    # obtener el email del reporte
                    recipient_list = [datosReporte.id_empleado.email]
                    send_mail(subject, message, email_from, recipient_list)

                else:
                    # print('no entra if')
                    # para evitar cuando se le mueve directo a la bd se vuelve a comprobar los sobrestantes y el combo aparezca como no asignado
                    sobrestante = Empleados.objects.filter(cargo = cargoEmpleado, zona = datosReporte.zona)
            
            else:
                # rellenar el combo con el empleado asignado si noes nuevo el reporte                
                idEmpleadoRaw = datosReporte.id_empleado.id            
                # mostrar alguna advertencia de si el reporte ya se le asignó un sobrestante

        #para partir las coordenadas
        coordenadas = datosReporte.geolocalizacion.split(sep=',')
                          
        context = {
            'datosReporte': reporteU,   
            'sobrestante':sobrestante,
            'estado': datosReporte.estado,
            'idEmpleadoReporte': idEmpleadoRaw,
            'empleadosDisponibles': listaEmpleadosDisponibles,
            'empleadosEnFuga': listaEmpleadosEnFuga,            
            'empleadosFuera': listaEmpleadosFuera,
            'advertencia':advertencia,
            'empleadoActual': datosEmpleadoAnterior,
            'idEmpleadoActual': empleadoAnterior,
            'tipoServicio': datosReporte.tipo_servicio,
            'longitud': coordenadas[0],
            'latitud': coordenadas[1]
        }

        return render(request, 'reportes/detallesReporteUsuario.html', context)
    return HttpResponseRedirect('/login/')

# recuperar contraseña SóLO del empleado
def recuperarContrasena(request):
    mensaje = ""
    if request.method == "POST":
        num_empleado = request.POST['num_empleado']
        if(num_empleado == ""):
            mensaje = 'Ingrese su número de empleado.'
            return render(request, 'recuperarContrasena.html', {'mensaje':mensaje})

        if Empleados.objects.filter(num_empleado = num_empleado).exists():            
            datos_empleado = Empleados.objects.get(num_empleado = num_empleado)            
            subject = 'Recuperación de contraseña'
            message = 'Su contraseña es: '+datos_empleado.contrasena
            email_from = base.EMAIL_HOST_USER
            # obtener el email del usuario
            recipient_list = [datos_empleado.email]
            send_mail(subject, message, email_from, recipient_list)
            mensaje = 'Se ha enviado su contraseña a su correo electrónico.'            
        else:
            mensaje = 'No se encontró su número de empleado.'
    return render(request, 'recuperarContrasena.html', {'mensaje':mensaje})