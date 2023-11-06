from django.db import models
from django.contrib.auth.models import User
from login_app.models import UserProfile 
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from add_product_main.constants import SLOVAK_MONTHS_SHORTENED
#from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.utils import timezone
#from haystack import indexes
import os
import uuid

def upload_to(instance, filename):
    # Get the first 10 characters of the username and slugify it
    truncated_username = slugify(instance.user_profile.user.username[:10])

    # Get the original filename without the extension and slugify it
    original_filename = os.path.splitext(filename)[0]
    slugified_filename = slugify(original_filename)

    # Generate a unique filename using the slugified username and a UUID
    unique_filename = f'{truncated_username}-{slugified_filename}-{uuid.uuid4()}'

    # Get the extension of the original filename
    ext = filename.split('.')[-1]

    # Combine the unique filename with the extension
    full_filename = f'{slugify(unique_filename)}.{ext}'

    # Return the complete path for the file
    return os.path.join('obrasteky', slugify(instance.user_profile.user.username), 'polozka', slugify(instance.nazov_produktu), full_filename)
    
class Polozka(models.Model):

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    nazov_produktu = models.CharField(max_length=100)
    info_nazov_produktu = models.CharField(max_length=255, default='')
    info_produktu = models.TextField(default='')
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nazov_produktu

    def is_available(self):
        """
        Checks if the product is available. If no associated availability, it's considered available.
        """
        try:
            # Attempt to fetch the associated availability
            availability = self.availability
            return availability.is_available()
        except Availability.DoesNotExist:
            # If no associated availability, the item is considered available
            return True

    def availability_status(self):
        """
        Returns a string indicating the availability status of the product.
        """
        # Check if the product is available
        if self.is_available():
            # If there's no associated availability, return "Available"
            try:
                availability = self.availability
            except Availability.DoesNotExist:
                return _("Available")
            
            today = timezone.now().date()
            current_year = today.year

            # Helper function to format the date using the custom Slovak month names
            def custom_date_format(date_obj):
                day = date_obj.day
                month = SLOVAK_MONTHS_SHORTENED[date_obj.strftime('%B')]
                year = ""
                if date_obj.year != current_year:
                    year = f" {date_obj.year}"
                return f"{day}. {month}{year}"

            # If the product is not available yet
            if availability.availability_start_date and availability.availability_start_date > today:
                return _("Available from: {}").format(custom_date_format(availability.availability_start_date))
            
            # If the product is already available
            elif availability.availability_end_date:
                return _("Available to: {}").format(custom_date_format(availability.availability_end_date))
            else:
                return _("Available")
        return _("Unavailable")

class AdditionalImage(models.Model):
    polozka = models.ForeignKey(Polozka, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return f"Additional Image for {self.polozka.nazov_produktu}"

class Availability(models.Model):
    """
    Model to handle the availability of a Polozka.
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    polozka = models.OneToOneField(Polozka, on_delete=models.CASCADE, related_name='availability')

    availability_start_date = models.DateField(blank=True, null=True)
    availability_end_date = models.DateField(blank=True, null=True)
    available_until_out_of_stock = models.BooleanField(default=False)
    stock_count = models.PositiveIntegerField(default=0)

    def is_available(self):
        """
        Checks if the product is available based on the date range and stock.
        """
        today = timezone.now().date()

        # If no availability information is set, the product is available
        if not self.availability_start_date and not self.availability_end_date and not self.available_until_out_of_stock:
            return True

        # If available until out of stock
        if self.available_until_out_of_stock:
            return self.stock_count > 0

        # If there's a start date but no end date
        if self.availability_start_date and not self.availability_end_date:
            return today >= self.availability_start_date
        
        # If there's an end date but no start date
        if not self.availability_start_date and self.availability_end_date:
            return today <= self.availability_end_date

        # If there's both start and end date
        if self.availability_start_date and self.availability_end_date:
            return self.availability_start_date <= today <= self.availability_end_date
        
        # Default: if none of the above conditions match, consider the product as not available
        return False

    def formatted_stock(self):
        """
        Returns the stock count in a formatted manner.
        If the stock count is more than 5, it returns "5+".
        Otherwise, it returns the actual stock count.
        """
        return "5+" if self.stock_count > 5 else str(self.stock_count)

class Transport(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    transport_type = models.CharField(max_length=100)
    transport_notes = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    unit = models.CharField(max_length=20)
    position = models.PositiveIntegerField(default=0)
    transport_name = models.CharField(max_length=100, blank=True)
  
    class Meta:
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.transport_name:
            # Generate a unique transport name using the user's username and a UUID
            username = self.user_profile.user.username
            unique_id = str(uuid.uuid4())[:8]  # Generate a random 8-character string
            slug = slugify(self.transport_type)[:50]  # Convert transport_type to a slug
            self.transport_name = f"{username}_{slug}_{unique_id}"
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.transport_name


class TransportLoc(models.Model):
    polozka = models.ForeignKey(Polozka, on_delete=models.CASCADE)

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    transport_type = models.CharField(max_length=100)
    transport_notes = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    unit = models.CharField(max_length=20)
    position = models.PositiveIntegerField(default=0)
    transport_name = models.CharField(max_length=100, blank=True)
  
    class Meta:
        ordering = ['position']

    def save(self, *args, **kwargs):
        if not self.transport_name:
            # Generate a unique transport name using the user's username and a UUID
            username = self.user_profile.user.username
            unique_id = str(uuid.uuid4())[:8]  # Generate a random 8-character string
            slug = slugify(self.transport_type)[:50]  # Convert transport_type to a slug
            self.transport_name = f"{username}_{slug}_{unique_id}"
        super().save(*args, **kwargs)  

    def __str__(self):
        return self.transport_name

class Cena(models.Model):

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    polozka = models.ForeignKey(Polozka, on_delete=models.CASCADE, related_name='ceny')
    amount = models.DecimalField(max_digits=20, decimal_places=5)
    unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

class PolozkaTransport(models.Model):
    polozka = models.ForeignKey(Polozka, on_delete=models.CASCADE)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE)

    def __str__(self):
        return f"Polozka: {self.polozka.nazov_produktu}, Transport: {self.transport.transport_name}"

