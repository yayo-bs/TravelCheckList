from django.contrib.auth.forms import UserCreationForm  # Formulario de registro ya preparado por Django
from django.shortcuts import render, redirect           # render devuelve HTML; redirect redirige a otra URL


def home(request):
    # Página de inicio pública
    return render(request, 'trips/home.html')


def signup(request):
    # Si el usuario envía el formulario, procesamos los datos
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        # Si el formulario es válido, guardamos el nuevo usuario
        if form.is_valid():
            form.save()
            return redirect('trips:login')  # Tras registrarse, lo enviamos al login
    else:
        # Si entra por GET, mostramos el formulario vacío
        form = UserCreationForm()

    # Renderizamos el template pasando el formulario al contexto
    return render(request, 'trips/signup.html', {'form': form})