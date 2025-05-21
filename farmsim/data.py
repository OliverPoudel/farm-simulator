from item import *
from soil import *

global inventory
global soils
global selected_item
global money
global current_menu

workers = []

current_menu = "Market"

inventory = [Item("Sickle"), Item("Watercan")]
soils = [Soil(i) for i in range(36)]

selected_item = 0
money = 10000
