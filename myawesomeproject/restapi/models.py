from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from restapi.validators import *


class Lesson(models.Model):

    TEACHER_CHOICES = [
        ('P', 'PAOLA'),
        ('G', 'GIADA'),
        ('K', 'KRESTEN'),
        ('I', 'IKRAM'),
        ('C', 'CLAUDIO'),
    ]

    INSTRUMENT_CHOICES = [
        ('G', 'GUITAR'),
        ('T', 'TRIANGLE'),
        ('P', 'PIANO'),
        ('U', 'UKULELE'),
    ]

    name = models.CharField(max_length=50, validators=[validate_name])

    teacher = models.CharField(
        max_length=2,
        choices=TEACHER_CHOICES,
        default='P', validators=[validate_teacher]
    )

    instrument = models.CharField(
        max_length=2,
        choices=INSTRUMENT_CHOICES,
        default='G', validators=[validate_instrument]
    )

    students = models.ManyToManyField(
        get_user_model())
    date_time = models.DateTimeField(
        auto_now=False, default=datetime.now, validators=[validate_date_time])
    duration = models.DurationField(default=timedelta(
        minutes=60), validators=[validate_duration])
    cost = models.DecimalField(
        max_digits=6, decimal_places=2, default=10.00, validators=[validate_cost])

    def get_students(self):
        return self.students.all()

    def __str__(self) -> str:
        return f"NAME: {self.name} | INSTRUMENT: {self.instrument} | TEACHER: {self.teacher} | DATE: {self.date_time} | DURATION: {self.duration} | COST: {self.cost} | STUDENT: {self.students.all()}"
