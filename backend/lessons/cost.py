from django.db import models

class Cost(models.Field):
    def __init__(self, euros:int=0, cents:int=0):
        if euros < 0 or cents < 0 :
            raise ValueError("You can't create a cost with negative values!")
        if cents >= 100:
            raise ValueError("Cents can go from 0 to 99!")
            # self.euros = cents % 100
            # self.cents = cents // (100 * cents%100)
            # self.cents = cents - euros * 100
        else:
            self.euros = euros
            self.cents = cents
