import json
from lib.filters import humate_filter
import pyrebase
from typing import List
from pathlib import Path
from datetime import datetime

from .humate import Humate
from .utils import UnitsRange, POUNDS_TO_KG_RATIO
from .dosage_dispension import optimal_dispension
from .filters import HumateFilter

class MedicineDatabase:
    def __init__(self):
        config = {}
        with open(Path(__file__).parent / "firebase_config.json") as f:
            config = json.load(f)
        config["serviceAccount"] = str(Path(__file__).parent / "humate-logger-firebase-adminsdk-6i22g-d194e91263.json")
        firebase = pyrebase.initialize_app(config)
        firebase.auth()
        self.db = firebase.database()
        
        self.cache_path = Path(__file__).parent / "medicine.json"
        self.cache = {}

        self.weight_kg = self.db.child("weight_lb").get().val() / POUNDS_TO_KG_RATIO
        self.__update_expired()

    def get_all(self) -> List[Humate]:
        medicines = self.db.child("medicine").order_by_child("used").get()
        if medicines.each() is None:
            return []
        return [Humate(**med.val()) for med in medicines]

    def get_available(self) -> List[Humate]:
        self.update_local_db()
        return [Humate(**v) for v in self.cache["medicine"].values()]

    def get_by_filters(self, humate_filter: HumateFilter, quantity=-1, get_all=False):
        self.update_local_db()
        get_func = self.get_all if get_all else self.get_available
        medicine = list(filter(lambda x: humate_filter.check(x), [h for h in get_func()]))
        if quantity > 0 and len(medicine) > quantity:
            return medicine[:quantity]
        return medicine

    def get_by_dose(self, units_per_kg: int, location: str) -> List[Humate]:
        units_range = UnitsRange(int(units_per_kg * self.weight_kg))
        print("Finding medicine in the range:", units_range, "at", location)
        humate_filter = HumateFilter()
        humate_filter.location = location
        medicine = self.get_by_filters(humate_filter)
        return optimal_dispension(units_range, medicine)

    def move(self, humate: Humate, new_location) -> bool:
        humate.location = new_location
        self.db.child("medicine").child(humate.barcode).update(humate.dict())
        self.__update_timestamp()
        return True

    def add(self, humate: Humate):
        self.db.child("medicine").child(humate.barcode).set(humate.dict())
        self.__update_timestamp()

    def use(self, humate: Humate, reason, date=0):
        humate.used = date if date else self.__current_ordinal_date()
        humate.reason = reason
        self.db.child("medicine").child(humate.barcode).update(humate.dict())
        self.__update_timestamp()

    def set_weight_lb(self, weight_lb: float):
        self.db.child("weight_lb").set(weight_lb)
        self.__update_timestamp()
        self.weight_kg = weight_lb / POUNDS_TO_KG_RATIO

    def update_local_db(self, mute=False):
        last_updated = self.db.child("last_updated").get().val()
        self.cache = {}
        if self.cache_path.exists():
            with open(self.cache_path) as f:
                self.cache = json.load(f)
        if self.cache.get("last_updated", -1) != last_updated:
            self.cache["last_updated"] = last_updated
            self.cache["medicine"] = {med.barcode: med.dict() for med in self.__get_available_remote()}
            with open(self.cache_path, "w") as f:
                json.dump(self.cache, f, indent=2)
            if not mute:
                print("Updated local database to latest version:", last_updated)

    def __get_available_remote(self) -> List[Humate]:
        medicines = self.db.child("medicine").order_by_child("used").equal_to(0).get()
        if medicines.each() is None:
            return []
        return [Humate(**med.val()) for med in medicines]

    def __update_timestamp(self):
        self.db.child("last_updated").set(datetime.timestamp(datetime.utcnow()))

    def __update_expired(self):
        last_check = self.db.child("last_expired_check").get().val()
        utc_now = datetime.utcnow()
        if (utc_now - datetime.fromtimestamp(last_check)).days < 2:
            return
        print("Checking for expired medicine...")
        curr_date = self.__current_ordinal_date()
        any_expired = False
        non_expired = self.__get_available_remote()
        for humate in non_expired:
            if humate.expiration < curr_date:
                humate.used = 1
                humate.reason = "expired"
                self.db.child("medicine").child(humate.barcode).update(humate.dict())
                any_expired = True
                print("* {}".format(humate))
        self.db.child("last_expired_check").set(datetime.timestamp(utc_now))
        if any_expired:
            self.__update_timestamp()
        self.update_local_db()

    def __current_ordinal_date(self) -> int:
        return datetime.utcnow().date().toordinal()
