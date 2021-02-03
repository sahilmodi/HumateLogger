from lib.humate import Humate
from lib.filters import *

class HumateFilter:
    units: RangeFilter or NullFilter
    expiration: RangeFilter or NullFilter
    received: RangeFilter or NullFilter
    used: RangeFilter or NullFilter
    barcode: StringFilter or NullFilter
    location: StringFilter or NullFilter
    reason: StringFilter or NullFilter

    def __init__(self):
        self.units = NullFilter()
        self.expiration = NullFilter()
        self.received = NullFilter()
        self.used = NullFilter()
        self.barcode = NullFilter()
        self.location = NullFilter()
        self.reason = NullFilter()

    def check(self, humate: Humate):
        attributes = list(humate.dict().keys())
        for attr in attributes:
            if not getattr(self, attr).check(getattr(humate, attr)):
                return False
        return True