# adding rooms and offers

from django import forms
from .models import RoomType, Offer


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ["name", "category_tag", "price_per_night", "max_guests", "description", "is_available"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g., Alpine Deluxe Suite"}),
            "category_tag": forms.TextInput(attrs={"placeholder": "e.g., Suites & Rooms"}),
            "price_per_night": forms.NumberInput(attrs={"placeholder": "e.g., 4500", "step": "0.01"}),
            "max_guests": forms.NumberInput(attrs={"min": 1}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Describe room features and view..."}),
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ["badge_text", "title", "description", "is_active"]
        widgets = {
            "badge_text": forms.TextInput(attrs={"placeholder": "e.g., Save 20% or Weekend Deal"}),
            "title": forms.TextInput(attrs={"placeholder": "e.g., Monsoon Mountain Escape"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Offer details and terms..."}),
        }