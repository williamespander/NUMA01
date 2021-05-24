# -*- coding: utf-8 -*-
"""
Created on Mon May 24 13:33:52 2021

@author: claud
"""

import datetime
import pytz
from matplotlib.pyplot import *
# ASTRAL CAN BE USED FOR SUNRISE/SUNSET TIMES.
# import astral

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
        # in int data type. Datetime objects are instantly converted from
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
            for line in txt:
                try:
                    self.data.append([pytz.utc.localize(
                        datetime.datetime.strptime(line.split(sep="  ", 
                                                              maxsplit=1)[0]
                                                   ,'%Y-%m-%d %H:%M:%S.%f'))
                        .astimezone(pytz.timezone('Europe/Stockholm')), 
                        int(line.split(sep="  ", maxsplit=1)[1])])
                except ValueError:
                    pass
        #print(len(self.data))
    
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
            try:
                if (self.data[i+1][1] - self.data[i][1] <= 25 and
                    self.data[i+1][1] - self.data[i][1] >= 0):
                    self.data[i][1] = abs(self.data[i+1][1] - 
                                          self.data[i][1])
                else:
                    self.data[i][1] = 0
            except IndexError:
                pass
            
        # Removes and adds lines based on timedeltas which are too low or
        # high.
        # ISSUE: FOR SOME REASON NO ITEMS ARE DELETED WHILE 20-30K ITEMS
        #        ARE ADDED IN THE LATTER PART.
        i = 0
        while (i <= len(self.data)):
            try:
                if (self.data[i][0] + datetime.timedelta
                    (minutes=1, seconds=30) > self.data[i+1][0]):
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
    def plot(self): #, start, end):
        x_values = [birdsData.data[i][0] for i in range(1, 240530)]
        y_values = [abs(birdsData.data[i][1]) 
                    for i in range(1, 240530)]
        ylim(0,60)
        plot(x_values,y_values)
        show()
        
birdsData = birds(r"C:/Users/claud/OneDrive/Documents/bird_jan25jan16.txt")
birdsData.preprocess()
birdsData.plot()
#print(len(birdsData.data))


#ställen där de går bakåt i tiden
#2016-01-12 22:18:05.547619    0

#2015-08-02 07:00:08.274214    24798
#2015-08-02 06:18:17.747048    0

#BirdsData.Ste,p1()
#print(BirdsData.data[0:12500])
#datumet: 2015, 2, 9, 8, 10
#2015-02-09 07:08:05.410445    802
#2015-02-09 07:10:05.219535   02
#2015-02-09 07:12:05.254474    802

#238746