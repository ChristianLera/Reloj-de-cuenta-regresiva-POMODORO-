"""
POMODORO TIMER - Professional Time Management Tool
Author: Custom Development
Version: 2.1 (Corregido)
Requires: Python 3.6+, tkinter, plyer
"""

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, simpledialog
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict
from plyer import notification
import threading
import time
import sys

# ==================== CONFIGURACIÓN INICIAL ====================
CONFIG_FILE = "pomodoro_config.json"
STATS_FILE = "pomodoro_stats.json"
TASKS_FILE = "pomodoro_tasks.json"

# Tiempos predeterminados (en segundos)
DEFAULT_WORK_TIME = 25 * 60
DEFAULT_SHORT_BREAK = 5 * 60
DEFAULT_LONG_BREAK = 15 * 60

# ==================== CLASE PRINCIPAL ====================
class PomodoroTimer:
    """
    Clase principal que maneja toda la lógica del temporizador Pomodoro.
    Implementa técnicas de productividad con interfaz gráfica profesional.
    """
    
    def __init__(self, root):
        """
        Inicializa la aplicación Pomodoro.
        
        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.root.title("🍅 Pomodoro Timer Pro - Técnica de Productividad")
        self.root.geometry("650x1000")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')
        
        # Variables de estado del temporizador
        self.current_time = DEFAULT_WORK_TIME
        self.is_running = False
        self.current_phase = "work"
        self.pomodoros_completed = 0
        self.current_session = 1
        
        # Cargar configuraciones y datos guardados
        self.load_config()
        self.load_stats()
        self.load_tasks()
        
        # Configurar la interfaz
        self.setup_ui()
        
        # Iniciar actualización del reloj
        self.update_clock()
        
        # Configurar manejo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # ==================== CARGA Y GUARDADO DE DATOS ====================
    def load_config(self):
        """Carga la configuración guardada o usa valores por defecto."""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.work_time = config.get('work_time', DEFAULT_WORK_TIME)
                    self.short_break_time = config.get('short_break_time', DEFAULT_SHORT_BREAK)
                    self.long_break_time = config.get('long_break_time', DEFAULT_LONG_BREAK)
                    self.posture_reminder = config.get('posture_reminder', 4)
            except:
                self.set_default_times()
        else:
            self.set_default_times()
    
    def set_default_times(self):
        """Establece tiempos por defecto."""
        self.work_time = DEFAULT_WORK_TIME
        self.short_break_time = DEFAULT_SHORT_BREAK
        self.long_break_time = DEFAULT_LONG_BREAK
        self.posture_reminder = 4
    
    def save_config(self):
        """Guarda la configuración actual en archivo JSON."""
        config = {
            'work_time': self.work_time,
            'short_break_time': self.short_break_time,
            'long_break_time': self.long_break_time,
            'posture_reminder': self.posture_reminder
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    
    def load_stats(self):
        """Carga estadísticas históricas."""
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    self.stats = json.load(f)
            except:
                self.stats = {'daily': {}, 'weekly': {}}
        else:
            self.stats = {'daily': {}, 'weekly': {}}
    
    def save_stats(self):
        """Guarda estadísticas actualizadas."""
        today = datetime.now().strftime("%Y-%m-%d")
        week = datetime.now().strftime("%Y-W%W")
        
        if today not in self.stats['daily']:
            self.stats['daily'][today] = 0
        self.stats['daily'][today] = self.pomodoros_completed
        
        if week not in self.stats['weekly']:
            self.stats['weekly'][week] = 0
        self.stats['weekly'][week] = self.pomodoros_completed
        
        with open(STATS_FILE, 'w') as f:
            json.dump(self.stats, f, indent=4)
    
    def load_tasks(self):
        """Carga la lista de tareas pendientes."""
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Guarda la lista de tareas."""
        with open(TASKS_FILE, 'w') as f:
            json.dump(self.tasks, f, indent=4)
    
    # ==================== INTERFAZ DE USUARIO ====================
    def setup_ui(self):
        """Configura todos los elementos visuales de la aplicación."""
        
        # Estilo personalizado para la barra de progreso
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("green.Horizontal.TProgressbar", 
                       background='#27AE60',
                       troughcolor='#34495E',
                       bordercolor='#2C3E50',
                       lightcolor='#27AE60',
                       darkcolor='#27AE60')
        
        # === Frame principal ===
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # === Título ===
        title_label = tk.Label(
            main_frame, 
            text="🍅 TÉCNICA POMODORO", 
            font=('Arial', 20, 'bold'),
            fg='#ECF0F1',
            bg='#2C3E50'
        )
        title_label.pack(pady=(0, 20))
        
        # === Contador de Pomodoros ===
        self.pomodoro_counter_label = tk.Label(
            main_frame,
            text=f"📊 Pomodoros hoy: {self.pomodoros_completed}",
            font=('Arial', 12),
            fg='#3498DB',
            bg='#2C3E50'
        )
        self.pomodoro_counter_label.pack()
        
        # === Fase actual ===
        self.phase_label = tk.Label(
            main_frame,
            text="🔴 TIEMPO DE TRABAJO",
            font=('Arial', 14, 'bold'),
            fg='#E74C3C',
            bg='#2C3E50'
        )
        self.phase_label.pack(pady=(10, 5))
        
        # === Reloj principal ===
        self.clock_label = tk.Label(
            main_frame,
            text=self.format_time(self.current_time),
            font=('Courier', 52, 'bold'),
            fg='#ECF0F1',
            bg='#2C3E50'
        )
        self.clock_label.pack(pady=20)
        
        # === Barra de progreso ===
        self.progress = ttk.Progressbar(
            main_frame,
            length=400,
            mode='determinate',
            style='green.Horizontal.TProgressbar'
        )
        self.progress.pack(pady=10)
        
        # === Frame de botones de control ===
        control_frame = tk.Frame(main_frame, bg='#2C3E50')
        control_frame.pack(pady=20)
        
        # Botones principales
        self.start_button = tk.Button(
            control_frame,
            text="▶ INICIAR",
            command=self.start_timer,
            bg='#27AE60',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = tk.Button(
            control_frame,
            text="⏸ PAUSAR",
            command=self.pause_timer,
            bg='#F39C12',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8,
            state=tk.DISABLED,
            cursor='hand2'
        )
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = tk.Button(
            control_frame,
            text="🔄 RESET",
            command=self.reset_timer,
            bg='#E74C3C',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.reset_button.grid(row=0, column=2, padx=5)
        
        self.skip_button = tk.Button(
            control_frame,
            text="⏩ SIGUIENTE",
            command=self.skip_phase,
            bg='#3498DB',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.skip_button.grid(row=0, column=3, padx=5)
        
        # === Botones de funcionalidades extra ===
        extra_frame = tk.Frame(main_frame, bg='#2C3E50')
        extra_frame.pack(pady=10)
        
        tk.Button(
            extra_frame,
            text="⚙️ Configurar Tiempos",
            command=self.open_settings,
            bg='#34495E',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        ).grid(row=0, column=0, padx=5)
        
        tk.Button(
            extra_frame,
            text="📈 Estadísticas",
            command=self.show_stats,
            bg='#34495E',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        ).grid(row=0, column=1, padx=5)
        
        tk.Button(
            extra_frame,
            text="📝 Tareas Pendientes",
            command=self.open_task_manager,
            bg='#34495E',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        ).grid(row=0, column=2, padx=5)
        
        tk.Button(
            extra_frame,
            text="🧘 Recordatorio Postura",
            command=self.manual_posture_reminder,
            bg='#34495E',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        ).grid(row=0, column=3, padx=5)
        
        # === Lista de tareas rápida ===
        tasks_frame = tk.LabelFrame(main_frame, text="📋 Tareas Rápidas", 
                                   bg='#2C3E50', fg='white', 
                                   font=('Arial', 10, 'bold'))
        tasks_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Listbox para tareas
        self.tasks_listbox = tk.Listbox(
            tasks_frame,
            height=6,
            bg='#34495E',
            fg='white',
            selectmode=tk.SINGLE,
            font=('Arial', 10)
        )
        self.tasks_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de botones de tareas
        task_buttons_frame = tk.Frame(tasks_frame, bg='#2C3E50')
        task_buttons_frame.pack(pady=(0, 10))
        
        tk.Button(
            task_buttons_frame,
            text="➕ Agregar Tarea",
            command=self.add_task,
            bg='#27AE60',
            fg='white',
            font=('Arial', 9),
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            task_buttons_frame,
            text="✓ Completar Tarea",
            command=self.complete_task,
            bg='#3498DB',
            fg='white',
            font=('Arial', 9),
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            task_buttons_frame,
            text="🗑 Eliminar Tarea",
            command=self.delete_task,
            bg='#E74C3C',
            fg='white',
            font=('Arial', 9),
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        self.refresh_tasks_list()
    
    # ==================== FUNCIONES DEL TEMPORIZADOR ====================
    def format_time(self, seconds):
        """Convierte segundos a formato MM:SS."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def update_clock(self):
        """Actualiza el reloj cada segundo cuando está activo."""
        if self.is_running and self.current_time > 0:
            self.current_time -= 1
            self.clock_label.config(text=self.format_time(self.current_time))
            
            # Actualizar barra de progreso
            total_time = self.get_current_phase_total_time()
            if total_time > 0:
                progress_percentage = ((total_time - self.current_time) / total_time) * 100
                self.progress['value'] = progress_percentage
            
            if self.current_time == 0:
                self.timer_complete()
        
        self.root.after(1000, self.update_clock)
    
    def get_current_phase_total_time(self):
        """Retorna el tiempo total de la fase actual."""
        if self.current_phase == "work":
            return self.work_time
        elif self.current_phase == "short_break":
            return self.short_break_time
        else:
            return self.long_break_time
    
    def start_timer(self):
        """Inicia el temporizador."""
        if not self.is_running and self.current_time > 0:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
    
    def pause_timer(self):
        """Pausa el temporizador."""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
    
    def reset_timer(self):
        """Resetea el temporizador al inicio de la fase actual."""
        self.is_running = False
        self.reset_phase_time()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.progress['value'] = 0
    
    def reset_phase_time(self):
        """Restablece el tiempo según la fase actual."""
        if self.current_phase == "work":
            self.current_time = self.work_time
        elif self.current_phase == "short_break":
            self.current_time = self.short_break_time
        else:
            self.current_time = self.long_break_time
        self.clock_label.config(text=self.format_time(self.current_time))
    
    def skip_phase(self):
        """Salta manualmente a la siguiente fase."""
        self.is_running = False
        self.change_phase()
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
    
    def timer_complete(self):
        """Maneja la finalización del temporizador."""
        self.is_running = False
        
        # Reproducir sonido y notificación
        self.play_sound()
        self.send_notification()
        
        # Si completó un trabajo, incrementar contador
        if self.current_phase == "work":
            self.pomodoros_completed += 1
            self.update_pomodoro_counter()
            self.save_stats()
            
            # Verificar recordatorio de postura
            if self.pomodoros_completed % self.posture_reminder == 0:
                self.show_posture_reminder()
        
        # Cambiar a la siguiente fase
        self.change_phase()
    
    def change_phase(self):
        """Cambia entre las diferentes fases del Pomodoro."""
        if self.current_phase == "work":
            # Decidir si es descanso corto o largo
            if self.current_session % 4 == 0:
                self.current_phase = "long_break"
                self.current_time = self.long_break_time
                self.phase_label.config(text="🟢 DESCANSO LARGO (15 min)", fg='#2ECC71')
                self.current_session = 1
            else:
                self.current_phase = "short_break"
                self.current_time = self.short_break_time
                self.phase_label.config(text="🟡 DESCANSO CORTO (5 min)", fg='#F1C40F')
                self.current_session += 1
        else:
            # Volver a trabajo
            self.current_phase = "work"
            self.current_time = self.work_time
            self.phase_label.config(text="🔴 TIEMPO DE TRABAJO", fg='#E74C3C')
        
        self.clock_label.config(text=self.format_time(self.current_time))
        self.progress['value'] = 0
    
    def update_pomodoro_counter(self):
        """Actualiza el contador visual de pomodoros."""
        self.pomodoro_counter_label.config(text=f"📊 Pomodoros hoy: {self.pomodoros_completed}")
    
    # ==================== FUNCIONES MULTIMEDIA ====================
    def play_sound(self):
        """Reproduce un sonido de alerta usando el sistema."""
        try:
            # Para Windows
            import winsound
            winsound.Beep(1000, 500)
        except:
            try:
                # Para Linux/Mac
                import os
                os.system('printf "\a"')
            except:
                pass  # Silencia errores si no hay sonido
    
    def send_notification(self):
        """Envía una notificación del sistema."""
        try:
            if self.current_phase == "work":
                title = "🍅 Pomodoro Completado"
                message = "¡Tiempo de tomar un descanso!"
            else:
                title = "🎉 Descanso Terminado"
                message = "¡Regresa al trabajo!"
            
            notification.notify(
                title=title,
                message=message,
                timeout=5,
                app_name="Pomodoro Timer"
            )
        except:
            pass  # Silencia errores si plyer no está disponible
    
    # ==================== FUNCIONES EXTRA ====================
    def open_settings(self):
        """Abre ventana de configuración de tiempos."""
        settings_window = Toplevel(self.root)
        settings_window.title("⚙️ Configuración de Tiempos")
        settings_window.geometry("400x400")
        settings_window.configure(bg='#2C3E50')
        settings_window.resizable(False, False)
        
        tk.Label(settings_window, text="Configuración Personalizada", 
                font=('Arial', 14, 'bold'), bg='#2C3E50', fg='white').pack(pady=10)
        
        # Work time
        tk.Label(settings_window, text="Tiempo de Trabajo (minutos):", 
                bg='#2C3E50', fg='white', font=('Arial', 11)).pack(pady=(10, 0))
        work_var = tk.IntVar(value=self.work_time // 60)
        work_spin = tk.Spinbox(settings_window, from_=1, to=60, textvariable=work_var, 
                               width=15, font=('Arial', 11))
        work_spin.pack(pady=5)
        
        # Short break
        tk.Label(settings_window, text="Descanso Corto (minutos):", 
                bg='#2C3E50', fg='white', font=('Arial', 11)).pack(pady=(10, 0))
        short_var = tk.IntVar(value=self.short_break_time // 60)
        short_spin = tk.Spinbox(settings_window, from_=1, to=30, textvariable=short_var, 
                                width=15, font=('Arial', 11))
        short_spin.pack(pady=5)
        
        # Long break
        tk.Label(settings_window, text="Descanso Largo (minutos):", 
                bg='#2C3E50', fg='white', font=('Arial', 11)).pack(pady=(10, 0))
        long_var = tk.IntVar(value=self.long_break_time // 60)
        long_spin = tk.Spinbox(settings_window, from_=1, to=45, textvariable=long_var, 
                               width=15, font=('Arial', 11))
        long_spin.pack(pady=5)
        
        # Posture reminder
        tk.Label(settings_window, text="Recordatorio de postura (cada X pomodoros):", 
                bg='#2C3E50', fg='white', font=('Arial', 11)).pack(pady=(10, 0))
        posture_var = tk.IntVar(value=self.posture_reminder)
        posture_spin = tk.Spinbox(settings_window, from_=1, to=10, textvariable=posture_var, 
                                  width=15, font=('Arial', 11))
        posture_spin.pack(pady=5)
        
        def save_settings():
            self.work_time = work_var.get() * 60
            self.short_break_time = short_var.get() * 60
            self.long_break_time = long_var.get() * 60
            self.posture_reminder = posture_var.get()
            self.save_config()
            self.reset_phase_time()
            settings_window.destroy()
            messagebox.showinfo("Éxito", "✅ Configuración guardada correctamente")
        
        tk.Button(settings_window, text="💾 Guardar Configuración", command=save_settings,
                 bg='#27AE60', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=10, cursor='hand2').pack(pady=20)
    
    def show_stats(self):
        """Muestra ventana con estadísticas."""
        stats_window = Toplevel(self.root)
        stats_window.title("📈 Estadísticas de Productividad")
        stats_window.geometry("550x450")
        stats_window.configure(bg='#2C3E50')
        
        tk.Label(stats_window, text="📊 Estadísticas de Pomodoros", 
                font=('Arial', 16, 'bold'), bg='#2C3E50', fg='white').pack(pady=15)
        
        # Estadísticas del día
        today = datetime.now().strftime("%Y-%m-%d")
        today_count = self.stats['daily'].get(today, 0)
        
        stats_frame = tk.Frame(stats_window, bg='#2C3E50')
        stats_frame.pack(pady=10)
        
        tk.Label(stats_frame, text=f"📅 Hoy:", 
                bg='#2C3E50', fg='#3498DB', font=('Arial', 13, 'bold')).pack()
        tk.Label(stats_frame, text=f"{today_count} pomodoros completados", 
                bg='#2C3E50', fg='white', font=('Arial', 12)).pack()
        
        # Total acumulado
        total = sum(self.stats['daily'].values())
        tk.Label(stats_frame, text=f"\n🏆 Total acumulado:", 
                bg='#2C3E50', fg='#F39C12', font=('Arial', 13, 'bold')).pack()
        tk.Label(stats_frame, text=f"{total} pomodoros", 
                bg='#2C3E50', fg='white', font=('Arial', 12)).pack()
        
        # Últimos 7 días
        tk.Label(stats_window, text="📆 Últimos 7 días:", 
                bg='#2C3E50', fg='white', font=('Arial', 12, 'bold')).pack(pady=(20, 5))
        
        stats_text = tk.Text(stats_window, height=8, width=40, 
                            bg='#34495E', fg='white', font=('Courier', 10))
        stats_text.pack(pady=10, padx=20)
        
        for i in range(7, 0, -1):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            count = self.stats['daily'].get(date, 0)
            stats_text.insert(tk.END, f"{date}: {'█' * min(count, 10)} {count}\n")
        
        stats_text.config(state=tk.DISABLED)
        
        tk.Button(stats_window, text="Cerrar", command=stats_window.destroy,
                 bg='#E74C3C', fg='white', font=('Arial', 11), 
                 padx=20, pady=5, cursor='hand2').pack(pady=15)
    
    def open_task_manager(self):
        """Abre el administrador completo de tareas."""
        task_window = Toplevel(self.root)
        task_window.title("📝 Administrador de Tareas")
        task_window.geometry("550x500")
        task_window.configure(bg='#2C3E50')
        
        tk.Label(task_window, text="📋 Mis Tareas Pendientes", 
                font=('Arial', 16, 'bold'), bg='#2C3E50', fg='white').pack(pady=15)
        
        # Lista de tareas
        task_listbox = tk.Listbox(task_window, height=12, 
                                 bg='#34495E', fg='white', 
                                 font=('Arial', 11), selectmode=tk.SINGLE)
        task_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for task in self.tasks:
            status = "✓" if task['completed'] else "□"
            task_listbox.insert(tk.END, f"{status} {task['title']}")
        
        # Entry para nueva tarea
        task_entry = tk.Entry(task_window, width=40, font=('Arial', 11),
                             bg='#34495E', fg='white', insertbackground='white')
        task_entry.pack(pady=10, padx=20)
        task_entry.insert(0, "Escribe tu nueva tarea aquí...")
        
        def on_entry_click(event):
            if task_entry.get() == "Escribe tu nueva tarea aquí...":
                task_entry.delete(0, tk.END)
        
        task_entry.bind('<FocusIn>', on_entry_click)
        
        def add_new_task():
            title = task_entry.get().strip()
            if title and title != "Escribe tu nueva tarea aquí...":
                self.tasks.append({'title': title, 'completed': False})
                self.save_tasks()
                task_listbox.insert(tk.END, f"□ {title}")
                task_entry.delete(0, tk.END)
                task_entry.insert(0, "Escribe tu nueva tarea aquí...")
                self.refresh_tasks_list()
                messagebox.showinfo("Éxito", "✅ Tarea agregada correctamente")
        
        def complete_selected():
            selection = task_listbox.curselection()
            if selection:
                idx = selection[0]
                if not self.tasks[idx]['completed']:
                    self.tasks[idx]['completed'] = True
                    self.save_tasks()
                    task_listbox.delete(idx)
                    status = "✓" if self.tasks[idx]['completed'] else "□"
                    task_listbox.insert(idx, f"{status} {self.tasks[idx]['title']}")
                    self.refresh_tasks_list()
                    messagebox.showinfo("Éxito", "🎉 ¡Tarea completada! Buen trabajo.")
                else:
                    messagebox.showwarning("Aviso", "Esta tarea ya está completada")
        
        def delete_selected():
            selection = task_listbox.curselection()
            if selection:
                idx = selection[0]
                confirm = messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?")
                if confirm:
                    del self.tasks[idx]
                    self.save_tasks()
                    task_listbox.delete(idx)
                    self.refresh_tasks_list()
        
        button_frame = tk.Frame(task_window, bg='#2C3E50')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="➕ Agregar Tarea", command=add_new_task,
                 bg='#27AE60', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="✓ Completar Tarea", command=complete_selected,
                 bg='#3498DB', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🗑 Eliminar Tarea", command=delete_selected,
                 bg='#E74C3C', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        """Agrega una tarea rápida desde la interfaz principal."""
        task_title = simpledialog.askstring("📝 Nueva Tarea", 
                                            "Ingrese la descripción de la tarea:")
        if task_title and task_title.strip():
            self.tasks.append({'title': task_title.strip(), 'completed': False})
            self.save_tasks()
            self.refresh_tasks_list()
            messagebox.showinfo("Éxito", f"✅ Tarea agregada: {task_title}")
    
    def complete_task(self):
        """Marca la tarea seleccionada como completada."""
        selection = self.tasks_listbox.curselection()
        if selection:
            idx = selection[0]
            # Encontrar la tarea real correspondiente (solo las no completadas)
            incomplete_tasks = [t for t in self.tasks if not t['completed']]
            if idx < len(incomplete_tasks):
                task = incomplete_tasks[idx]
                task['completed'] = True
                self.save_tasks()
                self.refresh_tasks_list()
                self.send_notification_completion()
                messagebox.showinfo("¡Felicidades!", f"🎉 Completaste: {task['title']}")
        else:
            messagebox.showwarning("Selección requerida", "Por favor, selecciona una tarea")
    
    def delete_task(self):
        """Elimina la tarea seleccionada."""
        selection = self.tasks_listbox.curselection()
        if selection:
            idx = selection[0]
            incomplete_tasks = [t for t in self.tasks if not t['completed']]
            if idx < len(incomplete_tasks):
                task = incomplete_tasks[idx]
                confirm = messagebox.askyesno("Confirmar", 
                                             f"¿Eliminar la tarea '{task['title']}'?")
                if confirm:
                    self.tasks.remove(task)
                    self.save_tasks()
                    self.refresh_tasks_list()
        else:
            messagebox.showwarning("Selección requerida", "Por favor, selecciona una tarea")
    
    def refresh_tasks_list(self):
        """Actualiza la lista visual de tareas."""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            if not task['completed']:
                self.tasks_listbox.insert(tk.END, f"□ {task['title']}")
    
    def send_notification_completion(self):
        """Notifica cuando se completa una tarea."""
        try:
            notification.notify(
                title="✅ Tarea Completada",
                message="¡Buen trabajo! Sigue así.",
                timeout=3,
                app_name="Pomodoro Timer"
            )
        except:
            pass
    
    def show_posture_reminder(self):
        """Muestra recordatorio para mejorar la postura."""
        reminder_window = Toplevel(self.root)
        reminder_window.title("🧘 Recordatorio de Salud")
        reminder_window.geometry("450x250")
        reminder_window.configure(bg='#2C3E50')
        reminder_window.resizable(False, False)
        
        tk.Label(reminder_window, text="¡Recordatorio de Postura!", 
                font=('Arial', 16, 'bold'), bg='#2C3E50', fg='#F39C12').pack(pady=20)
        
        tips_frame = tk.Frame(reminder_window, bg='#2C3E50')
        tips_frame.pack(pady=10)
        
        tips = [
            "✓ Endereza la espalda",
            "✓ Relaja los hombros",
            "✓ Mantén la pantalla a nivel de ojos",
            "✓ Toma aire profundo",
            "✓ Parpadea conscientemente"
        ]
        
        for tip in tips:
            tk.Label(tips_frame, text=tip, font=('Arial', 11),
                    bg='#2C3E50', fg='white', anchor='w').pack(anchor='w', pady=3)
        
        tk.Button(reminder_window, text="Entendido, gracias", 
                 command=reminder_window.destroy,
                 bg='#27AE60', fg='white', font=('Arial', 11, 'bold'),
                 padx=20, pady=8, cursor='hand2').pack(pady=15)
    
    def manual_posture_reminder(self):
        """Muestra recordatorio manual de postura."""
        self.show_posture_reminder()
    
    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        if self.is_running:
            confirm = messagebox.askyesno("Confirmar", 
                                         "¿Guardar progreso antes de salir?")
            if confirm:
                self.save_config()
                self.save_stats()
                self.save_tasks()
        else:
            self.save_config()
            self.save_stats()
            self.save_tasks()
        
        self.root.destroy()

# ==================== PUNTO DE ENTRADA ====================
if __name__ == "__main__":
    """
    Punto de entrada principal de la aplicación.
    Inicializa la ventana de Tkinter y ejecuta el Pomodoro Timer.
    """
    try:
        root = tk.Tk()
        app = PomodoroTimer(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presiona Enter para salir...")
