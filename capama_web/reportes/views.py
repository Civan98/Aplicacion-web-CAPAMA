from django.shortcuts import render, redirect
from .models import Empleados, Materiales, ReportesEmpleado, ReportesUsuario, Usuarios
# importar el formulario del registro del usuario del archivo forms
from .forms import UsuarioForm, EmpleadoForm
import re
# Create your views here.

def reportesUsuarios(request):
    reportesU = ReportesUsuario.objects.order_by('prioridad')
    # print(reportesU.)
    # cantidadReportesUsuario = reportesU.count()

    return render(request, 'reportesUsuarios.html', {'reportesU':reportesU})

def registrarUsuario(request):
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

def registrarEmpleado(request):
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

def mostrarUsuarios(request):
    infoUsuarios = Usuarios.objects.all()
    print(infoUsuarios)
    
    return render(request, 'mostrarUsuarios.html', {'usuarios':infoUsuarios})

def modificarUsuarios(request, idUsuario):
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

def mostrarEmpleados(request):
    infoEmpleados = Empleados.objects.all()
    print(infoEmpleados)
    return render(request,'mostrarEmpleados.html',{'empleados':infoEmpleados} )

def modificarEmpleados(request, idEmpleado):
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
        # print(num_empleadoForm)
        # if( Empleados.objects.filter(id = idEmpleado,num_empleado = num_empleadoForm).count() == 1):   
        #     error ='Error: su número de empleado ya ha sido registrado'
        #     print(formModificarEmpleado)
        #     context= {
        #         'datosNuevos':formModificarEmpleado,
        #         'error':error
        #     }                            
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
        
