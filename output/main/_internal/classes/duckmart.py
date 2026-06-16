from classes.shop import Shop

class DuckMart(Shop):

    def __init__(self, name):

        super().__init__(
            name,
            "Luxury",
            20
        )