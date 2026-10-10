import json
import heapq
import os
import numpy as np
import joblib
import PySimpleGUI as sg
from kanren import Relation, facts, run, var

# ============================================================
# CONFIGURACIÓN Y CONSTANTES
# ============================================================

MODELO_ARCHIVO = "modelo_tiempo_minutos.pkl"
RUTAS_ARCHIVO = "rutas_transporte.json"

# Tema personalizado
sg.theme('Dark Teal 12')
sg.set_options(
    font=('Arial', 11),
    button_element_size=(12, 1),
    border_width=1,
    tooltip_time=5
)

# ============================================================
# 1. CARGAR MODELO ENTRENADO
# ============================================================

def cargar_modelo():
    if not os.path.exists(MODELO_ARCHIVO):
        sg.popup_error(f"❌ No se encontró el archivo del modelo: {MODELO_ARCHIVO}")
        return None
    try:
        return joblib.load(MODELO_ARCHIVO)
    except Exception as e:
        sg.popup_error(f"❌ Error al cargar el modelo: {str(e)}")
        return None

modelo = cargar_modelo()
if modelo is None:
    exit()

# ============================================================
# 2. RELACIONES Y VARIABLES GLOBALES
# ============================================================

ruta = Relation()
estaciones = set()

def cargar_rutas():
    carpeta_programa = os.path.dirname(os.path.abspath(__file__))
    archivo_json = os.path.join(carpeta_programa, RUTAS_ARCHIVO)

    if not os.path.exists(archivo_json):
        sg.popup_error(f"❌ No se encontró el archivo '{RUTAS_ARCHIVO}'")
        return False

    try:
        with open(archivo_json, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        for r in datos:
            origen = r["origen"]
            destino = r["destino"]
            costo = r["costo"]
            distancia = r["distancia"]

            # Agregar estaciones
            estaciones.add(origen)
            estaciones.add(destino)

            # Registrar rutas bidireccionales
            facts(ruta, (origen, destino, costo, distancia))
            facts(ruta, (destino, origen, costo, distancia))

        return True
    except Exception as e:
        sg.popup_error(f"❌ Error al cargar rutas: {str(e)}")
        return False

def conexiones(estacion):
    destino = var()
    costo = var()
    distancia = var()
    return run(0, (destino, costo, distancia), ruta(estacion, destino, costo, distancia))

def mejor_ruta(inicio, fin):
    cola = [(0, 0, inicio, [inicio])]  # (costo, distancia_acum, actual, camino)
    visitados = set()

    while cola:
        costo, distancia_acum, actual, camino = heapq.heappop(cola)

        if actual == fin:
            return costo, distancia_acum, camino

        if actual in visitados:
            continue

        visitados.add(actual)

        for vecino, costo_ruta, distancia_ruta in conexiones(actual):
            if vecino not in visitados:
                nuevo_costo = costo + costo_ruta
                nueva_distancia = distancia_acum + distancia_ruta
                heapq.heappush(cola, (nuevo_costo, nueva_distancia, vecino, camino + [vecino]))

    return None, 0, []

# Cargar la base de conocimiento
if not cargar_rutas():
    exit()

# ============================================================
# 3. DISEÑO DE LA INTERFAZ GRÁFICA
# ============================================================

estaciones_disponibles = sorted(list(estaciones))

layout = [
    # Encabezado
    [sg.Text("🗺️ SISTEMA DE RUTAS INTELIGENTE", 
             font=("Arial", 20, "bold"), 
             justification="center", 
             expand_x=True,
             pad=(20, 30))],
    
    # Estadísticas rápidas
    [sg.Text(f"📊 Estaciones disponibles: {len(estaciones_disponibles)}", 
             font=("Arial", 9), 
             justification="center", 
             expand_x=True,
             text_color="#AAAAAA")],
    
    [sg.HorizontalSeparator(pad=(20, 20))],
    
    # Fila 1: Origen
    [sg.Text("📍 LUGAR ORIGEN:", font=("Arial", 12, "bold"), size=(15, 1), justification="right"),
     sg.Combo(estaciones_disponibles, 
              key="-ORIGEN-", 
              size=(30, 10), 
              enable_events=True,
              readonly=False),
     sg.Button("🔍 BUSCAR", 
               key="-BUSCAR-", 
               button_color=("white", "#00B050"), 
               font=("Arial", 11, "bold"), 
               size=(10, 1))],
    
    # Fila 2: Destino
    [sg.Text("🏁 LUGAR DESTINO:", font=("Arial", 12, "bold"), size=(15, 1), justification="right"),
     sg.Combo(estaciones_disponibles, 
              key="-DESTINO-", 
              size=(30, 10), 
              enable_events=True,
              readonly=False),
     sg.Button("🗑️ LIMPIAR", 
               key="-LIMPIAR-", 
               button_color=("white", "#FF8C00"), 
               font=("Arial", 11, "bold"), 
               size=(10, 1))],
    
    [sg.HorizontalSeparator(pad=(20, 15))],
    
    # Resultados
    [sg.Text("📋 RESULTADOS:", font=("Arial", 13, "bold"), justification="left", pad=(20, 10))],
    [sg.Multiline(
        key="-SALIDA-",
        size=(60, 12),
        font=("Consolas", 10),
        background_color="#1E1E1E",
        text_color="#FFFFFF",
        disabled=True,
        expand_x=True,
        pad=(20, 10)
    )],
    
    # Botones de acción
    [sg.Push(),
     sg.Button("🚪 SALIR", 
               key="-SALIR-", 
               button_color=("white", "#DC143C"), 
               font=("Arial", 10, "bold"), 
               size=(12, 1)),
     sg.Push()],
    
    [sg.Text("", font=("Arial", 5))]  # Espacio final
]

window = sg.Window(
    "🗺️ Sistema de Rutas Inteligente",
    layout,
    size=(800, 650),
    element_justification="center",
    finalize=True,
    resizable=True
)

# ============================================================
# 4. BUCLE DE EVENTOS
# ============================================================

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "-SALIR-":
        break

    if event == "-LIMPIAR-":
        window["-ORIGEN-"].update("")
        window["-DESTINO-"].update("")
        window["-SALIDA-"].update("📋 Esperando consulta...", justification="center")

    if event == "-BUSCAR-":
        inicio = values["-ORIGEN-"].strip()
        fin = values["-DESTINO-"].strip()

        # Validaciones
        if not inicio or not fin:
            window["-SALIDA-"].update("⚠️ Por favor, ingrese origen y destino.", justification="center")
            continue

        if inicio not in estaciones:
            window["-SALIDA-"].update(f"❌ La estación '{inicio}' no existe.", justification="center")
            continue

        if fin not in estaciones:
            window["-SALIDA-"].update(f"❌ La estación '{fin}' no existe.", justification="center")
            continue

        if inicio == fin:
            window["-SALIDA-"].update("⚠️ El origen y destino no pueden ser iguales.", justification="center")
            continue

        # Mostrar progreso
        window["-SALIDA-"].update("⏳ Calculando mejor ruta...", justification="center")
        window.refresh()

        # Obtener mejor ruta
        costo, distancia, camino = mejor_ruta(inicio, fin)

        if camino:
            # Predicción con el modelo ML
            try:
                datos_nuevos = np.array([[distancia]])
                prediccion = modelo.predict(datos_nuevos)
                tiempo_estimado = prediccion[0]
            except:
                tiempo_estimado = distancia * 2  # Fallback

            horas = int(tiempo_estimado // 60)
            minutos = int(tiempo_estimado % 60)

            # Construir texto con los resultados
            resultado_texto = "¡Ruta óptima encontrada con éxito!\n"
            resultado_texto += "----------------------------------------------\n"
            resultado_texto += f"Camino: {' -> '.join(camino)}\n"
            resultado_texto += f"Costo total: {costo}\n\n"
            resultado_texto += f"📏 Distancia: {distancia:.2f} km\n\n"
            resultado_texto += "⏱️  PREDICCIÓN DE TIEMPO\n"
            resultado_texto += "="*40 + "\n"
            resultado_texto += f"Tiempo estimado: {tiempo_estimado:.2f} minutos\n"
            resultado_texto += f"Equivale a: {horas}h {minutos}m\n"
            
            window["-SALIDA-"].update(resultado_texto, justification="left")
        else:
            window["-SALIDA-"].update("❌ No se encontró una ruta disponible.", justification="center")

window.close()
