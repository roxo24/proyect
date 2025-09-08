from django.urls import path
from gestion_pacientes import views


urlpatterns = [
    path("ingreso", views.ingreso, name= "ingreso" ),
    path("pacientes/", views.pagina_pacientes, name="pagina_pacientes"),
    path("doctores/", views.pagina_doctores, name="pagina_doctores"),
    path('atender_cita/<int:cita_id>/', views.atender_cita, name='atender_cita'),
    path("agendar_cita/", views.agendar_cita, name="agendar_cita"),
    path("consultar_citas/", views.consultar_citas, name="consultar_citas"),
    path("cancelar_cita/", views.cancelar_cita, name="cancelar_cita"),
    path("historial_medico/", views.ver_historias, name="ver_historia"),
    path("historial_medico_detalle/<int:historia_id>/", views.ver_historial, name="ver_historial"),
    path("generar_reporte/", views.generar_reporte, name="generar_reporte"),

]