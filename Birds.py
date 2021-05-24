    # -*- coding: utf-8 -*-
"""
Created on Sat May 22 18:04:50 2021

@author: willi
"""

import datetime
import pytz
import numpy
from matplotlib.pyplot import *
from astral import Location
# ASTRAL CAN BE USED FOR SUNRISE/SUNSET TIMES.
# import astralaa

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
        # Opening file and appending list "self.data" with lists that
        # contain the date in datetime format and the number of movements
        # in int data type. Datetime objects are converted from
        # UTC timezone to CET timezone. The instantiation raises an
        # exception on one line in which the data was corrupted.
        
        # ISSUE: I JUST TRIED TO MAKE THIS LOOK A BIT PRETTIER BUT IT
        #        DOESN'T WORK FOR WHATEVER REASON. LESS PRETTY, BUT
        #        FUNCTIONAL CODE BELOW.
        # with open(textfile, "r") as txt:
        #     for line in txt:
        #         try:
        #             self.data.append
        #             ([pytz.utc.localize(datetime.datetime.strptime
        #                                 (line.split(sep="  ", maxsplit=1)
        #                                  [0], '%Y-%m-%d %H:%M:%S.%f'))
        #               .astimezone(pytz.timezone('Europe/Stockholm'))
        #               ,int(line.split(sep="  ", maxsplit=1)[1])])
        #         except ValueError:
        #             pass
        with open(textfile, "r") as txt:
            # Source: Google Maps
            
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
        '''
        Method preprocesses the datafile. Data corruption were counts are
        reported incompletely are replaced. If lines are missing, they are
        added. If there are more than 4 movements registered per minute,
        they are changed to 0.
    
        PARAMETERS
    
        self: (.txt file) 
            A textfile with dates, times and numbers that correspond to
            movements of Birds. Datetime must be in format 
            '%Y-%m-%d %H:%M:%S.%f' and the corresponding integer should
            be separated by spaces. Each datapoint has to be separated by
            a new line.
        
        RETURNS
        -------
        None.
        
        '''
        # Sorting the data chronologically
        self.data.sort(key=lambda x: x[0])
        # If the items that come before or after a certain index in the
        # list of number of registered movements are the same but the
        # middle value is different, the middle value is changed to match
        # the previous value. IndexErrors are passed.
        for i in range(len(self.data)):
            try:
                if (self.data[i-1][1] == self.data[i+1][1] and 
                        self. data[i][1] != self.data[i-1][1]):
                    self.data[i][1] = self.data[i-1][1]
            except IndexError:
                pass

        # If the absolute value of the difference between the next and the
        # current item in the list is less than or equal to 8, the current
        # item takes on the value of the difference. Otherwise, the
        # current value is set to 0. IndexErrors are passed.
        # ISSUE: THE CURRENT CODE ASSIGNS THE VALUE TO THE EARLIER TIME 
        #        BUT IT WOULD BE MORE INTUITIVE IF THE VALUE WAS ASSIGNED
        #        TO THE LATER TIME. WE SHOULD ALSO CONSIDER CHANGING THE
        #        VALUES TO 8 INSTEAD OF 0 IF THE NUMBER IS PRETTY CLOSE TO
        #        8.
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
            
        # Removes and adds lines based on timedeltas which are too low or
        # high.
        # ISSUE: FOR SOME REASON NO ITEMS ARE DELETED WHILE 20-30K ITEMS
        #        ARE ADDED IN THE LATTER PART.
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
    

    # Plots a graph within a given interval.
    def plot(self, startdate, days):
        '''
        Method plots movements in the bird nest within a given time
        interval and outputs the plot.
    
        PARAMETERS
    
        self: (.txt file) 
            A textfile with dates, times and numbers that correspond to
            movements of Birds. Datetime must be in format 
            '%Y-%m-%d %H:%M:%S.%f' and the corresponding integer should
            be separated by spaces. Each datapoint has to be separated by
            a new line.
            
        startdate: (datetime.datetime object)
            A datetime object that sets the starting date for the plot.
        
        days: (datetime.timedelta object)
            A timedelta object that sets the end date for the plot as the
            number of days from the startdate.
            
        RETURNS
        -------
        None.
        
        '''
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
                                    , marker=".", markersize="8")
        title("."); legend(); xticks(rotation=45); xlabel(" "); 
        ylabel(" ")
        show()

    def UI(self):
        '''
        Method starts a UI that prompts the user for input for the plots.
        The method finally calls the "plot" method and outputs a plot.
        
        PARAMETERS
        
        self: (.txt file)
            A textfile with dates, times and numbers that correspond to
            movements of Birds. Datetime must be in format 
            '%Y-%m-%d %H:%M:%S.%f' and the corresponding integer should
            be separated by spaces. Each datapoint has to be separated by
            a new line.
            
        Returns
        -------
        None.

        '''
        # Prompts the user for a start date.
        while True:
            promptStart = input("Please enter a starting date.")
            try:
                if len(promptStart) == 19:
                    promptStart = promptStart + ".000000"
                elif len(promptStart) == 10:
                    promptStart = promptStart + " 00:00:00.000000"
                promptStart = pytz.utc.localize(datetime.datetime.strptime
                                    (promptStart,'%Y-%m-%d %H:%M:%S.%f')
                                    ).astimezone(pytz.timezone(
                                        'Europe/Stockholm'))
            except ValueError:
                print("Dates must be in format: YYYY-MM-DD HH:MM:SS")
                continue
            if (promptStart < self.data[0][0] or 
                    self.data[-1][0] < promptStart):
                print("Startdate must be between 2015-01-25 14:05:41.274647 "
                  + "and 2016-01-16 17:22:10.171150")
                continue
            else:
                break
        # Prompts the user for number of days.
        while True:
            try:
                promptDays = int(input("How many days after the start date"
                           + " do you wish to plot?"))
            except ValueError:
                print("You must enter a number.")
                continue
            if promptDays <= 0:
                print("You must enter a positive value.")
                continue
            promptDays = datetime.timedelta(days = promptDays)
            if ((self.data[-1][0]) < (promptStart + promptDays)):
                print("The file doesn't measure beyond 2016-01-16 " + 
                      "17:22:10.171150. Plot will only include dates up to" +
                      " this point.")
                continue
            else:
                break
        self.plot(promptStart, promptDays)
        
birdsData = birds(r"C:\Users\willi\Documents\GitHub\NUMA01\bird_jan25jan16.txt")
birdsData.preprocess()
birdsData.UI()
        
    


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