from humate import Humate
from datetime import date
import datetime

x = Humate(1860, date(2020, 12, 31), date(2020, 8, 15), date(2020, 9, 3), "prophy")
x = datetime.datetime.strptime("2020-12-3", "%Y-%m-%d")
print(datetime.date)
# def add(units, expiration, quantity):
