from datetime import datetime

class Humate:
    units: int
    expiration: int
    received: int
    used: int
    reason: str
    barcode: str
    location: str

    def __init__(self, **kwargs):
        self.units = kwargs.get("units", 0)
        self.expiration = kwargs.get("expiration", 0)
        self.received = kwargs.get("received", 0)
        self.used = kwargs.get("used", 0)
        self.reason = kwargs.get("reason", "")
        self.barcode = kwargs.get("barcode", "")
        self.location = kwargs.get("location", "")

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        barcode = self.barcode
        if len(barcode) > 23:
            barcode = self.barcode[:10] + "..." + self.barcode[-10:]
        res = ", ".join([
            "units: {}".format(self.units),
            "expiration: {}".format(datetime.fromordinal(self.expiration).date()),
            "location: {}".format(self.location),
            "received: {}".format(datetime.fromordinal(self.received).date()),
            "barcode: {}".format(barcode),
        ])
        return "{" + res + "}"
    
    def dict(self):
        return self.__dict__
