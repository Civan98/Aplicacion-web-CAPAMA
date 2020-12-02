from django import forms

class FormLogin(forms.Form):
    email    = forms.EmailField(label= 'Correo Electronico')
    password = forms.CharField(label= 'Contraseña', max_length=32, widget=forms.PasswordInput)
