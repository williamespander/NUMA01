# -*- coding: utf-8 -*-
"""
Created on Tue May 11 17:41:18 2021

@author: claud
"""

import pandas as pd
import numpy as np
from datetime import date
from datetime import time
from datetime import datetime
import matplotlib.pyplot as plt

mydata=pd.read_excel("C:/Users/claud/Downloads/BirdsData.xlsx")
mydata.head()
mydata['Date'] = pd.to_datetime(mydata['Date'])
mydata['Time'] = pd.to_datetime(mydata['Time'])

dates=mydata['Date'].tolist()
times=mydata['Time'].tolist()
moves=mydata['Movement'].tolist()
#%matplotlib
#mydata.plot(x="Date", y="Movement")

#plt.plot(mydata)
#plt.show()
print(moves)