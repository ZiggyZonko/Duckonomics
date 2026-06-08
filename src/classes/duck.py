import math
import random
import pygame
from classes.bakery import BreadShop

class Duck:
    def __init__(self, x, y):
        self.money = random.randint(0, 200)
        self.hunger = 100
        self.alive = True

        self.target_x = random.randint(0, 500)
        self.target_y = random.randint(0, 500)

        self.x = x
        self.y = y

        self.angle = 0

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

        if self.hunger <= 0 and self.money < nearest_shop.price:
            print("A duck has starved to death")
            self.alive = False

        if distance < 5:

            # Buy food if we're at a shop
            if self.hunger < 40 and self.money >= 5:
                if nearest_shop.sell_bread():
                    self.money -= 5
                    self.hunger += 50

            self.target_x = random.randint(0, 500)
            self.target_y = random.randint(0, 500)

            return

        speed = 1

        self.x += dx / distance * speed
        self.y += dy / distance * speed

    def draw(self, screen, duckimage):
        screen.blit(duckimage, (int(self.x), int(self.y)))

    # On Frame
    def update(self, breadshops):

        self.hunger -= 0.2

        if self.hunger < 0:
            self.hunger = 0

        self.move(breadshops)