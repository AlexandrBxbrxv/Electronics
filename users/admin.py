from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Для отображения модели User в админке."""

    list_display = ('id', 'email', 'is_active',)
    search_fields = ('email',)
    list_filter = ('is_active',)
