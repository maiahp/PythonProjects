# Maiah Pardo
# 5/9/19
# Lab 3

''' Produces a JSON file and SQL database file '''

import requests
from bs4 import BeautifulSoup
import re
import json
import sqlite3


URL = "https://www.bls.gov/ooh/computer-and-information-technology/home.htm"
JSON_FILE = 'data.json'


try:
    page = requests.get(URL)
except requests.exceptions.RequestException as ex:
    raise SystemExit("Could not connect to:", URL, ex)


page.encoding='utf-8' # makes sure that the encoding for the page is in utf-8 so that funky characters come out correctly
soup = BeautifulSoup(page.text, 'lxml') # page.content doesn't work because page.content=html & .text is the string version of html

h4_cells = soup.findAll("h4") # inside each h4 tag is the link of one of the 10 occupation names

start_partial_link = re.findall("http.*://www.\w*.\w{3}", URL)

link_list = [(str(*start_partial_link) + link.find('a')['href']) for link in h4_cells] # for each link in link_cells, that has an 'href' attribute, add it to main website link to be a full link

# we have to do a request for each link in link_list, each link takes us to a new page
# first extract all info, then write to a JSON file after all info is collected

json_record = {} # dict
for link in link_list:
    try:
        page = requests.get(link)
        page.encoding='utf-8' # makes sure that the encoding for the page is in utf-8 so that funky characters come out correctly
        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.find(id="quickfacts") # html table (quick facts table)

        header = table.find("thead").text.replace("Quick Facts: ", "").strip() # header = json_record key

        record_keys = [row.find('th').text.strip().replace('    ', '') for row in table.find('tbody').findAll('tr')]
        record_values = [row.find('td').text.strip().replace('See How to Become One', 'Certification') for row in table.find('tbody').findAll('tr')]

        i=[0,4,5,6]
        for index in i: #i=4,5,6, save num as int in table's 0,4,5,6 rows, replace record_values with string of number, turn into int
            record_values[index] = int(re.search('\d+(?:,\d+)?', record_values[index]).group(0).replace(',', '')) # ERROR: missing minus sign, so negative data is incorrect when plotting & in the database

        json_record[header] = dict(zip(record_keys, record_values)) #json_record = { key=header : value= {record_keys : record_values} }

    except requests.exceptions.RequestException as ex:
        print(ex)

with open(JSON_FILE, 'w') as f:
    json.dump(json_record, f, indent=3) # create a json file, load data as a dict (add indent=3 for a human to read)


''' create_table_record: insert a new sql project data into the sql projects table (database)'''
def create_table_record(conn, tableName, columnNames, rowData):
    numData = ', '.join('?' * len(rowData)) # number of data (question marks) to insert into table
    query_string = 'INSERT INTO ' + tableName + '(' + columnNames + ') VALUES ({});'.format(numData)
    curr = conn.cursor()
    try:
        curr.execute(query_string, rowData)
    except sqlite3.IntegrityError as ex:
        raise SystemExit("Database already exists, please delete it and try again or you will add the same data to the tables ")
    conn.commit()
    return curr.lastrowid

# we now extract data from the JSON file in order to add this data to the sql table (database)
json_dict = {}
try:
    with open(JSON_FILE, 'r') as f:
        json_dict = json.load(f)
except IOError as ex:
    raise SystemExit("Could not open", JSON_FILE, ex)


# grab the 7 field names out of json_dict, in keys of all inner dicts
occupation_keys = list(json_dict.keys()) # keys of outer dictionary
field_name_keys_list = list(json_dict[occupation_keys[0]].keys()) # grabs field names, which are the 7 keys of one inner dictionary

# grab the education level out of all json_dicts inner dicts
ed_level_dict = {}
job_data_list = []
ed_id = 1

job_data_list_equivalent = []

for job_id, key in enumerate(occupation_keys, 1):
    ed_level = json_dict[key][field_name_keys_list[1]]
    if ed_level not in ed_level_dict:
        ed_level_dict[ed_level] = ed_id
        ed_id += 1
    salary = json_dict[key][field_name_keys_list[0]]
    ed_level_id = ed_level_dict[ed_level]

    # in the comprehension, you are adding to job_data_list (in order): experience, training, numjobs, outlook, change
    job_data_list.append([job_id, key, salary, ed_level_id, *[json_dict[key][field_name_keys_list[i]] for i in range(2, 7)]])

# create ed_level_list from ed_level_dict to use for inserting data into the table by calling "create_table_record"
ed_level_list = [[v,k] for k,v in ed_level_dict.items()] # list = [[id,ed_level_str], [id, ed_level_str]...]


database = "sqlite.db"
conn = sqlite3.connect(database) # create a database connection
curr = conn.cursor() # cursor is an object that accesses the database

# for level in this table: UNIQUE ON CONFLICT IGNORE
sql_create_education_level_table = "CREATE TABLE IF NOT EXISTS education_level (\
                                        id INTEGER NOT NULL PRIMARY KEY,\
                                        level TEXT\
                                    );"


sql_create_job_data_table = "CREATE TABLE IF NOT EXISTS job_data (\
                                    id INTEGER NOT NULL PRIMARY KEY,\
                                    occupation TEXT,\
                                    salary REAL,\
                                    education_level_id INTEGER NOT NULL,\
                                    experience TEXT,\
                                    training TEXT,\
                                    numjobs REAL,\
                                    outlook INTEGER,\
                                    change REAL,\
                                    FOREIGN KEY (education_level_id) REFERENCES education_level (id)\
                                );"

# 1 row, 7 columns: data has actual names of the 7 data fields (no id)
sql_create_field_names_table = "CREATE TABLE IF NOT EXISTS field_names (\
                                    salary TEXT,\
                                    education_level TEXT,\
                                    experience TEXT,\
                                    training TEXT,\
                                    numjobs TEXT,\
                                    outlook TEXT,\
                                    change TEXT\
                                );"

if conn is not None:
    # create projects tables:
    curr.execute(sql_create_education_level_table)
    curr.execute(sql_create_job_data_table)
    curr.execute(sql_create_field_names_table)


col_field_names = "salary, education_level, experience, training, numjobs, outlook, change"
create_table_record(conn, "field_names", col_field_names, field_name_keys_list)

col_education_level = "id, level"
[create_table_record(conn, "education_level", col_education_level, elem) for elem in ed_level_list]

col_job_data = "id, occupation, salary, education_level_id, experience, training, numjobs, outlook, change"
[create_table_record(conn, "job_data", col_job_data, elem) for elem in job_data_list] # enter one entry at a time








'''
Notes: 

# open page in browser, inspect the html and find out what info in html (the id and tag) of the info you are interested in
# then you know what to ask for from beautiful soup
# run 'requests' then feed the whole page into beautiful soup & then ask bs to give us just the portion we are interested in and ignore the rest
# then feed whatever bs gives you back is in JSON and then save it to the JSON file that you created.

# then we need to open the JSON file and then convert the data structure into 3 tables into SQLite & store the 3 tables into SQLite (from JSON to SQLite)

# NOTE: in python 3.7, the insertion order of a dictionary is preserved
        #keyList = list(record.keys())
        #record[keyList[0]]
        #print(key)
    
        
To insert all data into a dict in one line: 
# record = {row.find('th').text.strip().replace('    ', ''): row.find('td').text.strip() for row in table.find('tbody').findAll('tr')} # record = { row0 : row1 }, becomes json_record value
'''



