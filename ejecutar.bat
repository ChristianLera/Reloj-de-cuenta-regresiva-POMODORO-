@echo off
title Pomodoro Timer Pro - Christian Lera
color 0A

echo ========================================
echo    🍅 POMODORO TIMER PRO - Christian Lera
echo ========================================
echo.

echo [1/3] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado.
    echo Por favor, instala Python 3.6 o superior desde python.org
    pause
    exit /b 1
)
echo OK - Python encontrado
echo.

echo [2/3] Instalando dependencias...
pip install plyer >nul 2>&1
if errorlevel 1 (
    echo ADVERTENCIA: No se pudo instalar plyer
    echo Intentando con permisos de usuario...
    pip install --user plyer >nul 2>&1
)
echo OK - Dependencias listas
echo.

echo [3/3] Iniciando Pomodoro Timer...
echo.
echo ========================================
echo    ¡La aplicacion se esta abriendo!
echo    No cierres esta ventana mientras
echo    estes usando el temporizador.
echo ========================================
echo.

python RelojPOMODORO.py

echo.
echo ========================================
echo    La aplicacion se ha cerrado.
echo ========================================
pause