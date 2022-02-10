# Maiah Pardo
# 4/18/19
# CIS 41B
# Lab 1

'''This file imports the Country class in order to work with its data.'''

from country import Country
import re

''' get Data: reads line by line from file and creates list of Record objects'''
def getData(DEFAULT_FILE = 'lab1in.csv'):
    try:
        with open(DEFAULT_FILE, 'r') as file:
            countryList = [Country(line) for line in file] # give country one line (a string) from file
        print("Read in {} countries\n".format(len(countryList))) # output of getData
        return countryList
    except IOError as ex:
        raise SystemExit("{} not found".format(file))
    # below was not shown in teachers solution: only had IOError
    except ValueError as ex:
        raise ValueError(str(ex)) # grabs ValueError string from init of Country Class

''' printAll: calls the print method of each Country object in the list of Country Objects'''
def printAll(countryList): # wants a 'counting number sequence' don't increment a count variable, use enumerate in the for loop
    # to count without looping, we could use a generator: countGen = (i for i in range(1, len(countrylist)+1), call with next(countGen)
    for count, countryObj in enumerate(countryList,1):
        print("{} {}".format(count, countryObj))
    # always use enumerate for counting

''' getChoice: prints a menu of choices for the user and returns the choice'''
def getChoice():
    print("\n=========================") # start of menu
    print("l: literacy rate\nd: population density\nq: quit\n")
    choice = input("Enter your choice: ")
    validChoiceMatch = re.search('^[ldq]$', choice) # returns None if no match, returns match object if match found #this doesnt check for only one letter
    while validChoiceMatch == None: # if there is no match of 'l' or 'd' or 'q'
        choice = input("Enter your choice: ")
        validChoiceMatch = re.search('^[ldq]$', choice)  # returns None if no match, returns match object if match found
    return choice
    # what you can do here instead of regex: 'while choice.lower() not in tuple("ldq"):' OR 'while choice.lower() not in ('l', 'd', 'q'):

''' retVal: a decorator that prints the return value of the function it decorates'''
def retVal(fcn): # decorator function
    def wrapper(*args, **kwargs):  # closure: calls fcn
        val = fcn(*args, **kwargs)
        print(val)
        return val # MUST RETURN result
    return wrapper

''' populationDensity: calculates the population density of each part of the world'''
@retVal # decorator call
def populationDensity(args):
    countryList = args[0]
    regionToContinentMap = {'northern africa':'Africa', 'sub-saharan africa':'Africa', 'asia':'Asia', 'eastern europe':'Europe',
                            'western europe':'Europe', 'near east':'Near East', 'northern america':'North America',
                            'oceania':'Oceania', 'latin amer. & carib':'South America'} #key=region, value=continent
    continentList = ['Africa','Asia', 'Europe', 'Near East', 'North America', 'Oceania', 'South America']

    popDensitybyContinent = {
        continent: [countryObj.getpopDensity() for countryObj in countryList if regionToContinentMap[countryObj.getRegion().lower()] == continent]
        for continent in continentList
    } # comprehension to create dict where key = continent, value = a list of population densities of each country in the continent

    avgPopDensityDict = {k: sum(v)/float(len(v)) for (k, v) in popDensitybyContinent.items()} # creates a dictionary of key=continent, value=avg population density using the dictionary popDensitybyContinent
    for key in sorted(avgPopDensityDict): # you can use a for loop for printing
        print("{:<15} {:>6.1f}".format(key, avgPopDensityDict[key]))

    popDensityOfCountriesList = [elem.getpopDensity() for elem in countryList]
    minPopDensity, maxPopDensity = min(popDensityOfCountriesList), max(popDensityOfCountriesList)
    return maxPopDensity, minPopDensity

''' literacyRate: loops to let the user press the Enter key to get a list of countries within a descending literacy rate'''
def literacyRate(args):
    # countryList = args[0] is unused, but args[0] is countryList
    gen = args[1]
    user_in = input("\nPress Enter to see countries and literacy rates, anything else to quit: ")
    while user_in == '': # user pressed enter key
        try:
            listOfCountries = next(gen) # next(gen) is a list of countries within a range of literacy rates (100-90, 90-80, etc)
            for countryObj in sorted(listOfCountries, key=lambda country: country.getliteracyRate(), reverse=True): #sort list of countries here by highest to lowest literacy rate
                print("{}: {}%".format(countryObj, countryObj.getliteracyRate()))
            user_in = input("\nPress enter for next names, anything else to quit: ")
        except StopIteration: # the while loop will stop when "StopIteration" exception is caught from the generator method "literacyRateGenerator"
            print("\nno more data")
            break # go back to menu

''' countryGenerator: yields one list of Country objects at a time in descending range of literacy rate'''
def literacyRateGenerator(countryList):
    num = 100
    while num > 10:
        yield [elem for elem in countryList if elem.getliteracyRate() <= num and elem.getliteracyRate() > num-10]  # yield in place of return, 'yield' doesn't end the function when 'return' does
        num -= 10

def main():
    try:
        countryList = getData() # optional: pass a filename of user's choice into getData()
        printAll(countryList)
        gen = literacyRateGenerator(countryList)
        taskDict = {'l': (lambda x: literacyRate(x)), 'd': (lambda x: populationDensity(x))}
        choice = getChoice() # presents menu to user and asks for choice from user
        while choice is not 'q':
            taskDict[choice]([countryList, gen]) # uses taskList to call the appropriate method the user chose, we are passing a single argument (one list of two arguments) to the functions
            choice = getChoice() # presents menu again to user and asks for next choice
        SystemExit
    except Exception as ex:
        print(str(ex))
        SystemExit # program ends

if __name__ == '__main__':
    main()



''' NOTE: working with a csv file: 
import csv
with open(DEFAULT_FILE, 'r') as file:
    countryList countryList = [Country(line) for line in csv.reader(file, delimiter = ",", quoting=csv.QUOTE_ALL, skipinitialspace=True)]
    
    # this gives Country class a list (a split line) where if there is a comma inside of double quotes, it is not split by that comma.

'''

''' NOTE:
Inside of populationDensity method: 
Complicated Comprehension that can be used without continentList, only regionToContinentMap dict:

popDensitybyContinent = {
    continent: [countryObj.getpopDensity() for countryObj in countryList if regionToContinentMap[countryObj.getRegion().lower()] == continent]
    for continent in {regionToContinentMap[countryObj.getRegion().lower()] for countryObj in countryList}
}

    -we start with the inner loop (or lower line) this loop loops through all the continents in the entire data set (countryList) and defines a variable 'continent'
    -this variable 'continent' is used in the external loop (the parent loop) to define the key and the if statement: which values are going to be added into the list.

    - inner for loop: 'for continent in {regionToContinentMap[countryObj.getRegion().lower()] for countryObj in countryList'
    - the outer for loop: 'continent: [countryObj.getpopDensity() for countryObj in countryList if regionToContinentMap[countryObj.getRegion().lower()] == continent]'
    - the outer for loop takes each continent from the inner loop and adds the entry to the dictionary with all the values of popDensity from countryObj
'''