class EqualityFilter:
    def __init__(self, value):
        self.value = value

    def check(self, test):
        return test == self.value