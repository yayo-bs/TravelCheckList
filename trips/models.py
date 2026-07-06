from django.conf import settings  # Para referenciar el modelo de usuario activo del proyecto
from django.db import models      # Base para definir modelos Django


class Trip(models.Model):
    # Cada viaje pertenece a un usuario
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,   # Si se borra el usuario, se borran sus viajes
        related_name='trips'        # Permite acceder desde user.trips.all()
    )

    # Campos básicos del viaje
    title = models.CharField(max_length=120)        # Título del viaje
    destination = models.CharField(max_length=120)  # Destino
    start_date = models.DateField()                 # Fecha de inicio
    end_date = models.DateField()                   # Fecha de fin
    notes = models.TextField(blank=True)            # Notas opcionales
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática

    class Meta:
        # Orden por defecto al consultar viajes:
        # primero los que empiezan más tarde y, si empatan, los más recientes
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        # Texto legible del objeto, útil en admin y depuración
        return f"{self.title} ({self.destination})"