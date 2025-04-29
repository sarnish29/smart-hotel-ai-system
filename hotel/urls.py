from django.contrib import admin
from django.urls import path, include
from orders import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('booking.urls')),
    path('order/', include('orders.urls')),
    path('checkout', views.checkout, name='checkout'),
    path('mark_order_as_delivered', views.mark_order_as_delivered, name='mark_order_as_delivered'),
    path('garbage/', include('dashboard.urls')),
    path('parking/', include('parking_zones.urls')),
    path('ledger/', include('ledger.urls')),
    path('personalized/', include('personalized_guest_experience.urls')),
    path('chatbot/', include('chatbot.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
