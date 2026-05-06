# 🍅 Pomodoro Timer Pro

Aplicación profesional de técnica Pomodoro para mejorar la productividad, con gestión de tareas, estadísticas y recordatorios de salud.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Mac-lightgrey.svg)

## ✨ Características

- ⏱️ **Temporizador Pomodoro** con fases de trabajo/descanso
- 📊 **Estadísticas de productividad** (diarias y semanales)
- 📝 **Gestor de tareas integrado**
- 🔔 **Notificaciones del sistema** al finalizar cada fase
- 🧘 **Recordatorios de postura** cada X pomodoros
- ⚙️ **Tiempos configurables** (trabajo, descanso corto, descanso largo)
- 💾 **Persistencia de datos** (configuración, estadísticas, tareas)
- 🎨 **Interfaz moderna** con barra de progreso visual

## 📋 Requisitos

- Python 3.6 o superior
- Pip (gestor de paquetes de Python)

## 🚀 Instalación

### Windows (Ejecución automática)
1. Descarga el proyecto
2. Ejecuta `ejecutar.bat` (instalará dependencias automáticamente)

### Windows (PowerShell)
```powershell
.\ejecutar.ps1
```

### Manual (Cualquier SO)
```bash
# Instalar dependencias
pip install plyer

# Ejecutar la aplicación
python RelojPOMODORO.py
```

## 🎮 Cómo usar

1. **Iniciar** - Presiona ▶ INICIAR para comenzar el temporizador
2. **Pausar** - ⏸ PAUSAR detiene el conteo
3. **Resetear** - 🔄 RESET vuelve al inicio de la fase actual
4. **Saltar fase** - ⏩ SIGUIENTE cambia manualmente a la siguiente fase

### Fases del Pomodoro
- 🔴 **Trabajo** - 25 minutos (por defecto)
- 🟡 **Descanso corto** - 5 minutos (por defecto)
- 🟢 **Descanso largo** - 15 minutos (cada 4 pomodoros)

## ⚙️ Configuración

Puedes personalizar:
- Tiempo de trabajo (1-60 min)
- Tiempo de descanso corto (1-30 min)
- Tiempo de descanso largo (1-45 min)
- Frecuencia de recordatorios de postura (cada X pomodoros)

## 📁 Estructura de archivos

```
Pomodoro-Timer/
├── RelojPOMODORO.py          # Aplicación principal
├── ejecutar.bat               # Lanzador para Windows (CMD)
├── ejecutar.ps1               # Lanzador para PowerShell
├── README.md                  # Este archivo
├── pomodoro_config.json       # Configuración (se crea automáticamente)
├── pomodoro_stats.json        # Estadísticas (se crea automáticamente)
└── pomodoro_tasks.json        # Tareas guardadas (se crea automáticamente)
```

## 🛠️ Tecnologías utilizadas

- **Tkinter** - Interfaz gráfica
- **Plyer** - Notificaciones del sistema
- **JSON** - Persistencia de datos
- **Threading** - Manejo de notificaciones

## 📊 Funcionalidades avanzadas

### Estadísticas
- Seguimiento diario de pomodoros completados
- Historial semanal
- Visualización de últimos 7 días

### Gestor de tareas
- Añadir/eliminar tareas
- Marcar tareas como completadas
- Notificaciones al completar tareas

### Salud
- Recordatorios de postura configurables
- Consejos ergonómicos
- Alertas visuales y sonoras

## 🐛 Solución de problemas

### Error: "No module named plyer"
```bash
pip install plyer
```

### Error: "TclError" en Linux
```bash
sudo apt-get install python3-tk
```

### Las notificaciones no funcionan en Linux
```bash
pip install plyer
sudo apt-get install libnotify-bin
```

## 📝 Notas para desarrolladores

- El código está completamente documentado
- Los datos se guardan automáticamente al cerrar
- Los archivos JSON se crean en el mismo directorio

## 👨‍💻 Autor

**Christian Lera**

## 📄 Licencia

MIT License - Libre para uso personal y comercial.

---

⭐ Si te gusta este proyecto, ¡considera darle una estrella en GitHub!
