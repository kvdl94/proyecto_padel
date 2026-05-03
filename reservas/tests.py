from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Bono, Pista, Reserva, Usuario


@override_settings(ALLOWED_HOSTS=['testserver'])
class ReservasTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='cliente',
            password='cliente123',
            email='cliente@example.com',
            creditos=1,
        )
        self.admin = Usuario.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            is_staff=True,
        )
        self.pista = Pista.objects.create(nombre='Pista Central')
        self.bono = Bono.objects.create(
            usuario=self.usuario,
            nombre='Bono Test',
            creditos=1,
            creditos_restantes=1,
            precio=1,
        )
        self.fecha_futura = timezone.localdate() + timedelta(days=1)

    def test_no_permite_reservas_duplicadas(self):
        Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=self.fecha_futura,
            bloque='09:00',
        )

        reserva_duplicada = Reserva(
            usuario=self.usuario,
            pista=self.pista,
            fecha=self.fecha_futura,
            bloque='09:00',
        )

        with self.assertRaises(ValidationError):
            reserva_duplicada.full_clean()

    def test_no_permite_reservar_en_el_pasado(self):
        reserva_pasada = Reserva(
            usuario=self.usuario,
            pista=self.pista,
            fecha=timezone.localdate() - timedelta(days=1),
            bloque='09:00',
        )

        with self.assertRaises(ValidationError):
            reserva_pasada.full_clean()

    def test_reservar_consume_credito_de_usuario_y_bono(self):
        self.client.login(username='cliente', password='cliente123')

        response = self.client.post(reverse('reservar_pista', args=[self.pista.id]), {
            'fecha': self.fecha_futura.isoformat(),
            'bloque': '09:00',
        })

        self.assertRedirects(response, reverse('home'))
        reserva = Reserva.objects.get(usuario=self.usuario, pista=self.pista)
        self.assertEqual(reserva.bono_consumido, self.bono)

        self.usuario.refresh_from_db()
        self.bono.refresh_from_db()
        self.assertEqual(self.usuario.creditos, 0)
        self.assertEqual(self.bono.creditos_restantes, 0)

    def test_anular_reserva_devuelve_credito_de_usuario_y_bono(self):
        reserva = Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=self.fecha_futura,
            bloque='09:00',
        )
        self.usuario.creditos = 0
        self.usuario.save()
        self.bono.creditos_restantes = 0
        self.bono.save()
        self.client.login(username='cliente', password='cliente123')

        response = self.client.post(reverse('anular_reserva', args=[reserva.id]))

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Reserva.objects.filter(id=reserva.id).exists())

        self.usuario.refresh_from_db()
        self.bono.refresh_from_db()
        self.assertEqual(self.usuario.creditos, 1)
        self.assertEqual(self.bono.creditos_restantes, 1)

    def test_usuario_normal_no_puede_entrar_al_panel_admin(self):
        self.client.login(username='cliente', password='cliente123')

        response = self.client.get(reverse('panel_admin'))

        self.assertRedirects(response, reverse('home'))

    def test_usuario_staff_puede_entrar_al_panel_admin(self):
        self.client.login(username='admin', password='admin123')

        response = self.client.get(reverse('panel_admin'))

        self.assertEqual(response.status_code, 200)

    def test_anular_reserva_no_acepta_get(self):
        reserva = Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=self.fecha_futura,
            bloque='09:00',
            bono_consumido=self.bono,
        )
        self.client.login(username='cliente', password='cliente123')

        response = self.client.get(reverse('anular_reserva', args=[reserva.id]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Reserva.objects.filter(id=reserva.id).exists())

    def test_acciones_admin_destructivas_no_aceptan_get(self):
        reserva = Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=self.fecha_futura,
            bloque='09:00',
            bono_consumido=self.bono,
        )
        self.client.login(username='admin', password='admin123')

        toggle_response = self.client.get(reverse('toggle_pista', args=[self.pista.id]))
        eliminar_response = self.client.get(reverse('eliminar_reserva_admin', args=[reserva.id]))

        self.assertEqual(toggle_response.status_code, 405)
        self.assertEqual(eliminar_response.status_code, 405)
        self.pista.refresh_from_db()
        self.assertTrue(self.pista.activa)
        self.assertTrue(Reserva.objects.filter(id=reserva.id).exists())
