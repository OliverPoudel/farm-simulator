import pygame, random, data
from constants import *
from item import *
from ui import *
from upgrades import upgrades
from worker import add_worker

pygame.display.set_caption("Farm Simulator")
window = pygame.display.set_mode((window_width, window_height))
screen = pygame.Surface((game_height, game_width))
clock = pygame.time.Clock()

soil_texture = pygame.image.load("assets/soiltexture.png").convert()
soil_texture = pygame.transform.scale(soil_texture, (100, 100))

screen_frame = pygame.image.load("assets/frame.png").convert_alpha()
screen_frame = pygame.transform.scale(screen_frame, (game_height, game_width))

def addItem(name):
    filtered = list(filter(lambda x: x == name, data.inventory))
    if filtered:
        filtered[0].quantity += 1
        return True

running = True
while running:
    dt = clock.tick(FPS)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if market_button.collidepoint(mouse_pos):
                data.current_menu = "Market"
            elif upgrades_button.collidepoint(mouse_pos):
                data.current_menu = "Upgrade"
            
            for index, soil in enumerate(data.soils):
                if soil.rect.collidepoint(mouse_pos):
                    if data.selected_item in range(len(data.inventory)):
                        if data.inventory[data.selected_item].name == "Watercan":
                            watering_upgrade = 30 + upgrades["More Watering"] * 10
                            soil.fertilization = min(soil.fertilization + watering_upgrade, 90)
                            watercan.play()
                            break
                        elif data.inventory[data.selected_item].name == "Sickle":
                            if soil.current_crop:
                                data.money += market_prices[soil.current_crop.name] + 10
                                soil.remove_crop()
                                sickle.play()
                            break
                        elif data.inventory[data.selected_item].type == "Crop":
                            item = data.inventory[data.selected_item]
                            if item.quantity > 0 and not soil.current_crop:
                                item.quantity -= 1
                                soil.add_crop(item)
                                plant.play()
                                if item.quantity <= 0:
                                    data.inventory.pop(data.selected_item)
                                    data.selected_item = None
                            break

            for index, inventory_slot in enumerate(inventory_slots):
                if inventory_slot.collidepoint(mouse_pos):
                    data.selected_item = index
                    break
            
            if data.current_menu == "Market":
                for button, name in marketplace_buttons:
                    if button.collidepoint(mouse_pos):
                        if len(data.inventory) >= 27: break
                        if data.money >= market_prices[name]:
                            data.money -= market_prices[name]
                            for item in data.inventory:
                                if item.name == name and item.type == "Crop":
                                    item.quantity += 1
                                    break
                            else:
                                data.inventory.append(Item(name, type="Crop"))
                            purchase.play()
                        break

            elif data.current_menu == "Upgrade":
                for button, name in marketplace_buttons:
                    if button.collidepoint(mouse_pos):
                        price = upgrade_prices[name]
                        if data.money >= price:
                            data.money -= price
                            upgrades[name] += 1
                            purchase.play()
                            if name =="Buy worker":
                                from worker import add_worker
                                add_worker()
                        break

    screen.fill(grass_color)
    
    for soil in data.soils:
        soil.fertilization = max(0, soil.fertilization - fertilization_decay)
        fertilization_layer = pygame.Surface((100, 100))
        fertilization_layer.set_alpha(soil.fertilization)
        screen.blit(soil_texture, (soil.rect.x, soil.rect.y))
        screen.blit(fertilization_layer, (soil.rect.x, soil.rect.y))
        if soil.current_crop:
            if soil.growth_timer > 0:
                soil.growth_timer = max(soil.growth_timer - dt, 0)
            crop_texture = pygame.image.load(f"assets/{soil.current_crop.name.lower()}{int(soil.growth_timer // (soil.current_crop.grow_time * 0.34))}.png").convert_alpha()
            crop_texture = pygame.transform.scale(crop_texture, (100, 100))
            screen.blit(crop_texture, (soil.rect.x, soil.rect.y))
    
    for worker in data.workers:
        worker.update_worker()
        worker.draw(screen)

    loadUI(screen)
    scaled_surface = pygame.transform.scale(screen, (window_width, window_height))
    window.blit(scaled_surface, (0, 0))
    pygame.display.flip()

