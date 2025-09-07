import soil, data
from itemdata import ItemData
class Item:
    def __init__(self, name, type=None, quantity=1, grow_time=None, image=None):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.grow_time = grow_time

        if self.type == "Crop" and self.grow_time is None:
            crop_grow_times = {
                "Wheat": 10,
                "Corn": 15,
                "Carrot": 8,
            }
            self.grow_time = crop_grow_times.get(self.name, 10)

        if image:
            self.image = image
        else:
            self.image = f"{self.name.lower()}.png"

    def __eq__(self, value):
        return self.name == value

    def plant(self, soil):
        if not soil.current_crop:
            self.quantity -= 1
            soil.add_seed(self)
            if self.quantity == 0:
                data.inventory.remove(self)

