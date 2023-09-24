from PyQt5.QtCore import QDate
from PyQt5.QtChart import QDateTimeAxis
from PyQt5.QtChart import QLineSeries
d=QDate(2020,1,3)
d2=QDate(2020,1,4)
series=QLineSeries()
series_list=[]
series_list.append(QLineSeries())
series_list.append(QLineSeries())

print(series_list)
print(len(series_list))

