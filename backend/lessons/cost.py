from django.db import models
from math import modf, floor

class Cost():
    def __init__(self, cost:float):
        cents, euros = modf(cost)
        cents = floor(cents*100)
        euros = floor(euros)
        if euros < 0 or cents < 0 :
            raise ValueError("You can't create a cost with negative values!")
        if cents >= 100:
            self.euros = euros + (cents // 100)
            self.cents = cents % 100
        else:
            self.euros = euros
            self.cents = cents

class CostField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs =  super().deconstruct()
        return name, path, args, kwargs
