import argparse
from datetime import datetime

from lib.medicine_database import MedicineDatabase
from lib.ui import get_input

ap = argparse.ArgumentParser()
ap.add_argument("--units", "-u", type=int, default=0, help="Units per kilogram required")
ap.add_argument("--expiration", "-e", type=str, default="", help="Units per kilogram required")
ap.add_argument("--location", "-l", type=str, default="school", help="Where the medicine is located")
ap.add_argument("--quantity", "-q", type=int, default=1, help="Number of boxes of medicine to get.")
args = ap.parse_args()

def use_ui(medicine):
    if get_input("Use this medicine? (y/n)", ["y", "yes"]):
        reason = get_input("Please enter a reason. Leave blank to use 'prophy'")
        if not reason:
            reason = "prophy"
        date_str = get_input("Please enter in a date in mm/dd/yyyy format. Leave empty to use today")
        date = datetime.now().toordinal()
        if date_str:
            date = datetime.strptime(date_str, "%m/%d/%yy").date().toordinal()
        print("Updating...")
        for humate in medicine:
            print("* Using", humate, "for", reason, "on", datetime.fromordinal(date).date())
            database.use(humate, reason, date)
        database.update_local_db(True)


if __name__ == "__main__":
    database = MedicineDatabase()
    print("")
    filters = {"location": args.location}
    if args.expiration:
        filters["expiration"] = datetime.strptime(args.expiration, "%m/%d/%y").date().toordinal()
    if args.units:
        filters["units"] = args.units
    medicine = database.get_by_filters(filters, args.quantity)
    if len(medicine) != args.quantity:
        print("Error: Only found {} boxes of medicine.".format(len(medicine)))
        exit()
    else:
        total = 0
        print("Found:")
        for humate in medicine:
            print("*", humate)
            total += humate.units
        print(str(total), "units total.\n")
        use_ui(medicine)
    
    print("Finished.")