# Simulación Económica con Agente Inteligente

Este proyecto implementa una simulación económica donde un agente inteligente toma decisiones relacionadas con las tasas de interés y optimiza el estado de la economía mediante el uso de diferentes algoritmos, incluyendo A*, DFS, BFS, y algoritmos genéticos. La simulación utiliza modelos macroeconómicos y factores como el PIB, tasas de interés, consumo y gasto público para generar predicciones y optimizar decisiones económicas.

## Estructura del Proyecto

El proyecto está dividido en tres archivos principales:

### 1. `agente_ambiente.py`
Este archivo contiene la implementación del **agente inteligente** y su interacción con el **entorno económico**. El agente tiene la capacidad de tomar decisiones sobre variables macroeconómicas como las tasas de interés, con el objetivo de optimizar el estado de la economía.

#### Funcionalidad:
- Definición de las reglas del agente.
- Cálculo de las decisiones basadas en el estado del entorno.
- Implementación de los métodos para optimizar la economía (A*, DFS, BFS, algoritmos genéticos).

### 2. `simulacion_economica.py`
En este archivo se implementa el **modelo económico** que simula el comportamiento de la economía con base en varios indicadores, como el PIB, la inflación, el consumo, la inversión, entre otros. Este archivo también maneja la actualización de los estados del modelo en función de choques económicos y las decisiones tomadas por el agente.

#### Funcionalidad:
- Definición de los indicadores económicos y sus interrelaciones.
- Actualización del estado del modelo económico en función de los choques y decisiones del agente.
- Cálculo de efectos secundarios (como el crecimiento del PIB y el impacto en la inflación).

### 3. `main.py`
Este es el archivo principal para ejecutar la simulación. En él se inicializan los modelos, se crean las instancias del agente y del entorno económico, y se ejecutan las simulaciones.

#### Funcionalidad:
- Inicialización de los objetos `Agente` y `ModeloEconómico`.
- Ejecución de la simulación en un ciclo de tiempo.
- Llamada a las funciones para actualizar el estado del modelo y las decisiones del agente.
- Manejo de excepciones y errores durante la ejecución.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalados los siguientes paquetes:

- Python 3.x
- `numpy`
- `matplotlib`
- `scipy`
- `random`

Puedes instalar los paquetes necesarios ejecutando:

```bash
pip install numpy matplotlib scipy

