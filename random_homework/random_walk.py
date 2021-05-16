import random
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def walk(coords, last_pos):
    direction = random.choice(["left", "up", "right", "down"])
    coords[last_pos] = coords[last_pos - 1]
    if direction == "left":
        coords[last_pos][0] -= 0.4
    elif direction == "up":
        coords[last_pos][1] += 0.4
    elif direction == "right":
        coords[last_pos][0] += 0.4
    elif direction == "down":
        coords[last_pos][1] -= 0.4


def generate_random_path(x_initial, y_initial, n_steps=1000):
    coords = np.zeros((n_steps, 2))
    coords[0][0] = x_initial
    coords[0][1] = y_initial
    print("Generating data...")
    for i in tqdm(range(1, n_steps)):
        walk(coords, i)
    return coords


def update(num, scatter_plot):
    # Take coordinates from global namespace to avoid it's passing to "update"
    # on every call
    scatter_plot.set_offsets(coords[:num])
    return scatter_plot,


duration = int(input("Enter number of algorithm steps (0 < integer < 10000000): "))
speed = int(input("Enter animation speed (0 < integer < 1000): "))
if speed < 0 or speed > 1000:
    print("Invalid speed value\nIt will be set to 100")
    speed = 100
if duration < 0 or duration > 1e7:
    print("Invalid duration value\nIt will be set to 1000000")
    duration = 1000000

fig, ax = plt.subplots()
plt.xlim(-100, 100)
plt.ylim(-100, 100)
coords = generate_random_path(0, 0, duration)
scatter = ax.scatter([0], [0], s=4, alpha=0.1)
anim = FuncAnimation(fig, func=update, fargs=(scatter,),
                     frames=range(1, duration, speed), blit=True, interval=1)
plt.show()
