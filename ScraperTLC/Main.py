import os
import Info as info
import csv
import Tkinter as tk
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

chromedriver = "chromedriver_win32/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get(info.destURL)#the intial url

def writeFile(name, param, data):
    if not (isinstance(data,basestring)):
        data = ''.join(str(e) for e in data)
    fo = open(name + ".txt", param)
    fo.write(data)
    fo.close()

def writeCsv(): #just testing
    f = open("hi.csv", 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow( ('Title 1', 'Title 2', 'Title 3'))
        for i in range(10):
            writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)))
    finally:
        f.close()

class Application(tk.Frame, object):#functions pertinent to scraping live here
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.enter = tk.Button(self)
        self.enter["text"] = "Date: " + datetime.date.today().strftime("%B %d, %Y") + " \nScrape WCONLINE\n(click me)"
        self.enter["command"] = self.reader
        self.enter.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def reader(self):#first login sets up the session
        email = driver.find_element_by_name("email")
        password = driver.find_element_by_name("password")

        email.send_keys(info.email)
        password.send_keys(info.password)

        driver.find_element_by_name("login").click()
        self.scrape()

    def scrape(self):
        self.selectName()
        #retaining session id from base login (I think) , go to final url (the master appoint report)
        driver.get(info.finURL)
        select = Select(driver.find_element_by_name('rid'))
        select.select_by_value("sc57be02ac4a7d7")
        sendKey("start_date", '09/04/2016')
        sendKey("end_date", '12/04/2016')

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        soup = soup.find("div", {"id": "messagebox2"})
        writeFile("websiteData", "wb", soup)
        return
    def selectName(self):
         self.enter = tk.Button(self)
         self.enter["text"] = "Scrape WCONLINE\n(click me)"

def sendKey(id, keys):
        el = driver.find_element_by_name(id)
        el.clear()
        el.send_keys(keys)
        el.submit()

root = tk.Tk()
app = Application(master=root)
app.mainloop()

