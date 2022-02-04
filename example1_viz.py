#!/usr/bin/env python3

from multiprocessing import Process
import random
import numpy as np
import pandas as pd

def random_walk(seed, num):
    stepsize = 0.01
    random.seed(seed)
    df = pd.DataFrame(columns=["p"+c+str(i) for i in range(num) for c in ['x','y','z']])
    for trial in range(num):
        x = 0
        y = 0
        z = 0
        path = []
        for step in range(10000):
            phi = 2 * np.pi * random.random()
            theta = np.arccos(2 * random.random() - 1)

            x += stepsize * np.cos(phi) * np.sin(theta)
            y += stepsize * np.sin(phi) * np.sin(theta)
            z += stepsize * np.cos(theta)
            if step % 10 == 0:
                path.append([x,y,z])
        df['px'+str(trial)] = [p[0] for p in path]
        df['py'+str(trial)] = [p[1] for p in path]
        df['pz'+str(trial)] = [p[2] for p in path]
    df['t'] = range(1000)
    df.to_csv("trials.csv")

if __name__ == "__main__":
    random_walk(0,6)
