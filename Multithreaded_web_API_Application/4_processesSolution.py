# Module 4 - processes,  Solution file

import multiprocessing as mp
import os
import time
import random
random.seed()


# 1. The following code shows how to creaate and run processes.
# a. How many processes run in the following code?   1 main process and 4 child processes
# b. predict the answer to the questions, then run the code to check your answer

def add1(n):
    newN = n + 1
    print("n:", n, "newN:", newN, "PID:", os.getpid(), "name:", mp.current_process().name)
                                     # getting PID and name of process

if __name__ == '__main__':   # this is needed for multiprocessing so our code is platform independent
    numbers = [10, 20, 30]
    procs = []
    
    for n in numbers:        # 3 times for 3 child processes
        p = mp.Process(target=add1, args=(n,))
        procs.append(p)
        p.start()
    
    namedP = mp.Process(target=add1, args=(-1,), name='named process')    # 4th child process that's named
    namedP.start()
    
    for p in procs:
        p.join()
    namedP.join()
    print("done1")


# 2. Check process status
# predict the status that's printed in the code below, then run the code to check your answer

def slowFunction():
    print("Start slow function")
    time.sleep(1)
    print("End slow function")

if __name__ == '__main__':
    p = mp.Process(target=slowFunction)
    print("main start: p alive status", p.is_alive())         # False
    
    p.start()
    print("p start: p alive status", p.is_alive())            # True

    p.join()
    print("main join: p alive status", p.is_alive(), ", p exit status", p.exitcode)    # False, 0 exitcode


# 3. Processes and shared resources
# Recall that we used a lock to prevent a race condition when 4 threads update a Counter object
# Now we do the same with 3 processes, and we observe the total count at the end
#    Answer: call at the end is 0 because each child process has a different memory space than the
#            parent process. None of the child processes updates the parent's Counter object, they
#            update their own Counter object.

class Counter() :
    def __init__(self) :
        self.counter = 0
        self.lock = mp.Lock()
    def inc(self) :
        with self.lock :
            for x in range(200000):    # 200,000 iterations
                self.counter += 1
        print(self.counter, os.getpid())   # each child process ends up with its own count of 200,000
    def printCount(self) :
        print(self.counter)    
    
if __name__ == '__main__':
    procs = []
    c = Counter()
    for i in range(3):
        p = mp.Process(target=c.inc, args=())
        procs.append(p)
        p.start()
    for p in procs:
        p.join()
    c.printCount()        # but count here is 0 because each process has its own memory space
                          # and none of the child processes incremented main process' count


# 4. What count value should be printed at the end? 
# What count value is printed? Why?
#   Answer: without a lock, the count value should be 200,000 because each of the 4 processes runs 50,000 times to increment num
#           but the count is below 200,000 because there is a race condition where all the processes try to write to the same file.
#  The fix is with a lock, as shown below.

def printFile(lock):     # accepts a lock
    with lock :          # can only read / write to file if lock is obtained
        with open("counter.txt","r") as fh :       
            num = fh.readline()
        for i in range(50000) :
            num = int(num) + 1
        with open("counter.txt","w") as fh :
            fh.write(" {:d}".format(num))
        
if __name__ == '__main__':
    lock = mp.Lock()       # parent process owns the lock
    procs = []
    with open("counter.txt", "w") as fh :
        fh.write("0")               
    for i in range(4) :
        p = mp.Process(target=printFile, args=(lock,))     # pass the lock to each child process
        procs.append(p)
        p.start()
    for p in procs :
        p.join()
    with open("counter.txt") as fh :
        print(fh.readline())
        

# 5. use Event to signal conditions
# What will be printed?    Answer: shown below with numerical order

def waitToPrint(e):
    e.wait()
    print(mp.current_process().name + ": printing...")        #3
        
def waitWithTimeout(e, t):
    e.wait(t)
    if e.is_set() :
        print(mp.current_process().name + ": printing...")
    else :
        print(mp.current_process().name + ": no printing")      #2

if __name__ == '__main__':
    e = mp.Event()
    p1 = mp.Process(name='wait_until_set', target=waitToPrint, args=(e,))  
    p1.start()

    p2 = mp.Process(name='wait_with_timeout', target=waitWithTimeout, args=(e, 1)) 
    p2.start()

    print("main: before setting Event")       #1
    time.sleep(2)
    e.set()
    print("main: event is set")               #3

    p1.join()
    p2.join()
    print("main: done")                       #4


# 6. Add to the code below to use  a queue as the data buffer for producer / consumer,
# then print all the numbers that are produced.

def randNum(length, outputQ) :          # accept queue from main process
    num = 0
    for i in range(length) :
        num += (10 ** i) * random.randint(0,9)
    outputQ.put(num)                    # put data into the queue, each child process is a producer

if __name__ == '__main__' :
    outputQ = mp.Queue()                   # create a queue in main process
    pList = []
    
    for i in range(3) :
        p = mp.Process(target=randNum, args=(5, outputQ))      # pass the queue to each child process
        pList.append(p)
        p.start()
    
    for p in pList:
        p.join()
    
    print(*(outputQ.get() for i in range(3)))        # after all child processes are done, main process is consumer, getting data from queue



# 7. Use a Pool to get multiple processes to run the same function but with different args
# various tasks to be run:
def square(x):
    time.sleep(4)       
    return x * x

def add(args) :         
    time.sleep(1)
    return args[0] + args[1]

def printResult(result) :
    print("result:", result)

if __name__ == '__main__' :
    pool = mp.Pool(processes=4)
    
    nums1 = [10,11,12,13,14]
    nums2 = [1, 2, 3, 4, 5]
    args = [(10,1), (11,2), (12,3), (13,4), (14,5)]   
    
    
    # a. what does this code print?     Prints the squares of nums1
    results = pool.map(square, nums1)          
    print("square results", results)
    
    
    
    # b. Add code below to run the add function in parallel.
    # which of the lists above can be used as input arguments to add?   args, because each element is a tuple of 2, matching what add needs
    results = pool.map(add, args)
    print("add results", results)
    print("main done")       # this is printed after the results
                             # because map is blocking
    
 
    
    # c. Add to the code to print the results
    results = [pool.apply_async(square, args=(x,)) for x in range(1,10)]            # ERROR: use pool.map since all processes do the same task!
    output = [r.get() for r in results]      # apply_async returns a list of result objects, we need to use get() to get the actual data
    print(output)
    # or shorter:   print (*(r.get() for r in results))
    
    
    
    # d. What does this print?
    for x in range(10,15) :
        pool.apply_async(square, args=(x,), callback=printResult)    
    # prints:
    # result: 100
    # result: 121
    # result: 144
    # result: 169
    # result: 196     
    
    pool.close()
    pool.join()

    
