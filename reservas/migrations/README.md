# Migraciones

Esta carpeta guarda la evolucion de la base de datos de la app `reservas`.

No se deben borrar migraciones ya aplicadas si se quiere conservar la base de datos actual.

## Migraciones importantes

- `0001_initial.py`: crea los modelos iniciales.
- `0003_pista_imagen_url.py`: anade imagen opcional a las pistas.
- `0004_...`: crea el modelo `Bono`.
- `0005_bono_creditos_restantes.py`: anade `creditos_restantes` y crea saldos iniciales para usuarios que ya tenian creditos.
- `0006_alter_reserva_bloque.py`: anade el horario `20:00 - 21:30`.
- `0007_reserva_reserva_unica_por_pista_fecha_bloque.py`: anade la restriccion unica para impedir reservas duplicadas.

## Comandos utiles

Crear nuevas migraciones:

```bash
python manage.py makemigrations
```

Aplicar migraciones:

```bash
python manage.py migrate
```

Comprobar si faltan migraciones:

```bash
python manage.py makemigrations --check --dry-run
```
