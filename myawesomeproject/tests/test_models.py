from datetime import datetime
import json

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def get_client(student=None):
    res = APIClient()
    if student is not None:
        res.forse_login(student)
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


@pytest.fixture()
def lesson(db):
    return [
        mixer.blend('restapi.Lesson'),
        mixer.blend('restapi.Lesson'),
        mixer.blend('restapi.Lesson')
    ]


@pytest.fixture()
def booking(db):
    return [
        mixer.blend('restapi.Booking'),
        mixer.blend('restapi.Booking'),
        mixer.blend('restapi.Booking')
    ]


def test():
    assert 1 == 1

def test_lesson_name_not_capitalized(db):
    lesson = mixer.blend('restapi.Lesson', name='sasdasdas dong name', date_time=datetime(2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")))
    with pytest.raises(ValidationError) as err:
        lesson.full_clean()
    assert 'Lesson name must be capitalized' in str(err)

def test_lesson_title_of_length_51_rises_exception(db):
    lesson = mixer.blend('restapi.Lesson', name='A' * 51, date_time=datetime(2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")))
    with pytest.raises(ValidationError) as err:
        lesson.full_clean()
    assert 'Lesson name must be less than 50 char' in str(err)


