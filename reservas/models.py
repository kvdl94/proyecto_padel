from datetime import date
from datetime import datetime as datetime_class

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Usuario(AbstractUser):
    creditos = models.PositiveIntegerField(default=0)


class Bono(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='bonos')
    nombre = models.CharField(max_length=50)
    creditos = models.PositiveIntegerField()
    creditos_restantes = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    @property
    def creditos_consumidos(self):
        return self.creditos - self.creditos_restantes

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username} ({self.creditos_restantes}/{self.creditos})"


class Pista(models.Model):
    nombre = models.CharField(max_length=100)
    imagen_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Pega aquí el enlace de una foto de una pista de pádel",
    )
    activa = models.BooleanField(default=True)

    @property
    def esta_llena_hoy(self):
        hoy = date.today()
        total_reservas_hoy = self.reserva_set.filter(fecha=hoy).count()
        return total_reservas_hoy >= 6

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    HORARIOS = [
        ('09:00', '09:00 - 10:30'),
        ('10:30', '10:30 - 12:00'),
        ('12:00', '12:00 - 13:30'),
        ('17:00', '17:00 - 18:30'),
        ('18:30', '18:30 - 20:00'),
        ('20:00', '20:00 - 21:30'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE)
    bono_consumido = models.ForeignKey(
        Bono,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas',
    )
    fecha = models.DateField()
    bloque = models.CharField(max_length=5, choices=HORARIOS)

    @property
    def fecha_hora_inicio(self):
        return datetime_class.combine(self.fecha, datetime_class.strptime(self.bloque, "%H:%M").time())

    @property
    def ha_pasado(self):
        return self.fecha_hora_inicio < timezone.localtime().replace(tzinfo=None)

    def clean(self):
        horarios_validos = dict(self.HORARIOS)
        if self.fecha and self.bloque in horarios_validos and self.ha_pasado:
            raise ValidationError("No puedes reservar en un horario que ya ha pasado.")

        if not self.pista_id or not self.fecha or not self.bloque:
            return

        reservas_iguales = Reserva.objects.filter(pista=self.pista, fecha=self.fecha, bloque=self.bloque)
        if self.pk:
            reservas_iguales = reservas_iguales.exclude(pk=self.pk)
        if reservas_iguales.exists():
            raise ValidationError("Esta pista ya está reservada en ese horario.")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['pista', 'fecha', 'bloque'],
                name='reserva_unica_por_pista_fecha_bloque',
            )
        ]
