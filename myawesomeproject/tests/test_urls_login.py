from .init import *
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from restapi.models import *

pytestmark = pytest.mark.django_db


class TestLogin:
    def test_login_as_student(self, db):
        User.objects.create_user(
            's0', 'vew@dindela.vi', 'MyAwesomePassword.99')
        Student.objects.create(
            name="Student 0", user=User.objects.get(username='s0'))
        client = get_client()
        response = client.post(reverse('rest_login'), {
            'username': 's0', 'password': 'MyAwesomePassword.99'}, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['key']

    def test_login_as_teacher(self, db):
        creteTeacher(1)
        client = get_client()
        response = client.post(reverse('rest_login'), {
            'username': 't0', 'password': 'MyAwesomePassword.99'}, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['key']


