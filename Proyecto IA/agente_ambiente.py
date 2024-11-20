import numpy as np
from datetime import datetime
import time
from threading import Lock
class ModeloISLM:
    def __init__(self):
        # Parámetros calibrados para mayor estabilidad
        self.sensibilidad_inversion_tasa = 0.2  # Reducido para menor volatilidad
        self.multiplicador_gasto = 1.1  # Ajustado para evitar amplificación excesiva
        self.sensibilidad_dinero_tasa = 0.15
        self.velocidad_ajuste = 0.03  # Reducido para suavizar cambios
        
        # Nuevos parámetros de estabilización
        self.max_cambio_pib = 0.02  # Límite de 2% de cambio por período
        self.inercia_pib = 0.8  # Factor de suavización
        self.elasticidad_exportaciones = 0.3
        
    def calcular_equilibrio(self, estado):
        # Cálculo de componentes con restricciones y factores de estabilización
        
        # Inversión con límites y ajuste por confianza
        tasa_real = estado.tasa_interes - estado.inflacion
        inversion_base = (0.20 - self.sensibilidad_inversion_tasa * tasa_real)
        inversion_ajustada = inversion_base * (estado.indice_confianza / 100)
        inversion = np.clip(inversion_ajustada, 0.15, 0.25) * estado.pib
        
        # Consumo con inercia y ajuste por inflación
        efecto_inflacion = max(0.8, 1 - 0.5 * estado.inflacion)
        consumo_base = 0.65 * estado.pib * efecto_inflacion
        consumo = consumo_base * (estado.indice_confianza / 100)
        consumo = np.clip(consumo, 0.5 * estado.pib, 0.7 * estado.pib)
        
        # Gasto gobierno como proporción estable del PIB
        gasto_gobierno = 0.18 * estado.pib
        
        # Exportaciones netas con mayor realismo
        competitividad = (1 / estado.tipo_cambio) ** self.elasticidad_exportaciones
        efecto_commodities = np.clip((estado.commodities / 100) ** 0.3, 0.7, 1.3)
        exportaciones_base = 0.15 * estado.pib * competitividad * efecto_commodities
        
        # Ajuste por riesgo país
        factor_riesgo = np.clip(1 - (estado.riesgo_pais - 200) / 1000, 0.8, 1.2)
        exportaciones = exportaciones_base * factor_riesgo
        
        # Demanda agregada con límites de variación
        demanda_total = consumo + inversion + gasto_gobierno + exportaciones
        
        # Calcular cambio en PIB con restricciones
        pib_objetivo = demanda_total
        brecha_pib = (pib_objetivo - estado.pib) / estado.pib
        
        # Limitar el cambio máximo y aplicar inercia
        cambio_maximo = self.max_cambio_pib
        cambio_pib_limitado = np.clip(brecha_pib, -cambio_maximo, cambio_maximo)
        
        # Aplicar velocidad de ajuste y suavización
        cambio_pib_final = (
            self.velocidad_ajuste * 
            cambio_pib_limitado * 
            (1 - self.inercia_pib)
        )
        
        # Calcular nuevo PIB
        nuevo_pib = estado.pib * (1 + cambio_pib_final)
        
        # Asegurar que el PIB se mantenga dentro de límites razonables
        pib_min = 0.95 * estado.pib  # Máxima caída de 5%
        pib_max = 1.05 * estado.pib  # Máximo crecimiento de 5%
        nuevo_pib = np.clip(nuevo_pib, pib_min, pib_max)
        
        return nuevo_pib, inversion

class ObjetivoEconomico:
    def __init__(self):
        # Objetivos basados en metas colombianas
        self.inflacion_objetivo = 0.03
        self.pib_objetivo = 100.0
        self.desempleo_objetivo = 0.08
        self.balanza_objetivo = 0.0
        self.tipo_cambio_objetivo = 1.0
        
        # Pesos para la función de pérdida
        self.peso_inflacion = 0.35
        self.peso_pib = 0.25
        self.peso_desempleo = 0.20
        self.peso_balanza = 0.10
        self.peso_tipo_cambio = 0.10

    def calcular_perdida(self, estado):
        return (
            self.peso_inflacion * abs(estado.inflacion - self.inflacion_objetivo) +
            self.peso_pib * abs(estado.pib - self.pib_objetivo) / 100 +
            self.peso_desempleo * abs(estado.desempleo - self.desempleo_objetivo) +
            self.peso_balanza * abs(estado.balanza_comercial) / estado.pib +
            self.peso_tipo_cambio * abs(estado.tipo_cambio - self.tipo_cambio_objetivo)
        )

class EstadoEconomico:
    def __init__(self, initial_state=None):
        """
        Inicializa el estado económico con valores por defecto o un estado inicial proporcionado.
        
        Args:
            initial_state (dict, optional): Diccionario con valores iniciales para sobrescribir los valores por defecto
        """
        # Valores iniciales calibrados para una economía en desarrollo
        self._state = {
            # Variables monetarias y precios
            'inflacion': 0.095,              # 9.5% inflación anual
            'tasa_interes': 0.13,            # 13% tasa de interés
            'tipo_cambio': 1.2,              # Tipo de cambio respecto a moneda de referencia
            
            # Variables reales
            'pib': 100.0,                    # PIB indexado (base 100)
            'desempleo': 0.105,              # 10.5% tasa de desempleo
            
            # Variables externas
            'commodities': 95.0,             # Índice de precios de commodities (base 100)
            'balanza_comercial': -0.03,      # -3% del PIB
            'riesgo_pais': 200,              # Puntos base de spread
            
            # Variables de expectativas y confianza
            'expectativas_inflacion': 0.07,   # 7% expectativa de inflación
            'indice_confianza': 100.0,       # Índice base 100
            
            # Choques externos
            'choque_externo': 0.0,           # Choque externo normalizado
            'choque_oferta': 0.0             # Choque de oferta normalizado
        }
        
        # Límites de variables para mantener realismo
        self._limits = {
            #'inflacion': (-0.02, 0.30),         # Deflación máx 2%, inflación máx 30%
            #'tasa_interes': (0.01, 0.35),       # Entre 1% y 35%
            #'tipo_cambio': (0.5, 3.0),          # Fluctuación máxima respecto a base
            #'pib': (50.0, 200.0),               # Rango del índice base 100
            #'desempleo': (0.03, 0.25),          # Entre 3% y 25%
            #'commodities': (40.0, 200.0),       # Rango del índice base 100
            #'balanza_comercial': (-0.3, 0.3), # Entre -15% y +15% del PIB
            #'riesgo_pais': (50, 1000),          # Entre 50 y 1000 puntos base
            #'expectativas_inflacion': (0, 0.35), # Entre 0% y 35%
            #'indice_confianza': (40.0, 160.0),  # Rango del índice base 100
            #'choque_externo': (-0.2, 0.2),      # Choques normalizados
            #'choque_oferta': (-0.2, 0.2)        # Choques normalizados
        }
        
        # Aplicar estado inicial si se proporciona
        if initial_state is not None:
            self.update_state(initial_state)
    
    def __getattr__(self, name):
        """Permite acceder a las variables de estado como atributos."""
        if name in self._state:
            return self._state[name]
        raise AttributeError(f"'{self.__class__.__name__}' no tiene el atributo '{name}'")
    
    def __setattr__(self, name, value):
        """Permite establecer variables de estado como atributos con validación."""
        if name in ('_state', '_limits'):
            super().__setattr__(name, value)
            return
            
        if name in self._state:
            self.update_state({name: value})
        else:
            super().__setattr__(name, value)
    
    def update_state(self, updates):
        """
        Actualiza múltiples variables de estado con validación.
        
        Args:
            updates (dict): Diccionario con las actualizaciones {variable: nuevo_valor}
        
        Raises:
            ValueError: Si algún valor está fuera de los límites permitidos
        """
        for var, value in updates.items():
            if var not in self._state:
                raise ValueError(f"Variable de estado inválida: {var}")
            
            # Validar límites si existen
            if var in self._limits:
                min_val, max_val = self._limits[var]
                if not min_val <= value <= max_val:
                    raise ValueError(
                        f"Valor fuera de rango para {var}: {value}. "
                        f"Rango permitido: [{min_val}, {max_val}]"
                    )
            
            self._state[var] = value
    
    def get_state_copy(self):
        """Retorna una copia del estado actual."""
        return self._state.copy()
    
    def get_summary(self):
        """Retorna un resumen del estado económico actual."""
        return {
            'monetary_indicators': {
                'inflacion': f"{self.inflacion:.1%}",
                'tasa_interes': f"{self.tasa_interes:.1%}",
                'tipo_cambio': f"{self.tipo_cambio:.2f}"
            },
            'real_indicators': {
                'pib': f"{self.pib:.1f}",
                'desempleo': f"{self.desempleo:.1%}"
            },
            'external_sector': {
                'commodities': f"{self.commodities:.1f}",
                'balanza_comercial': f"{self.balanza_comercial/self.pib:.1%} del PIB",
                'riesgo_pais': f"{self.riesgo_pais:d} pb"
            },
            'expectations': {
                'expectativas_inflacion': f"{self.expectativas_inflacion:.1%}",
                'indice_confianza': f"{self.indice_confianza:.1f}"
            }
        }
    
    def get_alert_conditions(self):
        """
        Evalúa y retorna condiciones que requieren atención.
        """
        alerts = []
        
        # Condiciones críticas
        if self.inflacion > 0.15:
            alerts.append(('CRÍTICO', 'Inflación muy elevada'))
        elif self.inflacion > 0.10:
            alerts.append(('ALERTA', 'Inflación alta'))
        
        if self.desempleo > 0.15:
            alerts.append(('CRÍTICO', 'Desempleo muy alto'))
        elif self.desempleo > 0.12:
            alerts.append(('ALERTA', 'Desempleo elevado'))
        
        if abs(self.balanza_comercial/self.pib) > 0.08:
            alerts.append(('CRÍTICO', 'Desequilibrio externo severo'))
        elif abs(self.balanza_comercial/self.pib) > 0.05:
            alerts.append(('ALERTA', 'Desequilibrio externo significativo'))
        
        if self.riesgo_pais > 500:
            alerts.append(('CRÍTICO', 'Riesgo país muy elevado'))
        elif self.riesgo_pais > 350:
            alerts.append(('ALERTA', 'Riesgo país alto'))
        
        if self.indice_confianza < 60:
            alerts.append(('CRÍTICO', 'Crisis de confianza'))
        elif self.indice_confianza < 80:
            alerts.append(('ALERTA', 'Baja confianza'))
        
        return alerts
    
    def calculate_policy_room(self):
        """
        Calcula el espacio disponible para política monetaria.
        """
        return {
            'tasa_real': self.tasa_interes - self.inflacion,
            'margen_baja': self.tasa_interes - self._limits['tasa_interes'][0],
            'margen_alza': self._limits['tasa_interes'][1] - self.tasa_interes,
            'stress_level': min(1.0, max(0.0,
                (self.riesgo_pais - 200) / 300 +
                abs(self.balanza_comercial/self.pib) / 0.1 +
                max(0, (self.inflacion - 0.1) / 0.1)
            ) / 3)
        }

class SimulacionAmbiente:
    def __init__(self):
        self.estado = EstadoEconomico()
        self.modelo = ModeloISLM()
        self.objetivo = ObjetivoEconomico()
        self.lock = Lock()
        
        self.historico = {
            'tiempo': [],
            'inflacion': [],
            'tasa_interes': [],
            'pib': [],
            'commodities': [],
            'desempleo': [],
            'balanza_comercial': [],
            'tipo_cambio': [],
            'indice_confianza': [],
            'riesgo_pais': [],
            'perdida': []
        }
        
        self.eventos = []
        self.tiempo_inicial = time.time()

    def actualizar(self):
        with self.lock:
            # Choques más suaves y realistas
            choque_demanda = np.random.normal(0, 0.005)
            choque_oferta = np.random.normal(0, 0.005)
            choque_externo = np.random.normal(0, 0.01)
            
            # Actualización de commodities con límites
            delta_commodities = (choque_externo +
                               0.1 * (self.estado.tipo_cambio - 1) -
                               0.05 * (self.estado.tasa_interes - self.estado.inflacion))
            max_cambio_commodities = 0.03
            delta_commodities = np.clip(delta_commodities, 
                                      -max_cambio_commodities, 
                                      max_cambio_commodities)
            self.estado.commodities *= (1 + delta_commodities)
            self.estado.commodities = np.clip(self.estado.commodities, 60, 140)
            
            nuevo_pib, inversion = self.modelo.calcular_equilibrio(self.estado)
            
            # Brecha de producto controlada
            brecha_producto = (nuevo_pib - self.estado.pib) / self.estado.pib
            brecha_producto = np.clip(brecha_producto, -0.02, 0.02)
            
            # Inflación con mayor inercia
            nueva_inflacion = (0.7 * self.estado.inflacion +
                             0.2 * self.estado.expectativas_inflacion +
                             0.05 * brecha_producto +
                             0.05 * (self.estado.tipo_cambio - 1) +
                             choque_oferta)
            max_cambio_inflacion = 0.01
            self.estado.inflacion = self.estado.inflacion + np.clip(
                nueva_inflacion - self.estado.inflacion,
                -max_cambio_inflacion,
                max_cambio_inflacion
            )
            
            # Desempleo más estable
            self.estado.desempleo = max(0.04, min(0.20,
                0.9 * self.estado.desempleo +
                0.1 * (0.08 - 0.5 * brecha_producto) +
                0.2 * choque_demanda))
            
            # Tipo de cambio con ajuste gradual
            delta_tipo_cambio = (0.05 * (self.estado.tasa_interes - self.estado.inflacion) +
                               0.1 * choque_externo +
                               0.02 * (self.estado.riesgo_pais - 200) / 200)
            max_cambio_tipo_cambio = 0.02
            delta_tipo_cambio = np.clip(delta_tipo_cambio, 
                                      -max_cambio_tipo_cambio, 
                                      max_cambio_tipo_cambio)
            self.estado.tipo_cambio *= (1 + delta_tipo_cambio)
            
            # Balanza comercial más realista
            self.estado.balanza_comercial = (
                -0.02 +
                0.08 * (self.estado.tipo_cambio - 1) +
                0.1 * (self.estado.commodities - 100) / 100 +
                choque_externo
            ) * self.estado.pib
            
            self.estado.balanza_comercial = np.clip(
                self.estado.balanza_comercial,
                -0.06 * self.estado.pib,
                0.04 * self.estado.pib
            )
            
            # Índice de confianza más estable
            delta_confianza = (0.1 * brecha_producto -
                             0.2 * (self.estado.inflacion - self.objetivo.inflacion_objetivo) +
                             0.05 * choque_demanda)
            max_cambio_confianza = 0.05
            delta_confianza = np.clip(delta_confianza, 
                                    -max_cambio_confianza, 
                                    max_cambio_confianza)
            self.estado.indice_confianza *= (1 + delta_confianza)
            self.estado.indice_confianza = np.clip(self.estado.indice_confianza, 60, 140)
            
            # Riesgo país más estable
            delta_riesgo = (0.1 * abs(self.estado.balanza_comercial) / self.estado.pib +
                          0.2 * (self.estado.inflacion - self.objetivo.inflacion_objetivo) +
                          0.05 * choque_externo)
            max_cambio_riesgo = 20
            delta_riesgo = np.clip(delta_riesgo * 200, -max_cambio_riesgo, max_cambio_riesgo)
            self.estado.riesgo_pais = np.clip(
                self.estado.riesgo_pais + delta_riesgo,
                100,
                500
            )
            
            self.estado.pib = nuevo_pib
            
            # Expectativas de inflación más ancladas
            self.estado.expectativas_inflacion = (
                0.8 * self.estado.expectativas_inflacion +
                0.2 * self.estado.inflacion
            )
            
            self._registrar_historico()
            self._generar_eventos()

    def _registrar_historico(self):
        tiempo_actual = time.time() - self.tiempo_inicial
        self.historico['tiempo'].append(tiempo_actual)
        self.historico['inflacion'].append(self.estado.inflacion)
        self.historico['tasa_interes'].append(self.estado.tasa_interes)
        self.historico['pib'].append(self.estado.pib)
        self.historico['commodities'].append(self.estado.commodities)
        self.historico['desempleo'].append(self.estado.desempleo)
        self.historico['balanza_comercial'].append(self.estado.balanza_comercial)
        self.historico['tipo_cambio'].append(self.estado.tipo_cambio)
        self.historico['indice_confianza'].append(self.estado.indice_confianza)
        self.historico['riesgo_pais'].append(self.estado.riesgo_pais)
        self.historico['perdida'].append(self.objetivo.calcular_perdida(self.estado))

    def _generar_eventos(self):
        # Eventos con umbrales ajustados
        if self.estado.inflacion > 0.12:
            self._agregar_evento("ALERTA CRÍTICA: Inflación superior al 12%")
        elif self.estado.inflacion > 0.08:
            self._agregar_evento("ALERTA: Alta inflación detectada")
        
        if self.estado.desempleo > 0.15:
            self._agregar_evento("ALERTA CRÍTICA: Desempleo superior al 15%")
        elif self.estado.desempleo > 0.12:
            self._agregar_evento("ALERTA: Aumento significativo del desempleo")
        
        if abs(self.estado.balanza_comercial) > 0.05 * self.estado.pib:
            self._agregar_evento("ALERTA CRÍTICA: Desequilibrio severo en balanza comercial")
        elif abs(self.estado.balanza_comercial) > 0.03 * self.estado.pib:
            self._agregar_evento("ALERTA: Desequilibrio importante en balanza comercial")
        
        if abs(self.estado.tipo_cambio - 1) > 0.25:
            self._agregar_evento("ALERTA: Alta volatilidad en tipo de cambio")
        
        if self.estado.indice_confianza < 75:
            self._agregar_evento("ALERTA: Baja confianza del consumidor")
        
        if self.estado.riesgo_pais > 350:
            self._agregar_evento("ALERTA CRÍTICA: Alto riesgo país")
        elif self.estado.riesgo_pais > 250:
            self._agregar_evento("ALERTA: Aumento del riesgo país")

    def _agregar_evento(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.eventos.append(f"[{timestamp}] {mensaje}")
        if len(self.eventos) > 50:
            self.eventos.pop(0)

class AlgoritmosDecision:
    @staticmethod
    def algoritmo_genetico(estado, objetivo):
        # Configuración del algoritmo genético
        tamano_poblacion = 30  # Aumentado para mejor exploración
        num_generaciones = 15
        prob_mutacion = 0.15
        
        # Rango de tasas basado en condiciones actuales
        rango_min = max(0.01, estado.tasa_interes - 0.015)  # Máximo 1.5% de cambio
        rango_max = min(0.20, estado.tasa_interes + 0.015)
        
        # Población inicial centrada alrededor de la tasa actual
        poblacion = np.random.normal(
            estado.tasa_interes,
            0.005,  # Desviación estándar pequeña
            size=tamano_poblacion
        )
        poblacion = np.clip(poblacion, rango_min, rango_max)
        
        mejor_historico = estado.tasa_interes
        mejor_score_historico = float('-inf')
        
        for _ in range(num_generaciones):
            # Evaluación con penalización por volatilidad
            fitness = []
            for tasa in poblacion:
                score_base = 1.0 / (1.0 + AlgoritmosDecision._evaluar_politica(tasa, estado, objetivo))
                penalizacion_volatilidad = abs(tasa - estado.tasa_interes) * 10
                fitness.append(score_base - penalizacion_volatilidad)
            
            fitness = np.array(fitness)
            
            # Actualizar mejor histórico
            mejor_actual = poblacion[np.argmax(fitness)]
            if fitness[np.argmax(fitness)] > mejor_score_historico:
                mejor_historico = mejor_actual
                mejor_score_historico = fitness[np.argmax(fitness)]
            
            # Normalización del fitness
            fitness = fitness - np.min(fitness)
            if np.sum(fitness) > 0:
                fitness = fitness / np.sum(fitness)
            else:
                fitness = np.ones_like(fitness) / len(fitness)
            
            # Selección de padres
            padres_indices = np.random.choice(
                tamano_poblacion,
                size=tamano_poblacion,
                p=fitness
            )
            padres = poblacion[padres_indices]
            
            # Nueva población
            nueva_poblacion = []
            
            # Elitismo: mantener el mejor
            nueva_poblacion.append(mejor_historico)
            
            # Cruce y mutación
            while len(nueva_poblacion) < tamano_poblacion:
                # Seleccionar padres
                padre1, padre2 = np.random.choice(padres, size=2)
                
                # Cruce BLX-α
                alpha = 0.3
                min_val = min(padre1, padre2)
                max_val = max(padre1, padre2)
                rango = max_val - min_val
                hijo = np.random.uniform(
                    min_val - alpha * rango,
                    max_val + alpha * rango
                )
                
                # Mutación adaptativa
                if np.random.random() < prob_mutacion:
                    # Mutación más pequeña si el fitness es bueno
                    mutacion_scale = 0.003 * (1 - max(fitness))
                    hijo += np.random.normal(0, mutacion_scale)
                
                # Asegurar límites
                hijo = np.clip(hijo, rango_min, rango_max)
                nueva_poblacion.append(hijo)
            
            poblacion = np.array(nueva_poblacion)
        
        # Retornar mejor solución encontrada con límite de cambio
        mejor_tasa = poblacion[np.argmax([1.0 / (1.0 + AlgoritmosDecision._evaluar_politica(tasa, estado, objetivo))
                                        for tasa in poblacion])]
        
        # Limitar el cambio máximo
        cambio_maximo = 0.005  # Máximo 0.5% de cambio por iteración
        if abs(mejor_tasa - estado.tasa_interes) > cambio_maximo:
            mejor_tasa = estado.tasa_interes + np.sign(
                mejor_tasa - estado.tasa_interes) * cambio_maximo
            
        return mejor_tasa

    @staticmethod
    def algoritmo_a_star(estado, objetivo):
        # Generar nodos con mayor granularidad cerca de la tasa actual
        tasas_cercanas = np.linspace(
            max(0.01, estado.tasa_interes - 0.01),
            min(0.20, estado.tasa_interes + 0.01),
            15
        )
        tasas_lejanas = np.linspace(0.01, 0.20, 10)
        tasas = np.unique(np.concatenate([tasas_cercanas, tasas_lejanas]))
        
        # Función heurística más sofisticada
        def heuristica(tasa):
            return (abs(estado.inflacion - objetivo.inflacion_objetivo) * 5 +
                   abs(estado.pib - objetivo.pib_objetivo) / 100 +
                   abs(tasa - estado.tasa_interes) * 8)
        
        # Calcular scores con la nueva heurística
        scores = [-AlgoritmosDecision._evaluar_politica(tasa, estado, objetivo) -
                 heuristica(tasa) for tasa in tasas]
        
        mejor_tasa = tasas[np.argmax(scores)]
        
        # Limitar cambio máximo
        cambio_maximo = 0.005
        if abs(mejor_tasa - estado.tasa_interes) > cambio_maximo:
            mejor_tasa = estado.tasa_interes + np.sign(
                mejor_tasa - estado.tasa_interes) * cambio_maximo
            
        return mejor_tasa

    @staticmethod
    def algoritmo_dfs(estado, objetivo):
        mejor_tasa = estado.tasa_interes
        mejor_score = -AlgoritmosDecision._evaluar_politica(estado.tasa_interes, estado, objetivo)
        visitados = set()
        
        def explorar(tasa, profundidad=0, cambio_acumulado=0):
            nonlocal mejor_tasa, mejor_score
            
            if profundidad > 5 or cambio_acumulado > 0.015:  # Limitar profundidad y cambio total
                return
            
            tasa_redondeada = round(tasa, 4)  # Reducir espacio de búsqueda
            if tasa_redondeada in visitados:
                return
            
            visitados.add(tasa_redondeada)
            score = -AlgoritmosDecision._evaluar_politica(tasa, estado, objetivo)
            
            if score > mejor_score:
                mejor_score = score
                mejor_tasa = tasa
            
            # Explorar cambios más pequeños primero
            for delta in [-0.005, -0.0025, 0.0025, 0.005]:
                nueva_tasa = max(0.01, min(0.20, tasa + delta))
                nuevo_cambio = cambio_acumulado + abs(delta)
                explorar(nueva_tasa, profundidad + 1, nuevo_cambio)
        
        explorar(estado.tasa_interes)
        return mejor_tasa

    @staticmethod
    def algoritmo_bfs(estado, objetivo):
        # Generar niveles de tasas con mayor detalle cerca de la tasa actual
        rango = 0.01  # Rango de búsqueda
        num_niveles = 3
        tasas_por_nivel = 7
        
        todas_tasas = []
        for nivel in range(num_niveles):
            rango_nivel = rango * (1 - nivel * 0.3)  # Reducir rango en niveles más profundos
            tasas_nivel = np.linspace(
                max(0.01, estado.tasa_interes - rango_nivel),
                min(0.20, estado.tasa_interes + rango_nivel),
                tasas_por_nivel
            )
            todas_tasas.extend(tasas_nivel)
        
        tasas = np.unique(todas_tasas)
        scores = [-AlgoritmosDecision._evaluar_politica(tasa, estado, objetivo) -
                 abs(tasa - estado.tasa_interes) * 5 for tasa in tasas]
        
        mejor_tasa = tasas[np.argmax(scores)]
        
        # Limitar cambio máximo
        cambio_maximo = 0.005
        if abs(mejor_tasa - estado.tasa_interes) > cambio_maximo:
            mejor_tasa = estado.tasa_interes + np.sign(
                mejor_tasa - estado.tasa_interes) * cambio_maximo
            
        return mejor_tasa

    @staticmethod
    def algoritmo_greedy(estado, objetivo):
        tasa_actual = estado.tasa_interes
        mejor_tasa = tasa_actual
        mejor_score = -AlgoritmosDecision._evaluar_politica(tasa_actual, estado, objetivo)
        
        # Búsqueda más granular cerca de la tasa actual
        deltas = [-0.005, -0.0025, -0.001, 0, 0.001, 0.0025, 0.005]
        
        for delta in deltas:
            nueva_tasa = max(0.01, min(0.20, tasa_actual + delta))
            score = -AlgoritmosDecision._evaluar_politica(nueva_tasa, estado, objetivo)
            
            # Penalización por volatilidad
            score -= abs(delta) * 5
            
            if score > mejor_score:
                mejor_score = score
                mejor_tasa = nueva_tasa
        
        return mejor_tasa

    @staticmethod
    def _evaluar_politica(tasa, estado, objetivo):
        """
        Evalúa una política monetaria considerando múltiples factores y sus interacciones.
        Retorna una penalización total (menor es mejor).
        """
        # Brecha de inflación con peso variable
        brecha_inflacion = abs(estado.inflacion - objetivo.inflacion_objetivo)
        peso_inflacion = 20 if estado.inflacion > objetivo.inflacion_objetivo else 15
        penalizacion_inflacion = brecha_inflacion * peso_inflacion
        
        # Brecha de PIB con zona neutral
        brecha_pib = abs(estado.pib - objetivo.pib_objetivo) / objetivo.pib_objetivo
        if brecha_pib < 0.02:  # 2% de zona neutral
            penalizacion_pib = 0
        else:
            penalizacion_pib = (brecha_pib - 0.02) * 10
        
        # Desempleo con histéresis
        brecha_desempleo = estado.desempleo - objetivo.desempleo_objetivo
        penalizacion_desempleo = abs(brecha_desempleo) * 12 * (1 + max(0, brecha_desempleo))
        
        # Balanza comercial con umbrales
        ratio_balanza = abs(estado.balanza_comercial) / estado.pib
        if ratio_balanza < 0.03:
            penalizacion_balanza = ratio_balanza * 3
        else:
            penalizacion_balanza = (0.03 * 3 + (ratio_balanza - 0.03) * 8)
        
        # Tipo de cambio con banda de tolerancia
        desviacion_tc = abs(estado.tipo_cambio - objetivo.tipo_cambio_objetivo)
        if desviacion_tc < 0.1:
            penalizacion_tc = desviacion_tc * 2
        else:
            penalizacion_tc = (0.1 * 2 + (desviacion_tc - 0.1) * 5)
        
        # Penalización por volatilidad de tasa
        penalizacion_volatilidad = abs(tasa - estado.tasa_interes) * 10
        
        # Penalizaciones adicionales por condiciones extremas
        if estado.inflacion > 0.12:  # Inflación > 12%
            penalizacion_inflacion *= 1.5
        if estado.desempleo > 0.12:  # Desempleo > 12%
            penalizacion_desempleo *= 1.5
        
        # Penalización por riesgo y confianza
        penalizacion_riesgo = max(0, (estado.riesgo_pais - 300) / 50)
        penalizacion_confianza = max(0, (100 - estado.indice_confianza) / 10)
        
        # Penalización por tasa real negativa persistente
        tasa_real = tasa - estado.inflacion
        if tasa_real < -0.02:  # Tasa real menor a -2%
            penalizacion_tasa_real = abs(tasa_real + 0.02) * 15
        else:
            penalizacion_tasa_real = 0
        
        return (penalizacion_inflacion + penalizacion_pib + 
                penalizacion_desempleo + penalizacion_balanza +
                penalizacion_tc + penalizacion_volatilidad +
                penalizacion_riesgo + penalizacion_confianza +
                penalizacion_tasa_real)

class AgenteAutonomo:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.algoritmo_actual = "Genético"
        self.algoritmos = {
            "Genético": AlgoritmosDecision.algoritmo_genetico,
            "A*": AlgoritmosDecision.algoritmo_a_star,
            "DFS": AlgoritmosDecision.algoritmo_dfs,
            "BFS": AlgoritmosDecision.algoritmo_bfs,
            "Greedy": AlgoritmosDecision.algoritmo_greedy
        }
        
        # Contadores y métricas
        self.decisiones_tomadas = 0
        self.historial_perdidas = []
        self.ultima_decision = None
        self.tiempo_ultima_decision = None
        
        # Nuevas métricas de desempeño
        self.ventana_evaluacion = 12  # Evalúa últimas 12 decisiones
        self.umbral_cambio_tasa = 0.0025  # 25 puntos base como cambio mínimo significativo
        self.historial_decisiones = []
        self.eficacia_decisiones = []

    def tomar_decision(self):
        estado_actual = self.ambiente.estado
        
        # Evaluar condiciones de mercado
        condiciones = self._evaluar_condiciones_mercado()
        
        # Ajustar parámetros según condiciones
        nueva_tasa = self._obtener_tasa_ajustada(condiciones)
        
        # Suavizar cambios grandes
        if self.ultima_decision is not None:
            max_cambio = self._calcular_max_cambio(condiciones)
            nueva_tasa = self._suavizar_cambio(nueva_tasa, max_cambio)
        
        # Registrar decisión
        self._registrar_decision(nueva_tasa)
        
        # Actualizar estado
        self.ambiente.estado.tasa_interes = nueva_tasa
        
        return self._generar_metricas(nueva_tasa)

    def _evaluar_condiciones_mercado(self):
        estado = self.ambiente.estado
        objetivo = self.ambiente.objetivo
        
        return {
            'crisis_inflacionaria': estado.inflacion > objetivo.inflacion_objetivo * 2,
            'deflacion': estado.inflacion < 0,
            'recesion': (estado.pib / objetivo.pib_objetivo) < 0.97,
            'sobrecalentamiento': (estado.pib / objetivo.pib_objetivo) > 1.03,
            'crisis_externa': abs(estado.balanza_comercial / estado.pib) > 0.05,
            'estres_financiero': estado.riesgo_pais > 350
        }

    def _obtener_tasa_ajustada(self, condiciones):
        # Obtener tasa base del algoritmo seleccionado
        tasa_base = self.algoritmos[self.algoritmo_actual](
            self.ambiente.estado,
            self.ambiente.objetivo
        )
        
        # Ajustar según condiciones especiales
        if condiciones['crisis_inflacionaria']:
            tasa_base += 0.005  # +50 puntos base
        elif condiciones['deflacion']:
            tasa_base -= 0.005
        
        if condiciones['recesion']:
            tasa_base -= 0.0025
        elif condiciones['sobrecalentamiento']:
            tasa_base += 0.0025
            
        return np.clip(tasa_base, 0.01, 0.20)  # Mantener en rango válido

    def _calcular_max_cambio(self, condiciones):
        # Cambio base de 50 puntos base
        max_cambio = 0.005
        
        # Ajustar según condiciones
        if condiciones['crisis_inflacionaria'] or condiciones['deflacion']:
            max_cambio = 0.0075  # Permite cambios más agresivos
        elif condiciones['estres_financiero']:
            max_cambio = 0.003  # Más cauteloso
            
        return max_cambio

    def _suavizar_cambio(self, nueva_tasa, max_cambio):
        if self.ultima_decision is None:
            return nueva_tasa
            
        cambio = nueva_tasa - self.ultima_decision
        if abs(cambio) > max_cambio:
            return self.ultima_decision + np.sign(cambio) * max_cambio
            
        return nueva_tasa

    def _registrar_decision(self, nueva_tasa):
        tiempo_actual = time.time()
        perdida_actual = self.ambiente.objetivo.calcular_perdida(self.ambiente.estado)
        
        self.decisiones_tomadas += 1
        self.historial_perdidas.append(perdida_actual)
        self.historial_decisiones.append({
            'tasa': nueva_tasa,
            'tiempo': tiempo_actual,
            'perdida': perdida_actual,
            'estado': self._capturar_estado_actual()
        })
        
        # Mantener historial manejable
        if len(self.historial_decisiones) > self.ventana_evaluacion:
            self.historial_decisiones.pop(0)
        
        # Registrar cambio significativo
        if (self.ultima_decision is not None and 
            abs(nueva_tasa - self.ultima_decision) > self.umbral_cambio_tasa):
            self.ambiente._agregar_evento(
                f"Ajuste tasa: {self.ultima_decision:.2%} → {nueva_tasa:.2%}"
            )
        
        self.ultima_decision = nueva_tasa
        self.tiempo_ultima_decision = tiempo_actual

    def _capturar_estado_actual(self):
        estado = self.ambiente.estado
        return {
            'inflacion': estado.inflacion,
            'pib': estado.pib,
            'desempleo': estado.desempleo,
            'balanza_comercial': estado.balanza_comercial,
            'tipo_cambio': estado.tipo_cambio,
            'riesgo_pais': estado.riesgo_pais,
            'indice_confianza': estado.indice_confianza
        }

    def _generar_metricas(self, nueva_tasa):
        return {
            'nueva_tasa': nueva_tasa,
            'perdida_actual': self.historial_perdidas[-1],
            'decisiones_tomadas': self.decisiones_tomadas,
            'perdida_promedio': np.mean(self.historial_perdidas[-10:])
                if len(self.historial_perdidas) >= 10 else None,
            'volatilidad_decisiones': np.std([d['tasa'] for d in self.historial_decisiones])
                if len(self.historial_decisiones) > 1 else 0,
            'eficacia_reciente': self._calcular_eficacia_reciente()
        }

    def _calcular_eficacia_reciente(self):
        if len(self.historial_perdidas) < self.ventana_evaluacion:
            return None
            
        perdidas_recientes = self.historial_perdidas[-self.ventana_evaluacion:]
        mejoras = sum(1 for i in range(1, len(perdidas_recientes))
                     if perdidas_recientes[i] < perdidas_recientes[i-1])
        return mejoras / (self.ventana_evaluacion - 1)

    def obtener_diagnostico(self):
        """Genera un diagnóstico detallado del desempeño del agente."""
        if len(self.historial_decisiones) < 2:
            return "Insuficientes datos para diagnóstico"

        estado = self.ambiente.estado
        objetivo = self.ambiente.objetivo
        
        # Análisis de tendencias
        perdidas_recientes = [d['perdida'] for d in self.historial_decisiones[-5:]]
        tendencia = np.polyfit(range(len(perdidas_recientes)), perdidas_recientes, 1)[0]
        
        # Volatilidad de decisiones
        volatilidad_tasa = np.std([d['tasa'] for d in self.historial_decisiones])
        
        # Análisis de brechas
        brecha_inflacion = abs(estado.inflacion - objetivo.inflacion_objetivo)
        brecha_pib = abs(estado.pib - objetivo.pib_objetivo) / objetivo.pib_objetivo
        
        mensajes = []
        
        # Evaluación de tendencia
        if tendencia < -0.001:
            mensajes.append("✓ Mejora consistente en desempeño")
        elif tendencia > 0.001:
            mensajes.append("⚠ Deterioro en desempeño")
        else:
            mensajes.append("→ Desempeño estable")
        
        # Evaluación de volatilidad
        if volatilidad_tasa > 0.0075:
            mensajes.append("⚠ Alta volatilidad en decisiones")
        elif volatilidad_tasa < 0.002:
            mensajes.append("⚠ Posible inercia excesiva")
        
        # Evaluación de objetivos
        if brecha_inflacion > 0.02:
            mensajes.append(f"⚠ Desvío inflación: {brecha_inflacion:.1%}")
        if brecha_pib > 0.03:
            mensajes.append(f"⚠ Desvío PIB: {brecha_pib:.1%}")
        
        # Sugerencias de política
        if self._calcular_eficacia_reciente() < 0.4:
            mensajes.append("⚠ Considerar cambio de estrategia")
        
        return " | ".join(mensajes)

    def reiniciar(self):
        """Reinicia todos los contadores y el historial del agente."""
        self.decisiones_tomadas = 0
        self.historial_perdidas = []
        self.ultima_decision = None
        self.tiempo_ultima_decision = None
        self.historial_decisiones = []
        self.eficacia_decisiones = []
