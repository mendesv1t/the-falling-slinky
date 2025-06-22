import numpy as np
import matplotlib.pyplot as plt

# parametros da simulacao
m = 1.0      
k = 10.0    
g = 9.8     
dx = 0.01   
x = np.arange(0, 1 + dx, dx)
N = len(x)
dt = 0.0005  
total_time = 1.0

c = np.sqrt(k / m)

# condicoes iniciais
y = - (m * g / k) * (x - 0.5 * x ** 2)
v = np.zeros_like(x)
a = np.zeros_like(x)

def compute_acceleration(y):
    a = np.zeros_like(y)
    for i in range(1, N - 1):
        a[i] = (k / m) * (y[i + 1] - 2 * y[i] + y[i - 1]) / dx ** 2 - g
    a[0] = (k / m) * (y[1] - y[0]) / dx ** 2 - g
    a[-1] = (k / m) * (y[-2] - y[-1]) / dx ** 2 - g
    return a

t = 0
positions = [y.copy()]
times = [0]
start_times = np.full(N, np.nan)

while t < total_time:
    a = compute_acceleration(y)

    v += a * dt
    y += v * dt

    for idx in range(N):
        if np.isnan(start_times[idx]) and abs(v[idx]) > 1e-4:
            start_times[idx] = t

    t += dt
    positions.append(y.copy())
    times.append(t)

positions = np.array(positions)
times = np.array(times)

plt.figure(figsize=(12, 6))
for idx in range(0, N, max(1, N // 10)):
    plt.plot(times, positions[:, idx], label=f'Massa {idx}')

plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Simulação da Queda de um Slinky - Caso Contínuo')
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(x, start_times, marker='o')
plt.xlabel('Posição Inicial Normalizada (x)')
plt.ylabel('Tempo de Início de Movimento (s)')
plt.title('Tempo em que Cada Parte do Slinky Começa a Cair - Caso Contínuo')
plt.grid()
plt.show()
