import json

class Storage:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(filename, "r") as f:
                self.pairs = json.load(f)
        except:
            self.pairs = ["CLANKERUSDT", "RESOLVUSDT", "USELESSUSDT"]
            self.save()

    def get_pairs(self):
        return self.pairs

    def add_pair(self, pair):
        if pair not in self.pairs:
            self.pairs.append(pair)
            self.save()

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.pairs, f)
