import sqlite3


'''
database = "sqlite.db"
conn = sqlite3.connect(database) # create a database connection
cur = conn.cursor() # cursor object that points to database


cur.execute("SELECT occupation FROM job_data ORDER BY occupation DESC;")  # point cursor to a record(row) in a table using the query string
#print(cur.fetchall())

#print([record[0] for record in cur.fetchall()])

conn.close()


dict = {"one":1, "two":2, "three":3, "four":4}
#[print(key) for key in dict]


gen = (x for x in range(10))

try:
    while True:
        var = next(gen)
        print(var)
except StopIteration:
    pass

print("done!")

'''

'''
conn=sqlite3.connect("mid.db")
cur = conn.cursor()
cur.execute("CREATE TABLE Counts (name TEXT, count INTEGER)")
name = 'deanza'
for i in range(5):
    cur.execute("SELECT count FROM Counts WHERE name = ?", (name,))
    result = cur.fetchone()
    if result is None:
        cur.execute("INSERT INTO Counts (name, count) VALUES (?,1)", (name,))
    else:
        var = result + 1
        cur.execute("UPDATE Counts SET count = ? WHERE name = ?", (var, name))
        conn.commit()
conn.close()
'''
'''

import os
import tkinter as tk
from tkinter import filedialog
import glob

d = tk.filedialog.askdirectory(initialdir= os.path.expanduser('~'))

L = [fname for fname in glob.glob(os.path.join(d,'*.csv'))]
print(L)
'''
import multiprocessing
import threading

N = 0
def setNum(N) :
    N = 1000
if __name__ == '__main__' :

    p1 = multiprocessing.Process(target=setNum, kwargs=dict(N=N))
    p1.start()
    p1.join()
    print(N)

    t = threading.Thread(target=setNum, args=(N,))
    t.start()
    t.join()
    print(N)