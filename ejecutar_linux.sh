#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "========================================"
echo " WANDA Padel Club - Arranque automatico"
echo "========================================"
echo

if [ ! -f "manage.py" ]; then
    echo "ERROR: Este script debe estar en la misma carpeta que manage.py."
    exit 1
fi

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "ERROR: No se ha encontrado Python instalado."
    echo "Instala Python y vuelve a ejecutar este script."
    exit 1
fi

if [ ! -f "env/bin/python" ]; then
    echo "Creando entorno virtual..."
    "$PYTHON_CMD" -m venv env
else
    echo "Entorno virtual encontrado."
fi

echo
echo "Instalando dependencias..."
"env/bin/python" -m pip install -r requirements.txt

echo
echo "Aplicando migraciones..."
"env/bin/python" manage.py migrate

echo
echo "Servidor iniciado. Para pararlo, pulsa Ctrl + C en esta ventana."
echo
if command -v xdg-open >/dev/null 2>&1; then
    (sleep 3 && xdg-open "http://127.0.0.1:8000/" >/dev/null 2>&1) &
else
    echo "Abre manualmente: http://127.0.0.1:8000/"
fi
"env/bin/python" manage.py runserver
