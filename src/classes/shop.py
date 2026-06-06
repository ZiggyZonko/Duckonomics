import random
import pygame

class BreadShop:
    def __init__(self, name):
        self.name = name
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.bread_price = 10
        self.stock = 100
        self.money = 0;

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 15, self.y - 15, 30, 30))

    def update(self):
        pass

    
