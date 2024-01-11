from django.core.signing import BadSignature, SignatureExpired, loads
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from allauth.account.models import EmailAddress
from django.contrib.auth.decorators import login_required

def email_verification_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the email_verified session variable is set
        if request.session.get('email_verified'):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You need to verify your email address to access this page.")
            return redirect('send_verification_email')
    return _wrapped_view
