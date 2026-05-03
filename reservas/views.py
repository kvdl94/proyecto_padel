from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps
from .forms import RegistroForm, PistaForm
from datetime import date, datetime
from .models import Usuario, Pista, Reserva


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "No tienes permisos de administrador.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def home(request):
    pistas = Pista.objects.filter(activa=True)
    reservas_usuario = []
    
    if request.user.is_authenticated:
        # Mejora Requisito 22: Ordenamos por fecha Y por bloque horario
        reservas_usuario = Reserva.objects.filter(usuario=request.user).order_by('fecha', 'bloque')
        
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
            messages.success(request, f"¡Bienvenido {user.username}! Tu cuenta ha sido creada con éxito.") 
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'reservas/registro.html', {'form': form})

@login_required
def comprar_bono(request):
    if request.method == 'POST':
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
    pista = get_object_or_404(Pista, id=pista_id)
    
    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        bloque = request.POST.get('bloque')
        user = request.user

        # --- MEJORA REQUISITO 24: Validar pasado exacto (Fecha + Hora) ---
        ahora = datetime.now()
        # Intentamos combinar la fecha y hora seleccionada para comparar
        try:
            # Esto asume que el bloque viene como "10:00", "17:30", etc.
            fecha_seleccionada = datetime.strptime(f"{fecha_str} {bloque}", "%Y-%m-%d %H:%M")
        except ValueError:
            # Si el formato falla, usamos una comparación básica de fecha
            fecha_seleccionada = datetime.combine(date.fromisoformat(fecha_str), ahora.time())

        if fecha_seleccionada < ahora:
            messages.error(request, "No puedes reservar en un horario que ya ha pasado.")
            return redirect('home')

        # --- Requisito 21: Validar saldo ---
        if user.creditos < 1:
            messages.error(request, "No tienes créditos suficientes.")
            return redirect('comprar_bono')

        # --- Requisito 20: Validar disponibilidad ---
        existe = Reserva.objects.filter(pista=pista, fecha=fecha_str, bloque=bloque).exists()
        
        if existe:
            messages.error(request, "Esta pista ya está ocupada para ese horario.")
        else:
            # Solo si es futuro y está libre, restamos crédito y guardamos
            Reserva.objects.create(usuario=user, pista=pista, fecha=fecha_str, bloque=bloque)
            user.creditos -= 1
            user.save()
            messages.success(request, f"¡Reserva en {pista.nombre} confirmada!")
            return redirect('home')

    return render(request, 'reservas/reservar_pista.html', {'pista': pista})

@login_required
def anular_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)

    user = request.user
    user.creditos += 1
    user.save()

    reserva.delete()
    messages.success(request, "Reserva anulada. Se ha devuelto 1 crédito a tu saldo.")
    return redirect('home')


# --- PANEL DE ADMINISTRACIÓN ---

@admin_required
def panel_admin(request):
    context = {
        'total_usuarios': Usuario.objects.count(),
        'total_pistas': Pista.objects.count(),
        'pistas_activas': Pista.objects.filter(activa=True).count(),
        'total_reservas': Reserva.objects.count(),
    }
    return render(request, 'reservas/panel_admin.html', context)


@admin_required
def gestionar_pistas(request):
    pistas = Pista.objects.all().order_by('nombre')
    return render(request, 'reservas/gestionar_pistas.html', {'pistas': pistas})


@admin_required
def crear_pista(request):
    if request.method == 'POST':
        form = PistaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pista creada correctamente.")
            return redirect('gestionar_pistas')
    else:
        form = PistaForm()
    return render(request, 'reservas/form_pista.html', {'form': form, 'titulo': 'Crear pista'})


@admin_required
def editar_pista(request, pista_id):
    pista = get_object_or_404(Pista, id=pista_id)
    if request.method == 'POST':
        form = PistaForm(request.POST, instance=pista)
        if form.is_valid():
            form.save()
            messages.success(request, f"Pista '{pista.nombre}' actualizada.")
            return redirect('gestionar_pistas')
    else:
        form = PistaForm(instance=pista)
    return render(request, 'reservas/form_pista.html', {'form': form, 'titulo': f'Editar: {pista.nombre}'})


@admin_required
def toggle_pista(request, pista_id):
    pista = get_object_or_404(Pista, id=pista_id)
    pista.activa = not pista.activa
    pista.save()
    estado = "activada" if pista.activa else "desactivada"
    messages.success(request, f"Pista '{pista.nombre}' {estado}.")
    return redirect('gestionar_pistas')


@admin_required
def gestionar_usuarios(request):
    usuarios = Usuario.objects.all().order_by('username')
    return render(request, 'reservas/gestionar_usuarios.html', {'usuarios': usuarios})


@admin_required
def ajustar_creditos(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        usuario.creditos = max(0, usuario.creditos + cantidad)
        usuario.save()
        accion = "añadidos" if cantidad >= 0 else "restados"
        messages.success(request, f"{abs(cantidad)} créditos {accion} a {usuario.username}. Saldo: {usuario.creditos}")
    return redirect('gestionar_usuarios')


@admin_required
def gestionar_reservas(request):
    reservas = Reserva.objects.select_related('usuario', 'pista').order_by('-fecha', 'bloque')
    return render(request, 'reservas/gestionar_reservas.html', {'reservas': reservas})


@admin_required
def eliminar_reserva_admin(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.usuario.creditos += 1
    reserva.usuario.save()
    reserva.delete()
    messages.success(request, "Reserva eliminada y crédito devuelto al usuario.")
    return redirect('gestionar_reservas')