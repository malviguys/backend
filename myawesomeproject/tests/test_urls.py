import json
from attr import dataclass
from rest_framework.authtoken.models import Token
import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from restapi.models import *
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from datetime import datetime, timedelta

pytestmark = pytest.mark.django_db


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


@pytest.fixture()
def student(db):
    return [
        mixer.blend('restapi.Student', username='s0',
                    password='s1', user=mixer.blend('restapi.User')),
    ]


@pytest.fixture()
def teacher(db):
    return [
        mixer.blend('restapi.Teacher', username='t1', password='t1'),
    ]


def creteInstrument(n):
    for i in range(n):
        Instrument.objects.create(name='Chitarra'+str(i))


def creteTeacher(n):
    for i in range(n):
        User.objects.create_user(
            't'+str(i), 'nuumo'+str(1)+'@zi.hk', 'MyAwesomePassword.99')
        Teacher.objects.create(
            name='Teacher '+str(i), user=User.objects.get(username='t'+str(i)))


def createStudents(n):
    for i in range(n):
        User.objects.create_user(
            's'+str(i), 'qwerqw'+str(i)+'@zi.hk', 'MyAwesomePassword.99')
        Student.objects.create(
            name='Student '+str(i), user=User.objects.get(username='s'+str(i)))


def createLessons(n):
    for i in range(n):
        Lesson.objects.create(name='Lesson'+str(i), instrument=Instrument.objects.get(name='Chitarra'+str(i)), teacher=Teacher.objects.get(
            name='Teacher '+str(i)), date_time='2021-12-21T20:54:00Z', duration=timedelta(hours=1), cost='10.00')


def createBookings(n):
    for i in range(n):
        Booking.objects.create(student=Student.objects.get(
            name='s'+str(i)), lesson=Lesson.objects.get(name='Lesson'+str(i)))


def test():
    assert 1 == 1


"""
/api/v1/auth/login/	
dj_rest_auth.views.LoginView	
rest_login

/api/v1/auth/logout/	
dj_rest_auth.views.LogoutView	
rest_logout

/api/v1/auth/password/change/	
dj_rest_auth.views.PasswordChangeView	
rest_password_change

/api/v1/auth/password/reset/	
dj_rest_auth.views.PasswordResetView	
rest_password_reset

/api/v1/auth/password/reset/confirm/	
dj_rest_auth.views.PasswordResetConfirmView	
rest_password_reset_confirm

/api/v1/auth/registration	
dj_rest_auth.registration.views.RegisterView	
rest_register

/api/v1/auth/registrationaccount-confirm-email/<key>/	
django.views.generic.base.TemplateView	
account_confirm_email

/api/v1/auth/registrationresend-email/	
dj_rest_auth.registration.views.ResendEmailVerificationView	
rest_resend_email

/api/v1/auth/registrationverify-email/	
dj_rest_auth.registration.views.VerifyEmailView	
rest_verify_email

/api/v1/auth/user/	
dj_rest_auth.views.UserDetailsView	
rest_user_details




/api/v1/booking/	
restapi.views.BookedView	
booking-list

/api/v1/booking/<pk>/	
restapi.views.BookedView	
booking-detail

/api/v1/lessons/	
restapi.views.LessonView	
lessons-list

/api/v1/lessons/<pk>/	
restapi.views.LessonView	
lessons-detail

"""


"""
Test REST API for no-logged user
/api/v1/booking/
booking-list

/api/v1/booking/<pk>/
booking-detail

/api/v1/lessons/
lessons-list

/api/v1/lessons/<pk>/
lessons-detail
"""

# GET /api/v1/lessons/


def test_lessons_anon_user_get_nothing():
    path = reverse('lessons-list')
    client = get_client()
    response = client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'Authentication credentials were not provided.')

# GET /api/v1/booking/


def test_booking_anon_user_get_nothing():
    path = reverse('booking-list')
    client = get_client()
    response = client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'Authentication credentials were not provided.')

# GET /api/v1/lessons/<pk>/


def test_lessons_anon_user_get_nothing_detail(db):
    path = reverse('lessons-detail', kwargs={'pk': 1})
    client = get_client()
    response = client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'Authentication credentials were not provided.')

# GET /api/v1/booking/<pk>/


def test_booking_anon_user_get_nothing_detail(db):
    path = reverse('booking-detail', kwargs={'pk': 1})
    client = get_client()
    response = client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'Authentication credentials were not provided.')


# GET /api/v1/lessons/<pk>/


def test_lessons_anon_user_post_nothing_detail(db):
    path = reverse('lessons-detail', kwargs={'pk': 1})
    client = get_client()
    response = client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'Authentication credentials were not provided.')

# GET /api/v1/booking/<pk>/


def test_booking_anon_user_post_nothing_detail(db):
    path = reverse('booking-detail', kwargs={'pk': 1})
    client = get_client()
    response = client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert contains(response, 'detail',
                    'Authentication credentials were not provided.')

# STUDENT


def test_login_as_student(db):
    User.objects.create_user('s0', 'vew@dindela.vi', 'MyAwesomePassword.99')
    Student.objects.create(
        name="Student 0", user=User.objects.get(username='s0'))
    client = get_client()
    response = client.post(reverse('rest_login'), {
                           'username': 's0', 'password': 'MyAwesomePassword.99'}, format='json')
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['key']


def test_as_student_get_lessons(db):
    creteInstrument(3)
    creteTeacher(3)
    createLessons(3)
    createStudents(1)
    client = get_client()
    user = User.objects.get(username='s0')
    # TODO Sostituire con un login "regolare"
    client.force_authenticate(user=user)
    response = client.get(reverse('lessons-list'))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    assert response.data[0]['name'] == 'Lesson0'


def test_student_cant_post_lessons(db):
    creteTeacher(1)
    createStudents(1)
    creteInstrument(1)
    client = get_client()
    user = User.objects.get(username='s0')
    client.force_authenticate(user=user)
    response = client.post(reverse('lessons-list'), {
        "name": "Lezione di Chitarra XYZ",
        "instrument": 1,
        "teacher": 1,
        "date_time": "2021-12-21T20:54:00Z",
        "duration": "01:00:00",
        "cost": "11.50",
    }, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert contains(response, 'detail',
                    'You do not have permission to perform this action.')


def test_student_cant_delete_lessons():
    creteTeacher(1)
    createStudents(1)
    creteInstrument(1)
    createLessons(1)
    client = get_client()
    user = User.objects.get(username='s0')
    print(user.username)
    client.force_authenticate(user=user)
    response = client.delete(reverse('lessons-detail', kwargs={'pk': 1}))
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert contains(response, 'detail',
                    'You do not have permission to perform this action.')


def test_student_cant_update_lessons():
    creteTeacher(1)
    createStudents(1)
    creteInstrument(1)
    createLessons(1)
    client = get_client()
    user = User.objects.get(username='s0')
    print(user.username)
    client.force_authenticate(user=user)
    response = client.put(reverse('lessons-detail', kwargs={'pk': 1}), data={
        "name": "Lezione di Chitarra XYZ",
        "instrument": 1,
        "teacher": 1,
        "date_time": "2021-12-21T20:54:00Z",
        "duration": "01:00:00",
        "cost": "11.50",
    }, content_type='application/json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert contains(response, 'detail',
                    'You do not have permission to perform this action.')

# def student_view_only_own_booking():
#     assert 1 != 1


# def student_can_create_booking():
#     assert 1 != 1


# def student_can_delete_only_onw_booking():
#     assert 1 != 1


# def student_can_update_only_own_booking():
#     assert 1 != 1


# # TEACHER
def test_login_as_teacher(db):
    creteTeacher(1)
    client = get_client()
    response = client.post(reverse('rest_login'), {
                           'username': 't0', 'password': 'MyAwesomePassword.99'}, format='json')
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['key']


def test_teacher_can_post_lessons(db):
    creteInstrument(1)
    creteTeacher(1)
    createStudents(1)
    client = get_client()
    user = User.objects.get(username='t0')
    # TODO Sostituire con un login "regolare"
    client.force_authenticate(user=user)

    response = client.post(reverse('lessons-list'), {
        "name": "Chitarra XYZ",
        "instrument": 1,
        "teacher": 1,
        "date_time": "2021-12-21T20:54:00Z",
        "duration": "01:00:00",
        "cost": "10.00",
    }, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Chitarra XYZ'


def test_teacher_can_delete_only_own_lessons():
    creteTeacher(1)
    createStudents(1)
    creteInstrument(1)
    createLessons(1)
    client = get_client()
    user = User.objects.get(username='t0')
    client.force_authenticate(user=user)
    response = client.delete(reverse('lessons-detail', kwargs={'pk': 1}))
    assert response.status_code == status.HTTP_204_NO_CONTENT

# def test_teacher_cant_post_lessons_with_invalid_data(db):
#     pass


def test_teacher_can_update_own_lessons():
    creteTeacher(2)
    createStudents(1)
    creteInstrument(1)
    createLessons(1)
    client = get_client()
    user = User.objects.get(username='t0')
    print(user.username)
    client.force_authenticate(user=user)
    response = client.put(reverse('lessons-detail', kwargs={'pk': 1}), data={
        "id": 1,
        "name": "Lezione di Chitarra XYZ",
        "instrument": 1,
        "teacher": 1,
        "date_time": "2021-12-21T20:54:00Z",
        "duration": "01:00:00",
        "cost": "11.50",
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Lezione di Chitarra XYZ'


def test_teacher_can_update_only_own_lessons():
    creteTeacher(2)
    createStudents(1)
    creteInstrument(1)
    createLessons(1)
    client = get_client()
    user = User.objects.get(username='t1')
    print(user.username)
    client.force_authenticate(user=user)
    response = client.put(reverse('lessons-detail', kwargs={'pk': 1}), data={
        "id": 1,
        "name": "Lezione di Chitarra XYZ",
        "instrument": 1,
        "teacher": 1,
        "date_time": "2021-12-21T20:54:00Z",
        "duration": "01:00:00",
        "cost": "11.50",
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert contains(response, 'detail',
                    'You do not have permission to perform this action.')
