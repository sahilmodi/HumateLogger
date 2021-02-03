import argparse
from datetime import datetime
from lib.humate import Humate

from lib import MedicineDatabase
from lib.filters import *
from lib.ui import get_input

ap = argparse.ArgumentParser()
ap.add_argument("--old_location", "-ol", type=str, required=True, help="Where the medicine is located")
ap.add_argument("--new_location", "-nl", type=str, required=True, help="Where the medicine is located")
ap.add_argument("--units", "-u", type=int, default=0, help="Units per kilogram required")
ap.add_argument("--expiration", "-e", type=str, default="", help="Units per kilogram required")
ap.add_argument("--quantity", "-q", type=int, default=1, help="Number of boxes of medicine to get.")
args = ap.parse_args()

def move_ui(medicine):
    if not get_input("Move this medicine? (y/n)", ["y", "yes"]):
        return
    print("Updating...")
    for humate in medicine:
        print("* Moving", humate, "to", args.new_location)
        database.move(humate, args.new_location)
    database.update_local_db(True)

if __name__ == "__main__":
    database = MedicineDatabase()
    print("")
    humate_filter = HumateFilter()
    humate_filter.location = StringFilter(args.old_location)
    if args.expiration:
        humate_filter.expiration = RangeFilter(datetime.strptime(args.expiration, "%m/%d/%y").date().toordinal())
    if args.units:
        humate_filter.units = RangeFilter(args.units)
    medicine = database.get_by_filters(humate_filter, args.quantity)
    if len(medicine) < args.quantity:
        print("[ERROR] Only found {} boxes of medicine at {}.".format(len(medicine), args.old_location))
        exit()
    total = 0
    print("Found:")
    for humate in medicine:
        print("*", humate)
        total += humate.units
    print(str(total), "units total.\n")
    move_ui(medicine)
    
    print("Finished.")