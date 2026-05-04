@echo off
setlocal

cd /d "%~dp0.."

echo ========================================
echo  WANDA Padel Club - Arranque automatico
echo ========================================
echo.

if not exist "manage.py" (
    echo ERROR: No se ha encontrado manage.py en la carpeta raiz del proyecto.
    pause
    exit /b 1
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        echo ERROR: No se ha encontrado Python instalado.
        echo Instala Python y vuelve a ejecutar este script.
        pause
        exit /b 1
    )
)

if not exist "env\Scripts\python.exe" (
    echo Creando entorno virtual...
    %PYTHON_CMD% -m venv env
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
) else (
    echo Entorno virtual encontrado.
)

echo.
echo Instalando dependencias...
"env\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo.
echo Aplicando migraciones...
"env\Scripts\python.exe" manage.py migrate
if errorlevel 1 (
    echo ERROR: No se pudieron aplicar las migraciones.
    pause
    exit /b 1
)

echo.
echo Servidor iniciado. Para pararlo, pulsa Ctrl + C en esta ventana.
echo.
start "" cmd /c "timeout /t 3 /nobreak >nul && start "" http://127.0.0.1:8000/"
"env\Scripts\python.exe" manage.py runserver

endlocal
