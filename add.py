import string
import random
import argparse
from datetime import datetime

from lib.humate import Humate 
from lib.medicine_database import MedicineDatabase

ap = argparse.ArgumentParser()
ap.add_argument("--units", "-u", required=True, type=int, help="Number of units in the medicine vial.")
ap.add_argument("--expiration", "-e", required=True, type=str, help="Expiration date in mm/dd/yy format.")
ap.add_argument("--received", "-r", required=True, type=str, help="Date medicine was received in mm/dd format.")
ap.add_argument("--location", "-l", required=True, type=str, help="Location of the medicine.")
ap.add_argument("--barcode", "-b", type=str, default="", help="Barcode of medicine. Randomly generated if omitted.")
ap.add_argument("--quantity", "-q", type=int, default=1, help="Quantity of medicine to add with a random barcode.")
args = ap.parse_args()

args.expiration = datetime.strptime(args.expiration, "%m/%d/%y").date().toordinal()
args.received = datetime.strptime(args.received, "%m/%d").date().replace(year=datetime.utcnow().year).toordinal()

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))

def add(database: MedicineDatabase, units: int, expiration: int, received: int, location: int, barcode="", quantity=1):
    print("")
    print("Adding...")
    humate_args = locals()
    humate_args.pop("quantity")
    for i in range(quantity):
        humate_args["barcode"] = barcode
        if quantity != 1 or not barcode:
            humate_args["barcode"] = get_random_alphanumeric_string(52)
        humate = Humate(**humate_args)
        print("* {}".format(humate))
        database.add(humate)
    boxes_str = "box" if quantity == 1 else "boxes"
    print("Added {} {} of medicine!".format(quantity, boxes_str))
    database.update_local_db(True)

if __name__ == "__main__":
    database = MedicineDatabase()
    add(database, **vars(args))