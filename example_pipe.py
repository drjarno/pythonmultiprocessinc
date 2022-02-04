#!/usr/bin/env python3

import multiprocessing as mp

def simulate(num, left_pipe, right_pipe):
    if left_pipe != None:
        left_pipe.send('a')
        print(f"Process {num:2d} received from left:  " + left_pipe.recv())
    if right_pipe != None:
        right_pipe.send('b')
        print(f"Process {num:2d} received from right: " + right_pipe.recv())

if __name__ == "__main__":
    pipes = [mp.Pipe() for _ in range(mp.cpu_count()-1)]
    processes = []
    processes.append(mp.Process(target=simulate, args=(0, None, pipes[0][0])))
    for i in range(mp.cpu_count()-2):
        processes.append(mp.Process(target=simulate, args=(i+1, pipes[i][1], pipes[i+1][0])))
    processes.append(mp.Process(target=simulate, args=(mp.cpu_count() - 1, pipes[-1][1], None)))

    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()
