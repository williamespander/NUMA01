import datetime
import pytz
import pandas
import csv
with open("/Users/williamkaul/Downloads/bird_jan25jan16.txt") as txt:
    L = [(pytz.utc.localize(datetime.datetime.strptime(line.split(sep="  ", maxsplit=1)[0],'%Y-%m-%d %H:%M:%S.%f')).astimezone(pytz.timezone('Europe/Stockholm')),
          int(line.split(sep="  ", maxsplit=1)[1])) for line in txt]
    #L = [(datetime.datetime.strptime(line.split(sep="  ", maxsplit=1)[0],'%Y-%m-%d %H:%M:%S.%f').astimezone(pytz.timezone('UTC')), int(line.split(sep="  ", maxsplit=1)[1])) for line in txt]
txt.close()
print(L[0])

    #astimezone(pytz.timezone('UTC')
#col2 = [int(line.split(sep="  ", maxsplit=1)[1]) for line in lines]

#datetime.datetime.strptime(f.icol(0),'%Y-%m-%d %H:%M:%S.%f');

#print(txt.splitlines()[9])
#for line in txt.splitlines()[1:3]:
#    dates.append(datetime.datetime.strptime(line[:-7],'%Y-%m-%d %H:%M:%S.%f'))
            #datestring="2015-01-25 14:24:04.558621"#    70
            #dateobj=datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S.%f')

