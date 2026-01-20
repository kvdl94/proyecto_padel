from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

class Usuario(AbstractUser):
    creditos = models.PositiveIntegerField(default=0)

class Pista(models.Model):
    nombre = models.CharField(max_length=100)
    imagen_url = models.URLField(max_length=500, blank=True, null=True, help_text="Pega aquí el enlace de una foto de una pista de pádel")
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    HORARIOS = [
        ('09:00', '09:00 - 10:30'),
        ('10:30', '10:30 - 12:00'),
        ('12:00', '12:00 - 13:30'),
        ('17:00', '17:00 - 18:30'),
        ('18:30', '18:30 - 20:00'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE)
    fecha = models.DateField()
    bloque = models.CharField(max_length=5, choices=HORARIOS)

    def clean(self):
        # Requisito 24: No reservar en el pasado
        if self.fecha < timezone.now().date():
            raise ValidationError("No puedes reservar en el pasado.")
        
        # Requisito 20: Evitar duplicados
        if Reserva.objects.filter(pista=self.pista, fecha=self.fecha, bloque=self.bloque).exists():
            raise ValidationError("Esta pista ya está reservada en ese horario.")