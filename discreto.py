import numpy as np
import matplotlib.pyplot as plt

# Parâmetros da simulação
n = 20  # número de massas
m = 0.05  # massa de cada corpo (kg)
k = 10.0  # constante elástica (N/m)
g = 9.8  # gravidade (m/s^2)
dt = 0.001  # passo de tempo (s)
total_time = 1.5  # tempo total da simulação (s)

# Inicialização das variáveis
y = np.zeros(n)
v = np.zeros(n)
a = np.zeros(n)

# Condições iniciais: equilíbrio estático
y[0] = 0
for i in range(1, n):
    y[i] = y[i - 1] - m * g / k

# Fixando a posição inicial relativa
y = y - y[-1]

# Função para calcular acelerações
def compute_accelerations(y):
    a = np.zeros(n)
    for i in range(n):
        if i == 0:
            a[i] = (-k * (y[i] - y[i + 1]) - m * g) / m
        elif i == n - 1:
            a[i] = (-k * (y[i] - y[i - 1]) - m * g) / m
        else:
            a[i] = (-k * (y[i] - y[i - 1]) - k * (y[i] - y[i + 1]) - m * g) / m
    return a

# Simulação
positions = [y.copy()]
times = [0]
t = 0
released = False

# Tempo de início de movimento para cada massa
start_times = np.full(n, np.nan)

while t < total_time:
    if not released:
        released = True  # libera a mola no tempo zero

    a = compute_accelerations(y)

    # Integração de Euler
    v += a * dt
    y += v * dt

    # Registra o tempo de início de movimento para cada massa
    for idx in range(n):
        if np.isnan(start_times[idx]) and abs(v[idx]) > 1e-4:
            start_times[idx] = t

    t += dt
    positions.append(y.copy())
    times.append(t)

positions = np.array(positions)
times = np.array(times)

# Plotando a simulação para algumas massas selecionadas
plt.figure(figsize=(12, 6))
for idx in range(0, n, max(1, n // 10)):
    plt.plot(times, positions[:, idx], label=f'Massa {idx}')

plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Simulação da Queda de uma Mola Discreta (Slinky)')
plt.legend()
plt.grid()
plt.show()

# Gráfico de tempo de início de movimento
plt.figure(figsize=(12, 6))
plt.plot(range(n), start_times, marker='o')
plt.xlabel('Índice da Massa (de cima para baixo)')
plt.ylabel('Tempo de Início de Movimento (s)')
plt.title('Tempo em que Cada Massa Começa a Cair')
plt.grid()
plt.show()
