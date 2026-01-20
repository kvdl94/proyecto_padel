from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from .models import Pista

def home(request):
    pistas = Pista.objects.filter(activa=True)
    return render(request, 'reservas/home.html', {'pistas': pistas})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Inicia sesión automáticamente tras registro
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'reservas/registro.html', {'form': form})