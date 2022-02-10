
'''
for i in range(0,5,2):
    print(i)
    '''
'''
import numpy as np


# array slicing test (viewing) similar to string slicing whereas [startIndex:endIndex-1]
arrL = [['a','b','c','d','e'],['f','g','h','i','j'],['k','l','m','n','o'],['p','q','r','s','t']]

arr = np.array(arrL)
print(arr)

print(arr[2,3])

print(arr[:3,2])

'''

'''
import os
import sys
import tkinter as tk


def gui2fg():
    #Brings tkinter GUI to foreground on Mac. Call gui2fg() after creating main window and before mainloop() start
    if sys.platform == 'darwin':
        tmpl  = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))


win = tk.Tk() # initialize win as Tk object
win.title("GUI exercise") # title of window
win.geometry("500x100") # 500 width, 100 height


entryText = tk.StringVar()
choiceText = tk.StringVar()
choiceText.set("Name")


def getInput(event):
    print("Got it. Your", choiceText.get(), "is", entryText.get())

tk.Label(win, text="Part1 - label and entry objects").grid(row=0)
F = tk.Frame(win)
F.grid()
L=tk.Label(F, textvariable=choiceText)
L.grid(row=0, column=0)
E=tk.Entry(F, textvariable=entryText)
E.grid(row=0, column=1)
E.bind("<Return>", getInput)



#add two radio buttons: Name, Major. Configure the buttons such that when the user clicks on a button,
# the getInput function runs and prints the proper response.

tk.Label(win, text="Part2 - radio buttons: Type info in textbox, then choose option").grid(row=2)
tk.Radiobutton(win, text="Name", variable=choiceText, value="Name", command=lambda : getInput(choiceText)).grid(row=3)
tk.Radiobutton(win, text="Major", variable=choiceText, value="Major", command=lambda: getInput(choiceText)).grid(row=4)


import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk

def plotfct():
    plotWin = tk.Toplevel()
    fig = plt.figure(figsize=(4,4))
    x = np.linspace(-5,5,100)
    plt.plot(x, x**2, "-r")
    canvas = FigureCanvasTkAgg(fig, master=plotWin)
    canvas.get_tk_widget().grid()
    canvas.draw()

tk.Label(win, text="Part3 - plotting").grid(row=5)
tk.Button(win, text="x^2", command=plotfct).grid(columnspan=2, row=6, sticky='e')


win.mainloop() # starts up the window

'''





'''
class mainWindow(tk.Tk): # inherit from tkinter Tk class
    def __init__(self):
        super().__init__()
        self.title('College Pricing Plots')
        tk.Button(self, text="Tuition Trend", command = tuitionWin()).grid()
        tk.Button(self, text="Room and Board Trend", command = self.tuitionWin()).grid()
        tk.Button(self, text="Total Cost for 4 Years", command = self.tuitionWin()).grid()

        gui2fg()  # call for mac
        self.mainloop() # window appears and stays open until X is clicked


class tuitionWin(tk.Toplevel): # inherit from tk TopLevel class
    def __init__(self):
        self.title("Sample Top Level Window is here!")

'''

'''
myL = ["well", "hello"]
print(myL[1])

STARTYEAR = 1971
ENDYEAR = 2018

year = 1

if year < STARTYEAR or year > ENDYEAR:
    print(year, " is valid") # this should print bec year > endyear

if year < STARTYEAR and year > ENDYEAR:
    print(year)
'''

innerDict = {1:'one', 2:'two', 3:'three', 4:'four'}
myDict ={"title1": innerDict, "title2": innerDict}
#print(myDict["title1"].keys())



def myMethod(name):
    print("hello", name,  "! it worked")

names = ['maiah', 'mollie', 'meee']
[myMethod(name) for name in names]