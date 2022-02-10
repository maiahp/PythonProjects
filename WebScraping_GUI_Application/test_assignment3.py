import sqlite3
'''


class Data():
    def __init__(self):
        database = "sqlite.db"
        self.conn = sqlite3.connect(database)  # create a database connection
        self.cur = self.conn.cursor()  # cursor object that points to database

    def select_record_from_table(self, *args):

        self.cur.execute("SELECT level FROM education_level WHERE id = ? LIMIT 1", args)
        print(self.cur.fetchall())

        #self.cur.execute(query_string)  # point cursor to a record(row) in a table using the query string
        #return self.cur.fetchall()  # return the data




    def getdata(self, getdatafcn):
        edLevelRecords = [record for record in getdatafcn("SELECT id,level FROM education_level")]  # returns [ (id, level), ]

        choice = 2
        # choice is 1, 2, 3, or 4

        if choice is not None:  # if user clicked X on dWin, choice var is set to None
            edLevel = [elem[0] for elem in getdatafcn("SELECT level FROM education_level WHERE id = ? LIMIT 1", 2)]  # grabs level using id from database
            occupations = getdatafcn("SELECT occupation FROM job_data WHERE education_level_id = " + str(choice) + " ORDER BY occupation ASC")  # order by ascending - will be in alphabetical order

data = Data()
data.select_record_from_table(2)


import re

URL = "https://www.bls.gov/ooh/computer-and-information-technology/home.htm"
partial_link = re.findall("http.*://www.\w*.\w{3}", URL)
print(partial_link)


def url_path_to_dict(path):
    pattern = (r'^'
               r'((?P<schema>.+?)://)?'
               r'((?P<user>.+?)(:(?P<password>.*?))?@)?'
               r'(?P<host>.*?)'
               r'(:(?P<port>\d+?))?'
               r'(?P<path>/.*?)?'
               r'(?P<query>[?].*?)?'
               r'$'
               )
    regex = re.compile(pattern)
    m = regex.match(path)
    d = m.groupdict() if m is not None else None

    return d
'''


#print(url_path_to_dict('http://example.example.com/example/example/example.html'))





import requests
from bs4 import BeautifulSoup
import re


page = requests.get("python.org")