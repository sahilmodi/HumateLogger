import argparse
from datetime import datetime

from lib.medicine_database import MedicineDatabase

ap = argparse.ArgumentParser()
ap.add_argument("--dose", "-d", required=True, type=int, help="Units per kilogram required")
ap.add_argument("--reason", "-r", type=str, default="prophy", help="Reason if medicine is being used")
args = ap.parse_args()


def get_input(query, valid_responses=[]):
    print(query)
    response = input()
    if len(valid_responses):
        return response if response.lower() in valid_responses else ""
    return response


def get(database: MedicineDatabase, dose: int):
    print("")
    medicine = database.get_by_dose(dose)
    if not len(medicine):
        print("ERROR: Not enough medicine available.")
    else:
        total = 0
        for humate in medicine:
            print("*", humate)
            total += humate.units
        print(str(total), "units total")
    return medicine

if __name__ == "__main__":
    database = MedicineDatabase()
    medicine = get(database, args.dose)
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
    print("Finished.")
    