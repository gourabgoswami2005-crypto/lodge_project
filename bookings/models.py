from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=120)
    category_tag = models.CharField(max_length=80, default="Suites & Rooms")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    max_guests = models.PositiveIntegerField(default=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_night}"


class Offer(models.Model):
    badge_text = models.CharField(max_length=50)
    title = models.CharField(max_length=140)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.badge_text})"


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
    room_type = models.CharField(max_length=120)
    ac_preference = models.CharField(max_length=10, choices=CLIMATE_TYPES, default='AC')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.full_name} ({self.room_type})"