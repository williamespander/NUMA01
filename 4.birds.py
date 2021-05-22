# -*- coding: utf-8 -*-
"""
Created on Sun May 16 15:04:16 2021

@author: claud
"""


import datetime
import pytz
import pandas
import csv
import sklearn.impute as SimpleImputer

class Birds:
# TASK 1 (DONE)
    def __init__(self, textfile):
        self.data = []
        with open(textfile, "r") as txt:
            for line in txt:
                try:
                    # Lägg till en entry när timedelta är för stort!
                    # if ...... :
                    self.data.append((pytz.utc.localize(
                        datetime.datetime.strptime(line.split(sep="  ", 
                                                              maxsplit=1)[0]
                                                   ,'%Y-%m-%d %H:%M:%S.%f'))
                        .astimezone(pytz.timezone('Europe/Stockholm')), 
                        int(line.split(sep="  ", maxsplit=1)[1])))
                except ValueError:
                    pass
        self.dt = self.data
    
    def Step1(self):
        for i, element in enumerate(self.data):
            if isinstance(self.data[30], int):
                self.data.drop([i])
            else:
                continue
            
        
    def Step2(self):
        dt=datetime.timedelta(minutes=2)
        for i, element in enumerate(self.data):
            try:
                 if element[0]+dt < self.data[i+1][0]:
                     self.data.insert(i+1,(element[0]+dt,element[1]))
            except IndexError:
                pass
            #print(i,element)
    
    def Step3(self):
        for i, element in enumerate(self.data):
            try:
                 if element[1]+8 <= self.data[i+1][1]:
                      self.data[i][1]=(element[1]+8)
            except IndexError:
                pass
            #print(i,element)

BirdsData = Birds(r"C:\Users\nordq\OneDrive\Dokument\GitHub\NUMA01\bird_jan25jan16.txt")
#BirdsData.Step2()
BirdsData.Step1()
print(BirdsData.data[5374:5376])
#print(BirdsData.data[502:510])
#print(len(BirdsData.data))