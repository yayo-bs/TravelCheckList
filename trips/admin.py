from django.contrib import admin
from .models import Trip, Task


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'destination', 'start_date', 'end_date', 'user')
    search_fields = ('title', 'destination', 'notes', 'user__username')
    list_filter = ('destination', 'start_date')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'trip', 'priority', 'due_date', 'done')
    search_fields = ('title', 'trip__title')
    list_filter = ('priority', 'done')