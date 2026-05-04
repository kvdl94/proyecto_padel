# WANDA Padel Club - Sistema de reservas

Aplicación web desarrollada con Django para gestionar reservas de pistas de pádel. Incluye autenticación, recuperación de contraseña, roles de usuario, compra y consumo de bonos, historial de reservas, validaciones automáticas y panel de administración personalizado.

## Tecnologías

| Capa | Tecnología |
| --- | --- |
| Backend | Python 3.12, Django 6.0.1 |
| Base de datos | SQLite3 |
| Frontend | Django Templates, HTML, Bootstrap 5 |
| Autenticación | Django Auth con modelo de usuario personalizado |
| Email | Console Email Backend para desarrollo |

## Funcionalidades principales

- Registro, inicio de sesión, cierre de sesión y recuperación de contraseña.
- Roles diferenciados con `is_staff`: usuario normal y administrador.
- Gestión de pistas desde panel propio: crear, editar, activar y desactivar.
- Sistema de reservas por pista, fecha y franja horaria.
- Control de disponibilidad con validación de modelo y restricción única en base de datos.
- Validación para impedir reservas en horarios pasados.
- Compra de bonos y consumo de créditos al reservar.
- Devolución de crédito al anular reservas futuras.
- Historial de compras de bonos con créditos totales, restantes y consumidos.
- Home con próximas reservas separadas del historial de reservas finalizadas.
- Panel de administración personalizado para usuarios, bonos, pistas y reservas.
- Notificaciones en pantalla mediante `django.contrib.messages`.
- Tests básicos para reservas, créditos y permisos.

## Modelos principales

- `Usuario`: usuario personalizado basado en `AbstractUser`, con saldo de `creditos`.
- `Bono`: registra compras o ajustes de créditos, con `creditos`, `creditos_restantes`, `precio` y `fecha_compra`.
- `Pista`: pista de pádel con nombre, imagen opcional y estado activo/inactivo.
- `Reserva`: reserva asociada a usuario, pista, fecha y bloque horario.

## Estructura

```text
proyecto_padel/
├── core/
│   ├── README.md
│   ├── settings.py
│   └── urls.py
├── reservas/
│   ├── README.md
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── migrations/
│   │   └── README.md
│   └── templates/
│       ├── README.md
│       └── reservas/
├── scripts/
│   ├── ejecutar_linux.sh
│   └── ejecutar_windows.bat
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## Ejecución automática

### Windows

Ejecuta:

```bat
scripts\ejecutar_windows.bat
```

El script crea el entorno virtual si no existe, instala dependencias, aplica migraciones y arranca el servidor.

### Linux

La primera vez:

```bash
chmod +x scripts/ejecutar_linux.sh
```

Después:

```bash
./scripts/ejecutar_linux.sh
```

## Ejecución manual

```bash
python -m venv env
```

En Windows:

```bash
.\env\Scripts\activate
```

En Linux/macOS:

```bash
source env/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Aplicar migraciones:

```bash
python manage.py migrate
```

Arrancar servidor:

```bash
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/
```

## Usuarios de prueba

### Administrador

| Campo | Valor |
| --- | --- |
| Usuario | `alumno` |
| Contraseña | `alumno` |
| Panel personalizado | `http://127.0.0.1:8000/panel-admin/` |
| Admin Django | `http://127.0.0.1:8000/admin/` |

### Usuario normal

| Campo | Valor |
| --- | --- |
| Usuario | `alumno1` |
| Contraseña | `alumno1` |
| URL | `http://127.0.0.1:8000/` |

## Recuperación de contraseña

La recuperación de contraseña está configurada para desarrollo con:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Esto significa que Django no envía un email real. El enlace de recuperación aparece en la terminal donde se está ejecutando `python manage.py runserver`.

Flujo de prueba:

1. Entrar en `http://127.0.0.1:8000/login/`.
2. Pulsar el enlace de recuperación de contraseña.
3. Introducir el email de un usuario registrado.
4. Copiar desde la terminal el enlace generado.
5. Abrirlo en el navegador y cambiar la contraseña.

## Tests

Ejecutar:

```bash
python manage.py test
```

Los tests cubren:

- Reserva duplicada.
- Reserva en el pasado.
- Consumo de crédito al reservar.
- Devolución de crédito al anular.
- Bloqueo del panel admin para usuarios normales.
- Acceso al panel admin para usuarios `is_staff`.

## Autores

Proyecto desarrollado por Kevin, David, Perdices y Rodrigo.
