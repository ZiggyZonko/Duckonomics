from classes.shop import Shop

class FishMarket(Shop):

    def __init__(self, name):

        super().__init__(
            name,
            "Fish",
            8
        )

        self.food_value = 80