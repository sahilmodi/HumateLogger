import pyrebase
from humate import Humate
from datetime import date, datetime
from pathlib import Path
import json
from typing import List
from lib import UnitsRange

class MedicineManager:
    def __init__(self, weight=130):
        config_path = Path(__file__).parent / "firebase_config.json"
        config = {}
        with open(config_path) as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        # firebase.auth()
        self.db = firebase.database()
        self.weight_kg = weight / 2.205
        
        self.cache_path = Path(__file__).parent / "medicine.json"
        self.__update_cache()
        
    def get_available(self) -> List[Humate]:
        # today = self.__current_ordinal_date()
        today = date(2019, 12, 31).toordinal()
        medicines = self.db.child("medicine").order_by_child("expiration").start_at(today + 1).get()
        return self.__convert_to_medicine(medicines)

    def get_dose(self, units_per_kg: int) -> List[Humate]:
        self.__update_cache()
        units_range = self.__get_valid_range(units_per_kg)
        
        print("Finding medicine in the range:", units_range)
        
        medicine = [Humate(v) for v in self.cache["medicine"].values()]
        medicine.sort(key=lambda humate: (-humate.units, humate.expiration))
        return self.__get(units_range, medicine, [])

    def add(self, humate: Humate):
        self.db.child("medicine").child(humate.barcode).set(humate.dict())
        self.__update_timestamp()

    def use(self, medicine: Humate, reason, date=0):
        medicine.used = date if date else self.__current_ordinal_date()
        medicine.reason = reason
        self.db.child("medicine").child(medicine.barcode).update(medicine.dict())
        self.__update_timestamp()

    def __get(self, units_range, medicine, res) -> List[Humate]:
        if units_range.max < 0:
            return []
        if units_range.min <= 0:
            return res

        for i in range(len(medicine)):
            humate = medicine[i]
            new_medicine = medicine[:i] + medicine[i+1:]
            recurse = self.__get_helper(units_range - humate.units, new_medicine, res + [humate])
            if len(recurse):
                return recurse
        
        return []

    def __get_valid_range(self, units_per_kg: int) -> UnitsRange:
        return UnitsRange(*[int((1 + 0.15*var)*dose*self.weight_kg) for var in [-1, 1]])

    def __update_timestamp(self):
        self.db.child("last_updated").set(datetime.timestamp(datetime.utcnow()))

    def __update_cache(self):
        last_updated = self.db.child("last_updated").get().val()
        self.cache = {}
        if self.cache_path.exists():
            with open(self.cache_path) as f:
                self.cache = json.load(f)
        if self.cache.get("last_updated", -1) != last_updated:
            print("Downloading and updating to latest version: ", last_updated)
            self.cache["last_updated"] = last_updated
            self.cache["medicine"] = {med.barcode: med.dict() for med in self.get_available()}
            with open(self.cache_path, "w") as f:
                json.dump(self.cache, f, indent=2)

    def __convert_to_medicine(self, db_data) -> List[Humate]:
        if db_data.each() is None:
            return []
        return [Humate(med.val()) for med in db_data]

    def __current_ordinal_date(self) -> int:
        return datetime.utcnow().date().toordinal()


def reset():
    mm = MedicineManager()
    for med in mm.db.child("medicine").get().each():
        mm.db.child("medicine").child(med.key()).remove()
    test_data = [
        {
            "units": 1860, 
            "expiration": date(2020, 12, 31).toordinal(), 
            "received": date(2020, 8, 15).toordinal(), 
            "used": date(2020, 9, 3).toordinal(), 
            "reason": "prophy",
            "barcode": "132412341234"
        },
        {
            "units": 1860, 
            "expiration": date(2020, 6, 30).toordinal(), 
            "received": date(2020, 8, 15).toordinal(), 
            "barcode": "453452345"
        },
        {
            "units": 440, 
            "expiration": date(2020, 5, 30).toordinal(), 
            "received": date(2020, 8, 15).toordinal(), 
            "used": date(2020, 9, 3).toordinal(), 
            "reason": "prophy",
            "barcode": "12341454"
        },
        {
            "units": 980, 
            "expiration": date(2020, 1, 30).toordinal(), 
            "received": date(2020, 8, 15).toordinal(), 
            "barcode": "452351234"
        },
    ]
    for t in test_data:
        mm.add(Humate(**t))
# reset()

mm = MedicineManager()
# print(mm.get())
# print(mm.get_available())
print(mm.get_dose(60))
# mm.add("test", x)