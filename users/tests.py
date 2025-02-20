from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserAPITestCase(APITestCase):
    """Тестирование работы контроллеров модели Network."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")

    def setUp(self) -> None:
        self.reset_sequence()

    def test_authorized_user_create(self):
        """Создание пользователя."""

        data = {
            "email": "testuser@test.com",
            "password": "1test"
        }

        response = self.client.post(
            "/users/register/",
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        black_list = ["date_joined", "password"]
        for key in black_list:
            response.json().pop(key)

        self.assertEqual(
            response.json(),
            {'id': 1,
             'last_login': None,
             'is_superuser': False,
             'first_name': '',
             'last_name': '',
             'is_staff': False,
             'is_active': True,
             'email': 'testuser@test.com',
             'groups': [],
             'user_permissions': []
             }
        )

        self.assertTrue(User.objects.filter(pk=1).exists())
