import math
import random
import pygame 
from classes import *

class Government:

    def __init__(self):

        self.money = 0

        self.income_tax_rate = 0.15
        self.business_tax_rate = 0.10

        self.total_income_tax = 0
        self.total_business_tax = 0

    def collect_income_tax(self, wage):

        tax = wage * self.income_tax_rate

        self.money += tax
        self.total_income_tax += tax

        return wage - tax

    def collect_business_tax(self, shop):

        tax = shop.money * self.business_tax_rate

        shop.money -= tax

        self.money += tax
        self.total_business_tax += tax