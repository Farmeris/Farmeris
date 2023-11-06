from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponse
from login_app.models import UserProfile  
from django.contrib.auth.decorators import login_required, user_passes_test
from add_product_main.models import Polozka
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from .forms import AvatarForm
from add_product_main.utils import is_valid_image
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.db import transaction


from datetime import datetime
import pytz

@login_required
def profile_editing(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user__username=username)

    if request.user.username != username:
        return HttpResponseForbidden("You can't edit someone else's profile!")
    
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)

        # Check for changes and update messages accordingly
        if user_profile.website != request.POST.get('website', ''):
            user_profile.website = request.POST.get('website', '')
            messages.success(request, 'Website updated successfully!')
        if user_profile.social_media != request.POST.get('social-media', ''):
            user_profile.social_media = request.POST.get('social-media', '')
            messages.success(request, 'Social media link updated successfully!')
        if user_profile.phone_number != request.POST.get('phone-number', ''):
            user_profile.phone_number = request.POST.get('phone-number', '')
            messages.success(request, 'Phone number updated successfully!')
        if user_profile.languages != request.POST.get('languages', ''):
            user_profile.languages = request.POST.get('languages', '')
            messages.success(request, 'Languages updated successfully!')
        if user_profile.location != request.POST.get('location', ''):
            user_profile.location = request.POST.get('location', '')
            messages.success(request, 'Location updated successfully!')
        if user_profile.bio != request.POST.get('bio', ''):
            user_profile.bio = request.POST.get('bio', '')
            messages.success(request, 'Bio updated successfully!')
        # Handle avatar
        if 'avatar' in request.FILES:
            if form.is_valid():
                avatar = form.cleaned_data['avatar']
                valid_content_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
                if avatar.content_type in valid_content_types:
                    if is_valid_image(avatar):
                        user_profile.avatar = avatar
                        messages.success(request, 'Profile picture updated successfully!')
                    else:
                        form.add_error('avatar', 'Invalid image file.')
                else:
                    form.add_error('avatar', 'Unsupported file type.')
            else:
                pass

        # Handle Address fields
        if user_profile.street_address != request.POST.get('street-address', ''):
            user_profile.street_address = request.POST.get('street-address', '')
            messages.success(request, 'Street Address updated successfully!')
        if user_profile.city != request.POST.get('city', ''):
            user_profile.city = request.POST.get('city', '')
            messages.success(request, 'City updated successfully!')
        if user_profile.state_province != request.POST.get('state', ''):
            user_profile.state_province = request.POST.get('state', '')
            messages.success(request, 'State/Province updated successfully!')
        if user_profile.zip_postal_code != request.POST.get('zipcode', ''):
            user_profile.zip_postal_code = request.POST.get('zipcode', '')
            messages.success(request, 'Zip/Postal Code updated successfully!')
        if user_profile.country != request.POST.get('country', ''):
            user_profile.country = request.POST.get('country', '')
            messages.success(request, 'Country updated successfully!')
        
        with transaction.atomic():
            user_profile.save()

        messages.success(request, 'Address details updated successfully!')
        return redirect('edit_profile:user_profile_editing', username=username)

    else:
        form = AvatarForm()

    context = {
        'username': username,
        'user_profile': user_profile,
        'avatar_form': form,
    }
    return render(request, 'settings_edit.html', context)

