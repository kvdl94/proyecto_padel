from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Para mostrar errores si la pista está ocupada
from .forms import RegistroForm
from datetime import date
from .models import Usuario, Pista, Reserva # Añadimos Reserva aquí
from django.contrib.auth import login

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
            # Notificación visual para el usuario
            messages.success(request, f"¡Bienvenido {user.username}! Tu cuenta ha sido creada con éxito.") 
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'reservas/registro.html', {'form': form})

@login_required
@login_required
def comprar_bono(request):
    if request.method == 'POST':
        # Obtenemos la cantidad de créditos del botón que pulsó el usuario
        cantidad = int(request.POST.get('cantidad', 0))
        if cantidad > 0:
            user = request.user
            user.creditos += cantidad
            user.save()
            messages.success(request, f"¡Has recargado {cantidad} créditos con éxito!")
            return redirect('home')
            
    return render(request, 'reservas/comprar_bono.html')

@login_required
def reservar_pista(request, pista_id):
    # Usamos get_object_or_404 para evitar errores si la pista no existe
    pista = get_object_or_404(Pista, id=pista_id)
    
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        bloque = request.POST.get('bloque')
        user = request.user

        # Requisito 24: No permitir reservar en el pasado
        if fecha < str(date.today()):
            messages.error(request, "No puedes reservar en una fecha que ya ha pasado.")
            return redirect('home')

        # Requisito 21: Validar si tiene saldo
        if user.creditos < 1:
            messages.error(request, "No tienes créditos suficientes.")
            return redirect('comprar_bono')

        # Requisito 20: Validar si la pista ya está ocupada
        existe = Reserva.objects.filter(pista=pista, fecha=fecha, bloque=bloque).exists()
        
        if existe:
            messages.error(request, "Esta pista ya está reservada para ese día y hora.")
        else:
            # Si está libre, creamos la reserva y restamos 1 crédito
            Reserva.objects.create(usuario=user, pista=pista, fecha=fecha, bloque=bloque)
            user.creditos -= 1
            user.save()
            messages.success(request, f"¡Reserva en {pista.nombre} confirmada!")
            return redirect('home')

    return render(request, 'reservas/reservar_pista.html', {'pista': pista})

@login_required
def anular_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
    
    # Devolvemos el crédito al usuario (Requisito 21)
    user = request.user
    user.creditos += 1
    user.save()
    
    reserva.delete()
    messages.success(request, "Reserva anulada. Se ha devuelto 1 crédito a tu saldo.")
    return redirect('home')