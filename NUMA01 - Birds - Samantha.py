# -*- coding: utf-8 -*-
"""
Created on Wed May 12 19:20:10 2021

@author: nordq
"""

import scipy as sc
import numpy as np
import matplotlib.pyplot as mpp
import pandas as pd
import tzlocal as tz
from datetime import datetime
from dateutil import parser

class Birds:
# TASK 1 (DONE)
    def __init__(self):
        self.data = pd.read_excel(r"C:\Users\nordq\OneDrive\Dokument\BirdsData.xlsx", "Sheet1")
        self.text_to_time = []
        self.text_to_date = []
        self.converted_time = []

# TASK 2 (DONE)
    def convert_time(self):
        for i in self.data['Time']:
            i = parser.parse(i)
            i = datetime.strftime(i, '%H:%M:%S.%f')
            self.text_to_time.append(i)
        return #self.text_to_time   

    def convert_date(self):
        for i in self.data['Date']:
            i = parser.parse(i)
            i = datetime.strftime(i, '%Y-%m-%d')
            self.text_to_date.append(i)
        return #self.text_to_date
     
    def convert_timezone(self):
        # Kinda done, see below.
        return


# TASK 3 (50% DONE)

# Change timezone test
clt = datetime.now()
print(clt)
cut = datetime.utcnow()
print(cut)
convert_to_local = tz.get_localzone()
current = cut.replace().astimezone(convert_to_local)
current = current.replace(tzinfo=None)
print(current)