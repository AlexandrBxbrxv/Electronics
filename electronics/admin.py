from django.contrib import admin, messages
from django.utils.translation import ngettext

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

    actions = ['clear_debt']

    @admin.action(description='Clear debt from selected networks')
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0.00)
        self.message_user(
            request,
            ngettext(
                "%d debt cleared to zero",
                "%d debts cleared to zero",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Для отображения модели Product в админке."""

    list_display = ('id', 'owner', 'network', 'title', 'model', 'launch_date',)
    search_fields = ('owner', 'network', 'title',)
