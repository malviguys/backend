import json
import pytest
from django.urls import reverse, resolve
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from restapi.models import *
from datetime import datetime, timedelta

pytestmark = pytest.mark.django_db


def get_client(student=None):
    res = APIClient()
    if student is not None:
        res.force_login(student)
    return res


def parse(response):
    response.render()
    content = response.content.decode()
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


def loginToApi(username):
    post = get_client().post(reverse('rest_login'), {
        'username': username, 'password': 'MyAwesomePassword.99'}, format='json')
    return post.data['key']


def creteInstrument(n):
    for i in range(n):
        Instrument.objects.create(name='Chitarra' + str(i))


def creteTeacher(n):
    for i in range(n):
        User.objects.create_user(
            't' + str(i), 'nuumo' + str(1) + '@zi.hk', 'MyAwesomePassword.99')
        Teacher.objects.create(
            name='Teacher ' + str(i), user=User.objects.get(username='t' + str(i)))


def createStudents(n):
    for i in range(n):
        User.objects.create_user(
            's' + str(i), 'qwerqw' + str(i) + '@zi.hk', 'MyAwesomePassword.99')
        Student.objects.create(
            name='Student ' + str(i), user=User.objects.get(username='s' + str(i)))


def createLessons(n):
    for i in range(n):
        Lesson.objects.create(name='Lesson' + str(i), instrument=Instrument.objects.get(name='Chitarra' + str(i)),
                              teacher=Teacher.objects.get(
            name='Teacher ' + str(i)), date_time='2021-12-21T20:54:00Z', duration=timedelta(hours=1),
            cost='10.00')


def createBookings(n):
    for i in range(n):
        Booking.objects.create(student=Student.objects.get(
            user=User.objects.get(username='s' + str(i))), lesson=Lesson.objects.get(name='Lesson' + str(i)))


def initDB(n):
    createStudents(n)
    creteInstrument(n)
    creteTeacher(n)
    createLessons(n)
    createBookings(n)
