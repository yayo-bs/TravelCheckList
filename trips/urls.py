from django.contrib.auth import views as auth_views  # Vistas genéricas de autenticación
from django.urls import path   # Función para definir rutas
from . import views            # Importamos las vistas de esta misma app

app_name = 'trips'             # Espacio de nombres para usar rutas como trips:home

urlpatterns = [
    path('', views.home, name='home'),  # Ruta raíz de la app: llama a la vista home
    path('signup/', views.signup, name='signup'),  # Ruta para el registro de usuarios

    # Login usando la vista genérica de Django y nuestro template personalizado
    path('login/', auth_views.LoginView.as_view(template_name='trips/login.html'), name='login'),

    # Logout usando la vista genérica de Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]