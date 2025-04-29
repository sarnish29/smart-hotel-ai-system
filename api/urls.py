from django.urls import path, include, re_path
from . import views

urlpatterns = [
    # Custom entry route
    re_path(r'^(?P<id>\d+)/(?P<level>.+)/$', views.add_entry, name='add_entry'),

    # Modular API routers
    path('', views.health_check),  # Optional health check
    path('booking/', include('booking.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('guest-ledger/', include('guest_ledger.urls')),
    path('hotel/', include('hotel.urls')),
    path('orders/', include('orders.urls')),
    path('parking/', include('parking_zones.urls')),
    path('network/', include('guest_blockchain_network.urls')),

]
