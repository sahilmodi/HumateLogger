import argparse
from datetime import datetime

from lib import MedicineDatabase

ap = argparse.ArgumentParser()
ap.add_argument("--dose", "-d", required=True, type=int, help="Units per kilogram required.")
ap.add_argument("--location", "-l", default="school", type=str, help="Location of the doses")
args = ap.parse_args()

if __name__ == "__main__":
    database = MedicineDatabase()
    medicines = database.get_available()
    total_units_left = 0
    for hum in medicines:
        if hum.location != args.location:
            continue
        total_units_left += hum.units
    print("Total Units Remaining:", total_units_left)
    dosage = int(total_units_left//(args.dose*database.weight_kg))
    print("Number of {} unit doses left: {}".format(args.dose, dosage))
