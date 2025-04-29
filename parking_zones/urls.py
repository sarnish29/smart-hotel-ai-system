
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from parking_zones import views as parkingzoneviews

urlpatterns = [
    path('', parkingzoneviews.index, name='index'),
    path('book/', login_required(parkingzoneviews.ReservationView.as_view()), name='book'),
    path('ticket/', login_required(parkingzoneviews.Ticket_Pdf.as_view()), name='ticket'),
    path('reservations/', login_required(parkingzoneviews.adminreservationview), name='reservations'),
    path('checkout/', parkingzoneviews.check_out, name='checkout')
    ]
