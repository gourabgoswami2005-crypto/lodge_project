from django.contrib import admin
from .models import RoomType, Offer, Reservation


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_tag', 'price_per_night', 'max_guests', 'is_available')
    list_editable = ('price_per_night', 'is_available')
    search_fields = ('name', 'category_tag')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_text', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title', 'badge_text')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'room_type', 'check_in_date', 'check_out_date', 'total_price', 'created_at')
    list_filter = ('room_type', 'ac_preference', 'check_in_date')
    search_fields = ('full_name', 'mobile_number', 'email_id')