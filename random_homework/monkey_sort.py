import random
import time
import matplotlib.pyplot as plt


def is_sorted(array):
    sorted_ = True
    for i in range(len(array)-1):
        sorted_ &= (array[i] <= array[i + 1])
        if not sorted_:
            break
    return sorted_


def monkey_sort(array):
    while not is_sorted(array):
        random.shuffle(array)
    return array


def sd(array):
    mean = sum(array) / len(array)
    return (sum(map(lambda x: (x - mean)**2, array)) / (len(array) - 1))**0.5


times = []
for arr_len in range(2, 9):
    stat = []
    for _ in range(10):
        start = time.time()
        monkey_sort([random.random() for _ in range(arr_len)])
        stat.append(time.time() - start)
    times.append(stat)

means = list(map(lambda x: sum(x)/len(x), times))
sds = list(map(lambda x: sd(x), times))

plt.errorbar(range(2, 9), means, yerr=sds, ecolor="k", capsize=5)
plt.xlabel("Array length")
plt.ylabel("Time, s")
plt.xticks(range(2, 9), range(2, 9))
plt.show()
