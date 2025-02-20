from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from electronics.models import Network, Contact, Product
from users.models import User


class AuthorizedNetworkAPITestCase(APITestCase):
    """Тестирование работы контроллеров модели Network."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE electronics_contact_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE electronics_network_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE electronics_product_id_seq RESTART WITH 1;")

    def setUp(self) -> None:

        self.reset_sequence()

        self.today = timezone.now().today().date().strftime("%Y-%m-%d")

        self.user = User.objects.create(
            email="user@test.com",
            password="test"
        )

        self.contacts = Contact.objects.create(
            owner=self.user,
            email="test@mail.ru",
            country="Russia",
            city="Moscow",
            street="Lenina",
            house_number=1
        )

        self.network = Network.objects.create(
            owner=self.user,
            contacts=self.contacts,
            supplier=None,
            title="network",
            debt=0.31,
        )

        self.product = Product.objects.create(
            owner=self.user,
            network=self.network,
            title="product",
            model="v1",
            launch_date="2025-02-25"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_authorized_network_create(self):
        """Создание сети авторизованным пользователем."""

        data = {
            "contacts": self.contacts.pk,
            "supplier": self.network.pk,
            "title": "network_2",
            "debt": 22.36944
        }

        response = self.client.post(
            "/electronics/network/create/",
            data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "level": 1,
                "owner": 1,
                "contacts": 1,
                "products": [],
                "supplier": 1,
                "title": "network_2",
                "debt": 22.37,
                "creation_time": self.today
            }
        )

        self.assertTrue(Network.objects.filter(pk=2).exists())

    def test_authorized_network_list(self):
        """Получение списка объектов сети авторизованным пользователем."""

        response = self.client.get(
            "/electronics/network/list/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{
                "id": 1,
                "level": 0,
                "owner": 1,
                "contacts": 1,
                "products": [{
                    "id": 1,
                    "title": "product",
                    "model": "v1",
                    "launch_date": "2025-02-25",
                    "owner": 1,
                    "network": 1
                }],
                "supplier": None,
                "title": "network",
                "debt": 0.31,
                "creation_time": self.today
            }]
        )

    def test_authorized_network_retrieve(self):
        """Получение объекта сети авторизованным пользователем."""

        response = self.client.get(
            f"/electronics/network/retrieve/{self.network.pk}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "level": 0,
                "owner": 1,
                "contacts": 1,
                "products": [{
                    "id": 1,
                    "title": "product",
                    "model": "v1",
                    "launch_date": "2025-02-25",
                    "owner": 1,
                    "network": 1
                }],
                "supplier": None,
                "title": "network",
                "debt": 0.31,
                "creation_time": self.today
            }
        )

    def test_authorized_network_update(self):
        """Изменение объекта сети авторизованным пользователем."""

        user_2 = User.objects.create(
            email="user2@test.com",
            password="test2"
        )

        data = {
            "id": 3,
            "title": "change",
            "creation_time": "2000-01-01",
            "debt": 5000.778,
            "level": 2,
            "owner": user_2.pk,
            "products": [{}]
        }

        response = self.client.patch(
            f"/electronics/network/update/{self.network.pk}/",
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "level": 0,
                "owner": 1,
                "contacts": 1,
                "products": [{
                    "id": 1,
                    "title": "product",
                    "model": "v1",
                    "launch_date": "2025-02-25",
                    "owner": 1,
                    "network": 1
                }],
                "supplier": None,
                "title": "change",
                "debt": 0.31,
                "creation_time": self.today
            }

        )

    def test_authorized_network_destroy(self):
        """Удаление объекта сети авторизованным пользователем."""

        response = self.client.delete(
            f"/electronics/network/destroy/{self.network.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertTrue(not Network.objects.filter(pk=self.network.pk).exists())


class UnauthorizedNetworkAPITestCase(APITestCase):
    """Тестирование закрытости доступов для контроллеров модели Network."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE electronics_network_id_seq RESTART WITH 1;")

    def setUp(self) -> None:

        self.reset_sequence()

        self.user = User.objects.create(
            email='user@test.com',
            password='test'
        )

        self.network = Network.objects.create(
            owner=self.user,
            title="test"
        )

    def test_unauthorized_network_create(self):
        """Создание сети без авторизации."""

        data = {
            "title": "test"
        }

        response = self.client.post(
            "/electronics/network/create/",
            data=data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertTrue(not Network.objects.filter(pk=2).exists())

    def test_unauthorized_network_list(self):
        """Получение списка объектов сети без авторизации."""

        response = self.client.get(
            "/electronics/network/list/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_network_retrieve(self):
        """Получение объекта сети без авторизации."""

        response = self.client.get(
            f"/electronics/network/retrieve/{self.network.pk}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_network_update(self):
        """Изменение объекта сети без авторизации."""

        data = {
            "title": "change"
        }

        response = self.client.patch(
            f"/electronics/network/update/{self.network.pk}/",
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_network_destroy(self):
        """Удаление объекта сети без авторизации."""

        response = self.client.delete(
            f"/electronics/network/destroy/{self.network.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class OthersNetworkAPITestCase(APITestCase):
    """Тестирование доступов для контроллеров модели Network, работа с чужими объектами не доступна."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE electronics_network_id_seq RESTART WITH 1;")

    def setUp(self) -> None:

        self.reset_sequence()

        self.user = User.objects.create(
            email='user@test.com',
            password='test'
        )

        self.other_user = User.objects.create(
            email='user2@test.com',
            password='test2'
        )

        self.others_network = Network.objects.create(
            owner=self.other_user,
            title="test"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_others_network_retrieve(self):
        """Получение объекта сети другого пользователя."""

        response = self.client.get(
            f"/electronics/network/retrieve/{self.others_network.pk}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_others_network_update(self):
        """Изменение объекта сети другого пользователя."""

        data = {
            "title": "change"
        }

        response = self.client.patch(
            f"/electronics/network/update/{self.others_network.pk}/",
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_others_network_destroy(self):
        """Удаление объекта сети другого пользователя."""

        response = self.client.delete(
            f"/electronics/network/destroy/{self.others_network.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
