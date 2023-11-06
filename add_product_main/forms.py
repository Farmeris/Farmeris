from django import forms
from login_app.models import UserProfile
from user_profile.forms import UserProfileForm
from .models import Polozka, Cena, Transport, PolozkaTransport
from django.core.validators import FileExtensionValidator


class PictureForm(forms.Form):
    image = forms.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])

class PolozkaForm(forms.ModelForm):
    class Meta:
        model = Polozka
        fields = ['nazov_produktu', 'info_nazov_produktu', 'info_produktu', 'image']

class CenaForm(forms.ModelForm):
    class Meta:
        model = Cena
        fields = ['amount', 'unit', 'price', 'currency']

class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ['transport_type', 'transport_notes', 'price', 'currency', 'amount', 'unit']
