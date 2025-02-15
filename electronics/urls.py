from django.urls import path

from electronics.apps import ElectronicsConfig
from electronics.views import NetworkCreateAPIView, NetworkListAPIView, NetworkRetrieveAPIView, NetworkUpdateAPIView, \
    NetworkDestroyAPIView

app_name = ElectronicsConfig.name

urlpatterns = [
    path('network/create/', NetworkCreateAPIView.as_view(), name='network_create'),
    path('network/list/', NetworkListAPIView.as_view(), name='network_list'),
    path('network/retrieve/<int:pk>/', NetworkRetrieveAPIView.as_view(), name='network_retrieve'),
    path('network/update/<int:pk>/', NetworkUpdateAPIView.as_view(), name='network_update'),
    path('network/destroy/<int:pk>/', NetworkDestroyAPIView.as_view(), name='network_destroy'),
]
