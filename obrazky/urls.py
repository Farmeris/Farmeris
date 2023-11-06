from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from obrazky import views as obrazky_views

app_name = 'obrazky'

urlpatterns = [
    path('<str:username>/main-image/<str:nazov_produktu>/<str:filename>/', obrazky_views.obrazky, name='user_obrazky'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)