# App `reservas`

Aplicación principal del proyecto. Contiene los modelos, vistas, formularios, panel de administración personalizado y tests.

---

## Modelos

Definidos en `models.py`.

### `Usuario`

Extiende `AbstractUser`. Añade un único campo extra:

| Campo | Tipo | Descripción |
|---|---|---|
| `creditos` | `PositiveIntegerField` | Saldo de créditos disponibles para reservar. |

### `Bono`

Registra cada compra o ajuste de créditos realizado sobre un usuario.

| Campo | Tipo | Descripción |
|---|---|---|
| `usuario` | FK → `Usuario` | Propietario del bono. |
| `nombre` | `CharField` | Nombre del bono (p. ej. "Bono Pro", "Ajuste admin"). |
| `creditos` | `PositiveIntegerField` | Créditos totales del bono al crearlo. |
| `creditos_restantes` | `PositiveIntegerField` | Créditos aún no consumidos. |
| `precio` | `DecimalField` | Precio pagado (0 para ajustes administrativos). |
| `fecha_compra` | `DateTimeField` | Fecha y hora de creación (auto). |

Propiedad calculada: `creditos_consumidos = creditos - creditos_restantes`.

### `Pista`

Representa una pista de pádel gestionable desde el panel de administración.

| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | `CharField` | Nombre identificativo de la pista. |
| `imagen_url` | `URLField` | URL de una imagen representativa (opcional). |
| `activa` | `BooleanField` | Controla si la pista aparece disponible en la home. |

Propiedad calculada: `esta_llena_hoy` — devuelve `True` si ya hay 6 reservas para hoy.

### `Reserva`

Asocia un usuario a una pista en una fecha y franja horaria concreta.

| Campo | Tipo | Descripción |
|---|---|---|
| `usuario` | FK → `Usuario` | Usuario que realiza la reserva. |
| `pista` | FK → `Pista` | Pista reservada. |
| `bono_consumido` | FK → `Bono` (nullable) | Bono del que se descontó el crédito. |
| `fecha` | `DateField` | Día de la reserva. |
| `bloque` | `CharField` | Franja horaria (choices). |

**Franjas horarias disponibles:** 09:00, 10:30, 12:00, 17:00, 18:30, 20:00.

**Validaciones en `clean()`:**
- No permite reservar en horarios ya pasados.
- No permite reservar una pista ya ocupada en el mismo bloque y fecha.

**Restricción de base de datos:** `UniqueConstraint` sobre `(pista, fecha, bloque)`.

---

## Vistas

Definidas en `views.py`.

### Vistas de usuario

| Vista | URL | Descripción |
|---|---|---|
| `home` | `/` | Muestra pistas activas, próximas reservas e historial del usuario autenticado. |
| `registro` | `/registro/` | Crea una cuenta y autentica al usuario automáticamente. |
| `comprar_bono` | `/comprar-bono/` | Muestra los bonos disponibles y procesa la compra (3 opciones: 5, 10 y 15 créditos). |
| `reservar_pista` | `/reservar/<id>/` | Valida disponibilidad, descuenta un crédito del bono más antiguo y crea la reserva. |
| `anular_reserva` | `/anular/<id>/` | Anula una reserva futura y devuelve el crédito al usuario y al bono original. Solo acepta POST. |

### Panel de administración personalizado

Accesible únicamente para usuarios con `is_staff=True`. El decorador `@admin_required` redirige a la home si el usuario no tiene permisos.

| Vista | URL | Descripción |
|---|---|---|
| `panel_admin` | `/panel-admin/` | Dashboard con contadores de usuarios, pistas, reservas y bonos. |
| `gestionar_pistas` | `/panel-admin/pistas/` | Lista todas las pistas con acciones de editar, crear y activar/desactivar. |
| `crear_pista` | `/panel-admin/pistas/crear/` | Formulario para crear una nueva pista. |
| `editar_pista` | `/panel-admin/pistas/<id>/editar/` | Formulario para editar nombre, imagen y estado de una pista existente. |
| `toggle_pista` | `/panel-admin/pistas/<id>/toggle/` | Activa o desactiva una pista. Solo acepta POST. |
| `gestionar_usuarios` | `/panel-admin/usuarios/` | Lista todos los usuarios con su saldo de créditos. |
| `ajustar_creditos` | `/panel-admin/usuarios/<id>/creditos/` | Suma o resta créditos a un usuario y registra el movimiento como `Bono`. |
| `gestionar_bonos` | `/panel-admin/bonos/` | Lista todos los bonos ordenados por fecha de compra descendente. |
| `gestionar_reservas` | `/panel-admin/reservas/` | Lista todas las reservas con usuario y pista asociados. |
| `eliminar_reserva_admin` | `/panel-admin/reservas/<id>/eliminar/` | Elimina una reserva; si es futura, devuelve el crédito al usuario. Solo acepta POST. |

---

## Formularios

Definidos en `forms.py`.

### `RegistroForm`

Basado en `ModelForm` sobre `Usuario`. Campos: `username`, `email`, `password` y `confirmar_password`. Valida que ambas contraseñas coincidan y aplica `set_password` al guardar.

### `PistaForm`

Basado en `ModelForm` sobre `Pista`. Campos: `nombre`, `imagen_url` y `activa`. Incluye widgets con clases Bootstrap.

---

## Admin Django

Registrado en `admin.py`.

- `BonoAdmin`: muestra columnas `nombre`, `usuario`, `creditos`, `creditos_restantes`, `precio` y `fecha_compra`. Permite filtrar por nombre y fecha, y buscar por username o nombre de bono.
- `Usuario`, `Pista` y `Reserva` registrados con configuración por defecto.

---

## Tests

Definidos en `tests.py`. Ejecutar con:

```bash
python manage.py test
```

| Test | Qué verifica |
|---|---|
| `test_no_permite_reservas_duplicadas` | `full_clean()` lanza `ValidationError` ante una reserva duplicada (misma pista, fecha y bloque). |
| `test_no_permite_reservar_en_el_pasado` | `full_clean()` lanza `ValidationError` para una fecha pasada. |
| `test_reservar_consume_credito_de_usuario_y_bono` | Al reservar, `Usuario.creditos` baja 1 y `Bono.creditos_restantes` baja 1. |
| `test_anular_reserva_devuelve_credito_de_usuario_y_bono` | Al anular, `Usuario.creditos` sube 1 y `Bono.creditos_restantes` sube 1. |
| `test_usuario_normal_no_puede_entrar_al_panel_admin` | Un usuario sin `is_staff` es redirigido a la home al intentar acceder al panel. |
| `test_usuario_staff_puede_entrar_al_panel_admin` | Un usuario con `is_staff` obtiene HTTP 200 en el panel. |
| `test_anular_reserva_no_acepta_get` | `GET /anular/<id>/` devuelve HTTP 405. |
| `test_acciones_admin_destructivas_no_aceptan_get` | `GET` sobre `toggle_pista` y `eliminar_reserva_admin` devuelve HTTP 405 sin modificar datos. |