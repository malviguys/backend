import pytest
from django.urls import reverse
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer
from rest_framework.test import APIClient
import json
from rest_framework import status


@pytest.fixture()
def lesson(db):
    return [
        mixer.blend('restapi.Lesson'),
        mixer.blend('restapi.Lesson'),
        mixer.blend('restapi.Lesson')
    ]


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


def test_lessons_anon_user_get_nothing():
    path = reverse('lessons-by-students-list')
    client = get_client()
    response = client.get(path)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert contains(response, 'detail', 'credentials were not provided')


# def test_lesson_name_not_capitalized(db):
#     lesson = mixer.blend('restapi.Lesson', name='wrong name')
#     with pytest.raises(ValidationError):
#         lesson.full_clean()


# def test_lesson_title_of_length_51_rises_exception(db):
#     lesson = mixer.blend('restapi.Lesson', name='A'*60)
#     with pytest.raises(ValidationError) as err:
#         lesson.full_clean()
#     assert 'Lesson name must be less than 50 char' in '\n'.join(
#         err.value.message)


# def test_example1():
#     assert 1==1

# def test_example2():
#     assert 2==2
