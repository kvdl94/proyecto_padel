# App `reservas`

Esta es la aplicacion principal del proyecto. Contiene la logica de usuarios, pistas, reservas, bonos, panel de administracion y tests.

## Modelos

Los modelos estan en `models.py`.

- `Usuario`: usuario personalizado basado en `AbstractUser`. Incluye el campo `creditos`.
- `Bono`: registra compras o ajustes de creditos. Guarda creditos totales, restantes, precio y fecha.
- `Pista`: representa una pista de padel. Puede estar activa o inactiva.
- `Reserva`: representa una reserva de usuario, pista, fecha y franja horaria.

`Reserva` incluye validaciones importantes:

- No permite reservar en horarios pasados.
- Evita duplicados de pista, fecha y bloque.
- Tiene una restriccion unica en base de datos para `pista + fecha + bloque`.

## Vistas

Las vistas estan en `views.py`.

Flujos principales:

- `home`: muestra pistas, proximas reservas e historial.
- `registro`: crea usuario y lo inicia automaticamente.
- `comprar_bono`: crea un `Bono` y suma creditos al usuario.
- `reservar_pista`: valida la reserva, consume credito y guarda la reserva.
- `anular_reserva`: anula reservas futuras y devuelve credito.

Panel admin personalizado:

- `panel_admin`
- `gestionar_pistas`
- `gestionar_usuarios`
- `gestionar_bonos`
- `gestionar_reservas`

## Formularios

Los formularios estan en `forms.py`.

- `RegistroForm`: valida contrasena y confirmacion.
- `PistaForm`: permite crear y editar pistas desde el panel.

## Admin Django

`admin.py` registra los modelos para el admin nativo de Django.

`BonoAdmin` muestra columnas utiles como usuario, creditos, creditos restantes, precio y fecha de compra.

## Tests

`tests.py` cubre:

- Reservas duplicadas.
- Reservas en pasado.
- Consumo de credito al reservar.
- Devolucion de credito al anular.
- Permisos del panel admin.

Ejecutar:

```bash
python manage.py test
```
