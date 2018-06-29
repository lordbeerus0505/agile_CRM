
import datetime
import calendar
def convert_to_epoch(date):
    #date format=MM/DD/YYYY
    day=int(date[3:5])
    month=int(date[0:2])
    year=int(date[6:10])
    time=datetime.datetime(year,month,day,0,0)
    time=calendar.timegm(time.timetuple())
    return time


#print(convert_to_epoch("04/01/2012"))

