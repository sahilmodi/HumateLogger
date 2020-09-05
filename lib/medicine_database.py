import json
import pyrebase
import firebase_admin
from typing import List
from pathlib import Path
from datetime import date, datetime

from lib.humate import Humate
from lib.utils import UnitsRange
from lib.dosage_dispension import optimal_dispension

class MedicineDatabase:
    def __init__(self, weight=130):
        config_path = Path(__file__).parent / "firebase_config.json"
        config = {}
        with open(config_path) as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        firebase.auth()
        self.db = firebase.database()
        self.weight_kg = weight / 2.205
        
        self.cache_path = Path(__file__).parent / "medicine.json"

        self.__update_expired()

    def get_available(self) -> List[Humate]:
        # today = self.__current_ordinal_date()
        today = date(2019, 12, 31).toordinal()
        medicines = self.db.child("medicine").order_by_child("used").equal_to(0).get()
        return self.__convert_to_medicine(medicines)

    def get_by_dose(self, units_per_kg: int) -> List[Humate]:
        self.update_local_db()
        units_range = self.__get_valid_range(units_per_kg)
        
        print("Finding medicine in the range:", units_range)
        medicine = [Humate(**v) for v in self.cache["medicine"].values()]
        return optimal_dispension(units_range, medicine)

    def get_by_barcode(self, barcode: str) -> Humate:
        self.update_local_db()
        if barcode not in self.cache["medicine"]:
            return None
        return Humate(**self.cache["medicine"][barcode])

    def move_available(self, src: str, dest: str) -> List[Humate]:
        moved = []
        for humate in self.get_available():
            if humate.location == src:
                humate.location = dest
                self.db.child("medicine").child(humate.barcode).update(humate.dict())
                moved.append(humate)

        if len(moved):
            self.__update_timestamp()
        return moved

    def add(self, humate: Humate):
        self.db.child("medicine").child(humate.barcode).set(humate.dict())
        self.__update_timestamp()

    def use(self, medicine: Humate, reason, date=0):
        medicine.used = date if date else self.__current_ordinal_date()
        medicine.reason = reason
        self.db.child("medicine").child(medicine.barcode).update(medicine.dict())
        self.__update_timestamp()

    def update_local_db(self, mute=False):
        last_updated = self.db.child("last_updated").get().val()
        self.cache = {}
        if self.cache_path.exists():
            with open(self.cache_path) as f:
                self.cache = json.load(f)
        if self.cache.get("last_updated", -1) != last_updated:
            self.cache["last_updated"] = last_updated
            self.cache["medicine"] = {med.barcode: med.dict() for med in self.get_available()}
            with open(self.cache_path, "w") as f:
                json.dump(self.cache, f, indent=2)
            if not mute:
                print("Updated local database to latest version:", last_updated)

    def __get_valid_range(self, units_per_kg: int) -> UnitsRange:
        return UnitsRange(*[int((1 + 0.15*var)*units_per_kg*self.weight_kg) for var in [-1, 1]])

    def __update_timestamp(self):
        self.db.child("last_updated").set(datetime.timestamp(datetime.utcnow()))

    def __update_expired(self):
        last_updated = self.db.child("last_updated").get().val()
        curr_date = self.__current_ordinal_date()
        if (datetime.utcnow() - datetime.fromtimestamp(last_updated)).days < 2:
            return
        print("Checking for expired medicine...")
        non_expired = self.get_available()
        for humate in non_expired:
            if humate.expiration < curr_date:
                humate.used = 1
                humate.reason = "expired"
                self.db.child("medicine").child(humate.barcode).update(humate.dict())
                print("* {}".format(humate))
        self.__update_timestamp()
        self.update_local_db()

    def __convert_to_medicine(self, db_data) -> List[Humate]:
        if db_data.each() is None:
            return []
        return [Humate(**med.val()) for med in db_data]

    def __current_ordinal_date(self) -> int:
        return datetime.utcnow().date().toordinal()
