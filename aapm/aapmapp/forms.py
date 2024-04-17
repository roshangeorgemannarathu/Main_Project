from django import forms
from .models import UserProfile  # Replace with your User model

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Replace with your User model
        fields = ['full_name', 'date_of_birth', 'gender', 'phone', 'house_name', 'pin_code', 'district', 'photo_id', 'photo']


from django import forms
from .models import Delivery, DeliveryMan

class DeliveryAssignmentForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['address', 'delivery_time', 'delivery_man']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['delivery_man'].queryset = DeliveryMan.objects.all()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))