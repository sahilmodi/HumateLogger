class UnitsRange:
    min: int
    max: int
    def __init__(self, min_val, max_val):
        self.min = min_val
        self.max = max_val
 
    def __add__(self, other):
        return UnitsRange(self.min + other, self.max + other)
    
    def __sub__(self, other):
        return self.__add__(-other)

    def __str__(self):
        return "[{}, {}]".format(self.min, self.max)

    def __repr__(self):
        return str(self)