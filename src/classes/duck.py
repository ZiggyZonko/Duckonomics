import random
import pygame
from classes.shop import BreadShop

class Duck:
    def __init__(self, x, y):
        self.money = 100
        self.hunger = 100

        self.target_x = random.randint(0, 500)
        self.target_y = random.randint(0, 500)

        self.x = x
        self.y = y

        self.job = "Unemployed"

    def move(self, breadshops):

        # Hungry ducks seek food
        if self.hunger < 40 and breadshops:

            nearest_shop = min(
                breadshops,
                key=lambda shop:
                    (shop.x - self.x) ** 2 +
                    (shop.y - self.y) ** 2
            )

            self.target_x = nearest_shop.x
            self.target_y = nearest_shop.y

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < 5:

            # Buy food if we're at a shop
            if self.hunger < 40:
                self.money -= 5
                nearest_shop.stock -= 1
                nearest_shop.money += 5
                self.hunger += 50

            self.target_x = random.randint(0, 500)
            self.target_y = random.randint(0, 500)

            return

        speed = 1

        self.x += dx / distance * speed
        self.y += dy / distance * speed

    def draw(self, screen):
        pygame.draw.circle(
        screen,
        (255, 255, 0*self.hunger/100),  # Color changes based on hunger
        (int(self.x), int(self.y)),
        10
    )

    # On Frame
    def update(self, breadshops):

        self.hunger -= 0.02

        if self.hunger < 0:
            self.hunger = 0

        self.move(breadshops)