from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Paciente, Doctor, Cita, HistoriaClinica

class UsuarioAdmin(UserAdmin):
    list_display = ('documento', 'nombre', 'is_paciente', 'is_doctor', 'is_staff')
    list_filter = ('is_paciente', 'is_doctor', 'is_staff')
    fieldsets = (
        (None, {'fields': ('documento', 'nombre', 'email', 'password')}),
        ('Información Personal', {'fields': ('telefono', 'direccion', 'fecha_nacimiento')}),
        ('Roles', {'fields': ('is_paciente', 'is_doctor', 'is_staff')}),
        ('Permisos', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('documento', 'nombre', 'email', 'password1', 'password2', 'is_paciente', 'is_doctor')}
        ),
    )
    search_fields = ('documento', 'nombre', 'email')
    ordering = ('documento',)

admin.site.register(Usuario, UsuarioAdmin)
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', )
    search_fields = ('usuario__nombre', 'usuario__documento')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'especialidad', 'numero_licencia', 'años_experiencia')
    search_fields = ('usuario__nombre', 'especialidad', 'numero_licencia')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha', 'doctor')
    search_fields = ('paciente__usuario__nombre', 'doctor__usuario__nombre')

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'doctor', 'motivo', 'diagnostico', 'fecha_creacion')
    search_fields = ('paciente__usuario__nombre', 'doctor__usuario__nombre', 'diagnostico')
    list_filter = ('fecha_creacion', 'doctor')
    readonly_fields = ('fecha_creacion',)