# Maiah Pardo
# 5/9/19
# Lab 3

''' GUI: Reads from a database to display data to the user '''

import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter.messagebox as tkmb

import sqlite3

import sys
import os


def gui2fg():
    '''Brings tkinter GUI to foreground on Mac. Call gui2fg() after creating main window and before mainloop() start'''
    if sys.platform == 'darwin':
        tmpl  = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))


''' MainWin: a class that inherits from Tk to display three buttons to the user in order to do different tasks '''
class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()  # creates MainWin window

        # open connection with database
        database = "sqlite.db"
        self.conn = sqlite3.connect(database) # create a database connection
        self.cur = self.conn.cursor() # cursor object that points to database

        self.minsize(300, 50)  # this is the minimum size the user can make the window
        self.maxsize(600, 100)  # this is the max size the user can make the window
        self.geometry("300x50")  # this is the size of the window when it first opens
        self.rowconfigure(0, weight=1)  # as window expands: row 1 is 'weighted', moves down (all buttons in row1)
        self.columnconfigure(0, weight=1)  # as window expands: col 1 is 'weighted' & moves sideways (button1)
        self.columnconfigure(1, weight=1)  # as window expands: col 2 is 'weighted' & moves sideways (button2)
        self.columnconfigure(2, weight=1)  # as window expands: col 3 is 'weighted' & moves sideways (button3)

        self.title("High Tech Jobs")
        b1 = tk.Button(master=self, text="By Salary", command=lambda: self.plotData(0, self.select_record_from_table)).grid(row=0, column=0, padx=10, pady=10) #sticky=?
        tk.Button(master=self, text="By Growth Rate", command=lambda: self.plotData(1, self.select_record_from_table)).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(master=self, text="By Degree", command=lambda: self.dialog(self.select_record_from_table)).grid(row=0, column=2, padx=10, pady=10)

        ''' close_connection: call back function to close connection to database'''
        def close_connection(): # callbackfcn to close connection
            self.conn.close() # close connection
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", close_connection) # override when user clicks X, callbackfcn executes then main win closes

    ''' select_record_from_table: retreives a record(row) from a table in the database with an open connection'''
    def select_record_from_table(self, query_string, *args): # *args is a tuple that you can add to query string
        try:
            self.cur.execute(query_string, args)  # point cursor to a record(row) in a table using the query string
            return self.cur.fetchall()  # return the data
        except sqlite3.OperationalError as ex:
            tkmb.showerror("Error", ex, parent=self, icon='warning')  # messagebox: parent=self because self=master. parent=master makes master inaccessible to user until user clicks OK on messagebox
            self.conn.close()
            self.destroy() # exits GUI once user clicks OK. we don't continue if there is an exception from database

    ''' plotData: function that passes plot data from database to plot window'''
    def plotData(self, choice, getdatafcn): #callbackfcn: the button click event causes this function to run
        plotChoiceDict = {0 : "SELECT salary,occupation FROM job_data ORDER BY salary ASC;",
                          1 : "SELECT outlook,occupation FROM job_data ORDER BY outlook ASC;"} # sorted by salary, descending order
        titleChoiceDict = {0 : "SELECT salary FROM field_names;", 1 : "SELECT outlook FROM field_names;"}
        xLabelDict = {0 : "Dollars", 1: "Percentage"}

        title = [elem[0] for elem in getdatafcn(titleChoiceDict[choice])] # must unpack the title from a list of one tuple
        xlabel = xLabelDict[choice]
        dataList = getdatafcn(plotChoiceDict[choice]) # the plot data, dataList = [(occupation, salary), (occupation, salary), ]
        xData = [elem[0] for elem in dataList] # list of (occupation, salary) sorted by either salary or outlook
        yData = [elem[1] for elem in dataList]
        PlotWin(self, title, xData, yData, xlabel) # master = self (mainWin)

    ''' dialog: callback function that passes data from database to dialog window and then to display window'''
    def dialog(self, getdatafcn):
        edLevelRecords = [record for record in getdatafcn("SELECT id,level FROM education_level")] # returns [ (id, level), ]
        dWin = DialogWin(self, edLevelRecords) # choice (a number 1-4) = one of the ids of education_level table
        self.wait_window(dWin) # waits on Dialog Win to be closed before continuing code

        if dWin.getChoice() is not None:
            edLevel = [elem[0] for elem in getdatafcn("SELECT level FROM education_level WHERE id = ? LIMIT 1", str(dWin.getChoice()))] # select_record_from_table fcn turns choice into a tuple
            occupations = getdatafcn("SELECT occupation FROM job_data WHERE education_level_id = ? ORDER BY occupation ASC", str(dWin.getChoice()))
            DisplayWin(self, edLevel, occupations)


''' PlotWin: given plot data, this class creates a plot in a window'''
class PlotWin(tk.Toplevel):
    def __init__(self, master, title, xData, yData, xlabel):
        super().__init__(master) # create top level win, give it a master in constructor
        self.master = master # master = MainWin
        self.resizable(False, False)  # the window is not resizeable
        fig = plt.figure(figsize=(8, 8))  # create matplotlib figure
        plt.title(*title, fontsize=15) # unpack: title is a list of one elem
        plt.xlabel(xlabel, fontsize=12)

        plt.barh((1,2,3,4,5,6,7,8,9,10), xData)
        plt.yticks((1,2,3,4,5,6,7,8,9,10), yData, wrap=True, fontsize=8, verticalalignment='center') # np.arange(len(yData)) in x place (fontsize=)

        canvas = FigureCanvasTkAgg(fig, master=self)  # create canvas that matplotlib figure will be plotted in. For widgets, their master is the window they show up in.
        canvas.get_tk_widget().grid()  # position the canvas in the window
        canvas.draw()


''' DialogWin: presents a dialog of degree choices for the user to pick '''
class DialogWin(tk.Toplevel):
    def __init__(self, master, edLevelRecords):
        super().__init__(master)  # create top level win, give it a master in constructor
        self.master = master  # master = MainWin
        self.title("Choose entry degree")
        self.geometry("300x150")  # this is the size of the window when it first opens
        self.resizable(False, False) # the window is not resizeable
        self.choice = tk.StringVar() # var is a tk var

        # self._controlVar = tk.IntVar() # make sure that a radiobutton is selected when window opens
        # self._controlVar.set(1) # select the first radiobutton

        for id, record in edLevelRecords: # self.choice() is given value of an id (1,2,3,4) from education level table
            tk.Radiobutton(master=self, text=record, variable=self.choice, value=id).grid(row=id, column=0, padx=5, pady=5, sticky='w') # no command, radio button only captures a choice from user
        tk.Button(master=self, text="OK", command=self.clickedButton).grid(row=5, column=0, sticky='w')

        self.protocol("WM_DELETE_WINDOW", self.exitWin) # override when X is clicked, exitWin is called

        # window is modal - no access to other windows
        self.focus_set() # doesn't allow mainwin to be accessed - sets the "focus" on a window
        self.grab_set() # doesn't allow mainwin to be accessed - only allows this window to be accessed
        self.transient(master=master)  # presents both window as one window in bottom bar to user (so as not to access mainwin)

    ''' exitWin: overrides X when clicked in order to destroy self window and set the user's choice to None'''
    def exitWin(self): # if user clicked X on Dialog Window
        self.choice = None # set choice to None
        self.destroy()

    ''' getChoice: returns the user's choice'''
    def getChoice(self):
        return self.choice

    ''' clickedButton: called when user clicks OK button to set user's choice'''
    def clickedButton(self):# callbackfcn: once user clicks OK, destroy self window and return choice
        self.destroy() # closes self window
        self.choice = self.choice.get() # set self.choice to equal it's value, no longer a tk variable


''' DisplayWin: displays data from database to user based on user's choice'''
class DisplayWin(tk.Toplevel):
    def __init__(self, master, title, data):
        super().__init__(master)
        self.master = master
        self.title("Minimum Degree: " + str(*title))
        self.geometry("453x170")
        self.resizable(False, False)  # the window is not resizeable
        self.focus_set()  # focus is on self window when open

        LB = tk.Listbox(self, height=10, width=50) # create empty listbox that can contain 10 lines of text
        LB.grid(row=0, column=0, rowspan=10) # must do this line separately or you can't do LB.insert(), .grid() makes LB = None
        [LB.insert(tk.END, elem[0]) for elem in data]


win = MainWin()
gui2fg()
win.mainloop()
