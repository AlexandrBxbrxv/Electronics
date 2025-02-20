from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="API Docs",
        default_version='v0.3',
    ),
    public=True,
    permission_classes=[AllowAny,],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('admin/', admin.site.urls),

    path('users/', include('users.urls', namespace='users')),
    path('electronics/', include('electronics.urls', namespace='electronics')),
]
