from tqdm import tqdm
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


ATTRACTOR_POINTS_X = [0, 50, 100, 0, 100, 0, 50, 100]
ATTRACTOR_POINTS_Y = [100] * 3 + [50] * 2 + [0] * 3


def walk(coords, last_pos):
    direction = random.choice(list(range(8)))
    coords[last_pos][0] = (coords[last_pos - 1][0] + 2*ATTRACTOR_POINTS_X[direction])/3
    coords[last_pos][1] = (coords[last_pos - 1][1] + 2*ATTRACTOR_POINTS_Y[direction])/3


def generate_carpet(x_initial, y_initial, n_steps=1000):
    coords = np.zeros((n_steps, 2))
    coords[0][0] = x_initial
    coords[0][1] = y_initial
    print("Generating data...")
    for i in tqdm(range(1, n_steps)):
        walk(coords, i)
    return coords


def update(num, scatter, text):
    # Take coordinates from global namespace to avoid it's passing to "update"
    # on every call
    scatter.set_offsets(coords[:num])
    text.set_text(f"Iteration: {num}")
    return scatter, text,


duration = int(input("Enter number of algorithm steps (0 < integer < 100000): "))
speed = int(input("Enter animation speed (0 < integer < 1000): "))
if speed < 0 or speed > 1000:
    print("Invalid speed value\nIt will be set to 10")
    speed = 10
if duration < 0 or duration > 1e5:
    print("Invalid duration value\nIt will be set to 100000")
    duration = 100000


fig, ax = plt.subplots()
plt.xlim(0, 100)
plt.ylim(-15, 100)
# Initial triangle
coords = generate_carpet(70, 50, duration)
scatter = ax.scatter([0], [0], s=4)
text = ax.text(3, -10, "Iteration: 0")
anim = FuncAnimation(fig, func=update, frames=range(1, duration, speed),
                     fargs=(scatter, text), blit=True, interval=1)
plt.show()
