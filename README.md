# APRENDIZAJE SUPERVISADO - ACT 3

Repositorio del proyecto de la actividad 3 del módulo de Inteligencia Artificial.

Este proyecto incluye un modelo de aprendizaje automático para predecir tiempos de viaje en función de la distancia, y un sistema de rutas que utiliza ese modelo para estimar el tiempo de recorrido entre distintos puntos.

## Archivos del proyecto

El proyecto está compuesto por 3 archivos principales que deben mantenerse en la misma carpeta:

1. MODELOHORAS.py
   - Entrena un modelo de regresión lineal.
   - Genera la gráfica de la función de regresión.
   - Guarda el modelo entrenado en un archivo .pkl.

2. APRENDIZAJESUPERVISADO_RUTAS_V2.py
   - Carga el modelo entrenado.
   - Lee las rutas desde el archivo JSON.
   - Calcula la ruta más óptima entre dos estaciones.
   - Usa el modelo para estimar el tiempo de viaje.
   - Ejecuta la interfaz gráfica del sistema.

3. rutas_transporte.json
   - Contiene las rutas, distancias y costos entre estaciones.
   - Sirve como base de conocimiento para el sistema de rutas.

## Estructura recomendada

Todos los archivos deben estar en una sola carpeta, por ejemplo:

```text
APRENDIZAJE-SUPERVISADO-ACT-3--EDWAR-VAYRON-ANDRES/
├── MODELOHORAS.py
├── APRENDIZAJESUPERVISADO_RUTAS_V2.py
├── rutas_transporte.json
├── modelo_tiempo_minutos.pkl
├── README.md
└── ...
```

Importante: si los archivos están separados en carpetas distintas, el programa puede no encontrar el modelo o el JSON.

---

## Requisitos previos

Antes de ejecutar el proyecto, debes tener instalado Python 3 y las librerías necesarias.

### Librerías requeridas

- numpy
  - Permite trabajar con arreglos numéricos y realizar cálculos de matrices.
- scikit-learn
  - Proporciona la clase LinearRegression para entrenar el modelo.
- matplotlib
  - Permite generar la gráfica del modelo y la función de regresión.
- joblib
  - Guarda y carga el modelo entrenado desde un archivo .pkl.
- PySimpleGUI
  - Crea la interfaz gráfica del sistema de rutas.
- kanren
  - Se usa para manejar relaciones lógicas y rutas en el sistema.

### Instalación de librerías

Ejecuta este comando en la terminal:

```bash
pip install numpy scikit-learn matplotlib joblib PySimpleGUI kanren
```

Si prefieres, también puedes crear un entorno virtual antes de instalar:

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# o
source venv/bin/activate   # Linux/macOS
```

Luego instala las librerías:

```bash
pip install numpy scikit-learn matplotlib joblib PySimpleGUI kanren
```

---

## Guía de uso paso a paso

## 1) Entrenar el modelo con MODELOHORAS.py

Primero debes ejecutar el archivo que entrena el modelo de aprendizaje automático:

```bash
python MODELOHORAS.py
```

### Qué hace este archivo

- Define los datos de entrenamiento:
  - tiempo en minutos
  - distancia en kilómetros
- Crea un modelo de regresión lineal con scikit-learn.
- Entrena el modelo con esos datos.
- Guarda el modelo en:

```text
modelo_tiempo_minutos.pkl
```

- Genera una gráfica que muestra la relación entre tiempo y distancia.

### Resultado esperado

Al ejecutar el script, aparecerá una gráfica con:
- puntos azules: datos de entrenamiento
- línea amarilla: función de regresión ajustada
- eje X: tiempo en minutos
- eje Y: distancia en kilómetros

La regresión lineal permite estimar cuántos minutos se necesitan para recorrer cierta distancia.

---

## 2) Ejecutar el sistema completo con APRENDIZAJESUPERVISADO_RUTAS_V2.py

Después de entrenar el modelo, ejecuta el sistema completo de rutas:

```bash
python APRENDIZAJESUPERVISADO_RUTAS_V2.py
```

### Qué hace este archivo

- Carga el modelo entrenado desde `modelo_tiempo_minutos.pkl`.
- Lee las rutas desde `rutas_transporte.json`.
- Busca la ruta óptima entre un origen y un destino.
- Calcula la distancia total.
- Predice el tiempo estimado usando el modelo de regresión lineal.
- Muestra estos resultados en una interfaz gráfica.

### Cómo usar la interfaz

1. Selecciona el lugar de origen.
2. Selecciona el lugar de destino.
3. Pulsa el botón BUSCAR.
4. El sistema mostrará:
   - la ruta más óptima
   - el costo total
   - la distancia total
   - el tiempo estimado

Ejemplo de uso:
- origen: Plaza_Bolivar
- destino: Palacio_Narino

El sistema calcula la ruta más conveniente y predice el tiempo que tomará recorrerla.

---

## 3) Archivo de rutas: rutas_transporte.json

Este archivo contiene la estructura base del sistema:

```json
[
  {"origen": "Plaza_Bolivar", "destino": "Museo_del_Oro", "distancia": 0.5, "costo": 1500},
  {"origen": "Museo_del_Oro", "destino": "Biblioteca_Luis_Angel_Arango", "distancia": 0.6, "costo": 1800}
]
```

Cada elemento representa una conexión entre dos estaciones con:
- origen
- destino
- distancia
- costo

Estos datos son usados para encontrar la mejor ruta entre dos puntos.

---

## Flujo recomendado de ejecución

Para que todo funcione correctamente, el orden correcto es:

```bash
1. python MODELOHORAS.py
2. python APRENDIZAJESUPERVISADO_RUTAS_V2.py
```

Esto es importante porque el segundo archivo necesita que el modelo ya haya sido generado y guardado.

---

## Importancia del modelo y del sistema completo

- El archivo MODELOHORAS.py genera el aprendizaje automático.
- El archivo APRENDIZAJESUPERVISADO_RUTAS_V2.py ejecuta el sistema completo.
- El archivo rutas_transporte.json suministra la información de rutas.

En conjunto, estos archivos permiten:
- entrenar el modelo predictivo
- visualizar la relación entre distancia y tiempo
- encontrar rutas óptimas
- estimar el tiempo de recorrido

---

## Solución rápida de errores comunes

### Error: No se encontró el archivo del modelo

Solución:

```bash
python MODELOHORAS.py
```

### Error: No se encontró rutas_transporte.json

Solución:
- verifica que el archivo esté en la misma carpeta que los scripts
- revisa que el nombre sea exactamente:

```text
rutas_transporte.json
```

### Error: ModuleNotFoundError

Solución:

```bash
pip install numpy scikit-learn matplotlib joblib PySimpleGUI kanren
```

### Error: la interfaz no abre

Solución:
- verifica que PySimpleGUI esté instalado
- ejecuta el script desde la terminal para ver mensajes de error

---

## Resumen breve

- Entrena el modelo: `MODELOHORAS.py`
- Ejecuta el sistema completo: `APRENDIZAJESUPERVISADO_RUTAS_V2.py`
- Base de rutas: `rutas_transporte.json`
- Todo debe estar en una misma carpeta.
- Deben instalarse las librerías necesarias antes de correr el proyecto.

---

## Conclusión

Este proyecto combina aprendizaje supervisado con lógica de rutas para resolver un problema práctico: predecir tiempos de recorrido y sugerir la mejor ruta entre estaciones. La ejecución correcta depende de entrenar primero el modelo y luego lanzar el sistema completo con las rutas cargadas.

Proyecto académico desarrollado en el módulo de Inteligencia Artificial.
