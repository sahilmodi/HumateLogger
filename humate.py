from dataclasses import dataclass
from datetime import datetime

class Humate:
    units: int
    expiration: int
    received: int
    used: int
    reason: str
    barcode: str
    location: str

    def __init__(self, metadata: dict):
        self.units = metadata.get("units", 0)
        self.expiration = metadata.get("expiration", 0)
        self.received = metadata.get("received", 0)
        self.used = metadata.get("used", 0)
        self.reason = metadata.get("reason", "")
        self.barcode = metadata.get("barcode", "")
        self.location = metadata.get("location", "")

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        res = ", ".join([
            "units: {}".format(self.units),
            "expiration: {}".format(datetime.fromordinal(self.expiration).date()),
            "barcode: {}".format(self.barcode)
        ])
        return "{" + res + "}"
    
    def dict(self):
        return self.__dict__
