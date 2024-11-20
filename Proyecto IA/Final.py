import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
import heapq
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from abc import ABC, abstractmethod

@dataclass
class EstadoEconomico:
    inflacion: float
    tasa_interes: float
    commodities: float
    pib: float
    timestamp: float = 0.0
    energia: float = 100.0  # Nueva variable para simulated annealing

    def distancia(self, otro_estado: 'EstadoEconomico') -> float:
        # Normalización mejorada con pesos
        pesos = {
            'inflacion': 0.3,
            'tasa_interes': 0.3,
            'commodities': 0.2,
            'pib': 0.2
        }
        
        diff_inflacion = (self.inflacion - otro_estado.inflacion) / max(0.001, otro_estado.inflacion)
        diff_tasa = (self.tasa_interes - otro_estado.tasa_interes) / max(0.001, otro_estado.tasa_interes)
        diff_commodities = (self.commodities - otro_estado.commodities) / max(0.001, otro_estado.commodities)
        diff_pib = (self.pib - otro_estado.pib) / max(0.001, otro_estado.pib)
        
        return math.sqrt(
            pesos['inflacion'] * diff_inflacion**2 + 
            pesos['tasa_interes'] * diff_tasa**2 + 
            pesos['commodities'] * diff_commodities**2 + 
            pesos['pib'] * diff_pib**2
        )

    def obtener_vecinos(self, num_vecinos: int = 8, temperatura: float = 1.0) -> List['EstadoEconomico']:
        vecinos = []
        # Factores de variación adaptativos basados en la temperatura
        var_inflacion = max(0.001, self.inflacion * 0.1 * temperatura)
        var_tasa = max(0.001, self.tasa_interes * 0.1 * temperatura)
        var_commodities = max(1.0, self.commodities * 0.05 * temperatura)
        var_pib = max(10.0, self.pib * 0.02 * temperatura)
        
        for _ in range(num_vecinos):
            vecinos.append(EstadoEconomico(
                inflacion=max(0, self.inflacion + random.gauss(0, var_inflacion)),
                tasa_interes=max(0, self.tasa_interes + random.gauss(0, var_tasa)),
                commodities=max(0, self.commodities + random.gauss(0, var_commodities)),
                pib=max(0, self.pib + random.gauss(0, var_pib)),
                timestamp=time.time(),
                energia=self.energia * 0.95  # Decaimiento de energía
            ))
        return vecinos

@dataclass
class EventoEconomico:
    timestamp: float
    descripcion: str
    impacto: Dict[str, float]

    def __str__(self):
        return f"[{time.strftime('%H:%M:%S', time.localtime(self.timestamp))}] {self.descripcion}"

class AmbienteEconomico:
    def __init__(self):
        # Estado inicial con valores típicos de una economía estable
        self.estado_actual = EstadoEconomico(
            inflacion=0.03,        # 3% de inflación anual
            tasa_interes=0.05,     # 5% tasa de interés de referencia
            commodities=100.0,     # Índice base 100 para materias primas
            pib=1000.0            # PIB base 1000 unidades monetarias
        )
        
        # Estado objetivo con mejores indicadores
        self.estado_objetivo = EstadoEconomico(
            inflacion=0.02,        # 2% inflación objetivo (típico de bancos centrales)
            tasa_interes=0.04,     # 4% tasa objetivo
            commodities=110.0,     # Crecimiento moderado en commodities
            pib=1100.0            # Crecimiento del 10% en PIB
        )
        
        self.historico = {
            'tiempo': [],
            'inflacion': [],
            'tasa_interes': [],
            'commodities': [],
            'pib': []
        }
        
        self.eventos = []
        self.actualizar_historico()
        
        # Nuevas variables para tracking de condiciones económicas
        self.ciclo_economico = "expansión"  # puede ser: expansión, peak, contracción, valle
        self.dias_en_ciclo = 0
        self.shock_externo = False
        self.crisis_financiera = False

    def actualizar_historico(self):
        self.historico['tiempo'].append(time.time())
        self.historico['inflacion'].append(self.estado_actual.inflacion)
        self.historico['tasa_interes'].append(self.estado_actual.tasa_interes)
        self.historico['commodities'].append(self.estado_actual.commodities)
        self.historico['pib'].append(self.estado_actual.pib)

    def generar_evento(self) -> EventoEconomico:
        eventos_posibles = [
            # Eventos monetarios
            {
                'descripcion': "Banco Central aumenta tasa de interés para controlar inflación",
                'impacto': {
                    'tasa_interes': 0.005,  # +50 puntos base
                    'inflacion': -0.002,    # Reducción gradual de inflación
                    'pib': -5.0             # Impacto negativo en crecimiento
                },
                'probabilidad': 0.15 if self.estado_actual.inflacion > 0.04 else 0.05
            },
            {
                'descripcion': "Banco Central reduce tasa de interés para estimular economía",
                'impacto': {
                    'tasa_interes': -0.005, # -50 puntos base
                    'inflacion': 0.001,     # Ligero aumento en inflación
                    'pib': 8.0              # Estímulo al crecimiento
                },
                'probabilidad': 0.15 if self.estado_actual.pib < 950 else 0.05
            },
            # Eventos de commodities
            {
                'descripcion': "Crisis energética eleva precios del petróleo",
                'impacto': {
                    'commodities': 15.0,    # Fuerte aumento en commodities
                    'inflacion': 0.004,     # Presión inflacionaria
                    'pib': -12.0            # Impacto negativo significativo
                },
                'probabilidad': 0.1 if not self.shock_externo else 0.02
            },
            {
                'descripcion': "Mejora en cadenas de suministro global",
                'impacto': {
                    'commodities': -8.0,    # Reducción en costos
                    'inflacion': -0.002,    # Menor presión inflacionaria
                    'pib': 6.0              # Impulso al crecimiento
                },
                'probabilidad': 0.1
            },
            # Eventos de crecimiento
            {
                'descripcion': "Boom tecnológico impulsa productividad",
                'impacto': {
                    'pib': 20.0,            # Fuerte impulso al PIB
                    'tasa_interes': 0.002,  # Ligero aumento en tasas
                    'commodities': 5.0      # Mayor demanda de materias primas
                },
                'probabilidad': 0.08 if self.ciclo_economico == "expansión" else 0.02
            },
            {
                'descripcion': "Crisis financiera afecta mercados globales",
                'impacto': {
                    'pib': -25.0,           # Fuerte contracción
                    'tasa_interes': -0.01,  # Reducción emergencial de tasas
                    'commodities': -12.0    # Caída en demanda de materias primas
                },
                'probabilidad': 0.05 if not self.crisis_financiera else 0.01
            },
            # Eventos inflacionarios
            {
                'descripcion': "Presiones salariales aumentan costos",
                'impacto': {
                    'inflacion': 0.003,     # Aumento en inflación
                    'pib': 4.0,             # Ligero impulso al consumo
                    'tasa_interes': 0.002   # Respuesta monetaria
                },
                'probabilidad': 0.12 if self.estado_actual.pib > 1050 else 0.04
            },
            {
                'descripcion': "Deflación amenaza estabilidad económica",
                'impacto': {
                    'inflacion': -0.004,    # Caída en precios
                    'pib': -8.0,            # Contracción económica
                    'tasa_interes': -0.003  # Respuesta monetaria
                },
                'probabilidad': 0.08 if self.estado_actual.inflacion < 0.01 else 0.02
            }
        ]
        
        # Normalizar probabilidades
        total_prob = sum(evento['probabilidad'] for evento in eventos_posibles)
        prob_acumulada = 0
        rand_val = random.random() * total_prob
        
        for evento in eventos_posibles:
            prob_acumulada += evento['probabilidad']
            if rand_val <= prob_acumulada:
                # Actualizar estado del ciclo económico
                self._actualizar_ciclo_economico(evento['impacto'])
                return EventoEconomico(
                    timestamp=time.time(),
                    descripcion=evento['descripcion'],
                    impacto=evento['impacto']
                )
                
        # Default evento (poco probable que se alcance)
        return EventoEconomico(
            timestamp=time.time(),
            descripcion="Estabilidad económica mantiene indicadores",
            impacto={'pib': 1.0, 'inflacion': 0.0001, 'tasa_interes': 0.0, 'commodities': 0.5}
        )

    def _actualizar_ciclo_economico(self, impacto: Dict[str, float]):
        # Actualizar días en ciclo actual
        self.dias_en_ciclo += 1
        
        # Determinar si hay cambio de ciclo basado en impactos
        impacto_total = sum(impacto.values())
        
        if self.ciclo_economico == "expansión":
            if impacto_total < -20 or self.dias_en_ciclo > 30:
                self.ciclo_economico = "peak"
                self.dias_en_ciclo = 0
        elif self.ciclo_economico == "peak":
            if impacto_total < -10:
                self.ciclo_economico = "contracción"
                self.dias_en_ciclo = 0
        elif self.ciclo_economico == "contracción":
            if self.dias_en_ciclo > 20:
                self.ciclo_economico = "valle"
                self.dias_en_ciclo = 0
        else:  # valle
            if impacto_total > 10 or self.dias_en_ciclo > 15:
                self.ciclo_economico = "expansión"
                self.dias_en_ciclo = 0
        
        # Actualizar condiciones especiales
        if impacto_total < -30:
            self.crisis_financiera = True
        elif impacto_total > 20:
            self.crisis_financiera = False
            
        if abs(impacto_total) > 25:
            self.shock_externo = True
        elif abs(impacto_total) < 10:
            self.shock_externo = False

    def aplicar_evento(self, evento: EventoEconomico):
        # Validar y aplicar cambios en inflación
        if 'inflacion' in evento.impacto:
            nueva_inflacion = self.estado_actual.inflacion + evento.impacto['inflacion']
            self.estado_actual.inflacion = max(0.001, min(0.15, nueva_inflacion))
            
        # Validar y aplicar cambios en tasa de interés
        if 'tasa_interes' in evento.impacto:
            nueva_tasa = self.estado_actual.tasa_interes + evento.impacto['tasa_interes']
            self.estado_actual.tasa_interes = max(0.001, min(0.20, nueva_tasa))
            
        # Validar y aplicar cambios en commodities
        if 'commodities' in evento.impacto:
            nuevos_commodities = self.estado_actual.commodities + evento.impacto['commodities']
            self.estado_actual.commodities = max(50.0, min(200.0, nuevos_commodities))
            
        # Validar y aplicar cambios en PIB
        if 'pib' in evento.impacto:
            nuevo_pib = self.estado_actual.pib + evento.impacto['pib']
            self.estado_actual.pib = max(500.0, min(2000.0, nuevo_pib))

    def actualizar(self):
        # Generar evento con probabilidad ajustada según el ciclo económico
        prob_evento = {
            "expansión": 0.3,
            "peak": 0.4,
            "contracción": 0.5,
            "valle": 0.3
        }[self.ciclo_economico]
        
        if random.random() < prob_evento:
            evento = self.generar_evento()
            self.aplicar_evento(evento)
            self.eventos.append(evento)
            if len(self.eventos) > 10:  # Mantener solo los últimos 10 eventos
                self.eventos.pop(0)
        
        self.actualizar_historico()

class AgenteEconomico:
    def __init__(self, ambiente: AmbienteEconomico):
        self.ambiente = ambiente
        self.algoritmo_actual = "BFS"
        self.metricas = {
            'nodos_visitados': 0,
            'tiempo_ejecucion': 0,
            'calidad_solucion': 0
        }
        self.algoritmos = {
            "BFS": BFS(),
            "DFS": DFS(),
            "A*": AEstrella(),
            "Temple Simulado": TempleSimulado(),
            "Ascenso Colinas": AscensoColinas()
        }


class AlgoritmoBase(ABC):
    @abstractmethod
    def buscar(self, estado_inicial: EstadoEconomico, estado_objetivo: EstadoEconomico,
               max_nodos: int) -> Tuple[List[EstadoEconomico], Dict]:
        pass

class BFS(AlgoritmoBase):
    def buscar(self, estado_inicial: EstadoEconomico, estado_objetivo: EstadoEconomico,
               max_nodos: int) -> Tuple[List[EstadoEconomico], Dict]:
        inicio_tiempo = time.time()
        visitados = set()
        cola = deque([(estado_inicial, [estado_inicial])])
        mejor_distancia = float('inf')
        mejor_camino = []
        nodos_visitados = 0

        while cola and nodos_visitados < max_nodos:
            estado_actual, camino = cola.popleft()
            nodos_visitados += 1
            
            distancia_actual = estado_actual.distancia(estado_objetivo)
            if distancia_actual < mejor_distancia:
                mejor_distancia = distancia_actual
                mejor_camino = camino
                
            if distancia_actual < 0.1:
                return camino, self._generar_metricas(nodos_visitados, inicio_tiempo, distancia_actual)
            
            for vecino in estado_actual.obtener_vecinos():
                estado_str = str(vars(vecino))
                if estado_str not in visitados:
                    visitados.add(estado_str)
                    cola.append((vecino, camino + [vecino]))

        return mejor_camino, self._generar_metricas(nodos_visitados, inicio_tiempo, mejor_distancia)

    def _generar_metricas(self, nodos_visitados: int, inicio_tiempo: float, distancia: float) -> Dict:
        return {
            'nodos_visitados': nodos_visitados,
            'tiempo_ejecucion': time.time() - inicio_tiempo,
            'calidad_solucion': 1 / (1 + distancia)
        }

class DFS(AlgoritmoBase):
    def buscar(self, estado_inicial: EstadoEconomico, estado_objetivo: EstadoEconomico,
               max_nodos: int) -> Tuple[List[EstadoEconomico], Dict]:
        inicio_tiempo = time.time()
        visitados = set()
        pila = [(estado_inicial, [estado_inicial])]
        mejor_distancia = float('inf')
        mejor_camino = []
        nodos_visitados = 0

        while pila and nodos_visitados < max_nodos:
            estado_actual, camino = pila.pop()
            nodos_visitados += 1
            
            distancia_actual = estado_actual.distancia(estado_objetivo)
            if distancia_actual < mejor_distancia:
                mejor_distancia = distancia_actual
                mejor_camino = camino
                
            if distancia_actual < 0.1:
                return camino, self._generar_metricas(nodos_visitados, inicio_tiempo, distancia_actual)
            
            for vecino in reversed(estado_actual.obtener_vecinos()):
                estado_str = str(vars(vecino))
                if estado_str not in visitados:
                    visitados.add(estado_str)
                    pila.append((vecino, camino + [vecino]))

        return mejor_camino, self._generar_metricas(nodos_visitados, inicio_tiempo, mejor_distancia)

    def _generar_metricas(self, nodos_visitados: int, inicio_tiempo: float, distancia: float) -> Dict:
        return {
            'nodos_visitados': nodos_visitados,
            'tiempo_ejecucion': time.time() - inicio_tiempo,
            'calidad_solucion': 1 / (1 + distancia)
        }

class AEstrella(AlgoritmoBase):
    def heuristica(self, estado: EstadoEconomico, objetivo: EstadoEconomico) -> float:
        return estado.distancia(objetivo)

    def buscar(self, estado_inicial: EstadoEconomico, estado_objetivo: EstadoEconomico,
               max_nodos: int) -> Tuple[List[EstadoEconomico], Dict]:
        inicio_tiempo = time.time()
        visitados = set()
        cola_prioridad = [(0, 0, estado_inicial, [estado_inicial])]  # (f_score, contador, estado, camino)
        g_score = {str(vars(estado_inicial)): 0}
        contador = 0  # Para desempatar prioridades iguales
        nodos_visitados = 0
        mejor_camino = []
        mejor_distancia = float('inf')

        while cola_prioridad and nodos_visitados < max_nodos:
            _, _, estado_actual, camino = heapq.heappop(cola_prioridad)
            nodos_visitados += 1
            
            distancia_actual = estado_actual.distancia(estado_objetivo)
            if distancia_actual < mejor_distancia:
                mejor_distancia = distancia_actual
                mejor_camino = camino
                
            if distancia_actual < 0.1:
                return camino, self._generar_metricas(nodos_visitados, inicio_tiempo, distancia_actual)
            
            for vecino in estado_actual.obtener_vecinos():
                estado_str = str(vars(vecino))
                if estado_str not in visitados:
                    visitados.add(estado_str)
                    g = g_score[str(vars(estado_actual))] + estado_actual.distancia(vecino)
                    h = self.heuristica(vecino, estado_objetivo)
                    f = g + h
                    contador += 1
                    heapq.heappush(cola_prioridad, (f, contador, vecino, camino + [vecino]))
                    g_score[estado_str] = g

        return mejor_camino, self._generar_metricas(nodos_visitados, inicio_tiempo, mejor_distancia)

    def _generar_metricas(self, nodos_visitados: int, inicio_tiempo: float, distancia: float) -> Dict:
        return {
            'nodos_visitados': nodos_visitados,
            'tiempo_ejecucion': time.time() - inicio_tiempo,
            'calidad_solucion': 1 / (1 + distancia)
        }

class TempleSimulado(AlgoritmoBase):
    def __init__(self, temp_inicial: float = 100.0, factor_enfriamiento: float = 0.95):
        self.temp_inicial = temp_inicial
        self.factor_enfriamiento = factor_enfriamiento

    def aceptar_transicion(self, delta_e: float, temperatura: float) -> bool:
        if delta_e < 0:  # Mejora la solución
            return True
        probabilidad = math.exp(-delta_e / temperatura)
        return random.random() < probabilidad

    def buscar(self, estado_inicial: EstadoEconomico, estado_objetivo: EstadoEconomico,
               max_nodos: int) -> Tuple[List[EstadoEconomico], Dict]:
        inicio_tiempo = time.time()
        temperatura = self.temp_inicial
        estado_actual = estado_inicial
        mejor_estado = estado_actual
        mejor_distancia = estado_actual.distancia(estado_objetivo)
        nodos_visitados = 0
        camino = [estado_actual]
        
        while temperatura > 0.1 and nodos_visitados < max_nodos:
            vecinos = estado_actual.obtener_vecinos(temperatura=temperatura/self.temp_inicial)
            for vecino in vecinos:
                nodos_visitados += 1
                distancia_vecino = vecino.distancia(estado_objetivo)
                delta_e = distancia_vecino - estado_actual.distancia(estado_objetivo)
                
                if self.aceptar_transicion(delta_e, temperatura):
                    estado_actual = vecino
                    camino.append(estado_actual)
                    
                    if distancia_vecino < mejor_distancia:
                        mejor_distancia = distancia_vecino
                        mejor_estado = vecino
                
                if distancia_vecino < 0.1:
                    return camino, self._generar_metricas(nodos_visitados, inicio_tiempo, distancia_vecino)
            
            temperatura *= self.factor_enfriamiento

        return camino, self._generar_metricas(nodos_visitados, inicio_tiempo, mejor_distancia)

    def _generar_metricas(self, nodos_visitados: int, inicio_tiempo: float, distancia: float) -> Dict:
        return {
            'nodos_visitados': nodos_visitados,
            'tiempo_ejecucion': time.time() - inicio_tiempo,
            'calidad_solucion': 1 / (1 + distancia)
        }

class AscensoColinas(AlgoritmoBase):
    def buscar(self, estado_inicial: EstadoEconomico, estado_objetivo: EstadoEconomico,
               max_nodos: int) -> Tuple[List[EstadoEconomico], Dict]:
        inicio_tiempo = time.time()
        estado_actual = estado_inicial
        mejor_distancia = estado_actual.distancia(estado_objetivo)
        nodos_visitados = 0
        sin_mejora = 0
        max_sin_mejora = 50  # Número máximo de iteraciones sin mejora
        camino = [estado_actual]

        while sin_mejora < max_sin_mejora and nodos_visitados < max_nodos:
            mejor_vecino = None
            mejor_distancia_vecino = float('inf')
            
            for vecino in estado_actual.obtener_vecinos():
                nodos_visitados += 1
                distancia_vecino = vecino.distancia(estado_objetivo)
                
                if distancia_vecino < mejor_distancia_vecino:
                    mejor_distancia_vecino = distancia_vecino
                    mejor_vecino = vecino
                
                if distancia_vecino < 0.1:
                    camino.append(vecino)
                    return camino, self._generar_metricas(nodos_visitados, inicio_tiempo, distancia_vecino)

            if mejor_distancia_vecino < mejor_distancia:
                mejor_distancia = mejor_distancia_vecino
                estado_actual = mejor_vecino
                camino.append(estado_actual)
                sin_mejora = 0
            else:
                sin_mejora += 1

        return camino, self._generar_metricas(nodos_visitados, inicio_tiempo, mejor_distancia)

    def _generar_metricas(self, nodos_visitados: int, inicio_tiempo: float, distancia: float) -> Dict:
        return {
            'nodos_visitados': nodos_visitados,
            'tiempo_ejecucion': time.time() - inicio_tiempo,
            'calidad_solucion': 1 / (1 + distancia)
        }

class SimulacionEconomica:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Simulación del Ambiente Económico con IA")
        self.root.geometry("1600x1000")
        
        self.ambiente = AmbienteEconomico()
        self.agente = AgenteEconomico(self.ambiente)
        self.running = False
        self.update_speed = 1.0
        
        self.algoritmos = {
            "BFS": BFS(),
            "DFS": DFS(),
            "A*": AEstrella(),
            "Temple Simulado": TempleSimulado(),
            "Ascenso Colinas": AscensoColinas()
        }
        
        self.crear_interfaz()
        # Remove the call to iniciar_graficos since that functionality is in crear_panel_graficos
        self.configurar_estilos()

    def configurar_estilos(self):
        style = ttk.Style()
        style.configure('TButton', padding=5)
        style.configure('TLabel', padding=3)
        style.configure('Heading.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('TLabelframe', padding=5)
        style.configure('Info.TLabel', foreground='blue')
        style.configure('Warning.TLabel', foreground='red')

    def crear_interfaz(self):
        # Frame principal con grid de 2x2
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Panel de control superior
        self.crear_panel_control()
        
        # Panel lateral izquierdo
        self.crear_panel_lateral()
        
        # Panel de gráficos
        self.crear_panel_graficos()
        
        # Configurar los pesos del grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    def crear_panel_control(self):
        control_frame = ttk.LabelFrame(self.main_frame, text="Panel de Control", padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # Primera fila: controles básicos
        frame_controles = ttk.Frame(control_frame)
        frame_controles.pack(fill="x", padx=5, pady=5)

        # Botones de control
        self.btn_start = ttk.Button(frame_controles, text="▶ Iniciar/Pausar", command=self.toggle_simulation)
        self.btn_start.pack(side="left", padx=5)

        self.btn_step = ttk.Button(frame_controles, text="⏭ Paso", command=self.step)
        self.btn_step.pack(side="left", padx=5)

        self.btn_reset = ttk.Button(frame_controles, text="↺ Reiniciar", command=self.reset_simulation)
        self.btn_reset.pack(side="left", padx=5)

        # Control de velocidad
        ttk.Label(frame_controles, text="Velocidad:").pack(side="left", padx=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(frame_controles, from_=0.1, to=2.0, 
                              variable=self.speed_var, orient="horizontal", length=100)
        speed_scale.pack(side="left", padx=5)

        # Segunda fila: configuración de algoritmos
        frame_algoritmos = ttk.Frame(control_frame)
        frame_algoritmos.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame_algoritmos, text="Algoritmo:").pack(side="left", padx=5)
        self.algoritmo_var = tk.StringVar(value="BFS")
        self.combo_algoritmo = ttk.Combobox(frame_algoritmos, 
                                          values=list(self.algoritmos.keys()),
                                          textvariable=self.algoritmo_var,
                                          state="readonly",
                                          width=20)
        self.combo_algoritmo.pack(side="left", padx=5)
        self.combo_algoritmo.bind('<<ComboboxSelected>>', self.cambiar_algoritmo)

        # Parámetros del algoritmo
        self.frame_params = ttk.Frame(frame_algoritmos)
        self.frame_params.pack(side="left", padx=5)
        self.actualizar_parametros_algoritmo()

    def crear_panel_lateral(self):
        lateral_frame = ttk.Frame(self.main_frame)
        lateral_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Estado actual
        estado_frame = ttk.LabelFrame(lateral_frame, text="Estado Actual")
        estado_frame.pack(fill="x", padx=5, pady=5)
        self.estado_text = scrolledtext.ScrolledText(estado_frame, height=6)
        self.estado_text.pack(fill="both", expand=True)

        # Eventos económicos
        eventos_frame = ttk.LabelFrame(lateral_frame, text="Eventos Económicos")
        eventos_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.eventos_text = scrolledtext.ScrolledText(eventos_frame)
        self.eventos_text.pack(fill="both", expand=True)

        # Métricas del algoritmo
        metricas_frame = ttk.LabelFrame(lateral_frame, text="Métricas del Algoritmo")
        metricas_frame.pack(fill="x", padx=5, pady=5)
        self.metricas_text = scrolledtext.ScrolledText(metricas_frame, height=6)
        self.metricas_text.pack(fill="both", expand=True)

    def crear_panel_graficos(self):
        self.graficos_frame = ttk.LabelFrame(self.main_frame, text="Visualización")
        self.graficos_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self.graficos_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Configurar subplots
        self.ax1 = self.fig.add_subplot(221, title="Inflación")
        self.ax2 = self.fig.add_subplot(222, title="Tasa de Interés")
        self.ax3 = self.fig.add_subplot(223, title="Commodities")
        self.ax4 = self.fig.add_subplot(224, title="PIB")

        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.grid(True)
            ax.set_xlabel("Tiempo")

    def actualizar_parametros_algoritmo(self):
        # Limpiar frame de parámetros
        for widget in self.frame_params.winfo_children():
            widget.destroy()

        algoritmo = self.algoritmo_var.get()
        if algoritmo == "Temple Simulado":
            ttk.Label(self.frame_params, text="Temperatura:").pack(side="left", padx=2)
            self.temp_var = tk.DoubleVar(value=100.0)
            temp_entry = ttk.Entry(self.frame_params, textvariable=self.temp_var, width=8)
            temp_entry.pack(side="left", padx=2)

            ttk.Label(self.frame_params, text="Factor enfriamiento:").pack(side="left", padx=2)
            self.enfr_var = tk.DoubleVar(value=0.95)
            enfr_entry = ttk.Entry(self.frame_params, textvariable=self.enfr_var, width=8)
            enfr_entry.pack(side="left", padx=2)
        elif algoritmo in ["BFS", "DFS", "A*"]:
            ttk.Label(self.frame_params, text="Max nodos:").pack(side="left", padx=2)
            self.max_nodos_var = tk.IntVar(value=1000)
            nodos_entry = ttk.Entry(self.frame_params, textvariable=self.max_nodos_var, width=8)
            nodos_entry.pack(side="left", padx=2)

    def cambiar_algoritmo(self, event=None):
        self.actualizar_parametros_algoritmo()
        self.agente.algoritmo_actual = self.algoritmo_var.get()
        # Actualizar el algoritmo en el agente
        if self.algoritmo_var.get() == "Temple Simulado":
            self.agente.algoritmos["Temple Simulado"] = TempleSimulado(
                temp_inicial=self.temp_var.get(),
                factor_enfriamiento=self.enfr_var.get()
            )

    def actualizar_graficos(self):
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
            ax.grid(True)
        
        tiempo = list(self.ambiente.historico['tiempo'])
        
        # Graficar datos históricos con colores y estilos mejorados
        self.ax1.plot(tiempo, self.ambiente.historico['inflacion'], 'r-', 
                     label="Actual", linewidth=2)
        self.ax1.axhline(y=self.ambiente.estado_objetivo.inflacion, 
                        color='g', linestyle='--', label="Objetivo")
        self.ax1.set_title("Inflación (%)")
        self.ax1.legend()

        self.ax2.plot(tiempo, self.ambiente.historico['tasa_interes'], 'b-', 
                     label="Actual", linewidth=2)
        self.ax2.axhline(y=self.ambiente.estado_objetivo.tasa_interes, 
                        color='g', linestyle='--', label="Objetivo")
        self.ax2.set_title("Tasa de Interés (%)")
        self.ax2.legend()

        self.ax3.plot(tiempo, self.ambiente.historico['commodities'], 'g-', 
                     label="Actual", linewidth=2)
        self.ax3.axhline(y=self.ambiente.estado_objetivo.commodities, 
                        color='g', linestyle='--', label="Objetivo")
        self.ax3.set_title("Commodities")
        self.ax3.legend()

        self.ax4.plot(tiempo, self.ambiente.historico['pib'], 'k-', 
                     label="Actual", linewidth=2)
        self.ax4.axhline(y=self.ambiente.estado_objetivo.pib, 
                        color='g', linestyle='--', label="Objetivo")
        self.ax4.set_title("PIB")
        self.ax4.legend()

        self.fig.tight_layout()
        self.canvas.draw()

    def actualizar_estado(self):
        estado_actual = self.ambiente.estado_actual
        estado_objetivo = self.ambiente.estado_objetivo
        
        estado_str = (
            f"Estado Actual:\n"
            f"  Inflación: {estado_actual.inflacion:.2%}\n"
            f"  Tasa de Interés: {estado_actual.tasa_interes:.2%}\n"
            f"  Commodities: {estado_actual.commodities:.2f}\n"
            f"  PIB: {estado_actual.pib:.2f}\n\n"
            f"Objetivo:\n"
            f"  Inflación: {estado_objetivo.inflacion:.2%}\n"
            f"  Tasa de Interés: {estado_objetivo.tasa_interes:.2%}\n"
            f"  Commodities: {estado_objetivo.commodities:.2f}\n"
            f"  PIB: {estado_objetivo.pib:.2f}"
        )
        
        self.estado_text.delete(1.0, tk.END)
        self.estado_text.insert(tk.END, estado_str)

    def actualizar_eventos(self):
        self.eventos_text.delete(1.0, tk.END)
        for evento in reversed(self.ambiente.eventos):
            self.eventos_text.insert(tk.END, str(evento) + "\n")

    def actualizar_metricas(self):
        self.metricas_text.delete(1.0, tk.END)
        metricas_str = (
            f"Algoritmo actual: {self.algoritmo_var.get()}\n"
            f"Nodos visitados: {self.agente.metricas['nodos_visitados']}\n"
            f"Tiempo de ejecución: {self.agente.metricas['tiempo_ejecucion']:.3f}s\n"
            f"Calidad de solución: {self.agente.metricas['calidad_solucion']:.3f}\n"
            f"Distancia al objetivo: {self.ambiente.estado_actual.distancia(self.ambiente.estado_objetivo):.4f}"
        )
        self.metricas_text.insert(tk.END, metricas_str)

    def toggle_simulation(self):
        self.running = not self.running
        if self.running:
            self.btn_start.configure(text="⏸ Pausar")
            self.ejecutar_simulacion()
        else:
            self.btn_start.configure(text="▶ Iniciar")

    def reset_simulation(self):
        self.ambiente = AmbienteEconomico()
        self.agente = AgenteEconomico(self.ambiente)
        self.running = False
        self.btn_start.configure(text="▶ Iniciar")
        self.actualizar_interfaz()

    def step(self):
        self.ambiente.actualizar()
        algoritmo = self.algoritmos[self.algoritmo_var.get()]
        camino, metricas = algoritmo.buscar(
            self.ambiente.estado_actual,
            self.ambiente.estado_objetivo,
            self.max_nodos_var.get() if hasattr(self, 'max_nodos_var') else 1000
        )
        
        if camino and len(camino) > 1:
            self.ambiente.estado_actual = camino[1]
            self.agente.metricas = metricas
        
        self.actualizar_interfaz()
        
        if self.ambiente.estado_actual.distancia(self.ambiente.estado_objetivo) < 0.1:
            messagebox.showinfo("Simulación", "¡Objetivo alcanzado!")
            self.running = False
            self.btn_start.configure(text="▶ Iniciar")

    def actualizar_interfaz(self):
        self.actualizar_graficos()
        self.actualizar_estado()
        self.actualizar_eventos()
        self.actualizar_metricas()

    def ejecutar_simulacion(self):
        if self.running:
            self.step()
            self.update_speed = self.speed_var.get()
            self.root.after(int(self.update_speed * 1000), self.ejecutar_simulacion)

    def iniciar(self):
        self.root.protocol("WM_DELETE_WINDOW", self.salir)
        self.actualizar_interfaz()
        self.root.mainloop()

    def salir(self):
        self.running = False
        self.root.quit()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SimulacionEconomica(root)
        app.iniciar()
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error inesperado:\n{str(e)}")
    finally:
        try:
            root.destroy()
        except:
            pass
