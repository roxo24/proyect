from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime


class UsuarioManager(BaseUserManager):
    def create_user(self, documento, nombre, password=None, **extra_fields):
        if not documento:
            raise ValueError("El usuario debe tener un documento de identidad")
        
        extra_fields.setdefault("is_active", True)
        
        user = self.model(documento=documento, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, documento, nombre, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(documento, nombre, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    

    
    is_paciente = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #
    objects = UsuarioManager()

    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['nombre']

    def save(self, *args, **kwargs):
        
        
        if self.pk is None or not self.password.startswith('pbkdf2_sha256$'):
            self.set_password(self.password)

        super().save(*args, **kwargs)

        
        if self.is_paciente and not hasattr(self, 'paciente'):
            Paciente.objects.create(usuario=self)

        
        if self.is_doctor and not hasattr(self, 'doctor'):
            Doctor.objects.create(usuario=self)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "gestion_pacientes_usuario"

class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="paciente")
    

    def __str__(self):
        return f"Paciente: {self.usuario.nombre}"

    class Meta:
        db_table = "gestion_pacientes_paciente"

class Doctor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="doctor")
    ESCOGER_ESPECIALIDAD = [
        ('Medicina general', 'Medicina General'),
        ('Ginecologia', 'Ginecologia'),
        ('Psicologia', 'Psicologia'),
        ('Odontologia', 'Odontologia'),
        ('Planificacion familiar', 'Planificacion Familiar'),
        ('Pediatria', 'Pediatria'),
    ]
    especialidad = models.CharField(max_length=50, choices=ESCOGER_ESPECIALIDAD, default='Medicina general')
    numero_licencia = models.CharField(max_length=50, unique=True, blank=True, null=True)
    años_experiencia = models.IntegerField(default=0, blank=True, null=True)
    inicio_horario = models.TimeField(blank=True, null=True)
    fin_horario = models.TimeField(blank=True, null=True)



    def __str__(self):
        return f"Dr. {self.usuario.nombre} - {self.especialidad}"

    class Meta:
        db_table = "gestion_pacientes_doctor"


class Cita(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'is_paciente': True}, related_name='citas')
    doctor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'is_doctor': True}, related_name='citas_recibidas')
    
    fecha = models.DateField()
    hora = models.TimeField()
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    fecha_creacion = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Cita: {self.paciente.nombre} con Dr. {self.doctor.nombre} el {self.fecha} a las {self.hora}'

    class Meta:
        db_table = "gestion_pacientes_cita"
        ordering = ['-fecha', '-hora']


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='historias_clinicas')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='historias_clinicas')
    Cita= models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='historias_clinicas')
    motivo = models.TextField()

    antecedentes_patologicos = models.TextField()
    antecedentes_quirurgicos = models.TextField()
    alergias = models.TextField()
    medicamentos_actuales = models.TextField()

    antecedentes_familiares = models.TextField()

    cardiovascular = models.TextField()
    respiratorio = models.TextField()
    gastrointestinal = models.TextField()
    neurologico = models.TextField()

    peso = models.DecimalField(max_digits=5, decimal_places=2)
    estatura = models.DecimalField(max_digits=5, decimal_places=2)
    
    
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField(blank=True, null=True)

    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Historia Clínica de {self.paciente.usuario.nombre} - {self.fecha_creacion}'

    class Meta:
        db_table = "gestion_pacientes_historia_clinica"
        ordering = ['-fecha_creacion']