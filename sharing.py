#!/usr/bin/env python3

from multiprocessing import Process
import multiprocessing

def cube():
    my_numbers[0] = 3
    for x in my_numbers:
        print(x*x*x)

if __name__ == '__main__':
    #multiprocessing.set_start_method('spawn')
    my_numbers = [1,2,3,4,5,6]
    p = Process(target=cube)
    p.start()
    p.join()
    print(my_numbers)
    cube()
    print(my_numbers)
