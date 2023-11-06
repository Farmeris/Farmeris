from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from .models import UserProfile
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login as auth_login
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from allauth.socialaccount.providers.google.urls import urlpatterns as google_urlpatterns
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.helpers import complete_social_login
from allauth.account.views import ConfirmEmailView as DefaultConfirmEmailView
from allauth.account.utils import complete_signup
from allauth.account import app_settings
from django.http import HttpResponseRedirect
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import pytz

def handle_unverified_email(request):
    if request.method == "POST":
        decision = request.POST.get('decision')

        if decision == "create_with_google":
            # Delete the unverified email from the original account
            unverified_email = EmailAddress.objects.get(email=request.session['email'])
            User.objects.filter(email=unverified_email.email).delete()
            unverified_email.delete()

            # Continue with the creation of a new account using Google OAuth
            try:
                app = providers.registry.by_id(GoogleOAuth2Adapter.provider_id).get_app(request)
                token = SocialToken(app=app, token=request.session['social_token'])
                login = SocialLogin(request=request, account=SocialAccount(user=request.user, provider=GoogleOAuth2Adapter.provider_id, uid=request.session['uid'], extra_data=request.session['extra_data']), token=token)
                login.state = SocialLogin.state_from_request(request)
                ret = complete_social_login(request, login)
                return ret
            except (RequestTokenException, OAuth2Error):
                return redirect('account_login') # or your error handling view
    context = {
        
    }
    return render(request, 'socialaccount/handle_unverified_email_template.html', context)

class CustomConfirmEmailView(DefaultConfirmEmailView):
    def post(self, *args, **kwargs):
        response = super().post(*args, **kwargs)
        # Confirm the email and log in the user
        emailconfirmation = self.get_object()
        emailconfirmation.confirm(self.request)
        get_adapter().login(self.request, emailconfirmation.email_address.user)
        # Redirect to the default post signup/login page
        return HttpResponseRedirect(app_settings.LOGIN_REDIRECT_URL)

@login_required
def resend_confirmation_email(request):
    try:
        emailconfirmation = EmailConfirmation.objects.filter(email_address__user=request.user, sent__isnull=False).order_by('-sent')[0]
    except EmailConfirmation.DoesNotExist:
        return redirect('account_email')  # Redirect to a page where they can add a verified email

    if emailconfirmation:
        send_email_confirmation(request, emailconfirmation)
        # Display a message to the user indicating an email has been sent
    return redirect('main.html')  # Redirect to a suitable location, maybe account settings or home page

def mapka(request):
    username = request.user.username
    timezone = pytz.timezone('Europe/Bratislava')
    now = datetime.now().strftime("%d. %m. %H:%M:%S")
    context = {'username': username, 'now': now}
    return render(request, 'mapka.html', context)

def privacy_policy(request):

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    else:
        user_profile = None

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'privacy_policy.html', context)