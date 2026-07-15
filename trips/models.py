from django.conf import settings
from django.db import models


class Trip(models.Model):
    # Relación con el usuario propietario del viaje
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    title = models.CharField(max_length=120)        # Título del viaje
    destination = models.CharField(max_length=120)  # Destino
    start_date = models.DateField()                 # Inicio del viaje
    end_date = models.DateField()                   # Fin del viaje
    notes = models.TextField(blank=True)            # Notas opcionales
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    class Meta:
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.destination})"


class Task(models.Model):
    # Opciones cerradas para la prioridad
    class Priority(models.IntegerChoices):
        LOW = 1, 'Baja'
        MEDIUM = 2, 'Media'
        HIGH = 3, 'Alta'

    # Cada tarea pertenece a un viaje
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,  # Si se borra el viaje, se borran sus tareas
        related_name='tasks'       # Permite acceder desde trip.tasks.all()
    )

    title = models.CharField(max_length=160)  # Nombre de la tarea

    # Prioridad con valores controlados
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    due_date = models.DateField(null=True, blank=True)  # Fecha límite opcional
    done = models.BooleanField(default=False)           # Indica si la tarea está hecha
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Primero las pendientes, luego las más prioritarias
        ordering = ['done', '-priority', 'due_date', '-created_at']

    def __str__(self):
        return self.title