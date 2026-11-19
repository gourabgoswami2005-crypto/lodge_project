from django.db import models

# Create your models here.

from django.db import models
                                                                      
class Room(models.Model):                                           
    ROOM_TYPES = [
        ('deluxe', 'Deluxe Lodge Room'),
        ('suite', 'Alpine Panorama Suite'),
        ('cabin', 'Private Timber Cabin'),
        ('igloo', 'Stargazer Glass Igloo'),
        ('treehouse', 'Pine Needle Treehouse'),
        ('chalet', 'Royal Heritage Chalet'),
        ('glass_pod', 'Cliffside Glass Pod'),
        ('family_villa', 'Valley View Family Villa'),
        ('river_cabin', 'Riverfront Log Cabin'),
    ]
    
    room_name = models.CharField(max_length=50, choices=ROOM_TYPES, unique=True)
    base_price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    max_adults = models.PositiveIntegerField(default=2)
    max_children = models.PositiveIntegerField(default=1)
    description = models.TextField()

    def __str__(self):
        return f"{self.get_room_name_display()} - ₹{self.base_price_per_night}/night"

class Reservation(models.Model):
    CLIMATE_TYPES = [
        ('AC', 'Air Conditioned (AC)'),
        ('Non-AC', 'Non-Air Conditioned (Non-AC)'),
    ]

    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10)
    aadhaar_card = models.CharField(max_length=12)
    email_id = models.EmailField()
    voter_card = models.CharField(max_length=50, blank=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    adults = models.PositiveIntegerField(default=2)
    children = models.PositiveIntegerField(default=0)
    room_type = models.CharField(max_length=20)
    ac_preference = models.CharField(max_length=10, choices=CLIMATE_TYPES, default='AC')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.full_name} ({self.room_type})"