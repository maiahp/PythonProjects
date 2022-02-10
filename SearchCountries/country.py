# Maiah Pardo
# 4/18/19
# CIS 41B
# Lab 1

'''This Country class works with a list of countries by reading the country data from a file and letting the user search
for coutries based on their data.'''
import re

class Country:
    ''' Constructor: accepts one line of input file, separates the line into 4 data values and stores the data as instance variables'''
    def __init__(self, line): # accepts one line of the data file and stores them as the instance variables
        lineList = re.split(r",(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))", line) # splits by comma but ignores commas inside of double quotes
        countryData = [elem.replace("\"", "").replace(',',';').rstrip() for elem in lineList] # data of one country (one line)
        try:
            self._countryName, self._region, self._popDensity, self._literacyRate = countryData[0], countryData[1], \
                                                                                    float(countryData[2]), float(countryData[3])
        except ValueError:
            self._countryName, self._region, self._popDensity, self._literacyRate = countryData[0], countryData[1], \
                                                                                    float(countryData[2]), 0

    '''
    def __init__(self, line):
        if line.startswith('"') :
            line = line.replace(',', ':', 1).replace('"', '') # the one here only replaces the FIRST comma in the line
        '''

    ''' __str__: the country name is returned when print(CountryObj) is called by user'''
    def __str__(self):
        return self._countryName

    ''' getRegion: returns region'''
    def getRegion(self):
        return self._region

    ''' getPopDensity: returns popDensity'''
    def getpopDensity(self):
        return self._popDensity

    ''' getLiteracyRate: returns literacyRate'''
    def getliteracyRate(self):
        return self._literacyRate



''' NOTE: how to do the regex manually in __init__():
        lineList = line.split(",")
        if '"' in lineList[0]:
            lineList[0] = lineList[0] + "," + lineList[1]
            lineList.pop(1) # pop(index) removes an element at the index specified from the list '''

# when you get a file with an error, end program - no try-except, just raise the exception.
# try-except is to handle the exception, we are not handling it, we let the user handle it.


