import pygame
import random

# ---- Classes ---- #
from classes.duck import Duck
from classes.shop import BreadShop

# ---- Pygame Initialization ---- #
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("🦆 Duckonomics")

# ---- Sprites ---- #
duck_image = pygame.image.load("assets/duck.png").convert_alpha()
duck_scaled = pygame.transform.scale(duck_image, (32, 32))

# ---- Object Arrays ---- #
ducks = []
breadshops = []

# ---- Generating Objects ---- #
for i in range(5):
    breadshops.append(
        BreadShop(
            f"Bread Shop {i+1}"
        )
    )
    print(f"Created {breadshops[-1].name} at ({breadshops[-1].x}, {breadshops[-1].y})")

for i in range(20):
    ducks.append(
        Duck(
            random.randint(0, 500),
            random.randint(0, 500)
        )
    )


# ---- MAIN GAME LOOP ---- #
while True:

    screen.fill((7, 138, 255))  # Clear screen to black

    for duck in ducks:
        duck.update(breadshops)
        duck.draw(screen, duck_scaled)

    for shop in breadshops:
        shop.draw(screen)

    clock.tick(60)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()