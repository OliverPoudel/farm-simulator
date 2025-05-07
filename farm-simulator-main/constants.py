import pygame
pygame.mixer.init()
# Colors
grass_color = (75, 50, 20)
soil_color = (150, 75, 0)

#Marketplace Prices
market_prices = {
    "Carrot": 5,
    "Wheat": 10,
}

#Upgrade Prices
upgrade_prices = {
    "Faster Growth": 100,
    "More Watering": 150,
}

# Audios
watercan = pygame.mixer.Sound("assets\\watercan.mp3")
purchase = pygame.mixer.Sound("assets\\purchase.mp3")
sickle = pygame.mixer.Sound("assets\\sickle.mp3")
plant = pygame.mixer.Sound("assets\\plant.mp3")

# Constants
FPS = 30
fertilization_decay = 0.1 # Common 0.1 / maybe make into an upgrade