from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Lesson(models.Model):
    name = models.CharField(max_length=70)
    teacher = models.CharField(max_length=70)
    instrument = models.CharField(max_length=40)
    students = models.ManyToManyField(get_user_model())
    date_time = models.DateTimeField(auto_now=False)
    duration = models.DurationField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self) -> str:
        return f"Lesson {self.name} of instrument {self.instrument}\n- presented by: {self.teacher}\nDate and time:{self.date_time}"