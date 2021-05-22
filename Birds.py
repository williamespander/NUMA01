# -*- coding: utf-8 -*-
"""
Created on Sat May 22 18:04:50 2021

@author: willi
"""

import datetime
import pytz
from matplotlib.pyplot import *

class Birds:
    def __init__(self, textfile):
        self.data = []
        with open(textfile, "r") as txt:
            for line in txt:
                try:
                    self.data.append([pytz.utc.localize(datetime.
                                                        datetime.strptime
                                                        (line.split(sep="  ",
                                                        maxsplit=1)
                                                        [0], 
                                                        '%Y-%m-%d %H:%M:%S.%f'))
                                      .astimezone(pytz.timezone
                                                  ('Europe/Stockholm'))
                                      ,int(line.split(sep="  ", maxsplit=1)
                                           [1])])
                except ValueError:
                    pass
    # def Step1(self): #ändrar fel element där antalet blir ett fel värde som 2172 072 2172
    #     d1=0
    #     for i, element in enumerate(self.data[75100:76100]): #fixa nollställningen?
    #         try:
    #             if element[1] > self.data[i+1][1] and element[1] <= self.data[i+2][1]: #för större säkerhet, öka till i+5 och kör while-loop.
    #                 self.data[i+1][1]=element[1]
    #             #if element[1] > self.data[i+1][1] and element[1] > self.data[i+2][1] :
    #             #    self.data[i + 1][1] = element[1] + self.data[i + 1][1] - d1
    #             #    if self.data[i+1][1]-d1 > 0:
    #             #        d1=self.data[i+1][1]-d1
    #         except IndexError:
    #             pass
    #         print(i, element, d1)
    
    # def Step1(self):
    #     for i in range(len(self.data)):
    #         if self.data[i][1]
            
        


    def Step2(self): #ta bort datum som går backåt i tiden + lägger in tider för rader som ej finns
        dt=datetime.timedelta(minutes=2)
        for i, element in enumerate(self.data):
            try:
                if element[0]+dt < self.data[i+1][0]:
                    self.data.insert(i+1, [element[0]+dt,element[1]])
                while element[0] > self.data[i+1][0]:
                    del self.data[i+1]
            except IndexError:
                pass
            # print(i, element)

    def Step3(self):
        for i, element in enumerate(self.data):
            try:
                  if element[1]+8 <= self.data[i+1][1]:
                      self.data[i][1]=element[1]+8
            except IndexError:
                pass

BirdsData = Birds("bird_jan25jan16.txt")
BirdsData.Step2()
BirdsData.Step3()


x_values = [BirdsData.data[i][0] for i in range(300, 2000)]
y_values = [(BirdsData.data[i][1] - BirdsData.data[i-1][1]) for i in range(300, 2000)]
plot(x_values, y_values)
show()

#ställen där de går bakåt i tiden
#2016-01-12 22:18:05.547619    0

#2015-08-02 07:00:08.274214    24798
#2015-08-02 06:18:17.747048    0

#BirdsData.Step1()
#print(BirdsData.data[0:12500])
#datumet: 2015, 2, 9, 8, 10
#2015-02-09 07:08:05.410445    802
#2015-02-09 07:10:05.219535   02
#2015-02-09 07:12:05.254474    802

#238746