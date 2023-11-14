from django.core.signing import BadSignature, SignatureExpired, loads
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def email_verification_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the session indicates that the email has been verified
        if not request.session.get('email_verified'):
            # Redirect to send verification email view if not verified
            return redirect('send_verification_email')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
