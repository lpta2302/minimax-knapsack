class Item:
    def __init__(self, value: int, weight: int):
        self.value = value
        self.weight = weight
    def __repr__(self):
        return f"Item(value={self.value}, weight={self.weight})"
    