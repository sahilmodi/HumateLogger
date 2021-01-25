import argparse
from datetime import datetime

from lib.medicine_database import MedicineDatabase
from lib.ui import get_input

ap = argparse.ArgumentParser()
ap.add_argument("--dose", "-d", required=True, type=int, help="Units per kilogram required")
ap.add_argument("--location", "-l", type=str, default="school", help="Where the medicine is located")
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
    medicine = database.get_by_dose(args.dose, args.location)
    if not len(medicine):
        print("Error: Could not find a valid medicine combination.")
        exit()
    else:
        total = 0
        for humate in medicine:
            print("*", humate)
            total += humate.units
        print(str(total), "units total.\n")
        use_ui(medicine)
    
        
    print("Finished.")
    