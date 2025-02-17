from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ngettext

from electronics.models import Contact, Network, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Для отображения модели Contact в админке."""

    list_display = ('id', 'owner', 'email', 'country', 'city', 'street', 'house_number',)
    search_fields = ('owner__email', 'email', 'country',)


class NetworkAdmin(admin.ModelAdmin):
    """Для отображения модели Network в админке."""

    list_display = ('id', 'owner', 'contacts', 'supplier_link', 'title', 'debt', 'creation_time',)
    search_fields = ('contacts__city',)

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

    def supplier_link(self, obj):
        """Создает ссылку на поставщика."""
        if obj.supplier:
            url = reverse("admin:electronics_network_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.title)
        return "-"

    supplier_link.short_description = "Поставщик"


admin.site.register(Network, NetworkAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Для отображения модели Product в админке."""

    list_display = ('id', 'owner', 'network', 'title', 'model', 'launch_date',)
    search_fields = ('owner__email', 'network', 'title',)
