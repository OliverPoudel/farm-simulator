import pygame, random, data
from constants import *
from item import *
from ui import *
from upgrades import upgrades

pygame.display.set_caption("Farm Simulator")

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

soil_texture = pygame.image.load("assets\\soiltexture.png").convert()
soil_texture = pygame.transform.scale(soil_texture, (100, 100))

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
                                data.money += market_prices[soil.current_crop.name]
                                soil.remove_crop()
                                sickle.play()
                            break
                        elif data.inventory[data.selected_item].type == "Crop":
                            if not soil.current_crop:
                                soil.add_crop(data.inventory[data.selected_item])
                                plant.play()
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
                            data.inventory.append(Item(name))
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
            crop_texture = pygame.image.load(f"assets\\{soil.current_crop.name.lower()}{int(soil.growth_timer // (soil.current_crop.grow_time * 0.34))}.png").convert_alpha()
            crop_texture = pygame.transform.scale(crop_texture, (100, 100))
            screen.blit(crop_texture, (soil.rect.x, soil.rect.y))
    
    loadUI(screen)

    pygame.display.flip()

