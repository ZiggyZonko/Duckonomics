import random
import pygame
from sklearn.linear_model import LinearRegression
from constants import *

class BreadShop:
    def __init__(self, name):
        self.name = name

        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)

        self.stock = 100
        self.money = 0
        self.price = 5

        self.daily_sales = 0

        self.history = []

        self.model = LinearRegression()
        self.predicted_demand = 20

    def draw(self, screen, image):
        screen.blit(image, (self.x, self.y))

    def update(self):
        pass

    def sell_bread(self):
        """Attempt to sell one loaf of bread."""

        if self.stock <= 0:
            return False

        self.stock -= 1
        self.money += self.price
        self.daily_sales += 1

        return True

    def end_day(self, population, avg_hunger):

        # Store today's data
        self.history.append({
            "population": population,
            "avg_hunger": avg_hunger,
            "price": self.price,
            "sales": self.daily_sales
        })

        # Train once we have enough data
        if len(self.history) >= 1:

            X = []
            y = []

            for day in self.history:
                X.append([
                    day["population"],
                    day["avg_hunger"],
                    day["price"]
                ])

                y.append(day["sales"])

            self.model.fit(X, y)

            self.predicted_demand = max(
                1,
                int(
                    self.model.predict([
                        [
                            population,
                            avg_hunger,
                            self.price
                        ]
                    ])[0]
                )
            )

        # Restock using prediction
        target_stock = int(self.predicted_demand * 1.2) + 5

        if self.stock < target_stock:

            loaves_to_bake = target_stock - self.stock

            # Optional production cost
            production_cost = loaves_to_bake * 1

            if self.money >= production_cost:
                self.money -= production_cost
                self.stock += loaves_to_bake

        print(
            f"{self.name} | "
            f"Sales: {self.daily_sales} | "
            f"Prediction: {self.predicted_demand} | "
            f"Stock: {self.stock} | "
            f"Money: ${self.money:.0f}"
        )

        # Reset for tomorrow
        self.daily_sales = 0

    def text(self, screen, icon):
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"$ {self.money:.0f}", True, (255, 255, 255))
        stockicon = (icon, (self.x - 25, self.y - 25))
        stock = font.render(f"{self.stock}", True, (255, 255, 255))
        screen.blit(text, (self.x - 12.5, self.y - 50))
        screen.blit(stockicon[0], stockicon[1])
        screen.blit(stock, (self.x - 12.5, self.y - 25))