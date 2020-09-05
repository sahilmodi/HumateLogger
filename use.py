import argparse
from datetime import datetime

from lib.medicine_database import MedicineDatabase

ap = argparse.ArgumentParser()
ap.add_argument("--dose", "-d", required=True, type=int, help="Units per kilogram required")
args = ap.parse_args()


def get_input(query, valid_responses=[]):
    print(query)
    response = input()
    if len(valid_responses):
        return response if response.lower() in valid_responses else ""
    return response


if __name__ == "__main__":
    database = MedicineDatabase()
    print("")
    medicine = database.get_by_dose(args.dose)
    if not len(medicine):
        print("Error: Could not find a valid medicine combination.")
        exit()
    else:
        total = 0
        for humate in medicine:
            print("*", humate)
            total += humate.units
        print(str(total), "units total.\n")
   
    if get_input("Use this medicine? (y/n)", ["y", "yes"]):
        reason = get_input("Please enter a reason. Leave blank to use 'prophy'")
        if not reason:
            reason = "prophy"
        date_str = get_input("Please enter in a date in mm/dd/yyyy format. Leave empty to use today")
        date = datetime.now().toordinal()
        if date_str:
            date = datetime.strptime(date_str, "%m/%d/%y").date().toordinal()
        print("Updating...")
        for humate in medicine:
            print("* Using", humate, "for", reason, "on", datetime.fromordinal(date).date())
            database.use(humate, reason, date)
        database.update_local_db(True)
        
    print("Finished.")
    