import numpy as np
import matplotlib.pyplot as plt

n = 20  
m = 0.05
k = 10.0
g = 9.8 
dt = 0.001
total_time = 1.5

y = np.zeros(n)
v = np.zeros(n)
a = np.zeros(n)


y[0] = 0
for i in range(1, n):
    y[i] = y[i - 1] - m * g / k


y = y - y[-1]


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

positions = [y.copy()]
times = [0]
t = 0
released = False

start_times = np.full(n, np.nan)

while t < total_time:
    if not released:
        released = True 

    a = compute_accelerations(y)

    v += a * dt
    y += v * dt

    for idx in range(n):
        if np.isnan(start_times[idx]) and abs(v[idx]) > 1e-4:
            start_times[idx] = t

    t += dt
    positions.append(y.copy())
    times.append(t)

positions = np.array(positions)
times = np.array(times)

plt.figure(figsize=(12, 6))
for idx in range(0, n, max(1, n // 10)):
    plt.plot(times, positions[:, idx], label=f'Massa {idx}')

plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Simulação da Queda de uma Mola Discreta (Slinky)')
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(range(n), start_times, marker='o')
plt.xlabel('Índice da Massa (de cima para baixo)')
plt.ylabel('Tempo de Início de Movimento (s)')
plt.title('Tempo em que Cada Massa Começa a Cair')
plt.grid()
plt.show()
