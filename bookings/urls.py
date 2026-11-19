from django.urls import path
from .views import (
    home_view, 
    booking_view, 
    book_room_api, 
    signup_view, 
    signin_view, 
    logout_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('booking/', booking_view, name='booking'),
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('api/book/', book_room_api, name='book_room'),
]