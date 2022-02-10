dict = {1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven'}

dict1={1:'one'}

#print(*dict1.keys())

#print(dict1.values())


import os
#print(os.getcwd()) # gets the current working directory (current directory that python file sits in)

from tkinter import filedialog
#dir = filedialog.askdirectory() # pops up a window to ask for directory from user
#print(dir)

#filename_and_directory = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("Text File", "*.txt"), ("all files", "*.*")))  # code to get filename that user chooses. os.getcwd() = get the current working directory of the .py file

#directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Please select a directory", filetypes=(("Text File", "*.txt")))  # code to get user chosen directory. os.getcwd() = get the current working directory of the .py file

'''

all_items = ['California: César E. Chávez National Monument', 'California: Death Valley National Park']

selected_items = [elem.split(":")[1].strip() for elem in all_items]  # splits by ":" and takes ":" out


print(selected_items)
'''


import threading
import time

def taskA():
    print('taskA')
    time.sleep(1)

def taskB():
    print('taskB')
    time.sleep(3)

def work(e):
    while e.isSet():
        taskA()
    taskB()

e = threading.Event()
e.set()
t = threading.Thread(target=work, args=(e,))
t.start()
start = time.time()
time.sleep(4)
e.clear()
t.join()
time.sleep(3)
print(time.time()-start)