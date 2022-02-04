#!/usr/bin/env python3

from multiprocessing import Process
import random
import numpy as np

def random_walk(seed, num):
    stepsize = 0.01
    random.seed(seed)
    results = []
    for trial in range(num):
        x = 0
        y = 0
        z = 0
        for step in range(10000):
            phi = 2 * np.pi * random.random()
            theta = np.arccos(2 * random.random() - 1)

            x += stepsize * np.cos(phi) * np.sin(theta)
            y += stepsize * np.sin(phi) * np.sin(theta)
            z += stepsize * np.cos(theta)
        results.append([x,y,z])

    mean = 0
    for result in results:
        mean += np.sqrt(result[0]*result[0] + result[1]*result[1] + result[2]*result[2])
    print(mean / num)

if __name__ == "__main__":
    procs = [Process(target=random_walk, args=(i, 100)) for i in range(16)]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()
