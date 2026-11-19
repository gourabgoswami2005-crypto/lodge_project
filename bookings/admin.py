from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Room, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('get_room_name_display', 'base_price_per_night', 'max_adults')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'room_type', 'check_in_date', 'check_out_date', 'total_price', 'created_at')
    list_filter = ('room_type', 'ac_preference', 'check_in_date')
    search_fields = ('full_name', 'mobile_number', 'email_id')