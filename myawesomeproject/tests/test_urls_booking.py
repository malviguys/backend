from .init import *
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from restapi.models import *

pytestmark = pytest.mark.django_db

class TestBooking:

    def test_booking_anon_user_get_nothing(self):
        path = reverse('booking-list')
        client = get_client()
        response = client.get(path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert contains(response, 'detail',
                        'Authentication credentials were not provided.')

    def test_booking_anon_user_get_nothing_detail(self):
        path = reverse('booking-detail', kwargs={'pk': 1})
        client = get_client()
        response = client.get(path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert contains(response, 'detail',
                        'Authentication credentials were not provided.')

    def test_booking_anon_user_post_nothing_detail(self):
        path = reverse('booking-detail', kwargs={'pk': 1})
        client = get_client()
        response = client.get(path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert contains(response, 'detail',
                        'Authentication credentials were not provided.')

    def test_student_view_only_own_booking(self):
        initDB(3)
        user = User.objects.get(username='s0')
        client = get_client()
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('s0'))
        response = client.get(reverse('booking-list'))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['student']['user'] == user.id

    def test_student_can_create_booking(self):
        initDB(3)
        client = get_client()
        user = User.objects.get(username='s0')
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('s0'))
        response = client.post(reverse('booking-list'), {
            "student": {
                "id": 1,
                "name": "Studente 1",
                "user": 1
            },
            "lesson": {
                "id": 1
            }
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['student']['user'] == user.id

    def test_student_can_create_only_onw_booking(self):
        initDB(3)
        client = get_client()
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('s0'))
        response = client.post(reverse('booking-list'), {
            "student": {
                "id": 2,
                "name": "Studente 2",
                "user": 2
            },
            "lesson": {
                "id": 2
            }
        }, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert contains(response, 'detail',
                        'You do not have permission to perform this action.')

    def test_student_can_update_own_booking(self):
        initDB(3)
        client = get_client()
        user = User.objects.get(username='s0')
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('s0'))
        response = client.put(reverse('booking-detail', kwargs={'pk': 1}), {
            "student": {
                "id": 1,
                "name": "Studente 0",
                "user": 1
            },
            "lesson": {
                "id": 3
            }
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['student']['user'] == user.id

    def test_student_can_update_only_own_booking(self):
        initDB(3)
        client = get_client()
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('s0'))

        response = client.put(reverse('booking-detail', kwargs={'pk': 2}), {
            "id": 2,
            "student": {
                "id": 1,
                "name": "Studente 0",
                "user": 1
            },
            "lesson": {
                "id": 1
            }
        }, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert contains(response, 'detail',
                        'Not found.')
