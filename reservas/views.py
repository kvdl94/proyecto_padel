from datetime import date
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PistaForm, RegistroForm
from .models import Bono, Pista, Reserva, Usuario


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "No tienes permisos de administrador.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def leer_entero_post(request, campo, default=0):
    try:
        return int(request.POST.get(campo, default))
    except (TypeError, ValueError):
        return default


def home(request):
    pistas = Pista.objects.filter(activa=True)
    reservas_proximas = []
    reservas_historial = []

    if request.user.is_authenticated:
        reservas_usuario = Reserva.objects.filter(usuario=request.user).order_by('fecha', 'bloque')
        reservas_proximas = [reserva for reserva in reservas_usuario if not reserva.ha_pasado]
        reservas_historial = [reserva for reserva in reservas_usuario if reserva.ha_pasado]

    return render(request, 'reservas/home.html', {
        'pistas': pistas,
        'reservas': reservas_proximas,
        'reservas_historial': reservas_historial,
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
        cantidad = leer_entero_post(request, 'cantidad')
        bonos_disponibles = {
            5: {"nombre": "Bono Básico", "precio": 5},
            10: {"nombre": "Bono Pro", "precio": 9},
            15: {"nombre": "Bono Master", "precio": 12},
        }

        if cantidad in bonos_disponibles:
            user = request.user
            bono = bonos_disponibles[cantidad]
            with transaction.atomic():
                Bono.objects.create(
                    usuario=user,
                    nombre=bono["nombre"],
                    creditos=cantidad,
                    creditos_restantes=cantidad,
                    precio=bono["precio"],
                )
                Usuario.objects.filter(id=user.id).update(creditos=F('creditos') + cantidad)
            messages.success(request, f"¡Has recargado {cantidad} créditos con éxito!")
            return redirect('home')
        messages.error(request, "Bono no válido.")

    return render(request, 'reservas/comprar_bono.html')


def consumir_credito_bono(user):
    bono = Bono.objects.select_for_update().filter(
        usuario=user,
        creditos_restantes__gt=0,
    ).order_by('fecha_compra').first()
    if not bono:
        return None

    bono.creditos_restantes = F('creditos_restantes') - 1
    bono.save(update_fields=['creditos_restantes'])
    bono.refresh_from_db()
    return bono


def devolver_credito_bono(reserva):
    bono = None
    if reserva.bono_consumido_id:
        bono = Bono.objects.select_for_update().filter(
            id=reserva.bono_consumido_id,
            creditos_restantes__lt=F('creditos'),
        ).first()

    if bono is None:
        bono = Bono.objects.select_for_update().filter(
            usuario=reserva.usuario,
            creditos_restantes__lt=F('creditos'),
        ).order_by('-fecha_compra').first()

    if bono:
        bono.creditos_restantes = F('creditos_restantes') + 1
        bono.save(update_fields=['creditos_restantes'])


def restar_creditos_bonos(user, cantidad):
    creditos_por_restar = cantidad
    bonos = Bono.objects.select_for_update().filter(
        usuario=user,
        creditos_restantes__gt=0,
    ).order_by('fecha_compra')

    for bono in bonos:
        if creditos_por_restar <= 0:
            break
        descuento = min(bono.creditos_restantes, creditos_por_restar)
        bono.creditos_restantes = F('creditos_restantes') - descuento
        bono.save(update_fields=['creditos_restantes'])
        creditos_por_restar -= descuento


def registrar_ajuste_creditos(user, cantidad):
    if cantidad > 0:
        Bono.objects.create(
            usuario=user,
            nombre="Ajuste admin",
            creditos=cantidad,
            creditos_restantes=cantidad,
            precio=0,
        )
    elif cantidad < 0:
        restar_creditos_bonos(user, abs(cantidad))


def errores_validacion_texto(error):
    if hasattr(error, 'messages'):
        return " ".join(error.messages)
    return str(error)


@login_required
def reservar_pista(request, pista_id):
    pista = get_object_or_404(Pista, id=pista_id)

    if request.method == 'POST':
        fecha_str = request.POST.get('fecha')
        bloque = request.POST.get('bloque')
        user = request.user

        try:
            fecha_reserva = date.fromisoformat(fecha_str)
        except (TypeError, ValueError):
            messages.error(request, "Selecciona una fecha válida.")
            return redirect('home')

        if user.creditos < 1:
            messages.error(request, "No tienes créditos suficientes.")
            return redirect('comprar_bono')

        reserva = Reserva(usuario=user, pista=pista, fecha=fecha_reserva, bloque=bloque)
        try:
            reserva.full_clean()
            with transaction.atomic():
                bono_consumido = consumir_credito_bono(user)
                if not bono_consumido:
                    messages.error(request, "No tienes bonos con créditos disponibles.")
                    return redirect('comprar_bono')
                reserva.bono_consumido = bono_consumido
                reserva.save()
                Usuario.objects.filter(id=user.id).update(creditos=F('creditos') - 1)
        except ValidationError as error:
            messages.error(request, errores_validacion_texto(error))
        except IntegrityError:
            messages.error(request, "Esta pista ya está ocupada para ese horario.")
        else:
            messages.success(request, f"¡Reserva en {pista.nombre} confirmada!")
            return redirect('home')

    return render(request, 'reservas/reservar_pista.html', {'pista': pista})


@login_required
@require_POST
def anular_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)

    if reserva.ha_pasado:
        messages.error(request, "No puedes anular una reserva que ya ha pasado.")
        return redirect('home')

    with transaction.atomic():
        Usuario.objects.filter(id=reserva.usuario_id).update(creditos=F('creditos') + 1)
        devolver_credito_bono(reserva)
        reserva.delete()

    messages.success(request, "Reserva anulada. Se ha devuelto 1 crédito a tu saldo.")
    return redirect('home')


@admin_required
def panel_admin(request):
    context = {
        'total_usuarios': Usuario.objects.count(),
        'total_pistas': Pista.objects.count(),
        'pistas_activas': Pista.objects.filter(activa=True).count(),
        'total_reservas': Reserva.objects.count(),
        'total_bonos': Bono.objects.count(),
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
@require_POST
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
        cantidad = leer_entero_post(request, 'cantidad')
        saldo_anterior = usuario.creditos
        usuario.creditos = max(0, usuario.creditos + cantidad)
        ajuste_real = usuario.creditos - saldo_anterior

        with transaction.atomic():
            registrar_ajuste_creditos(usuario, ajuste_real)
            usuario.save()

        accion = "añadidos" if ajuste_real >= 0 else "restados"
        messages.success(request, f"{abs(ajuste_real)} créditos {accion} a {usuario.username}. Saldo: {usuario.creditos}")
    return redirect('gestionar_usuarios')


@admin_required
def gestionar_bonos(request):
    bonos = Bono.objects.select_related('usuario').order_by('-fecha_compra')
    return render(request, 'reservas/gestionar_bonos.html', {'bonos': bonos})


@admin_required
def gestionar_reservas(request):
    reservas = Reserva.objects.select_related('usuario', 'pista').order_by('-fecha', 'bloque')
    return render(request, 'reservas/gestionar_reservas.html', {'reservas': reservas})


@admin_required
@require_POST
def eliminar_reserva_admin(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    with transaction.atomic():
        if not reserva.ha_pasado:
            Usuario.objects.filter(id=reserva.usuario_id).update(creditos=F('creditos') + 1)
            devolver_credito_bono(reserva)
        reserva.delete()
    messages.success(request, "Reserva eliminada correctamente.")
    return redirect('gestionar_reservas')
