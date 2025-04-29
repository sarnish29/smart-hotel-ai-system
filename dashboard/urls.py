from django.conf.urls import include
from django.urls import path, re_path
import booking.views as bviews
import dashboard.views as dviews

urlpatterns = [
    # path('', views.login_view),
    # # path('login/', views.login_view),
    # url('register/', views.register_view),
    # path('logout/', views.logout_view),
    path('dashboard/', dviews.dashboard_view),
    re_path(r"^details/(?P<dustbin_id>\d+)/$", dviews.details_view),
]
