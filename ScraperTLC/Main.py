import Info as info
import csv
import Tkinter as tk
import mechanize
from bs4 import BeautifulSoup
import cookielib

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open(info.destURL)#URL

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

class Application(tk.Frame, object):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.enter = tk.Button(self)
        self.enter["text"] = "Scrape WCONLINE\n(click me)"
        self.enter["command"] = self.reader
        self.enter.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def reader(self):#first login
        br.select_form(nr=0)#select the first form
        br.form['email'] = info.email
        br.form['password'] = info.password
        control = br.form.find_control("scheduleid")
        control.disabled = False
        control.value = [info.CL]
        br.submit()

        soup = BeautifulSoup(br.response().read(), "lxml")
        writeFile("websiteData", "wb", soup)
        writeCsv()
        #self.scrape(soup)

    def scrape(self, soup):
        #do stuff
        br.follow_link('https://georgebrown.mywconline.com/tn_manage3.php?mov=no&sid=sc57be012c4a18b')
        soup = BeautifulSoup(br.response().read(), "lxml")

        print (soup)
        return

root = tk.Tk()
app = Application(master=root)
app.mainloop()

