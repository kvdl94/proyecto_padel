from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Para mostrar errores si la pista está ocupada
from .forms import RegistroForm
from .models import Usuario, Pista, Reserva # Añadimos Reserva aquí

def home(request):
    pistas = Pista.objects.filter(activa=True)
    reservas_usuario = []
    
    # Si el usuario está logueado, buscamos SUS reservas
    if request.user.is_authenticated:
        reservas_usuario = Reserva.objects.filter(usuario=request.user).order_by('fecha')
        
    return render(request, 'reservas/home.html', {
        'pistas': pistas,
        'reservas': reservas_usuario
    })

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'reservas/registro.html', {'form': form})

@login_required
def comprar_bono(request):
    if request.method == 'POST':
        user = request.user
        user.creditos += 10
        user.save()
        return redirect('home')
    return render(request, 'reservas/comprar_bono.html')

# --- NUEVA FUNCIÓN PARA EL REQUISITO 20 ---
@login_required
def reservar_pista(request, pista_id):
    pista = Pista.objects.get(id=pista_id)
    
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        bloque = request.POST.get('bloque')
        user = request.user

        # Requisito 21: Validar si tiene saldo
        if user.creditos < 1:
            messages.error(request, "No tienes créditos suficientes.")
            return redirect('comprar_bono')

        # Requisito 20: Validar si la pista ya está ocupada
        existe = Reserva.objects.filter(pista=pista, fecha=fecha, bloque=bloque).exists()
        
        if existe:
            # Si ya existe, enviamos error y no guardamos
            messages.error(request, "Esta pista ya está reservada para ese día y hora.")
        else:
            # Si está libre, creamos la reserva y restamos 1 crédito
            Reserva.objects.create(usuario=user, pista=pista, fecha=fecha, bloque=bloque)
            user.creditos -= 1
            user.save()
            messages.success(request, "¡Reserva confirmada!")
            return redirect('home')

    return render(request, 'reservas/reservar_pista.html', {'pista': pista})