# email_verification/urls.py
from django.urls import path
from . import views
# from .views import send_verification_email, verify_email

urlpatterns = [
    path('send-verification-email/', views.send_verification_email, name='send_verification_email'),
    path('verify-email/<token>/', views.verify_email, name='verify_email'),
]
