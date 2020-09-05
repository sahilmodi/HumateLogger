class UnitsRange:
    min: int
    max: int
    target: int
    tolerance = 0.10
    def __init__(self, target_units: int):
        self.min = int((1 - self.tolerance) * target_units)
        self.max = int((1 + self.tolerance) * target_units)
 
    def __add__(self, other):
        new = UnitsRange(0)
        new.min = self.min + other
        new.max = self.max + other
        return new
    
    def __sub__(self, other):
        return self.__add__(-other)

    def __str__(self):
        return "[{}, {}]".format(self.min, self.max)

    def __repr__(self):
        return str(self)

POUNDS_TO_KG_RATIO = 2.204