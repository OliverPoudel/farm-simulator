import pygame
from upgrades import upgrades

class Soil:
    def __init__(self, index):
        self.fertilization = 0
        self.rect = pygame.Rect((index%6)*105, 3+(index//6)*105, 100, 100)
        self.current_crop = None
        self.growth_timer = 0

    def add_crop(self, crop):
        self.current_crop = crop
        growth_upgrade = 1 - 0.01 * upgrades["Faster Growth"]
        #kui liiga palju growth upgreidi osta ss m2ng crashib
        fertilization_effect = 1 - (self.fertilization / 100) * 0.5
        combined_effect = growth_upgrade * fertilization_effect
        self.growth_timer = crop.grow_time * combined_effect

    def remove_crop(self):
        self.current_crop = None
