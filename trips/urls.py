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

    # Rutas del CRUD de viajes
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/new/', views.trip_create, name='trip_create'),
    path('trips/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:pk>/edit/', views.trip_update, name='trip_update'),
    path('trips/<int:pk>/delete/', views.trip_delete, name='trip_delete'),

    # Rutas del CRUD de tareas
    path('trips/<int:trip_pk>/tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
]