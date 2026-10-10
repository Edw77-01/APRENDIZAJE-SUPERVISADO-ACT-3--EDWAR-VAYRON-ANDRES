import numpy as np
import joblib
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# ==========================
# 1. DATOS DE ENTRENAMIENTO
# ==========================
X = np.array([0.5, 1, 1.5, 2.5, 3, 4, 5.5, 6]).reshape(-1, 1)  # Minutos
y = np.array([1, 2, 3, 5, 6, 8, 11, 12])  # Kilometros (Velocidad constante de 30 km/h)

print("\nDatos de entrenamiento:")
for i in range(len(X)):
    print(f"{X[i][0]} minutos -> {y[i]} kilometros")

# ==========================
# 2. ENTRENAMIENTO
# ==========================
modelo = LinearRegression()
modelo.fit(X, y)

print("\nModelo entrenado correctamente")
print(f"Coeficiente (pendiente): {modelo.coef_[0]:.2f}")
print(f"Intercepto (punto de corte): {modelo.intercept_:.2f}")

# ==========================
# 3. GUARDAR MODELO
# ==========================
joblib.dump(modelo, "modelo_tiempo_minutos.pkl")
print("\nModelo exportado como: modelo_tiempo_minutos.pkl")
# 4. Visualización de los resultados
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Datos de Entrenamiento')
plt.plot(X, modelo.predict(X), color='yellow', label='Línea de Regresión')

plt.title('Regresión Lineal: Predicción de Tiempo a Distancia (Velocidad Constante de 30 km/h)')
plt.xlabel('Tiempo en Minutos')
plt.ylabel('Distancia en Kilometros')
plt.legend()
plt.grid(True)
plt.show()
