WANDA Padel Club - Sistema de Reservas 🎾
Este proyecto es una aplicación web desarrollada con Django para la gestión de reservas de pistas de pádel, ofreciendo una experiencia premium y eficiente para los usuarios.

🚀 Funcionalidades Principales (Requisitos)
Gestión de Usuarios (Req. 16): Sistema completo de registro e inicio de sesión.

Catálogo de Pistas (Req. 18): Visualización dinámica de pistas (Espartales, El Val, etc.) con imágenes y estado de disponibilidad.

Lógica de Reservas (Req. 20): Sistema que impide reservas duplicadas en la misma pista, fecha y horario.

Sistema de Créditos (Req. 21): Los usuarios consumen créditos al reservar y pueden recargarlos mediante una tienda de bonos con descuentos del 10% y 20%.

Panel de Usuario (Req. 19): Historial de reservas confirmadas visible en la página principal para cada usuario.

🛠️ Tecnologías Utilizadas
Backend: Python 3.x y Django 5.x.

Base de Datos: SQLite3 (archivo db.sqlite3).

Frontend: HTML5, CSS3 y Bootstrap 5 para un diseño responsivo y moderno.

Iconografía: Bootstrap Icons.

📂 Estructura del Proyecto
/core: Configuración principal de Django (settings, urls).

/reservas: Aplicación principal que contiene los modelos de Pistas, Usuarios y Reservas.

/templates: Archivos HTML organizados por funcionalidad (base, home, login, etc.).

👤 Autor
Kevin - Desarrollador del proyecto.
DAVID - Desarrollador del proyecto.
PERDICES - Desarrollador del proyecto.
RODRIGO - Desarrollador del proyecto.

🛠️ Guía de Instalación
Sigue estos pasos para configurar el proyecto en tu entorno local:

1. Clonar o descargar el proyecto
Descarga la carpeta del proyecto y ábrela con VS Code.

2. Crear y activar el entorno virtual
Es importante para que las librerías no choquen con otras versiones de tu PC:

Abrir terminal en VS Code y escribir:

Bash

python -m venv env
Activar el entorno:

En Windows: .\env\Scripts\activate

En Mac/Linux: source env/bin/activate

3. Instalar Django
Con el entorno activo (verás que pone (env) en la terminal), instala la versión necesaria:

Bash

pip install django
4. Preparar la Base de Datos
Como ya tienes el archivo db.sqlite3, solo asegúrate de que las tablas estén al día:

Bash

python manage.py migrate
5. Crear un Administrador (Opcional)
Si el profesor quiere entrar al panel /admin, puede crear su propia cuenta:

Bash

python manage.py createsuperuser
6. Ejecutar el servidor
Arranca la aplicación con este comando:

Bash

python manage.py runserver
Luego, abre tu navegador en: http://127.0.0.1:8000/

👥 Usuarios de Prueba 
Para facilitar la corrección del proyecto, se han configurado los siguientes perfiles con roles diferenciados:

1. Administrador (Gestión de pistas y bonos)
Usuario: alumno

Contraseña: alumno 

Acceso: Puede entrar en /admin para activar/desactivar pistas y ver todas las reservas.

2. Usuario Cliente (Reserva y anulación)
Usuario: alumno1

Contraseña: alumno1

Acceso: Web principal. Permite probar la compra de bonos, reserva de pistas y el historial.
