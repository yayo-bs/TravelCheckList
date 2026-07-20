from django.contrib.auth.decorators import login_required  # Obliga a iniciar sesión
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TripForm, TaskForm
from .models import Trip, Task


def home(request):
    # Home pública
    return render(request, 'trips/home.html')


def signup(request):
    # Registro de usuario
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trips:login')
    else:
        form = UserCreationForm()

    return render(request, 'trips/signup.html', {'form': form})


@login_required
def trip_list(request):
    # Mostramos solo los viajes del usuario autenticado
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'trips/trip_list.html', {'trips': trips})


@login_required
def trip_create(request):
    # Crear viaje
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)  # Creamos el objeto sin guardar todavía
            trip.user = request.user        # Asignamos el usuario autenticado
            trip.save()
            return redirect('trips:trip_list')
    else:
        form = TripForm()

    return render(request, 'trips/trip_form.html', {'form': form, 'mode': 'create'})


@login_required
def trip_detail(request, pk):
    # Recupera el viaje del usuario o devuelve 404 si no existe/no le pertenece
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    tasks = trip.tasks.all()
    return render(request, 'trips/trip_detail.html', {'trip': trip, 'tasks': tasks})


@login_required
def trip_update(request, pk):
    # Edición de un viaje existente
    trip = get_object_or_404(Trip, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect('trips:trip_detail', pk=trip.pk)
    else:
        form = TripForm(instance=trip)

    return render(request, 'trips/trip_form.html', {'form': form, 'mode': 'update', 'trip': trip})


@login_required
def trip_delete(request, pk):
    # Borrado de un viaje existente
    trip = get_object_or_404(Trip, pk=pk, user=request.user)

    if request.method == 'POST':
        trip.delete()
        return redirect('trips:trip_list')

    return render(request, 'trips/trip_confirm_delete.html', {'trip': trip})


@login_required
def task_create(request, trip_pk):
    # Crear una tarea asociada a un viaje concreto del usuario
    trip = get_object_or_404(Trip, pk=trip_pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.trip = trip
            task.save()
            return redirect('trips:trip_detail', pk=trip.pk)
    else:
        form = TaskForm()

    return render(request, 'trips/task_form.html', {'form': form, 'trip': trip, 'mode': 'create'})


@login_required
def task_update(request, pk):
    # Editar una tarea; comprobamos que el usuario sea dueño del viaje al que pertenece
    task = get_object_or_404(Task, pk=pk, trip__user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('trips:trip_detail', pk=task.trip.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'trips/task_form.html', {'form': form, 'trip': task.trip, 'task': task, 'mode': 'update'})


@login_required
def task_delete(request, pk):
    # Borrar tarea y volver al detalle del viaje
    task = get_object_or_404(Task, pk=pk, trip__user=request.user)
    trip = task.trip

    if request.method == 'POST':
        task.delete()
        return redirect('trips:trip_detail', pk=trip.pk)

    return render(request, 'trips/task_confirm_delete.html', {'task': task, 'trip': trip})