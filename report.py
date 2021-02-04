import argparse
from datetime import datetime
from lib.reports import *

save_availablity()

start_date = datetime.strptime("12/01/20", "%m/%d/%y").date().toordinal()
end_date = datetime.strptime("01/31/22", "%m/%d/%y").date().toordinal()
print_usage(start_date, end_date)
