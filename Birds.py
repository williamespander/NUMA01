from matplotlib.pyplot import *
from numpy import *
from datetime import *
import pytz

lines = []
CETtimezonelist = []
# Reading and closing Datafile with "with/as" statement
with open("bird_jan25jan16.txt", "r") as datafile:
    lines = datafile.readlines()
# Looping through the list and converting string to tuple with datetime obj.
# and the number of registered movements. 
for i in range(len(lines)):
    # Consider removing microseconds to improve speed
    lines[i] = (datetime.strptime(lines[i][0:26], 
                                  '%Y-%m-%d %H:%M:%S.%f').astimezone(
                                      pytz.timezone('UTC'))
                ,lines[i][30:-2])
    # Appending CETtimezonelist with timezone-converted tuples
    CETtimezonelist.append((lines[i][0].astimezone(pytz.timezone
                                                   ('Europe/Stockholm')), 
                            lines[i][1]))

print(lines[30222])
print(CETtimezonelist[26356])
