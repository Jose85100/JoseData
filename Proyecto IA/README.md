# Simulación Económica con Agente Inteligente
# Jose Gabriel Orosco
Este proyecto implementa una simulación económica donde un agente inteligente toma decisiones relacionadas con las tasas de interés y optimiza el estado de la economía mediante el uso de diferentes algoritmos, incluyendo A*, DFS, BFS, y algoritmos genéticos. La simulación utiliza modelos macroeconómicos y factores como el PIB, tasas de interés, consumo y gasto público para generar predicciones y optimizar decisiones económicas.

## Estructura del Proyecto

El proyecto está dividido en dos versiones:

### 1. **Versión Modular (Agente y Simulación Separados)**

En esta versión, el código está dividido en tres archivos principales que trabajan en conjunto:

- **`agente_ambiente.py`**: Contiene la implementación del agente inteligente y su interacción con el entorno económico.
- **`simulacion_economica.py`**: Define el modelo económico que simula el comportamiento de la economía.
- **`main.py`**: El archivo principal para ejecutar la simulación, que maneja la inicialización y ejecución del modelo.

### 2. **Versión Final (Todo en un Solo Archivo)**

En esta versión, el modelo completo se encuentra en un solo archivo denominado `Final.py`. Este archivo contiene la implementación del agente inteligente, la simulación económica y la ejecución del ciclo principal en un solo lugar.

#### Librerías Utilizadas:
El proyecto utiliza las siguientes librerías de Python:

- **`numpy`**: Para cálculos matemáticos.
- **`tkinter`**: Para la creación de la interfaz gráfica de usuario (GUI).
- **`matplotlib`**: Para la visualización de datos y gráficos.
- **`heapq`**: Para implementar estructuras de datos de colas de prioridad.
- **`math`**: Para funciones matemáticas adicionales.
- **`collections.deque`**: Para el manejo eficiente de colas.
- **`dataclasses`**: Para la creación de clases con valores por defecto.
- **`typing`**: Para definiciones de tipos de datos.
- **`abc`**: Para la creación de clases base abstractas.

#### Código:
El código en `Final.py` es una versión integral del modelo que no requiere archivos separados. A continuación se presentan las principales funcionalidades del archivo:

1. **Agente Inteligente**: El agente toma decisiones en base a la simulación de variables macroeconómicas como las tasas de interés.
2. **Simulación Económica**: Se definen los indicadores económicos como el PIB, el consumo, la inflación, entre otros.
3. **Interfaz Gráfica**: Se utiliza `tkinter` para crear una interfaz gráfica donde los resultados de la simulación pueden ser visualizados en tiempo real.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener instalados los siguientes paquetes:

- Python 3.x
- `numpy`
- `matplotlib`
- `tkinter`

Puedes instalar las dependencias necesarias ejecutando:

```bash
pip install numpy matplotlib


