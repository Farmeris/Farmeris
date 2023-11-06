from allauth.socialaccount.signals import pre_social_login
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress
from django.dispatch import receiver
from django.shortcuts import redirect

@receiver(pre_social_login)
def link_to_local_account(sender, request, sociallogin, **kwargs):
    email = sociallogin.account.extra_data['email']

    try:
        email_account = EmailAddress.objects.get(email=email)

        if email_account.verified:
            # The email is verified. Link Google account with this user.
            sociallogin.connect(request, email_account.user)
        else:
            # The email is not verified.
            request.session['email_exists_but_not_verified'] = True
            return redirect('handle_unverified_email')

    except EmailAddress.DoesNotExist:
        # The email does not exist in the system. This is a new account.
        pass