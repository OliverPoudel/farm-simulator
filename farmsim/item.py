import soil, data
from itemdata import ItemData

class Item:
    def __init__(self, name, quantity=None):
        self.name = name
        self.image = ItemData[name]["Image"]
        self.type = ItemData[name]["Type"]
        self.quantity = quantity or 1

        if self.type == "Seed":
            self.grow_time = ItemData[name]["GrowTime"]
            self.crop_name = ItemData[name]["CropName"]
    
    def __eq__(self, value):
        return self.name == value

    def plant(self, soil):
        if not soil.current_crop:
            self.quantity -= 1
            soil.add_seed(self)
            if self.quantity == 0:
                data.inventory.remove(self)

