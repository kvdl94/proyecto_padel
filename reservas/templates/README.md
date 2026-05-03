# Templates

Esta carpeta contiene las plantillas HTML de la app `reservas`.

Las plantillas usan Django Templates y Bootstrap 5.

## Base

- `reservas/base.html`: estructura comun, barra de navegacion, mensajes y carga de Bootstrap.

## Pantallas publicas y de usuario

- `reservas/home.html`: muestra pistas disponibles, proximas reservas e historial.
- `reservas/login.html`: inicio de sesion.
- `reservas/registro.html`: registro de usuario.
- `reservas/reservar_pista.html`: formulario para reservar una pista.
- `reservas/comprar_bono.html`: tienda de bonos.

## Recuperacion de contrasena

- `reservas/password_reset.html`: solicita el email.
- `reservas/password_reset_done.html`: confirma que el email se ha generado.
- `reservas/password_reset_confirm.html`: permite escribir nueva contrasena.
- `reservas/password_reset_complete.html`: confirma el cambio.
- `reservas/password_reset_email.html`: cuerpo del email.
- `reservas/password_reset_subject.txt`: asunto del email.

En desarrollo, el email aparece en la consola del servidor.

## Panel admin personalizado

- `reservas/panel_admin.html`: dashboard del panel.
- `reservas/gestionar_pistas.html`: listado y acciones de pistas.
- `reservas/form_pista.html`: formulario de crear/editar pista.
- `reservas/gestionar_usuarios.html`: listado de usuarios y ajuste de creditos.
- `reservas/gestionar_bonos.html`: historial de bonos y creditos restantes.
- `reservas/gestionar_reservas.html`: listado de reservas y eliminacion admin.
