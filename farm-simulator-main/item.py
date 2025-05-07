import soil, data
from itemdata import ItemData

class Item:
    def __init__(self, name, quantity=None):
        self.name = name
        self.image = ItemData[name]["Image"]
        self.type = ItemData[name]["Type"]
        self.quantity = quantity or 1

        if self.type == "Crop":
            self.grow_time = ItemData[name]["GrowTime"]
    
    def plant(self, item, soil):
        if not soil.current_plant:
            item.quantity -= 1
            soil.add_crop(item)
