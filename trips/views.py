from django.contrib.auth.decorators import login_required  # Obliga a iniciar sesión
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TripForm
from .models import Trip


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
    return render(request, 'trips/trip_detail.html', {'trip': trip})


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