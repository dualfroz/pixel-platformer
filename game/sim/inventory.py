class Inventory:
    def __init__(self):
        self.counts = {}
        self.keys = 0

    def add(self, kind, amount=1):
        self.counts[kind] = self.counts.get(kind, 0) + amount
        if kind == "key":
            self.keys += amount
        return self.counts[kind]

    def count(self, kind):
        return self.counts.get(kind, 0)

    def has(self, kind, amount=1):
        return self.count(kind) >= amount

    def consume(self, kind, amount=1):
        if self.count(kind) < amount:
            return False
        self.counts[kind] -= amount
        if kind == "key":
            self.keys -= amount
        return True

    def asDict(self):
        return {"counts": dict(self.counts), "keys": self.keys}

    def loadDict(self, record):
        self.counts = dict(record.get("counts", {}))
        self.keys = record.get("keys", 0)
