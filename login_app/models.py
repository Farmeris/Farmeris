from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

import os
import uuid
from django.utils.text import slugify
#from django.apps import apps

def upload_to2(instance, filename):
    truncated_username = slugify(instance.user.username[:10])

    # The rest of the logic remains the same:
    original_filename = os.path.splitext(filename)[0]
    slugified_filename = slugify(original_filename)
    unique_filename = f'{truncated_username}-{slugified_filename}-{uuid.uuid4()}'
    ext = filename.split('.')[-1]
    full_filename = f'{slugify(unique_filename)}.{ext}'

    # The storage path is modified. We'll store the avatar in a folder named 'avatar' inside the user's folder:
    return os.path.join('obrasteky', slugify(instance.user.username), 'avatar', full_filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #color theme
    theme = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    
    # Personal details
    avatar = models.ImageField(upload_to=upload_to2, null=True, blank=True)
    website = models.URLField(_('website'), blank=True, null=True)
    social_media = models.URLField(_('social media'), blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    languages = models.CharField(_('languages'), max_length=100, blank=True, null=True)
    location = models.CharField(_('location'), max_length=150, blank=True, null=True)
    bio = models.TextField(_('bio'), blank=True, null=True)

    # Address details
    street_address = models.CharField(_('street-address'), max_length=255, blank=True, null=True)
    city = models.CharField(_('city'), max_length=50, blank=True, null=True)
    state_province = models.CharField(_('state'), max_length=50, blank=True, null=True)
    zip_postal_code = models.CharField(_('zipcode'), max_length=12, blank=True, null=True)
    country = models.CharField(_('country'), max_length=50, blank=True, null=True)

    #saving pagination preference
    pagination_preference = models.PositiveIntegerField(default=10)

    #languages
    PREFERRED_LANGUAGES = [
        ('sk', _('Slovak')),
        ('en', _('English')),
        ('cz', _('Czech')),
    ]
    preferred_language = models.CharField(_('preferred language'), max_length=10, choices=PREFERRED_LANGUAGES, default='sk')

    def __str__(self):
        return self.user.username

