# Carpeta `core`

Esta carpeta contiene la configuracion principal del proyecto Django.

## Archivos principales

- `settings.py`: ajustes globales del proyecto.
- `urls.py`: rutas principales de la aplicacion.
- `wsgi.py` y `asgi.py`: puntos de entrada del servidor.

## Configuracion destacada

- `INSTALLED_APPS` incluye la app principal `reservas`.
- `AUTH_USER_MODEL = 'reservas.Usuario'` activa el modelo de usuario personalizado.
- `LOGIN_URL = 'login'` define la ruta de inicio de sesion.
- `LOGIN_REDIRECT_URL = 'home'` envia al usuario a la home tras iniciar sesion.
- `LANGUAGE_CODE = 'es-es'` y `TIME_ZONE = 'Europe/Madrid'`.
- `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` muestra los emails en consola durante desarrollo.

## Rutas principales

`urls.py` conecta:

- Home, registro, login y logout.
- Recuperacion de contrasena.
- Compra de bonos.
- Reserva y anulacion de reservas.
- Panel admin personalizado.
- Admin nativo de Django.

El panel personalizado empieza en:

```text
/panel-admin/
```

El admin nativo de Django esta en:

```text
/admin/
```
