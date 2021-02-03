class RangeFilter:
    def __init__(self, low=0, high=None) -> None:
        self.low = low
        self.high = high
        if self.high is None:
            self.high = self.low

    def check(self, test):
        return self.low <= test <= self.high