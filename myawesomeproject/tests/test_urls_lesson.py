from .init import *
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from restapi.models import *

pytestmark = pytest.mark.django_db


class TestLessons:
    def test_lessons_anon_user_get_nothing(self):
        path = reverse('lessons-list')
        client = get_client()
        response = client.get(path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert contains(response, 'detail',
                        'Authentication credentials were not provided.')

    def test_lessons_anon_user_get_nothing_detail(self, db):
        path = reverse('lessons-detail', kwargs={'pk': 1})
        client = get_client()
        response = client.get(path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert contains(response, 'detail',
                        'Authentication credentials were not provided.')

    def test_lessons_anon_user_post_nothing_detail(self, db):
        path = reverse('lessons-detail', kwargs={'pk': 1})
        client = get_client()
        response = client.get(path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert contains(response, 'detail',
                        'Authentication credentials were not provided.')

    def test_teacher_can_post_lessons(self, db):
        initDB(3)
        client = get_client()
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('t0'))

        response = client.post(reverse('lessons-list'), {
            "name": "Chitarra 1",
            "teacher": {
                "id": 1,
                "name": "t0",
                "user": 4
            },
            "instrument": {
                "id": 1,
                "name": "Guitar"
            },
            "date_time": "2021-12-21T21:54:00+01:00",
            "duration": "02:00:00",
            "cost": "10.00"
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Chitarra 1'

    def test_teacher_can_delete_only_own_lessons(self):
        initDB(3)
        client = get_client()
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('t0'))
        response = client.delete(reverse('lessons-detail', kwargs={'pk': 1}))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_teacher_can_update_own_lessons(self):
        initDB(3)
        client = get_client()
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('t0'))
        response = client.put(reverse('lessons-detail', kwargs={'pk': 1}), data={
            "name": "Chitarra 1000",
            "teacher": {
                "id": 1,
                "name": "t0",
                "user": 1
            },
            "instrument": {
                "id": 1,
                "name": "Guitar"
            },
            "date_time": "2021-12-21T21:54:00+01:00",
            "duration": "02:00:00",
            "cost": "10.00"
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Chitarra 1000'

    def test_teacher_can_update_only_own_lessons(self):
        initDB(3)
        client = get_client()
        client.credentials(HTTP_AUTHORIZATION='Token ' + loginToApi('t0'))
        response = client.put(reverse('lessons-detail', kwargs={'pk': 2}), data={
            "id": 2,
            "name": "Chitarra 1000",
            "teacher": {
                "id": 2,
                "name": "t1",
                "user": 5
            },
            "instrument": {
                "id": 1,
                "name": "Guitar"
            },
            "date_time": "2021-12-21T21:54:00+01:00",
            "duration": "02:00:00",
            "cost": "10.00"
        }, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert contains(response, 'detail',
                        'You do not have permission to perform this action.')
