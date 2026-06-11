import random
import pygame
from sklearn.linear_model import LinearRegression
from constants import *

class Shop:

    def __init__(self, name, product_name, price):

        self.name = name
        self.product_name = product_name

        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)

        self.stock = 100
        self.money = 0

        self.price = price

        self.daily_sales = 0

        self.history = []

        self.model = LinearRegression()
        self.predicted_demand = 20

    def sell(self):

        if self.stock <= 0:
            return False

        self.stock -= 1
        self.money += self.price
        self.daily_sales += 1

        return True

    def train_ai(self, population, avg_hunger):

        self.history.append({
            "population": population,
            "avg_hunger": avg_hunger,
            "price": self.price,
            "sales": self.daily_sales
        })

        if len(self.history) >= 5:

            X = [
                [
                    day["population"],
                    day["avg_hunger"],
                    day["price"]
                ]
                for day in self.history
            ]

            y = [
                day["sales"]
                for day in self.history
            ]

            self.model.fit(X, y)

            self.predicted_demand = max(
                1,
                int(
                    self.model.predict(
                        [[population, avg_hunger, self.price]]
                    )[0]
                )
            )

        self.daily_sales = 0