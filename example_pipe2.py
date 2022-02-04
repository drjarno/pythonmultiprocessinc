#!/usr/bin/env python3

import multiprocessing as mp
import sys

# Create a zigzag pattern for the initial state
def initial_state(x):
    if x < 2048/2:
        return x
    elif x < 4096/2:
        return 4096/2 - x
    elif x < 6144/2:
        return x - 4096/2
    elif x < 8192/2:
        return 8192/2 - x
    elif x < 10240/2:
        return x - 8192/2
    elif x < 12288/2:
        return 12288/2 - x
    elif x < 14336/2:
        return x - 12288/2
    elif x < 16384/2:
        return 16384/2 - x
    elif x < 18432/2:
        return x - 16384/2
    elif x < 20480/2:
        return 20480/2 - x
    else:
        return 0

# This simulation function runs on only part of the domain
def simulate(num, size, steps, left_pipe, right_pipe, output_pipe):
    # Initialize the simulation domain with the initial state.
    # Add one cell the left and right to send/receive to/from the neighbour process
    domain = [initial_state(x + num*size - 1) for x in range(size+2)]

    # Create the same subdomain for the future state
    future_domain = [0 for x in range(size+2)]

    domain[0] = 1000
    domain[-1] = 0
    coeff = 0.4
    for t in range(steps):
        # Simulate
        for i in range(1, size+1):
            future_domain[i] = domain[i] + coeff * (domain[i-1] - 2*domain[i] + domain[i+1]);

        # Swap the buffers so that "domain" contains the data for the current time step
        tmp = domain
        domain = future_domain
        future_domain = tmp

        # Exchange the border values
        if left_pipe != None:
            left_pipe.send(domain[1])
            domain[0] = left_pipe.recv()
        if right_pipe != None:
            right_pipe.send(domain[-2])
            domain[-1] = right_pipe.recv()

        if t % 1000 == 0:
            output_pipe.send([num, domain[1:-2]])

if __name__ == "__main__":
    timesteps = 3000000
    size = 20480//2  # Funny number, but divisible by 2, 4, 8, and 16. Makes subdomain_size whole number
    subdomain_size = int(size / mp.cpu_count())

    with open("initial.csv", 'w') as f:
        for i in range(size):
            f.write(f"{i},{initial_state(i)}\n")

    pipes = [mp.Pipe() for _ in range(mp.cpu_count()-1)]
    output_pipe = mp.Pipe()
    processes = []
    processes.append(mp.Process(target=simulate, args=(0, subdomain_size, timesteps, None, pipes[0][0], output_pipe[0])))
    for i in range(mp.cpu_count()-2):
        processes.append(mp.Process(target=simulate, args=(i+1, subdomain_size, timesteps, pipes[i][1], pipes[i+1][0], output_pipe[0])))
    processes.append(mp.Process(target=simulate, args=(mp.cpu_count()-1, subdomain_size, timesteps, pipes[-1][1], None, output_pipe[0])))

    for proc in processes:
        proc.start()

    for t in range(timesteps // 1000):
        with open(f"output_{t:06d}.csv", 'w') as f:
            i = 0
            # Order of pipes is not guarenteed, so sort by process number
            output_states = sorted([output_pipe[1].recv() for proc in processes])
            for process_output in output_states:
                for y in process_output[1]:
                    f.write(f"{i},{y}\n")
                    i += 1

    for proc in processes:
        proc.join()
