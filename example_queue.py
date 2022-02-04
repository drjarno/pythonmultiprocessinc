#!/usr/bin/env python3

import multiprocessing as mp

# Read data for each file in the file list
def reader(filenames, q):
    for filename in filenames:
        with open('data/' + filename) as f:
            print(filename)
            data = f.read().lower()
            q.put(data)

# Do some analysis on the data from one file
def analyzer(q,r):
    data = q.get()
    hist = {}
    for letter in data:
        try:
            if letter in hist:
                hist[letter] += 1
            else:
                hist[letter] = 1
        except:
            pass
    hist = sorted(hist.items(), key=lambda x:x[1], reverse=True)[:5]
    r.put(hist)

if __name__ == "__main__":
    filenames = [
         'Frankenstein.txt',
         'Pride and Prejudice.txt',
         'The Adventures of Sherlock Holmes.txt',
         'The Great Gatsby.txt',
         'The Scarlet Letter.txt',
         'Ulysses.txt'
    ]

    # Create a queue. The read_process Process will read the file and place it in here
    q = mp.Queue()
    read_process = mp.Process(target=reader, args=(filenames, q))
    read_process.start()

    # Processes cannot return data so use another queue to get the data back out
    results = mp.Queue()

    # Create one process per file. These will run while the other files are still being read and will run
    # in parallel.
    analyzer_processes = [mp.Process(target=analyzer, args=(q,results)) for _ in filenames]
    for p in analyzer_processes:
        p.start()

    # Wait for the read_process to finish
    read_process.join()

    # Get the results back from the analyzer processes
    for _ in filenames:
        print(results.get())

    # Wait for the analyzer processes to finish
    # Note that they have already finishes since we use .get() on the result queue. This just makes it official
    for p in analyzer_processes:
        p.join()
