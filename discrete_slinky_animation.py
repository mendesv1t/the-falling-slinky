import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

n = 10
m = 0.1
k = 1.0
g = 9.8
dt = 0.01
total_time = 5

positions = np.zeros(n)
velocities = np.zeros(n)

scale_factor = 1
for i in range(1, n):
    positions[i] = positions[i - 1] - scale_factor * (m * g / k)

positions -= positions[-1]
initial_positions = positions.copy()

time_points = [0]
positions_over_time = [positions.copy()]
num_steps = int(total_time / dt)

limiar_significativo = abs(initial_positions[n - 1] - initial_positions[0]) * 0.0001

for step in range(num_steps):
    accelerations = np.zeros(n)

    for i in range(n):
        if i == 0:
            spring_force = -k * (positions[i] - positions[i + 1])
            accelerations[i] = (spring_force - m * g) / m
        elif i == n - 1:
            spring_force = -k * (2 * positions[i] - positions[i - 1])
        else:
            spring_force = -k * (2 * positions[i] - positions[i - 1] - positions[i + 1])

        if i != 0:
            deslocamento_massa_superior = abs(positions[i - 1] - initial_positions[i - 1])
            if deslocamento_massa_superior > limiar_significativo:
                accelerations[i] = (spring_force - m * g) / m
            else:
                accelerations[i] = 0

    velocities += accelerations * dt
    positions += velocities * dt

    time_points.append((step + 1) * dt)
    positions_over_time.append(positions.copy())

positions_over_time = np.array(positions_over_time)
time_points = np.array(time_points)


fig, ax = plt.subplots(figsize=(6, 8))
plt.subplots_adjust(bottom=0.3)

zoom_factor = 10
ax.set_xlim(-0.1 / zoom_factor, 0.1 / zoom_factor)

y_min = np.min(positions_over_time) - 1.0
y_max = np.max(positions_over_time[0]) + 1.0

ax.set_ylim(y_max, -1 * y_max)
ax.invert_yaxis()

bolinha_markersize = 10
bolinha_diametro = 0.02  
raio_bolinha = bolinha_diametro / 80


spring_lines, = ax.plot([], [], color='gray', linewidth=1.5, label='Molas', zorder=1)
first_point, = ax.plot([], [], 'o', color='red', markersize=bolinha_markersize, label='Primeira Massa', zorder=3)
middle_points, = ax.plot([], [], 'o', color='black', markersize=bolinha_markersize, label='Massas Intermediárias', zorder=3)
last_point, = ax.plot([], [], 'o', color='green', markersize=bolinha_markersize, label='Última Massa', zorder=3)


fixed_base_y = positions_over_time[0, -1]
base_line = ax.axhline(y=fixed_base_y, color='red', linestyle='--', label='Posição Inicial da Base')

spring_lines, = ax.plot([], [], color='gray', linewidth=1.5, label='Molas')

is_running = {'value': False}
current_frame = {'index': 0}

def zigzag_between_points(x0, y0, x1, y1, num_zigs=6, amplitude=raio_bolinha):
    y0_corrigido = y0 + raio_bolinha
    y1_corrigido = y1 - raio_bolinha

    ys = np.linspace(y0_corrigido, y1_corrigido, num_zigs * 2 + 1)
    xs = np.zeros_like(ys)

    for i in range(1, len(xs) - 1):
        xs[i] = amplitude if i % 2 == 0 else -amplitude

    return xs, ys

def spring_curve(x0, y0, x1, y1, num_coils=5, amplitude=raio_bolinha):
    y0_corrigido = y0 + raio_bolinha
    y1_corrigido = y1 - raio_bolinha

    length = y1_corrigido - y0_corrigido
    ys = np.linspace(y0_corrigido, y1_corrigido, num_coils * 300)
    xs = amplitude * np.sin(2 * np.pi * num_coils * (ys - y0_corrigido) / length)
    return xs, ys


def init():

    y = positions_over_time[0]
    x = np.zeros(n)

    spring_x = []
    spring_y = []

    for i in range(n - 1):
        xs, ys = spring_curve(x[i], y[i], x[i + 1], y[i + 1])
        spring_x.extend(xs)
        spring_y.extend(ys)

    first_point.set_data(0, y[0])
    middle_points.set_data(np.zeros(n - 2), y[1:-1])
    last_point.set_data(0, y[-1])

    spring_lines.set_data(spring_x, spring_y)


    return first_point, middle_points, last_point, spring_lines

def update(frame):
    if is_running['value'] and current_frame['index'] < len(time_points):
        y = positions_over_time[current_frame['index']]
        x = np.zeros(n)

        first_point.set_data(0, y[0])
        middle_points.set_data(np.zeros(n - 2), y[1:-1])
        last_point.set_data(0, y[-1])

        spring_x = []
        spring_y = []

        for i in range(n - 1):
            xs, ys = spring_curve(x[i], y[i], x[i + 1], y[i + 1])
            spring_x.extend(xs)
            spring_y.extend(ys)

        spring_lines.set_data(spring_x, spring_y)

        current_frame['index'] += 1

    return first_point, middle_points, last_point, spring_lines

ax_play = plt.axes([0.2, 0.05, 0.2, 0.075])
btn_play = Button(ax_play, 'Play')

ax_reset = plt.axes([0.6, 0.05, 0.2, 0.075])
btn_reset = Button(ax_reset, 'Reset')

def start_animation(event):
    is_running['value'] = True

def reset_animation(event):
    is_running['value'] = False
    current_frame['index'] = 0
    init()
    plt.draw()

btn_play.on_clicked(start_animation)
btn_reset.on_clicked(reset_animation)

ani = animation.FuncAnimation(fig, update, frames=len(time_points), init_func=init,
                              blit=True, interval=20)

plt.title('Simulação Visual da Queda do Slinky - Caso Discreto Poroso', x=-0.4)
plt.legend()
plt.show()
