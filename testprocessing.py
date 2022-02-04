#!/usr/bin/env python3

from multiprocessing import Pool

def f(x):
    for i in range(1000000000):
        x = x + 1
    return x*x

if __name__ == "__main__":
    with Pool(5) as p:
        print(p.map(f, [1,2,3]))
