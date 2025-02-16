from django.db import models

from users.models import User, NULLABLE


class Contact(models.Model):
    """Модель контактов сети."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact_owner", verbose_name="владелец")

    email = models.EmailField(verbose_name="email")
    country = models.CharField(max_length=100, verbose_name="страна")
    city = models.CharField(max_length=100, verbose_name="город")
    street = models.CharField(max_length=150, verbose_name="улица")

    house_number = models.PositiveSmallIntegerField(verbose_name="номер дома")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'контакты сети'
        verbose_name_plural = 'контакты сетей'


class Network(models.Model):
    """Модель сеть."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="network_owner", verbose_name="владелец")
    contacts = models.ForeignKey(Contact, **NULLABLE, on_delete=models.SET_NULL, related_name="network_contacts",
                                 verbose_name="контакты")
    supplier = models.ForeignKey("Network", **NULLABLE, on_delete=models.SET_NULL, related_name="network_supplier",
                                 verbose_name="поставщик")

    title = models.CharField(max_length=250, verbose_name="наименование")
    debt = models.FloatField(default=0.00, verbose_name="задолженность перед поставщиком")
    creation_time = models.DateField(auto_now=True, verbose_name="дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сеть'
        verbose_name_plural = 'сети'


class Product(models.Model):
    """Модель продукта сети."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_owner", verbose_name="владелец")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name="product_network", verbose_name="сеть")

    title = models.CharField(max_length=200, verbose_name="наименование")
    model = models.CharField(max_length=200, verbose_name="модель")
    launch_date = models.DateField(verbose_name="дата выхода на рынок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
