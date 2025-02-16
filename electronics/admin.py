from django.contrib import admin

from electronics.models import Contact, Network, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Для отображения модели Contact в админке."""

    list_display = ('id', 'owner', 'email', 'country', 'city', 'street', 'house_number',)
    search_fields = ('owner', 'email', 'country',)


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    """Для отображения модели Network в админке."""

    list_display = ('id', 'owner', 'contacts', 'supplier', 'title', 'debt', 'creation_time',)
    search_fields = ('owner', 'title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Для отображения модели Product в админке."""

    list_display = ('id', 'owner', 'network', 'title', 'model', 'launch_date',)
    search_fields = ('owner', 'network', 'title',)
