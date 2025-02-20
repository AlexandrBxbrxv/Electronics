from rest_framework import serializers

from electronics.models import Contact, Network, Product


class ContactSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Contact."""

    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ("owner",)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product."""

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("owner",)


class BaseNetworkSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели Network."""

    products = ProductSerializer(source='product_network', many=True, read_only=True)
    contacts = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all())
    level = serializers.SerializerMethodField()

    class Meta:
        model = Network
        fields = "__all__"

    @staticmethod
    def get_level(network) -> int:
        """Возвращает уровень сети."""
        if network.supplier is None:
            return 0
        if network.supplier and network.supplier.supplier:
            return 2
        return 1


class CreateNetworkSerializer(BaseNetworkSerializer):
    """Сериализатор для создания модели Network."""

    class Meta(BaseNetworkSerializer.Meta):
        read_only_fields = ("owner",)

    def create(self, validated_data):
        """Устанавливает owner автоматически."""
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class NetworkSerializer(BaseNetworkSerializer):
    """Основной сериализатор для модели Network."""

    class Meta(BaseNetworkSerializer.Meta):
        read_only_fields = ("owner", "debt")
