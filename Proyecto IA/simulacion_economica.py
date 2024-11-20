import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from threading import Thread
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
from agente_ambiente import SimulacionAmbiente, AgenteAutonomo

class SimulacionEconomica:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simulador de Política Monetaria")
        self.root.geometry("1600x900")
        
        # Variables de control - MOVER AQUÍ antes de crear_interfaz()
        self.modo_automatico = tk.BooleanVar(value=True)
        self.algoritmo_seleccionado = tk.StringVar(value="Genético")
        self.velocidad = 1.0
        self.simulacion_activa = False
        
        # Inicialización de componentes
        self.simulacion = SimulacionAmbiente()
        self.agente = AgenteAutonomo(self.simulacion)
        
        # Crear la interfaz después de inicializar todas las variables
        self.crear_interfaz()

    def crear_interfaz(self):
        # Configuración del grid principal
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        # Panel izquierdo (gráficos)
        self.panel_graficos = ttk.Frame(self.root)
        self.panel_graficos.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.crear_panel_graficos()

        # Panel derecho (controles y datos)
        self.panel_control = ttk.Frame(self.root)
        self.panel_control.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.crear_panel_control()

    def crear_panel_graficos(self):
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(12, 8), dpi=100)
        
        # Configurar subplots
        self.ax_pib = self.fig.add_subplot(321)
        self.ax_inflacion = self.fig.add_subplot(322)
        self.ax_tasa = self.fig.add_subplot(323)
        self.ax_desempleo = self.fig.add_subplot(324)
        self.ax_commodities = self.fig.add_subplot(325)
        self.ax_balanza = self.fig.add_subplot(326)
        
        # Ajustar espaciado
        self.fig.tight_layout(pad=3.0)
        
        # Crear canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel_graficos)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def crear_panel_control(self):
        # Frame para estadísticas actuales
        stats_frame = ttk.LabelFrame(self.panel_control, text="Estadísticas Actuales")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=8)
        self.stats_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame para eventos
        eventos_frame = ttk.LabelFrame(self.panel_control, text="Eventos Económicos")
        eventos_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.eventos_text = scrolledtext.ScrolledText(eventos_frame)
        self.eventos_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para controles
        control_frame = ttk.LabelFrame(self.panel_control, text="Panel de Control")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Control de velocidad
        ttk.Label(control_frame, text="Velocidad de simulación:").pack(padx=5, pady=2)
        self.velocidad_scale = ttk.Scale(control_frame, from_=0.1, to=3.0, 
                                       orient=tk.HORIZONTAL, value=1.0)
        self.velocidad_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Control de modo
        ttk.Checkbutton(control_frame, text="Modo Automático", 
                       variable=self.modo_automatico).pack(padx=5, pady=2)
        
        # Selección de algoritmo
        ttk.Label(control_frame, text="Algoritmo de decisión:").pack(padx=5, pady=2)
        algoritmos = ttk.Combobox(control_frame, textvariable=self.algoritmo_seleccionado,
                                values=list(self.agente.algoritmos.keys()))
        algoritmos.pack(fill=tk.X, padx=5, pady=2)
        
        # Botones de control
        botones_frame = ttk.Frame(control_frame)
        botones_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.btn_iniciar = ttk.Button(botones_frame, text="Iniciar",
                                    command=self.iniciar_simulacion)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        
        self.btn_pausar = ttk.Button(botones_frame, text="Pausar",
                                   command=self.pausar_simulacion)
        self.btn_pausar.pack(side=tk.LEFT, padx=5)
        
        self.btn_reiniciar = ttk.Button(botones_frame, text="Reiniciar",
                                      command=self.reiniciar_simulacion)
        self.btn_reiniciar.pack(side=tk.LEFT, padx=5)
        
        # Frame para choques económicos
        choques_frame = ttk.LabelFrame(self.panel_control, text="Aplicar Choques")
        choques_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.choque_tipo = ttk.Combobox(choques_frame, 
            values=["Inflación", "Tasa de Interés", "Commodities", "PIB"])
        self.choque_tipo.set("Inflación")
        self.choque_tipo.pack(fill=tk.X, padx=5, pady=2)
        
        self.choque_magnitud = ttk.Entry(choques_frame)
        self.choque_magnitud.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Button(choques_frame, text="Aplicar Choque",
                  command=self.aplicar_choque).pack(padx=5, pady=2)

    def actualizar_graficos(self):
        hist = self.simulacion.historico
    
    # Limpiar gráficos
        for ax in [self.ax_pib, self.ax_inflacion, self.ax_tasa, 
                  self.ax_desempleo, self.ax_commodities, self.ax_balanza]:
            ax.clear()
    
    # Obtener el número total de puntos
        n_points = len(hist['tiempo'])
        if n_points < 2:  # Necesitamos al menos 2 puntos para dibujar
            return
        
    # Configurar el número de puntos que queremos mostrar en el "rastro"
        trail_length = 12  # Ajusta este valor para un rastro más largo o más corto
        
    # Crear el efecto de desvanecimiento
        def plot_with_fade(ax, x, y, color):
            if len(x) <= trail_length:
            # Si tenemos menos puntos que el largo del rastro, mostrar todo
                alphas = np.linspace(0.1, 1, len(x))
                for i in range(len(x)-1):
                    ax.plot(x[i:i+2], y[i:i+2], color=color, alpha=alphas[i])
            else:
            # Mostrar solo los últimos trail_length puntos con fade
                start_idx = len(x) - trail_length
                x = x[start_idx:]
                y = y[start_idx:]
                alphas = np.linspace(0.1, 1, trail_length)
                for i in range(trail_length-1):
                    ax.plot(x[i:i+2], y[i:i+2], color=color, alpha=alphas[i])
    
    # Actualizar cada gráfico con el efecto de desvanecimiento
        tiempo = hist['tiempo']
    
        plot_with_fade(self.ax_pib, tiempo, hist['pib'], 'blue')
        self.ax_pib.set_title('PIB')
    
        plot_with_fade(self.ax_inflacion, tiempo, 
                  [x * 100 for x in hist['inflacion']], 'red')
        self.ax_inflacion.set_title('Inflación (%)')
    
        plot_with_fade(self.ax_tasa, tiempo, 
                  [x * 100 for x in hist['tasa_interes']], 'green')
        self.ax_tasa.set_title('Tasa de Interés (%)')
    
        plot_with_fade(self.ax_desempleo, tiempo, 
                  [x * 100 for x in hist['desempleo']], 'magenta')
        self.ax_desempleo.set_title('Desempleo (%)')
    
        plot_with_fade(self.ax_commodities, tiempo, 
                  hist['commodities'], 'yellow')
        self.ax_commodities.set_title('Índice de Commodities')
    
        plot_with_fade(self.ax_balanza, tiempo, 
                  hist['balanza_comercial'], 'cyan')
        self.ax_balanza.set_title('Balanza Comercial')
    
    # Configurar límites dinámicos y estilo de los gráficos
        for ax in [self.ax_pib, self.ax_inflacion, self.ax_tasa, 
                  self.ax_desempleo, self.ax_commodities, self.ax_balanza]:
            ax.relim()
            ax.autoscale_view()
            ax.grid(True, alpha=0.3)
            ax.set_facecolor('#f8f9fa')  # Fondo claro para mejor visibilidad
    
    # Ajustar diseño y redibujar
        self.fig.tight_layout()
        self.canvas.draw()

    def actualizar_estadisticas(self):
        estado = self.simulacion.estado
        
        # Limpiar texto actual
        self.stats_text.delete(1.0, tk.END)
        
        # Insertar estadísticas actualizadas
        stats = f"""PIB: {estado.pib:.2f}
Inflación: {estado.inflacion:.2%}
Tasa de Interés: {estado.tasa_interes:.2%}
Desempleo: {estado.desempleo:.2%}
Commodities: {estado.commodities:.2f}
Balanza Comercial: {estado.balanza_comercial:.2f}
Tipo de Cambio: {estado.tipo_cambio:.2f}"""
        
        self.stats_text.insert(tk.END, stats)

    def actualizar_eventos(self):
        # Limpiar eventos actuales
        self.eventos_text.delete(1.0, tk.END)
        
        # Insertar eventos actualizados
        for evento in self.simulacion.eventos:
            self.eventos_text.insert(tk.END, evento + "\n")
        
        # Auto-scroll al final
        self.eventos_text.see(tk.END)

    def ejecutar_simulacion(self):
        while self.simulacion_activa:
            try:
                # Actualizar simulación
                self.simulacion.actualizar()
                
                # Si está en modo automático, el agente toma decisiones
                if self.modo_automatico.get():
                    self.agente.algoritmo_actual = self.algoritmo_seleccionado.get()
                    self.agente.tomar_decision()
                
                # Actualizar interfaz
                self.root.after(0, self.actualizar_graficos)
                self.root.after(0, self.actualizar_estadisticas)
                self.root.after(0, self.actualizar_eventos)
                
                # Esperar según la velocidad configurada
                time.sleep(1 / self.velocidad_scale.get())
                
            except Exception as e:
                messagebox.showerror("Error", f"Error en la simulación: {str(e)}")
                self.pausar_simulacion()
                break

    def iniciar_simulacion(self):
        if not self.simulacion_activa:
            self.simulacion_activa = True
            self.btn_iniciar.state(['disabled'])
            self.btn_pausar.state(['!disabled'])
            
            # Iniciar simulación en un hilo separado
            Thread(target=self.ejecutar_simulacion, daemon=True).start()

    def pausar_simulacion(self):
        self.simulacion_activa = False
        self.btn_iniciar.state(['!disabled'])
        self.btn_pausar.state(['disabled'])

    def reiniciar_simulacion(self):
        self.pausar_simulacion()
        self.simulacion = SimulacionAmbiente()
        self.agente = AgenteAutonomo(self.simulacion)
        self.actualizar_graficos()
        self.actualizar_estadisticas()
        self.actualizar_eventos()

    def aplicar_choque(self):
        try:
            tipo = self.choque_tipo.get().lower().replace(" ", "_")
            magnitud = float(self.choque_magnitud.get())
            
            if abs(magnitud) > 1.0:
                if not messagebox.askyesno("Confirmación", 
                    "La magnitud del choque es muy alta. ¿Desea continuar?"):
                    return
            
            self.simulacion.estado.choque_externo = magnitud
            self.simulacion._agregar_evento(
                f"Choque aplicado - {tipo}: {magnitud:+.2%}")
            
        except ValueError:
            messagebox.showerror("Error", 
                "Por favor ingrese un valor numérico válido para la magnitud")
