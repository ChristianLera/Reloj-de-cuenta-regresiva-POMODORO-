# Pomodoro Timer Pro - Launch Script for PowerShell
# Author: Christian Lera

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   🍅 POMODORO TIMER PRO - Christian Lera" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/3] Verificando Python..." -ForegroundColor White
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK - $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python no esta instalado." -ForegroundColor Red
    Write-Host "Por favor, instala Python 3.6 o superior desde python.org" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}
Write-Host ""

# Install dependencies
Write-Host "[2/3] Instalando dependencias..." -ForegroundColor White
try {
    $result = pip install plyer 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK - Dependencias listas" -ForegroundColor Green
    } else {
        Write-Host "ADVERTENCIA: Intentando con permisos de usuario..." -ForegroundColor Yellow
        pip install --user plyer 2>&1 | Out-Null
        Write-Host "OK - Dependencias instaladas" -ForegroundColor Green
    }
} catch {
    Write-Host "ADVERTENCIA: No se pudo verificar la instalacion de plyer" -ForegroundColor Yellow
}
Write-Host ""

# Launch the application
Write-Host "[3/3] Iniciando Pomodoro Timer..." -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ¡La aplicacion se esta abriendo!" -ForegroundColor Green
Write-Host "   No cierres esta ventana mientras" -ForegroundColor Green
Write-Host "   estes usando el temporizador." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python RelojPOMODORO.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   La aplicacion se ha cerrado." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Presiona Enter para salir"