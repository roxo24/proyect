from django.urls import path
from _principal import views


urlpatterns = [
    path("", views.home, name= "home" ),
    path("contacto", views.contacto, name= "servi" ),
    path("info", views.info , name= "info" ),
    path("extras", views.extras, name= "extras" ),
] 
