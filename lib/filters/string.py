class StringFilter:
    def __init__(self, value="", exact_match=True):
        self.value = value
        self.exact_match = exact_match
    
    def check(self, test):
        if self.exact_match:
            return self.value == test
        return self.value in test