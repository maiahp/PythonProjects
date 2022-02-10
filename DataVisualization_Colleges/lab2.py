# Maiah Pardo
# 4/25/19
# CIS 41B
# Lab 2

'''This file is a tkinter user interface and imports the College class in order to present it's data'''


import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import  tkinter.messagebox as tkmb
#IMPORT THE ABOVE FIRST IN THIS EXACT ORDER

# only import college after the stuff above
from college import College
import sys
import os


def main():
    c = College(1971, 2018) # to change filename, keyword is 'filename='
    c.plotTuitionTrend()
    c.plotRoomBoardTrend()
    c.plotPaths()

#main()


def gui2fg():
    '''Brings tkinter GUI to foreground on Mac. Call gui2fg() after creating main window and before mainloop() start'''
    if sys.platform == 'darwin':
        tmpl  = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))


''' DialogWin: a class that inherits from tk TopLevel to display a window that allows user to enter a graduation year '''
class DialogWin(tk.Toplevel):
    ''' constructor: creates a window in order to collect user input and call '''
    def __init__(self, master, college):
        super().__init__(master) # creates toplevel window, where master=mainWin
        self.resizable(False, False) # the window is not resizeable
        F = tk.Frame(self) # create a frame, master=self, exists in self window (DialogWin)
        F.grid()
        L = tk.Label(F, text="Enter year of graduation or click and press Enter for latest year ") # create label for prompt inside of frame, master=frame
        L.grid() # automatically (row=0,column=0)

        ''' checkGradYearToPlot: call back function, checks that gradYear is a valid year & passes gradYear to DisplayPlots class to plot'''
        def checkGradYearToPlot(event): # callback function
            gradYear = userInput.get()
            # if gradYear is a valid year, you pass gradYear to DisplayPlots class

            if gradYear == '': # no user input, pressed Enter Key
                gradYear = college.endYear
                entry.insert(1, gradYear) # shows end year in text box
            else:
                try:
                    gradYear = int(gradYear.strip()) # strip white space, convert to int
                    if len(str(gradYear)) is not 3:
                        if gradYear < college.startYear+3 or gradYear > college.endYear: # if year is invalid
                            raise ValueError("Year must be 4 digits between {} and {}".format(college.startYear+3, college.endYear))
                except ValueError as ex:
                    tkmb.showerror("Error", ex, master=self, icon='warning')  # A messagebox: master=self, self window inaccessible until user clicks ok (parent=self makes error pop up under self window)
                    entry.delete(0, tk.END)  # clears out the entry widget (because it is a callback fcn, it recognizes "entry" before initialized)
                    return  # blank return exits checkValidYear method (meaning year is invalid)
            # if gradYear is a valid year typed in by user, method continues:
            displayPlot = DisplayPlots(master, college, 3) # create displayPlots class instance variable (master=mainWindow) # ERROR: dialog win should only get the user input. It should not do the plotting. The main window does the plot. This also causes an empty window to appear first before the plot window.
            displayPlot.setGradYear(gradYear)
            displayPlot.plot() # call display plots method to plot graph 3
            self.after(1000) # delay dialog window closing so that user can see input in textbox
            self.destroy()  # close dialog window

        userInput = tk.StringVar()  # create StringVar to store user input
        entry = tk.Entry(F, textvariable=userInput) # create entry box for user input
        entry.grid(row=0, column=1) # sits next to Label
        entry.bind("<Return>", checkGradYearToPlot) # the callback fcn runs when user hits <Return> key (Enter key)

        # make window modal - no access to mainWindow when self is open (master=mainWin)
        self.focus_set()  # doesn't allow mainwin to be accessed - sets the "focus" on a window
        self.grab_set()  # doesn't allow mainwin to be accessed - only allows this window to be accessed
        self.transient(master=master) # presents both window as one window in bottom bar to user (so as not to access mainwin)


''' DisplayPlots: a class that inherits from tk TopLevel to display a window with a matplotlib graph from College Class'''
class DisplayPlots(tk.Toplevel):
    ''' constructor: creates topLevel window '''
    def __init__(self, master, college, plotChoice):
        super().__init__(master) # create a toplevel window where the master = mainWin
        self.resizable(False, False) # the window is not resizeable
        self.master = master # master = MainWin
        self.plotChoice = plotChoice
        self.college = college

    ''' setGradYear: sets grad year as attribute to class '''
    def setGradYear(self, gradYear): # will only be used when plot 3 is to be graphed from DisplayWin.
        self.gradYear = gradYear

    ''' plot: plots a graph in the topLevel window the constructor (self) created '''
    def plot(self):
        fig = plt.figure(figsize=(12,8)) # create matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self) # create canvas that matplotlib figure will be plotted in. For widgets, their master is the window they show up in.

        taskDict = {1: self.college.plotTuitionTrend, 2: self.college.plotRoomBoardTrend, 3: lambda: self.college.plotPaths(self.gradYear)}
        taskDict[self.plotChoice]()  # gradYear is already an int when it is set in setGradYear by DialogWin class

        canvas.get_tk_widget().grid() # position the canvas in the window
        canvas.draw()


''' MainWin: a class that inherits from Tk to display three buttons to the user in order to do different tasks '''
class MainWin(tk.Tk): # Main Window, inherit from tkinter Tk class
    ''' constructor: creates main window with three buttons'''
    def __init__(self):
        super().__init__() # creates MainWin window

        self.title("College Pricing")
        self.configure(bg = 'white') # color of window background
        self.minsize(440, 50) # this is the minimum size the user can make the window
        self.maxsize(840, 300) # this is the max size the user can make the window
        self.geometry("440x50") # this is the size of the window when it first opens

        tk.Button(master=self, text="Tuition Trend", command=lambda: self.PlotGraphs(1)).grid(row=1, column=1) # we only use grid(): the cell size of the button(area it sits in)
        tk.Button(master=self, text="Room and Board Trend", command=lambda: self.PlotGraphs(2)).grid(row=1, column=2) #padx & pady is the padding on x,y axis of the button
        tk.Button(master=self, text="Total Cost for 4 Years", command=self.Dialog).grid(row=1, column=3)

        self.rowconfigure(1, weight=1) # as window expands: row 1 is 'weighted', moves down (all buttons in row1)
        self.columnconfigure(1, weight=1) # as window expands: col 1 is 'weighted' & moves sideways (button1)
        self.columnconfigure(2, weight=1) # as window expands: col 2 is 'weighted' & moves sideways (button2)
        self.columnconfigure(3, weight=1) # as window expands: col 3 is 'weighted' & moves sideways (button3)

        try:
            self.college = College() # instantiate College class object (data analysis object)
        except Exception as ex: # make sure that you are checking for all errors here, or only IOError?             # ERROR: CHECK FOR A SPECIFIC EXCEPTION
            tkmb.showerror("Error", ex, parent=self, icon='warning') # A messagebox: parent=self because self=master. parent=master makes master inaccessible to user until user clicks OK on messagebox
            self.destroy() # destroys all main window once user clicks OK. we want to destroy mainWindow if there is an exception from college class

    ''' PlotGraphs: calls DisplayPlots Class to plot the graph that the user chooses '''
    def PlotGraphs(self, plotChoice):
        DisplayPlots(self, self.college, plotChoice).plot() # displayplots(master=self(MainWin), collegeObj, plotChoice)

    ''' Dialog: calls DialogWin Class to user when user chooses "Total Cost for 4 Years" button '''
    def Dialog(self):
        DialogWin(self, self.college) # give Dialog win a master=self (master=MainWin)

app = MainWin() # start and end year for college
gui2fg()
app.mainloop()


''' 
Data Science Analysis: (Extra Credit)

The most cost effective way to earn a four-year degree is by attending a two-year public college for the first two years
of college and transferring to a a four-year public university for the last two years. In order of least cost to highest
cost, the options are ranked: 
1) Two-year public college and a transfer to a four-year public college
2) Four-year Public College
3) Two-Year Public and a transfer to a four-year private college
4) Four-year private college

Average Tuition by Year for Each Path (In 2018 dollar): 

1) In 2018:
    1) 2-year public & transfer to 4-year public: $27,710
    2) 4-year public: $40,590
    3) 2-Year Public & transfer to 4-year private: $78,760
    4) 4-year private: $140,780

2) In 2014:
    1) 2-year public & transfer to 4-year public: $26,040
    2) 4-year public: $38,020
    3) 2-Year Public & transfer to 4-year private: $72,360
    4) 4-year private: $128,580

3) In 2012:
    1) 2-year public & transfer to 4-year public: $24,930
    2) 4-year public: $35,840
    3) 2-Year Public & transfer to 4-year private: $69,170
    4) 4-year private: $124,050
    
4) In 2008:
    1) 2-year public & transfer to 4-year public: $20,670
    2) 4-year public: $29,310
    3) 2-Year Public & transfer to 4-year private: $62,390
    4) 4-year private: $111,460

5) In 1990:
    1) 2-year public & transfer to 4-year public: $10,470
    2) 4-year public: $13,790
    3) 2-Year Public & transfer to 4-year private: $38,930
    4) 4-year private: $68,210


I chose the 5 sample years: 2018, 2014, 2012, 2008, 1990. 
The first four years (2018, 2014, 2012, 2008) are the most recent years in a four year sequence. These years show that 
for every year there is a rise in the cost of all college paths.
Between 2008 and 2018, the percent difference for each path's cost:
1) Price of 2-year public & transfer to 4-year public increased by: 34.1% 
2) Price of 4-year public increased by: 38.5%
3) Price of 2-Year Public & transfer to 4-year private increased by: 26.2%
4) Price of 4-year private increased by: 26.3% 

We see here that attending a 4-year public college has the largest percent increase between 2008 and 2018. 
The smallest percent increase is the price of attending a 2-year public college and transferring to a 4-year private.

I chose the year 1990 so that we could look at the percent difference between the most recent year, 2018 and 1990.
This will let us look at how much the prices have jumped over a longer period of time.
Between 2018 and 1990, the percent difference for each path's cost:
1) Price of 2-year public & transfer to 4-year public increased by: 164.7% 
2) Price of 4-year public increased by: 194.3%
3) Price of 2-Year Public & transfer to 4-year private increased by: 102.3%
4) Price of 4-year private increased by: 106.4% 

We see here that the largest jump in price is the price of attending a 4-year public college, and the smallest jump in 
price is the cost of attending a 2-year public and transferring to a 4-year private college.

The cost of attending a 4-year public college has the largest increase in cost over the last 10 years and also over the 
last 28 years. The cost of attending a 2-year public college and transferring to a 4-year private has the smallest 
increase in cost over the last 10 years and also the last 28 years. In future years, it is likely that attending a 
2-year public college and transferring to a 4-year private college will be the cheapest option for students, however it 
is currently the most cost effective for students to attend a 2-year public college and transfer to a 4-year public 
college. 

'''





'''
my notes:

-Master of all plots is mainWin, master of dialog win is mainWin
this is because the textbox window will close once the graph is displayed. If textbox was the master of the plot window, then plot window would also close
this is why the plot windows master must be mainWin (also textbox's master must be mainWin)

-on window of graphs: resizable(horizontal_boolean(True or False), vertical_boolean) make sure that graph can't be pushed out of shape

-self.wait_window(dWin) # while dialogWin is open, the code below this line (in this method) waits until window is closed to execute. If there is no self.destroy(), this will wait forever
'''