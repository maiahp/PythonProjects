# Maiah Pardo
# 4/25/19
# CIS 41B
# Lab 2

'''This file contains a College class that handles the data analysis and visualization.'''

import numpy as np
import matplotlib
matplotlib.use("TkAgg") # is this necessary? I don't know
import matplotlib.pyplot as plt

DEFAULT_FILENAME = 'tuition.csv'  # THESE MUST BE INSIDE OF THE CLASS COLLEGE. Must be class attriutes.
STARTYEAR = 1971
ENDYEAR = 2018
# when you put these inside of college class, to call them, you say college.STARTYEAR or self.STARTYEAR


class College:


    ''' __init__: constructor of College class, has a default filename and sets attributes'''
    def __init__(self, startYear=STARTYEAR, endYear=ENDYEAR, filename=DEFAULT_FILENAME):
        self.fileName = filename
        self.startYear = startYear
        self.endYear = endYear
        self.readFile() # readFile() is not within the scope of the init class, must call by self.classmethod()

    '''readFile: method to read in the file and return a numpy array of 2018 dollar college price data'''
    def readFile(self):
        try:
            self.collegePricesArr = np.genfromtxt(self.fileName, delimiter=',', skip_footer=(self.endYear-self.startYear+1)) # resulting np array has same shape as the csv file. same num of columns, read in num rows of self.endYear-self.startYear so to only include 2018 dollar
            # float is the default data type of an np array. writing dtype = float as a keyword is not necessary
        except IOError as ex: # this is a file open error
            raise IOError("{} not found".format(self.fileName))

    ''' plotTuitionTrend: plots the tuition cost over time for private 4-years, public 4-years, and public 2-years'''
    def plotTuitionTrend(self):
        colors = ['b', 'C1', 'g']
        labelsForLegend = ['Private 4-year', 'Public 4-year', 'Public 2-year']
        overallMaxCost = 0 # will be the max of the price of tuition in all selected columns that we use for plotting
        for i in range(3): # we are plotting 3 diff data sets as three diff lines on the same graph
            arrView = self.collegePricesArr[:(self.endYear-self.startYear)+1, i*2] # we are plotting the data from the "view" of the numpy array collegePricesArr
            plt.plot(np.arange(self.startYear,self.endYear+1), arrView, ".-"+colors[i], label=labelsForLegend[i]) #plot.plot(xDataList,yDataList), np.arange(1,5) will count from 1 to 4, +1 each time
            max = arrView.max()
            if max > overallMaxCost: # find max of all selected columns so that you can use this as yMax value in the plot
                overallMaxCost = max
        plt.legend(loc='best') # best location for the legend to appear on the graph
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Tuition (dollars)', fontsize=12)
        plt.title("Tuition Trend", weight='bold')
        plt.axis((self.startYear-2, self.endYear+2, -500, overallMaxCost+1000)) #axis(xStart, xEnd, yStart, yEnd)
        plt.xticks((np.arange(self.startYear,self.endYear+1)), rotation=90, fontsize=8) # controls the spacing & how many ticks there are on the graph
        #plt.show()

    ''' plotRoomBoardTrend: Plots the room and board cost over time for private 4-years and public 4-years.'''
    def plotRoomBoardTrend(self):
        colors = ['c', 'm']
        privateFourYearTotal = self.collegePricesArr[:(self.endYear - self.startYear)+1, 6] # view of numpy array: room & board + tuition
        publicFourYearTotal = self.collegePricesArr[:(self.endYear - self.startYear)+1, 8] # view of numpy array: room & board + tuition
        tuitionPrivateFourYear = self.collegePricesArr[:(self.endYear-self.startYear)+1, 0] # view of numpy array: tuition
        tuitionPublicFourYear = self.collegePricesArr[:(self.endYear - self.startYear) + 1, 2] # view of numpy array: tuition
        privateFourYearRoomBoard = privateFourYearTotal - tuitionPrivateFourYear
        publicFourYearRoomBoard = publicFourYearTotal - tuitionPublicFourYear

        plt.plot(np.arange(self.startYear,self.endYear+1), privateFourYearRoomBoard, ".-"+colors[0], label='Private 4-year') #markersize=3,
        plt.plot(np.arange(self.startYear,self.endYear+1), publicFourYearRoomBoard, ".-"+colors[1], label='Public 4-year') #markersize=3,

        maxCostPrivate = privateFourYearRoomBoard.max()
        maxCostPublic = publicFourYearRoomBoard.max()
        maxCost = max(maxCostPrivate, maxCostPublic) # max of all room & board costs to use for y-Max in graph

        plt.legend(loc="best")
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Room and Board Cost (dollars)', fontsize=12)
        plt.title("Room and Board Trend")
        plt.axis((self.startYear - 2, self.endYear + 2, -500, maxCost+1000))  # axis(xStart, xEnd, yStart, yEnd)
        plt.xticks((np.arange(self.startYear, self.endYear + 1)), rotation=90, fontsize=8)  # controls the spacing & how many ticks there are on the graph
        #plt.show()

    ''' retVal: a decorator that prints the return value of the function it decorates'''
    def retVal(fcn):  # decorator function
        def wrapper(*args, **kwargs):  # closure: calls fcn, the wrapper prints the return value of the fcn
            val = fcn(*args, **kwargs)
            print(val)
            return val
        return wrapper


    ''' plotPaths_internal: shows different paths for a student's college cost over a four year period starting from a chosen graduation year'''
    @retVal # call to decorator
    def plotPaths(self, gradYear): # works with main() in lab2
        #gradYear = int(input("Enter year of graduation: "))
        privateFourYearsCost = (self.collegePricesArr[(gradYear - self.startYear - 3):(gradYear - self.startYear + 1), 0]).sum()  # gradYear-self.startYear-3 = first row index of numpy array(self.startYear) / gradYear-self.startYear+1 = last row index of numpy array(gradyear)
        publicFourYearsCost = (self.collegePricesArr[(gradYear - self.startYear - 3):(gradYear - self.startYear + 1), 2]).sum()
        publicToPrivateCost = np.concatenate((self.collegePricesArr[(gradYear - self.startYear - 3):(gradYear - self.startYear - 1), 4],
             self.collegePricesArr[(gradYear - self.startYear - 1):(gradYear - self.startYear + 1), 0])).sum()  # first two years are public, next 2 are private
        publicToPublicCost = np.concatenate((self.collegePricesArr[(gradYear - self.startYear - 3):(gradYear - self.startYear - 1), 4],
             self.collegePricesArr[(gradYear - self.startYear - 1):(gradYear - self.startYear + 1), 2])).sum()  # first two years are private, next 2 years are public

        plt.bar((1, 2, 3, 4), (privateFourYearsCost, publicFourYearsCost, publicToPrivateCost, publicToPublicCost),
                align="center", color="navy")  # (xData, yData) you could also put "color= colorList" & each color will differ
        plt.xticks((1, 2, 3, 4), ["4-Year\nPrivate College", "4-Year\nPublic College", "2-Year Public\n& Transfer to\n4-Year Private",
                    "2-Year Public\n& Transfer to\n4-Year Public"]) # don't put xlabel inside of plt.bar this only works on mac! must do plt.xticks((1,2,3,4), (list of labels)) and put plt.bar(1,2,3,4), ()) the tuple (1,2,3,4) is what you are plotting, their labels are the list
        plt.xlabel("Student Path")
        plt.ylabel("Tuition Cost (dollars)")
        plt.title("Tuition Cost for Different Student Paths for {}".format(gradYear))
        plt.tight_layout()
        # plt.show()
        return (privateFourYearsCost, publicFourYearsCost, publicToPrivateCost, publicToPublicCost)


''' 
my notes: 
- it is very bad practice to save attributes self.var = var in other methods other than the constructor
this is because when you do this, the user might call (in main) things out of order, and you expect the user
to call certain functions in a certain order in order to have your attribute saved that you may use in another method.
if method1 saves a class attribute that method2 uses, but user calls in main method2 first then your variable has no value.
- To get around this: you must call all methods that save a class attribute inside of the __init__
The only way you can save a class attribute in another method other than init, is if you call that method in the init

array slicing "viewing" note: [startRow:endRow-1, startColumn:endColumn-1]

colors = ['r', 'g', 'b', 'k', '-r', 'c', 'm', 'y', 'C4', 'C0', 'C1', 'C2', 'C3'] 

'''
