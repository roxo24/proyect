from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import  HistoriaClinica
from django import forms
from .models import Usuario, Cita, HistoriaClinica

class RegistroPacienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['documento', 'nombre', 'email', 'fecha_nacimiento', 'telefono', 'direccion', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_paciente = True
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Documento de Identidad")  
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        documento = self.cleaned_data.get('username')
        return documento 
    
class agendar_citaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'doctor', 'fecha', 'hora']

    def save(self, commit=True):
        cita = super().save(commit=False)
        cita.paciente = self.cleaned_data['paciente']
        cita.doctor = self.cleaned_data['doctor']

        if commit:
            cita.save()
            
        return cita

    

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        exclude = ['paciente', 'doctor', 'Cita', 'fecha_creacion']
