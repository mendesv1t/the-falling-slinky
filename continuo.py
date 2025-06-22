import numpy as np
import matplotlib.pyplot as plt

# Parâmetros da simulação
m = 1.0      # massa total (kg)
k = 10.0     # constante elástica (N/m)
g = 9.8      # gravidade (m/s^2)
dx = 0.01    # passo espacial
x = np.arange(0, 1 + dx, dx)
N = len(x)
dt = 0.0005  # passo de tempo (s)
total_time = 1.0

c = np.sqrt(k / m)

# Condições iniciais
y = - (m * g / k) * (x - 0.5 * x ** 2)
v = np.zeros_like(x)
a = np.zeros_like(x)

# Fronteiras de Neumann (derivada zero nas bordas)
def compute_acceleration(y):
    a = np.zeros_like(y)
    for i in range(1, N - 1):
        a[i] = (k / m) * (y[i + 1] - 2 * y[i] + y[i - 1]) / dx ** 2 - g
    # Condições de contorno: derivada zero nas bordas
    a[0] = (k / m) * (y[1] - y[0]) / dx ** 2 - g
    a[-1] = (k / m) * (y[-2] - y[-1]) / dx ** 2 - g
    return a

# Simulação
t = 0
positions = [y.copy()]
times = [0]
start_times = np.full(N, np.nan)

while t < total_time:
    a = compute_acceleration(y)

    # Integração de Euler
    v += a * dt
    y += v * dt

    # Registro do início de movimento
    for idx in range(N):
        if np.isnan(start_times[idx]) and abs(v[idx]) > 1e-4:
            start_times[idx] = t

    t += dt
    positions.append(y.copy())
    times.append(t)

positions = np.array(positions)
times = np.array(times)

# Gráfico das posições ao longo do tempo
plt.figure(figsize=(12, 6))
for idx in range(0, N, max(1, N // 10)):
    plt.plot(times, positions[:, idx], label=f'Massa {idx}')

plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Simulação da Queda de um Slinky - Caso Contínuo')
plt.legend()
plt.grid()
plt.show()

# Gráfico de tempo de início de movimento
plt.figure(figsize=(12, 6))
plt.plot(x, start_times, marker='o')
plt.xlabel('Posição Inicial Normalizada (x)')
plt.ylabel('Tempo de Início de Movimento (s)')
plt.title('Tempo em que Cada Parte do Slinky Começa a Cair - Caso Contínuo')
plt.grid()
plt.show()
