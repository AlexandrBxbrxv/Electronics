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


class NetworkSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Network."""

    products = ProductSerializer(source='product_network', many=True)
    contacts = ContactSerializer()
    level = serializers.SerializerMethodField()

    class Meta:
        model = Network
        fields = "__all__"
        read_only_fields = ("owner", "debt")

    @staticmethod
    def get_level(network) -> int:
        """Возвращает цифру уровня на котором находится сеть."""
        if network.supplier is None:
            return 0
        if network.supplier:
            if network.supplier.supplier:
                return 2
            return 1
