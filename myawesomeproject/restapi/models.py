from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from restapi.validators import *


class Lesson(models.Model):
    name = models.CharField(max_length=50, validators=[validate_name])
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)
    date_time = models.DateTimeField(
        auto_now=False, default=datetime.now, validators=[validate_date_time])
    duration = models.DurationField(default=timedelta(
        minutes=60), validators=[validate_duration])
    cost = models.DecimalField(
        max_digits=6, decimal_places=2, default=10.00, validators=[validate_cost])

    def __str__(self) -> str:
        return f"NAME: {self.name} | INSTRUMENT: {self.instrument} | TEACHER: {self.teacher} | DATE: {self.date_time} | DURATION: {self.duration} | COST: {self.cost}"


class Booking(models.Model):
    student = models.ForeignKey(
        "Student", on_delete=models.CASCADE, related_name='student')
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='lesson')

    def __str__(self) -> str:
        return f"STUDENT: {self.student} | LESSON: {self.lesson}"


class Student(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=50, validators=[
                            validate_name], default='')

    def __str__(self) -> str:
        return f"{self.name}"


class Teacher(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='teacher')
    name = models.CharField(max_length=50, validators=[
                            validate_name], default='')
    
    def __str__(self) -> str:
        return f"{self.name}"


class Instrument(models.Model):
    name = models.CharField(max_length=50, validators=[
                            validate_name], default='')

    def __str__(self) -> str:
        return f"{self.name}"
