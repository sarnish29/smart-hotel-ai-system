from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    # path('login', views.login_request, name='login'),
    # path('register/', views.register, name='register'),
    path('logout', views.logout_request, name='logout'),
    #path('Pizza', views.pizza, name='pizza'),
    path('Pakistani_Cuisine', views.pakistani_cuisine, name='pakistani_cuisine'),
    path('French_Cuisine', views.french_cuisine, name='french_cuisine'),
    path('Mexican_Cuisine', views.mexican_cuisine, name='mexican_cuisine'),
    path('Italian_Cuisine', views.italian_cuisine, name='italian_cuisine'),
    path('Turkish_Cuisine', views.turkish_cuisine, name='turkish_cuisine'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('view-orders', views.view_orders, name='view_orders'),
    path('mark_order_as_delivered', views.mark_order_as_delivered, name='mark_order_as_delivered'),
    path('save_cart', views.save_cart, name='save_cart'),
    path('retrieve_saved_cart', views.retrieve_saved_cart, name='retrieve_saved_cart'),
    path('check_superuser', views.check_superuser, name='check_superuser'),
]
