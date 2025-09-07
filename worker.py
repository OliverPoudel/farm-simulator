import data
from constants import *
import pygame
import math

step = 5



def add_worker():
    new_worker = Worker()
    data.workers.append(new_worker)
    print("adding") #debug


class Worker:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.assigned_soil = None
        self.state = "Idle"
        self.current_soil_index = None

    def update_worker(self):
        if self.assigned_soil is None:
            for i, soil in enumerate(data.soils):
                if soil.current_crop is None and not self.is_soil_occupied(i):
                    crop_to_plant = None
                    for item in data.inventory:
                        if item.type == "Crop" and item.quantity > 0:
                            crop_to_plant = item
                            break
                    if crop_to_plant:
                        self.assigned_soil = soil
                        self.state = "planting"
                        self.current_soil_index = i
                        break

            if self.assigned_soil is None:
                for i, soil in enumerate(data.soils):
                    if soil.current_crop and soil.growth_timer <= 0 and not self.is_soil_occupied(i):
                        self.assigned_soil = soil
                        self.state = "harvesting"
                        self.current_soil_index = i
                        break

            if self.assigned_soil is None:
                self.state = "idle"
                return
            
            if self.x == 0 and self.y == 0:
                self.x = self.assigned_soil.rect.x
                self.y = self.assigned_soil.rect.y

        assigned_x = self.assigned_soil.rect.x
        assigned_y = self.assigned_soil.rect.y

        distance_x = assigned_x - self.x
        distance_y = assigned_y - self.y

        distance = math.sqrt((distance_x **2 + distance_y ** 2))

        if distance < step:
            self.x = assigned_x
            self.y = assigned_y

            if self.state == "planting":
                crop_to_plant = None
                for item in data.inventory:
                    if item.type == "Crop" and item.quantity > 0:
                        crop_to_plant = item
                        break
                if crop_to_plant and self.assigned_soil.current_crop is None:
                    crop_to_plant.quantity -= 1
                    self.assigned_soil.add_crop(crop_to_plant)
                    if crop_to_plant.quantity <= 0:
                        data.inventory.remove(crop_to_plant)
                    self.assigned_soil = None
                    self.state = "idle"
                    self.current_soil_index = None

            elif self.state == "harvesting":
                if self.assigned_soil.current_crop:
                    data.money += market_prices[self.assigned_soil.current_crop.name] + 5
                    self.assigned_soil.remove_crop()
                    self.assigned_soil = None
                    self.state = "idle"
                    self.current_soil_index = None

        else:
            self.x += distance_x / distance * step
            self.y += distance_y / distance * step

    def is_soil_occupied(self, soil_index):
        for worker in data.workers:
            if worker.current_soil_index == soil_index and worker != self:
                return True
            return False
        
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(int(self.x) + 25, int(self.y) + 25, 50, 50))