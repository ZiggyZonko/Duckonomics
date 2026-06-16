import math
import random
import pygame
from classes.bakery import BreadShop
from constants import *
from classes.government import *

class Duck:
    def __init__(self, x, y):
        self.money = random.randint(0, 2000)
        self.hunger = 100
        self.alive = True

        self.target_x = random.randint(0, SCREEN_WIDTH)
        self.target_y = random.randint(0, SCREEN_HEIGHT)

        self.target_shop = None

        self.x = x
        self.y = y

        self.angle = 0

        # ---- Personality Traits ---- #
        self.name = (random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES))
        self.speed = random.uniform(0.5, 1.5)
        self.appetite = random.uniform(0.8, 1.2)
        self.job = random.choice(list(JOBS.keys()))
        self.age = 6
        self.happiness = 50
        self.hadChild = False
        self.generation = 1
        self.parent = "Mysterious Universe..."

    def move(self, breadshops):

        # Hungry ducks seek food
        if self.hunger < 40 and breadshops:

            available_shops = [
                shop for shop in breadshops
                if shop.stock > 0
            ]

            if available_shops:
                nearest_shop = min(
                    available_shops,
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
                    self.happiness += 10

            self.target_x = random.randint(0, SCREEN_WIDTH)
            self.target_y = random.randint(0, SCREEN_HEIGHT)

            return

        speed = 1 * self.speed

        self.x += dx / distance * speed
        self.y += dy / distance * speed

    def draw(self, screen, duckimage):
        screen.blit(duckimage, (int(self.x), int(self.y)))

    # On Frame
    def update(self, breadshops):

        self.hunger -= HUNGER_RATE * self.appetite

        if self.hunger < 0:
            self.hunger = 0

        self.move(breadshops)

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            48,  # duck width
            48   # duck height
        )
    
    def show_stats(self, screen, font):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y +50, 50, 80))
        appetitetext = font.render(f"A: {math.ceil(self.appetite)}", True, (255, 255, 255))
        screen.blit(appetitetext, (self.x, self.y))

    def accessory(self, screen, accessories):

        for wealth, image in sorted(
            accessories.items(),
            reverse=True
        ):

            if self.money >= wealth:

                screen.blit(
                    image,
                    (int(self.x + 8), int(self.y - 8))
                )

                break

    def birth(self, table, death_table):
        if (self.money > 100 and self.happiness > 30 and self.age > 5):
            if (random.random() < BIRTH_RATE and len(table)+1 <= POPULATION_MAX):
                #if(self.hadChild == False):

                    baby = Duck(
                        int(self.x),
                        int(self.y)
                    )
                    baby.generation = self.generation+1
                    baby.parent = self.name
                    baby.speed = self.speed + random.uniform(-0.1, 0.1)
                    baby.appetite = self.appetite + random.uniform(-0.1, 0.1)
                    baby.money = (self.money / 2)

                    surname = self.name.split()[1]

                    baby.name = (
                        random.choice(FIRST_NAMES) + " " + surname
                    )
                    table.append(baby)

                    print("A beautiful duckling is born")
                    #self.hadChild = True

        if (self.age >=LIFESPAN):
            death_table.append(
                {
                    "name": self.name,
                    "age": self.age,
                    "job": self.job
                }
            )

            print("Died from old age")
            self.alive = False

        if random.random() < DEATH_CHANCE:
            death_table.append(
                {
                    "name": self.name,
                    "age": self.age,
                    "job": self.job
                }
            )

            print("Died from natural causes")
            self.alive = False

    def work(self, government):
        wage = JOBS[self.job]

        self.money += government.collect_income_tax(wage)