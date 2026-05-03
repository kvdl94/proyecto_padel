# WANDA Padel Club — Sistema de Reservas

Aplicación web completa desarrollada con **Django 6** para la gestión integral de reservas de pistas de pádel. El sistema cubre desde el registro de usuarios hasta un panel de administración personalizado, incluyendo un sistema de créditos, validaciones automáticas y notificaciones en tiempo real.

---

## Índice

1. [Tecnologías](#tecnologías)
2. [Funcionalidades](#funcionalidades)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Instalación](#instalación)
5. [Usuarios de prueba](#usuarios-de-prueba)
6. [Autores](#autores)

---

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.12 · Django 6.0.1 |
| Base de datos | SQLite3 (incluida con datos de prueba) |
| Frontend | HTML5 · Bootstrap 5 · Bootstrap Icons |
| Autenticación | Django Auth (modelo de usuario personalizado) |
| Email | Django Console Backend (desarrollo) |

---

## Funcionalidades

El proyecto implementa los 14 requisitos funcionales establecidos:

| # | Funcionalidad |
|---|--------------|
| 1 | Aplicación completa desarrollada en Django |
| 2 | Autenticación: registro, inicio de sesión y **recuperación de contraseña** |
| 3 | Roles diferenciados: usuario normal y administrador (`is_staff`) |
| 4 | Gestión de pistas desde la app: crear, editar, activar y desactivar (solo admin) |
| 5 | Reservas con selección de pista, fecha y franja horaria; cancelación con devolución de crédito |
| 6 | Control de disponibilidad: bloqueo de reservas duplicadas en la misma franja |
| 7 | Sistema de bonos y créditos: compra, consumo al reservar y devolución al anular |
| 8 | Historial de reservas ordenado por fecha y horario, accesible desde la home |
| 9 | Panel de administración personalizado: gestión de usuarios, créditos, pistas y reservas |
| 10 | Validación automática: no se permiten reservas en fechas u horas pasadas |
| 11 | Notificaciones en pantalla (éxito/error) mediante `django.contrib.messages` |
| 12 | Interfaz responsive con Django Templates y Bootstrap 5 |
| 13 | Modelos de base de datos: `Usuario`, `Pista` y `Reserva` con migraciones |
| 14 | Documentación completa: instalación, migraciones, usuarios de prueba y `requirements.txt` |

---

## Estructura del proyecto

```
proyecto_padel/
├── core/                   # Configuración del proyecto Django
│   ├── settings.py         # Ajustes globales (BD, auth, email, zona horaria)
│   └── urls.py             # Enrutamiento principal
├── reservas/               # Aplicación principal
│   ├── models.py           # Modelos: Usuario, Pista, Reserva
│   ├── views.py            # Lógica de negocio y vistas
│   ├── forms.py            # Formularios: RegistroForm, PistaForm
│   ├── admin.py            # Registro en el panel Django Admin
│   ├── migrations/         # Historial de migraciones de la BD
│   └── templates/reservas/ # Plantillas HTML
├── db.sqlite3              # Base de datos con datos de prueba
├── requirements.txt        # Dependencias del proyecto
└── README.md
```

---

## Instalación

### Requisitos previos

- Python 3.10 o superior
- Git

### Pasos

**1. Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd proyecto_padel
```

**2. Crear y activar el entorno virtual**

```bash
# Crear entorno virtual
python -m venv env

# Activar en Windows
.\env\Scripts\activate

# Activar en macOS / Linux
source env/bin/activate
```

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Aplicar migraciones**

```bash
python manage.py migrate
```

> La base de datos `db.sqlite3` ya está incluida con datos de prueba. Este paso solo es necesario si se parte de cero.

**5. Iniciar el servidor de desarrollo**

```bash
python manage.py runserver
```

Abrir en el navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Usuarios de prueba

La base de datos incluida contiene los siguientes perfiles listos para usar:

### Administrador

| Campo | Valor |
|-------|-------|
| URL | http://127.0.0.1:8000/panel-admin/ |
| Usuario | `alumno` |
| Contraseña | `alumno` |
| Permisos | Acceso total: gestión de pistas, usuarios, créditos y reservas |

### Usuario estándar

| Campo | Valor |
|-------|-------|
| URL | http://127.0.0.1:8000 |
| Usuario | `alumno1` |
| Contraseña | `alumno1` |
| Permisos | Reservar pistas, comprar bonos, consultar historial |

---

## Autores

Proyecto desarrollado por **Kevin, David, Perdices y Rodrigo** como parte de un trabajo de desarrollo web con Django.
