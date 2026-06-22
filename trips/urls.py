from django.urls import path   # Función para definir rutas
from . import views            # Importamos las vistas de esta misma app

app_name = 'trips'             # Espacio de nombres para usar rutas como trips:home

urlpatterns = [
    path('', views.home, name='home'),  # Ruta raíz de la app: llama a la vista home
]