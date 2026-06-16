import pygame
import random
from constants import *
import tkinter as tk
from path import *
import os
print(os.getcwd())
import sys

# ---- Classes ---- #
from classes.duck import Duck
from classes.bakery import BreadShop
from classes.government import Government

# ---- Pygame Initialisation ---- #
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000,1000))
pygame.display.set_caption("🦆 Duckonomics")

# ---- Discord Initialisation ---- #
#rpc = discordrpc.RPC(app_id=997621592995680376)

# ---- Object Arrays ---- #
ducks = []
breadshops = []
waves = []
dead_ducks = []
government = Government()

# ---- Variables ---- #
day = 1
day_timer = 0
day_length = 30  # seconds
population = len(ducks)
selected_duck = None
game_state = "menu"

# ---- Sprites ---- #
duck_image = pygame.image.load(resource_path("assets/duck.png")).convert_alpha()
duck_scaled = pygame.transform.scale(duck_image, (48, 48))
shop_image = pygame.image.load(resource_path("assets/shop.png")).convert_alpha()
scaled_shop = pygame.transform.scale(shop_image, (30, 30))
wave_image = pygame.image.load(resource_path("assets/wave.png")).convert_alpha()
bread_image = pygame.image.load(resource_path("assets/bread.png")).convert_alpha()
scaled_bread = pygame.transform.scale(bread_image, (20, 20))
tophat_image = pygame.image.load(resource_path("assets/tophat.png")).convert_alpha()
tophat_scaled = pygame.transform.scale(tophat_image, (20, 20))
graduation_cap = pygame.image.load(resource_path("assets/graduation_cap.png")).convert_alpha()
gradcap_scaled = pygame.transform.scale(graduation_cap, (30, 30))
crown_image = pygame.image.load(resource_path("assets/crown.png")).convert_alpha()
crown_scaled = pygame.transform.scale(crown_image, (20, 20))
dayfont = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 48)

# ---- Duck Accessories --- #
accessories = {
    1000: crown_scaled,
    500: gradcap_scaled,
    100: tophat_scaled
}

# ---- Main Menu Buttons ---- #
start_button = pygame.Rect(
    SCREEN_WIDTH//2 - 100,
    630,
    200,
    60
)

quit_button = pygame.Rect(
    SCREEN_WIDTH//2 - 100,
    730,
    200,
    60
)

# ---- Generating Objects ---- #
for i in range(5):
    breadshops.append(
        BreadShop(
            f"Bread Shop {i+1}"
        )
    )
    print(f"Created {breadshops[-1].name} at ({breadshops[-1].x}, {breadshops[-1].y})")

for _ in range(40):
    ducks.append(
        Duck(
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT)
        )
    )


for _ in range(10):
    waves.append(
        (
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT)
        )
    )

for _ in range(5):
    waves.append(
        (
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT)
        )
    )

"""rpc.set_activity(
    state="Duckonomics",
    details=f"A duck powered economic simulator\n Day: {day}\n Population: {population}\n Government: {government.money}\n"
)"""

# ---- Main Menu Function ---- #
def draw_menu(screen):

    screen.fill((7, 138, 255))

    title = title_font.render(
        "DUCKONOMICS",
        True,
        (255, 255, 255)
    )

    pygame.draw.rect(
        screen,
        (50, 100, 200),
        start_button
    )

    pygame.draw.rect(
        screen,
        (50, 100, 200),
        quit_button
    )

    start_text = button_font.render(
        "Start Game",
        True,
        (255, 255, 255)
    )

    quit_text = button_font.render(
        "Quit Game",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (
            SCREEN_WIDTH//2 - title.get_width()//2,
            150
        )
    )

    screen.blit(
        duck_image, 
        (
            SCREEN_WIDTH//2 - title.get_width()//2 - 40,
            200
        )
    )

    screen.blit(
        start_text,
        (
            start_button.centerx - start_text.get_width()//2,
            start_button.centery - start_text.get_height()//2
        )
    )

    screen.blit(
        quit_text,
        (
            quit_button.centerx - quit_text.get_width()//2,
            quit_button.centery - quit_text.get_height()//2
        )
    )

# ---- MAIN GAME LOOP ---- #
while True:

    dt = clock.tick(120) / 1000

    if game_state == "menu":

        draw_menu(screen)

    elif game_state == "game":

        screen.fill((7, 138, 255))  # Clear screen to black

        # ---- Statistics Box ---- #
        if selected_duck:

            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (750, 20, 220, 180)
            )

            lines = [
                f"Name: {selected_duck.name}",
                f"Age: {selected_duck.age}",
                f"Money: ${selected_duck.money:.0f}",
                f"Happiness: {selected_duck.happiness:.0f}",
                f"Appetite: {selected_duck.appetite:.2f}",
                f"Job: {selected_duck.job}"
            ]

            for i, line in enumerate(lines):

                text = dayfont.render(
                    line,
                    True,
                    (255,255,255)
                )

                screen.blit(
                    text,
                    (760, 30 + i * 25)
                )

        # ---- Loops for Objects ---- #
        for wave in waves:
            screen.blit(wave_image, (wave[0], wave[1]))

        for duck in ducks[:]:
            duck.update(breadshops)
            duck.accessory(screen, accessories)

            if not duck.alive:
                ducks.remove(duck)
                continue

            duck.draw(screen, duck_scaled)

        for BreadShop in breadshops:
            BreadShop.draw(screen, scaled_shop)
            BreadShop.text(screen, scaled_bread)

        # ---- Day Logic ---- #
        day_timer += dt
        hour = (day_timer / day_length)

        if day_timer >= day_length and len(ducks) > 0:

            avg_hunger = (
                sum(duck.hunger for duck in ducks)
                / len(ducks)
            )

            for BreadShop in breadshops:
                BreadShop.end_day(
                    len(ducks),
                    avg_hunger
                )

            day += 1

            for duck in ducks[:]:
                duck.birth(ducks, dead_ducks)
                duck.work(government)
                duck.age+=1

            for BreadShop in breadshops[:]:
                    government.collect_business_tax(BreadShop)

            day_timer = 0

            print(f"Day {day} has begun!")
            print(f"Obituary: " + str([dead_ducks]))
        
        # ---- UI ---- #
        day_text = dayfont.render(f"Day {day}", True, (255, 255, 255))
        time_of_day_text = dayfont.render(f"Time: {int(hour * 24)}:00", True, (255, 255, 255))
        population_text = dayfont.render(f"Population: {len(ducks)}", True, (255, 255, 255))
        treasurey_text = dayfont.render(f"Treasury: ${government.money}", True, (255, 255, 255))
        screen.blit(treasurey_text, (10, 70))
        screen.blit(population_text, (10, 50))
        screen.blit(time_of_day_text, (10, 30))
        screen.blit(day_text, (10, 10))

    pygame.display.update()

    # ---- Click Detection ---- #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 is Left Click

            if game_state == "menu":
                if start_button.collidepoint(event.pos):

                    game_state = "game"

                    print("Starting Duckonomics...")

                if quit_button.collidepoint(event.pos):

                    pygame.quit()
                    
                    sys.exit()

            if game_state == "game":

                for duck in ducks:
                    if duck.get_rect().collidepoint(event.pos):

                        print("Ducky Clicked")

                        selected_duck = duck