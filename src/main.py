import pygame
import random

# ---- Classes ---- #
from classes.duck import Duck
from classes.bakery import BreadShop

# ---- Pygame Initialization ---- #
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("🦆 Duckonomics")

# ---- Object Arrays ---- #
ducks = []
breadshops = []
waves = []

# ---- Variables ---- #
day = 1
day_timer = 0
day_length = 30  # seconds
population = len(ducks)

# ---- Sprites ---- #
duck_image = pygame.image.load("assets/duck.png").convert_alpha()
duck_scaled = pygame.transform.scale(duck_image, (48, 48))
shop_image = pygame.image.load("assets/shop.png").convert_alpha()
scaled_shop = pygame.transform.scale(shop_image, (30, 30))
wave_image = pygame.image.load("assets/wave.png").convert_alpha()
bread_image = pygame.image.load("assets/bread.png").convert_alpha()
scaled_bread = pygame.transform.scale(bread_image, (20, 20))
dayfont = pygame.font.SysFont(None, 24)

# ---- Generating Objects ---- #
for i in range(5):
    breadshops.append(
        BreadShop(
            f"Bread Shop {i+1}"
        )
    )
    print(f"Created {breadshops[-1].name} at ({breadshops[-1].x}, {breadshops[-1].y})")

for _ in range(20):
    ducks.append(
        Duck(
            random.randint(0, 500),
            random.randint(0, 500)
        )
    )


for _ in range(10):
    waves.append(
        (
            random.randint(0, 500),
            random.randint(0, 500)
        )
    )

for _ in range(5):
    waves.append(
        (
            random.randint(0, 500),
            random.randint(0, 500)
        )
    )

# ---- MAIN GAME LOOP ---- #
while True:

    screen.fill((7, 138, 255))  # Clear screen to black

    # ---- Loops for Objects ---- #
    for wave in waves:
        screen.blit(wave_image, (wave[0], wave[1]))

    for duck in ducks[:]:
        duck.update(breadshops)

        if not duck.alive:
            ducks.remove(duck)
            continue

        duck.draw(screen, duck_scaled)

    for shop in breadshops:
        shop.draw(screen, scaled_shop)
        shop.text(screen, scaled_bread)

    # ---- Day Logic ---- #
    dt = clock.tick(120) / 1000
    day_timer += dt
    hour = (day_timer / day_length)

    if day_timer >= day_length and duck.alive:

        avg_hunger = (
            sum(duck.hunger for duck in ducks)
            / len(ducks)
        )

        for shop in breadshops:
            shop.end_day(
                len(ducks),
                avg_hunger
            )

        day += 1
        day_timer = 0

        print(f"Day {day} has begun!")
    
    # ---- UI ---- #
    day_text = dayfont.render(f"Day {day}", True, (255, 255, 255))
    time_of_day_text = dayfont.render(f"Time: {int(hour * 24)}:00", True, (255, 255, 255))
    population_text = dayfont.render(f"Population: {len(ducks)}", True, (255, 255, 255))
    screen.blit(population_text, (10, 50))
    screen.blit(time_of_day_text, (10, 30))
    screen.blit(day_text, (10, 10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()