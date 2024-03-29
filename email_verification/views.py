from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.signing import dumps, loads, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import render, redirect
from django.conf import settings
from django.template.loader import render_to_string
from . import views
from allauth.account.views import EmailView
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def send_verification_email(request):
    if request.method == 'GET':
        # Generate a unique token for the user
        token = dumps(request.user.pk)

        # Create a verification URL
        verify_url = request.build_absolute_uri(reverse('verify_email', args=[token]))

        # Render email body with a template
        message = render_to_string('email_verification/email_verification.txt', {
            'user': request.user,
            'verify_url': verify_url,
        })

        # Email subject and message
        subject = 'Verify Your Email Address'

        # Send email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=False)

        messages.success(request, 'A verification email has been sent to your current email address.')
        # Redirect to a page informing the user that a verification email has been sent
        return redirect('verification_email_sent')

    # This should probably be a GET request instead, showing a form or a button to send the email
    return render(request, 'email_verification/send_verification_email.html')

@login_required
def verify_email(request, token):
    try:
        user_pk = loads(token, max_age=3600)  # Token is valid for 1 hour
        if user_pk == request.user.pk:
            request.session['email_verified'] = True  # Set the session variable to bypass restrictions
            messages.success(request, 'Your email address has been verified.')
            return redirect('account_email')  # Redirect to the allauth email change form
    except (SignatureExpired, BadSignature) as e:
        messages.error(request, 'The verification link is invalid or has expired.')
        # Handle the error, e.g., by logging it or informing the user
        return redirect('send_verification_email')
    except Exception as e:
        # Handle any other exceptions
        return redirect('send_verification_email')

@login_required
def verification_email_sent(request):
    # You can simply render a template that shows the message
    context = {'email': request.user.email}
    return render(request, 'email_verification/verification_email_sent.html', context)

class CustomEmailView(LoginRequiredMixin, EmailView):
    def post(self, request, *args, **kwargs):
        # Perform the email change operation
        response = super().post(request, *args, **kwargs)

        # If the email has been changed and the email_verified session variable is set, clear it
        if 'email_verified' in request.session:
            request.session.pop('email_verified', None)
            messages.success(request, "Your email has been updated.")

        return response
