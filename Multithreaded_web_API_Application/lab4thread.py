# Maiah Pardo
# 5/21/19
# Assignment 4

''' lab4thread: uses threads and web access to present parks data to the user '''

import json
import requests
import threading
import queue

import tkinter as tk
import tkinter.messagebox as tkmb
from tkinter import filedialog

import sys
import os

''' MainWin: Displays list of states to the user '''
class MainWin(tk.Tk):
    URL = "https://developer.nps.gov/api/v1/parks?stateCode={}&api_key={}"
    API_KEY = "FXy7q006a43S2DCWPnqhcErZPe3V53eCT8ZOfgdO"
    JSON_FILE = "states_hash.json"

    def __init__(self):
        super().__init__()  # creates MainWin window
        self.geometry("340x300") # window dimensions in pixels
        self.resizable(False, False)
        self.title("US National Parks")
        self.q = queue.Queue() # queue for the thread to pass to

        try: # open and returns a json file as a dictionary of key= state key, val= state name
            with open(self.JSON_FILE, 'r') as f:
                self.states_dict = json.load(f)
        except IOError:
            tkmb.showerror("Error", "Could not open " + str(self.JSON_FILE), icon='warning')
            self.destroy()

        tk.Label(self, text="Select up to 3 states", fg='black').grid() # create a label
        S = tk.Scrollbar(self) # create scrollbar
        S.grid(row=1,column=1, sticky= "NE"+"SE")
        LB = tk.Listbox(self, height=10, width=30, selectmode='multiple', yscrollcommand=S.set) # associate scrollbar w/ listbox
        LB.grid(row=1, padx=15, pady=15) # separate line, when you use .grid(), LB will be None
        S.config(command=LB.yview) # callback for listbox view function to change when scrollbar is moved


        print(*[state_name for state_name in self.states_dict.values()])
        print([state_name for state_name in self.states_dict.values()])

        LB.insert(tk.END, *[state_name for state_name in self.states_dict.values()]) # insert state names from states_dict into listbox
        tk.Button(master=self, text="OK", command=lambda: self.clickOK(LB)).grid() # when "OK" clicked, calls getData callback fcn given Listbox (contains selected choices)
        self.Label = tk.Label(self, text='', fg='black')
        self.Label.grid() # separate line so that L does not return None

    ''' refreshStatus: refreshes the Label at the bottom of MainWin with a new string'''
    def refreshStatus(self, text):
        self.Label.configure(text=text)  # add a new string to label
        self.update()  # update window (so that new text will show)

    ''' clickOK: checks user's selected choices are between 1 and 3 from listbox, then creates threads to call getData simultaneously with choices'''
    def clickOK(self, LB): # callback to 'OK' button
        index_selection = LB.curselection()
        threads = []
        list_q_data = [] # save data from queue in a list

        if len(index_selection) in [1,2,3]: # user selected 1, 2 or 3 choices
            selected_state_keys = [list(self.states_dict.keys())[index] for index in index_selection]  # list of state_keys of user's selected states
            # main thread starts:
            for state_key in selected_state_keys:  # task: use threads to call getData with state_key of user choices
                t = threading.Thread(target=self.getData, args=(state_key,))  # call start when you assign thread, the loop executes faster than the thread starts, so the thread's fcn call(param) - the param will have the same value BUT you can't do this because then t returns None
                t.start()
                threads.append(t)  # each time you append the thread object

            self.refreshStatus("Result: ") # add text to Label

            for t in threads:  # number of threads is number of times you wait for a result from the queue
                t.join() # waits until thread is done to continue (thread exited)
                thread_result = self.q.get()  # the data from the queue, (result of the thread)
                list_q_data.append(thread_result)  # save data from queue in a list
                text_string = self.states_dict[str(*(thread_result.keys()))] + ": " + str(thread_result[str(*(thread_result.keys()))]['total']) # ERROR: need to update the label as each thread is finished. This means the label update should be done before the t.join()   # state key = thread_result.keys() - 1 key, which is state name key, number of parks = thread_result[str(*(thread_result.keys()))]['total'] - 1 value, which is the num_parks value in inner data dict
                text = self.Label.cget("text") + text_string + "  "  # ERROR: Update for one state at a time as its thread is finished. Need to use a queue: each thread puts the count of state parks into the queue, and the main thread needs to loop and continuously fetch from the queue, as the threads are still running.  # create a new text string using Label's current string + new string / this is "state name: num parks" - thread_result['data'][0]['states']
                self.refreshStatus(text)

            # main thread done
            DisplayWin(self, self.states_dict, list_q_data)  # call DisplayWin when results from all selected states is done (when main thread is done)
        else: # user has not selected between 1 and 3 choices
            tkmb.showerror("Error", "Select 1 to 3 choices", icon='warning')  # messagebox

    ''' getData: gets data from URL and puts it into the queue'''
    def getData(self, state_key): # state = full state name
        try:
            response = requests.get(self.URL.format(state_key, self.API_KEY))
            data_dict = {}
            data_dict[state_key] = json.loads(response.text)  # loads: loads string into json dict
            self.q.put(data_dict)  # put data into the queue # ERROR: need to put the count of state park into the queue so it can get to the main thread.
        except ConnectionError:  # request failed
            tkmb.showerror("Error", "Failed to open URL", icon='warning')

''' DisplayWin: displays list of parks to the user '''
class DisplayWin(tk.Toplevel):
    def __init__(self, master, states_dict, chosen_states_data):
        super().__init__(master)  # create top level win, give it a master in constructor
        self.master = master # master is MainWin
        self.states_dict = states_dict
        self.chosen_states_data = chosen_states_data # data of chosen states,  {'state key' : {data_dict} }

        self.focus_set()  # doesn't allow mainwin to be accessed - sets the "focus" on a window
        self.grab_set()  # doesn't allow mainwin to be accessed - only allows this window to be accessed
        self.transient(master=master)  # presents both window as one window in bottom bar to user (so as not to access mainwin)

        self.geometry("550x280")  # window dimensions in pixels
        self.resizable(False, False)

        tk.Label(self, text="Select parks to save to file", fg='black').grid()  # create a label
        S = tk.Scrollbar(self)  # create scrollbar
        S.grid(row=1, column=1, sticky="NE" + "SE")
        LB = tk.Listbox(self, height=10, width=55, selectmode='multiple', yscrollcommand=S.set)  # associate scrollbar w/ listbox
        LB.grid(row=1, padx=15, pady=15)  # separate line, when you use .grid(), LB will be None
        S.config(command=LB.yview)  # callback for listbox view function to change when scrollbar is moved

        for state_data in self.chosen_states_data:
            for state_key in state_data: # state_data = the dict of [ {'state_key' : state_data_dict } ]
                for i in range(int(state_data[state_key]['total'])): # for i in range(number of parks) - loops thru lists of dicts inside data
                    LB.insert(tk.END, self.states_dict[state_key] + ": " + state_data[state_key]['data'][i]['fullName']) # "state name: name of park", have to get state name from outer dict bc inner dict has cases where there is more than one state key

        tk.Button(master=self, text="OK", command= lambda:self.clickedOK(LB)).grid()  # when "OK" clicked, calls getData callback fcn given Listbox (contains selected choices)
        self.protocol("WM_DELETE_WINDOW", self.exitWin)  # override when user clicks X

    ''' exitWin: callbackfcn when user exits self win, clears MainWin bottom status bar '''
    def exitWin(self):
        self.master.refreshStatus('') # refresh label with empty string, # you can also say: MainWin(self.master, '') but writing this way you don't have to pass "self" argument
        self.destroy()

    ''' clickedOK: callbackfcn, saves chosen parks data into a text file called parks.txt'''
    def clickedOK(self, LB):
        index_selection = LB.curselection() # tuple of user selected indexes
        all_items = LB.get(0,tk.END) # tuple of all strings from listbox choices
        selected_items = [all_items[index].split(":")[1].strip() for index in index_selection] # tuple user selected items (strings) from listbox, split into inner lists by ":", takes out ":", and only keeps index [1] (park name) and not state name

        # task: get park's names from user selected states (chosen_state_data) & compare with parks name from cursor selected choices.
        # if they match, grab all data from this park inside of chosen_states_data & print out the information into parks.txt

        if len(index_selection) != 0: # if there is 1 or more user choice
            contents = []
            for state_data in self.chosen_states_data:  # chosen_states_data = [ {state data dict}, {state data dict}, ... ]
                for state_key in state_data:
                    for i in range(int(state_data[state_key]['total'])):
                        if state_data[state_key]['data'][i]['fullName'] in selected_items:
                            contents.append(str(state_data[state_key]['data'][i]['fullName'] + ", " + self.states_dict[state_key] + "\n" + state_data[state_key]['data'][i]['description'] + "\n\n"))

            directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select a directory") # get user chosen directory. os.getcwd() = get the current working directory of the .py file
            if os.path.isdir(directory): # if directory exists (if no selected directory, directory='' )
                filepath = os.path.join(directory, "parks.txt")
                if os.path.isfile(filepath): # if file exists
                    tkmb.showwarning('Warning', 'parks.txt already exists in this location and will be overwritten', icon='warning')
                try:
                    with open(filepath, 'w') as outfile: # directory + filename is an absolute path where file is saved
                        [outfile.write(str(elem)) for elem in contents]
                    self.destroy()  # close dialog win and return to main win after file is saved
                    self.master.refreshStatus('') # writing this way gives refreshStatus 2 args: self.master & ''
                except IOError:
                    tkmb.showerror("Error", "could not write to file", icon='warning')
        else: # if there is no user choice
            tkmb.showerror("Error", "Choose one or more park", icon='warning')

def gui2fg():
    '''Brings tkinter GUI to foreground on Mac. Call gui2fg() after creating main window and before mainloop() start'''
    if sys.platform == 'darwin':
        tmpl  = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid()))

win = MainWin()
gui2fg()
win.mainloop()





'''notes: 
# state_selection = [LB.get(index) for index in LB.curselection()] # curselection() is the cursor selected choices (a tuple of index vals) from listbox, this returns the value of the index in listbox
# responses normally contain html, but because we are using an API key, the response will contain a JSON string
# LB.selection_clear(0, tk.END)  # clear out cursor selection from listbox


queues: 
- buckets of things. you can always write to it
- but if you try to read from it and it is empty then your program waits until something goes in it
- if you try to read from a queue and it gets suspended, program stops and nothing more happens
- my code counts number of threads that I have, and then takes same num items out of queue otherwise program will get suspended 

'''