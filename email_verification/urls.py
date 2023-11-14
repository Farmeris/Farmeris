# email_verification/urls.py
from django.urls import path
from email_verification.views import send_verification_email, verify_email

urlpatterns = [
    path('send-verification-email/', views.send_verification_email, name='send_verification_email'),
    path('verify-email/<token>/', views.verify_email, name='verify_email'),
]
