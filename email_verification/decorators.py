from django.core.signing import BadSignature, SignatureExpired, loads
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from allauth.account.models import EmailAddress

def email_verification_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get the user's primary email address or None if it doesn't exist
        user = request.user
        email_address = EmailAddress.objects.filter(user=user, primary=True).first()

        # If the user has no primary email or it's not verified, allow access
        if email_address is None or not email_address.verified:
            return view_func(request, *args, **kwargs)

        # Otherwise, the primary email is verified; show an error and redirect
        messages.error(request, "Your primary email is already verified.")
        return redirect('send_verification_email')
    return _wrapped_view
