from django import forms
from .models import Usuarios, Empleados, ReportesUsuario
import re

class UsuarioForm(forms.ModelForm):
    # campo de contraseña temporal para validaciones
    contrasena = forms.CharField(label='Contraseña', max_length=45, min_length=4, required=True)
    temp_contrasena = forms.CharField(label='Repita su contraseña', max_length=45, min_length=4, required=True)


    class Meta:
        
        model = Usuarios
        # especificar el orden de aparición de los inputs
        fields = ['nombre','apellidos','telefono', 'email', 'num_contrato','colonia','calle','cp','contrasena']
        # para modificar los atributos del html
        widgets ={
            'nombre': forms.TextInput(attrs={'placeholder':'Nombre completo'}),
            'apellidos': forms.TextInput(attrs={'placeholder':'Apellidos'}),
            'telefono': forms.NumberInput(attrs={'placeholder':'ej. 7441010122'}),
            'email': forms.EmailInput(attrs={'placeholder':'example@example.com'}),
            'cp': forms.NumberInput(attrs={'placeholder':'ej. 39920','minlenght':5, 'maxlenght':5}),
            'num_contrato': forms.TextInput(attrs={'placeholder':'ej. 111-222-3333-1'})
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if(len(telefono) == 10):
            return telefono
        else:            
            raise forms.ValidationError('Ingrese un teléfono válido')

    def clean_cp(self):
        cp = str(self.cleaned_data.get('cp'))
        if(len(cp)==5):            
            return cp
        else:
           raise forms.ValidationError('Ingrese un código postal válido')
    # def clean_num_contrato(self):
    #     pattern = '[0-9]{3,3}\-[0-9]{3,3}\-[0-9]{4,4}\-[0-9]'
    #     num_contratoObtenido = self.cleaned_data.get('num_contrato')
    #     conincidencia = re.findall(pattern,num_contratoObtenido)
    #     if (conincidencia == []):
    #         raise forms.ValidationError('Inserte correctamente su número de contrato (incluya guiones)')
    #     else:
    #         if Usuarios.objects.filter(num_contrato = num_contratoObtenido).exists():
    #             raise forms.ValidationError('Error: Su número de contrato ya ha sido registrado')
    #         else:
    #             return num_contratoObtenido

    def clean(self):
        contrasena = self.cleaned_data.get('contrasena')
        temp_contrasena = self.cleaned_data.get('temp_contrasena')

        if(contrasena == temp_contrasena):
            if(len(contrasena) < 4):                
                raise forms.ValidationError('La contraseña debe ser mayor a 4 caracteres')
            # da error si retorno la contraseña 
        else:
            # print(contrasena)
            # print(temp_contrasena)
            raise forms.ValidationError('Las contraseñas no coinciden')
    
        
class EmpleadoForm(forms.ModelForm):
    CARGOS =(
        ('Administrador', 'Administrador'),
        ('Sobrestante', 'Sobrestante'),
    )

    temp_contrasena = forms.CharField(label='Repita su contraseña', max_length=45, required=True)
    cargo = forms.ChoiceField(required=True, choices=CARGOS)
   
    # disponibilidad = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly', 'hidden':'true'}))
    class Meta:
        model = Empleados
        fields = ['nombre','apellidos','telefono', 'email', 'cargo', 'num_empleado','zona','colonia','calle','cp','contrasena']
        widgets ={
            'nombre': forms.TextInput(attrs={'placeholder':'Nombre completo'}),
            'apellidos': forms.TextInput(attrs={'placeholder':'Apellidos'}),
            'telefono': forms.NumberInput(attrs={'placeholder':'ej. 7441010122'}),
            'email': forms.EmailInput(attrs={'placeholder':'example@example.com'}),
            'cp': forms.NumberInput(attrs={'placeholder':'ej. 39920'}),
            'num_empleado': forms.TextInput(attrs={'placeholder':'ej. por modificar'})
        }
    




    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if(len(telefono) == 10):
            return telefono
        else:            
            raise forms.ValidationError('Ingrese un teléfono válido')


    def clean_cp(self):
        cp = str(self.cleaned_data.get('cp'))
        if(len(cp)==5):            
            return cp
        else:
           raise forms.ValidationError('Ingrese un código postal válido')
    # def clean_num_empleado(self):
    #     num_empleadoForm = self.cleaned_data.get('num_empleado')
    #     if Empleados.objects.filter(num_empleado = num_empleadoForm).exists():
    #         raise forms.ValidationError('Error: El número de empleado introducido ya está registrado')
    #     else:
    #         return num_empleadoForm
    def clean(self):
        contrasena = self.cleaned_data.get('contrasena')
        temp_contrasena = self.cleaned_data.get('temp_contrasena')

        if(contrasena == temp_contrasena):
            if(len(contrasena) < 4):                
                raise forms.ValidationError('La contraseña debe ser mayor a 4 caracteres')
        else:
            raise forms.ValidationError('Las contraseñas no coinciden')


class DetallesReporteUsuarioForm(forms.ModelForm):


    # campos de sólo lectura
    zona = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    tipo_anomalia = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    folio_seguimiento = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    foto = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    prioridad = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    geoLocalizacion = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    colonia = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    calle = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    cp = forms.IntegerField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    num_interior = forms.IntegerField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    num_exterior = forms.IntegerField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    descripcion = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    fecha = forms.DateTimeField( widget=forms.TextInput(attrs={'readonly':'readonly'}))
    id_usuario = forms.CharField(label='Usuario',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    estado = forms.CharField(label='Estado',widget=forms.TextInput(attrs={'readonly':'readonly'}))
    

    class Meta:
        model= ReportesUsuario
        # exclude = ('num_empleado',)
        fields =['zona', 'tipo_anomalia', 'folio_seguimiento', 'foto', 'prioridad', 'geoLocalizacion', 'colonia','calle', 'cp','num_interior','num_exterior','descripcion','id_usuario','estado']
        


# class ModificiarUsuarioForm(forms.ModelForm, id):
#     class Meta:
#         model = Usuarios
#         # especificar el orden de aparición de los inputs
#         fields = ['nombre','apellidos','telefono', 'email', 'num_contrato', 'colonia','calle','cp','contrasena']
#         # para modificar los atributos del html
#         widgets ={
#             'nombre': forms.TextInput(attrs={'placeholder':'Nombre completo'}),
#             'apellidos': forms.TextInput(attrs={'placeholder':'Apellidos'}),
#             'telefono': forms.NumberInput(attrs={'placeholder':'ej. 7441010122'}),
#             'email': forms.EmailInput(attrs={'placeholder':'example@example.com'}),
#             'cp': forms.NumberInput(attrs={'placeholder':'ej. 39920'}),
#             'num_contrato': forms.TextInput(attrs={'placeholder':'ej. 111-222-3333-1'})
#         }
