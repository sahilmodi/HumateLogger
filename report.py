import argparse
from datetime import datetime, timedelta
from lib.reports import *

save_availablity()

start_date = (datetime.now().date() - timedelta(days=30)).toordinal()
# start_date = datetime.strptime("12/01/20", "%m/%d/%y").date().toordinal()
end_date = datetime.now().date().toordinal()
print_usage(start_date, end_date)
