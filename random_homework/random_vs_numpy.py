import random
import time
import numpy as np
import matplotlib.pyplot as plt


random_times = []
numpy_times = []
array_lengths = [10**x for x in range(8)]
for array_len in array_lengths:
    start = time.time()
    [random.uniform(0, 1) for _ in range(array_len)]
    random_times.append(time.time() - start)

    start = time.time()
    np.random.uniform(0, 1, array_len)
    numpy_times.append(time.time() - start)

plt.plot(array_lengths, random_times, label="random")
plt.plot(array_lengths, numpy_times, label="numpy")
plt.xlabel("Array length")
plt.ylabel("Time, s")
plt.legend()
plt.show()
