import pyrebase
from humate import Humate
from datetime import date, datetime
from pathlib import Path
import json

class MedicineManager:
    def __init__(self, MedicineType):
        config_path = Path(__file__).parent / "firebase_config.json"
        config = {}
        with open(config_path) as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        # firebase.auth()
        self.db = firebase.database()
        self.Medicine = MedicineType
        
        self.cache_path = Path(__file__).parent / "medicine.json"
        self.__update_cache()
        
    def get_available(self):
        # today = datetime.now().date().toordinal()
        today = date(2019, 12, 31).toordinal()
        medicines = self.db.child("medicine").order_by_child("expiration").start_at(today + 1).get()
        return self.__convert_to_medicine(medicines)

    def get(self, units: int, expiration: int, quantity=1):
        self.__update_cache()
        medicines = []
        for med in self.cache["medicine"]:
            if len(medicines) == quantity:
                break
            if med.units == units:
                medicines.append(med)
        
        assert len(medicines) == quantity, "Not enough medicine found!"
        return medicines

    def add(self, humate: Humate):
        self.db.child("medicine").child(humate.barcode).set(humate.dict())
        self.__update_timestamp()

    def use(self, medicine: Humate, reason, date=0):
        medicine.used = date if date else datetime.now().date().toordinal()
        medicine.reason = reason
        self.db.child("medicine").child(medicine.barcode).update(medicine.dict())
        self.__update_timestamp()

    def __update_timestamp(self):
        self.db.child("last_updated").set(datetime.timestamp(datetime.now()))

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

    def __convert_to_medicine(self, db_data):
        if db_data.each() is None:
            return []
        return [self.Medicine(**med.val()) for med in db_data]


def reset():
    mm = MedicineManager(Humate)
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

mm = MedicineManager(Humate)
# print(mm.get(1860, 0))
print(mm.get_available())
# mm.add("test", x)