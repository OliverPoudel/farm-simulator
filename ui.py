import pygame, data
from constants import *
from upgrades import upgrades

pygame.init()

market_button = pygame.Rect(655, 30, 155, 40)
upgrades_button = pygame.Rect(815, 30, 155, 40)

inventory_slots = []
marketplace_buttons = []

#text_font = pygame.font.SysFont("Ariel", 45)
text_font = pygame.font.Font("assets/alagard.ttf", 35)

def draw_market_ui(screen):
    marketplace_buttons.clear()
    for i, item in enumerate(market_prices.items()):
        name, value = item
        item_frame = pygame.Rect(655, 75 + i*55, 315, 50)
        pygame.draw.rect(screen, (160, 150, 100), item_frame)

        name_text = text_font.render(name, True, (220, 220, 220))
        value_text = text_font.render(str(value), True, (220, 220, 220))
        screen.blit(name_text, (item_frame.x + 5, item_frame.y + 5))
        screen.blit(value_text, (item_frame.x + name_text.get_width() + 15 , item_frame.y + 5))

        marketplace_buttons.append((item_frame, name))

def draw_upgrade_ui(screen):
        marketplace_buttons.clear()
        for i, upgrade in enumerate(upgrade_prices.items()):
            name, value = upgrade
            item_frame = pygame.Rect(655, 75 + i*55, 315, 50)
            pygame.draw.rect(screen, (160, 150, 100), item_frame)

            level = upgrades.get(name, 0)
            name_text = text_font.render(f"{name} x{level + 1}", True, (220, 220, 220))
            value_text = text_font.render(str(value), True, (220, 220, 220))
            screen.blit(name_text, (item_frame.x + 5, item_frame.y + 5))
            screen.blit(value_text, (item_frame.x + name_text.get_width() + 15 , item_frame.y + 5))

            marketplace_buttons.append((item_frame, name))


def loadUI(screen):
    from data import current_menu
    side_menu_frame = pygame.Rect(625, 0, 375, 1000)
    side_menu_innerframe = pygame.Rect(650, 25, 325, 1000)
    pygame.draw.rect(screen, (50, 50, 40), side_menu_frame)
    pygame.draw.rect(screen, (120, 115, 85), side_menu_innerframe)
    pygame.draw.rect(screen, (50, 50, 40), market_button)
    pygame.draw.rect(screen, (50, 50, 40), upgrades_button)

    market_text = text_font.render("Market", True, (220, 220, 220))
    upgrades_text = text_font.render("Upgrades", True, (220, 220, 220))
    money_text = text_font.render(f"${data.money}", True, (220, 220, 220))
    screen.blit(market_text, (market_button.x + 5, market_button.y + 5))
    screen.blit(upgrades_text, (upgrades_button.x + 5, upgrades_button.y + 5))
    screen.blit(money_text, (655, 600))

    if current_menu == "Market":
        draw_market_ui(screen)
    elif current_menu == "Upgrade":
        draw_upgrade_ui(screen)

    inventory_frame = pygame.Rect(0, 630, 1000, 370)
    inventory_innerframe = pygame.Rect(25, 655, 950, 320)
    pygame.draw.rect(screen, (50, 50, 40), inventory_frame)
    pygame.draw.rect(screen, (120, 115, 85), inventory_innerframe)

    if data.selected_item != None:
        outline = pygame.Rect(29 + (data.selected_item%9)*105, 659 + (data.selected_item//9)*105, 102, 102)
        pygame.draw.rect(screen, (255, 255, 255), outline)

    inventory_slots.clear()
    for j in range(3):
        for i in range(9):
            inventory_slot = pygame.Rect(30 + i*105, 660 + j*105, 100, 100)
            inventory_slots.append(inventory_slot)
            pygame.draw.rect(screen, (160, 150, 100), inventory_slot)

    for i, item in enumerate(data.inventory):
        item_texture = pygame.image.load(f"assets/{item.image}").convert_alpha()
        item_texture = pygame.transform.scale(item_texture, (100, 100))
        quantity = text_font.render(str(item.quantity), True, (220, 220, 220))
        screen.blit(item_texture, (inventory_slots[i].x, inventory_slots[i].y))
        screen.blit(quantity, (inventory_slots[i].x + 5, inventory_slots[i].y + 5))

