from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from electronics.models import Network
from electronics.serializers import NetworkSerializer
from users.permissions import IsOwner


class NetworkCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания сети."""
    serializer_class = NetworkSerializer
    queryset = Network.objects.all()

    def perform_create(self, serializer):
        """Записывает создателя сети и округляет задолженность до двух цифр после запятой."""
        user = self.request.user
        network = serializer.save()
        network.owner = user
        network.debt = round(network.debt, 2)
        network.save()


class NetworkListAPIView(generics.ListAPIView):
    """Контроллер для просмотра сетей."""
    serializer_class = NetworkSerializer
    queryset = Network.objects.all()


class NetworkRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра сети текущего пользователя."""
    serializer_class = NetworkSerializer
    queryset = Network.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class NetworkUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для обновления сети текущего пользователя."""
    serializer_class = NetworkSerializer
    queryset = Network.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class NetworkDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления сети текущего пользователя."""
    queryset = Network.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
