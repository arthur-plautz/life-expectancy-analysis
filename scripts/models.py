from data.definitions import FEATURES, TARGET

class Splitted:
    def __init__(self, tag, features, target):
        self.tag = tag
        self.features = features
        self.target = target

    def df(self):
        df = self.features
        df[TARGET] = self.target
        return df