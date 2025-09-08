from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Cita, Usuario, HistoriaClinica, Doctor

from django.contrib.auth.decorators import login_required

def ingreso(request):
    if request.method == "POST":
        if request.POST.get("type") == "form_login":
            
            documento = request.POST["documento"]
            password = request.POST["password"]
            user = authenticate(request, documento=documento, password=password)

            if user is not None:
                login(request, user)
                
                
                if user.is_paciente:
                    return redirect("pagina_pacientes")
                elif user.is_doctor:
                    return redirect("pagina_doctores")
                else:
                    return redirect("admin:index")

            else:
                messages.error(request, "Usuario o contraseña incorrectos.")

        elif request.POST.get("type") == "form_register":
            documento = request.POST["documento"]
            nombre = request.POST["nombre"]
            email = request.POST["email"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]

            if password1 != password2:
                messages.error(request, "Las contraseñas no coinciden.")
                return redirect("ingreso")

            if Usuario.objects.filter(documento=documento).exists():
                messages.error(request, "Este usuario ya está registrado.")
                return redirect("ingreso")
            user = Usuario.objects.create(
                documento=documento,
                nombre=nombre,
                email=email,
                password=(password1),  
                is_paciente=True  
            )

            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect("ingreso")

    return render(request, "gestion_pacientes/login.html")

@login_required
def pagina_pacientes(request):
    user = request.user
    if not user.is_paciente:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return render(request, "gestion_pacientes/indexpc.html")


@login_required
def agendar_cita(request):
    user = request.user
    if not user.is_paciente:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    if request.method == 'POST':
        if request.POST.get("type") == "form_agendar_cita":
            cita= request.POST.get("cita")
            
            fecha = request.POST['fecha']
            hora = request.POST['hora']
            doctor_id = request.POST['doctor']  
            doctor = Doctor.objects.get(id=doctor_id)
            doctor_usuario = doctor.usuario

            if Cita.objects.filter(id=cita).exists():
                messages.error(request, "Esta cita ya ha sido agendada.")
                return redirect('agendar_cita')
            if Cita.objects.filter( fecha=fecha, hora=hora, doctor=doctor_usuario).exists():
                messages.error(request, "El doctor ya tiene una cita programada para esa fecha y hora.")
                return redirect('agendar_cita')
        
            cita = Cita.objects.create(fecha=fecha, hora=hora, paciente=user, doctor=doctor_usuario)  

            messages.success(request, "cita agendada correctamente.")

            return redirect('agendar_cita')
            
      
    doctores = Doctor.objects.all()
    return render(request, 'gestion_pacientes/indexac.html', {'doctores': doctores})

@login_required
def consultar_citas(request):
    user = request.user
    if not user.is_paciente:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    
    citas = Cita.objects.filter(paciente=user, estado="pendiente").select_related('doctor')
    citas = citas.order_by('fecha')
    for cita in citas:
        cita.doctor_perfil = Doctor.objects.filter(usuario=cita.doctor).first()

    
    return render(request, "gestion_pacientes/indexcc.html", {'citas': citas})

@login_required
def cancelar_cita(request):
    user = request.user
    if not user.is_paciente:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    

    citas = Cita.objects.filter(paciente=user, estado="pendiente").select_related('doctor')
    citas = citas.order_by('fecha')
    for cita in citas:
        cita.doctor_perfil = Doctor.objects.filter(usuario=cita.doctor).first()

    
    
    if request.method == 'POST':
        cita_id = request.POST.get('cita_id')
        try:
            cita = Cita.objects.get(id=cita_id, paciente=user)
            cita.delete()
            messages.success(request, "Cita cancelada exitosamente.")
        except Cita.DoesNotExist:
            messages.error(request, "No se encontró la cita.")
        return redirect('cancelar_cita')
        
    return render(request, "gestion_pacientes/indexcac.html", {'citas': citas})

@login_required
def pagina_doctores(request):
    user = request.user
    if not user.is_doctor:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    citas = Cita.objects.filter(doctor=user, estado="pendiente").order_by('fecha')

    return render(request, "gestion_pacientes/indexmd.html", {'citas': citas})
    


@login_required
def atender_cita(request, cita_id):
    user= request.user
    if not user.is_doctor:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    cita = Cita.objects.get(id=cita_id)
    paciente = cita.paciente.paciente
    doctor = cita.doctor.doctor 

    if request.method == 'POST':
        if request.POST.get("type") == "form_atender":
            motivo = request.POST.get("motivo")
            antecedentes_patologicos = request.POST.get("antecedentes_patologicos")
            antecedentes_quirurgicos = request.POST.get("antecedentes_quirurgicos")
            alergias = request.POST.get("alergias")
            medicamentos = request.POST.get("medicamentos")
            
            antecedentes_familiares = request.POST.get("antecedentes_familiares")
            revision_cardiovascular = request.POST.get("revision_cardio")
            revision_respiratoria = request.POST.get("revision_respiratoria")
            revision_digestiva = request.POST.get("revision_digestiva")
            revision_neurologica = request.POST.get("revision_neurologica")
            peso = request.POST.get("peso")
            estatura = request.POST.get("estatura")
            diagnostico = request.POST.get("diagnostico")
            plan_tratamiento = request.POST.get("plan_tratamiento")
            
            HistoriaClinica.objects.create(
                paciente=paciente,
                doctor=doctor,
                Cita=cita,
                motivo=motivo,
                antecedentes_patologicos=antecedentes_patologicos,
                antecedentes_quirurgicos=antecedentes_quirurgicos,
                alergias=alergias,
                medicamentos_actuales=medicamentos,
                
                antecedentes_familiares=antecedentes_familiares,
                cardiovascular=revision_cardiovascular,
                respiratorio=revision_respiratoria,
                gastrointestinal=revision_digestiva,
                neurologico=revision_neurologica,
                peso=peso,
                estatura=estatura,
                diagnostico=diagnostico,
                tratamiento=plan_tratamiento
            )

            cita.estado = 'completada'
            cita.save()
            messages.success(request, "Historia clínica creada exitosamente.")
            return redirect('atender_cita', cita_id=cita_id)
    return render(request, 'gestion_pacientes/indexr.html', {'cita': cita, 'paciente': paciente, 'doctor': doctor})

@login_required
def ver_historias(request):
    user = request.user
    if not user.is_paciente:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    historias = HistoriaClinica.objects.filter(paciente=user.paciente).order_by('-fecha_creacion')
    return render(request, 'gestion_pacientes/ver_historia.html', {'historias': historias})

@login_required
def ver_historial(request, historia_id):
    user = request.user
    if not user.is_paciente:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    historia = HistoriaClinica.objects.get(id=historia_id, paciente=user.paciente) 

    return render(request, 'gestion_pacientes/ver_historia_detalle.html', {'historia': historia})

@login_required
def generar_reporte(request):
    user = request.user
    if not user.is_doctor:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    historias = HistoriaClinica.objects.filter(doctor=user.doctor).order_by('-fecha_creacion')
    
    return render(request, 'gestion_pacientes/reporte_historias.html', {'historias': historias})