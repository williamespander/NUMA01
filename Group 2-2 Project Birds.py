# -*- coding: utf-8 -*-
"""
Created on Tue May 25 20:55:37 2021

@author: Claudia Skoglund, Samantha Nordqvist,
 William Kaul, William Espander Jansson, Benjamin Dahlén
"""

import datetime
import pytz
import numpy
import os
from matplotlib.pyplot import *
from astral import *

class birds:
    '''
    Class processes a datafile which registers in- and out-movements of
    a bird at a nesting box. The data in the file contains lines of the
    type:
        
        2015-03-01 14:22:05.911302    2072
    
    with the date, the time in UTC and the total number of registered
    movements so far.
    '''
    def __init__(self, textfile):
        self.data = []
   
        with open(textfile, "r") as txt:
            
            for line in txt:
                try:
                    self.data.append([pytz.utc.localize(
                        datetime.datetime.strptime(line.split(sep="  ", 
                                                              maxsplit=1)[0]
                                                   ,'%Y-%m-%d %H:%M:%S.%f'))
                        .astimezone(pytz.timezone('Europe/Stockholm')), 
                        int(line.split(sep="  ", maxsplit=1)[1]) 
                        ])
                except ValueError:
                    pass
            
        
    def preprocess(self):

        # Sorting the data chronologically
        self.data.sort(key=lambda x: x[0])
        
        '''
        Step 1: 
        If the items that come before or after a certain index in the
        list of number of registered movements are the same but the
        middle value is different, the middle value is changed to match
        the previous value. IndexErrors are passed.
        '''
        for i in range(len(self.data)):
            try:
                if (self.data[i-1][1] == self.data[i+1][1] and 
                        self. data[i][1] != self.data[i-1][1]):
                    self.data[i][1] = self.data[i-1][1]
            except IndexError:
                pass
        '''
        Step 3: 
        If the absolute value of the difference between the next and the
        current item in the list is less than or equal to 20, the current
        item takes on the value of the difference. Otherwise, the
        current value is set to 20. IndexErrors are passed.
        '''
        for i in range(len(self.data)):
            maxmv = 20
            try:
                if (self.data[i+1][1] - self.data[i][1] <= maxmv and
                        self.data[i+1][1] - self.data[i][1] >= 0):
                    self.data[i][1] = abs(self.data[i+1][1] - 
                                          self.data[i][1])
                else:
                    if (self.data[i+1][1] - self.data[i][1] > maxmv):
                        self.data[i][1] = maxmv
                    else:
                        self.data[i][1] = 0
            except IndexError:
                self.data[i][1] = 0
                
        '''        
        Step 2:     
        Removes and adds lines based on timedeltas which are too low or
        high.
        '''
        i = 0
        while (i <= len(self.data)):
            try:
                if (self.data[i][0] + datetime.timedelta
                    (minutes=0, seconds=0) > self.data[i+1][0]):
                # if (self.data[i][1] != 0):
                #     pass
                # else:
                    del self.data[i+1]
                elif (self.data[i][0] + datetime.timedelta(minutes=3) <
                      self.data[i+1][0]):
                    self.data.insert(i + 1, [self.data[i][0] + 
                                          datetime.timedelta(minutes=2)
                                          , self.data[i][1]])
            except IndexError:
                pass
            i += 1
            
        #Defining dusk and dawn via Astral:
        Latitude = 55.72
        Longitude = 13.35
        Dawn = []
        Dusk = []
        daytime = Astral()
        i = 0
        while (i < len(self.data)+1):
            try:
                DATA = daytime.sun_utc(date = (self.data[i][0])
                                                .astimezone(
                                                pytz.timezone(
                                                'Europe/Stockholm')),
                                                 latitude = 55.72,
                                                 longitude=13.35)
                Dawn.append(DATA['dawn'])
                Dusk.append(DATA['dusk'])
            except:
                pass
            i+=1
        
        #list for day vs night: 
        Color = np.zeros([len(self.data)]) #Defining a new list 
        T = [self.data[i][0] for i in range(len(self.data))]
        for i in range(len(self.data)):
            try:
                if Dawn[i]<T[i] and T[i]<Dusk[i]: #if the time is between dawn and dusk
                    Color[i] = 1 #Day
                else:
                    Color[i] = 0 #Night
            except Exception as E:
                pass
        self.Color = Color
       
    

    # Plots a graph within a given interval.
    def plot(self, startdate, days):
       
        # Finds the list index of the startdate in self.data.
        llimit = 0
        ulimit = len(self.data)
        while (True):
            date = int((llimit + ulimit) / 2)
            if (date == 0):
                startIndex = 0
                break
            if (date == ulimit - 1):
                startIndex = ulimit - 1
                break
            if (self.data[date - 1][0] < startdate
                    < self.data[date + 1][0]):
                startIndex = date
                break
            elif startdate < self.data[date][0]:
                ulimit = date
            elif self.data[date][0] < startdate:
                llimit = date
        # The enddate is set to the startdate + the number of days.
        endDate = self.data[startIndex][0] + days
        # Finds the list index of the enddate.
        endIndex = startIndex
        while self.data[endIndex][0] < endDate:
            endIndex += 1
        # Sets x-values to matplotlib.dates.date2num datatype and creates
        # x-axis.
        x_values = [matplotlib.dates.date2num(self.data[i][0]) for i in
                    range(startIndex, endIndex)]
        # Sets y-values to number of movements and matches dates.   
        y_values = [self.data[i][1] for i in range(startIndex - 1, 
                                                    endIndex - 1)]

        matplotlib.pyplot.plot_date(x_values, y_values, label="Movement"
                                    , marker=".", markersize="5", linewidth=3, linestyle='-')
        if days <= datetime.timedelta(days = 30):
            Colors = self.Color[startIndex-1 : endIndex-1]
            for i in range(len(Colors)-1):    
                if Colors[i] == 1:    
                    matplotlib.pyplot.axvspan(xmin = x_values[i], xmax = 
                                              x_values[i+1] , 
                                              ymax = max(y_values), 
                                              color = 'green', alpha = 0.1) 
                    #green color for daytime phase 
                else:
                    pass
        else:
            print("Attention! The visualisation of day and night phases are removed"
                  " when the interval exceeds 30 days.")
        title("."); legend(); xticks(rotation=45); xlabel(" "); 
        ylabel(" ")
        show()

            

    def UI(self):
        '''
        Method starts a UI that prompts the user for input for the plots.
        The method finally calls the "plot" method and outputs a plot.
        
        '''
     
        print("Welcome to the Birds Data simulation program!"
              " In this program we have visualized the in and out movements"
              " of birds in a nesting box over a period of time. To start the simulation,"
              " follow instructions below.")
        
        # Prompts the user for a start date.
        while True:
            promptStart = input("Please enter a starting date.")
            
            try:
                if len(promptStart) == 19: #number of characters in date and time
                    promptStart = promptStart + ".000000" #adds microseconds
                elif len(promptStart) == 10: #number of characters in date only
                    promptStart = promptStart + " 00:00:00.000000" #adds time
                promptStart = pytz.utc.localize(datetime.datetime.strptime
                                    (promptStart,'%Y-%m-%d %H:%M:%S.%f')
                                    ).astimezone(pytz.timezone(
                                        'Europe/Stockholm'))
            except ValueError:
                print("Error. Dates must be in format: YYYY-MM-DD HH:MM:SS")
                continue
            
            if (promptStart < self.data[0][0] or 
                    self.data[-1][0] < promptStart):
                print("Error. Startdate must be between 2015-01-25 14:05:41.274647 "
                  + "and 2016-01-16 17:22:10.171150")
                continue
            else:
                break
            
        #Prompts the user for number of days.
        while True:
            try:
                promptDays = int(input("How many days after the start date"
                          + " do you wish to plot?"))
            except ValueError:
                print("Error. You must enter a number.")
                continue
            if promptDays <= 0:
                print("Error. Number of days cannot be negative or equal to zero.")
                continue
            promptDays = datetime.timedelta(days = promptDays)
            if ((self.data[-1][0]) < (promptStart + promptDays)):
                print("Error. The file doesn't measure beyond 2016-01-16 " + 
                      "17:22:10.171150. Plot will only include dates up to" +
                      " this point.")
                continue
            else:
                break
        self.plot(promptStart, promptDays)


        
birdsData = birds(r"C:/Users/claud/OneDrive/Documents/bird_jan25jan16.txt")
birdsData.preprocess()
birdsData.UI()
        
    