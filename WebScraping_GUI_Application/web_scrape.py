import requests
from bs4 import BeautifulSoup
import os

url = "https://www.deanza.edu/cis/faculty.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')

'''
elems = soup.find_all('a', {"class":"h3-link"}) # gives you a list of soup elements
for elem in elems:
    print(elem.text)
    print(elem['href']) # this is the partial(relative) link, add to beginning link
    print(url + "/" + elem['href']) # print full path


# starting at a more outer point
elems = soup.find_all('div', {"class":"col-md-6"}) # gives you a list of soup elements in this outer class - wraps around all data we want
for elem in elems: # there are multiple div "col-md-6" classes
    p_tag = elem.find('p', {"class":"mt-0"})
    alink = p_tag.find('a')['href'] # when doing findall, must iterate through it (returns a list)
    print(alink)

    #print(p_tag.text) # there is only one find (one instructor name) for each elem

'''


items = soup.select('h3 a[href]') # soup.select returns a list of items
for i in items:
    print(i.text)
    print(i['href'])
    #print(i['href'])
#for i in items:
    #print(i)










'''
# midterm2 practice :

# MIN AND MAX SJ SHARKS PLAYERS BDAYS
url = "https://www.nhl.com/sharks/roster"
page = requests.get(url)
page.encoding='utf-8' # makes sure that the encoding for the page is in utf-8 so that funky characters come out correctly

soup = BeautifulSoup(page.content, "lxml")

# complicated html:
tables = soup.findAll('td', class_="birthdate-col") # narrow it down to outer tag
bdays = [(row.find('span', class_='all-but-xs-sm-md').text.split(',')[1]) for row in tables]
print("Oldest:", min(bdays))
print("Youngest:", max(bdays))

'''

'''
notes: 

soup.find('td') # finds the first td
soup.findAll('td') # finds all td's

page.text returns html as a python string
page.content returns the content of the html as a byte string
page.json returns the html page in json format




import tkinter as tk
import json

class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()  # creates MainWin window
        tk.Button(master=self, text='Joke', command=self.joke).grid()
        self.topLB = tk.Label(text='')
        self.topLB.grid()

        self.bottomLB = tk.Label(text='')
        self.bottomLB.grid()

        var = tk.IntVar()
        var.set(0)
        for i in range(4):
            tk.Radiobutton(self, text=i, variable=var, value=i).grid()



    def joke(self):
        response = requests.get('https://api.icndb.com/jokes/random')
        response.encoding = 'utf-8'  # makes sure that the encoding for the page is in utf-8 so that funky characters come out correctly
        dict = json.loads(response.text) # turns response into a dict

        joke = dict['value']['joke']

        self.topLB.configure(text=joke)  # add a new string to label
        self.update()  # update window (so that new text will show)


win = MainWin()
win.mainloop()

'''

# practice
'''
url = "https://pokemondb.net/pokedex/national"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

container = soup.find_all('div', class_='infocard')

for item in container:
    name = item.find('a', class_='ent-name').text

    types = item.find_all('small')[1].find_all('a') # can only index with find, not find_all
    type_l = []
    for type in types:
        type_l.append(type.text)

    print(name, "type:", type_l)

'''






