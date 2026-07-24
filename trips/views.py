from django.contrib.auth.decorators import login_required  # Obliga a iniciar sesión
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator  # Divide resultados en páginas
from django.db.models import Q               # Permite búsquedas OR en varios campos
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

        # form.is_valid() lanza la validación del formulario
        if form.is_valid():
            form.save()
            return redirect('trips:login')
    else:
        form = UserCreationForm()

    return render(request, 'trips/signup.html', {'form': form})


@login_required
def trip_list(request):
    # 1) Consulta base: solo viajes del usuario autenticado
    trips = Trip.objects.filter(user=request.user)

    # 2) Leemos parámetros GET del listado
    q = request.GET.get('q', '').strip()
    destination = request.GET.get('destination', '').strip()
    order = request.GET.get('order', 'start_desc')

    # 3) Búsqueda libre en varios campos
    if q:
        trips = trips.filter(
            Q(title__icontains=q) |
            Q(destination__icontains=q) |
            Q(notes__icontains=q)
        )

    # 4) Filtro por destino exacto (lo recibimos desde un desplegable)
    if destination:
        trips = trips.filter(destination=destination)

    # 5) Orden dinámico según la opción elegida
    order_options = {
        'start_desc': '-start_date',   # Más recientes primero
        'start_asc': 'start_date',     # Más antiguos primero
        'destination_asc': 'destination',
        'created_desc': '-created_at',
        'created_asc': 'created_at',
    }
    trips = trips.order_by(order_options.get(order, '-start_date'))

    # 6) Lista de destinos únicos para rellenar el filtro del template
    destinations = (
        Trip.objects
        .filter(user=request.user)
        .values_list('destination', flat=True)
        .distinct()
        .order_by('destination')
    )

    # 7) Paginación: 4 viajes por página
    paginator = Paginator(trips, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 8) Enviamos al template tanto la página actual como los filtros activos
    context = {
        'trips': page_obj.object_list,
        'page_obj': page_obj,
        'q': q,
        'destination': destination,
        'order': order,
        'destinations': destinations,
    }
    return render(request, 'trips/trip_list.html', context)


@login_required
def trip_create(request):
    # Crear un nuevo viaje
    if request.method == 'POST':
        form = TripForm(request.POST)

        # Si el formulario pasa validación, guardamos el viaje
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('trips:trip_list')
    else:
        form = TripForm()

    return render(request, 'trips/trip_form.html', {'form': form, 'mode': 'create'})


@login_required
def trip_detail(request, pk):
    # Mostramos el viaje y todas sus tareas asociadas
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    tasks = trip.tasks.all()
    return render(request, 'trips/trip_detail.html', {'trip': trip, 'tasks': tasks})


@login_required
def trip_update(request, pk):
    # Editar un viaje existente
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
    # Borrar un viaje
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
