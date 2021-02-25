from lib import Humate
from lib.filters import humate_filter
from datetime import datetime
from collections import defaultdict

from lib import MedicineDatabase
from lib.filters import HumateFilter, RangeFilter

def humate_usage_str(humate: Humate):
    d = {
            "units": humate.units, 
            "expiration": str(datetime.fromordinal(humate.used).date()),
            "received": str(datetime.fromordinal(humate.received).date()),
        }
    return f"{d} for {humate.reason}"

def print_usage(start_date, end_date):
    database = MedicineDatabase()
    humate_filter = HumateFilter()
    humate_filter.used = RangeFilter(start_date, end_date)
    boxes = database.get_by_filters(humate_filter, get_all=True)

    print("Have used a total of", 
            len(boxes), 
            "boxes of medicine between", 
            datetime.fromordinal(start_date).date(), 
            "to", datetime.fromordinal(end_date).date())
    location_map = defaultdict(list)
    for box in boxes:
        location_map[box.location].append(box)

    for location in location_map:
        print(f"=== {location} ===")
        date_map = defaultdict(list)
        for box in location_map[location]:
            date_map[box.used].append(box)
        for date in sorted(date_map.keys()):
            str_date = datetime.fromordinal(date).date()
            print("-", str_date)
            for box in date_map[date]:
                print("\t *", f"{humate_usage_str(box)}.")
        
        print()

