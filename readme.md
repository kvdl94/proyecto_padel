# WANDA Padel Club - Sistema de Reservas 🎾

Este proyecto es una aplicación web desarrollada con Django para la gestión de reservas de pistas de pádel, ofreciendo una experiencia premium y eficiente para los usuarios.

## 🚀 Funcionalidades Principales (Requisitos)

- **Gestión de Usuarios (Req. 16):** Sistema completo de registro e inicio de sesión.
- **Catálogo de Pistas (Req. 18):** Visualización dinámica de pistas (Espartales, El Val, etc.) con imágenes y estado de disponibilidad.
- **Lógica de Reservas (Req. 20):** Sistema que impide reservas duplicadas en la misma pista, fecha y horario.
- **Sistema de Créditos (Req. 21):** Los usuarios consumen créditos al reservar y pueden recargarlos mediante una tienda de bonos con descuentos del 10% y 20%.
- **Panel de Usuario (Req. 19):** Historial de reservas confirmadas visible en la página principal para cada usuario.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.12 y Django 6.0.1.
- **Base de Datos:** SQLite3 (archivo `db.sqlite3` incluido con datos de prueba).
- **Frontend:** HTML5, CSS3 y Bootstrap 5 para un diseño responsivo.
- **Iconografía:** Bootstrap Icons.

## 📂 Estructura del Proyecto

- `/core`: Configuración principal de Django (settings, urls).
- `/reservas`: Aplicación principal que contiene los modelos de Pistas, Usuarios y Reservas.
- `/templates`: Archivos HTML organizados por funcionalidad.

## 👤 Autores

- Kevin, David, Perdices y Rodrigo.

---

## 🛠️ Guía de Instalación y Replicabilidad

Sigue estos pasos para configurar el proyecto en cualquier entorno local (Windows):

### 1. Descargar el proyecto

Descarga la carpeta del proyecto desde el repositorio de GitHub y ábrela con Visual Studio Code.

### 2. Crear y activar el entorno virtual

Es fundamental para aislar las dependencias y asegurar que el proyecto funcione correctamente:

```bash
# Crear entorno virtual
python -m venv env

# Activar en Windows
.\env\Scripts\activate
3. Instalar Dependencias
Con el entorno activo, instala la versión exacta de Django y las librerías necesarias mediante el archivo de requerimientos:

Bash
pip install -r requirements.txt
4. Ejecutar el servidor
Lanza la aplicación localmente con el siguiente comando:

Bash
python manage.py runserver
Una vez iniciado, abre el navegador en: http://127.0.0.1:8000/

👥 Usuarios de Prueba y Acceso Administrativo
Para facilitar la evaluación y corrección del proyecto, se han configurado los siguientes perfiles:

🔐 Panel de Administración (Gestión Total)
URL de acceso: http://127.0.0.1:8000/admin

Usuario: alumno

Contraseña: alumno

Uso: Permite gestionar las pistas existentes, administrar usuarios y supervisar todas las reservas del sistema.

👤 Usuario Cliente (Pruebas de Reserva)
URL de acceso: Página principal / Login

Usuario: alumno1

Contraseña: alumno1

Uso: Permite probar el flujo completo de reserva, la compra de bonos de crédito y consultar el historial de usuario.
```
