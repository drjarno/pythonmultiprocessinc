#!/usr/bin/env python3

import threading

def f(x):
    for i in range(1000000000):
        x = x + 1
    return x*x

if __name__ == "__main__":
    threading.Thread(target=f, args=(1,)).start()
    threading.Thread(target=f, args=(2,)).start()
    threading.Thread(target=f, args=(3,)).start()
