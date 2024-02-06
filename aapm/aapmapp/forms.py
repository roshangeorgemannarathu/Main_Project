from django import forms
from .models import UserProfile  # Replace with your User model

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Replace with your User model
        fields = ['full_name', 'date_of_birth', 'gender', 'phone', 'house_name', 'pin_code', 'district', 'photo_id', 'photo']
