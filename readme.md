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

Sigue estos pasos para configurar el proyecto en tu entorno local (Windows):

### 1. Descargar el proyecto

Descarga la carpeta del proyecto desde GitHub y ábrela con VS Code.

### 2. Crear y activar el entorno virtual

Es necesario para aislar las dependencias del proyecto:

```bash
# Crear entorno
python -m venv env

# Activar en Windows
.\env\Scripts\activate
```
