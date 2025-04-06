import numpy as np
from math import pi
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

# === 1. Crear circuito cuántico ===
InputQ = QuantumRegister(1, name='InputQ')
Medida = ClassicalRegister(1, name='Medida')
circuito_fractal = QuantumCircuit(InputQ, Medida)

# Compuertas cuánticas aplicadas al qubit
circuito_fractal.h(0)
circuito_fractal.x(0)
circuito_fractal.s(0)
circuito_fractal.x(0)
circuito_fractal.u(pi/152, -pi/4, pi/16, 0)

# Función para aplicar X varias veces
def aplicar_compuertas(circuito, repeticiones=3):
    for i in range(repeticiones):
        circuito.x(0)
        circuito_fractal.s(0)
        circuito_fractal.x(0)
        circuito_fractal.u(pi/152, -pi/4, pi/16, 0)
    return circuito


def cn():
    global circuito_fractal
    circuito_fractal = aplicar_compuertas(circuito_fractal)
    
    # === 2. Simular circuito cuántico ===
    simulador = AerSimulator(method='statevector')
    copia = circuito_fractal.copy()
    copia.save_statevector()
    transp_circuit = transpile(copia, simulador)
    resultado = simulador.run(transp_circuit).result()
    estado_final = resultado.get_statevector(transp_circuit)
    
    # Obtener amplitudes z0 y z1
    z0 = estado_final.data[0]
    z1 = estado_final.data[1]
    
    # Calcular c = z0 / z1 (si z1 ≠ 0)
    if z1 != 0:
        z = z0 / z1
    else:
        z = 0
    
 #   print("Valor de c =", z)
    return z

# === 3. Función para graficar el conjunto de Julia ===
def julia_set(c=cn(), height=1000, width=1000, zoom=1, max_iterations=500):
    x_width = 1.5
    y_height = 1.5 * height / width
    x = np.linspace(-x_width / zoom, x_width / zoom, width)
    y = np.linspace(-y_height / zoom, y_height / zoom, height)
    z_grid = x + y[:, None] * 1j

    div_time = np.zeros(z_grid.shape, dtype=int)
    m = np.full(z_grid.shape, True, dtype=bool)

    for i in range(max_iterations):
        z_grid[m] = z_grid[m]**2 + cn()
        m[np.abs(z_grid) > 2] = False
        div_time[m] = i

    return div_time

# === 4. Mostrar el fractal ===
plt.imshow(julia_set(), cmap='twilight_shifted')
plt.axis("off")
plt.title("Fractal de Julia con c generado aleatoriamente.")
plt.show()

