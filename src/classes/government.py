import math
import random
import pygame 
from classes import *

class Government:
    def __init__(self):
        self.money = 0
        self.income_tax_rate = 0.15

    def collect_income_tax(self, wage):
        tax = wage * self.income_tax_rate

        self.money += tax

        return wage - tax